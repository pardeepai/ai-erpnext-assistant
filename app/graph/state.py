from typing import TypedDict


class AgentState(TypedDict):
    customer: str
    sales_orders: dict
    order_counts: dict
    analysis: str
    reflection: str
    approved: bool
    iteration: int
    feedback: str
    lesson: str
    previous_attempts: list


class MultiAgentState(TypedDict):
    user_query: str
    customer_name: str | None

    customer_details: dict
    customer_contact: dict
    sales_order_data: dict

    route: str

    contact_response: str
    details_response: str
    sales_order_response: str
    final_response: str