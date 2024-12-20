from operations.add_column import add_column as add_col
from graph.GraphState import GraphState

def add_column(state: GraphState) -> GraphState:
    
    table = state["table"]
    params = state["next_operation_parameters"]
    llm = state["llm"]
    operation_chain = state["operation_chain"]
    descriptions = state["column_descriptions"]
    
    name = params["name"]
    description = descriptions[name]
    
    new_table = add_col(table, name, description, llm)
    
    state["table"] = new_table
    state["operation_chain"].append({"func": "add_column", "params": params})
    state["operation_chain"] = operation_chain
    
    return state