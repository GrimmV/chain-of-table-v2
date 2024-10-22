
def add_column_params_prompt(query: str, table: str) -> str:
    
    prompt = f'''Given the following table and user query, provide the name of a new column 
        you want to add to the table which can be derived from the existing table values.\n
        
        table content: \n{table}\n
            
        user query: {query}        
    '''
    
    return prompt