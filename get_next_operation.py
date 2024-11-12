from pydantic import BaseModel, field_validator
from typing import List
from prompts.next_operation_prompt import next_operation_prompt
from utils.next_operations import possible_next_operations

from llm.llm import ChatGPT


class NextOperation(BaseModel):
    next_operation: str
    # operation_parameters: List[str]
    # explanation: str

    @field_validator("next_operation")
    @classmethod
    def operation_must_contain(cls, v: str) -> str:
        if v not in list(possible_next_operations.keys()) and v != "None":
            raise ValueError(
                f"next operation must be one of {str(possible_next_operations.keys())} or None but it is {v}"
            )
        return v


def get_next_operation(
    query: str,
    table_content: str,
    llm: ChatGPT = None,
    next_operations: list[str] = list(possible_next_operations.keys())
) -> dict:

    prompt = next_operation_prompt(next_operations, table_content)

    response = llm.generate_structured_reasoning_response(
        query,
        context=prompt,
    )
    
    print(response.reasoning)

    return response.final_response