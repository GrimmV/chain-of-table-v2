from llm.llm import ChatGPT
from pydantic import BaseModel

class FinalEval(BaseModel):
    istrue: bool

def final_evaluation(query: str, op_chain: dict, table: str, llm: ChatGPT):
    
    prompt = "Evaluate the user query based on the given query and tell if the statement is true or false."
    
    prompt += f"statement: {query}\n\n"
    
    prompt += f"These operations formed the table below: {op_chain}\n\n"
    
    prompt += f"table: {table}\n\n"
    
    response = llm.generate(prompt, response_model=FinalEval, system_message="You are a helpful assistant.")
    
    return response.dict()
    
    