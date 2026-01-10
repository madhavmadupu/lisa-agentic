from langgraph.graph import StateGraph, END
from state.state import AgentState
from agents.architect import architect_node
from agents.coder import coder_node
from agents.reviewer import reviewer_node

def should_continue(state):
    """
    Determines if we need to loop back to Coder or end.
    """
    feedback = state.get('review_feedback', '')
    retry_count = state.get('retry_count', 0)
    
    if feedback == "Approved":
        return END
    
    if retry_count >= 3:
        return END # Max retries reached
        
    return "coder"

# Define the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("architect", architect_node)
workflow.add_node("coder", coder_node)
workflow.add_node("reviewer", reviewer_node)

# Add edges
workflow.set_entry_point("architect")
workflow.add_edge("architect", "coder")
workflow.add_edge("coder", "reviewer")

# Conditional edge from reviewer
workflow.add_conditional_edges(
    "reviewer",
    should_continue,
    {
        "coder": "coder",
        END: END
    }
)

# Compile
app = workflow.compile()
