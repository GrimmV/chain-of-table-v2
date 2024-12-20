from llm.llm import ChatGPT
from pydantic import BaseModel

from prompts.final_evaluation_prompt import final_evaluation_prompt

class FinalEval(BaseModel):
    istrue: bool
    explanation: str

def final_evaluation(query: str, op_chain: dict, table: str, llm: ChatGPT):
    
    prompt = final_evaluation_prompt(query, table, op_chain)
    
    response = llm.generate(query, prompt, FinalEval)
    
    return response.model_dump()
    
    