import pandas as pd

def sort_column(df: pd.DataFrame, column, ascending: str = "ascending"):
    
    is_ascending = not ascending != "ascending"
    
    df = df.sort_values(by=column, ascending=is_ascending)
    
    return df