def group_by_params_prompt(query, table, column_descriptions):
    prompt = f"""You are provided with a table and a user query. Your task is to suggest the most appropriate column to group the data by and a fitting aggregation function based on the user's request.

    Table:\n {table}\n
    
    Column descriptions: \n{column_descriptions}\n
    
    User Query: "{query}"

    Your goal is to:

        Identify the column(s) to group the data by, based on the focus of the query.
        Recommend a suitable aggregation function that aligns with the query’s objective.

    Consider the following aggregation functions:

        Summarization:
            sum: Total of values.
            mean: Average of values.
            median: Median of values.
            count: Count of non-null values.
            size: Size of each group (total number of rows).
        Extremes:
            max: Maximum value.
            min: Minimum value.
        Distribution & Dispersion:
            std: Standard deviation.
            var: Variance.
        Position-based:
            first: First value in each group.
            last: Last value in each group.

    Output format:

        Suggested column to group by
        Suggested aggregation function
        Brief explanation
    """
    
    return prompt