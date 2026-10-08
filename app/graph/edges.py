from debug.debug_graph import log_state


def should_continue(state):
    log_state(f"ROUTING DECISION: {state}", state)
    if state["approved"]:
        print("ROUTING DECISION: Approved, moving to END")
        return "approved"
    
    elif not state["approved"] and state["iteration"] < 3:
        print("ROUTING DECISION: Not approved, requesting feedback")
        return "feedback"
    
    elif not state["approved"] and state["iteration"] >= 3:
        print("ROUTING DECISION: Not approved, max iterations reached, moving to END")
        return "max_iterations"
    

def route_request(state):
    log_state(f"route_request: {state}", state)
    if state["route"] == "contact":
        print("ROUTING DECISION: Contact route, moving to contact agent")
        return "contact_agent"

    if state["route"] == "details":
        print("ROUTING DECISION: Details route, moving to details agent")
        return "details_agent"

    if state["route"] == "both":
        print("ROUTING DECISION: Both route, moving to details agent")
        return "details_agent"

    raise ValueError(f"Unknown route: {state['route']}")


def route_after_details(state):
    log_state(f"route_after_details: {state}", state)
    if state["route"] == "both":
        print("ROUTING DECISION: Both route, moving to contact agent")
        return "contact_agent"

    print("ROUTING DECISION: Details route completed, moving to final response")
    return "final_response"

# def route_after_contact(state):
#     log_state(f"route_after_contact: {state}", state)
#     if state["route"] == "both":
#         print("ROUTING DECISION: Both route completed, moving to final response")
#         return "final_response"

#     print("ROUTING DECISION: Contact route completed, moving to final response")
#     return "final_response"