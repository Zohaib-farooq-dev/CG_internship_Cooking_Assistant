
from app.graphs.state import MyState
def irrelevant_agent(state: MyState):
    msg = "This content is irrelevant to the Agent context. This agent is only for cooking or recipe-related queries."
    state["content"] = {"content": msg}
    return state
