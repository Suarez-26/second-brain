import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

load_dotenv(Path(__file__).parent.parent / ".env")
key = os.getenv("GEMINI_API_KEY", "")
client = genai.Client(api_key=key)

test_models = [
    "gemini-flash-latest",
    "gemini-flash-lite-latest",
    "gemini-3.1-flash-lite",
    "gemini-3-flash-preview",
    "gemini-2.5-pro",
    "gemini-3.1-pro-preview",
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash"
]

for m in test_models:
    try:
        res = client.models.generate_content(
            model=m,
            contents="Hola"
        )
        print(f"AVAILABLE: {m} -> {res.text.strip()[:30]}")
    except Exception as e:
        err = str(e)
        code = "503" if "503" in err else ("404" if "404" in err else err[:50])
        print(f"FAILED: {m} -> {code}")
