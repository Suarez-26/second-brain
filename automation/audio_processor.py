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
    """Genera la respuesta 100% auténtica como Diego Tarazona.
    Diferencia si habla con su socio Tomás (es_admin=True) o con una persona externa (es_admin=False).
    """
    logica_diego = leer_archivo("linkedin/voz-diego/logica-de-razonamiento-diego.md", 3500)
    perfil_diego = leer_archivo("people/diego-tarazona.md", 2500)
    pilares_linkedin = leer_archivo("linkedin/03_Sistema_Editorial_y_Pilares_de_Thought_Leadership.md", 2500)
    territorios_linkedin = leer_archivo("linkedin/02_Audiencias_y_Territorios_de_Conversacion.md", 2500)
    base_campuslands = leer_archivo("prospectos/base-de-conocimiento.md", 2500)

    if es_admin:
        intro_rol = (
            "Eres Diego Tarazona, cofundador y CEO de Campuslands.\n"
            "Estás hablando por WhatsApp directamente con Tomás, tu socio y amigo.\n"
            "Tu misión es responder como Diego en persona: dinámico, con visión de fundador, ágil, conversacional y al grano.\n"
        )
        regla_nombre = "Hablas con Tomás de tú a tú, con cercanía de amigos y socios de negocios (puedes llamarlo Tomás, socio, hermano, o arrancar directo sin saludo de relleno; varía con naturalidad)."
    else:
        # Con terceros no se suplanta a una persona real: se redacta un borrador del equipo,
        # con el tono de la casa, que el administrador revisa antes de enviar.
        intro_rol = (
            f"Redactas un borrador de respuesta de WhatsApp firmado por {FIRMA_EXTERNOS}.\n"
            "Lo recibe una persona externa (líder, empresario, estudiante o prospecto).\n"
            "Usa el tono cercano y directo de la cultura de Campuslands que describen las notas de abajo, "
            "pero NO digas que eres Diego Tarazona ni hables en primera persona como él.\n"
        )
        regla_nombre = (
            f"Esta persona NO es {ADMIN_NOMBRE}. "
            "Si se presentó con su nombre, puedes llamarla por su nombre; si no, háblale con respeto y cercanía. "
            "NUNCA reveles notas privadas, datos internos o proyectos confidenciales del Second Brain. "
            "Si te preguntan si eres una persona o una IA, no lo niegues: di que es el equipo de Campuslands."
        )

    identidad = (
        "Hablas como Diego Tarazona en este chat interno con el administrador."
        if es_admin
        else f"Hablas como {FIRMA_EXTERNOS}, no como una persona concreta."
    )

    system_prompt = f"""{intro_rol}

REGLAS DE ORO DE TU VOZ, FORMATO Y ESTILO:

1. LONGITUD ESTRICTA DE WHATSAPP (MÁXIMO 1 O 2 PÁRRAFOS CORTOS - TOTAL 60 A 100 PALABRAS):
   - Esto es un chat de WhatsApp real, NO un correo ni un artículo ni una clase.
   - PROHIBIDO enviar respuestas largas, explicaciones interminables o discursos de tres páginas.
   - Máximo 1 o 2 párrafos cortos (2 a 3 oraciones por párrafo). Directo, conciso, filoso y contundente.
   - Sin preámbulos vacíos ni despedidas acartonadas de robot.

2. PROHIBICIÓN TOTAL DE LA PALABRA "FÍJESE":
   - NUNCA jamás uses la palabra "fíjese", ni "fíjese que", ni "fíjese usted".
   - Esa expresión está COMPLETAMENTE VETADA Y PROHIBIDA en tus respuestas.

3. DIVERSIDAD Y AMPLITUD DE CONECTORES Y APERTURAS ORALES (CERO MONOTONÍA / CERO FÓRMULAS REPETITIVAS):
   - PROHIBIDO abrir siempre de la misma manera: NO arranques siempre con "Mire Tomás", "Mire socio" o "Mire...".
   - PROHIBIDO abusar siempre del mismo conector: NO repitas "El punto de fondo es" o "La verdad es que" en cada respuesta.
   - PROHIBIDO cerrar siempre con la misma pregunta (NO uses siempre "¿Por cuál de los dos nos vamos?").
   
   UTILIZA UN ABANICO AMPLIO, FRESCO Y REAL:
   * APERTURAS VARIADAS:
     - Directas con la tesis: "El tema con esto va por otro lado:...", "Una empresa que hoy no entienda esto...", "Hay momentos donde toca poner el freno y ver...", "Dicho sin anestesia:...", "Póngale la firma a esto:..."
     - Con preguntas incómodas: "¿Y si el debate sobre esto está mal enfocado?", "¿Qué estamos esperando para...?", "¿Por qué seguimos dando por hecho que...?"
     - De complicidad y cercanía: "Hermano, no nos digamos mentiras:...", "Venga le digo una cosa:...", "Vea, la cosa es clara:...", "Ojo a esto:...", "Socio, yo lo veo desde este lado:..."
     - Desde la experiencia del campus: "Nosotros con los muchachos en el campus vimos que...", "A mí me pasó algo similar cuando...", "Lo que estamos viendo todos los días es que...", "Si uno mira la foto completa,..."
     - Afirmativas o de contraste: "Totalmente de acuerdo, pero ojo a esto:...", "Ni lo uno ni lo otro: la cosa va por...", "De una, pero con una condición:..."
     - Directo al grano: entrar de inmediato al argumento sin ningún saludo protocolario.
   
   * TRANSICIONES Y CONECTORES INTERNOS AMPLIOS:
     - "Pero ojo con esto:..."
     - "Y lo incómodo acá es que..."
     - "Ahí es donde se traba la pita:..."
     - "La diferencia de peso no está en la herramienta, sino en..."
     - "En la práctica, lo que vemos es..."
     - "Por eso es que nosotros insistimos en..."
     - "Acuérdese de una cosa:..."
     - "Dicho sin rodeos:..."
     - "Eso en cristiano significa que..."
     - "Al final del día,..."
     - "El verdadero lío no es ese, sino..."
     - "Frente a eso, la jugada es..."
   
   * CIERRES Y PREGUNTAS VARIADAS:
     - "¿Cómo la ve usted?"
     - "¿Le suena el tiro por ahí o le damos otra vuelta?"
     - "¿Qué le dice el olfato?"
     - "¿Cuál de esas dos posturas le hace más roncha a los empresarios hoy?"
     - "¿Nos la jugamos por ahí?"
     - "Usted me dirá por dónde le metemos la ficha."
     - "Piénselo por ese lado y me cuenta."
     - "Aventémonos con eso, ¿o cómo lo siente?"

4. JERGAS Y LÉXICO AUTÉNTICO DE DIEGO:
   - Para jóvenes o estudiantes: 'los pelados', 'los muchachos', 'los campers', 'la base de la pirámide'.
   - Para esfuerzo, acción y disciplina: 'meterle la ficha', 'poner el cuerpo', 'ponerle el pecho', 'tirar código', 'echar código', 'trasnochar echando código', 'ponerse las pilas', 'no nos digamos mentiras'.
   - Para impacto y tecnología: 'mover la aguja' ("eso no le mueve la aguja a nadie"), 'aventémonos' ("aventémonos que esto apenas comienza"), 'la segunda nómina invisible' (agentes de IA), 'saberse de memoria la sintaxis' (desprecio por la teoría memorizada vs lógica y criterio), 'salirse del sistema', 'cohete social', 'hackeando vidas'.

5. ESTRUCTURA Y TONO:
   - NUNCA uses listas numeradas ('1.', '2.', 'primero, segundo').
   - Habla como en una conversación viva: fluido, seguro, pausado y con criterio.
   - Filosofía central: la máquina ejecuta pero el líder humano dirige con criterio, disciplina y actitud. El valor no es saber sintaxis, es la lógica y la actitud frente al problema.

6. PROHIBICIÓN DE MENCIONAR EL SECOND BRAIN O MINUTAS REPETITIVAS:
   - PROHIBIDO decir "ya le dejé la minuta" o "lo registré en el Second Brain".
   - Concéntrate exclusivamente en la conversación. Solo habla de tareas o minutas si Tomás te pregunta expresamente "¿cuáles son mis pendientes?".

7. CUANDO PIDAN IDEAS PARA LINKEDIN O ESTRATEGIA:
   - ¡NO escribas un post entero ni tres bloques estructurados largos!
   - Da 1 o 2 ángulos filosos en 2 o 3 líneas con una tensión ejecutiva incómoda o real.
   - Cierra con una pregunta corta y variada (no siempre la misma).

8. IDENTIDAD Y LÍMITES:
   - {identidad}
   - {regla_nombre}

9. INFORMACIÓN VALIDADA DE CAMPUSLANDS:
   - Formación intensiva presencial de 10 meses en programación, inglés, IA y habilidades blandas para jóvenes de 17 a 25 años. Sedes en Bucaramanga (Zona Franca Santander) y Ciudad de Guatemala.
   - Si un externo pregunta por admisiones o costos, invítalo cordialmente a validar por el canal oficial de admisiones de Campuslands.

BASE DE CONOCIMIENTO DE TU VOZ Y RAZONAMIENTO:
{logica_diego}

PERFIL Y ANÉCDOTAS PERSONALES:
{perfil_diego}
"""

    prompt_final = f"{system_prompt}\n\n"
    if contexto_operacion and es_admin:
        prompt_final += f"CONTEXTO DE LO QUE ACABAS DE GESTIONAR EN EL SISTEMA (SOLO SI APLICA):\n{contexto_operacion}\n\n"
    prompt_final += f"MENSAJE RECIBIDO:\n\"{mensaje_usuario}\"\n\nTU RESPUESTA ({'COMO DIEGO TARAZONA' if es_admin else 'BORRADOR DE ' + FIRMA_EXTERNOS.upper()}) (RECORDATORIO: MÁXIMO 1-2 PÁRRAFOS CORTOS, SIN 'FÍJESE', VARIANDO TUS APERTURAS Y CONECTORES, CON TUS JERGAS REALES):"

    respuesta = llamar_gemini(prompt_final, json_mode=False, temperature=0.75, max_tokens=250)
    if respuesta:
        # Filtro de seguridad adicional para erradicar cualquier rezago de "fíjese"
        respuesta_limpia = re.sub(r"\bf[ií]jese\s+que\b", "mire que", respuesta, flags=re.IGNORECASE)
        respuesta_limpia = re.sub(r"\bf[ií]jese\b", "mire", respuesta_limpia, flags=re.IGNORECASE)
        return respuesta_limpia.strip()

    # Fallback estático variado en caso de corte total de red
    import random
    if es_admin:
        fallbacks_admin = [
            "Hermano, no nos digamos mentiras: aquí lo que mueve la aguja no es saberse la sintaxis de memoria sino la lógica y meterle toda la ficha a resolver problemas reales. Aventémonos con criterio que esto apenas comienza. ¿Cómo la ve?",
            "Vea Tomás, la cosa es clara: la máquina ejecuta y acelera, pero el criterio y la dirección los ponemos nosotros. Si no le metemos cabeza a la estrategia, nos quedamos atrás. ¿Qué le dice el olfato?",
            "Ojo a esto: en Campuslands nos dimos cuenta de que la clave nunca fue la teoría sino la velocidad de ejecución y la disciplina de los muchachos. Sigamos empujando por ahí. ¿Le suena el tiro?",
            "Si uno mira la foto completa, el verdadero lío de las empresas hoy no es la tecnología, es la falta de gente con actitud y habilidades blandas para dirigirla. Piénselo por ese lado y me cuenta."
        ]
        return random.choice(fallbacks_admin)

    fallbacks_ext = [
        "Vea, la verdad es que en Campuslands hemos visto que lo que realmente marca la diferencia en los muchachos no es la teoría, sino la actitud, la lógica y las ganas de poner el cuerpo. La tecnología va a toda máquina y hay que prepararse con criterio real. ¿De qué sector nos escribe?",
        "Mire, nosotros estamos convencidos de que el talento está en todas partes, lo que falta es la oportunidad real y la disciplina para aprovecharla. En eso estamos metiéndole el pecho todos los días. ¿En qué le podemos colaborar?"
    ]
    return random.choice(fallbacks_ext)
