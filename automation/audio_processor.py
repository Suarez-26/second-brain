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

import base64
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

ADMIN_NOMBRE = os.getenv("ADMIN_NOMBRE", 'Paola Granados "Pao"')
FIRMA_EXTERNOS = os.getenv("FIRMA_EXTERNOS", "Equipo Campuslands")

# Modelos configurables sin tocar el código: GEMINI_MODELOS=modelo1,modelo2
GEMINI_MODELOS = [m.strip() for m in os.getenv("GEMINI_MODELOS", "gemini-3-flash-preview,gemini-3.5-flash,gemini-3.6-flash,gemini-flash-lite-latest").split(",") if m.strip()]
GEMINI_TIMEOUT_TOTAL = float(os.getenv("GEMINI_TIMEOUT_TOTAL", "40"))


def leer_archivo(ruta_rel: str, max_chars: int = 4000) -> str:
    return vault_io.leer(ruta_rel, max_chars)


def llamar_gemini(
    prompt: str,
    json_mode: bool = False,
    temperature: float = 0.7,
    max_tokens: int | None = None,
    image_path: Path | str | None = None,
) -> str:
    """Prueba los modelos en orden hasta agotar GEMINI_TIMEOUT_TOTAL. Soporta imágenes inline (multimodal)."""
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key:
        print("[WARN] GEMINI_API_KEY no configurada", flush=True)
        return ""

    gen_cfg: dict[str, Any] = {"temperature": temperature}
    if json_mode:
        gen_cfg["responseMimeType"] = "application/json"
    if max_tokens:
        gen_cfg["maxOutputTokens"] = max_tokens

    parts: list[dict[str, Any]] = []
    if image_path:
        p = Path(image_path)
        if p.exists():
            mime = "image/jpeg"
            suf = p.suffix.lower()
            if suf == ".png":
                mime = "image/png"
            elif suf == ".webp":
                mime = "image/webp"
            elif suf == ".gif":
                mime = "image/gif"
            try:
                b64 = base64.b64encode(p.read_bytes()).decode("utf-8")
                parts.append({"inline_data": {"mime_type": mime, "data": b64}})
            except Exception as e:
                print(f"[WARN] Error codificando imagen {p}: {e}", flush=True)

    parts.append({"text": prompt})
    payload = {"contents": [{"parts": parts}], "generationConfig": gen_cfg}
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
2. "reporte_actividades": SOLO si {ADMIN_NOMBRE} está INFORMANDO EXPRESAMENTE de tareas laborales propias terminadas hoy en su jornada (ej: "hoy me reuní con el cliente X", "ya terminé el informe financiero") O si pide explícitamente anotar un pendiente laboral formal (ej: "tengo que enviar la propuesta el viernes", "anota pendiente X").
3. "consulta_general" (INCLUYE CONSULTAS, IDEAS, PEDIDOS DE REDES Y RETROALIMENTACIÓN):
   - Si {ADMIN_NOMBRE} está pidiendo ideas, posts para LinkedIn u otras redes, consejos, opiniones, o charlando.
   - REGLA CRÍTICA DE RETROALIMENTACIÓN / CORRECCIÓN CONVERSACIONAL:
     Si {ADMIN_NOMBRE} comenta o corrige sobre una propuesta previa, rechaza un borrador o dice frases como:
     * "esta publicación ya la hice" / "ya la publiqué" / "ya lo subí"
     * "dame otra idea" / "propón otro post" / "cambia el enfoque"
     * "no me gusta esa opción" / "eso no me sirve" / "ya lo vi"
     ESTO ES ESTRICTAMENTE "consulta_general". NO es un reporte de actividades ni una tarea de trabajo.
   EN CASO DE "consulta_general":
   - "tareas_completadas" DEBE SER [].
   - "compromisos_nuevos" DEBE SER []. NUNCA conviertas una solicitud, comentario o pregunta de {ADMIN_NOMBRE} en una tarea o pendiente.
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


