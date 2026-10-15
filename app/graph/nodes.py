from app.agents.analyzer import SalesOrderAnalyzer
from app.agents.reflector import SalesOrderReflector
from app.agents.feedback import FeedbackAgent
from app.agents.lesson import LessonAgent
from app.graph.state import AgentState
from app.agents.customer_contact_agent import CustomerContactAgent
from app.agents.customer_details_agent import CustomerDetailsAgent
from app.agents.customer_supervisor import CustomerSupervisorAgent
from app.agents.sales_order_agent import SalesOrderAgent
from debug.debug_graph import log_state
from langchain_core.prompts import ChatPromptTemplate
from app.erpnext.customer import CustomerService
from app.erpnext.sales_order import SalesOrderService
from app.erpnext.contact import ContactService
import logging

logger = logging.getLogger(__name__)


analyzer = SalesOrderAnalyzer()
reflector = SalesOrderReflector()
feedback = FeedbackAgent()
lesson = LessonAgent()

supervisor=CustomerSupervisorAgent()
details=CustomerDetailsAgent()
contact=CustomerContactAgent()
customer_service = CustomerService()
contact_service = ContactService()
sales_order_agent= SalesOrderAgent()
sales_services=SalesOrderService()


def analyzer_node(state: AgentState):
    analyzer_result = analyzer.analyze(
        state["customer"],
        state["sales_orders"],
        state["order_counts"],
        state["feedback"],
        state["lesson"],
        state["previous_attempts"],
    )

    log_state("AFTER ANALYZER", state)

    return {
        **state,
        "analysis": analyzer_result,
        "iteration": state["iteration"] + 1,
    }

def reflector_node(state: AgentState):
    result =reflector.reflect(
        state["analysis"],
        state["sales_orders"],
        state["order_counts"]
)
    
    log_state("AFTER REFLECTOR", state)

    return {
        **state,
        "reflection": result["reflection"],
        "approved": result["approved"],
    }


def feedback_node(state: AgentState):
    feedback_result = feedback.generate_feedback(
        state["reflection"]
    )
    
    log_state(f"After FEEDBACK: {feedback_result}", state)

    return {
        **state,
        "feedback": feedback_result,
    }


def lesson_node(state: AgentState):
    lesson_result = lesson.generate_lesson(
        state["reflection"],
        state["feedback"],
    )

    previous_attempts = state["previous_attempts"]
    
    previous_attempts.append({
        "answer": state["analysis"],
        "critique": state["reflection"],
        "feedback": state["feedback"],
        "lesson": lesson_result,
    })
    
    log_state(f"After LESSON: {lesson_result}", state)
    
    return {
        **state,
        "lesson": lesson_result,
        "previous_attempts": previous_attempts,
    }

#----------------Multi Agent Nodes-------------------

def extract_customer_node(state):
    log_state(f"extract_customer_node: {state}", state)

    # Step 1: Extract customer name from the user query.
    customer_name = supervisor.extract_customer_name(
        state["user_query"]
    )
    print(f"Extracted customer name: {customer_name}")

    if not customer_name:
        return {
            "customer_name": None,
            "customer_found": False,
        }

    # Step 2: Verify customer exists in ERPNext.
    customer_found = customer_service.verify_customer_exists(
        customer_name=customer_name
    )
    print(f"Customer found in ERPNext: {customer_found}")

    # Step 3: Stop if customer does not exist.
    if not customer_found:
        return {
            "customer_name": customer_name,
            "customer_found": False,
        }

    # Step 4: Continue workflow for a valid customer.
    return {
        "customer_name": customer_name,
        "customer_found": True,
    }


def supervisor_route_node(state):

    route = supervisor.supervisor_route(
        state["user_query"]
    )

    return {
        "route": route
    }

def details_agent_node(state):
    log_state(f"details_agent_node: {state}", state)
    user_query = state["user_query"]
    customer_name = state["customer_name"]
    customer_details = customer_service.get_customers(
        customer_name=customer_name
    )

    response = details.customer_response(
        user_query,
        customer_details
    )

    return {
        "details_response": response,
        "customer_details": customer_details,
    }
    

def contact_agent_node(state):
    log_state(f"contact_agent_node: {state}", state)
    user_query = state["user_query"]
    customer_name = state["customer_name"]

    customer_contact = contact_service.get_customer_contacts(
        customer_name=customer_name
    )

    response = contact.contact_response(
        user_query,
        customer_contact
    )

    return {
        "customer_contact": customer_contact,
        "contact_response": response
    }



def sales_order_agent_node(state):
    log_state(f"sales_order_agent_node: {state}", state)

    user_query = state["user_query"]
    sales_order_data = state["sales_order_data"]
    
    response = sales_order_agent.sales_order_response(
        user_query,
        sales_order_data
    )

    return {
        "sales_order_response": response
    }





