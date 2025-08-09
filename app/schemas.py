from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

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
    region: str = Field(..., description="Region: Asia, North America, South America, Central America, Caribbean, Middle East, Europe, Africa, or Oceania")
    ingredients: List[str] = Field(..., description="List of ingredients")
    substitutions: Dict[str, Any] = Field(..., description="Ingredient substitutions")
    instructions: List[str] = Field(..., description="Step-by-step process")
    fun_facts: List[str] = Field(..., description="Fun facts about the recipe")
    cultural_insights: str = Field(..., description="Cultural background and historical context of the dish")
    image_url: Optional[str] = Field(None, description="URL of the recipe image")
    shortform_video_url: Optional[str] = Field(None, description="URL of the shortform video")
    longform_video_url: Optional[str] = Field(None, description="URL of the longform video")

    class Config:
        json_schema_extra = {
            "example": {
                "recipe_name": "Spaghetti Carbonara",
                "cuisine": "Italian",
                "region": "Europe",
                "ingredients": ["spaghetti", "eggs", "pancetta", "parmesan cheese", "black pepper"],
                "substitutions": {"pancetta": "bacon"},
                "instructions": [
                    "Boil the spaghetti.",
                    "Cook the pancetta.",
                    "Mix eggs and cheese.",
                    "Combine everything and serve."
                ],
                "fun_facts": ["Carbonara is a Roman dish.", "Traditionally, no cream is used."],
                "cultural_insights": "Carbonara is a beloved Roman pasta dish that originated in the mid-20th century. It was created by coal miners (carbonai) who needed a hearty, protein-rich meal that could be made with simple ingredients. The dish represents the ingenuity of Italian cuisine, turning basic ingredients into something extraordinary. Today, it's a symbol of Roman culinary tradition and is enjoyed worldwide.",
                "image_url": "https://example.com/spaghetti-carbonara.jpg",
                "shortform_video_url": "https://example.com/spaghetti-carbonara-short.mp4",
                "longform_video_url": "https://example.com/spaghetti-carbonara-long.mp4"
            }
        } 