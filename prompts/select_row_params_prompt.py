def select_row_params_prompt(query, table):
    prompt = f"""You are given a table and a user query. Based on the user's query, 
    provide a list of filter conditions that include the column name, operator, and value to compare.

    Table: \n{table}\n

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

    
    User Query: \n{query}\n
    Output:
    """
    
    return prompt
