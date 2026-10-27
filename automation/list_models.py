import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")
key = os.getenv("GEMINI_API_KEY", "")

from google import genai

client = genai.Client(api_key=key)

for m in client.models.list():
    if "generateContent" in (m.supported_actions or []):
        print(m.name)
