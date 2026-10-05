from langchain_ollama import ChatOllama
from app.graph.prompts import CUSTOMER_PROMPT


class CustomerAgent:

    def __init__(self):
        self.llm = ChatOllama(
            model="qwen2.5:3b",
            temperature=0,
        )

    def customer_response(self, user_query, customer_data):
        messages = CUSTOMER_PROMPT.invoke({
            "user_query": user_query,
            "customer_data": customer_data,
        })
        print("Messages sent to LLM:",messages )

        response = self.llm.invoke(messages)

        return response.content.strip()