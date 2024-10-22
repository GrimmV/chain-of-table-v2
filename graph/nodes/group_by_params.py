from operations.group_by import get_group_by_params
from transform_dataset import df2pipe

def group_by_params(state):
    
    query = state["query"]
    table = state["table"]
    llm = state["llm"]
    caption = state["caption"]
    
    pipe_table = df2pipe(table, caption)
    
    response = get_group_by_params(query, pipe_table, llm)
    
    state["next_operation_parameters"] = response
    
    return state