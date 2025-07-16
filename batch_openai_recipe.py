import os
import json
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import re

load_dotenv()

# Function to extract JSON from LLM output (copied from openai_direct_recipe.py)
def extract_json_from_llm_output(output: str):
    match = re.search(r"```json\s*(\{[\s\S]*?\})\s*```", output)
    if match:
        json_str = match.group(1)
    else:
        match = re.search(r"(\{[\s\S]*\})", output)
        if match:
            json_str = match.group(1)
        else:
            json_str = output
    return json.loads(json_str)

# Function to generate a recipe using OpenAI (copied from openai_direct_recipe.py)
def generate_recipe(recipe_query):
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    prompt = (
        f"You are a world-class recipe assistant with access to real-time web search. "
        f"For the following recipe query, provide a comprehensive, up-to-date recipe including: "
        f"- Title\n- A list of ingredients\n- Step-by-step instructions\n- A short summary\n- (Optional) Notable sources or references if available.\n"
        f"Return only a valid JSON object with keys: title, ingredients (list), instructions (list), summary (string), sources (list of URLs or names if available). "
        f"Do not include any explanation or markdown code block.\n\n"
        f"Recipe query: {recipe_query}"
    )
    response = llm.invoke(prompt)
    content = response.content if hasattr(response, 'content') else response
    return extract_json_from_llm_output(content)

# List of recipes to generate
recipe_list = [
    "Butter Chicken",
    "Ramen",
    "Tiramisu",
    "Pad Thai",
    "Falafel", 
    "Pizza",
    "Sushi",
    "Burger",
    "Salad",
    "Cake",
    "Steak",
    "Fish and Chips",
]

# Ensure output directory exists
output_dir = "recipes"
os.makedirs(output_dir, exist_ok=True)

for recipe_name in recipe_list:
    print(f"Generating recipe for: {recipe_name}")
    try:
        result = generate_recipe(recipe_name)
        filename = os.path.join(output_dir, f"direct_recipe_{recipe_name.replace(' ', '_').lower()}.json")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'query': recipe_name,
                'recipe': result
            }, f, indent=2, ensure_ascii=False)
        print(f"Saved: {filename}")
    except Exception as e:
        print(f"Failed to generate recipe for {recipe_name}: {e}") 