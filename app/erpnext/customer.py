from app.erpnext.client import ERPNextClient

import json


class CustomerService:

    def __init__(self):
        self.client = ERPNextClient()

    def get_customers(self, customer_name=None, limit=10):
        filters = []
        if customer_name:
            # Use 'like' for flexible search (e.g., searching "Acme" matches "Acme Corp")
            filters.append(["customer_name", "like", f"%{customer_name}%"])

        params = {
            # ERPNext expects fields as a JSON-encoded list string
            "fields": json.dumps(
                ["name", "customer_name", "customer_group", "territory", "customer_type","mobile_no", "email_id"]
            ),
            "limit_page_length": limit,
        }

        if filters:
            params["filters"] = json.dumps(filters)

        return self.client.get("/api/resource/Customer", params=params)