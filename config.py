import os
from dotenv import load_dotenv

load_dotenv()

# --- Configuration for API Keys ---
# It's recommended to use Streamlit's built-in secrets management for deployed apps:
# https://docs.streamlit.io/en/stable/deploy_streamlit_app.html#share-your-app-with-streamlit-sharing
# For local development, .env is used.

def get_google_api_key() -> str | None:
    """Retrieves the Google API Key from environment variables."""
    api_key = os.getenv("GOOGLE_API_KEY")
    return api_key