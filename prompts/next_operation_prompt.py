from utils.next_operations import possible_next_operations

def next_operation_prompt(operations: list[str], table: str, query: str) -> str:
    described_operations = _get_operation_descriptions(operations, possible_next_operations)
    prompt = f"""Context: You are provided with a snippet table and a query that requires insights based on the data. Your task is to suggest operations that will extract the relevant informations from the full table.

    This is the users query: {query}
    This is a snippet of the table: \n{table}
    
    Objective: Suggest one single table operation that improves the table structure to address the user query.

    Instructions:

        Review the Table: Start by carefully reviewing the provided table and query.
        Choose an Operation: Identify one operation you believe should be performed next. 
        
        The available operations are: {described_operations} and None
        
        Explain why this operation is necessary.

    Constraints:

        Do not assume that the table immediately provides the answer.
        Do not add any parameters to the operations - provide only the operation name.
        Do not conclude the process prematurely. Always consider if another operation could refine or enhance the information.

    Examples:

        - Select a row of the table based on [Condition X], as this will narrow down the data to the most relevant subset for the query.
        - Sort the results by [Column Y] to highlight trends or outliers in the data.
        - Groupby [Column Z] to calculate the sum/average, which helps quantify the overall effect.

    """
    return prompt


def _get_operation_descriptions(available_operations: list[str], all_operations: dict) -> dict:
    
    described_operations = {}
    
    for op in available_operations:
        condition = all_operations[op].get("condition")
        if condition not in available_operations:
            described_operations[op] = all_operations[op]["description"]
        
    return described_operations