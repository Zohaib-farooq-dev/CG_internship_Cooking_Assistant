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
              - Consider that a single tool can be used for multiple steps (e.g., a Little Pot can be used for washing, marinating, and cooking). 
              - Consider creative substitutions with the available tools. 
              - If the recipe can be cooked realistically with the above tools using reasonable assumptions, respond True.


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

             Content:"Marinate chicken cubes and shallow-fry them in a Frying Pan with a little butter or oil until cooked and golden. 
             For a smoky touch, heat a piece of charcoal on the Stovetop, place it in a small steel spoon inside the Little Pot with the cooked chicken,
             and cover to trap the smoke. Use the Spatula, Whisk, and Spoon to mix, garnish, and serve a creamy, restaurant-style Malai Boti.",
             {{
               "is_recipe":True,
               "can_make_with_cookwares":True
             }}

             Content:"Chicken boneless cubes are marinated with cream, yogurt, lemon juice, ginger-garlic paste, and spices, then threaded onto skewers. 
             They are cooked over a charcoal grill or in a tandoor at high heat until tender, golden brown, and infused with a smoky flavor.",
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