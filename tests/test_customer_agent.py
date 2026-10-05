from app.erpnext.customer import CustomerService
from app.agents.customer_details_agent import CustomerDetailsAgent


def main():
    # Get customer data from ERPNext
    service = CustomerService()
    result = service.get_customers("sandeep", limit=10)

    print("\nERPNext Customer Data:")
    print(result)

    # Pass ERPNext data to Customer Agent
    agent = CustomerDetailsAgent()

    response = agent.customer_response(
        user_query="Show me the customer details",
        customer_data=result,
    )

    print("\nCustomer Agent Response:")
    print(response)


if __name__ == "__main__":
    main()