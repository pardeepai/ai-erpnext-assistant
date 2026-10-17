
from langgraph.graph import StateGraph, START, END

from app.graph.state import MultiAgentState as AgentState
from app.graph.edges import (
    route_request,
    route_after_details,
    route_after_sales_order,
    route_after_customer_extraction,
)
from app.graph.nodes import (
    extract_customer_node,
    supervisor_route_node,
    details_agent_node,
    contact_agent_node,
    retrieve_sales_orders_node,
    sales_order_agent_node,
    final_response_node,
)

# Create the graph
graph = StateGraph(AgentState)

# Add nodes
graph.add_node("customer_name", extract_customer_node)
graph.add_node("route", supervisor_route_node)
graph.add_node("details_response", details_agent_node)
graph.add_node("contact_response", contact_agent_node)
graph.add_node("sales_order_data", retrieve_sales_orders_node)
graph.add_node("sales_order_response", sales_order_agent_node)
graph.add_node("final_response", final_response_node)

# Normal edges
graph.add_edge(START, "customer_name")

graph.add_edge("contact_response", "final_response")
graph.add_edge("sales_order_data", "sales_order_response")

graph.add_edge("final_response", END)

# Conditional routing from supervisor
graph.add_conditional_edges(
    "route",
    route_request,
    {
        "contact_agent": "contact_response",
        "details_agent": "details_response",
        "sales_order_agent": "sales_order_data",
    },
)

# Conditional routing after Details Agent
graph.add_conditional_edges(
    "details_response",
    route_after_details,
    {
        "contact_agent": "contact_response",
        "final_response": "final_response",
    },
)


graph.add_conditional_edges(
    "sales_order_response",
    route_after_sales_order,
    {
        "contact_agent": "contact_response",
        "details_agent": "details_response",
        "final_response": "final_response",
    },
)


graph.add_conditional_edges(
    "customer_name",
    route_after_customer_extraction,
    {
        "error": "final_response",
        "customer_not_found": "final_response",
        "continue": "route",
    },
)


# Compile the graph
workflow = graph.compile()

print(workflow.get_graph().draw_mermaid())
