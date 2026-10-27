"""Procesador avanzado de audio, reuniones y agente Diego Tarazona para Second Brain.

Capacidades:
1. Transcribe notas de voz y audios con faster-whisper (CPU int8).
2. Analiza el contenido con Google Gemini (fallback inteligente: 3.5-flash -> 3.8-flash -> 3.7-flash -> 3.5-flash-lite).
3. Clasifica:
   - Reunión / Conferencia: Genera minuta ejecutiva en sources/reuniones/ y extrae compromisos.
   - Reporte diario de actividades: Registra en journal/, tacha tareas hechas [x] y añade nuevos open loops [ ].
   - Consulta / Reflexión: Responde directamente en la voz auténtica de Diego Tarazona.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

RAIZ = Path(__file__).resolve().parent.parent
load_dotenv(RAIZ / ".env")

OPEN_LOOPS_PATH = RAIZ / "meta" / "open-loops.md"
REUNIONES_DIR = RAIZ / "sources" / "reuniones"
REUNIONES_DIR.mkdir(parents=True, exist_ok=True)
LOG_VAULT_PATH = RAIZ / "meta" / "log.md"

FALLBACK_MODELS = [
    "gemini-flash-lite-latest",
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash",
    "gemini-3.8-flash",
    "gemini-3.7-flash",
]

def registrar_log(accion: str, archivo: str, detalle: str) -> None:
    try:
        ahora = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
        with LOG_VAULT_PATH.open("a", encoding="utf-8") as f:
            f.write(f"{ahora} | {accion} | {archivo} | {detalle}\n")
    except Exception:
        pass

def leer_archivo(ruta_rel: str, max_chars: int = 4000) -> str:
    p = RAIZ / ruta_rel
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8", errors="replace")[:max_chars]

def llamar_gemini(prompt: str, json_mode: bool = False, temperature: float = 0.7, max_tokens: int | None = None) -> str:
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key:
        print("[WARN] GEMINI_API_KEY no configurada", flush=True)
        return ""

    # 1. Intentar vía SDK nativo de Google (HTTP/2 gRPC de alta velocidad)
    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=key)
        for model_name in ["gemini-flash-lite-latest", "gemini-3.1-flash-lite", "gemini-3.5-flash-lite", "gemini-3.5-flash"]:
            try:
                cfg = types.GenerateContentConfig(temperature=temperature)
                if json_mode:
                    cfg.response_mime_type = "application/json"
                if max_tokens:
                    cfg.max_output_tokens = max_tokens
                resp = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=cfg
                )
                if resp and resp.text:
                    return resp.text.strip()
            except Exception as e:
                err_msg = str(e)
                print(f"[INFO] SDK {model_name} falló ({err_msg[:60]}), probando siguiente...", flush=True)
                continue
    except Exception as e:
        print(f"[INFO] Error inicializando SDK google.genai: {e}", flush=True)

    # 2. Fallback vía REST directo
    import requests
    for model_name in ["gemini-3.5-flash", "gemini-3.1-flash-lite", "gemini-flash-lite-latest"]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={key}"
        gen_cfg: dict[str, Any] = {"temperature": temperature}
        if json_mode:
            gen_cfg["responseMimeType"] = "application/json"
        if max_tokens:
            gen_cfg["maxOutputTokens"] = max_tokens

        payload: dict[str, Any] = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": gen_cfg
        }

        try:
            resp = requests.post(url, json=payload, timeout=35)
            if resp.status_code == 200:
                data = resp.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return text.strip()
        except Exception as e:
            print(f"[INFO] REST {model_name} error ({e}), probando siguiente...", flush=True)
            continue

    return ""

def transcribir_archivo_audio(audio_path: Path) -> str:
    try:
        from faster_whisper import WhisperModel
        model = WhisperModel("base", device="cpu", compute_type="int8")
        segments, _ = model.transcribe(str(audio_path), language="es", beam_size=5)
        textos = [s.text.strip() for s in segments]
        return " ".join(textos)
    except Exception as e:
        print(f"[ERROR] faster-whisper: {e}", flush=True)
        return ""

def analizar_contenido_con_ia(texto: str) -> dict[str, Any]:
    hoy = dt.date.today().strftime("%Y-%m-%d")
    prompt = f"""Eres el cerebro analítico del Second Brain de Tomás.
Analiza el siguiente texto (que proviene de un mensaje de voz transcrito o texto enviado por WhatsApp el {hoy}):

