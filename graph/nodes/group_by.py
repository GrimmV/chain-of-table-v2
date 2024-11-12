from operations.group_by import group_by as groupby
from graph.GraphState import GraphState

def group_by(state: GraphState) -> GraphState:
    
    table = state["table"]
    params = state["next_operation_parameters"]
    operation_chain = state["operation_chain"]
    
    column = params["column"]
    agg_function = params["agg_function"]
    
    print(table.head())
    
    new_table = groupby(table, column=column, agg_function=agg_function)
    
    state["table"] = new_table
    state["operation_chain"].append({"func": "group_by", "params": params})
    state["operation_chain"] = operation_chain
    
    return state