from graph.GraphState import GraphState
from utils.check_numeric_column import check_numeric_column
from validation.validate_select_row_params import validate_select_row_params

def evaluate_select_row_params(state: GraphState) -> GraphState:
    
    table = state["table"]
    llm = state["llm"]
    conditions = state["next_operation_parameters"]
    descriptions = state["column_descriptions"]
    
    columns = table.columns
    column_type_dict = {}
    
    for column in columns:
        column_type_dict[column] = {"is_numeric": bool(check_numeric_column(table[column]))}
        
    validation_context = {"column_types": column_type_dict}
    
    print(f"initial conditions: {conditions}")
    new_conditions = []
    
    for condition in conditions:
        column = condition["column"]
        description = descriptions[column]
        column_snippet = table[column].head()
        
        updated_condition = validate_select_row_params(llm, condition, column_snippet, description, validation_context)
        
        print(f"updated condition: {updated_condition}")
        if (updated_condition != None):
            new_conditions.append(updated_condition)
    
    
    state["next_operation_parameters"] = new_conditions
    
    print(f"updated conditions: {new_conditions}")
    
    return state