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
        2. research_general → Cooking-related queries that are timeless and can be answered confidently from internal knowledge (e.g. recipes, ingredients, cooking methods).  
        3. research_updated → Cooking-related queries that either require the latest/real-time information OR cannot be confidently answered from your internal knowledge (e.g., region-specific recipes, new recipes uploaded recently).

        ### Instructions:
        - If the query is not about cooking → Irrelevant
        - If the query is about cooking and you can answer confidently from your internal knowledge → research_general
        - If the query is about cooking but you **cannot answer confidently** from internal knowledge or it’s time/region-specific → research_updated

        ### Examples:

        Query: "How to make biryani at home?"  
        Class: research_general  

        Query: "I have chicken, rice, and tomatoes. What can I cook?"  
        Class: research_general 

        Query: "What is the traditional dessert served in Mirpur during Eid?"
        Class: research_updated

        Query: "How do you make Siri-Paye the way its cooked in Lahore streets?"
        Class: research_updated 

        Query: "I have drumsticks, jaggery, and pumpkin. What traditional Sindhi dish can I make?"
        Class: research_updated

        Query: "How can I cook cookies like Crumble cooks in Pakistan?"
        Class: research_updated

        Query: "What recipes are listed on Apna Khana YouTube channel?"  
        Class: research_updated  

        Query: "What recipe Village Cooking Channel uploaded today?"  
        Class: research_updated  

        Query: "What are the dishes that are in trend?"  
        Class: research_updated  

        Query: "Explain machine learning in simple terms."  
        Class: Irrelevant  

        Query: "What is SGI in networking?"  
        Class: Irrelevant  

        Query: "What is the price of Honda CG 125 in Pakistan?"  
        Class: Irrelevant  

        Now classify the following query strictly as either 'Irrelevant', 'research_general', or 'research_updated'. Consider the LLM’s confidence: if you **cannot confidently answer** the query from internal knowledge, choose 'research_updated':
        """
        f"\n\nQuery:\n{query}"
    ).content
    print(f"\n\n{classifier}")

    state["classifier"] = classifier
    return state