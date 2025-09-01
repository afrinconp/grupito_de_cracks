import base64
from io import BytesIO
from PIL import Image
import json

def image_to_base64(image_path: str = None, uploaded_file: BytesIO = None) -> str | None:
    """
    Converts an image file (from path or uploaded Streamlit file) to a base64 encoded string.

    Args:
        image_path (str, optional): The file path to the image. Defaults to None.
        uploaded_file (BytesIO, optional): An uploaded file object from Streamlit. Defaults to None.

    Returns:
        str | None: A base64 encoded string of the image, or None if an error occurs.
    """
    if image_path:
        try:
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')
        except FileNotFoundError:
            print(f"Error: Image file not found at {image_path}")
            return None
        except Exception as e:
            print(f"An error occurred while processing the image from path: {e}")
            return None
    elif uploaded_file:
        try:
            # Ensure the file pointer is at the beginning
            uploaded_file.seek(0)
            return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
        except Exception as e:
            print(f"An error occurred while processing the uploaded image: {e}")
            return None
    return None

def parse_json_response(response_content: str) -> dict | list | None:
    """
    Parses a JSON string from a model response, handling markdown fences and
    ensuring it's a valid JSON array even if a single object is returned.

    Args:
        response_content (str): The raw string content from the model.

    Returns:
        dict | list | None: The parsed JSON object/list, or None if parsing fails.
    """
    cleaned_content = response_content.strip()

    # Remove markdown JSON fences if present
    if cleaned_content.startswith("```json"):
        cleaned_content = cleaned_content[7:]
    if cleaned_content.endswith("```"):
        cleaned_content = cleaned_content[:-3]
    
    cleaned_content = cleaned_content.strip()

    # Ensure the content is treated as a JSON array
    if not cleaned_content.startswith("[") and not cleaned_content.endswith("]"):
        cleaned_content = f"[{cleaned_content}]"
    
    try:
        return json.loads(cleaned_content)
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        print(f"Raw content that caused error: {cleaned_content}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during JSON parsing: {e}")
        return None