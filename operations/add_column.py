import pandas as pd
from pydantic import BaseModel, field_validator, ValidationInfo
from llm.llm import ChatGPT
from prompts.add_column_params_prompt import add_column_params_prompt


class AddColumnParams(BaseModel):
    name: str
    description: str


class ColumnValue(BaseModel):
    value: str | int | float
    explanation: str


def _get_column_value(
    row: list, column_text: str, name: str, description: str, llm: ChatGPT
) -> ColumnValue:
    row_text = ", ".join([f"{val}" for val in row])
    prompt = f"""These are the column names: {column_text} \
        
        these are the row values: {row_text} \
            
        construct the value of the new column based on the given rows. The new column is called {name} and described as follows: {description}. \
                
    """
    value = llm.generate(
        query="",
        prompt=prompt,
        response_model=ColumnValue,
        system_message="You are a helpful assistant.",
    )

    return value


def get_add_column_parameters(
    table: str,
    query: str,
    validation_context: dict,
    llm: ChatGPT,
    column_descriptions: dict,
) -> dict:

    prompt = add_column_params_prompt(query, table, column_descriptions)

    response = llm.generate(
        query,
        prompt,
        response_model=AddColumnParams,
        system_message="You are a helpful assistant and expert in transforming tables based on python pandas operations.",
        validation_context=validation_context,
    )

    return response.dict()


def add_column(df: pd.DataFrame, name: str, description: str, llm: ChatGPT):

    new_col = []
    column_names = df.columns
    column_text = ", ".join([f"{val}" for val in column_names])

    for _, row in df.iterrows():
        response = _get_column_value(row, column_text, name, description, llm)
        print(response.value)
        print(response.explanation)
        new_col.append(response.value)

    df.insert(len(df.columns) - 1, name, new_col)

    return df
