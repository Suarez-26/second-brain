import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(Path(__file__).parent.parent / ".env")
key = os.getenv("GEMINI_API_KEY", "")
client = genai.Client(api_key=key, http_options={"api_version": "v1beta"})

models = ["gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-3.5-flash"]

for m in models:
    try:
        cfg = types.GenerateContentConfig(response_mime_type="application/json")
        res = client.models.generate_content(
            model=m,
            contents="Devuelve un json con un campo 'saludo': 'hola'",
            config=cfg
        )
        print(f"SUCCESS {m}: {res.text}")
        break
    except Exception as e:
        print(f"Error {m}: {e}")
