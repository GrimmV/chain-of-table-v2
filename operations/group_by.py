import pandas as pd
from prompts.group_by_params_prompt import group_by_params_prompt
from pydantic import BaseModel


class GroupByParams(BaseModel):
    column: str
    agg_function: str
    explanation: str


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
