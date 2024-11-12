def sort_column_params_prompt(query, table, column_descriptions):
    
    prompt = f"""You are given a table and a user query. Based on the user's query, 
    provide a column to sort and the order to sort in, i.e. 'ascending' or 'descending'.
    
    Snippet of the table: \n{table}\n
    
    Column descriptions: \n{column_descriptions}\n

    User Query: {query}
    
    """
    
    return prompt