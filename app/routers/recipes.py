from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.schemas import RecipeSchema
from app.database import db
from bson.objectid import ObjectId

router = APIRouter(prefix="/recipes", tags=["Recipes"])

collection = db["new_recipes"]

# Helper to convert MongoDB document to dict
def recipe_helper(recipe) -> dict:
    del recipe["_id"]
    return recipe

@router.get("/", response_model=List[RecipeSchema])
def get_all_recipes():
    recipes = list(collection.find())
    print(f"Found {len(recipes)} recipes in database")
    if recipes:
        print(f"First recipe keys: {list(recipes[0].keys())}")
    return [recipe_helper(r) for r in recipes]

@router.get("/{recipe_id}", response_model=RecipeSchema)
def get_recipe(recipe_id: str):
    try:
        # Validate that recipe_id is a valid ObjectId
        if not recipe_id or recipe_id == "undefined":
            raise HTTPException(status_code=400, detail="Invalid recipe ID")
        
        recipe = collection.find_one({"_id": ObjectId(recipe_id)})
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        return recipe_helper(recipe)
    except Exception as e:
        if "InvalidId" in str(e):
            raise HTTPException(status_code=400, detail="Invalid recipe ID format")
        raise e
