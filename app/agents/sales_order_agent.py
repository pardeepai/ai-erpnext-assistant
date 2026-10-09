from langchain_ollama import ChatOllama
from app.graph.prompts import SALES_ORDER_PROMPT
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

                Valid sales order statuses include:
                - Draft
                - To Deliver
                - To Deliver and Bill
                - To Bill
                - Completed
                - Cancelled
                - Closed

                Examples:
                - "Show me sandeep draft sales orders" → Draft
                - "Show me completed sales orders" → Completed
                - "Show me sandeep orders to deliver" → To Deliver
                - "Show me orders that are waiting for delivery" → To Deliver
                - "Show me sandeep orders to deliver and bill" → To Deliver and Bill
                - "Show me all sandeep sales orders" → None
                - "Show me sandeep customer group" → None

                Rules:
                - Return ONLY one valid status from the list above.
                - If no specific sales order status is requested, return None.
                - Do not return the customer name.
                - Do not invent or guess a status.
                - Match the status to the user's actual request."""
            ),
            ("human", "{user_query}")
        ])
        
        
        chain = prompt | self.llm
        response = chain.invoke({
            "user_query": user_query
    })
        
        
        print("SALES ORDER STATUS EXTRACTOR RESPONSE:", response.content)
        status = response.content.strip()
        if status.lower() == "none":
            return None
        
        return status

    def sales_order_response(self, user_query, sales_data):
        messages = SALES_ORDER_PROMPT.invoke({
            "user_query": user_query,
            "sales_data": sales_data,
        })
        print("Messages sent to LLM:",messages )

        response = self.llm.invoke(messages)

        return response.content.strip()