from transform_dataset import table2pipe, pipe2table
from load_dataset import load_tabfact_dataset

dataset = load_tabfact_dataset("data/data.jsonl")

first_table = dataset[0]

stringified_table = table2pipe(first_table["table_text"], caption=first_table["table_caption"])
print(stringified_table)

pandas_table = pipe2table(stringified_table) 

print(pandas_table.head())