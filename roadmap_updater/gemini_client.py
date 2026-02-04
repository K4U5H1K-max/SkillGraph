import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in environment variables")

client = genai.Client(api_key=API_KEY)


def call_gemini(messages: list[str]) -> str:
    """
    messages: list of conversation strings
    returns: model response text
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages
    )
    return response.text.strip()
