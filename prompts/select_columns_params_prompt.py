def select_columns_params_prompt(query, table):
    
    prompt = f"""You are given a table and a user query. Based on the user's query, 
    provide the column names to filter for.
    
    Table: \n{table}\n

    User Query: {query}
    
    """
    
    return prompt