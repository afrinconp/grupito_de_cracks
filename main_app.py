import streamlit as st
from PIL import Image
import os
import hashlib

from config import get_google_api_key
from gemini_api import identify_food, suggest_recipes_for_food

# --- Language & UI Text ---
UI_TEXT = {
    "en": {
        "page_title": "Food AI & Recipe Generator",
        "app_title": "🍔 Food AI & Recipe Generator",
        "app_description": "Upload an image of food, and I'll tell you what it is and suggest some recipes!",
        "sidebar_header": "Configuration",
        "api_key_input_label": "Enter your Google API Key",
        "api_key_set_success": "Google API Key set!",
        "api_key_warning": "Please enter your Google API Key to use the application.",
        "file_uploader_label": "Choose an image...",
        "new_image_info": "New image detected. Click **Identify Food & Get Recipes** to analyze it.",
        "identify_button": "Identify Food",
        "api_key_error": "Google API Key is not set. Please enter it in the sidebar.",
        "subheader_choose": "Choose a food",
        "recipe_subheader": "--- Food Identification and Recipe Report ---",
        "error_occurred": "An error occurred: {error}",
        "raw_response": "Raw Model Response: {raw_response}",
        "unexpected_error": "Unexpected or empty food details. Please check the backend.",
        "detections_header": "Detections",
        "dish_name": "Dish Name:",
        "confidence": "Confidence:",
        "description": "Description:",
        "no_recipes_info": "No recipe suggestions available for this item.",
        "multiselect_label": "🍽️ Select the foods you want:",
        "get_recipes_button": "Get Recipes",
        "at_least_one_food_warning": "Please select at least one food.",
        "fetching_recipes_spinner": "Fetching recipes...",
        "suggested_recipes_header": "Suggested Recipes:",
        "key_ingredients": "Key Ingredients:",
        "invalid_recipe_format": "Invalid recipe format: {recipe}",
        "error_getting_recipes": "Error getting recipes: {error}",
        "unexpected_format": "Unexpected format for suggested recipes: {data}"
    },
    "es": {
        "page_title": "Asesor de Comidas y Recetas",
        "app_title": "🍔 Asesor de Comidas y Recetas",
        "app_description": "¡Sube una imagen de comida y te diré qué es y te sugeriré algunas recetas!",
        "sidebar_header": "Configuración",
        "api_key_input_label": "Introduce tu Clave API de Google",
        "api_key_set_success": "¡Clave API de Google configurada!",
        "api_key_warning": "Por favor, introduce tu Clave API de Google para usar la aplicación.",
        "file_uploader_label": "Elige una imagen...",
        "new_image_info": "Nueva imagen detectada. Haz clic en **Identificar Comida y Obtener Recetas** para analizarla.",
        "identify_button": "Identificar Comida",
        "api_key_error": "La Clave API de Google no está configurada. Por favor, introdúcela en la barra lateral.",
        "subheader_choose": "Elige una comida",
        "recipe_subheader": "--- Reporte de Identificación de Comida y Recetas ---",
        "error_occurred": "Ha ocurrido un error: {error}",
        "raw_response": "Respuesta cruda del modelo: {raw_response}",
        "unexpected_error": "Detalles de comida inesperados o vacíos. Por favor, revisa el backend.",
        "detections_header": "Detecciones",
        "dish_name": "Nombre del Plato:",
        "confidence": "Confianza:",
        "description": "Descripción:",
        "no_recipes_info": "No hay sugerencias de recetas disponibles para este artículo.",
        "multiselect_label": "🍽️ Selecciona las comidas que quieras:",
        "get_recipes_button": "Obtener Recetas",
        "at_least_one_food_warning": "Por favor, selecciona al menos una comida.",
        "fetching_recipes_spinner": "Obteniendo recetas...",
        "suggested_recipes_header": "Recetas Sugeridas:",
        "key_ingredients": "Ingredientes Clave:",
        "invalid_recipe_format": "Formato de receta inválido: {recipe}",
        "error_getting_recipes": "Error al obtener recetas: {error}",
        "unexpected_format": "Formato inesperado para las recetas sugeridas: {data}"
    }
}


# ---------- helper to detect new image ----------
def _file_signature(uploaded_file):
    if not uploaded_file:
        return None
    data = uploaded_file.getvalue()
    # robust signature (content-based, not filename-based)
    return hashlib.md5(data).hexdigest()

