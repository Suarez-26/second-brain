"""Procesador de audio, reuniones y agente conversacional del Second Brain.

Capacidades:
1. Transcribe notas de voz con faster-whisper (modelo cargado una sola vez por proceso).
2. Analiza el contenido con Google Gemini (cadena de modelos con tiempo límite total).
3. Clasifica:
   - Reunión / Conferencia: minuta en sources/reuniones/ y propuestas de compromisos.
   - Reporte de actividades: entrada en journal/ y propuestas para open-loops.
   - Consulta / Reflexión: respuesta conversacional.

Toda escritura pasa por vault_io. open-loops.md nunca se edita directo: se crean propuestas
(ver pendientes.py) que el administrador acepta o rechaza.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import threading
import time
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

import pendientes
import vault_io
from vault_io import registrar_log  # noqa: F401  (reexportado para los bots)

RAIZ = vault_io.RAIZ
load_dotenv(RAIZ / ".env")

ADMIN_NOMBRE = os.getenv("ADMIN_NOMBRE", "Tomás")
FIRMA_EXTERNOS = os.getenv("FIRMA_EXTERNOS", "Equipo Campuslands")

# Modelos configurables sin tocar el código: GEMINI_MODELOS=modelo1,modelo2
GEMINI_MODELOS = [m.strip() for m in os.getenv("GEMINI_MODELOS", "gemini-flash-lite-latest,gemini-3.5-flash").split(",") if m.strip()]
GEMINI_TIMEOUT_TOTAL = float(os.getenv("GEMINI_TIMEOUT_TOTAL", "40"))


def leer_archivo(ruta_rel: str, max_chars: int = 4000) -> str:
    return vault_io.leer(ruta_rel, max_chars)


def llamar_gemini(prompt: str, json_mode: bool = False, temperature: float = 0.7, max_tokens: int | None = None) -> str:
    """Prueba los modelos en orden hasta agotar GEMINI_TIMEOUT_TOTAL. La key va en header, nunca en la URL."""
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key:
        print("[WARN] GEMINI_API_KEY no configurada", flush=True)
        return ""

    gen_cfg: dict[str, Any] = {"temperature": temperature}
    if json_mode:
        gen_cfg["responseMimeType"] = "application/json"
    if max_tokens:
        gen_cfg["maxOutputTokens"] = max_tokens
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": gen_cfg}
    headers = {"x-goog-api-key": key, "Content-Type": "application/json"}

    limite = time.monotonic() + GEMINI_TIMEOUT_TOTAL
    for modelo in GEMINI_MODELOS:
        restante = limite - time.monotonic()
        if restante < 3:
            break
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=min(25, restante))
            if resp.status_code == 200:
                return resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
            print(f"[INFO] Gemini {modelo} devolvió {resp.status_code}, probando el siguiente...", flush=True)
        except Exception as e:
            print(f"[INFO] Gemini {modelo} error ({type(e).__name__}), probando el siguiente...", flush=True)
    return ""


_whisper = None
_whisper_lock = threading.Lock()


def transcribir_archivo_audio(audio_path: Path) -> str:
    """Transcripción local. El modelo se carga la primera vez y se reutiliza."""
    global _whisper
    try:
        with _whisper_lock:
            if _whisper is None:
                from faster_whisper import WhisperModel
                _whisper = WhisperModel(os.getenv("WHISPER_MODELO", "base"), device="cpu", compute_type="int8")
            segments, _ = _whisper.transcribe(str(audio_path), language="es", beam_size=5)
            return " ".join(s.text.strip() for s in segments)
    except ImportError:
        print("[WARN] faster-whisper no instalado; se depende de la transcripción de Kapso.", flush=True)
    except Exception as e:
        print(f"[ERROR] faster-whisper: {e}", flush=True)
    return ""


def analizar_contenido_con_ia(texto: str) -> dict[str, Any]:
    hoy = dt.date.today().strftime("%Y-%m-%d")
    prompt = f"""Eres el cerebro analítico del Second Brain de {ADMIN_NOMBRE}.
Analiza el siguiente texto (que proviene de un mensaje de voz transcrito o texto enviado por WhatsApp el {hoy}):

MENSAJE RECIBIDO:
\"\"\"{texto}\"\"\"

