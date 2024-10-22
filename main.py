from transform_dataset import table2pipe, pipe2table, df2pipe
from load_dataset import load_dataset
from final_evaluation import final_evaluation
import pandas as pd
from utils.next_operations import possible_next_operations

from llm.llm import ChatGPT

from graph.workflow import get_workflow

import os
from dotenv import load_dotenv

# load .env file to environment
load_dotenv()

API_KEY = os.getenv('API_KEY')
MODEL_NAME = os.getenv("MODEL_NAME")

dataset = load_dataset("data/tabfact.jsonl")
llm = ChatGPT(model_name=MODEL_NAME, key=API_KEY)

def get_final_table(query, table, llm, caption) -> pd.DataFrame:
    next_operation = "START"
    pandas_table = pipe2table(table)
    available_operations = possible_next_operations
    op_chain = []
    inputs = {
        "llm": llm,
        "table": pandas_table,
        "caption": caption,
        "query": query,
        "available_operations": available_operations,
        "operation_chain": op_chain,
        "next_operation": next_operation,
        "next_operation_parameters": {}
    }
    app = get_workflow()
    for output in app.stream(inputs):
        print(output)
    # print(output)
        

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
    #     # print(df2pipe(final_table, caption))
        
    #     final_response = final_evaluation(statement, final_table, llm)
        
    #     print(f"model evaluation: {final_response["istrue"]}")
    #     print(f"label: {True if label == 1 else False}")
        
    #     eval_values.append({"pred": final_response["istrue"], "label": True if label == 1 else False})
    
    # correct_pairs = 0
    # for elem in eval_values:
    #     if elem["pred"] == elem["label"]:
    #         correct_pairs += 1
    
    # print(correct_pairs / num_samples)
