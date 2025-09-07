# 🍔 Food AI & Recipe Generator

A Streamlit web application that uses the Google Gemini Vision and Language models to identify food from an uploaded image and suggest creative recipes.

 <!-- It's highly recommended to replace this with an actual screenshot of your app! -->

## 📜 Description

This project provides a simple and intuitive interface for users to get culinary inspiration from a photo. Simply upload an image of a dish, and the application will:

1.  **Identify the Food:** Analyze the image using the Gemini Vision Pro model to determine the name of the dish, provide a short description, and give a confidence score.
2.  **Generate Recipes:** Based on the identified food, it then uses the Gemini text model to generate five unique and appealing recipe suggestions.

The application is built with Streamlit for the user interface and leverages the LangChain framework to interact with the Google Gemini API.

## ✨ Features

- **Image-based Food Recognition:** Upload any JPG, JPEG, or PNG image of a dish.
- **Detailed Identification:** Get the food's name, a description, and a confidence score.
- **AI-Powered Recipe Suggestions:** Receive 5 unique recipes for the identified food, complete with a name, description, and key ingredients.
- **Robust JSON Parsing:** Handles model responses gracefully, cleaning up markdown fences for reliable data extraction.
- **Secure API Key Management:** Uses environment variables for API key configuration, with a convenient input in the Streamlit sidebar.

## ⚙️ Technology Stack
- **Python:** 3.12.7
- **Frontend:** [Streamlit](https://streamlit.io/)
- **AI Model:** [Google Gemini Pro Vision & Gemini 2.0 Flash](https://deepmind.google/technologies/gemini/)
- **AI Framework:** [LangChain](https://www.langchain.com/) (`langchain-google-genai`)
- **Programming Language:** Python 3.9+
- **Image Processing:** Pillow (`PIL`)
- **Configuration:** python-dotenv

## 🚀 How to Run the Project Locally

Follow these instructions to get the application running on your local machine.

### 1. Prerequisites

- [Python 3.9](https://www.python.org/downloads/) or higher
- [Git](https://git-scm.com/)
- A [Google API Key](https://ai.google.dev/gemini-api/docs/api-key) for the Gemini API.

### 2. Clone the Repository

Open your terminal and clone the repository:

```bash
git clone https://github.com/your-username/grupito_de_cracks.git
cd grupito_de_cracks
```

### 3. Create a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

```bash
# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

### 4. Install Dependencies

Create a `requirements.txt` file in the root of your project with the following content:

**`requirements.txt`**
```
streamlit
pillow
langchain-google-genai
python-dotenv
```

Now, install these dependencies using pip:

```bash
pip install -r requirements.txt
```

### 5. Set Up Your API Key (Optional)

The application uses an `.env` file to manage the Google API Key.

1.  Rename the provided `.env` file or create a new one.
2.  Open the `.env` file and add your Google API Key:

**`.env`**
```
GOOGLE_API_KEY="your-actual-google-api-key-goes-here"
```

### 6. Run the Streamlit App

You are now ready to run the application! Execute the following command in your terminal:

```bash
streamlit run main_app.py
```

Your web browser should automatically open to the application's URL (usually `http://localhost:8501`). You can also enter your API key directly in the sidebar for quick testing.

## 📁 File Structure

Here's a brief overview of the key files in this project:

```
.
├── main_app.py           # The main Streamlit application file (UI and logic).
├── gemini_apy.py         # Handles all interactions with the Gemini API via LangChain.
├── utils.py              # Contains helper functions for image encoding and JSON parsing.
├── config.py             # Manages configuration, like retrieving the API key.
├── .env                  # Stores the Google API Key (ignored by git).
└── requirements.txt      # Lists all the Python dependencies for the project.
```

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements or find a bug, please feel free to open an issue or submit a pull request.

## 📝 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
