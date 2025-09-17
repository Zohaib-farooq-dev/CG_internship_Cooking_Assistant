from backend.app.graphs.utils.state import MyState
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.app.graphs.utils.cookwares import cookwares
from backend.app.graphs.utils.prompts import alternative_prompt
from backend.app.graphs.utils.constants import model_name, GEMINI_API_KEY

def alternative_recipe_agent(state: MyState):
    print("Invoking Cookware response modifier agent")
    content= state["content"]["content"]
    llm = ChatGoogleGenerativeAI(model=model_name, google_api_key=GEMINI_API_KEY)
    prompt = alternative_prompt.format( content=content, cookwares=cookwares)
    result = llm.invoke(prompt).content

    state["content"]["content"] = result
    return state