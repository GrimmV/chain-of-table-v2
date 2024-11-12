def select_columns_params_prompt(query, table, column_descriptions):
    
    prompt = f"""You are given a table and a user query. Based on the user's query, 
    provide the column names to filter for.
    
    Snippet of the table: \n{table}\n
    
    Column descriptions: \n{column_descriptions}\n

    User Query: {query}
    
    """
    
    return prompt