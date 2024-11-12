import pandas as pd
from utils.is_stringified_number import is_stringified_number

def table2df(table_text, num_rows=100):
    header, rows = table_text[0], table_text[1:]
    rows = rows[:num_rows]
    df = pd.DataFrame(data=rows, columns=header)
    # Convert columns where the first value is a stringified number
    for col in df.columns:
        first_value = df[col].iloc[0]
        if isinstance(first_value, str) and is_stringified_number(first_value):
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df


def df2pipe(df, caption=None, size: int = 5, approach = "limited"):
    linear_table = ""
    if caption is not None:
        linear_table += "table caption : " + caption + "\n"

    header = "col : " + " | ".join(df.columns) + "\n"
    linear_table += header
    rows = df.values.tolist()
    for row_idx, row in enumerate(rows):
        if approach == "limited" and row_idx >= size: break
        row = [str(x) for x in row]
        line = "row {} : ".format(row_idx + 1) + " | ".join(row)
        if row_idx != len(rows) - 1:
            line += "\n"
        linear_table += line
    return linear_table

def table2pipe(
    table_text,
    num_rows=100,
    caption=None,
):
    df = table2df(table_text, num_rows)
    linear_table = df2pipe(df, caption)
    return linear_table

def pipe2table(pipe: str):
    
    # Splitting the rows and processing the pipe-formatted data
    rows = [line.split(" : ")[1].split(" | ") for line in pipe.strip().split("\n")[2:]]
    columns = [line.split(" : ")[1].split(" | ") for line in pipe.strip().split("\n")[1:2]][0]

    # Creating the DataFrame
    df = pd.DataFrame(rows, columns=columns)
    
    return df