import os
import json
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import re
from app.config import Config

load_dotenv()

# Set up LangSmith tracking environment variables
os.environ["LANGSMITH_TRACING"] = Config.LANGSMITH_TRACING
os.environ["LANGSMITH_ENDPOINT"] = Config.LANGSMITH_ENDPOINT
os.environ["LANGSMITH_API_KEY"] = Config.LANGSMITH_API_KEY
os.environ["LANGSMITH_PROJECT"] = Config.LANGSMITH_PROJECT

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


# Function to convert substitutions list to dictionary
# Each item is 'ingredient_name | substitution_name'
def substitutions_list_to_dict(substitutions_list):
    subs_dict = {}
    for item in substitutions_list:
        if '|' in item:
            key, value = item.split('|', 1)
            subs_dict[key.strip()] = value.strip()
        else:
            subs_dict[item.strip()] = None
    return subs_dict


# Function to generate a recipe using OpenAI with LangSmith tracking
def generate_recipe(recipe_query):
    llm = ChatOpenAI(
        model="gpt-4o", 
        temperature=0,
        tags=["recipe-generation", "savor-sync"]
    )
    
    prompt = (
        f"You are a world-class recipe assistant with access to real-time web search. "
        f"For the following recipe query, provide a comprehensive, up-to-date recipe including: "
        f"- Title\n- A list of ingredients (each as 'ingredient_name | quantity', e.g., 'boneless chicken | 1kg')\n- A list of substitutions (each as 'ingredient_name | substitution_name', matching the order of the ingredients list; if no good substitution, use 'none')\n- Step-by-step instructions \n- A short summary\n- 2-3 fun facts about the recipe, its history, ingredients, or cultural significance (as a list under the key 'fun_facts')\n- Region classification: Classify the recipe into one of these regions: Asia, North America, South America, Caribbean, Middle East, Europe, Africa, or Oceania\n- Cultural insights: Write a 2-4 sentence cultural background for the dish. Include where it comes from, when or why it is eaten, and any interesting cultural or historical facts or stories associated with it. Make it warm and informative, as if you're introducing it to someone new to the culture.\n"
        f"Return only a valid JSON object with keys: title, ingredients (list), substitutions (list), instructions (list), summary (string), fun_facts (list of strings), region (string), cultural_insights (string). "
        f"Do not include any explanation or markdown code block.\n\n"
        f"Recipe query: {recipe_query}"
    )
    
    # Invoke the LLM with tracking
    response = llm.invoke(prompt)
    content = response.content if hasattr(response, 'content') else response
    
    # Extract and return the JSON response
    result = extract_json_from_llm_output(content)
    # Convert substitutions to dictionary if present and is a list
    if 'substitutions' in result and isinstance(result['substitutions'], list):
        result['substitutions'] = substitutions_list_to_dict(result['substitutions'])
    return result