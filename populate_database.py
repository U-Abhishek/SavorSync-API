import requests
import json
import time
import os
from typing import Dict, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API endpoint configuration
BASE_URL = "http://localhost:8000"
GENERATION_ENDPOINT = f"{BASE_URL}/generation/recipe"
ADMIN_API_KEY = os.environ.get("ADMIN_API_KEY")

if not ADMIN_API_KEY:
    raise ValueError("ADMIN_API_KEY environment variable is not set. Please set it in your .env file.")

# Cuisines and their recipes
CUISINES_AND_RECIPES = {
    "Italian": [
        "Spaghetti Carbonara",
        "Margherita Pizza",
        "Risotto alla Milanese",
        "Osso Buco",
        "Tiramisu",
        "Pasta alla Norma",
        "Bruschetta",
        "Minestrone Soup",
        "Gnocchi with Pesto",
        "Panna Cotta"
    ],
    "Indian": [
        "Chicken Tikka Masala",
        "Butter Chicken",
        "Biryani",
        "Palak Paneer",
        "Tandoori Chicken",
        "Dal Makhani",
        "Naan Bread",
        "Gulab Jamun",
        "Rogan Josh",
        "Kheer"
    ],
    "Chinese": [
        "Kung Pao Chicken",
        "Sweet and Sour Pork",
        "Mapo Tofu",
        "Peking Duck",
        "Dim Sum",
        "Hot and Sour Soup",
        "General Tso's Chicken",
        "Wonton Soup",
        "Fried Rice",
        "Egg Drop Soup"
    ],
    "Mexican": [
        "Tacos al Pastor",
        "Guacamole",
        "Chiles Rellenos",
        "Mole Poblano",
        "Ceviche",
        "Tamales",
        "Pozole",
        "Churros",
        "Enchiladas",
        "Horchata"
    ],
    "Japanese": [
        "Sushi Roll",
        "Ramen",
        "Tempura",
        "Teriyaki Chicken",
        "Miso Soup",
        "Tonkatsu",
        "Gyoza",
        "Okonomiyaki",
        "Matcha Green Tea",
        "Takoyaki"
    ],
    "French": [
        "Coq au Vin",
        "Beef Bourguignon",
        "Ratatouille",
        "Quiche Lorraine",
        "French Onion Soup",
        "Crème Brûlée",
        "Croissants",
        "Bouillabaisse",
        "Tarte Tatin",
        "Escargot"
    ],
    "Thai": [
        "Pad Thai",
        "Green Curry",
        "Tom Yum Soup",
        "Massaman Curry",
        "Som Tam",
        "Pad See Ew",
        "Mango Sticky Rice",
        "Thai Basil Chicken",
        "Larb",
        "Tom Kha Gai"
    ],
    "Greek": [
        "Moussaka",
        "Souvlaki",
        "Greek Salad",
        "Spanakopita",
        "Pastitsio",
        "Dolmades",
        "Baklava",
        "Avgolemono Soup",
        "Gyros",
        "Galaktoboureko"
    ],
    "Spanish": [
        "Paella",
        "Gazpacho",
        "Tortilla Española",
        "Patatas Bravas",
        "Churros con Chocolate",
        "Jamón Ibérico",
        "Pulpo a la Gallega",
        "Crema Catalana",
        "Empanadas",
        "Sangria"
    ],
    "Korean": [
        "Bibimbap",
        "Kimchi Jjigae",
        "Bulgogi",
        "Japchae",
        "Samgyeopsal",
        "Tteokbokki",
        "Korean Fried Chicken",
        "Sundubu Jjigae",
        "Hotteok",
        "Bingsu"
    ],
    "Lebanese": [
        "Hummus",
        "Falafel",
        "Shawarma",
        "Tabbouleh",
        "Baba Ganoush",
        "Kibbeh",
        "Fattoush Salad",
        "Manaeesh",
        "Kunafa",
        "Labneh"
    ],
    "Vietnamese": [
        "Pho",
        "Banh Mi",
        "Spring Rolls",
        "Bun Cha",
        "Cao Lau",
        "Banh Xeo",
        "Com Tam",
        "Che",
        "Bun Bo Hue",
        "Goi Cuon"
    ]
}

def generate_recipe(recipe_name: str, cuisine: str, save_to_db: bool = True) -> Dict:
    """
    Generate a recipe by calling the API endpoint.
    
    Args:
        recipe_name: Name of the recipe to generate
        cuisine: Cuisine type
        save_to_db: Whether to save to database
    
    Returns:
        Response from the API
    """
    payload = {
        "recipe_name": recipe_name,
        "cuisine": cuisine,
        "save_to_database": save_to_db
    }
    
    try:
        response = requests.post(
            GENERATION_ENDPOINT,
            json=payload,
            headers={
                "Content-Type": "application/json",
                "admin-api-key": ADMIN_API_KEY
            }
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error generating {recipe_name}: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Exception generating {recipe_name}: {str(e)}")
        return None

def populate_database():
    """
    Populate the database with recipes from all cuisines.
    """
    print("Starting database population...")
    print("=" * 50)
    
    total_recipes = sum(len(recipes) for recipes in CUISINES_AND_RECIPES.values())
    current_recipe = 0
    
    successful_generations = 0
    failed_generations = 0
    
    for cuisine, recipes in CUISINES_AND_RECIPES.items():
        print(f"\nProcessing {cuisine} cuisine ({len(recipes)} recipes)...")
        print("-" * 30)
        
        for recipe_name in recipes:
            current_recipe += 1
            print(f"[{current_recipe}/{total_recipes}] Generating: {recipe_name}")
            
            result = generate_recipe(recipe_name, cuisine, save_to_db=True)
            
            if result:
                successful_generations += 1
                print(f"✓ Successfully generated: {recipe_name}")
            else:
                failed_generations += 1
                print(f"✗ Failed to generate: {recipe_name}")
            
            # Add a small delay to avoid overwhelming the API
            time.sleep(1)
    
    print("\n" + "=" * 50)
    print("Database population completed!")
    print(f"Total recipes processed: {total_recipes}")
    print(f"Successful generations: {successful_generations}")
    print(f"Failed generations: {failed_generations}")
    print(f"Success rate: {(successful_generations/total_recipes)*100:.1f}%")

def generate_single_recipe(recipe_name: str, cuisine: str):
    """
    Generate a single recipe for testing.
    
    Args:
        recipe_name: Name of the recipe
        cuisine: Cuisine type
    """
    print(f"Generating single recipe: {recipe_name} ({cuisine})")
    result = generate_recipe(recipe_name, cuisine, save_to_db=False)
    
    if result:
        print("Generated recipe:")
        print(json.dumps(result, indent=2))
    else:
        print("Failed to generate recipe")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            # Test with a single recipe
            generate_single_recipe("Chicken Tikka Masala", "Indian")
        elif sys.argv[1] == "populate":
            # Populate the entire database
            populate_database()
        else:
            print("Usage:")
            print("  python populate_database.py test    - Generate a single test recipe")
            print("  python populate_database.py populate - Populate the entire database")
    else:
        print("Usage:")
        print("  python populate_database.py test    - Generate a single test recipe")
        print("  python populate_database.py populate - Populate the entire database") 