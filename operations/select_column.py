import pandas as pd
from pydantic import BaseModel
from prompts.select_columns_params_prompt import select_columns_params_prompt

class SelectColumnsParams(BaseModel):
    columns: list[str]

def select_column(df: pd.DataFrame, columns: list[str]):
    
    return df[columns]

def get_select_column_params(query, table, llm):
    
    prompt = select_columns_params_prompt(query, table)
    
    response = llm.generate(
        prompt,
        response_model=SelectColumnsParams,
        system_message="You are a helpful assistant and expert in transforming tables based on python pandas operations.",
    )

    return response.dict()