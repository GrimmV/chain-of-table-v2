from operations.sort_column import get_sort_column_params
from transform_dataset import df2pipe

def sort_column_params(state):

    query = state["query"]
    table = state["table"]
    llm = state["llm"]
    caption = state["caption"]
    
    pipe_table = df2pipe(table, caption)
    
    response = get_sort_column_params(query, pipe_table, llm)
    
    state["next_operation_parameters"] = response
    
    return state