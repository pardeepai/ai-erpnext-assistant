from langchain_ollama import ChatOllama
from app.graph.prompts import CUSTOMER_CONTACT_PROMPT


class ContactAgent:

    def __init__(self):
        self.llm = ChatOllama(
            model="qwen2.5:3b",
            temperature=0,
        )

    def contact_response(self, user_query, contact_data):
        messages = CUSTOMER_CONTACT_PROMPT.invoke({
            "user_query": user_query,
            "contact_data": contact_data,
        })
        print("Messages sent to LLM:",messages )

        response = self.llm.invoke(messages)

        return response.content.strip()