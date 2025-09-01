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
        f""" You are a classification system. Your job is to classify a user query into one of three classes:

        1. Irrelevant → Not related to cooking/recipes.  
        2. Relevant-General → Cooking related queries that are timeless and can be answered from internal knowledge (e.g. recipes, ingredients, cooking methods).  
        3. Relevant-Updated → Cooking related queries that require latest/real-time information (e.g. "Aaj Village Cooking channel ne kya banaya?", "new recipes uploaded recently").  

        ### Examples:

        Query: "How to make biryani at home?"  
        Class: research_general  

        Query: "I have chicken, rice, and tomatoes. What can I cook?"  
        Class: research_general

        Query: "What recipes are listed on Apna Khana YouTube channel?"  
        Class: research_updated  

        Query: "What recipe Village Cooking Channel uploaded today?"  
        Class: research_updated 
        
        Query: "What are the recent recipes?"  
        Class: research_updated 

        Query: "What are the dishes that are in trend?"  
        Class: research_updated  

        Query: "Explain machine learning in simple terms."  
        Class: Irrelevant  

        Query: "What is SGI in networking?"  
        Class: Irrelevant  

        Query: "What is the price of Honda CG 125 in Pakistan?"  
        Class: Irrelevant  

        Now classify the following query strictly as either 'Irrelevant', 'research_general', or 'research_updated':"""
        f"\n\nQuery:\n{query}"
    ).content
    print(f"\n\n{classifier}")

    state["classifier"] = classifier
    return state