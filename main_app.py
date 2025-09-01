import streamlit as st
from PIL import Image
from io import BytesIO
import os

from config import get_google_api_key
from gemini_api import identify_food_and_suggest_recipes

def display_recipe_results(food_details: list | dict):
    """
    Displays the food identification and recipe generation results in Streamlit.

    Args:
        food_details (list | dict): The result from identify_food_and_suggest_recipes.
    """
    st.subheader("--- Food Identification and Recipe Report ---")
    if "error" in food_details:
        st.error(f"An error occurred: {food_details['error']}")
        if "raw_response" in food_details:
            st.code(f"Raw Model Response: {food_details['raw_response']}")
    elif isinstance(food_details, list):
        for element in food_details:
            st.markdown("---")
            st.markdown(f"**Dish Name:** {element.get('food_name', 'N/A')}")
            st.markdown(f"**Confidence:** {element.get('confidence_score', 'N/A')}/10")
            st.markdown(f"**Description:** {element.get('description', 'N/A')}")
            
            if "suggested_recipes" in element:
                st.subheader("Suggested Recipes:")
                recipes_data = element["suggested_recipes"]
                
                # Ensure recipes_data is iterable and contains dictionaries
                if isinstance(recipes_data, list):
                    for recipe in recipes_data:
                        if isinstance(recipe, dict):
                            st.markdown(f"**- Recipe:** {recipe.get('recipe_name', 'N/A')}")
                            st.write(f"  **Description:** {recipe.get('description', 'N/A')}")
                            st.write(f"  **Key Ingredients:** {', '.join(recipe.get('key_ingredients', []))}")
                        else:
                            st.warning(f"Invalid recipe format encountered: {recipe}. Expected dictionary.")
                elif isinstance(recipes_data, dict) and "error" in recipes_data:
                    st.warning(f"Error getting recipes: {recipes_data['error']}")
                else:
                    st.warning(f"Unexpected format for suggested recipes: {recipes_data}")
            else:
                st.info("No recipe suggestions available for this item.")
    else:
        st.error("Unexpected format for food details. Please check the backend.")


def main():
    """Main function to run the Streamlit application."""
    st.set_page_config(page_title="Food AI & Recipe Generator", page_icon="🍔")

    st.title("🍔 Food AI & Recipe Generator")
    st.write("Upload an image of food, and I'll tell you what it is and suggest some recipes!")

    # API Key Input (for convenience during development/testing)
    st.sidebar.header("Configuration")
    current_api_key = get_google_api_key()
    
    api_key_placeholder = "YOUR_GOOGLE_API_KEY_HERE" if not current_api_key else current_api_key
    
    google_api_key_input = st.sidebar.text_input(
        "Enter your Google API Key",
        type="password",
        value=api_key_placeholder
    )

    if google_api_key_input and google_api_key_input != "YOUR_GOOGLE_API_KEY_HERE":
        os.environ["GOOGLE_API_KEY"] = google_api_key_input
        st.sidebar.success("Google API Key set!")
    else:
        st.sidebar.warning("Please enter your Google API Key to use the application.")


    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        st.write("")

        if st.button("Identify Food & Get Recipes"):
            api_key_check = get_google_api_key()
            if not api_key_check:
                st.error("Google API Key is not set. Please enter it in the sidebar.")
            else:
                with st.spinner("Analyzing image and generating recipes..."):
                    food_details = identify_food_and_suggest_recipes(uploaded_file)
                    display_recipe_results(food_details)

if __name__ == "__main__":
    main()