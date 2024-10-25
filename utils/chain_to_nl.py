
def chain_to_nl(chain):
    
    text = ""
    
    for elem in chain:
        func = elem["func"]
        params = elem["params"]
        
        if func == "select_row":
            text += "Selected rows based on the following conditions:\n"
            for condition in params:
                text += f"{condition["column"]} {condition["operator"]} {condition["value"]} \n"
        elif func == "select_column":
            text += f"Selected the following columns: {params["columns"]}\n"
        elif func == "add_column":
            text += f"Added a column with the name {params["name"]}\n"
        elif func == "sort_column":
            text += f"Sorted column {params["column"]} in {params["order"]} order\n"
        elif func == "group_by":
            text += f"Grouped dataframe by column {params["column"]} and aggregated it based on {params["agg_function"]}\n"
            
    return text