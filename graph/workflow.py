from langgraph.graph import StateGraph, END


from graph.GraphState import GraphState
from graph.nodes.next_operation import next_operation

from graph.nodes.add_column_params import add_column_params
from graph.nodes.add_column import add_column
from graph.nodes.group_by_params import group_by_params
from graph.nodes.group_by import group_by
from graph.nodes.select_column_params import select_column_params
from graph.nodes.select_column import select_column
from graph.nodes.select_row_params import select_row_params
from graph.nodes.select_row import select_row
from graph.nodes.sort_column_params import sort_column_params
from graph.nodes.sort_column import sort_column
from graph.nodes.reset_state import reset_state
from graph.nodes.evaluate_select_row_params import evaluate_select_row_params

max_operations = 3

def decide_cat_path(state):
    operation = state["next_operation"]
    table = state["table"]
    return operation


def decide_end(state):
    operation_chain = state["operation_chain"]
    last_operation = state["next_operation"]
    table = state["table"]
    table_is_empty = table.empty
    last_operation_is_none = last_operation == "None"
    more_than_max_operations = len(operation_chain) >= max_operations
    out = (
        "end"
        if more_than_max_operations or last_operation_is_none or table_is_empty
        else "loop"
    )
    return out


def get_workflow():
    workflow = StateGraph(GraphState)

    workflow.add_node("get_next_operation", next_operation)
    workflow.add_node("add_column_params", add_column_params)
    workflow.add_node("group_by_params", group_by_params)
    workflow.add_node("select_column_params", select_column_params)
    workflow.add_node("select_row_params", select_row_params)
    # workflow.add_node("validate_row_params", evaluate_select_row_params)
    workflow.add_node("sort_column_params", sort_column_params)
    workflow.add_node("add_column", add_column)
    workflow.add_node("group_by", group_by)
    workflow.add_node("select_column", select_column)
    workflow.add_node("select_row", select_row)
    workflow.add_node("sort_column", sort_column)
    workflow.add_node("reset_state", reset_state)

    workflow.set_entry_point("reset_state")
    workflow.add_edge("reset_state", "get_next_operation")
    workflow.add_conditional_edges(
        "get_next_operation",
        decide_cat_path,
        {
            "select_row": "select_row_params",
            "add_column": "add_column_params",
            "select_column": "select_column_params",
            "group_by": "group_by_params",
            "sort_column": "sort_column_params",
            "None": END,
        },
    )
    workflow.add_edge("select_row_params", "select_row")
    # workflow.add_edge("validate_row_params", "select_row")
    workflow.add_edge("add_column_params", "add_column")
    workflow.add_edge("select_column_params", "select_column")
    workflow.add_edge("group_by_params", "group_by")
    workflow.add_edge("sort_column_params", "sort_column")
    workflow.add_conditional_edges(
        "select_row", decide_end, {"loop": "get_next_operation", "end": END}
    )
    workflow.add_conditional_edges(
        "add_column", decide_end, {"loop": "get_next_operation", "end": END}
    )
    workflow.add_conditional_edges(
        "select_column", decide_end, {"loop": "get_next_operation", "end": END}
    )
    workflow.add_conditional_edges(
        "group_by", decide_end, {"loop": "get_next_operation", "end": END}
    )
    workflow.add_conditional_edges(
        "sort_column", decide_end, {"loop": "get_next_operation", "end": END}
    )

    # workflow.add_edge("reset_state", END)

    return workflow.compile()
