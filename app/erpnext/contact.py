import json
from app.erpnext.client import ERPNextClient


class ContactService:

    def __init__(self):
        self.client = ERPNextClient()

    def get_customer_contacts(self, customer_name, limit=10):
        """
        Retrieves phone and email_id for contacts linked to a specific Customer.
        Filters out records with missing phone or email numbers.
        """
        filters = [
            ["Dynamic Link", "link_doctype", "=", "Customer"],
            ["Dynamic Link", "link_name", "=", customer_name],
            ["Contact", "phone", "!=", ""],
            ["Contact", "email_id", "!=", ""],
        ]

        params = {
            "fields": json.dumps(["phone", "email_id"]),
            "filters": json.dumps(filters),
            "limit_page_length": limit,
        }

        return self.client.get("/api/resource/Contact", params=params)