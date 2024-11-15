from llm.llm import ChatGPT
from pydantic import BaseModel

from prompts.final_evaluation_baseline_prompt import final_evaluation_baseline_prompt

class FinalEval(BaseModel):
    istrue: bool
    explanation: str

def final_evaluation_baseline(query: str, table: str, llm: ChatGPT):
    
    prompt = final_evaluation_baseline_prompt(query, table)
    
    response = llm.generate(query, prompt, FinalEval)
    
    return response.model_dump()
    
    