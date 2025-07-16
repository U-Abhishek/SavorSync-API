from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.schemas import RecipeSchema
from app.database import db
from bson.objectid import ObjectId

router = APIRouter(prefix="/recipes", tags=["Recipes"])

collection = db["recipes"]

# Helper to convert MongoDB document to dict with string id
def recipe_helper(recipe) -> dict:
    recipe["id"] = str(recipe["_id"])
    del recipe["_id"]
    return recipe

@router.get("/", response_model=List[RecipeSchema])
def get_all_recipes():
    recipes = list(collection.find())
    return [recipe_helper(r) for r in recipes]

@router.get("/{recipe_id}", response_model=RecipeSchema)
def get_recipe(recipe_id: str):
    recipe = collection.find_one({"_id": ObjectId(recipe_id)})
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe_helper(recipe)
