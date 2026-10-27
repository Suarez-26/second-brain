import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from audio_processor import responder_como_diego, analizar_contenido_con_ia

print("--- Test 1: Pregunta directa ---", flush=True)
resp = responder_como_diego("¿Qué opinas de la inteligencia artificial y los agentes?")
print("Respuesta de Diego:", resp, flush=True)

print("\n--- Test 2: Análisis de reporte ---", flush=True)
analisis = analizar_contenido_con_ia("Hoy terminé la investigación de Diego Tarazona y quedé de cuadrar la reunión con Andrés Lizarazo para el lunes.")
print("Análisis JSON:", analisis, flush=True)
