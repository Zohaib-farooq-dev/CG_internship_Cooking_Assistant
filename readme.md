# Cooking Agent Project

This project is an AI-powered cooking assistant system. It uses LLMs (Google Gemini) to classify, evaluate, and adapt recipes based on available cookware. You can interact with it via FastAPI, Swagger UI, Postman, or curl.
_____

# Getting Started

## 1. Environment Setup

1. Create a `.env` file in the root of your project.
2. Add your API keys for Google Gemini and Tavily Search:

-GEMINI_API_KEY=Your_API_Key_Here
-TAVILY_API_KEY=Your_API_Key_Here
____

## 2. Installing Packages
Tip: If you are using a virtual environment (venv), make sure to activate it before installing packages
```pip install -r requirements.txt```
____

## 3. Start the Server 
```uvicorn app.main:app --reloaad```
____

## 4. Interacting with the Cooking Assistant

### 4.1. Swagger UI

Open your browser and hit the following URL
http://127.0.0.1:8000/docs
You can interact with all the endpoints here.

### 4.2. Postman

1. Open Postman and create a new POST request.

2. Set the URL to your endpoint (e.g., http://127.0.0.1:8000/process).

3. Set Content-Type to application/json.

4. Add the request body with your query in JSON format:
   ``` 
   {
    "query": "Your recipe query here"
   }
   ```

5. Send the request and see the response.

### 4.3. Curl command 
You can also test via command line using curl:
```
curl -X POST http://127.0.0.1:8000/process \
-H "Content-Type: application/json" \
-d "{\"query\": \"Your recipe query here\"}"
```
____

## 5. How it Works 

1. Classifier Agent: Determines if a query is relevant and classifies it (research_general, research_updated, irrelevant).

2. Research Agents: Generate content or find relevant answers based on classification.

3. Evaluation Agent: Checks if the generated content is a recipe and whether it can be made with available cookware.

4. Cookware Agent: If the recipe cannot be made with the available cookware, this agent generates an alternative version suitable for your tools.
