from transform_dataset import table2pipe, pipe2table, df2pipe
from load_dataset import load_dataset
from final_evaluation import final_evaluation
import pandas as pd
from utils.next_operations import possible_next_operations

from get_next_operation import get_next_operation
from llm.llm import ChatGPT
from operations.add_column import add_column
from operations.select_column import select_column
from operations.select_row import select_row
from operations.sort_column import sort_column
from operations.group_by import group_by

import os
from dotenv import load_dotenv

# load .env file to environment
load_dotenv()

API_KEY = os.getenv('API_KEY')
MODEL_NAME = os.getenv("MODEL_NAME")

max_iterations = 3

dataset = load_dataset("data/tabfact.jsonl")
llm = ChatGPT(model_name=MODEL_NAME, key=API_KEY)

def get_final_table(query, table, llm, caption) -> pd.DataFrame:
    next_operation = "START"
    iteration = 0
    pandas_table = pipe2table(table)
    available_operations = possible_next_operations
    while next_operation != "None" and iteration < max_iterations:
        pipe_table = df2pipe(pandas_table, caption)
        next_operation_info = get_next_operation(query, pipe_table, llm=llm, next_operations=available_operations)
        print(next_operation_info)
        next_operation = next_operation_info["next_operation"]
        op_parameters = next_operation_info["operation_parameters"]
        if (next_operation == "add_column"):
            pandas_table = add_column(pandas_table, name=op_parameters[0], llm=llm)
        elif (next_operation == "select_row"):
            pandas_table = select_row(pandas_table, rows=op_parameters)
        elif (next_operation == "select_column"):
            pandas_table = select_column(pandas_table, columns=op_parameters)
        elif (next_operation == "sort_column"):
            pandas_table = sort_column(pandas_table, column=op_parameters[0], ascending=op_parameters[1])
        elif (next_operation == "group_column"):
            pandas_table = group_by(pandas_table)
        iteration += 1
        if next_operation != "None":
            available_operations.remove(next_operation)
        
    return pandas_table
        

if __name__ == "__main__":
    num_samples = 10
    eval_values = []
    for idx in range(num_samples):
        active_table = dataset[idx]
        caption = active_table["table_caption"]
        label = active_table["label"]

        stringified_table = table2pipe(active_table["table_text"], caption=caption)
        statement = active_table["statement"]
        final_table = get_final_table(statement, stringified_table, llm, caption)
        print(df2pipe(final_table, caption))
        
        final_response = final_evaluation(statement, final_table, llm)
        
        print(f"model evaluation: {final_response["istrue"]}")
        print(f"label: {True if label == 1 else False}")
        
        eval_values.append({"pred": final_response["istrue"], "label": True if label == 1 else False})
    
    correct_pairs = 0
    for elem in eval_values:
        if elem["pred"] == elem["label"]:
            correct_pairs += 1
    
    print(correct_pairs / num_samples)
