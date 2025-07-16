from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.schemas import RecipeSchema
from app.database import db
from app.auth import verify_admin
from bson.objectid import ObjectId

router = APIRouter(prefix="/admin", tags=["Admin"])

collection = db["recipes"]

# Helper to convert MongoDB document to dict with string id
def recipe_helper(recipe) -> dict:
    recipe["id"] = str(recipe["_id"])
    del recipe["_id"]
    return recipe

@router.post("/recipes", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_recipe_admin(recipe: RecipeSchema, admin: bool = Depends(verify_admin)):
    """Admin-only endpoint to create a new recipe."""
    result = collection.insert_one(recipe.model_dump())
    return {"id": str(result.inserted_id), "message": "Recipe created successfully"}

@router.put("/recipes/{recipe_id}", response_model=dict)
def update_recipe_admin(recipe_id: str, recipe: RecipeSchema, admin: bool = Depends(verify_admin)):
    """Admin-only endpoint to update a recipe."""
    result = collection.update_one({"_id": ObjectId(recipe_id)}, {"$set": recipe.model_dump()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {"message": "Recipe updated successfully"}

@router.delete("/recipes/{recipe_id}", response_model=dict)
def delete_recipe_admin(recipe_id: str, admin: bool = Depends(verify_admin)):
    """Admin-only endpoint to delete a recipe."""
    result = collection.delete_one({"_id": ObjectId(recipe_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {"message": "Recipe deleted successfully"}

@router.get("/recipes", response_model=List[RecipeSchema])
def get_all_recipes_admin(admin: bool = Depends(verify_admin)):
    """Admin-only endpoint to get all recipes."""
    recipes = list(collection.find())
    return [recipe_helper(r) for r in recipes] 