REGLAS ESTRICTAS DE CLASIFICACIÓN:
1. "reunion": SOLO si el texto evidencia una grabación, llamada, sincronización o conferencia entre varias personas donde se tomaron acuerdos o minutas.
2. "reporte_actividades": SOLO si {ADMIN_NOMBRE} está INFORMANDO EXPRESAMENTE de cosas que él ya hizo o terminó hoy (ej: "hoy me reuní con...", "ya terminé el informe...", "acabo de cerrar X") O si pide explícitamente anotar una tarea (ej: "tengo que enviar la propuesta el viernes", "anota pendiente X").
3. "consulta_general": Si {ADMIN_NOMBRE} está preguntando algo, pidiendo opiniones, pidiendo ideas (ej: "dame una idea para LinkedIn...", "qué opinas de..."), charlando, reflexionando o pidiendo un consejo.
   EN CASO DE "consulta_general":
   - "tareas_completadas" DEBE SER [].
   - "compromisos_nuevos" DEBE SER []. NUNCA conviertas una solicitud o pregunta de {ADMIN_NOMBRE} en una tarea o pendiente.
   - "hechos_realizados" DEBE SER [].
   - "es_reunion" DEBE SER false.

Tu trabajo es clasificar y extraer información estructurada en JSON estricto con los siguientes campos:
{{
  "tipo": "reunion" | "reporte_actividades" | "consulta_general",
  "asunto": "<asunto breve y claro>",
  "es_reunion": true/false,
  "resumen_ejecutivo": "<resumen de lo tratado o consultado>",
  "hechos_realizados": ["<solo si reportó cosas ya hechas>"],
  "tareas_completadas": ["<solo si reportó tareas terminadas>"],
  "compromisos_nuevos": ["<solo si adquirió un nuevo compromiso explícito>"],
  "asistentes": ["<personas presentes>"],
  "decisiones": ["<decisiones tomadas>"],
  "temas_clave": ["<temas principales>"]
}}
"""
    raw = llamar_gemini(prompt, json_mode=True, temperature=0.1)
    # Limpiar posibles bloques ```json
    raw_clean = re.sub(r"^```json\s*", "", raw, flags=re.IGNORECASE)
    raw_clean = re.sub(r"\s*```$", "", raw_clean).strip()

    try:
        data = json.loads(raw_clean)
        # Validar tipo booleano
        if not isinstance(data.get("es_reunion"), bool):
            data["es_reunion"] = (data.get("tipo") == "reunion")
        return data
    except Exception as e:
        print(f"[WARN] Error parseando JSON de Gemini ({e}): {raw[:150]}", flush=True)
        # Fallback heurístico
        texto_lower = texto.lower()
        es_reu = any(k in texto_lower for k in ["reunión", "reunion", "conferencia", "llamada con", "acordamos con", "minuta"])
        return {
            "tipo": "reunion" if es_reu else "consulta_general",
            "asunto": "Nota de voz / mensaje",
            "es_reunion": es_reu,
            "resumen_ejecutivo": texto[:200],
            "hechos_realizados": [],
            "tareas_completadas": [],
            "compromisos_nuevos": [],
            "asistentes": [],
            "decisiones": [],
            "temas_clave": []
        }



def _plantilla_journal(hoy: str) -> str:
    return f"---\nfecha: {hoy}\ncontexto: personal\ntipo: journal\n---\n\n# Journal {hoy}\n\n## Entradas del día\n"


def anexar_journal(bloque: str, motivo: str) -> str:
    hoy = dt.date.today().isoformat()
    ruta = f"journal/{hoy}.md"
    vault_io.anexar(ruta, bloque, motivo, plantilla=_plantilla_journal(hoy), accion="JOURNAL")
    return ruta


def guardar_minuta_reunion(analisis: dict[str, Any], audio_filename: str = "") -> tuple[str, list[int]]:
    """Crea la minuta, la enlaza en el journal y propone (no aplica) los compromisos."""
    hoy = dt.date.today().isoformat()
    asunto = analisis.get("asunto") or "Reunión"
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", asunto).strip("-").lower()[:40] or "reunion"

    asistentes = ", ".join(analisis.get("asistentes") or []) or "No especificados"
    temas = "\n".join(f"- {t}" for t in analisis.get("temas_clave") or []) or "- Varios temas discutidos."
    compromisos = "\n".join(f"- {c}" for c in analisis.get("compromisos_nuevos") or []) or "- No se registraron compromisos."
    decisiones = "\n".join(f"- {d}" for d in analisis.get("decisiones") or []) or "- Sin decisiones formales."
    fuente = f"sources/audio/{audio_filename}" if audio_filename else "WhatsApp directo"

    contenido = f"""---
