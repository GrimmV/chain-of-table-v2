from operations.select_row import select_row as selectrow

def select_row(state):
    
    table = state["table"]
    params = state["next_operation_parameters"]
    available_operations = state["available_operations"]
    operation_chain = state["operation_chain"]
    
    column = params["column"]
    operator = params["operator"]
    value = params["value"]
    
    new_table = selectrow(table, column, operator, value)
    
    state["table"] = new_table
    available_operations.remove("select_row")
    state["available_operations"] = available_operations
    state["operation_chain"].append({"func": "select_row", "params": params})
    state["operation_chain"] = operation_chain
    
    return state