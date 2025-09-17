from langchain_google_genai import  ChatGoogleGenerativeAI
from backend.app.graphs.utils.state import MyState
from backend.app.graphs.utils.prompts import classify_prompt
from backend.app.graphs.utils.constants import model_name, GEMINI_API_KEY

def classify_agent(state: MyState):
    query = state["query"]
    llm = ChatGoogleGenerativeAI(model=model_name, google_api_key=GEMINI_API_KEY)
    prompt = classify_prompt.format(query= query)

    classifier= llm.invoke(prompt).content
    print(f"\n\n{classifier}")

    state["classifier"] = classifier
    return state