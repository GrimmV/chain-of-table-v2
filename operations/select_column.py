import pandas as pd
from pydantic import BaseModel, field_validator, ValidationInfo
from prompts.select_columns_params_prompt import select_columns_params_prompt

class SelectColumnsParams(BaseModel):
    columns: list[str]
    
    
    @field_validator('columns')
    def check_columns(cls, v, info: ValidationInfo):
        columns = info.context["columns"]
        filter_columns = set(v)
        if not filter_columns.issubset(set(columns)):
            raise ValueError(f"Not all specified columns exist: {v}. Available columns are {columns}")
        return v

def select_column(df: pd.DataFrame, columns: list[str]):
    
    return df[columns]

def get_select_column_params(query: str, table: str, validation_context: dict, llm, column_descriptions) -> dict:
    
    prompt = select_columns_params_prompt(query, table, column_descriptions)
    
    response = llm.generate(
        query,
        prompt,
        response_model=SelectColumnsParams,
        system_message="You are a helpful assistant and expert in transforming tables based on python pandas operations.",
        validation_context=validation_context
    )

    return response.dict()