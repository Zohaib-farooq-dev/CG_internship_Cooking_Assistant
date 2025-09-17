import os
from dotenv import load_dotenv

# Load .env file once
load_dotenv()

# === Model names ===
model_name = "gemini-2.5-flash"

# === API keys ===
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # e.g., set in .env
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

image_path = "backend/app/graphs/graph_visualization/graph-flow.png"