from get_next_operation import get_next_operation

def next_operation(state):
    
    query = state.query
    table = state.table_content
    llm = state.llm
    
    return get_next_operation(query, table, llm)