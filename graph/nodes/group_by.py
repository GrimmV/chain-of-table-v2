from operations.group_by import group_by as groupby

def group_by(state):
    
    table = state["table"]
    params = state["next_operation_parameters"]
    available_operations = state["available_operations"]
    operation_chain = state["operation_chain"]
    
    column = params["column"]
    agg_function = params["agg_function"]
    
    new_table = groupby(table, column=column, agg_function=agg_function)
    
    state["table"] = new_table
    available_operations.remove("group_by")
    state["available_operations"] = available_operations
    state["operation_chain"].append({"func": "group_by", "params": params})
    state["operation_chain"] = operation_chain
    
    return state