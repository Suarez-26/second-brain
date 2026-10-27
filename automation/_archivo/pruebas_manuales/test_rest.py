import os
import requests
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(r"c:\Users\tomas\second-brain\.env"))
key = os.getenv("GEMINI_API_KEY", "")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-lite-latest:generateContent?key={key}"
payload = {
    "contents": [{"parts": [{"text": "Genera un json con clave 'test': 'ok'"}]}],
    "generationConfig": {"responseMimeType": "application/json"}
}
r = requests.post(url, json=payload, timeout=6)
print("HTTP:", r.status_code)
if r.status_code == 200:
    print("JSON:", r.json()["candidates"][0]["content"]["parts"][0]["text"])
else:
    print("Err:", r.text)