def analizar_imagen_con_ia(image_path: Path, caption: str = "") -> dict[str, Any]:
    """Analiza una imagen recibida (OCR, descripción, clasificación y compromisos)."""
    hoy = dt.date.today().strftime("%Y-%m-%d")
    prompt = f"""Eres el cerebro analítico del Second Brain de {ADMIN_NOMBRE}.
Analiza la siguiente imagen enviada por WhatsApp el {hoy}.
{f'PIE DE FOTO O PREGUNTA DEL USUARIO: "{caption}"' if caption else '(El usuario no incluyó pie de foto)'}

REGLAS ESTRICTAS:
- Si el usuario comparte la imagen para pedir feedback, opiniones, reflexiones o para publicarla/adaptarla a redes sociales (ej: "¿cómo ves esto para LinkedIn?", "mira esta frase"), "compromisos_nuevos" y "tareas_completadas" DEBEN SER LISTAS VACÍAS [].
- SOLO incluye "compromisos_nuevos" si hay una orden explícita de tarea o compromiso laboral a ejecutar (ej: "pagar esta factura el lunes", "enviar este contrato a X").

Clasifica y extrae información estructurada en JSON estricto con los siguientes campos:
{{
  "tipo": "documento" | "comprobante" | "pizarra" | "captura" | "foto" | "otro",
  "asunto": "<asunto muy breve y descriptivo en 3 a 6 palabras>",
  "descripcion": "<descripción clara y concisa de lo que se ve en la imagen en 1 o 2 oraciones>",
  "texto_extraido": "<transcribe el texto legible más relevante que aparezca en la imagen si lo hay, o cadena vacía si no>",
  "compromisos_nuevos": ["<solo si contiene un compromiso laboral explícito a realizar>"],
  "tareas_completadas": ["<solo si muestra una tarea terminada>"]
}}
"""
    raw = llamar_gemini(prompt, json_mode=True, temperature=0.1, image_path=image_path)
    raw_clean = re.sub(r"^```json\s*", "", raw, flags=re.IGNORECASE)
    raw_clean = re.sub(r"\s*```$", "", raw_clean).strip()
    try:
        data = json.loads(raw_clean)
        if not isinstance(data.get("compromisos_nuevos"), list):
            data["compromisos_nuevos"] = []
        if not isinstance(data.get("tareas_completadas"), list):
            data["tareas_completadas"] = []
        return data
    except Exception as e:
        print(f"[WARN] Error parseando JSON de análisis de imagen ({e}): {raw[:150]}", flush=True)
        return {
            "tipo": "imagen",
            "asunto": "Imagen recibida",
            "descripcion": "Imagen recibida",
            "texto_extraido": "",
            "compromisos_nuevos": [],
            "tareas_completadas": []
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


def registrar_imagen_en_journal(image_filename: str, caption: str, analisis: dict[str, Any]) -> tuple[str, list[int]]:
    """Registra la imagen y su análisis en el journal del día y genera propuestas si detecta compromisos."""
    hora = dt.datetime.now().strftime("%H:%M")
    desc = analisis.get("descripcion", "").strip()
    ocr = analisis.get("texto_extraido", "").strip()
    asunto = analisis.get("asunto", "Imagen").strip()

    bloque = f"\n### 📷 Imagen ({hora}): {asunto}\n"
    bloque += f"- **Archivo:** `sources/imagenes/{image_filename}`\n"
    if caption:
        bloque += f"- **Mensaje / Pie de foto:** {caption}\n"
    if desc:
        bloque += f"- **Descripción visual:** {desc}\n"
    if ocr:
        bloque += f"- **Texto en imagen (OCR):**\n> {ocr.replace(chr(10), chr(10) + '> ')}\n"

    ruta = anexar_journal(bloque, f"Imagen {image_filename} ({hora})")
    propuestas = pendientes.proponer_desde_analisis(analisis, origen=ruta)
    return ruta, propuestas


STOP_WORDS_BUSQUEDA = {
    "el", "la", "los", "las", "un", "una", "unos", "unas", "de", "del", "a", "al", "en", "con",
    "por", "para", "sin", "sobre", "y", "o", "u", "e", "que", "qué", "como", "cómo", "cuando",
    "cuándo", "donde", "dónde", "quien", "quién", "cual", "cuál", "cuales", "cuáles", "si", "no",
    "me", "te", "se", "nos", "os", "le", "les", "lo", "la", "los", "las", "mi", "mis", "tu", "tus",
    "su", "sus", "nuestro", "nuestra", "nuestros", "nuestras", "este", "esta", "estos", "estas",
    "ese", "esa", "esos", "esas", "aquel", "aquella", "aquellos", "aquellas", "esto", "eso",
    "aquello", "todo", "toda", "todos", "todas", "otro", "otra", "otros", "otras", "mismo",
    "misma", "mismos", "mismas", "tan", "tanto", "tanta", "tantos", "tantas", "mas", "más",
    "pero", "aunque", "porque", "pues", "ya", "muy", "mucho", "mucha", "muchos", "muchas",
    "poco", "poca", "pocos", "pocas", "bien", "mal", "siempre", "nunca", "jamas", "jamás",
    "hola", "buenos", "buenas", "dias", "días", "tardes", "noches", "saludos", "gracias",
    "dime", "dame", "cuentame", "cuéntame", "di", "cuenta", "responde", "responder", "manera",
    "simple", "concisa", "consisa", "pregunta", "duda", "necesidad", "nesecidad", "favor",
    "porfa", "oye", "mira", "mire", "vea", "diego", "pao"
}


def es_saludo_o_cortesia_simple(texto: str) -> bool:
    """Detecta si un mensaje es únicamente un saludo o cortesía básica."""
    t = re.sub(r"[^\w\s]", "", texto.strip().lower())
    palabras = t.split()
    if not palabras:
        return True
    saludos_directos = {
        "hola", "buenas", "buen dia", "buenos dias", "buenas tardes", "buenas noches",
        "que tal", "que mas", "hola diego", "buenas diego", "que hubo", "que hubo diego",
        "saludos", "como vas", "cómo vas", "como estas", "cómo estás"
    }
    if t in saludos_directos:
        return True
    if len(palabras) <= 3 and any(p in ["hola", "buenas", "saludos", "que tal"] for p in palabras):
        preguntas = ["donde", "dónde", "que", "qué", "como", "cómo", "cuando", "cuándo", "quien", "quién", "sede", "sedes", "tarea", "pendiente", "minuta", "journal"]
        if not any(preg in t for preg in preguntas):
            return True
    return False


def recuperar_contexto_relevante(consulta: str, es_admin: bool = True, max_bloques: int = 4) -> str:
    """Busca en el índice FTS5 (index.db) solo cuando la consulta tiene términos sustantivos de búsqueda.
    Evita búsquedas ruidosas para saludos o mensajes conversacionales simples.
    """
    if es_saludo_o_cortesia_simple(consulta):
        return ""

    terminos_clave = [t for t in re.findall(r"\w+", consulta.lower()) if len(t) > 2 and t not in STOP_WORDS_BUSQUEDA]
    if not terminos_clave:
        return ""

    bloques = []
    vistos = set()
    try:
        import indice
        con = indice.conectar()
        # Búsqueda estricta con AND de los términos clave para evitar ruido
        q_fts = " AND ".join(f'"{t}"*' if len(t) > 3 else f'"{t}"' for t in terminos_clave)
        filas = con.execute(
            """SELECT ruta, seccion, texto, bm25(bloques, 0, 6.0, 3.0, 1.0) AS puntaje
               FROM bloques WHERE bloques MATCH ?
               ORDER BY puntaje ASC LIMIT ?""",
            [q_fts, max_bloques * 3],
        ).fetchall()
        for f in filas:
            ruta = f["ruta"]
            # Excluir transcripciones crudas de podcasts y notas privadas para externos
            if "corpus_youtube_podcasts" in ruta or "05_transcripciones" in ruta:
                continue
            if not es_admin and (ruta.startswith("meta/") or ruta.startswith("journal/")):
                continue
            clave = (ruta, f["seccion"])
            if clave in vistos:
                continue
            vistos.add(clave)
            es_post_previo = "02_publicaciones" in ruta or "redes-sociales" in ruta
            if es_post_previo:
                etiqueta = f"--- [ANTECEDENTE HISTÓRICO - PUBLICACIÓN YA REALIZADA PREVIAMENTE (NO REPETIR, USAR SOLO DE REFERENCIA): {ruta}] ---"
            else:
                etiqueta = f"--- [Fuente: {ruta} | Sección: {f['seccion']}] ---"
            bloques.append(f"{etiqueta}\n{f['texto'].strip()}")
            if len(bloques) >= max_bloques:
                break
        con.close()
    except Exception as e:
        print(f"[WARN] Error recuperando contexto de index.db: {e}", flush=True)

    consulta_l = consulta.lower()
    claves_redes = [
        "linkedin", "tiktok", "tik tok", "instagram", "reel", "reels", "carrusel",
        "post", "guion", "guión", "video corto", "publicar", "publicacion", "publicación",
        "copy", "otra idea", "otro post", "otro angulo", "otro ángulo", "otro enfoque"
    ]
    if any(k in consulta_l for k in claves_redes):
        redes_txt = leer_archivo("investigacion/diego-tarazona/fuentes/redes-sociales.md", 5000)
        if redes_txt:
            bloques.append(f"--- [HISTÓRICO DE PUBLICACIONES PASADAS (NO REPETIR, USAR SOLO DE REFERENCIA): investigacion/diego-tarazona/fuentes/redes-sociales.md] ---\n{redes_txt[:3500]}")

    return "\n\n".join(bloques)


def detectar_crisis(texto: str) -> bool:
    """Detecta expresiones de autolesión o ideación de crisis para respuesta inmediata de protección."""
    t = texto.lower()
    patrones = [
        r"\bque me mate\b", r"\bmatarme\b", r"\bme quiero matar\b", r"\bsuicid",
        r"\bquitarme la vida\b", r"\bacabar con mi vida\b", r"\bno quiero vivir\b",
        r"\bme voy a matar\b", r"\bdeseo morir\b"
    ]
    return any(re.search(p, t) for p in patrones)


def responder_como_diego(
    mensaje_usuario: str,
    contexto_operacion: str = "",
    es_admin: bool = True,
    remitente: str = "",
    image_path: Path | None = None,
) -> str:
    """Genera una respuesta siempre simple, natural, humana y directa a la pregunta o necesidad.
    Diferencia si habla con el administrador (es_admin=True) o con una persona externa (es_admin=False).
    Soporta análisis visual multimodal cuando se adjunta image_path.
    """
    # 0. Protocolo de seguridad y contención emocional ante autolesión
    if detectar_crisis(mensaje_usuario):
        return (
            "Si estás pasando por un momento difícil o te sientes abrumado, por favor no estás solo y tu vida es lo más importante. "
            "En Colombia puedes comunicarte gratis y de forma confidencial a la Línea 106, a la Línea 192 (salud mental) o a la Línea de la Esperanza (018000 113 113). "
            "También puedes hablar con un profesional de la salud o con una persona de tu entera confianza. Por favor busca apoyo hoy mismo."
        )

    msg_l = mensaje_usuario.lower()
    claves_redes = [
        "linkedin", "tiktok", "tik tok", "instagram", "reel", "reels", "carrusel",
        "post", "guion", "guión", "video corto", "red social", "redes sociales",
        "publicar", "publicacion", "publicación", "copy", "otra idea", "otro post",
        "otro angulo", "otro ángulo", "otro enfoque", "ya la hice", "ya lo publiqué",
        "ya la publiqué", "ya lo subí", "ya la subí"
    ]
    es_pedido_redes = any(k in msg_l for k in claves_redes)
    es_rechazo_o_cambio_post = any(
        k in msg_l for k in [
            "ya la hice", "ya lo hice", "ya se hizo", "ya la publiqué", "ya lo publiqué",
            "ya lo subí", "ya la subí", "otra idea", "otro post", "otro ángulo", "otro angulo",
            "cambia el enfoque", "cambia el ángulo", "dame otra", "otra propuesta"
        ]
    )
    if es_rechazo_o_cambio_post:
        es_pedido_redes = True
    es_saludo = es_saludo_o_cortesia_simple(mensaje_usuario) and not image_path

    if es_admin:
        intro_rol = (
            "Eres Diego Tarazona, cofundador y CEO de Campuslands.\n"
            f"Estás respondiendo por WhatsApp a {ADMIN_NOMBRE}.\n"
            "Eres una persona real: un líder y empresario santandereano, cercano, humano, inteligente y con criterio.\n"
            "Tu misión es responder SIEMPRE de manera simple, natural, concisa y directa al grano, sin rodeos innecesarios.\n"
        )
        regla_nombre = (
            f"Hablas con {ADMIN_NOMBRE} de forma cercana, ejecutiva y natural (llámala Pao con calidez cuando amerite)."
        )
    else:
        intro_rol = (
            f"Redactas un borrador de respuesta de WhatsApp firmado por {FIRMA_EXTERNOS}.\n"
            "Lo recibe una persona externa (líder, empresario, estudiante o prospecto).\n"
            "Usa un tono educado, cercano, profesional, simple y directo a la pregunta, ceñido estrictamente al guion validado de abajo, "
            "y NO digas que eres Diego Tarazona ni hables en primera persona como él.\n"
        )
        regla_nombre = (
            f"Esta persona NO es {ADMIN_NOMBRE}. "
            "Háblale con respeto, calidez, sencillez y concisión. "
            "NUNCA reveles notas privadas, datos internos o proyectos confidenciales del Second Brain. "
            "Si te preguntan si eres una persona o una IA, no lo niegues: di que es el equipo de Campuslands."
        )

    identidad = (
        "Hablas como Diego Tarazona en este chat interno."
        if es_admin
        else f"Hablas como {FIRMA_EXTERNOS}, no como una persona concreta."
    )

    if es_pedido_redes:
        instruccion_cambio = ""
        if es_rechazo_o_cambio_post:
            instruccion_cambio = """
   - ATENCIÓN - CORRECCIÓN / OTRA IDEA SOLICITADA:
     El usuario indica que la publicación sugerida ya se hizo ("esta publicación ya la hice") o te pide otra idea / otro enfoque.
     * Reconoce con naturalidad y calidez en una sola frase breve de inicio (ej: "¡Totalmente de acuerdo Pao, démosle una vuelta con un enfoque nuevo y más provocador!").
     * E INMEDIATAMENTE entrega una NUEVA propuesta completa de publicación para LinkedIn con un hook totalmente distinto, otra anécdota o reflexión, y diferente desarrollo.
     * PROHIBIDO quedarte preguntando pasivamente "¿publicamos otra cosa o tienes un borrador?" sin dar la nueva propuesta.
"""
        regla_tono_y_formato = f"""1. ESTRUCTURA CANÓNICA DE POST / REDES SOCIALES (ADN DE DIEGO Y CAMPUSLANDS):
   El usuario pide una idea, post o guion para redes sociales. NO DES UN RESUMEN PLANO NI UN PARRAFITO CORTO.
   Entrega la pieza COMPLETA Y ESTRUCTURADA con la anatomía real de las publicaciones previas documentadas en diego_investigacion y linkedin/03_Sistema_Editorial:
{instruccion_cambio}
   - REGLA DE ORO DE ORIGINALIDAD (PROHIBIDO DUPLICAR O REPETIR POSTS ANTERIORES):
     * En las fuentes del Second Brain verás publicaciones previas que Diego ya hizo (ej: posts en LinkedIn, paneles en Econova, Innovaética, etc.).
     * Esas publicaciones son ANTECEDENTES HISTÓRICOS para que conozcas el contexto y NO repitas lo mismo.
     * NUNCA copies ni reproduzcas textualmente una publicación pasada.
     * Genera siempre una propuesta FRESCA, NUEVA y ORIGINAL: un nuevo ángulo reflexivo, una anécdota tras bambalinas, un aprendizaje posterior o una pregunta provocadora diferente.

   - SI ES LINKEDIN (Anatomía real de posts anteriores de Diego):
     * Hook (Línea 1): Afirmación provocadora, paradoja o quiebre de creencia.
     * Ritmo visual: Párrafos de 1 o 2 oraciones máximo, con amplio aire entre ellos.
     * Tensión / Contraste: La inercia tradicional vs. la velocidad real de la industria tecnológica.
     * Quiebre con viñetas: Preguntas estratégicas o datos directos.
     * Anclaje y Experiencia: Mención a Campuslands o al trabajo de campo como evidencia operativa real.
     * Cierre reflexivo: Pregunta estratégica abierta o afirmación contundente que invite a la reflexión ejecutiva.
     * Hashtags: 3 a 5 funcionales (#Campuslands, #TalentoTech, #InteligenciaArtificial).

   - SI ES TIKTOK / REELS / VIDEO CORTO (Guion vertical dinámico de 45 a 60 segundos):
     * [0-3s Hook]: Frase disruptiva al lente que frena el scroll + TEXTO SUGERIDO EN PANTALLA.
     * [3-15s Tensión]: El problema o mito común (ej. pasar 5 años en un aula con pensum desactualizado).
     * [15-40s Desarrollo / Contraste]: El modelo práctico intensivo (10 meses, 8-10 horas diarias presenciales, programación, IA, inglés, retos con empresas).
     * [40-50s Prueba / Datos]: Casos de éxito de campers, contratos en dólares o empleo en multinacionales.
     * [50-60s Cierre / CTA]: Frase contundente de impacto o el lema insignia de Campuslands ("GOFORIT!").

   - SI ES INSTAGRAM (Carrusel o Post):
     * Portada: Título gancho con estética terminal/código (tags </...>, llaves, Poppins/Roboto Mono).
     * Diapositivas (Slides 1 a 5): Problema → Por qué falla el método convencional → El nuevo modelo → Evidencia → Conclusión.
     * Copy de pie de foto (Caption): Párrafos cortos con gancho y hashtags oficiales."""
    else:
        regla_tono_y_formato = """1. REGLA FUNDAMENTAL: RESPUESTAS SIEMPRE SIMPLES, CONCISAS Y NATURALES
   - Responde de forma directa, humana, relajada y al grano. WhatsApp es un canal ágil: sé breve, claro y natural.
   - Longitud estricta: 1 a 3 oraciones cortas (máximo 40 a 60 palabras). Si te piden una lista de datos (ej. sedes), usa viñetas cortas y limpias sin rodeos ni relleno histórico.
   - NUNCA des discursos, ni sermones, ni explicaciones no solicitadas, ni preámbulos vacíos ("Mirá, te cuento rápido...", "Hola Pao, ¿cómo van las cosas?...").
   - NUNCA te salgas de contexto. Responde ÚNICAMENTE a lo que la persona acaba de decir o preguntar.

2. CÓMO MANEJAR CASOS COMUNES:
   - SALUDOS ("Hola", "Buenas", "¿Qué tal?"):
     Responde con un saludo natural, cálido y BREVE en UNA sola oración (ej: "¡Hola Pao! ¿Cómo vas? ¿En qué te ayudo hoy?").
     ESTÁ COMPLETAMENTE PROHIBIDO hablar de la familia, la salud o retos de Campuslands si solo te saludaron.
   - PREGUNTAS POR FAMILIA O BIENESTAR ("¿cómo estás?", "¿cómo está la familia?"):
     Responde breve y cercano en una frase (ej: "Todo muy bien por acá con la familia, gracias a Dios. ¿Y tú, cómo vas?").
   - SI PIDEN DATOS O INFORMACIÓN (ej. sedes):
     Entrega los datos de forma limpia y directa, sin anécdotas históricas no pedidas ni adornos.
   - SI TE PREGUNTAN QUÉ HACES CUANDO ALGUIEN NO CREE O NO QUIERE CAMPUSLANDS:
     Responde con la postura real Hunter de forma simple y contundente (1-2 oraciones): "No nos desgastamos rogando ni convenciendo a nadie. El modelo exige 8 a 10 horas de código diario y disciplina; no es para todos. Nuestro foco total está en los jóvenes que sí quieren meterle la ficha y transformar su vida con tecnología."
   - SI TE DAN UNA INSTRUCCIÓN O FEEDBACK (ej. "responde simple y conciso"):
     Acepta con naturalidad y brevedad: "Entendido, seré breve y directo a lo que necesites. ¿En qué te colaboro hoy?".
   - SI UN MENSAJE NO SE ENTIENDE O ES CONFUSO:
     Pregunta con naturalidad: "No te entendí bien esa última frase, ¿a qué te refieres?".

3. TONO NATURAL, HUMANO Y CERO ROBÓTICO:
   - Habla como una persona real en WhatsApp: cercano, profesional y con criterio.
   - PROHIBIDO decir frases como "No dispongo de datos en mi sistema", "No tengo esa información en mis registros" o sonar como software.
   - Si no tienes un dato puntual a mano, dilo como persona: "Ese dato puntual no lo tengo presente ahora, pero lo valido con el equipo y te cuento"."""

    # Si es solo un saludo simple, evitamos inyectar miles de caracteres de contexto innecesario
    if es_saludo:
        contexto_adicional = ""
    else:
        hechos_campuslands = leer_archivo("investigacion/diego-tarazona/memoria/campuslands-hechos.md", 2500)
        base_campuslands = leer_archivo("prospectos/base-de-conocimiento.md", 2500)
        cultura_hunter = leer_archivo("areas/cultura-hunter.md", 2000)
        perfil_diego = leer_archivo("people/diego-tarazona.md", 2000)
        logica_diego = leer_archivo("linkedin/voz-diego/logica-de-razonamiento-diego.md", 2500)
        contexto_recuperado = recuperar_contexto_relevante(mensaje_usuario, es_admin=es_admin)

        contexto_adicional = f"""
CULTURA HUNTER Y VALORES DE CAMPUSLANDS:
{cultura_hunter}

INFORMACIÓN RELEVANTE Y FUENTES DEL SECOND BRAIN:
{contexto_recuperado if contexto_recuperado else '(Sin notas adicionales coincidentes en el vault)'}

GUION Y BASE DE CONOCIMIENTO VALIDADA DE CAMPUSLANDS:
{base_campuslands}

HECHOS CORPORATIVOS VERIFICADOS DE CAMPUSLANDS:
{hechos_campuslands}

PERFIL DE DIEGO TARAZONA:
{perfil_diego}

CRITERIOS Y LÓGICA DE RESPUESTA:
{logica_diego}
"""

    system_prompt = f"""{intro_rol}

REGLAS ESTRICTAS DE RESPUESTA:

{regla_tono_y_formato}

2. CRITERIO SOBRE FUENTES Y HECHOS:
   - Usa los hechos corporativos verificados y las fuentes de abajo cuando aplique.
   - Si te preguntan un dato operativo muy específico que no tienes a mano, responde con sencillez y naturalidad: "Ese dato puntual no lo tengo presente ahora, pero lo valido con el equipo y te cuento", jamás como una base de datos.

3. SILENCIO ABSOLUTO SOBRE EL SISTEMA INTERNO:
   - PROHIBIDO TERMINANTEMENTE MENCIONAR RUTAS DE ARCHIVOS (como "journal/...", "sources/...", ".md", ".py") O NOMBRES DE CARPETAS en tus respuestas por WhatsApp.
   - NUNCA menciones minutas, open-loops ni el "Second Brain" a menos que el administrador pregunte expresamente por sus notas o pendientes.
   - Responde con total naturalidad humana y ejecutiva como Diego Tarazona conversando con Pao por WhatsApp.

4. IDENTIDAD Y LÍMITES:
   - {identidad}
   - {regla_nombre}
{contexto_adicional}
"""

    prompt_final = f"{system_prompt}\n\n"
    if contexto_operacion and es_admin:
        prompt_final += f"CONTEXTO DE LO QUE ACABAS DE GESTIONAR EN EL SISTEMA (SOLO SI APLICA):\n{contexto_operacion}\n\n"
    if image_path:
        prompt_final += (
            "[SE ADJUNTA UNA IMAGEN EN EL MENSAJE. Analízala visualmente y responde al mensaje o pregunta del usuario "
            "con base en lo que ves en ella. Recuerda responder de forma simple, concisa y natural (1 a 3 oraciones cortas), "
            "sin rodeos ni tecnicismos innecesarios.]\n\n"
        )
    prompt_final += (
        f"MENSAJE RECIBIDO:\n\"{mensaje_usuario}\"\n\n"
        f"TU RESPUESTA ({'COMO DIEGO TARAZONA' if es_admin else 'BORRADOR DE ' + FIRMA_EXTERNOS.upper()}) "
        f"{'(ESTRUCTURA DE POST / GUION COMPLETO SEGÚN LA RED)' if es_pedido_redes else '(RECORDATORIO OBLIGATORIO: MÁXIMO 1-3 ORACIONES O VIÑETAS BREVES, SIMPLE, NATURAL, DIRECTO AL GRANO, SIN SALIRTE DE CONTEXTO)'}:"
    )

    temperatura_usar = 0.5 if es_pedido_redes else 0.2
    max_tokens_usar = None if es_pedido_redes else 250
    respuesta = llamar_gemini(
        prompt_final,
        json_mode=False,
        temperature=temperatura_usar,
        max_tokens=max_tokens_usar,
        image_path=image_path,
    )
    if respuesta:
        respuesta_limpia = re.sub(r"\bf[ií]jese\s+que\b", "ten en cuenta que", respuesta, flags=re.IGNORECASE)
        respuesta_limpia = re.sub(r"\bf[ií]jese\b", "", respuesta_limpia, flags=re.IGNORECASE)
        return respuesta_limpia.strip()

    # Fallback neutro y ceñido al guion en caso de corte de red
    if es_admin:
        if image_path:
            return f"Recibí la imagen{' (' + mensaje_usuario + ')' if mensaje_usuario else ''} correctamente."
        return "¡Hola Pao! ¿Cómo vas? ¿En qué te ayudo hoy?" if es_saludo else (
            "Recibí tu mensaje. En este momento no pude consultar el modelo para darte una respuesta específica, "
            "pero el mensaje ya quedó registrado."
        )

    if image_path:
        return "Hola. Recibimos tu imagen correctamente en el equipo de Campuslands."
    return "¡Hola! Con gusto te colaboramos desde Campuslands. ¿En qué podemos orientarte?" if es_saludo else (
        "Hola. En Campuslands ofrecemos formación intensiva en programación, inglés, inteligencia artificial y "
        "habilidades blandas, con sedes activas en Bucaramanga (Zona Franca Santander) y Ciudad de Guatemala. "
        "Para detalles específicos de admisiones, fechas o costos, lo confirmamos con el equipo de Campuslands."
    )
