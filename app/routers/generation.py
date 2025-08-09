from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas import RecipeSchema, RecipeGenerationRequest
from app.database import db
from app.auth import verify_admin
from app.recipe_generation import generate_recipe
from bson.objectid import ObjectId
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/generation", tags=["Recipe Generation"])

collection = db["new_recipes"]

# Helper to convert MongoDB document to dict
def recipe_helper(recipe) -> dict:
    del recipe["_id"]
    return recipe

@router.post("/recipe", response_model=RecipeSchema)
async def generate_new_recipe(
    request: RecipeGenerationRequest,
    admin_verified: bool = Depends(verify_admin)
):
    """
    Generate a new recipe using AI based on recipe name and cuisine.
    Admin authentication required.
    """
    try:
        logger.info(f"Recipe generation request: {request.recipe_name} ({request.cuisine}) - Save to DB: {request.save_to_database}")
        
        # Create the query string for recipe generation
        recipe_query = f"{request.recipe_name} {request.cuisine} cuisine recipe"
        
        # Generate the recipe using AI
        generated_recipe = generate_recipe(recipe_query)
        
        # Transform the generated recipe to match our schema
        recipe_data = {
            "recipe_name": generated_recipe.get("title", request.recipe_name),
            "cuisine": request.cuisine,
            "region": generated_recipe.get("region", "Unknown"),
            "ingredients": generated_recipe.get("ingredients", []),
            "substitutions": generated_recipe.get("substitutions", {}),
            "instructions": generated_recipe.get("instructions", []),
            "fun_facts": generated_recipe.get("fun_facts", []),
            "cultural_insights": generated_recipe.get("cultural_insights", "")
        }

        # Validate with Pydantic before saving or returning
        validated_recipe = RecipeSchema(**recipe_data)
        
        # Save to database only if requested
        if request.save_to_database:
            result = collection.insert_one(validated_recipe.model_dump())
            created_recipe = collection.find_one({"_id": result.inserted_id})
            logger.info(f"Recipe generated and saved to database: {recipe_data['recipe_name']}")
            return recipe_helper(created_recipe)
        else:
            # Return the recipe without saving to database
            logger.info(f"Recipe generated (not saved to database): {recipe_data['recipe_name']}")
            return validated_recipe
        
    except Exception as e:
        logger.error(f"Error generating recipe: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate recipe: {str(e)}"
        ) 