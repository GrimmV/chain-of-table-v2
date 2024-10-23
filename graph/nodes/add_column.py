from operations.add_column import add_column as add_col

def add_column(state):
    
    table = state["table"]
    params = state["next_operation_parameters"]
    llm = state["llm"]
    operation_chain = state["operation_chain"]
    
    name = params["name"]
    
    new_table = add_col(table, name, llm)
    
    state["table"] = new_table
    state["operation_chain"].append({"func": "add_column", "params": params})
    state["operation_chain"] = operation_chain
    
    return state