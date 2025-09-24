from langchain_google_genai import  ChatGoogleGenerativeAI
from backend.app.graphs.utils.state import MyState
from backend.app.graphs.utils.prompts import CookingPrompt
from backend.app.graphs.utils.constants import MODEL_NAME, GEMINI_API_KEY
from backend.app.config.logging import get_logger

#Initialize logger 
logger = get_logger("classify") 

def classify_agent(state: MyState)->MyState:
    """
    Classifies the input query into cooking relevant or irrelevant using a Google Generative AI model.
    Stores it in the state under 'classifier',
    and returns the updated state.

    Args:
        state (MyState): 
            A mutable state object (typically a dict-like mapping) that must
            contain the key ``"query"`` holding the user's input text to be
            classified.

    Returns:
        MyState:
            The same state object with an additional key ``"classifier"``
            containing the model's classification result as a string.
    """
    logger.info("Invoking classify agent")
    query = state["query"]
    llm = ChatGoogleGenerativeAI(model=MODEL_NAME, google_api_key=GEMINI_API_KEY)
    prompt = CookingPrompt.CLASSIFY.format(query= query)

    classifier= llm.invoke(prompt).content
    print(f"\n\n{classifier}")

    state["classifier"] = classifier
    return state