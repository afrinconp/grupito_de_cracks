import os
import json
from io import BytesIO
from typing import List, Dict, Any, Optional

from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from config import get_google_api_key
from utils import image_to_base64, parse_json_response

def _initialize_llm(model_name: str) -> ChatGoogleGenerativeAI | None:
    """Initializes and returns a ChatGoogleGenerativeAI model."""
    api_key = get_google_api_key()
    if not api_key:
        print("Error: GOOGLE_API_KEY not found. Please set it in your .env file or Streamlit secrets.")
        return None
    return ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key)

def generate_recipes(food_name: str) -> List[Dict[str, Any]] | Dict[str, str]:
    """
    Generates 5 recipe suggestions for a given food item using the Gemini text model.

    Args:
        food_name (str): The name of the food for which to generate recipes.

    Returns:
        list: A list of dictionaries, each representing a recipe.
              Returns a dictionary with an "error" key if an issue occurs.
    """
    llm = _initialize_llm("gemini-2.0-flash")
    if not llm:
        return {"error": "Failed to initialize Gemini model for recipe generation."}

    prompt_text = f"""
    You are a culinary expert. Based on "{food_name}", suggest 5 unique and appealing recipes that one person can cook.
    
    Respond ONLY with a JSON array of objects. Each object should have the following keys:
    - "recipe_name": The name of the recipe.
    - "description": A brief, one-sentence description of the recipe.
    - "key_ingredients": A list of 3-5 essential ingredients for the recipe.

    Do not include any text, markdown formatting, or explanations outside of the JSON object.
    """

    message = HumanMessage(content=prompt_text)

    print(f"🍳 Generating recipes for {food_name}...")
    try:
        response = llm.invoke([message])
        parsed_response = parse_json_response(response.content)

        if parsed_response is None:
            return {
                "error": "Failed to parse JSON response for recipes from the model.",
                "raw_response": response.content
            }
        return parsed_response

    except Exception as e:
        return {"error": f"An unexpected error occurred during recipe generation: {e}"}


def identify_food(uploaded_file_bytes: BytesIO) -> List[Dict[str, Any]] | Dict[str, str]:
    """
    Identifies food in an image using Gemini Vision and then suggests recipes.

    Args:
        uploaded_file_bytes (BytesIO): The uploaded image file as BytesIO.

    Returns:
        list: A list of dictionaries, each containing identified food's details and
              recipe suggestions. Returns a dictionary with an "error" key if an issue occurs.
    """
    llm_vision = _initialize_llm("gemini-2.0-flash")
    if not llm_vision:
        return {"error": "Failed to initialize Gemini Vision model."}

    base64_image = image_to_base64(uploaded_file=uploaded_file_bytes)
    if not base64_image:
        return {"error": "Failed to encode the image."}

    prompt_text_vision = """
    You are an expert food identifier. Analyze the image and identify the food. If no food is present, state that clearly.
    
    Respond ONLY with a JSON object with the following keys for each food:
    - "food_name": The name of the food (e.g., "Margherita Pizza", "No food detected").
    - "description": A brief, one-sentence description of the food.
    - "confidence_score": An integer from 1 (not confident) to 10 (very confident).

    Do not include any text, markdown formatting, or explanations outside of the JSON object.
    """
    
    message_vision = HumanMessage(
        content=[
            {
                "type": "text",
                "text": prompt_text_vision,
            },
            {
                "type": "image_url",
                "image_url": f"data:image/jpeg;base64,{base64_image}"
            },
        ]
    )

    print("🤖 Sending image to Gemini for analysis...")
    try:
        response_vision = llm_vision.invoke([message_vision])
        identified_foods = parse_json_response(response_vision.content)
        
        if identified_foods is None:
            return {
                "error": "Failed to parse JSON response from the vision model.",
                "raw_response": response_vision.content
            }
        
        # Ensure identified_foods is always a list for consistent processing
        if not isinstance(identified_foods, list):
            identified_foods = [identified_foods]
        return identified_foods

    except Exception as e:
        return {"error": f"An unexpected error occurred during food identification: {e}"}

def suggest_recipes_for_food(food_name: list) -> str:
    """
    Suggests recipes for a given food name.

    Args:
        food_name (str): The name of the food item.

    Returns:
        list: A list of dictionaries, each representing a recipe.
              Returns a dictionary with an "error" key if an issue occurs.
    """
    """
    Generates 5 recipe suggestions for a given food item using the Gemini text model.

    Args:
        food_name (str): The name of the food for which to generate recipes.

    Returns:
        list: A list of dictionaries, each representing a recipe.
              Returns a dictionary with an "error" key if an issue occurs.
    """
    llm = _initialize_llm("gemini-2.0-flash")
    if not llm:
        return {"error": "Failed to initialize Gemini model for recipe generation."}
    print(food_name)

    prompt_text = f"""
    You are a culinary expert. Based on the following list of ingredients "{str(food_name)}", suggest 5 unique and appealing recipes that one person can cook.
    
    Respond ONLY with a JSON array of objects. Each object should have the following keys:
    - "recipe_name": The name of the recipe.
    - "description": A brief, one-sentence description of the recipe.
    - "key_ingredients": A list of 3-5 essential ingredients for the recipe.

    Do not include any text, markdown formatting, or explanations outside of the JSON object.
    """

    message = HumanMessage(content=prompt_text)

    print(f"🍳 Generating recipes for {food_name}...")
    try:
        response = llm.invoke([message])
        parsed_response = parse_json_response(response.content)

        if parsed_response is None:
            return {
                "error": "Failed to parse JSON response for recipes from the model.",
                "raw_response": response.content
            }
        return parsed_response

    except Exception as e:
        return {"error": f"An unexpected error occurred during recipe generation: {e}"}
    