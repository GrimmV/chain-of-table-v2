from operations.add_column import add_column as add_col

def add_column(state):
    
    table = state["table"]
    params = state["next_operation_parameters"]
    llm = state["llm"]
    available_operations = state["available_operations"]
    operation_chain = state["operation_chain"]
    
    name = params["name"]
    
    new_table = add_col(table, name, llm)
    
    state["table"] = new_table
    available_operations.remove("add_column")
    state["available_operations"] = available_operations
    state["operation_chain"].append({"func": "add_column", "params": params})
    state["operation_chain"] = operation_chain
    
    return state