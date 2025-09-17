import json, re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, FunctionMessage
from langchain_tavily import TavilySearch
from langchain.agents import Tool
from langgraph.prebuilt import create_react_agent
from backend.app.graphs.utils.state import MyState  # tumhara state class
from backend.app.graphs.utils.prompts import recipe_prompt
from backend.app.graphs.utils.constants import model_name, GEMINI_API_KEY, TAVILY_API_KEY

# ---- initialize once (global) ----
llm = ChatGoogleGenerativeAI(
    model=model_name,
    google_api_key=GEMINI_API_KEY
)

# Tavily search tool
search_tool = Tool(
    name="TavilySearch",
    func=TavilySearch(api_key=TAVILY_API_KEY, max_results=3).run,
    description=(
        "Use this tool when the question needs the latest or real-time information "
        "(e.g. trending recipes, seasonal dishes, ingredient prices). "
        "If your own knowledge is enough, you can answer directly."
    )
)

# Create the React Agent (no AgentType required)
react_agent = create_react_agent(
    llm,
    tools=[search_tool],
    prompt=(recipe_prompt)
)


def cooking_research_agent(state: MyState) -> MyState:
    print("Invoking cooking research agent")
    query = state["query"].strip()
    print("DEBUG query:", repr(query))

    raw_result = react_agent.invoke({"messages": [{"role": "user", "content": query}]})
    print("RAW RESULT:", raw_result)

    final_message = raw_result.get("messages")[-1]
    raw_text = final_message.content

    print("DEBUG raw_text repr:", repr(raw_text))

    # This regex is specifically designed to handle code fences with "json"
    json_match = re.search(r"```json\n?([\s\S]*?)\n?```", raw_text)
    
    if json_match:
        cleaned = json_match.group(1).strip()
    else:
        # Fallback for direct answers without code fences
        cleaned = raw_text.strip()

    try:
        result_dict = json.loads(cleaned)
    except json.JSONDecodeError:
        print(f"JSON DECODE ERROR: Could not parse JSON from: {cleaned}")
        result_dict = {"content": "I'm sorry, an error occurred while processing your request.", "source": "LLM generated response"}

    print("DEBUG parsed result:", result_dict)
    state["content"] = result_dict
    return state