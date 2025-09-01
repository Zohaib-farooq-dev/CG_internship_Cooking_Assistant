from app.graphs.langgraph import app_graph, START
from app.models.query import QueryRequest

async def process_query(request: QueryRequest):
    # Prepare initial state for the grap
    state = {
        "query": request.query,
        "classifier": "",
        "content": {},
        "evaluate": False
    }

    # Run the graph starting from START node
    final_state = app_graph.invoke(state, start_node=START)

    # Return the final content from the state
    return {"result": final_state["content"]}