import pandas as pd
from typing import Optional

from llm.llm import ChatGPT
from operations.select_row import SelectRowParams

from prompts.validate_select_row_params_prompt import validate_select_row_params_prompt

def validate_select_row_params(llm: ChatGPT, condition: dict, column_snippet: pd.Series, column_description: str, validation_context: dict) -> dict:
        
    prompt = validate_select_row_params_prompt(condition, column_snippet, column_description)
    
    response = llm.generate(
        prompt,
        response_model=SelectRowParams,
        system_message="You are a helpful assistant and expert in transforming tables based on python pandas operations.",
        validation_context=validation_context
    )

    return response.dict()