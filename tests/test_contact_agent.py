from app.erpnext.contact import ContactService
from app.agents.customer_contact_agent import CustomerContactAgent



def main():
    # Get contact data from ERPNext
    service = ContactService()
    result = service.get_customer_contacts("sandeep", limit=10)
    contact_data = result["data"][0]

    print("\nERPNext Contact Data:")
    print(contact_data)

    # Pass ERPNext data to Contact Agent
    agent = CustomerContactAgent()

    response = agent.contact_response(
        user_query="Show me the contact details",
        contact_data=contact_data,
    )

    print("\nContact Agent Response:")
    print(response)


if __name__ == "__main__":
    main()