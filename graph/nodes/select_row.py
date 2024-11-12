from operations.select_row import select_row as selectrow
from graph.GraphState import GraphState

def select_row(state: GraphState) -> GraphState:
    
    table = state["table"]
    params = state["next_operation_parameters"]
    operation_chain = state["operation_chain"]
    
    conditions = params
    
    new_table = selectrow(table, conditions)
    
    state["table"] = new_table
    operation_chain.append({"func": "select_row", "params": params})
    state["operation_chain"] = operation_chain
    state["available_operations"]
    
    return state