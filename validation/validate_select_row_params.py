import pandas as pd
from typing import List, Dict

from llm.llm import ChatGPT
from operations.select_row import SelectRowParams

from prompts.validate_select_row_params_prompt import validate_select_row_params_prompt

def validate_select_row_params(llm: ChatGPT, conditions: List[Dict], query: str, table_snippet: pd.DataFrame, column_descriptions: List[str], validation_context: Dict) -> List:
        
    prompt = validate_select_row_params_prompt(conditions, table_snippet, query, column_descriptions)
    
    response = llm.generate(
        prompt,
        response_model=List[SelectRowParams],
        system_message="You are a helpful assistant and expert in transforming tables based on python pandas operations.",
        validation_context=validation_context
    )
    
    dict_response = []
    for elem in response:
        print(elem.explanation)
        dict_response.append(elem.dict())

    return dict_response