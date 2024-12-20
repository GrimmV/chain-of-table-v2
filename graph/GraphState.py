from typing_extensions import TypedDict
from llm.llm import ChatGPT
import pandas as pd

class GraphState(TypedDict):
    """
    Represents the state of our graph.
    """
    llm: ChatGPT
    table: pd.DataFrame
    query: str
    caption: str
    initial_column_descriptions: dict
    column_descriptions: dict
    available_operations: list[str]
    operation_chain: list[str]
    next_operation: str
    next_operation_parameters: list[dict] | dict