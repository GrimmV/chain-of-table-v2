from operations.select_column import select_column as selectcolumn

def select_column(state):
    
    table = state["table"]
    params = state["next_operation_parameters"]
    available_operations = state["available_operations"]
    operation_chain = state["operation_chain"]
    
    columns = params["columns"]
    
    new_table = selectcolumn(table, columns)
    
    state["table"] = new_table
    available_operations.remove("select_column")
    state["available_operations"] = available_operations
    state["operation_chain"].append({"func": "select_column", "params": params})
    state["operation_chain"] = operation_chain
    
    return state