MENSAJE RECIBIDO:
\"\"\"{texto}\"\"\"

REGLAS ESTRICTAS DE CLASIFICACIÓN:
1. "reunion": SOLO si el texto evidencia una grabación, llamada, sincronización o conferencia entre varias personas donde se tomaron acuerdos o minutas.
2. "reporte_actividades": SOLO si Tomás está INFORMANDO EXPRESAMENTE de cosas que él ya hizo o terminó hoy (ej: "hoy me reuní con...", "ya terminé el informe...", "acabo de cerrar X") O si pide explícitamente anotar una tarea (ej: "tengo que enviar la propuesta el viernes", "anota pendiente X").
3. "consulta_general": Si Tomás está preguntando algo, pidiendo opiniones, pidiendo ideas (ej: "dame una idea para LinkedIn...", "qué opinas de..."), charlando, reflexionando o pidiendo un consejo.
   EN CASO DE "consulta_general":
   - "tareas_completadas" DEBE SER [].
   - "compromisos_nuevos" DEBE SER []. NUNCA conviertas una solicitud o pregunta de Tomás en una tarea o pendiente.
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

def actualizar_open_loops(completadas: list[str], nuevas: list[str]) -> list[str]:
    """Actualiza meta/open-loops.md: tacha tareas y agrega nuevos compromisos."""
    if not OPEN_LOOPS_PATH.exists():
        return []

    lineas = OPEN_LOOPS_PATH.read_text(encoding="utf-8", errors="replace").splitlines()
    nuevas_lineas = []
    tareas_tachadas = []
    hoy_str = dt.date.today().strftime("%Y-%m-%d")

    # 1. Tachar completadas
    for linea in lineas:
        linea_mod = linea
        if linea.strip().startswith("- [ ]"):
            linea_txt = linea.lower()
            for comp in completadas:
                c_clean = comp.lower().strip()
                # Coincidencia si la tarea contiene palabras clave significativas
                palabras_clave = [p for p in re.findall(r"\w+", c_clean) if len(p) > 3]
                coincidencias = sum(1 for p in palabras_clave if p in linea_txt)
                if (c_clean in linea_txt) or (len(palabras_clave) >= 2 and coincidencias >= max(2, len(palabras_clave) - 1)):
                    linea_mod = linea.replace("- [ ]", f"- [x] ~~{linea.strip()[6:]}~~ → completado {hoy_str}")
                    tareas_tachadas.append(linea.strip()[6:])
                    registrar_log("TASK_DONE", "meta/open-loops.md", f"Completado: {comp}")
                    break
        nuevas_lineas.append(linea_mod)

    # 2. Agregar nuevas antes de la sección "## Cerrados" o al final
    indice_insercion = len(nuevas_lineas)
    for i, l in enumerate(nuevas_lineas):
        if l.strip().startswith("## Cerrados"):
            indice_insercion = i
            break

    agregadas = []
    lineas_a_insertar = []
    for n in nuevas:
        n_clean = n.strip()
        if n_clean:
            item = f"- [ ] {n_clean} (vía WhatsApp {hoy_str})"
            lineas_a_insertar.append(item)
            agregadas.append(n_clean)
            registrar_log("TASK_ADD", "meta/open-loops.md", f"Nuevo loop: {n_clean}")

    if lineas_a_insertar:
        nuevas_lineas[indice_insercion:indice_insercion] = lineas_a_insertar + [""]

    OPEN_LOOPS_PATH.write_text("\n".join(nuevas_lineas) + "\n", encoding="utf-8")
    return agregadas

