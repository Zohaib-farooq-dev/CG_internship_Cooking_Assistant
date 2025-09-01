from langgraph.graph import StateGraph, START, END
from app.agents.classify import classify_agent
from app.agents.research_general import research_agent
from app.agents.research_updated import research_updated_agent
from app.agents.irrelevant import irrelevant_agent
from app.agents.evaluation import evaluation_agent
from app.agents.cookware_response import cookware_agent
from app.graphs.state import MyState

graph = StateGraph(MyState)

graph.add_node("classifier", classify_agent)
graph.add_node("research_general", research_agent)
graph.add_node("research_updated", research_updated_agent)
graph.add_node("irrelevant", irrelevant_agent)
graph.add_node("evaluation", evaluation_agent)
graph.add_node("cookware_agent", cookware_agent)


graph.add_edge(START, "classifier")

graph.add_conditional_edges(
    "classifier",
    lambda state: state.get("classifier", "").lower(),
    {
        "irrelevant": "irrelevant",
        "research_general": "research_general",
        "research_updated": "research_updated"
    }
)

graph.add_edge("research_general", "evaluation")
graph.add_edge("research_updated", "evaluation")

graph.add_edge("irrelevant", END)


graph.add_conditional_edges(
    "evaluation",
    lambda state: (
        END
        if not state["evaluate"].get("is_recipe", False)
        else (
            END
            if state["evaluate"].get("can_make_with_cookwares", False)
            else "cookware_agent"
        )
    ),
    {
        "cookware_agent": "cookware_agent",
        END: END,
    }
)
graph.add_edge("cookware_agent", END)


# dot = Digraph(format='png')
# for state in graph.nodes:
#     dot.node(state)

# # LangGraph me edges ka real structure: graph.edges -> dict {source: [targets]}
# for edge in graph.edges:
#     if len(edge) == 3:
#         src, tgt, condition = edge
#         if condition:  # agar condition hai
#             dot.edge(src, tgt, label=str(condition))
#         else:         # condition None ya empty ho
#             dot.edge(src, tgt)
#     else:
#         # fallback in case edge is just a 2-tuple
#         src, tgt = edge
#         dot.edge(src, tgt)
# # for edge in graph.edges:
# #     if len(edge) == 3:
# #         src, tgt, condition = edge
# #         if condition:
# #             dot.edge(src, tgt, label=str(condition))
# #         else:
# #             dot.edge(src, tgt)
# #     else:  # fallback for normal 2-tuple edges
# #         src, tgt = edge
# #         dot.edge(src, tgt)
# # for src, tgt in graph.edges:
# #     dot.edge(src, tgt)

# # --- Visualize ---
# dot.render('langgraph_graph', view=True)

app_graph = graph.compile()

