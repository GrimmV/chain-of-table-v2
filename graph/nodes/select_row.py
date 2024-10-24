from operations.select_row import select_row as selectrow

def select_row(state):
    
    table = state["table"]
    params = state["next_operation_parameters"]
    operation_chain = state["operation_chain"]
    
    conditions = params
    
    new_table = selectrow(table, conditions)
    
    state["table"] = new_table
    state["operation_chain"].append({"func": "select_row", "params": params})
    state["operation_chain"] = operation_chain
    
    return state