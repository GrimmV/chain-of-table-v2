from operations.add_column import get_add_column_parameters
from transform_dataset import df2pipe
from graph.GraphState import GraphState

def add_column_params(state: GraphState) -> GraphState:
    
    query = state["query"]
    table = state["table"]
    llm = state["llm"]
    caption = state["caption"]
    descriptions = state["column_descriptions"]
    columns = table.columns
    validation_context = {"columns": columns}
    
    pipe_table = df2pipe(table, caption)
    
    response = get_add_column_parameters(query, pipe_table, validation_context, llm, descriptions)
    
    state["next_operation_parameters"] = response
    descriptions[response["name"]] = response["description"]
    state["column_descriptions"] = descriptions
    
    return state