from pydantic import BaseModel, Field
from typing import List, Dict, Any

class Recipe(BaseModel):
    recipe_name: str = Field(..., description="Name of the recipe")
    cuisine: str = Field(..., description="Cuisine type")
    ingredients: List[str] = Field(..., description="List of ingredients")
    substitutions: Dict[str, Any] = Field(..., description="Ingredient substitutions")
    recipe_process: List[str] = Field(..., description="Step-by-step process")
    fun_facts: List[str] = Field(..., description="Fun facts about the recipe") 