from app.agents.analyzer import SalesOrderAnalyzer
from app.agents.reflector import SalesOrderReflector
from app.agents.feedback import FeedbackAgent
from app.agents.lesson import LessonAgent
from app.graph.state import AgentState
from app.agents.customer_contact_agent import CustomerContactAgent
from app.agents.customer_details_agent import CustomerDetailsAgent
from app.agents.customer_supervisor import CustomerSupervisorAgent
from debug.debug_graph import log_state
from langchain_core.prompts import ChatPromptTemplate
from app.erpnext.customer import CustomerService
from app.erpnext.contact import ContactService


analyzer = SalesOrderAnalyzer()
reflector = SalesOrderReflector()
feedback = FeedbackAgent()
lesson = LessonAgent()

supervisor=CustomerSupervisorAgent()
details=CustomerDetailsAgent()
contact=CustomerContactAgent()
customer_service = CustomerService()
contact_service = ContactService()


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
    customer_name = supervisor.extract_customer_name(
        state["user_query"]
    )
    print(f"Extracted customer name: {customer_name}")
    
    if not customer_name:
        print('102: Customer name not found in the user query.')
        raise AssertionError("Customer is not available in ERPNext")

    customer_details = customer_service.get_customers(
        customer_name=customer_name
    )

    return {
        "customer_name": customer_name,
        "customer_details": customer_details
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
    customer_details = state["customer_details"]

    response = details.customer_response(
        user_query,
        customer_details
    )

    return {
        "details_response": response
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

def final_response_node(state):
    log_state(f"final_response_node: {state}", state)
    customer_name = state["customer_name"]

    print(state, "state in final response node")

    if state["route"] == "details":
        print("Generating final response for details route")

        customer_details = state["customer_details"]["data"][0]

        final_response = f"""**Customer Information:**

                - **Customer Name:** {customer_name}
                - **Customer Type:** {customer_details.get("customer_type") or "Not Provided"}
                - **Customer Group:** {customer_details.get("customer_group") or "Not Provided"}
                """

    elif state["route"] == "contact":
        print("Generating final response for contact route")

        customer_contact = state["customer_contact"]["data"][0]

        final_response = f"""**Customer Information:**

                - **Customer Name:** {customer_name}
                - **Phone Number:** {customer_contact.get("phone") or "Not Provided"}
                - **Email Address:** {customer_contact.get("email_id") or "Not Provided"}
                """

    elif state["route"] == "both":
        print("Generating final response for both route")

        customer_details = state["customer_details"]["data"][0]
        customer_contact = state["customer_contact"]["data"][0]

        final_response = f"""**Customer Information:**

                - **Customer Name:** {customer_name}
                - **Customer Type:** {customer_details.get("customer_type") or "Not Provided"}
                - **Customer Group:** {customer_details.get("customer_group") or "Not Provided"}
                - **Phone Number:** {customer_contact.get("phone") or "Not Provided"}
                - **Email Address:** {customer_contact.get("email_id") or "Not Provided"}
                """

    else:
        raise ValueError(f"Unknown route: {state['route']}")

    return {
        "final_response": final_response
    }