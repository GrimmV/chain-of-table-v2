import pandas as pd

def select_row(df: pd.DataFrame, rows: list[str]) -> pd.DataFrame:
    
    numeric_rows = _extract_row_numbers(rows)
    print(numeric_rows)
    
    return df.iloc[numeric_rows]


def _extract_row_numbers(rows: list[str]) -> list[int]:
    
    numeric_rows = [int(item.split()[1]) - 1 for item in rows]
    
    return numeric_rows
        