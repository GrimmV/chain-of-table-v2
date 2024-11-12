from typing import List, Dict
import pandas as pd

def validate_select_row_params_prompt(conditions: List[Dict], table: pd.DataFrame, query: str, column_descriptions: List[str]) -> str:
    prompt = f"""You are given a user query, a table and filter operations that are logically combined with AND. 
    Validate if the filter operations are sensible for the given user query. Remove and add filter operations as needed.
    
    Either return the provided filter operations again or update the filter operations to make them sensible.

    User query: \n{query}\n

    Snippet of the table: \n{table}\n
    
    Column descriptions: \n{column_descriptions}\n
    
    Filter condition to be applied: \n{conditions}\n

    You are only allowed to use the following operators for number-values: '>=', '<=', '>', '<', '==', '!='
    You are only allowed to use the following operators for string-values: 'contains'
    
    Make sure that the filter condition is valid and respects the values and spelling from the column of the given table. Think step by step.
    The values need to match the format in the columns, otherwise the filtering will not work. Abreviations and similar simplifications need to be respected.
    
    Output:
    """
    
    return prompt
