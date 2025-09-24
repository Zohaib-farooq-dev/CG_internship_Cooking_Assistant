import json, re

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, FunctionMessage
from langchain_tavily import TavilySearch
from langchain.agents import Tool
from langgraph.prebuilt import create_react_agent
from backend.app.graphs.utils.state import MyState  # tumhara state class
from backend.app.graphs.utils.prompts import CookingPrompt
from backend.app.graphs.utils.constants import MODEL_NAME, GEMINI_API_KEY, TAVILY_API_KEY
from backend.app.config.logging import get_logger

#Initialize logger 
logger = get_logger("recipe_generate") 

# Initialize once (global) 
llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
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
    prompt=(CookingPrompt.RECIPE_PROMPT)
)

def cooking_research_agent(state: MyState) -> MyState:
    """
    Executes the LangGraph ReAct agent to answer cooking-related queries 
    using a LLM model with an optional real time searcing (Tavily search tool) to
    generate responses. And stores the parsed result in the state's 'content' field.

    Args:
        state (MyState):
            A mutable state object (typically a dict-like container) that must
            contain the key ``"query"`` with the user's cooking question as a
            string. The function reads and updates this object in-place.

    Returns:
        MyState:
            The same state object with an additional or updated key
            ``"content"``.  
            • If JSON parsing succeeds, ``state["content"]`` contains a Python
              dictionary parsed from the model's JSON output.  
            • If parsing fails, ``state["content"]`` contains a fallback
              dictionary of the form:
              ``{"content": "<error message>", "source": "LLM generated response"}``.

    Logging:
        Uses the module-level logger to record:
            • INFO messages for high-level process flow (agent invocation).
            • DEBUG messages for query text, raw model output, and parsed data.
            • EXCEPTION logs if JSON decoding fails (includes full stack trace).

    """
    logger.info("Invoking cooking research agent")
    query = state["query"].strip()
    logger.debug("DEBUG query: %r", query)

    raw_result = react_agent.invoke({"messages": [{"role": "user", "content": query}]})
    logger.debug("RAW RESULT: %s", raw_result)

    final_message = raw_result.get("messages")[-1]
    raw_text = final_message.content

    logger.debug("DEBUG raw_text repr: %r", raw_text)

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
        logger.exception(f"JSON DECODE ERROR: Could not parse JSON from: {cleaned}")
        result_dict = {"content": "I'm sorry, an error occurred while processing your request.", "source": "LLM generated response"}

    logger.debug("DEBUG parsed result: %s", result_dict)
    state["content"] = result_dict
    return state