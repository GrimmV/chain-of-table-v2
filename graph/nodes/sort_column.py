from operations.sort_column import sort_column as sortcolumn

def sort_column(state):
    
    table = state["table"]
    params = state["next_operation_parameters"]
    available_operations = state["available_operations"]
    operation_chain = state["operation_chain"]
    
    column = params["column"]
    order = params["order"]
    
    new_table = sortcolumn(table, column, order)
    
    state["table"] = new_table
    available_operations.remove("sort_column")
    state["available_operations"] = available_operations
    operation_chain.append({"func": "sort_column", "params": params})
    state["operation_chain"] = operation_chain
    
    return state