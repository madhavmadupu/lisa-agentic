from typing import TypedDict, List, Annotated
import operator

class AgentState(TypedDict):
    """
    State definition for the LISA agent system.
    Propagates the user constraint, the plan, the code, and execution feedback throughout the graph.
    """
    user_request: str
    plan: dict
    code: str
    review_feedback: str
    execution_output: str
    retry_count: int
    revision_number: int
    error: str
