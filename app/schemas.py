from pydantic import BaseModel, Field
from typing import List, Dict, Any

class RecipeSchema(BaseModel):
    """Schema for a recipe."""
    recipe_name: str = Field(..., description="Name of the recipe")
    cuisine: str = Field(..., description="Cuisine type")
    ingredients: List[str] = Field(..., description="List of ingredients")
    substitutions: Dict[str, Any] = Field(..., description="Ingredient substitutions")
    recipe_process: List[str] = Field(..., description="Step-by-step process")
    fun_facts: List[str] = Field(..., description="Fun facts about the recipe")

    class Config:
        json_schema_extra = {
            "example": {
                "recipe_name": "Spaghetti Carbonara",
                "cuisine": "Italian",
                "ingredients": ["spaghetti", "eggs", "pancetta", "parmesan cheese", "black pepper"],
                "substitutions": {"pancetta": "bacon"},
                "recipe_process": [
                    "Boil the spaghetti.",
                    "Cook the pancetta.",
                    "Mix eggs and cheese.",
                    "Combine everything and serve."
                ],
                "fun_facts": ["Carbonara is a Roman dish.", "Traditionally, no cream is used."]
            }
        } 