import time
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")
key = os.getenv("GEMINI_API_KEY", "")

from google import genai
from google.genai import types

client = genai.Client(api_key=key)

prompt = "Eres Diego Tarazona de Campuslands. Pao te pide: 'dame una idea para linkedin sobre el avance de la IA'. Dale 3 opciones con hooks y argumentos de CEO. No menciones el Second Brain."

t0 = time.time()
res = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=prompt,
    config=types.GenerateContentConfig(temperature=0.7)
)
print("SDK latency:", round(time.time() - t0, 2), "seconds")
print("Response:\n", res.text.strip()[:300])
