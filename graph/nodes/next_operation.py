from get_next_operation import get_next_operation
from transform_dataset import df2pipe

def next_operation(state):
    
    query = state["query"]
    table = state["table"]
    llm = state["llm"]
    caption = state["caption"]
    
    pipe_table = df2pipe(table, caption)
    
    return get_next_operation(query, pipe_table, llm)