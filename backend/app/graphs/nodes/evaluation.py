"""
Graph node for evaluating recipe content based on cookwares using a LLM model.
"""
import json, re
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.app.graphs.utils.state import MyState
from backend.app.graphs.utils.cookwares import cookwares
from backend.app.graphs.utils.prompts import evaluation_prompt
from backend.app.graphs.utils.constants import model_name, GEMINI_API_KEY

def evaluation_agent(state: MyState)->MyState:
    """
    Evaluates the generated recipe content against available cookwares using LLM model.
    And stores the cleaned/parses result in the state's 'evaluate' field.
    """
    print("Invoking evaluation agent")
    content= state["content"]["content"]
    llm = ChatGoogleGenerativeAI(model=model_name, google_api_key=GEMINI_API_KEY)
    prompt = evaluation_prompt.format( content=content, cookwares=cookwares)

    result = llm.invoke(prompt).content

    raw_result = result.strip()

    # remove code fences if any
    cleaned = re.sub(r"^```[a-zA-Z]*\n?", "", raw_result)
    cleaned = re.sub(r"\n?```$", "", cleaned).strip()

    print("cleaned result:", cleaned)

    result_dict = json.loads(cleaned)

    state["evaluate"] = result_dict
    return state