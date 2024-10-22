import pandas as pd
from pydantic import BaseModel
from llm.llm import ChatGPT
from prompts.add_column_params_prompt import add_column_params_prompt


class AddColumnParams(BaseModel):
    name: str


class ColumnValue(BaseModel):
    value: str | int | float


def _get_column_value(
    row: list, column_text: str, name: str, llm: ChatGPT
) -> ColumnValue:
    row_text = ", ".join([f"{val}" for val in row])
    prompt = f"""These are the column names: {column_text} \
        
        these are the row values: {row_text} \
            
        construct the value of the new column based on the given rows. The new column is called {name}. \
                
    """
    value = llm.generate(
        prompt,
        response_model=ColumnValue,
        system_message="You are a helpful assistant.",
    )

    return value


def get_add_column_parameters(table: str, query: str, llm: ChatGPT):

    prompt = add_column_params_prompt(query, table)

    response = llm.generate(
        prompt,
        response_model=AddColumnParams,
        system_message="You are a helpful assistant and expert in transforming tables based on python pandas operations.",
    )

    return response.dict()


def add_column(df: pd.DataFrame, name: str, llm: ChatGPT):

    new_col = []
    column_names = df.columns
    column_text = ", ".join([f"{val}" for val in column_names])

    for _, row in df.iterrows():
        response = _get_column_value(row, column_text, name, llm)
        new_col.append(response.value)

    df.insert(len(df.columns) - 1, name, new_col)

    return df
