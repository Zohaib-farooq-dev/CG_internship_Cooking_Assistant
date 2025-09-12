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
    print("Invoking google search agent")
    query = state["query"]
    tavily_results = tavily_search.invoke({"query": query, "raw_content": True})
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

        **Example
             User: "What is the recipe of an omelette?"  
             Output:  
             {{
              "content": "To make an omelette, whisk 2 eggs with salt and pepper, heat oil in a pan, pour the mixture, cook until set, and fold.",
              "source": "https://youtube.com/jhsvhvhj"
             }}

             User: "How can i cook the malai boti recipe in a lahori flavor?"  
             Output:  
             {{
                "content": "To make Malai Boti with a Lahori twist, marinate 500g boneless chicken with 1/2 cup thick yogurt, 1/2 cup fresh cream, 1 tbsp ginger paste, 1 tbsp garlic paste, 2 green chilies (finely chopped), 1 tsp roasted cumin powder, 1 tsp roasted coriander powder, 1.5 tsp garam masala, 1/2 tsp black pepper, 1/2 tsp white pepper, 1 tsp salt, and juice of 1 lemon. Let it marinate for at least 4 hours. Skewer the chicken and grill or cook on a tawa until golden brown. Serve hot with naan or rice.",
                "source": "https://www.youtube.com/watch?v=koHCXnLlNsM"
             }}
             User: "I have pumpkin and jaggery. Can you suggest a traditional sindhi dish or recipe?"
             Output:
             {{
                "content": "You can make 'Pumpkin Jaggery Halwa', a traditional South Asian dessert. Peel and grate 500g pumpkin. Heat 2 tbsp ghee in a pan, add pumpkin, and cook for 5-7 minutes. Add 100g grated jaggery and 1/2 cup milk, stir continuously on low heat. Cook until mixture thickens and jaggery is fully dissolved. Add a pinch of cardamom powder for flavor. Serve warm garnished with chopped nuts.",
                "source": "https://www.example.com/pumpkin-halwa"
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