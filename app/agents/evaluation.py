import os, json, re
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from app.graphs.state import MyState
from app.cookwares import cookwares

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

def evaluation_agent(state: MyState):
    print("Invoking evaluation agent")
    content= state["content"]["content"]
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=API_KEY)

    result = llm.invoke(
        f""" You are an expert cooking evaluator. 
             A cooking assistant generated this content:

             Content:
             {content}

             Here are the available cookwares/tools:
             {cookwares}

             Answer the following separately:
             1. Is this content a recipe? (Respond only True or False)
             2. Can this recipe be made realistically using only the above tools? (Respond only True or False)

             Task:
             Answer the following strictly in JSON with only booleans:
             {{
               "is_recipe": True/False,
               "can_make_with_cookwares": True/False
             }}
             ***Examples:
             Content:"A basic cake recipe involves creaming together butter and sugar, adding eggs one at a time, 
             then incorporating dry ingredients (flour, baking powder, salt) and wet ingredients (milk, vanilla extract) alternately.  
             The batter is poured into a greased and floured pan and baked until a toothpick inserted comes out clean.",
             {{
               "is_recipe":True,
               "can_make_with_cookwares":False
             }}

            
             """
    ).content

    raw_result = result.strip()

    # remove code fences if any
    cleaned = re.sub(r"^```[a-zA-Z]*\n?", "", raw_result)
    cleaned = re.sub(r"\n?```$", "", cleaned).strip()

    print("cleaned result:", cleaned)

    result_dict = json.loads(cleaned)

    state["evaluate"] = result_dict
    return state