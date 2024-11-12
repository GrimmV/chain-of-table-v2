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
    
    @field_validator('column')
    def check_column(cls, v, info: ValidationInfo):
        
        column = v
        column_types = info.context["column_types"]
        columns = column_types.keys()
        column_is_numeric = column_types[column]["is_numeric"]
        value = info.data.get('value')
        if column not in columns:
            raise ValueError(f"The specified column '{column}' does not exist. Available columns are {columns}")
        # elif isinstance(value, (int, float)) and not column_is_numeric:
        #     print(f"the value is a number: {value}")
        #     raise ValueError(f"The value of the filter operation must be numeric as the column '{column}' has dtype string. Currently, it is a string: {value}")
        # elif isinstance(value, str) and column_is_numeric:
        #     raise ValueError(f"The value of the filter operation must be a string as the column '{column}' has a numeric dtype. Currently, it is a number: {value}")
        
        return v
    
    @field_validator('operator')
    def check_operator(cls, v, info: ValidationInfo):
        value = info.data.get('value')
        if isinstance(value, (int, float)) and v not in num_operators:
            raise ValueError(f"operator must be one of {num_operators} when value is a number but you provided {v}")
        elif isinstance(value, str) and v not in str_operators:
            if v == "==":
                return "contains"
            raise ValueError(f"operator must be one of {str_operators} when value is a string but you provided {v}")
        return v

def select_row(df: pd.DataFrame, conditions: List[Dict]) -> pd.DataFrame:
    
    masks = []
    
    for condition in conditions:
        
        column = condition["column"]
        operator = condition["operator"]
        value = condition["value"]

        print(condition)
    
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
    
    print(combined_mask)
    
    return df[combined_mask]


def get_select_row_params(query: str, table: str, validation_context: Dict, llm: ChatGPT, column_descriptions: Dict) -> List[Dict]:
    
    prompt = select_row_params_prompt(query, table, column_descriptions)
    
    response = llm.generate(
        prompt,
        response_model=List[SelectRowParams],
        system_message="You are a helpful assistant and expert in transforming tables based on python pandas operations.",
        validation_context=validation_context
    )
    
    dict_response = []
    for elem in response:
        dict_response.append(elem.dict())


    return dict_response