from utils.next_operations import possible_next_operations

def reset_state(state):
    
    state["available_operations"] = list(possible_next_operations)
    state["operation_chain"] = []
    state["next_operation"] = "START"
    state["next_operation_parameters"] = {}
    
    return state