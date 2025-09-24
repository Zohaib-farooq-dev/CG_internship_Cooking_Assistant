from backend.app.graphs.langgraph import app_graph, START
from backend.app.models.query import QueryRequest

async def process_query(request: QueryRequest)->dict:
    """
    Run the LangGraph pipeline on the provided user query.

    Args:
        request (QueryRequest): The validated request body containing the user query.

    Returns:
        dict: A JSON-compatible dictionary containing the final processed content
              under the key `"result"`.
    """
    # Prepare initial state for the graph
    state = {
        "query": request.query,
        "classifier": "",
        "content": {},
        "evaluate": False,
    }

    #Invoke the graph starting from START
    final_state = await app_graph.ainvoke(state, start_node=START,debug =True)

    # Return the final content from the state
    return {"result": final_state["content"]}
