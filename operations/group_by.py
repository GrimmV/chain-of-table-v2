import pandas as pd
from prompts.group_by_params_prompt import group_by_params_prompt
from pydantic import BaseModel, field_validator

allowed_agg_functions = ["sum", "mean", "median", "count", "size", "max", "min", "std", "var", "first", "last"]

class GroupByParams(BaseModel):
    column: str
    agg_function: str
    explanation: str
    
    @field_validator('agg_function')
    def check_operator(cls, v):
        if v not in allowed_agg_functions:
            matched_substring = matched_substrings(v, allowed_agg_functions)
            if (len(matched_substring) > 0):
                return matched_substring[0]
            raise ValueError(f"The aggregation function must be one of {allowed_agg_functions} but it is {v}")
        return v

def group_by(df: pd.DataFrame, column, agg_function):
    result = getattr(df.groupby(column), agg_function)()
    return result


def get_group_by_params(query, table, llm):

    prompt = group_by_params_prompt(query, table)

    params = llm.generate(
        prompt,
        response_model=GroupByParams,
        system_message="You are a helpful assistant and expert in transforming tables based on python pandas operations.",
    )

    return params.dict()

def matched_substrings(main_string, substrings):
    return [substring for substring in substrings if substring in main_string]