def next_operation_prompt(operations: list[str], table: str, query: str) -> str:
    prompt = f"""Context: You are provided with a table and a query that requires insights based on the data. Your task is to reason step-by-step through the process of deriving these insights, using explicit operations on the table.

    this is the users query: {query}
    this is the table: \n{table}
    
    Objective: You must conduct operations iteratively until the final insight is reached. At each step, choose only one operation to perform. After performing that operation, evaluate the updated table or interim results to decide what the next operation should be. Continue this process until all necessary steps have been taken and the final, optimized table or answer has been derived.

    Instructions:

        Review the Table: Start by carefully reviewing the provided table and query.
        Choose an Operation: Identify one operation you believe should be performed next. 
        
        The available operations are: {operations}
        
        Explain why this operation is necessary.
        Perform the Operation: Simulate the operation and describe the resulting table or interim results.
        Evaluate Next Steps: Based on the updated information, decide the next operation that should be conducted.
        Iterate Until Completion: Continue this process until the final result or insight has been reached. Do not jump to conclusions based on the initial data alone.
        Summarize the Insights: Once all steps are completed, provide a final summary of the insights or the final optimized table.

    Constraints:

        Do not assume that the table immediately provides the answer.
        Do not conclude the process prematurely. Always consider if another operation could refine or enhance the information.
        Avoid stating that "the table already provides all necessary information" without performing operations on it.

    Example:

        Step 1: Select a row of the table based on [Condition X], as this will narrow down the data to the most relevant subset for the query.
        Step 2: After filtering, sort the results by [Column Y] to highlight trends or outliers in the data.
        Step 3: Next, groupby [Column Z] to calculate the sum/average, which helps quantify the overall effect.

    """
    return prompt