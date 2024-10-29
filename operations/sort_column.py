import pandas as pd
from pydantic import BaseModel, field_validator, ValidationInfo
from prompts.sort_column_params_prompt import sort_column_params_prompt

order_values = ["ascending", "descending"]

class SortColumnParams(BaseModel):
    column: str
    order: str
    
    @field_validator('column')
    def check_column(cls, v, info: ValidationInfo):
        column = v
        columns = info.context["columns"]
        if column not in columns:
            raise ValueError(f"The specified column '{column}' does not exist. Available columns are {columns}")
        return v
    
    @field_validator('order')
    def check_order(cls, v):
        order = v
        if order not in order_values:
            raise ValueError(f"You specified order as {order}, but it must be one of {order_values}")
        return v

def sort_column(df: pd.DataFrame, column, order: str = "ascending"):
    
    is_ascending = order == "ascending"
    print(f"column to sort {column}")
    
    df = df.sort_values(by=[column], ascending=is_ascending)
    
    return df

def get_sort_column_params(query: str, table: str, validation_context: dict, llm) -> dict:
        
    prompt = sort_column_params_prompt(query, table)
    
    response = llm.generate(
        prompt,
        response_model=SortColumnParams,
        system_message="You are a helpful assistant and expert in transforming tables based on python pandas operations.",
        validation_context=validation_context
    )

    return response.dict()