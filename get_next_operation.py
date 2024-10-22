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
        if v not in possible_next_operations and v != "None":
            raise ValueError(
                f"next operation must be one of {str(possible_next_operations)} or None but it is {v}"
            )
        return v


def get_next_operation(
    query: str,
    table_content: str,
    llm: ChatGPT = None,
    next_operations: list[str] = possible_next_operations
) -> dict:

    prompt = next_operation_prompt(next_operations, query, table_content)

    response = llm.generate(
        prompt,
        response_model=NextOperation,
        system_message="You are a helpful assistant and expert in transforming tables based on python pandas operations.",
    )

    return response.dict()