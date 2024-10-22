import pandas as pd
from pydantic import BaseModel
from prompts.sort_column_params_prompt import sort_column_params_prompt

class SortColumnParams(BaseModel):
    column: str
    order: str

def sort_column(df: pd.DataFrame, column, order: str = "ascending"):
    
    is_ascending = not order != "ascending"
    
    df = df.sort_values(by=column, ascending=is_ascending)
    
    return df

def get_sort_column_params(query, table, llm):
        
    prompt = sort_column_params_prompt(query, table)
    
    response = llm.generate(
        prompt,
        response_model=SortColumnParams,
        system_message="You are a helpful assistant and expert in transforming tables based on python pandas operations.",
    )

    return response.dict()