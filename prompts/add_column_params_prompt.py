
def add_column_params_prompt(query: str, table: str, column_descriptions) -> str:
    
    prompt = f'''Given the following table and user query, provide the name of a new column 
        you want to add to the table which can be derived from the existing table values. 
        Describe the purpose of the new column and its dtype.\n
        
        snippet of the table: \n{table}\n
        
        Column descriptions: \n{column_descriptions}\n
            
        user query: {query}        
    '''
    
    return prompt