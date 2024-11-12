
def final_evaluation_prompt(query: str, table: str, op_chain: dict) -> str:
    
    prompt = f'''Evaluate the user query based on the given table and tell if the users statement is true or false.\n
    
        statement: {query}\n\n
        table: {table}\n\n
        These operations formed the table below: {op_chain}\n\n
        
        How did the operations help to break down the table? Think step by step.
    '''
    
    return prompt