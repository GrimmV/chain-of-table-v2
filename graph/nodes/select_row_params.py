from operations.select_row import get_select_row_params
from transform_dataset import df2pipe
from utils.check_numeric_column import check_numeric_column
from graph.GraphState import GraphState

def select_row_params(state: GraphState) -> GraphState:
    
    query = state["query"]
    table = state["table"]
    llm = state["llm"]
    caption = state["caption"]
    descriptions = state["column_descriptions"]
    
    pipe_table = df2pipe(table, caption)
    columns = table.columns
    column_type_dict = {}
    
    for column in columns:
        column_type_dict[column] = {"is_numeric": bool(check_numeric_column(table[column]))}
        
    validation_context = {"column_types": column_type_dict}
    
    response = get_select_row_params(query, pipe_table, validation_context, llm, descriptions)
    
    state["next_operation_parameters"] = response
    
    return state