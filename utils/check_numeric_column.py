import pandas as pd

# Function to check if a column contains only numeric values
def check_numeric_column(column):
    return pd.to_numeric(column, errors='coerce').notna().all()