def retrieve_sales_orders_node(state):
    log_state("retrieve_sales_orders_node started", state)

    user_query = state["user_query"]
    customer_name = state["customer_name"]

    if not customer_name:
        return {
            "sales_order_data": {"data": []},
            "sales_order_error": "Customer name is required.",
        }

    try:
        status_result = sales_order_agent.extract_sales_order_status(
            user_query
        )

        # 1. Handle status validation errors before the API call.
        if isinstance(status_result, dict) and status_result.get("error"):
            error = status_result["error"]

            print("Sales order status validation error:", error)

            return {
                "sales_order_data": {"data": []},
                "sales_order_error": error,
            }

        # 2. Extract the status string.
        if isinstance(status_result, dict):
            status = status_result.get("status")
        else:
            # Backward compatibility with an extractor returning None
            # or a status string directly.
            status = status_result

        print("Extracted status:", status)

        # 3. Retrieve sales orders from ERPNext.
        orders = sales_services.get_sales_orders(
            customer_name,
            status=status,
            limit=10,
        )

        print("Retrieved sales orders:", orders)

        # 4. Validate the response structure, not the number of orders.
        if not isinstance(orders, dict) or "data" not in orders:
            raise ValueError(
                "Invalid sales order response from the service."
            )

        log_state(
            "sales_order_status_extracted",
            {
                "user_query": user_query,
                "extracted_status": status,
            },
        )

        log_state(
            "sales_order_data_retrieved",
            {
                "user_query": user_query,
                "sales_order_data": orders,
            },
        )

        # An empty data list is a valid result.
        return {
            "sales_order_data": orders,
            "sales_order_error": None,
        }

    except Exception:
        logger.exception(
            "Failed to retrieve sales orders for customer: %s",
            customer_name,
        )

        return {
            "sales_order_data": {"data": []},
            "sales_order_error": (
                "Unable to retrieve sales orders right now. "
                "Please try again later."
            ),
        }


def get_first_record(state, key):
    """Safely return the first record or an empty dictionary."""
    data = (state.get(key) or {}).get("data") or []
    return data[0] if data else {}


def get_sales_order_response(state, customer_name):
    """Return sales-order response or a fallback message."""
    return state.get("sales_order_response") or (
        f"No sales order response was generated for {customer_name}."
    )


def format_customer_details(customer_name, customer_details):
    """Format basic customer information."""
    customer_type = customer_details.get("customer_type") or "Not Available"
    customer_group = customer_details.get("customer_group") or "Not Available"

    return f"""**Customer Information:**

- **Customer Name:** {customer_name}
- **Customer Type:** {customer_type}
- **Customer Group:** {customer_group}"""


def format_customer_contact(customer_name, customer_contact):
    """Format customer contact information."""
    phone = customer_contact.get("phone") or "Not Available"
    email = customer_contact.get("email_id") or "Not Available"

    return f"""**Customer Information:**

- **Customer Name:** {customer_name}
- **Phone Number:** {phone}
- **Email Address:** {email}"""


def format_all_customer_info(
    customer_name, customer_details, customer_contact
):
    """Format customer details and contact information."""
    customer_type = customer_details.get("customer_type") or "Not Available"
    customer_group = customer_details.get("customer_group") or "Not Available"
    phone = customer_contact.get("phone") or "Not Available"
    email = customer_contact.get("email_id") or "Not Available"

    return f"""**Customer Information:**

- **Customer Name:** {customer_name}
- **Customer Type:** {customer_type}
- **Customer Group:** {customer_group}
- **Phone Number:** {phone}
- **Email Address:** {email}"""


def append_sales_orders(customer_info, sales_order_response):
    """Append sales-order information to customer information."""
    return f"""{customer_info}



{sales_order_response}"""


def final_response_node(state):
    """Coordinate final response generation."""
    log_state(f"final_response_node: {state}", state)

    customer_name = state.get("customer_name") or "Unknown Customer"
    route = state.get("route")
    if state.get("customer_found") is False:
        return {
        "final_response": (
            f"Customer '{customer_name}' was not found in ERPNext."
        )
    }
    
    
    if state.get("sales_order_error"):
        return {
            "final_response": (
                f"Error retrieving sales orders for {customer_name}: "
                f"{state['sales_order_error']}"
            )
        }

    customer_details = get_first_record(state, "customer_details")
    customer_contact = get_first_record(state, "customer_contact")
    sales_orders = get_sales_order_response(state, customer_name)

    if route == "details":
        response = format_customer_details(
            customer_name, customer_details
        )

    elif route == "contact":
        response = format_customer_contact(
            customer_name, customer_contact
        )

    elif route == "both":
        response = format_all_customer_info(
            customer_name, customer_details, customer_contact
        )

    elif route == "sales_order":
        response = sales_orders

    elif route == "details_and_sales_order":
        customer_info = format_customer_details(
            customer_name, customer_details
        )
        response = append_sales_orders(customer_info, sales_orders)

    elif route == "contact_and_sales_order":
        customer_info = format_customer_contact(
            customer_name, customer_contact
        )
        response = append_sales_orders(customer_info, sales_orders)

    elif route == "all":
        customer_info = format_all_customer_info(
            customer_name, customer_details, customer_contact
        )
        response = append_sales_orders(customer_info, sales_orders)

    else:
        raise ValueError(f"Unknown route: {route}")

    print("Final response generated:", response)

    return {"final_response": response}