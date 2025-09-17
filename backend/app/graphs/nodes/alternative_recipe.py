"""
Graph node for creating an alternative recipe using the provided
cookware list and LLM model.
"""
from backend.app.graphs.utils.state import MyState
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.app.graphs.utils.cookwares import cookwares
from backend.app.graphs.utils.prompts import alternative_prompt
from backend.app.graphs.utils.constants import model_name, GEMINI_API_KEY

def alternative_recipe_agent(state: MyState)->MyState:
    """
    Generates an alternative version of the recipe based on available cookwares.

    Takes the current recipe content from the state, formats an alternative
    recipe prompt, invokes the LLM model, and updates the state's 'content' 
    field with the modified recipe text.
    """
    print("Invoking Cookware response modifier agent")
    content= state["content"]["content"]
    llm = ChatGoogleGenerativeAI(model=model_name, google_api_key=GEMINI_API_KEY)
    prompt = alternative_prompt.format( content=content, cookwares=cookwares)
    result = llm.invoke(prompt).content

    state["content"]["content"] = result
    return state