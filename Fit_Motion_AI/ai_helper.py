
import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from streamlit.errors import StreamlitSecretNotFoundError

load_dotenv()

def get_api_key():
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        return api_key

    try:
        return st.secrets["GOOGLE_API_KEY"]
    except (KeyError, StreamlitSecretNotFoundError):
        return None


api_key = get_api_key()
model_name = os.getenv(
    "GEMMA_MODEL",
    "gemma4:e2b"
)

client = genai.Client(api_key=api_key) if api_key else None

def ask_gemma(prompt):
    """Send a prompt to Gemma and return its text response."""

    if client is None:
        return (
            "AI is not configured yet. Add your API key "
            "to the local .env file."
        )

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )

        if response.text:
            return response.text

        return "The model returned an empty response."

    except Exception as error:
        return (
            "I couldn't reach the AI service. Check your "
            "model ID, API access, internet connection, "
            "and usage limits.\n\n"
            f"Technical detail: {error}"
        )