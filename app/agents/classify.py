import os
from dotenv import load_dotenv
from langchain_google_genai import  ChatGoogleGenerativeAI
from app.graphs.state import MyState

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

def classify_agent(state: MyState):
    query = state["query"]
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=API_KEY)

    classifier= llm.invoke(
        f""" You are a classification system for cooking queries.
            Classify the user query into exactly one of the following:
            1. Irrelevant → Not related to cooking/recipes.
            2. research_general → Cooking-related queries that you can confidently answer
            with your own knowledge or with creative combinations of common ingredients,
            even if the recipe is regional (e.g., "Mumbai butter chicken", "Lahori Karahi")
            **IF** it is a known/traditional dish you likely have information about.
            3. research_updated → Cooking-related queries that require
            (a) real-time or trending info (e.g., "latest viral TikTok recipe"),
            (b) hyper-local or very obscure dishes you cannot confidently answer,
            or (c) brand-specific/restaurant-specific secret recipes
            (e.g., "exact KFC Zinger formula", "today’s Village Cooking Channel recipe").

            ### Rules:
            - Region or city **alone** does not force 'research_updated'.
            - Always attempt to combine your internal knowledge creatively
            before deciding you cannot answer.
            - Choose 'research_updated' only when you are genuinely unsure
            or need up-to-date external data.

            ### Examples:
            Query: "How to make biryani at home?"
            Class: research_general

            Query: "How to cook Mumbai style butter chicken?"
            Class: research_general

            Query: "What recipe Village Cooking Channel uploaded today?"
            Class: research_updated

            Query: "Exact secret spices used in Karachi Burns Road Nihari?"
            Class: research_updated

            Query: "Explain machine learning in simple terms."
            Class: Irrelevant

            Now classify this query strictly as 'Irrelevant', 'research_general', or 'research_updated"""
        f"\n\nQuery:\n{query}"
    ).content
    print(f"\n\n{classifier}")

    state["classifier"] = classifier
    return state