import pandas as pd
from pydantic import BaseModel, field_validator, ValidationInfo
from prompts.select_row_params_prompt import select_row_params_prompt
from typing import List, Dict
from llm.llm import ChatGPT

num_operators = ["<=", ">=", "<", ">", "==", "!="]
str_operators = ["contains"]

class SelectRowParams(BaseModel):
    value: int | str | float
    column: str
    operator: str
    
    @field_validator('operator')
    def check_operator(cls, v, info: ValidationInfo):
        value = info.data.get('value')
        if isinstance(value, (int, float)) and v not in num_operators:
            raise ValueError(f"operator must be one of {num_operators} when value is a number")
        elif isinstance(value, str) and v not in str_operators:
            raise ValueError(f"operator must be one of {str_operators} when value is a string")
        return v

def select_row(df: pd.DataFrame, conditions: List[Dict]) -> pd.DataFrame:
    
    masks = []
    
    for condition in conditions:
        
        column = condition["column"]
        operator = condition["operator"]
        value = condition["value"]
    
    
        if isinstance(value, str):
            if operator == "contains":
                mask = eval(f"df['{column}'].str.contains('{value}')")
                
        else:
            df[column] = pd.to_numeric(df[column], errors='coerce')
            mask = eval(f"df['{column}'] {operator} {value}")
        
        masks.append(mask)
    
    combined_mask = masks[0]
    if len(masks) > 1:
        for mask in masks[1:]:
            combined_mask &= mask
    
    return df[combined_mask]


def get_select_row_params(query, table, llm: ChatGPT):
    
    prompt = select_row_params_prompt(query, table)
    
    response = llm.generate(
        prompt,
        response_model=List[SelectRowParams],
        system_message="You are a helpful assistant and expert in transforming tables based on python pandas operations.",
    )
    
    dict_response = []
    for elem in response:
        dict_response.append(elem.dict())


    return dict_response