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

# Cuisines and their recipes - 35 Global Cuisines (Popular dishes only)
CUISINES_AND_RECIPES = {
    # ASIA (12 cuisines) - 85 recipes
    "Chinese": [
        "Kung Pao Chicken",
        "Sweet and Sour Pork",
        "Peking Duck",
        "Fried Rice",
        "Dim Sum",
        "Hot and Sour Soup",
        "Mapo Tofu"
    ],
    "Indian": [
        "Chicken Tikka Masala",
        "Butter Chicken",
        "Biryani",
        "Palak Paneer",
        "Tandoori Chicken",
        "Dal Makhani",
        "Naan Bread",
        "Gulab Jamun"
    ],
    "Japanese": [
        "Sushi",
        "Ramen",
        "Tempura",
        "Teriyaki Chicken",
        "Miso Soup",
        "Tonkatsu"
    ],
    "Thai": [
        "Pad Thai",
        "Green Curry",
        "Tom Yum Soup",
        "Massaman Curry",
        "Som Tam",
        "Mango Sticky Rice"
    ],
    "Korean": [
        "Bibimbap",
        "Kimchi",
        "Bulgogi",
        "Korean Fried Chicken",
        "Tteokbokki"
    ],
    "Vietnamese": [
        "Pho",
        "Banh Mi",
        "Spring Rolls",
        "Bun Cha"
    ],
    "Indonesian": [
        "Nasi Goreng",
        "Rendang",
        "Satay",
        "Gado-Gado"
    ],
    "Filipino": [
        "Adobo",
        "Lumpia",
        "Lechon",
        "Sinigang"
    ],
    "Malaysian": [
        "Nasi Lemak",
        "Laksa",
        "Char Kway Teow",
        "Roti Canai"
    ],
    "Pakistani": [
        "Biryani",
        "Karahi",
        "Seekh Kebab"
    ],
    "Singaporean": [
        "Hainanese Chicken Rice",
        "Chili Crab",
        "Laksa"
    ],
    "Sri Lankan": [
        "Rice and Curry",
        "Kottu Roti",
        "Hoppers"
    ],

    # EUROPE (8 cuisines) - 65 recipes
    "Italian": [
        "Spaghetti Carbonara",
        "Margherita Pizza",
        "Risotto",
        "Tiramisu",
        "Lasagna",
        "Bruschetta",
        "Gnocchi",
        "Panna Cotta"
    ],
    "French": [
        "Coq au Vin",
        "Beef Bourguignon",
        "Ratatouille",
        "Croissants",
        "French Onion Soup",
        "Crème Brûlée",
        "Escargot"
    ],
    "Spanish": [
        "Paella",
        "Gazpacho",
        "Tortilla Española",
        "Jamón Ibérico",
        "Churros",
        "Patatas Bravas"
    ],
    "Greek": [
        "Moussaka",
        "Greek Salad",
        "Souvlaki",
        "Gyros",
        "Baklava",
        "Spanakopita"
    ],
    "German": [
        "Schnitzel",
        "Bratwurst",
        "Sauerkraut",
        "Pretzels",
        "Black Forest Cake"
    ],
    "Portuguese": [
        "Pastéis de Nata",
        "Bacalhau",
        "Francesinha",
        "Caldo Verde"
    ],
    "Russian": [
        "Borscht",
        "Beef Stroganoff",
        "Pelmeni",
        "Blini"
    ],
    "British": [
        "Fish and Chips",
        "Shepherd's Pie",
        "Full English Breakfast",
        "Scones with Clotted Cream"
    ],

    # NORTH AMERICA (4 cuisines) - 32 recipes
    "American": [
        "BBQ Ribs",
        "Hamburger",
        "Mac and Cheese",
        "Fried Chicken",
        "Apple Pie",
        "Buffalo Wings",
        "Pancakes",
        "Cheesecake"
    ],
    "Mexican": [
        "Tacos",
        "Guacamole",
        "Burritos",
        "Quesadillas",
        "Mole",
        "Enchiladas",
        "Churros"
    ],
    "Canadian": [
        "Poutine",
        "Tourtière",
        "Butter Tarts",
        "Maple Syrup Pancakes"
    ],
    "Guatemalan": [
        "Pepian",
        "Tamales",
        "Kak'ik"
    ],

    # MIDDLE EAST (4 cuisines) - 28 recipes
    "Lebanese": [
        "Hummus",
        "Falafel",
        "Shawarma",
        "Tabbouleh",
        "Baba Ganoush",
        "Kibbeh",
        "Manaeesh"
    ],
    "Turkish": [
        "Kebab",
        "Baklava",
        "Turkish Delight",
        "Dolma",
        "Turkish Coffee",
        "Börek"
    ],
    "Iranian": [
        "Ghormeh Sabzi",
        "Kebab Koobideh",
        "Tahdig",
        "Fesenjan"
    ],
    "Israeli": [
        "Falafel",
        "Hummus",
        "Shakshuka",
        "Sabich"
    ],

    # SOUTH AMERICA (3 cuisines) - 21 recipes
    "Brazilian": [
        "Feijoada",
        "Churrasco",
        "Açaí Bowl",
        "Coxinha",
        "Brigadeiro",
        "Caipirinha",
        "Moqueca"
    ],
    "Peruvian": [
        "Ceviche",
        "Lomo Saltado",
        "Aji de Gallina",
        "Anticuchos",
        "Pisco Sour"
    ],
    "Argentine": [
        "Asado",
        "Empanadas",
        "Milanesa",
        "Chimichurri",
        "Dulce de Leche"
    ],

    # CARIBBEAN (2 cuisines) - 12 recipes
    "Jamaican": [
        "Jerk Chicken",
        "Ackee and Saltfish",
        "Curry Goat",
        "Rice and Peas",
        "Patties",
        "Rum Punch"
    ],
    "Cuban": [
        "Ropa Vieja",
        "Cuban Sandwich",
        "Mojo Pork",
        "Black Beans and Rice",
        "Mojito",
        "Flan"
    ],

    # AFRICA (2 cuisines) - 12 recipes
    "Moroccan": [
        "Tagine",
        "Couscous",
        "Pastilla",
        "Harira",
        "Mint Tea"
    ],
    "Ethiopian": [
        "Injera",
        "Doro Wat",
        "Kitfo",
        "Shiro",
        "Ethiopian Coffee",
        "Berbere Spice"
    ],

    # OCEANIA (1 cuisine) - 5 recipes
    "Australian": [
        "Meat Pie",
        "Lamington",
        "Pavlova",
        "Flat White Coffee",
        "Tim Tam"
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
    result = generate_recipe(recipe_name, cuisine, save_to_db=True)
    
    if result:
        print("Generated recipe and saved to database:")
        print(json.dumps(result, indent=2))
    else:
        print("Failed to generate recipe")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            # Test with a single recipe
            generate_single_recipe("Kung Pao Chicken", "Chinese")
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