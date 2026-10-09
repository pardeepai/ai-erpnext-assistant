from app.erpnext.sales_order import SalesOrderService
from app.agents.sales_order_agent import SalesOrderAgent


def main():
    # Get sales order data from ERPNext
    service = SalesOrderService()
    result = service.get_sales_orders("sandeep")

    print("\nERPNext Sales Order Data:")
    print(result)

    # Pass ERPNext data to Sales Order Agent
    agent = SalesOrderAgent()

    response = agent.sales_order_response(
        #user_query="Show me Sandeep's sales orders",
        user_query="Show me Sandeep's Draft orders",
        sales_data=result,
    )

    print("\nSales Order Agent Response:")
    print(response)


if __name__ == "__main__":
    main()