
from pydantic import BaseModel
from typing import List
from prompts.few_shot_individual_op import few_shot_individual_op
from utils.next_operations import possible_next_operations_dict

class NextOperation(BaseModel):
    next_operation: str
    operation_parameters: List[str]


def get_next_operation(statement, table_content, last_operation=None, llm_options=None, llm=None):
    
    last_operation = "<init>" if not last_operation else last_operation
    possible_next_operations = possible_next_operations_dict[last_operation]
    
    prompt = _construct_prompt(statement, table_content, possible_next_operations)
    
    response = llm.generate_plus_with_score(
        prompt, response_model=NextOperation, options=llm_options, end_str="\n\n"
    )
        
        
def _construct_prompt(statement, table_content, possible_next_operations):
    prompt = ""
    for operation in possible_next_operations:
        if operation == "<END>":
            continue
        prompt += few_shot_individual_op[f"plan_{operation}_demo"] + "\n\n"

    prompt += "/*\n" + table_content + "\n*/\n"
    prompt += "Statement: " + statement + "\n"

    _possible_next_operations_str = " or ".join(
        [f"f_{op}()" if op != "<END>" else op for op in possible_next_operations]
    )

    if len(possible_next_operations) > 1:
        prompt += (
            f"The next operation must be one of {_possible_next_operations_str}.\n"
        )
    else:
        prompt += f"The next operation must be {_possible_next_operations_str}.\n"
        
    return prompt