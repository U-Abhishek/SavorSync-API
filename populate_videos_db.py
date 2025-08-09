import requests
from app.database import db
from app.config import Config
import sys

# Function to get YouTube video URL

def get_youtube_video(recipe_name: str, api_key: str, duration: str) -> str:
    """
    Searches YouTube for a recipe video with specified duration.

    Args:
        recipe_name (str): Recipe name to search.
        api_key (str): YouTube Data API key.
        duration (str): 'short', 'medium', or 'long'

    Returns:
        str: Short YouTube URL or a message if none found.
    """
    search_url = "https://www.googleapis.com/youtube/v3/search"
    query = f"{recipe_name} recipe"

    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 1,
        "videoDuration": duration,
        "key": api_key
    }

    response = requests.get(search_url, params=params)
    if response.status_code != 200:
        return f"Error: {response.status_code} - {response.text}"

    data = response.json()
    items = data.get("items", [])
    if not items:
        return f"No {duration} video found."

    video_id = items[0]["id"]["videoId"]
    return f"https://youtu.be/{video_id}"

# Functions to get short and long videos

def get_short_video(recipe_name: str, api_key: str) -> str:
    return get_youtube_video(recipe_name, api_key, duration="short")

def get_long_video(recipe_name: str, api_key: str) -> str:
    return get_youtube_video(recipe_name, api_key, duration="long")

# Main function to update the database

def update_videos_in_db(api_key: str, overwrite=False):
    collection = db["new_recipes"]
    
    for recipe in collection.find():
        recipe_name = recipe.get("recipe_name")
        if not recipe_name:
            continue
        
        # Skip if already has videos and not overwriting
        if not overwrite and recipe.get("shortform_video_url") and recipe.get("longform_video_url"):
            print(f"Skipping {recipe_name} (already has videos)")
            continue
        
        print(f"Processing {recipe_name}...")
        
        # Get video URLs
        short_video_url = get_short_video(recipe_name, api_key)
        long_video_url = get_long_video(recipe_name, api_key)
        
        # Update the database
        collection.update_one(
            {"recipe_name": recipe_name},
            {"$set": {
                "shortform_video_url": short_video_url,
                "longform_video_url": long_video_url
            }}
        )
        print(f"Updated {recipe_name} with videos")

if __name__ == "__main__":
    api_key = Config.GOOGLE_API
    if not api_key:
        print("Error: GOOGLE_API key not found in environment variables.")
    else:
        overwrite = "--overwrite" in sys.argv
        update_videos_in_db(api_key, overwrite)
        