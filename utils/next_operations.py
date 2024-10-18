
possible_next_operations_dict = {
    "<init>": [
        "select_row", 
        "add_column", 
        "select_column",
        "group_column",
        "sort_column",
    ],
    "select_row": [
        "add_column", 
        "select_column", 
        "group_column", 
        "sort_column",
        "<END>",
    ],
    "add_column": [
        "select_column",
        "group_column",
        "sort_column",
        "<END>",
    ],
    "select_column": [
        "group_column",
        "sort_column",
        "<END>",
    ],
    "group_column": [
        "sort_column",
        "<END>",
    ],
    "sort_column": [
        "<END>",
    ],
}