def guardar_minuta_reunion(analisis: dict[str, Any], audio_filename: str = "") -> tuple[Path, str]:
    hoy = dt.date.today().strftime("%Y-%m-%d")
    asunto_raw = analisis.get("asunto", "reunion")
    asunto_slug = re.sub(r"[^a-zA-Z0-9]+", "-", asunto_raw).strip("-").lower()[:40] or "reunion"
    filename = f"{hoy}_{asunto_slug}.md"
    minuta_path = REUNIONES_DIR / filename

    asistentes_str = ", ".join(analisis.get("asistentes", [])) or "No especificados"
    temas_str = "\n".join(f"- {t}" for t in analisis.get("temas_clave", [])) or "- Varios temas discutidos."
    compromisos_str = "\n".join(f"- [ ] {c}" for c in analisis.get("compromisos_nuevos", [])) or "- No se registraron compromisos adicionales."
    decisiones_str = "\n".join(f"- {d}" for d in analisis.get("decisiones", [])) or "- Sin decisiones críticas formales."
    fuente_audio = f"sources/audio/{audio_filename}" if audio_filename else "WhatsApp directo"

    contenido = f"""---
fecha: {hoy}
tipo: reunion
asunto: {analisis.get("asunto", "Reunión")}
asistentes: [{asistentes_str}]
fuente_audio: {fuente_audio}
---

# Minuta: {analisis.get("asunto", "Reunión")}

## 1. Resumen Ejecutivo
{analisis.get("resumen_ejecutivo", "")}

## 2. Temas Discutidos
{temas_str}

## 3. Compromisos y Acuerdos
{compromisos_str}

## 4. Decisiones Clave
{decisiones_str}
"""
    minuta_path.write_text(contenido, encoding="utf-8")
    registrar_log("MEETING_MINUTES", f"sources/reuniones/{filename}", f"Minuta: {analisis.get('asunto')}")

    # Enlazar en el Journal de hoy
    journal_path = RAIZ / "journal" / f"{hoy}.md"
    nota_journal = (
        f"\n\n### 👥 Minuta de Reunión: [[sources/reuniones/{filename}|{analisis.get('asunto')}]]\n"
        f"- **Resumen:** {analisis.get('resumen_ejecutivo')}\n"
        f"- **Compromisos:** {len(analisis.get('compromisos_nuevos', []))} registrados en open-loops.\n"
    )
    if journal_path.exists():
        with open(journal_path, "a", encoding="utf-8") as f:
            f.write(nota_journal)
    else:
        journal_path.parent.mkdir(parents=True, exist_ok=True)
        journal_path.write_text(f"# Journal {hoy}\n\n## Entradas del día{nota_journal}\n", encoding="utf-8")

    return minuta_path, filename

def registrar_reporte_en_journal(analisis: dict[str, Any], texto_original: str, audio_filename: str = "") -> None:
    hoy = dt.date.today().strftime("%Y-%m-%d")
    journal_path = RAIZ / "journal" / f"{hoy}.md"
    hora = dt.datetime.now().strftime("%H:%M")

    hechos = "\n".join(f"- {h}" for h in analisis.get("hechos_realizados", []))
    if not hechos:
        hechos = f"- {texto_original}"

    entrada = f"\n\n### 🎙️ Reporte de Actividades ({hora})\n"
    if audio_filename:
        entrada += f"- **Audio:** `sources/audio/{audio_filename}`\n"
    entrada += f"{hechos}\n"

    if analisis.get("tareas_completadas"):
        entrada += f"- **Tareas cerradas:** {', '.join(analisis['tareas_completadas'])}\n"
    if analisis.get("compromisos_nuevos"):
        entrada += f"- **Nuevos pendientes:** {', '.join(analisis['compromisos_nuevos'])}\n"

    journal_path.parent.mkdir(parents=True, exist_ok=True)
    if journal_path.exists():
        with open(journal_path, "a", encoding="utf-8") as f:
            f.write(entrada)
    else:
        journal_path.write_text(f"# Journal {hoy}\n\n## Entradas del día{entrada}\n", encoding="utf-8")

    registrar_log("JOURNAL_REPORT", f"journal/{hoy}.md", f"Actividades registradas ({hora})")

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
        intro_rol = (
            "Eres Diego Tarazona, cofundador y CEO de Campuslands.\n"
            "Estás hablando por WhatsApp con una persona externa (un líder, empresario, estudiante o contacto que te escribió).\n"
            "Tu misión es atenderle como Diego Tarazona: cercano, inspirador, seguro, con criterio de fundador.\n"
        )
        regla_nombre = (
            "Esta persona NO es Tomás. No la llames Tomás bajo ninguna circunstancia. "
            "Si se presentó con su nombre, puedes llamarla por su nombre; si no, háblale con respeto y cercanía. "
            "NUNCA reveles notas privadas, datos internos o proyectos confidenciales de Tomás o del Second Brain."
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
   - Eres Diego Tarazona. Jamás digas que eres una IA o asistente virtual.
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
    prompt_final += f"MENSAJE RECIBIDO:\n\"{mensaje_usuario}\"\n\nTU RESPUESTA COMO DIEGO TARAZONA (RECORDATORIO: MÁXIMO 1-2 PÁRRAFOS CORTOS, SIN 'FÍJESE', VARIANDO TUS APERTURAS Y CONECTORES, CON TUS JERGAS REALES):"

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
