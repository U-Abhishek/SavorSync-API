import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGODB_URI = os.environ.get("MONGODB_URI")
    ADMIN_API_KEY = os.environ.get("ADMIN_API_KEY")
    # LangSmith tracking configuration
    LANGSMITH_TRACING = os.environ.get("LANGSMITH_TRACING_V2", "true")
    LANGSMITH_ENDPOINT = os.environ.get("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")
    LANGSMITH_API_KEY = os.environ.get("LANGSMITH_API_KEY")
    LANGSMITH_PROJECT = os.environ.get("LANGSMITH_PROJECT", "savor-sync-recipe-generation")
    # Add other configuration variables here as needed, e.g.:
    # API_KEY = os.environ.get("API_KEY")
    GOOGLE_API = os.environ.get("GOOGLE_API") 
