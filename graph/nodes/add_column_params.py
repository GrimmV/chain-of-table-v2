from operations.add_column import get_add_column_parameters
from transform_dataset import df2pipe

def add_column_params(state):
    
    query = state["query"]
    table = state["table"]
    llm = state["llm"]
    caption = state["caption"]
    
    pipe_table = df2pipe(table, caption)
    
    response = get_add_column_parameters(query, pipe_table, llm)
    
    state["next_operation_parameters"] = response
    
    return state