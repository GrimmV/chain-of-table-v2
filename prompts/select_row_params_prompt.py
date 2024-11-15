def select_row_params_prompt(query, table, column_descriptions):
    prompt = f"""You are given a snippet of a table and a user query. Based on the user's query, 
    provide filter conditions that include the column name, operator, and value to compare.

    Snippet of the table: \n{table}\n
    
    Column descriptions: \n{column_descriptions}\n

    User Query: {query}

    User Query Example:
    "Select the rows where the status is 'active'."

    Expected Output:

    Column: status
    Operator: contains
    Value: 'active'

    You are only allowed to use the following operators for string-values: 'contains'
    You are not allowed to filter based on numerical values.
    
    Make sure that the filter condition is valid and respects the values and spelling from the column of the given table.
    Only filter for numbers if it is explicitely necessary.
    
    Do not reason beyond your task of calculating the filter conditions.
    """
    
    return prompt
