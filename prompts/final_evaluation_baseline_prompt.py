
def final_evaluation_baseline_prompt(query: str, table: str) -> str:
    
    prompt = f'''Evaluate the user query based on the given table and tell if the users statement is true or false.\n
    
        statement: {query}\n\n
        table: {table}\n\n
        
        Evaluate the user query based on the given table and tell if the users statement is true or false. Think step by step.
    '''
    
    return prompt