from utils.next_operations import possible_next_operations
from graph.GraphState import GraphState

def reset_state(state: GraphState) -> GraphState:
    
    state["available_operations"] = list(possible_next_operations.keys())
    state["operation_chain"] = []
    state["next_operation"] = "START"
    state["next_operation_parameters"] = {}
    state["column_descriptions"] = state["initial_column_descriptions"]
    
    return state