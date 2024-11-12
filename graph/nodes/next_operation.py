from get_next_operation import get_next_operation
from transform_dataset import df2pipe
from graph.GraphState import GraphState

def next_operation(state: GraphState) -> GraphState:
    
    # print(state["next_operation"])
    # print(state["table"])
    
    query = state["query"]
    table = state["table"]
    llm = state["llm"]
    caption = state["caption"]
    available_operations = state["available_operations"]
    
    pipe_table = df2pipe(table, caption)
    
    next_operation = get_next_operation(query, pipe_table, llm, available_operations)
    
    state["next_operation"] = next_operation
    state["available_operations"].remove(next_operation)
    
    return state