fecha: {hoy}
contexto: campuslands
tipo: reunion
calidad: resumido
asunto: "{asunto.replace('"', "'")}"
asistentes: [{asistentes}]
fuente: {fuente}
---

# Minuta: {asunto}

## 1. Resumen ejecutivo
{analisis.get("resumen_ejecutivo", "")}

## 2. Temas discutidos
{temas}

## 3. Compromisos (propuestos para open-loops, pendientes de aprobación)
{compromisos}

## 4. Decisiones
{decisiones}

Enlaces: [[journal/{hoy}]] · [[open-loops]]
"""
    ruta = vault_io.crear(f"sources/reuniones/{hoy}_{slug}.md", contenido, f"Minuta: {asunto}", accion="MEETING_MINUTES")
    propuestas = pendientes.proponer_desde_analisis(analisis, origen=ruta)
    anexar_journal(
        f"\n### 👥 Reunión: [[{ruta.removesuffix('.md')}|{asunto}]]\n"
        f"- **Resumen:** {analisis.get('resumen_ejecutivo', '')}\n"
        f"- **Propuestas para open-loops:** {len(propuestas)} (pendientes de aprobación)\n",
        f"Enlace a minuta {ruta}",
    )
    return ruta, propuestas


def registrar_reporte_en_journal(analisis: dict[str, Any], texto_original: str, audio_filename: str = "") -> tuple[str, list[int]]:
    hora = dt.datetime.now().strftime("%H:%M")
    hechos = "\n".join(f"- {h}" for h in analisis.get("hechos_realizados") or []) or f"- {texto_original}"
    entrada = f"\n### 🎙️ Reporte de actividades ({hora})\n"
    if audio_filename:
        entrada += f"- **Audio:** `sources/audio/{audio_filename}`\n"
    entrada += f"{hechos}\n"
    ruta = anexar_journal(entrada, f"Actividades registradas ({hora})")
    propuestas = pendientes.proponer_desde_analisis(analisis, origen=ruta)
    return ruta, propuestas


def registrar_nota_journal(texto: str, audio_filename: str = "") -> str:
    hora = dt.datetime.now().strftime("%H:%M")
    bloque = f"\n### 🎙️ Nota de WhatsApp ({hora})\n"
    if audio_filename:
        bloque += f"- **Audio:** `sources/audio/{audio_filename}`\n"
    bloque += f"> {texto}\n"
    return anexar_journal(bloque, f"Nota de WhatsApp ({hora})")


def responder_como_diego(mensaje_usuario: str, contexto_operacion: str = "", es_admin: bool = True, remitente: str = "") -> str:
    """Genera una respuesta con tono neutro, simple y directo a la pregunta, sin salirse del guion.
    Diferencia si habla con el administrador (es_admin=True) o con una persona externa (es_admin=False).
    """
    logica_diego = leer_archivo("linkedin/voz-diego/logica-de-razonamiento-diego.md", 3500)
    perfil_diego = leer_archivo("people/diego-tarazona.md", 2500)
    hechos_campuslands = leer_archivo("investigacion/diego-tarazona/memoria/campuslands-hechos.md", 2500)
    base_campuslands = leer_archivo("prospectos/base-de-conocimiento.md", 2500)

    if es_admin:
        intro_rol = (
            "Eres Diego Tarazona, cofundador y CEO de Campuslands.\n"
            f"Estás respondiendo por WhatsApp a {ADMIN_NOMBRE}.\n"
            "Tu misión es responder de forma neutra, simple y directa a la pregunta, sin salirte del guion validado.\n"
        )
        regla_nombre = (
            f"Hablas con {ADMIN_NOMBRE} de forma directa y profesional, sin saludos de relleno ni muletillas."
        )
    else:
        # Con terceros no se suplanta a una persona real: se redacta un borrador del equipo,
        # que el administrador revisa antes de enviar.
        intro_rol = (
            f"Redactas un borrador de respuesta de WhatsApp firmado por {FIRMA_EXTERNOS}.\n"
            "Lo recibe una persona externa (líder, empresario, estudiante o prospecto).\n"
            "Usa un tono neutro, simple y directo a la pregunta, ceñido estrictamente al guion validado de abajo, "
            "y NO digas que eres Diego Tarazona ni hables en primera persona como él.\n"
        )
        regla_nombre = (
            f"Esta persona NO es {ADMIN_NOMBRE}. "
            "Háblale con respeto y sencillez. "
            "NUNCA reveles notas privadas, datos internos o proyectos confidenciales del Second Brain. "
            "Si te preguntan si eres una persona o una IA, no lo niegues: di que es el equipo de Campuslands."
        )

    identidad = (
        "Hablas como Diego Tarazona en este chat interno con el administrador."
        if es_admin
        else f"Hablas como {FIRMA_EXTERNOS}, no como una persona concreta."
    )

    system_prompt = f"""{intro_rol}

