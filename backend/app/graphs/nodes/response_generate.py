# backend/app/graphs/response_generate.py
from backend.app.graphs.utils.state import MyState

def generate_response(state: MyState):

    # Predefined irrelevant message
    irrelevant_msg = (
        """This content is irrelevant to the Agent context. 
         This agent is only for cooking or recipe-related queries."""
    )

    # Check if the classifier marked it as irrelevant
    if state.get("classifier") == "irrelevant":
        state["content"] = {"content": irrelevant_msg}
        return state

