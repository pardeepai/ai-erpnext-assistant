from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate


class SalesOrderAgent:

    def __init__(self):
        self.llm = ChatOllama(
            model="qwen2.5:3b",
            temperature=0,
        )
        
        
    
    
    def extract_sales_order_status(self, user_query):
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """Extract the sales order status from the user's request.

                Valid sales order statuses:
                - Draft
                - To Deliver
                - To Deliver and Bill
                - To Bill
                - Completed
                - Cancelled
                - On Hold
                -Closed

                Known rejected statuses:
                - Started
                - Marked
                -Overdue

                Rules:
                - Return the exact valid status name if requested.
                - Return NONE if no specific status is requested.
                - If a known rejected status is explicitly requested,
                return INVALID: followed by the requested status.
                - If a status is neither valid nor in the rejected list,
                return NONE.
                - Do not return the customer name.
                - Do not guess or map statuses to other statuses.

                Examples:
                - "Show Sandeep draft sales orders" -> Draft
                - "Show completed sales orders" -> Completed
                - "Show orders to deliver" -> To Deliver
                - "Show all Sandeep sales orders" -> NONE
                - "Show only Started sales orders for Sandeep"
                -> INVALID: Started
                - "Show Marked sales orders for Sandeep"
                -> INVALID: Marked"""
            ),
            ("human", "{user_query}")
        ])

        chain = prompt | self.llm
        response = chain.invoke({"user_query": user_query})

        raw_status = response.content.strip()

        print("SALES ORDER STATUS EXTRACTOR RESPONSE:", raw_status)

        # 1. Handle NONE response
        if raw_status.casefold() == "none":
            query = user_query.casefold()
            for status in VALID_SALES_ORDER_STATUSES.values():
                if status.casefold() in query:
                    return {
                        "status": status,
                        "error": None,
                    }

            return {
                "status": None,
                "error": None,
    }

        # 2. Handle explicitly rejected statuses
        # 2. Handle INVALID responses safely
        if raw_status.casefold().startswith("invalid:"):
            rejected_status = raw_status.split(":", 1)[1].strip()
            normalized_status = rejected_status.casefold()

            # Protect valid statuses from incorrect LLM classification
            valid_status = VALID_SALES_ORDER_STATUSES.get(normalized_status)

            if valid_status is not None:
                return {
                    "status": valid_status,
                    "error": None,
                }

            # Reject explicitly unsupported statuses
            if normalized_status in REJECTED_SALES_ORDER_STATUSES:
                return {
                    "status": None,
                    "error": f"Unsupported sales order status: {rejected_status}",
                }

            # Handle other unexpected INVALID responses
            return {
                "status": None,
                "error": (
                    f"Unable to validate requested sales order status: "
                    f"{rejected_status}"
                ),
            }

        # 3. Validate and normalize supported statuses
        valid_status = VALID_SALES_ORDER_STATUSES.get(
            raw_status.casefold()
        )

        if valid_status is not None:
            return {
                "status": valid_status,
                "error": None,
            }

        # 4. Unexpected extractor output: do not silently ignore it
        return {
            "status": None,
            "error": (
                "Unable to interpret the requested sales order status."
            ),
        }

    
    def sales_order_response(self, user_query, sales_order_data):
        orders = sales_order_data.get("data", [])

        if not orders:
            return "No sales orders found for this customer."

        lines = [
            "| Sales Order ID | Customer | Order Status |",
            "|---|---|---|",
        ]

        for order in orders:
            order_id = order.get("name") or "Not Provided"
            customer = order.get("customer") or "Not Provided"
            status = order.get("status") or "Not Provided"

            lines.append(
                f"| {order_id} | {customer} | {status} |"
            )

        return "**Sales Orders:**\n\n" + "\n".join(lines)




VALID_SALES_ORDER_STATUSES = {
    "draft": "Draft",
    "to deliver": "To Deliver",
    "to deliver and bill": "To Deliver and Bill",
    "to bill": "To Bill",
    "completed": "Completed",
    "cancelled": "Cancelled",
    "closed": "Closed",
    "on hold": "On Hold",
}

REJECTED_SALES_ORDER_STATUSES = {
    "started",
    "marked",
}