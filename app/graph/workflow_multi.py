from langgraph.graph import StateGraph, START, END

from app.graph.state import MultiAgentState as AgentState
from app.graph.edges import (
    route_request,
    route_after_details,
)
from app.graph.nodes import (
    extract_customer_node,
    supervisor_route_node,
    details_agent_node,
    contact_agent_node,
    final_response_node,
)


# Create the graph
graph = StateGraph(AgentState)


# Add nodes
graph.add_node("customer_name", extract_customer_node)
graph.add_node("route", supervisor_route_node)
graph.add_node("details_response", details_agent_node)
graph.add_node("contact_response", contact_agent_node)
graph.add_node("final_response", final_response_node)


# Normal edges
graph.add_edge(START, "customer_name")
graph.add_edge("customer_name", "route")
graph.add_edge("contact_response", "final_response")


# Conditional routing from supervisor
graph.add_conditional_edges(
    "route",
    route_request,
    {
        "contact_agent": "contact_response",
        "details_agent": "details_response",
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

# graph.add_conditional_edges(
#     "contact_response",
#     route_after_contact,
#     {
#         "final_response": "final_response",
#     },
# )


# Compile the graph
workflow = graph.compile()
print(workflow.get_graph().draw_mermaid())