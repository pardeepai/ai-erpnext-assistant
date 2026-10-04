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