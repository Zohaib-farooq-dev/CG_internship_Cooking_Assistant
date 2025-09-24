from backend.app.graphs.utils.state import MyState

def generate_response(state: MyState)->MyState:
    """
    Replace the state's content with a predefined message for irrelevant queries.

    Args:
        state (MyState):
            A custom state object (dict-like) expected to contain a
            `content` key. Other keys in the state are preserved.

    Returns:
        MyState:
            The same `state` object with its
            - `state["content"]` (dict)
            replaced by:
            {
                "content": "<irrelevant query warning message>"
            }
    """
    # Predefined irrelevant message
    irrelevant_msg = (
        """This content is irrelevant to the Agent context. 
         This agent is only for cooking or recipe-related queries.
         """
    )
    state["content"] = {"content": irrelevant_msg}
    return state

