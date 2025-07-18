from pydantic import BaseModel, Field
from typing import List, Dict, Any

class RecipeGenerationRequest(BaseModel):
    """Schema for recipe generation request."""
    recipe_name: str = Field(..., min_length=1, max_length=100, description="Name of the recipe to generate")
    cuisine: str = Field(..., min_length=1, max_length=50, description="Cuisine type for the recipe")
    save_to_database: bool = Field(default=False, description="Whether to save the generated recipe to database")

    class Config:
        json_schema_extra = {
            "example": {
                "recipe_name": "Chicken Tikka Masala",
                "cuisine": "Indian",
                "save_to_database": False
            }
        }

class RecipeSchema(BaseModel):
    """Schema for a recipe."""
    recipe_name: str = Field(..., description="Name of the recipe")
    cuisine: str = Field(..., description="Cuisine type")
    ingredients: List[str] = Field(..., description="List of ingredients")
    substitutions: Dict[str, Any] = Field(..., description="Ingredient substitutions")
    instructions: List[str] = Field(..., description="Step-by-step process")
    fun_facts: List[str] = Field(..., description="Fun facts about the recipe")

    class Config:
        json_schema_extra = {
            "example": {
                "recipe_name": "Spaghetti Carbonara",
                "cuisine": "Italian",
                "ingredients": ["spaghetti", "eggs", "pancetta", "parmesan cheese", "black pepper"],
                "substitutions": {"pancetta": "bacon"},
                "instructions": [
                    "Boil the spaghetti.",
                    "Cook the pancetta.",
                    "Mix eggs and cheese.",
                    "Combine everything and serve."
                ],
                "fun_facts": ["Carbonara is a Roman dish.", "Traditionally, no cream is used."]
            }
        } 