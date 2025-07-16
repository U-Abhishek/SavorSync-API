import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGODB_URI = os.environ.get("MONGODB_URI")
    ADMIN_API_KEY = os.environ.get("ADMIN_API_KEY")
    # Add other configuration variables here as needed, e.g.:
    # API_KEY = os.environ.get("API_KEY")
