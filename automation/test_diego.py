import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from automation.audio_processor import responder_como_diego

consultas = [
    "dame una idea para linkedin sobre el avance de la IA",
    "¿crees que deberíamos abrir inscripciones ya o esperar a la otra semana?",
    "los pelados me dijeron que están cansados de trasnochar echando código"
]

for i, q in enumerate(consultas, 1):
    print(f"=== TEST {i}: \"{q}\" ===")
    resp = responder_como_diego(q, es_admin=True)
    print(resp)
    palabras = len(resp.split())
    tiene_fijese = "fíjese" in resp.lower() or "fijese" in resp.lower()
    print(f"[Stats] Palabras: {palabras} | 'fíjese': {tiene_fijese}")
    print("\n" + "-"*50 + "\n")
