import streamlit as st
from PIL import Image
import os, hashlib

from config import get_google_api_key
from gemini_api import identify_food, suggest_recipes_for_food

# ---------- helper to detect new image ----------
def _file_signature(uploaded_file):
    if not uploaded_file:
        return None
    data = uploaded_file.getvalue()
    # robust signature (content-based, not filename-based)
    return hashlib.md5(data).hexdigest()

def display_recipe_results(food_details):
    st.subheader("--- Food Identification and Recipe Report ---")

    if isinstance(food_details, dict) and "error" in food_details:
        st.error(f"An error occurred: {food_details['error']}")
        if "raw_response" in food_details:
            st.code(f"Raw Model Response: {food_details['raw_response']}")
        return

    if not isinstance(food_details, list) or not food_details:
        st.error("Unexpected or empty food details. Please check the backend.")
        return

    st.markdown("### Detections")
    food_options = []
    for element in food_details:
        st.markdown("---")
        st.markdown(f"**Dish Name:** {element.get('food_name', 'N/A')}")
        st.markdown(f"**Confidence:** {element.get('confidence_score', 'N/A')}/10")
        st.markdown(f"**Description:** {element.get('description', 'N/A')}")
        name = element.get("food_name")
        if name and name != "No food detected":
            food_options.append(name)
        else:
            st.info("No recipe suggestions available for this item.")
            st.error(element.get("description"))
            return


    # Layout: left = selection, right = recipes
    left_col, right_col = st.columns([1, 2], gap="large")

    with left_col:
        # defaults
        st.session_state.setdefault("selected_foods", [])
        st.session_state.setdefault("ready_to_show", False)
        st.session_state.setdefault("recipes", None)

        # Clear recipes on any selection change
        def _on_foods_change():
            st.session_state["ready_to_show"] = False
            st.session_state["recipes"] = None

        selected = st.multiselect(
            "🍽️ Select the foods you want:",
            options=food_options,
            default=st.session_state["selected_foods"],
            key="selected_foods",
            on_change=_on_foods_change,
        )

        if st.button("Get Recipes"):
            if not selected:
                st.warning("Please select at least one food.")
            else:
                with st.spinner("Fetching recipes..."):
                    recipes = suggest_recipes_for_food(selected)
                st.session_state["recipes"] = recipes
                st.session_state["ready_to_show"] = True

    with right_col:
        if st.session_state.get("ready_to_show") and st.session_state.get("recipes"):
            st.subheader("Suggested Recipes:")
            recipes_data = st.session_state["recipes"]
            if isinstance(recipes_data, list):
                for recipe in recipes_data:
                    if isinstance(recipe, dict):
                        st.markdown(f"- **{recipe.get('recipe_name', 'N/A')}**")
                        st.write(f"  **Description:** {recipe.get('description', 'N/A')}")
                        st.write(f"  **Key Ingredients:** {', '.join(recipe.get('key_ingredients', []))}")
                    else:
                        st.warning(f"Invalid recipe format: {recipe}.")
            elif isinstance(recipes_data, dict) and "error" in recipes_data:
                st.warning(f"Error getting recipes: {recipes_data['error']}")
            else:
                st.warning(f"Unexpected format for suggested recipes: {recipes_data}")

def main():
    st.set_page_config(page_title="Food AI & Recipe Generator", page_icon="🍔")
    st.title("🍔 Food AI & Recipe Generator")
    st.write("Upload an image of food, and I'll tell you what it is and suggest some recipes!")

    # Sidebar API key
    st.sidebar.header("Configuration")
    current_api_key = get_google_api_key()
    google_api_key_input = st.sidebar.text_input("Enter your Google API Key", type="password", value="")
    if google_api_key_input:
        os.environ["GOOGLE_API_KEY"] = google_api_key_input
        st.sidebar.success("Google API Key set!")
    elif not current_api_key:
        st.sidebar.warning("Please enter your Google API Key to use the application.")

    # Ensure state keys exist
    st.session_state.setdefault("uploaded_file_sig", None)

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], key="uploader")

    # ----- reset state if NEW image arrives -----
    if uploaded_file is not None:
        new_sig = _file_signature(uploaded_file)
        if new_sig != st.session_state.get("uploaded_file_sig"):
            # New image detected: clear all previous results
            st.session_state["uploaded_file_sig"] = new_sig
            for k in ("food_details", "selected_foods", "recipes", "ready_to_show"):
                st.session_state.pop(k, None)
            st.info("New image detected. Click **Identify Food & Get Recipes** to analyze it.")

        # Show the newly uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image")

        # Identify button: fetch detections for the CURRENT image only
        if st.button("Identify Food", key="identify_button_food"):
            api_key_check = get_google_api_key()
            if not api_key_check:
                st.error("Google API Key is not set. Please enter it in the sidebar.")
            else:
                with st.spinner("Analyzing image and generating detections..."):
                    st.session_state["food_details"] = identify_food(uploaded_file)
                # Reset selection/recipes after new identification
                st.session_state["selected_foods"] = []
                st.session_state["recipes"] = None
                st.session_state["ready_to_show"] = False

    # Render results OUTSIDE the button block (persist across reruns)
    if "food_details" in st.session_state and st.session_state["food_details"]:
        st.subheader("Choose a food")
        display_recipe_results(st.session_state["food_details"])

if __name__ == "__main__":
    main()

