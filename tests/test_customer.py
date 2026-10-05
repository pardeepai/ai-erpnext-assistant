from app.erpnext.customer import CustomerService


service = CustomerService()

result = service.get_customers('sandeep',limit=10)
print(result)
