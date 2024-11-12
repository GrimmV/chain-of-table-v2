from transform_dataset import table2pipe, pipe2table, df2pipe, table2df
from load_dataset import load_dataset
from final_evaluation import final_evaluation
import pandas as pd
from utils.next_operations import possible_next_operations

from llm.llm import ChatGPT
from llm.ollama import OllamaOpenAI
from utils.chain_to_nl import chain_to_nl

from graph.workflow import get_workflow

import os
from dotenv import load_dotenv

# load .env file to environment
load_dotenv()

API_KEY = os.getenv('API_KEY')
MODEL_NAME = os.getenv("MODEL_NAME")
BASE_URL = os.getenv("BASE_URL")

model = "gpt"
dataset = load_dataset("data/data.jsonl")
if model == "nemo":
    llm = OllamaOpenAI(model_name=MODEL_NAME, base_url=BASE_URL)
else:
    llm = ChatGPT(model_name=MODEL_NAME, key=API_KEY)
    

def get_final_table(query, table: pd.DataFrame, llm, caption: str, column_descriptions: dict) -> pd.DataFrame:
    next_operation = "START"
    available_operations = list(possible_next_operations.keys())
    op_chain = []
    inputs = {
        "llm": llm,
        "table": table,
        "caption": caption,
        "initial_column_descriptions": column_descriptions,
        "column_descriptions": column_descriptions,
        "query": query,
        "available_operations": available_operations,
        "operation_chain": op_chain,
        "next_operation": next_operation,
        "next_operation_parameters": {}
    }
    app = get_workflow()
    for output in app.stream(inputs):
        keys = list(output.keys())
        print_table = output[keys[0]]["table"]
    keys = list(output.keys())
    return {"table": output[keys[0]]["table"], "chain": output[keys[0]]["operation_chain"]}
        

if __name__ == "__main__":
    num_samples = 7
    eval_values = []
    for idx in range(num_samples):
        active_table = dataset[idx]
        caption = active_table["table_caption"]
        label = active_table["label"]
        statement = active_table["statement"]
        table_text = active_table["table_text"]
        descriptions = active_table["column_descriptions"]
        pandas_table = table2df(table_text)
        
        
        final_table_info = get_final_table(statement, pandas_table, llm, caption, descriptions)
        
        
        final_table = final_table_info["table"]
        op_chain = final_table_info["chain"]
        op_chain_nl = chain_to_nl(op_chain)
        
        
        print(f"user query: {statement}")
        print("function chain:")
        print(op_chain_nl)
        print(df2pipe(final_table, caption))
        
        final_response = final_evaluation(statement, op_chain_nl, final_table, llm)
        
        print(final_response["explanation"])
        
        print(f"model evaluation: {final_response['istrue']}")
        print(f"label: {True if label == 1 else False}")
        
        eval_values.append({"pred": final_response["istrue"], "label": True if label == 1 else False})
    
    correct_pairs = 0
    for elem in eval_values:
        if elem["pred"] == elem["label"]:
            correct_pairs += 1
    
    print(correct_pairs / num_samples)
