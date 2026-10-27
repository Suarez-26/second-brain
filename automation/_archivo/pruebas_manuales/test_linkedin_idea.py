import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from audio_processor import responder_como_diego, analizar_contenido_con_ia

prompt_usuario = "dame una idea para linkedin sobre el avance de la IA"

print("1. Clasificación con IA:", flush=True)
analisis = analizar_contenido_con_ia(prompt_usuario)
print(analisis, flush=True)

print("\n2. Respuesta de Diego Tarazona:", flush=True)
respuesta = responder_como_diego(prompt_usuario)
print(respuesta, flush=True)
