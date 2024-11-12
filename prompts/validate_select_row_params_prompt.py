def validate_select_row_params_prompt(condition, column, column_description):
    prompt = f"""You are given a table column and a filter operations. 
    Validate if the filter operation is sensible. 
    
    Either return the provided filter operation again or update the filter operation to make it sensible

    Snippet of the table column: \n{column}\n
    
    Column descriptions: \n{column_description}\n
    
    Filter condition to be applied: \n{condition}\n

    You are only allowed to use the following operators for number-values: '>=', '<=', '>', '<', '==', '!='
    You are only allowed to use the following operators for string-values: 'contains'
    
    Make sure that the filter condition is valid and respects the values and vocabular from the column of the given table. 
    The values need to match the format in the columns, otherwise the filtering will not work. Abreviations or 
    
    Output:
    """
    
    return prompt
