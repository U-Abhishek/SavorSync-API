#!/usr/bin/env python3
"""
Minimal recipe image updater
"""

import time
from app.database import db
from duckduckgo_search import DDGS

def update_recipe_images(overwrite=False):
    """Update recipe images in database"""
    collection = db["new_recipes"]
    
    # Create single browser instance
    with DDGS() as ddgs:
        for recipe in collection.find():
            recipe_name = recipe.get("recipe_name")
            if not recipe_name:
                continue
                
            # Skip if already has image and not overwriting
            if not overwrite and recipe.get("image_url"):
                print(f"Skipping {recipe_name} (already has image)")
                continue
                
            print(f"Processing {recipe_name}...")
            
            # Search for image using the same browser instance
            try:
                query = f"{recipe_name} recipe"
                results = ddgs.images(query, max_results=20)
                
                # Attempt to find a landscape image first
                image_url = None
                for result in results:
                    if result.get("width", 0) > result.get("height", 0):
                        image_url = result["image"]
                        break
                
                # If no landscape image is found, take the first available image
                if not image_url and results:
                    image_url = results[0]["image"]
                
                if image_url:
                    collection.update_one(
                        {"recipe_name": recipe_name},
                        {"$set": {"image_url": image_url}}
                    )
                    print(f"Updated {recipe_name} with image")
                else:
                    print(f"No image found for {recipe_name}")
                    
            except Exception as e:
                print(f"Error searching for {recipe_name}: {e}")
            
            time.sleep(1)  # Be respectful to API

if __name__ == "__main__":
    import sys
    overwrite = "--overwrite" in sys.argv
    update_recipe_images(overwrite) 