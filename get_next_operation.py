from pydantic import BaseModel, field_validator
from typing import List
from prompts.few_shot_individual_op import few_shot_individual_operation
from utils.next_operations import possible_next_operations

from llm.llm import ChatGPT


class NextOperation(BaseModel):
    next_operation: str
    operation_parameters: List[str]
    explanation: str

    @field_validator("next_operation")
    @classmethod
    def operation_must_contain(cls, v: str) -> str:
        if v not in possible_next_operations and v != "None":
            raise ValueError(
                f"next operation must be one of {str(possible_next_operations)} or None but it is {v}"
            )
        return v


def get_next_operation(query: str, table_content: str, llm: ChatGPT = None, next_operations: list[str]= possible_next_operations) -> dict:

    prompt = _construct_prompt(query, table_content, next_operations)

    response = llm.generate(
        prompt,
        response_model=NextOperation,
        system_message='''You are a helpful assistant that has the goal to transform a table so that the query can be handled most efficiently. \
            
            You are supposed to choose the next operation to approach this goal and make the table as concise and comprehensible as possible. \
            If there is no operation that can improve the table, provide None as operation.
        ''',
    )

    print(response)

    return response.dict()


def _construct_prompt(query, table_content, possible_next_operations):
    prompt = ""
    for operation in possible_next_operations:
        prompt += few_shot_individual_operation[f"plan_{operation}_demo"] + "\n\n"

    prompt += "/*\n" + table_content + "\n*/\n"
    prompt += "Query: " + query + "\n"

    _possible_next_operations_str = " or ".join([op for op in possible_next_operations])

    _possible_next_operations_str += " or None, if further transformation of the table does not help to handle the query."

    prompt += f"The next operation must be one of {_possible_next_operations_str}.\n"

    return prompt
