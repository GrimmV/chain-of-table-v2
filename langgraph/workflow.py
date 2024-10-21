from langgraph.graph import StateGraph, END
from GraphState import GraphState
from nodes.next_operation import next_operation

def decide_cat_path(state):
    cat = state["category"]
    if cat == "General":
        return "general"
    elif cat == "Guidance":
        return "guidance"
    else:
        return "data"

def get_workflow():
    workflow = StateGraph(GraphState)

    workflow.add_node("get_next_operation", next_operation)
    workflow.add_node("add_column", add_column)
    workflow.add_node("select_column", select_column)
    workflow.add_node("select_row", select_row)
    workflow.add_node("sort_column", sort_column)
    workflow.add_node("general_response", general_response)
    workflow.add_node("save_history", save_history)
    workflow.add_node("clear_state", clear_state)

    workflow.set_entry_point("categorize")
    workflow.add_conditional_edges(
        "categorize",
        decide_cat_path,
        {
            "data": "handle_thread",
            "guidance": "guidance_response",
            "general": "general_response",
        }
    )
    workflow.add_edge("handle_thread", "choose_data")
    workflow.add_edge("choose_data", "data_response")
    workflow.add_edge("data_response", "save_history")
    workflow.add_edge("guidance_response", "save_history")
    workflow.add_edge("general_response", "save_history")
    workflow.add_edge("save_history", "clear_state")
    workflow.add_edge("clear_state", END)
    
    return workflow.compile(checkpointer=memory)