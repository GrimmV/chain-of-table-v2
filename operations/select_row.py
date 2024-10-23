import pandas as pd
from pydantic import BaseModel
from prompts.select_row_params_prompt import select_row_params_prompt

class SelectRowParams(BaseModel):
    column: str
    operator: str
    value: int | str | float

def select_row(df: pd.DataFrame, column: str, operator: str, value: int | str | float) -> pd.DataFrame:
    
    if isinstance(value, str):
        if operator == "==":
            mask = eval(f"df['{column}'].str.contains('{value}')")
        else:
            mask = eval(f"~df['{column}'].str.contains('{value}')")
            
    else:
        df[column] = pd.to_numeric(df[column], errors='coerce')
        mask = eval(f"df['{column}'] {operator} {value}")
        
    # e.g. df["column1"] > 20
    
    return df[mask]


def get_select_row_params(query, table, llm):
    
    prompt = select_row_params_prompt(query, table)
    
    response = llm.generate(
        prompt,
        response_model=SelectRowParams,
        system_message="You are a helpful assistant and expert in transforming tables based on python pandas operations.",
    )


    return response.dict()