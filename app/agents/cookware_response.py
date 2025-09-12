import os,re,json
from app.graphs.state import MyState
from langchain_google_genai import ChatGoogleGenerativeAI
from app.cookwares import cookwares
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

def cookware_agent(state: MyState):
    print("Invoking Cookware response modifier agent")
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
             **Important:** Generate a **concise summary in 5-6 lines only** **Do include all the steps in this summary. don't miss any step.** 
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

             Content:" Chicken boneless cubes are marinated with cream, yogurt, lemon juice, ginger-garlic paste, and spices, then threaded onto skewers. 
             They are cooked over a charcoal grill or in a tandoor at high heat until tender, golden brown, and infused with a smoky flavor."
             
             Response:"Marinate chicken cubes and shallow-fry them in a Frying Pan with a little butter or oil until cooked and golden. 
             For a smoky touch, heat a piece of charcoal on the Stovetop, place it in a small steel spoon inside the Little Pot with the cooked chicken, and cover to trap the smoke. 
             Use the Spatula, Whisk, and Spoon to mix, garnish, and serve a creamy, restaurant-style Malai Boti."

             """
    ).content

    state["content"]["content"] = result
    return state