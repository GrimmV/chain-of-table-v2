from llm.llm import ChatGPT
from pydantic import BaseModel

class FinalEval(BaseModel):
    istrue: bool
    explanation: str

def final_evaluation(query: str, op_chain: dict, table: str, llm: ChatGPT):
    
    prompt = "Evaluate the user query based on the given query and tell if the statement is true or false."
    
    prompt += f"statement: {query}\n\n"
    
    prompt += f"table: {table}\n\n"
    
    prompt += f"These operations formed the table below: {op_chain}\n\n"
    
    prompt += "Here are the statement about the table and the task is to tell whether the statement is True or False."
    
    response = llm.generate(prompt, response_model=FinalEval, system_message="You are a helpful assistant that is an expert in table comprehension.")
    
    return response.dict()
    
    