from app.erpnext.contact import ContactService



service = ContactService()

result = service.get_customer_contacts('sandeep', limit=10)
print(result)
