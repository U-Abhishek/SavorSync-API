#!/usr/bin/env python3
"""
Check database status for recipe images
"""

from app.database import db

def main():
    print("Database Status Check")
    print("=" * 25)
    
    collection = db["new_recipes"]
    
    # Count total recipes
    total_recipes = collection.count_documents({})
    print(f"Total recipes: {total_recipes}")
    
    # Count recipes with images
    recipes_with_images = collection.count_documents({"image_url": {"$exists": True, "$ne": None}})
    print(f"Recipes with images: {recipes_with_images}")
    
    # Count recipes without images
    recipes_without_images = collection.count_documents({
        "$or": [
            {"image_url": {"$exists": False}},
            {"image_url": None}
        ]
    })
    print(f"Recipes without images: {recipes_without_images}")
    
    # Show percentage
    if total_recipes > 0:
        percentage = (recipes_with_images / total_recipes) * 100
        print(f"Coverage: {percentage:.1f}%")
    
    # Show a few examples
    print("\nSample recipes with images:")
    sample_recipes = list(collection.find({"image_url": {"$exists": True, "$ne": None}}, {"recipe_name": 1, "image_url": 1}).limit(5))
    
    for recipe in sample_recipes:
        print(f"  - {recipe['recipe_name']}")
        print(f"    Image: {recipe['image_url'][:50]}...")

if __name__ == "__main__":
    main() 