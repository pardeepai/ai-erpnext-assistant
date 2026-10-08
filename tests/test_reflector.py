from app.agents.reflector import SalesOrderReflector


reflector = SalesOrderReflector()

analysis = """
Customer: sandeep

Total Orders: 1
Completed Orders: 0
Pending Orders: 1
Cancelled Orders: 0

Observation:
The only order placed by the customer sandeep is currently
in Draft status.
"""

sales_orders = [
    {
        "name": "SAL-ORD-2026-00001",
        "customer": "sandeep",
        "status": "Draft",
    }
]

order_counts = {
    "total": 1,
    "completed": 0,
    "pending": 0,
    "cancelled": 0,
    "draft": 1,
    "to_deliver": 0,
}

result = reflector.reflect(
    analysis,
    sales_orders,
    order_counts,
)

print("Reflection:", result["reflection"])
print("Approved:", result["approved"])