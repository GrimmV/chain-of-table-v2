from operations.select_column import select_column as selectcolumn
from graph.GraphState import GraphState

def select_column(state: GraphState) -> GraphState:
    
    table = state["table"]
    params = state["next_operation_parameters"]
    operation_chain = state["operation_chain"]
    
    columns = params["columns"]
    
    new_table = selectcolumn(table, columns)
    
    state["table"] = new_table
    state["operation_chain"].append({"func": "select_column", "params": params})
    state["operation_chain"] = operation_chain
    
    return state