from backend.app.graphs.langgraph import app_graph, START
from backend.app.models.query import QueryRequest

async def process_query(request: QueryRequest):
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
