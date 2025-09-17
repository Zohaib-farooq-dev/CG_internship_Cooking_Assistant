"""
Defines the LangGraph workflow for cooking queries.

This graph connects the individual nodes (classifier, recipe generator,
evaluator, and alternative_recipe) and sets the conditional transitions between them to
create a complete cooking-query pipeline.

The graph is compiled as `app_graph` and automatically saves a PNG
visualization of the flow to `image_path`.
"""
from langgraph.graph import StateGraph, START, END
from backend.app.graphs.nodes.classify import classify_agent
from backend.app.graphs.nodes.recipe_generate import cooking_research_agent
from backend.app.graphs.nodes.evaluation import evaluation_agent
from backend.app.graphs.nodes.alternative_recipe import alternative_recipe_agent
from backend.app.graphs.nodes.response_generate import generate_response
from backend.app.graphs.utils.state import MyState
from backend.app.graphs.utils.constants import image_path

graph = StateGraph(MyState)

graph.add_node("classifier", classify_agent)
graph.add_node("cooking_recipe", cooking_research_agent)
graph.add_node("evaluation", evaluation_agent)
graph.add_node("alternative_agent", alternative_recipe_agent)
graph.add_node("response", generate_response)

graph.add_edge(START, "classifier")

graph.add_conditional_edges(
    "classifier",
    lambda state: state.get("classifier", "").lower(),
    {
        "irrelevant": "response",
        "relevant": "cooking_recipe"
    }
)

graph.add_edge("cooking_recipe", "evaluation")

graph.add_conditional_edges(
    "evaluation",
    lambda state: (
        END
        if not state["evaluate"].get("is_recipe", False)
        else (
            END
            if state["evaluate"].get("can_make_with_cookwares", False)
            else "alternative_agent"
        )
    ),
    {
        "alternative_agent": "alternative_agent",
        END:END,
    }
)
graph.add_edge("alternative_agent", END)
graph.add_edge("response", END)

app_graph = graph.compile()


try:
    png_image_bytes = app_graph.get_graph().draw_mermaid_png()

    # Save the bytes to a file
    with open(image_path, "wb") as f:
        f.write(png_image_bytes)
except Exception as e:
    print(f"Error generating graph: {e}")
    print("Please ensure you have run 'pip install pyppeteer' and 'python -m pyppeteer.install'")

