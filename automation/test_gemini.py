import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")
key = os.getenv("GEMINI_API_KEY", "")

from google import genai

client = genai.Client(api_key=key)

for m in ["gemini-2.5-flash-lite", "gemini-3.5-flash", "gemini-3.8-flash", "gemini-3.1-flash-lite"]:
    try:
        print(f"Testing model {m}...")
        res = client.models.generate_content(
            model=m,
            contents="Hola responde en 3 palabras"
        )
        print(f"SUCCESS {m}: {res.text.strip()}")
        break
    except Exception as e:
        print(f"FAILED {m}: {e}")
