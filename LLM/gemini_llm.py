
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_response(prompt: str) -> str:
    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")
    response = model.generate_content(prompt)
    return response.text