REGLAS ESTRICTAS DE RESPUESTA:

1. TONO NEUTRO, SIMPLE Y DIRECTO A LA PREGUNTA:
   - Responde directamente lo que se pregunta desde la primera oración.
   - Usa un lenguaje neutro, sencillo, claro y conciso.
   - Máximo 1 o 2 párrafos cortos (40 a 80 palabras en total).
   - PROHIBIDO usar preámbulos vacíos, saludos largos, despedidas acartonadas, jergas forzadas, muletillas ("fíjese", "hermano", "socio", "venga le digo") o listas numeradas.
   - No agregues preguntas retóricas al final salvo que necesites un dato concreto para responder.

2. PROHIBIDO SALIRSE DEL GUION (CEÑIDO ESTRICTAMENTE A LAS FUENTES):
   - Usa ÚNICAMENTE la información que aparece en el guion y las fuentes de abajo.
   - NUNCA inventes datos, cifras, fechas, precios, becas, salarios, garantías de empleo ni sedes que no estén en la sección validada del guion.
   - Si preguntan por costos, becas, pago diferido, fechas de cohortes, cupos, requisitos de admisión o garantías laborales (datos marcados como "NO validado"), responde de forma simple y directa que ese dato puntual se confirma con el equipo de admisiones de Campuslands.
   - Si preguntan por un tema ajeno al guion, responde brevemente que no tienes información confirmada sobre ese punto y mantente dentro de los temas de Campuslands, talento y tecnología.

3. SILENCIO SOBRE EL SISTEMA INTERNO:
   - No menciones minutas ni el "Second Brain" a menos que el administrador pregunte expresamente por sus pendientes o notas.

4. IDENTIDAD Y LÍMITES:
   - {identidad}
   - {regla_nombre}

GUION Y BASE DE CONOCIMIENTO VALIDADA DE CAMPUSLANDS:
{base_campuslands}

HECHOS CORPORATIVOS VERIFICADOS DE CAMPUSLANDS:
{hechos_campuslands}

PERFIL DE DIEGO TARAZONA:
{perfil_diego}

CRITERIOS Y LÓGICA DE RESPUESTA:
{logica_diego}
"""

    prompt_final = f"{system_prompt}\n\n"
    if contexto_operacion and es_admin:
        prompt_final += f"CONTEXTO DE LO QUE ACABAS DE GESTIONAR EN EL SISTEMA (SOLO SI APLICA):\n{contexto_operacion}\n\n"
    prompt_final += (
        f"MENSAJE RECIBIDO:\n\"{mensaje_usuario}\"\n\n"
        f"TU RESPUESTA ({'COMO DIEGO TARAZONA' if es_admin else 'BORRADOR DE ' + FIRMA_EXTERNOS.upper()}) "
        "(RECORDATORIO: TONO NEUTRO, SIMPLE Y DIRECTO A LA PREGUNTA; 1-2 PÁRRAFOS CORTOS; SIN SALIRSE DEL GUION):"
    )

    respuesta = llamar_gemini(prompt_final, json_mode=False, temperature=0.2)
    if respuesta:
        respuesta_limpia = re.sub(r"\bf[ií]jese\s+que\b", "ten en cuenta que", respuesta, flags=re.IGNORECASE)
        respuesta_limpia = re.sub(r"\bf[ií]jese\b", "", respuesta_limpia, flags=re.IGNORECASE)
        return respuesta_limpia.strip()

    # Fallback neutro y ceñido al guion en caso de corte de red
    if es_admin:
        return (
            "Recibí tu mensaje. En este momento no pude consultar el modelo para darte una respuesta específica, "
            "pero el mensaje ya quedó registrado."
        )

    return (
        "Hola. En Campuslands ofrecemos formación intensiva en programación, inglés, inteligencia artificial y "
        "habilidades blandas, con sedes activas en Bucaramanga (Zona Franca Santander) y Ciudad de Guatemala. "
        "Para detalles específicos de admisiones, fechas o costos, lo confirmamos con el equipo de Campuslands."
    )
