from langchain_ollama import ChatOllama
from app.graph.prompts import SUPERVISOR_PROMPT
from langchain_core.prompts import ChatPromptTemplate

class CustomerSupervisorAgent:

    def __init__(self):
        self.llm = ChatOllama(
            model="qwen2.5:3b",
            temperature=0,
        )

    def extract_customer_name(self, user_query):
        prompt = ChatPromptTemplate.from_messages([
                (
                    "system",
                    """Extract the customer name from the user's request.

                                The customer name is usually the person's or company's name mentioned
                                in the request.

                                Examples:
                                - "Show me sandeep customer group" → sandeep
                                - "Show me sandeep phone number" → sandeep
                                - "Give me sandeep email" → sandeep
                                - "Show me sandeep customer group and phone number" → sandeep

                                Rules:
                                - Return ONLY the customer name.
                                - Never return None if a customer name is present in the request.
                                - Do not return words such as customer, phone, email, group, details, number.
                                - If there is genuinely no customer name, return None."""
                ),
                ("human", "{user_query}")
            ])
        
        chain = prompt | self.llm
        response = chain.invoke({
            "user_query": user_query
        })
        
        print("CUSTOMER EXTRACTOR RESPONSE:", response.content)
        customer_name = response.content.strip()
        if customer_name.lower() == "none":
            return None
        
        return customer_name
    
    def supervisor_route(self, user_query):

        messages = SUPERVISOR_PROMPT.invoke({
            "user_query": user_query,
        })

        print("Messages sent to LLM:", messages)

        response = self.llm.invoke(messages)

        return response.content.strip()