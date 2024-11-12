def select_row_params_prompt(query, table, column_descriptions):
    prompt = f"""You are given a table and a user query. Based on the user's query, 
    provide filter conditions that include the column name, operator, and value to compare.

    Snippet of the table: \n{table}\n
    
    Column descriptions: \n{column_descriptions}\n

    User Query: {query}
    
    User Query Example 1:
    "Find all rows where the age is greater than 30."

    Expected Output:

    Column: age
    Operator: >
    Value: 30

    User Query Example 2:
    "Select the rows where the status is 'active'."

    Expected Output:

    Column: status
    Operator: ==
    Value: 'active'

    You are only allowed to use the following operators for number-values: '>=', '<=', '>', '<', '==', '!='
    You are only allowed to use the following operators for string-values: 'contains'
    
    Make sure that the filter condition is valid and respects the values and spelling from the column of the given table.
    Only filter for numbers if it is explicitely necessary.
    
    Output:
    """
    
    return prompt
