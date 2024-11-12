from transform_dataset import table2pipe, pipe2table, df2pipe, table2df
from load_dataset import load_dataset
from final_evaluation import final_evaluation
from final_evaluation_baseline import final_evaluation_baseline
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
MODEL_NAME_NEMO = os.getenv("MODEL_NAME_NEMO")
MODEL_NAME_GPT = os.getenv("MODEL_NAME_GPT")
BASE_URL = os.getenv("BASE_URL")

model = "gpt"
dataset = load_dataset("data/data.jsonl")
if model == "nemo":
    llm = OllamaOpenAI(model_name=MODEL_NAME_NEMO, base_url=BASE_URL)
else:
    llm = ChatGPT(model_name=MODEL_NAME_GPT, key=API_KEY)
    

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
    eval_values_baseline = []
    for idx in range(num_samples):
        active_table = dataset[idx]
        caption = active_table["table_caption"]
        label = active_table["label"]
        statement = active_table["statement"]
        table_text = active_table["table_text"]
        descriptions = active_table["column_descriptions"]
        pandas_table = table2df(table_text)
        pipe_table = df2pipe(pandas_table, caption, approach="unlimited")
        
        
        final_table_info = get_final_table(statement, pandas_table, llm, caption, descriptions)
        
        
        final_table = final_table_info["table"]
        op_chain = final_table_info["chain"]
        print(op_chain)
        op_chain_nl = chain_to_nl(op_chain)
        
        final_pipe_table = df2pipe(final_table, caption)
        
        final_response = final_evaluation(statement, op_chain_nl, final_pipe_table, llm)
        final_response_baseline = final_evaluation_baseline(statement, pipe_table, llm)
        # Specify the file path where you want to save the output
        output_file = "output_log.txt"

        # log results
        with open(output_file, 'a') as file:
            file.write(f"user query: {statement}\n")
            file.write("function chain:\n")
            file.write(f"{op_chain_nl}\n")
            file.write(f"{df2pipe(final_table, caption)}\n")
            
            file.write("evaluation output:\n")
            file.write(f"{final_response['explanation']}\n")
            file.write(f"model evaluation: {final_response['istrue']}\n")
            
            file.write("baseline output:\n")
            file.write(f"{final_response_baseline['explanation']}\n")
            file.write(f"model evaluation: {final_response_baseline['istrue']}\n")
            
            file.write(f"label: {True if label == 1 else False}\n")
            file.write("\n")  # Add a newline for separation between entries
        
        eval_values.append({"pred": final_response["istrue"], "label": True if label == 1 else False})
        eval_values_baseline.append({"pred": final_response_baseline["istrue"], "label": True if label == 1 else False})
    
    correct_pairs = 0
    correct_pairs_baseline = 0
    for i, elem in enumerate(eval_values):
        baseline_elem = eval_values_baseline[i]
        if elem["pred"] == elem["label"]:
            correct_pairs += 1
        if baseline_elem["pred"] == elem["label"]:
            correct_pairs_baseline += 1
        
    ratio_eval = correct_pairs / num_samples
    ratio_baseline = correct_pairs_baseline / num_samples
    
        # log results
    with open(output_file, 'a') as file:
        file.write(f"ealuation ratio: {ratio_eval}\n")
        file.write(f"baseline ratio: {ratio_baseline}\n")
