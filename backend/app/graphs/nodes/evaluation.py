import json, re

from langchain_google_genai import ChatGoogleGenerativeAI
from backend.app.graphs.utils.state import MyState
from backend.app.graphs.utils.cookwares import cookwares
from backend.app.graphs.utils.prompts import CookingPrompt
from backend.app.graphs.utils.constants import MODEL_NAME, GEMINI_API_KEY
from backend.app.config.logging import get_logger

#Initialize logger 
logger = get_logger("evaluation") 

def evaluation_agent(state: MyState)->MyState:
    """
    Evaluates the generated recipe content against available cookwares using LLM model.
    And stores the cleaned/parses result in the state's 'evaluate' field.

    Args:
        state (MyState):
            A custom state object (dict-like) that must contain:
            - `state["content"]["content"]` (str): The recipe text/content that needs to be evaluated.

    Returns:
        MyState:
            The same `state` object updated with a new key:
            - `state["evaluate"]` (dict): A JSON-parsed dictionary containing the model's evaluation output.

    """
    logger.info("Invoking evaluation agent")
    content= state["content"]["content"]
    llm = ChatGoogleGenerativeAI(model=MODEL_NAME, google_api_key=GEMINI_API_KEY)
    prompt = CookingPrompt.EVALUATION_PROMPT.format( content=content, cookwares=cookwares)

    result = llm.invoke(prompt).content

    raw_result = result.strip()

    # remove code fences if any
    cleaned = re.sub(r"^```[a-zA-Z]*\n?", "", raw_result)
    cleaned = re.sub(r"\n?```$", "", cleaned).strip()

    print("cleaned result:", cleaned)

    result_dict = json.loads(cleaned)

    state["evaluate"] = result_dict
    return state