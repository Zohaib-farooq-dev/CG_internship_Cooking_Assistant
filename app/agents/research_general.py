import os, json,re
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from app.graphs.state import MyState

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

def research_agent(state: MyState):
    query = state["query"] 
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=API_KEY)

    result = llm.invoke(
        f""" Answer the following query clearly and concisely. 
        Also provide relevant explanation if needed. And give response strictly in python dictionary

        **Example
             User: "What is the recipe of an omelette?"  
             Output:  
             {{
              "content": "To make an omelette, whisk 2 eggs with salt and pepper, heat oil in a pan, pour the mixture, cook until set, and fold.",
              "source": "LLM generated response"
             }}"""
        f"\n\nQuery:\n{query}"
    ).content

    raw_result = result.strip()

    # remove code fences if any
    cleaned = re.sub(r"^```[a-zA-Z]*\n?", "", raw_result)
    cleaned = re.sub(r"\n?```$", "", cleaned).strip()

    print("DEBUG cleaned result:", cleaned)

    result_dict = json.loads(cleaned)

    state["content"] = result_dict
    return state