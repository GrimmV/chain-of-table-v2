from operations.select_row import get_select_row_params
from transform_dataset import df2pipe

def select_row_params(state):
    
    query = state["query"]
    table = state["table"]
    llm = state["llm"]
    caption = state["caption"]
    
    pipe_table = df2pipe(table, caption)
    
    response = get_select_row_params(query, pipe_table, llm)
    
    print(response)
    
    state["next_operation_parameters"] = response
    
    return state