def display_recipe_results(food_details, lang):
    t = UI_TEXT[lang]

    st.subheader(t["recipe_subheader"])

    if isinstance(food_details, dict) and "error" in food_details:
        st.error(t["error_occurred"].format(error=food_details['error']))
        if "raw_response" in food_details:
            st.code(t["raw_response"].format(raw_response=food_details['raw_response']))
        return

    if not isinstance(food_details, list) or not food_details:
        st.error(t["unexpected_error"])
        return

    st.markdown(f"### {t['detections_header']}")
    food_options = []
    for element in food_details:
        st.markdown("---")
        st.markdown(f"**{t['dish_name']}** {element.get('food_name', 'N/A')}")
        st.markdown(f"**{t['confidence']}** {element.get('confidence_score', 'N/A')}/10")
        st.markdown(f"**{t['description']}** {element.get('description', 'N/A')}")
        name = element.get("food_name")
        if name and name != "No food detected":
            food_options.append(name)
        else:
            st.info(t["no_recipes_info"])
            return

    # Layout: left = selection, right = recipes
    left_col, right_col = st.columns([1, 2], gap="large")

    with left_col:
        st.session_state.setdefault("selected_foods", [])
        st.session_state.setdefault("ready_to_show", False)
        st.session_state.setdefault("recipes", None)

        def _on_foods_change():
            st.session_state["ready_to_show"] = False
            st.session_state["recipes"] = None

        selected = st.multiselect(
            t["multiselect_label"],
            options=food_options,
            default=st.session_state["selected_foods"],
            key="selected_foods",
            on_change=_on_foods_change,
        )

        if st.button(t["get_recipes_button"]):
            if not selected:
                st.warning(t["at_least_one_food_warning"])
            else:
                with st.spinner(t["fetching_recipes_spinner"]):
                    recipes = suggest_recipes_for_food(selected, lang)
                st.session_state["recipes"] = recipes
                st.session_state["ready_to_show"] = True

    with right_col:
        if st.session_state.get("ready_to_show") and st.session_state.get("recipes"):
            st.subheader(t["suggested_recipes_header"])
            recipes_data = st.session_state["recipes"]
            if isinstance(recipes_data, list):
                for recipe in recipes_data:
                    if isinstance(recipe, dict):
                        st.markdown(f"- **{recipe.get('recipe_name', 'N/A')}**")
                        st.write(f"  **{t['description']}** {recipe.get('description', 'N/A')}")
                        st.write(f"  **{t['key_ingredients']}** {', '.join(recipe.get('key_ingredients', []))}")
                    else:
                        st.warning(t["invalid_recipe_format"].format(recipe=recipe))
            elif isinstance(recipes_data, dict) and "error" in recipes_data:
                st.warning(t["error_getting_recipes"].format(error=recipes_data['error']))
            else:
                st.warning(t["unexpected_format"].format(data=recipes_data))

def main():
    st.session_state.setdefault("language", "en")
    lang_map = {"English": "en", "Español": "es"}
    lang_selection = st.sidebar.selectbox("Language", options=list(lang_map.keys()))
    st.session_state["language"] = lang_map[lang_selection]
    t = UI_TEXT[st.session_state["language"]]

    st.set_page_config(page_title=t["page_title"], page_icon="🍔")
    st.title(t["app_title"])
    st.write(t["app_description"])

    st.sidebar.header(t["sidebar_header"])
    current_api_key = get_google_api_key()
    google_api_key_input = st.sidebar.text_input(t["api_key_input_label"], type="password", value="")
    if google_api_key_input:
        os.environ["GOOGLE_API_KEY"] = google_api_key_input
        st.sidebar.success(t["api_key_set_success"])
    elif not current_api_key:
        st.sidebar.warning(t["api_key_warning"])

    st.session_state.setdefault("uploaded_file_sig", None)

    uploaded_file = st.file_uploader(t["file_uploader_label"], type=["jpg", "jpeg", "png"], key="uploader")

    if uploaded_file is not None:
        new_sig = _file_signature(uploaded_file)
        if new_sig != st.session_state.get("uploaded_file_sig"):
            st.session_state["uploaded_file_sig"] = new_sig
            for k in ("food_details", "selected_foods", "recipes", "ready_to_show"):
                st.session_state.pop(k, None)
            st.info(t["new_image_info"])

        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image")

        if st.button(t["identify_button"], key="identify_button_food"):
            api_key_check = get_google_api_key()
            if not api_key_check:
                st.error(t["api_key_error"])
            else:
                with st.spinner("Analyzing image and generating detections..."):
                    st.session_state["food_details"] = identify_food(uploaded_file, st.session_state["language"])
                st.session_state["selected_foods"] = []
                st.session_state["recipes"] = None
                st.session_state["ready_to_show"] = False

    if "food_details" in st.session_state and st.session_state["food_details"]:
        st.subheader(t["subheader_choose"])
        display_recipe_results(st.session_state["food_details"], st.session_state["language"])

if __name__ == "__main__":
    main()
