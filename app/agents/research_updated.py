import os, json , re
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from app.graphs.state import MyState

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


tavily_search = TavilySearch(api_key=TAVILY_API_KEY, max_results=3)

def research_updated_agent(state: MyState):
    query = state["query"]
    tavily_results = tavily_search.invoke({"query": query})
    print("DEBUG tavily_results: \n", f"{tavily_results}\n")

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=API_KEY)

    result = llm.invoke(
        f""" You are a cooking/recipe assistant. 
        I already did a web search for this query: "{query}".

        Use ONLY the following results to answer the query.
        Return output STRICTLY as a JSON object with this schema:
        {{
            "content": "<short helpful answer to the query based on the results>",
            "source": "<best matching url from the results>"
        }}

        Do not add extra text, explanations, or code fences.
        
        Results:
        {json.dumps(tavily_results, indent=2)}"""
    ).content

    raw_result = result.strip()

    # remove code fences if any
    cleaned = re.sub(r"^```[a-zA-Z]*\n?", "", raw_result)
    cleaned = re.sub(r"\n?```$", "", cleaned).strip()

    print("DEBUG cleaned result:", cleaned)

    result_dict = json.loads(cleaned)

    state["content"] = result_dict
    return state