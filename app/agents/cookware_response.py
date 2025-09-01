import os,re,json
from app.graphs.state import MyState
from langchain_google_genai import ChatGoogleGenerativeAI
from app.cookwares import cookwares
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

def cookware_agent(state: MyState):
    content= state["content"]["content"]
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=API_KEY)

    result = llm.invoke(
        f""" You are a professional chef and recipe re-designer.
             A cooking assistant generated this content:

             Content:
             {content}
             Which is not able to make with the follwoing available cookwares 

             Here are the available cookwares/tools:
             {cookwares}
             **Important:** Generate a **concise summary in 3-4 lines only** Do not write full step-by-step instructions.
             Generate the alternatice recipe which should be cookable by above cookwares
             Suggest an **alternative version** of the recipe that can be cooked realistically using only the given cookwares.
             Mention what **extra cookware** would be required for the original recipe or original taste.

             ***Example:
             Content:" basic cake recipe involves creaming together butter and sugar, adding eggs one at a time, 
             then incorporating dry ingredients (flour, baking powder, salt) and wet ingredients (milk, vanilla extract) alternately.  
             The batter is poured into a greased and floured pan and baked until a toothpick inserted comes out clean."
             
             Response:"Cream butter and sugar using a Spatula or Whisk. Add eggs one at a time, then fold in dry ingredients (flour, baking powder, salt) alternately with milk and vanilla. 
             Pour batter into a greased Little Pot or Frying Pan, cover with a lid, and cook on low flame for 30 to 40 minutes 
             until the cake springs back when gently pressed. For original oven-like texture, a baking tin and oven would be required."

             """
    ).content

    state["content"]["content"] = result
    return state