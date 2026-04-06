import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

if api_key:
    genai.configure(api_key=api_key)
    models = genai.list_models()
    print("Available models:")
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            print(f"  - {model.name}")
else:
    print("GEMINI_API_KEY not found in .env")
