# Function to check if a value is a stringified number
def is_stringified_number(value):
    try:
        float(value)  # Try to convert the value to float
        return True
    except (ValueError, TypeError):
        return False