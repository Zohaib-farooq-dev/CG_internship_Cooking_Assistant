import os
from dotenv import load_dotenv
from langchain_google_genai import  ChatGoogleGenerativeAI
from backend.app.graphs.state import MyState

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

def classify_agent(state: MyState):
    query = state["query"]
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=API_KEY)

    classifier= llm.invoke(
        f""" You are a classification system for cooking queries.
            Classify the user query into exactly one of the following two classes:

            1. irrelevant → Not related to cooking or recipes.
            2. relevant → Any query related to cooking, recipes, ingredients, or food preparation, 
            including traditional, regional, or brand-specific dishes.

            ### Rules:
            - Always classify queries about food, ingredients, or recipes as 'relevant', 
            even if the recipe is rare, regional, or you may need external information.
            - Classify anything outside the domain of cooking as 'irrelevant'.
            - Return ONLY one class: 'irrelevant' or 'relevant'.

            ### Examples:
            Query: "How to make biryani at home?"
            Class: relevant

            Query: "How to cook Mumbai style butter chicken?"
            Class: relevant

            Query: "What recipe Village Cooking Channel uploaded today?"
            Class: relevant

            Query: "Exact secret spices used in Karachi Burns Road Nihari?"
            Class: relevant

            Query: "Explain machine learning in simple terms."
            Class: irrelevant

            Now classify this query strictly as 'irrelevant' or 'relevant':"""
        f"\n\nQuery:\n{query}"
    ).content
    print(f"\n\n{classifier}")

    state["classifier"] = classifier
    return state