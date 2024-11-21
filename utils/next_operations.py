
possible_next_operations = {
        "select_row": {
                "description": "Filter rows based on filter criteria."
        }, 
        # "select_first_n": {
        #         "description": "Filter the first n rows from the table."      
        # },
        "add_column": {
                "description": "Add a custom column to the table to improve verbosity.",
                "condition": "select_row"
        }, 
        "select_column": {
                "description": "Choose a subset of columns."
        }, 
        "group_by": {
                "description": "Group the column based on a column and apply aggregation methods."
        }, 
        "sort_column": {
                "description": "Order the table in ascending or descending order. Either based on numerical values or alphabetical ordering."
        }
}