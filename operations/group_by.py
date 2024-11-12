import pandas as pd
from prompts.group_by_params_prompt import group_by_params_prompt
from pydantic import BaseModel, field_validator, ValidationInfo

allowed_agg_functions = ["sum", "mean", "median", "count", "size", "max", "min", "std", "var", "first", "last"]

class GroupByParams(BaseModel):
    column: str
    agg_function: str
    explanation: str
    
    @field_validator('agg_function')
    def check_aggregation_function(cls, v):
        if v not in allowed_agg_functions:
            matched_substring = matched_substrings(v, allowed_agg_functions)
            if (len(matched_substring) > 0):
                return matched_substring[0]
            raise ValueError(f"The aggregation function must be one of {allowed_agg_functions} but it is {v}")
        return v
    
        
    @field_validator('column')
    def check_column(cls, v, info: ValidationInfo):
        column = v
        columns = info.context["columns"]
        if column not in columns:
            raise ValueError(f"The specified column '{column}' does not exist. Available columns are {columns}")
        return v

def group_by(df: pd.DataFrame, column, agg_function):
    result = df.groupby(by=[column]).agg(agg_function).reset_index()
    return result


def get_group_by_params(query: str, table: str, validation_context: dict, llm, column_descriptions) -> dict:

    prompt = group_by_params_prompt(query, table, column_descriptions)

    params = llm.generate(
        prompt,
        response_model=GroupByParams,
        system_message="You are a helpful assistant and expert in transforming tables based on python pandas operations.",
        validation_context=validation_context
    )

    return params.dict()

def matched_substrings(main_string, substrings):
    return [substring for substring in substrings if substring in main_string]