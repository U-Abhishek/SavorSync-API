from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class Recipe(BaseModel):
    recipe_name: str = Field(..., description="Name of the recipe")
    cuisine: str = Field(..., description="Cuisine type")
    region: str = Field(..., description="Region: Asia, North America, South America, Central America, Caribbean, Middle East, Europe, Africa, or Oceania")
    ingredients: List[str] = Field(..., description="List of ingredients")
    substitutions: Dict[str, Any] = Field(..., description="Ingredient substitutions")
    recipe_process: List[str] = Field(..., description="Step-by-step process")
    fun_facts: List[str] = Field(..., description="Fun facts about the recipe")
    cultural_insights: str = Field(..., description="Cultural background and historical context of the dish")
    image_url: Optional[str] = Field(None, description="URL of the recipe image")
    shortform_video_url: Optional[str] = Field(None, description="URL of the shortform video")
    longform_video_url: Optional[str] = Field(None, description="URL of the longform video") 