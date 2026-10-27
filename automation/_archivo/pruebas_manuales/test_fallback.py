import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

load_dotenv(Path(__file__).parent.parent / ".env")
key = os.getenv("GEMINI_API_KEY", "")
client = genai.Client(api_key=key)

models = ["gemini-3.5-flash", "gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.5-flash-lite", "gemini-3.1-flash-lite"]

for m in models:
    try:
        print(f"Probando {m}...")
        res = client.models.generate_content(
            model=m,
            contents="Responde en una frase como Diego Tarazona sobre la IA:"
        )
        print(f"EXITO con {m}:")
        print(res.text.strip())
        break
    except Exception as e:
        print(f"Error {m}: {e}")
