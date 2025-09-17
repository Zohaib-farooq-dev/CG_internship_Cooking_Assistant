"""
Graph node for creating the final output message
for irrelevant queries.
"""
from backend.app.graphs.utils.state import MyState

def generate_response(state: MyState)->MyState:
    """
    Replace the state's content with a predefined message for irrelevant quries.
    """
    # Predefined irrelevant message
    irrelevant_msg = (
        """This content is irrelevant to the Agent context. 
         This agent is only for cooking or recipe-related queries."""
    )
    state["content"] = {"content": irrelevant_msg}
    return state

