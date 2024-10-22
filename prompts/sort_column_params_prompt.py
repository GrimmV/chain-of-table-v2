def sort_column_params_prompt(query, table):
    
    prompt = f"""You are given a table and a user query. Based on the user's query, 
    provide a column to sort and the order to sort in, i.e. 'ascending' or 'descending'.
    
    Table: \n{table}\n

    User Query: {query}
    
    """
    
    return prompt