"""
LangGraph node for classifying the user's query via LLM Model.
"""
from langchain_google_genai import  ChatGoogleGenerativeAI
from backend.app.graphs.utils.state import MyState
from backend.app.graphs.utils.prompts import classify_prompt
from backend.app.graphs.utils.constants import model_name, GEMINI_API_KEY

def classify_agent(state: MyState)->MyState:
    """
    Classifies the input query into cooking relevant or irrelevant using a Google Generative AI model.
    Stores it in the state under 'classifier',
    and returns the updated state.
    """
    query = state["query"]
    llm = ChatGoogleGenerativeAI(model=model_name, google_api_key=GEMINI_API_KEY)
    prompt = classify_prompt.format(query= query)

    classifier= llm.invoke(prompt).content
    print(f"\n\n{classifier}")

    state["classifier"] = classifier
    return state