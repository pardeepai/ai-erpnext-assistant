from app.erpnext.contact import ContactService
from app.erpnext.customer import CustomerService

from app.agents.customer_supervisor import CustomerSupervisorAgent
from app.agents.customer_contact_agent import CustomerContactAgent
from app.agents.customer_details_agent import CustomerDetailsAgent


def main(user_query):

    # Initialize agents/services
    supervisor_agent = CustomerSupervisorAgent()
    contact_service = ContactService()
    customer_service = CustomerService()

    # --------------------------------------------------
    # Step 1: Extract customer name
    # --------------------------------------------------

    customer_name = supervisor_agent.extract_customer_name(user_query)

    print("\nExtracted Customer:")
    print(customer_name)

    # --------------------------------------------------
    # Step 2: Supervisor decides the route
    # --------------------------------------------------

    route = supervisor_agent.supervisor_route(
        user_query=user_query,
    )

    print("\nSupervisor Route:")
    print(route)

    # --------------------------------------------------
    # Step 3: Contact route
    # --------------------------------------------------

    if route == "contact":

        result = contact_service.get_customer_contacts(
            customer_name,
            limit=10
        )

        contact_data = result["data"][0]

        print("\nERPNext Contact Data:")
        print(contact_data)

        contact_agent = CustomerContactAgent()

        response = contact_agent.contact_response(
            user_query=user_query,
            contact_data=contact_data,
        )

        print("\nContact Agent Response:")
        print(response)

    # --------------------------------------------------
    # Step 4: Details route
    # --------------------------------------------------

    elif route == "details":

        result = customer_service.get_customers(
            customer_name,
            limit=10
        )

        customer_data = result["data"][0]

        print("\nERPNext Customer Data:")
        print(customer_data)

        details_agent = CustomerDetailsAgent()

        
        response = details_agent.customer_response(
            user_query=user_query,
            customer_data=customer_data,
    )

        print("\nCustomer Details Agent Response:")
        print(response)

    else:
        print("\nRoute not handled yet:", route)


if __name__ == "__main__":

    user_query = "Show me customer sandeep customer group"

    main(user_query)