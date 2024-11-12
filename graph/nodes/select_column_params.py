from operations.select_column import get_select_column_params
from transform_dataset import df2pipe
from graph.GraphState import GraphState

def select_column_params(state: GraphState) -> GraphState:
    
    query = state["query"]
    table = state["table"]
    llm = state["llm"]
    caption = state["caption"]
    descriptions = state["column_descriptions"]
    columns = table.columns
    validation_context = {"columns": columns}
    
    pipe_table = df2pipe(table, caption)
    
    response = get_select_column_params(query, pipe_table, validation_context, llm, descriptions)
    
    state["next_operation_parameters"] = response
    
    return state