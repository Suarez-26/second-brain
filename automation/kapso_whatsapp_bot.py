"""Bot de WhatsApp para Second Brain usando la API oficial de Kapso.
Voz y Personalidad: Diego Tarazona (Cofundador de Campuslands).

Capacidades:
1. Ingesta y transcripción de audios de reuniones, conferencias y notas de voz (faster-whisper).
2. Clasificación automática con Gemini:
   - Reuniones -> Minutas en sources/reuniones/ + extracción de compromisos a meta/open-loops.md
   - Reportes de actividades ("hoy hice tal cosa") -> Registro en journal/ + tacha tareas [x] y añade [ ]
   - Preguntas y reflexiones -> Respuestas 100% auténticas como Diego Tarazona
3. Comunicación bidireccional por WhatsApp (soporte para Sandbox y números de producción).
4. Modo copiloto obligatorio: a terceros nunca se responde directo; el borrador va al
   administrador (ADMIN_PHONE_NUMBER), que responde Enviar N / Editar N: texto / Descartar N / Pendientes.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import sys
import threading
import time
from pathlib import Path
from typing import Any

import requests
from flask import Flask, jsonify, request

# Codificación UTF-8 en consola Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

RAIZ = Path(__file__).resolve().parent.parent
ENV_PATH = RAIZ / ".env"
LOG_VAULT_PATH = RAIZ / "meta" / "log.md"
ESTADO_PATH = RAIZ / "automation" / ".estado_kapso_bot.json"
AUDIO_DIR = RAIZ / "sources" / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# Importar motor analítico de Diego y Second Brain
sys.path.append(str(RAIZ / "automation"))
from audio_processor import (
    actualizar_open_loops,
    analizar_contenido_con_ia,
    guardar_minuta_reunion,
    registrar_log,
    registrar_reporte_en_journal,
    responder_como_diego,
    transcribir_archivo_audio,
)

app = Flask(__name__)

# Cargar .env
def cargar_env() -> None:
    if not ENV_PATH.exists():
        return
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

cargar_env()

KAPSO_API_BASE_URL = os.getenv("KAPSO_API_BASE_URL", "https://api.kapso.ai").rstrip("/")
KAPSO_API_KEY = os.getenv("KAPSO_API_KEY", "")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "597907523413541")

# Estado persistente para deduplicar mensajes
def cargar_estado() -> dict[str, Any]:
    if ESTADO_PATH.exists():
        try:
            return json.loads(ESTADO_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"mensajes_procesados": []}

def guardar_estado(estado: dict[str, Any]) -> None:
    estado["mensajes_procesados"] = estado.get("mensajes_procesados", [])[-500:]
    ESTADO_PATH.write_text(json.dumps(estado, ensure_ascii=False, indent=2), encoding="utf-8")

# Enviar mensaje vía Kapso
def enviar_mensaje_kapso(to: str, texto: str, phone_id: str | None = None) -> bool:
    if not to:
        print("[ERROR] Destinatario ('to') vacío, no se puede enviar mensaje.", flush=True)
        return False
    # Normalizar número (quitar + y espacios)
    destinatario = to.lstrip("+").strip().replace(" ", "")
    target_pid = phone_id or PHONE_NUMBER_ID
    url = f"{KAPSO_API_BASE_URL}/meta/whatsapp/v24.0/{target_pid}/messages"
    headers = {
        "X-API-Key": KAPSO_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": destinatario,
        "type": "text",
        "text": {"body": texto}
    }
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=20)
        print(f"[ENVÍO DESDE {target_pid} A {destinatario}] Status {resp.status_code}: {resp.text}", flush=True)
        return resp.status_code in (200, 201)
    except Exception as e:
        print(f"[ERROR] Excepción enviando WhatsApp a {destinatario}: {e}", flush=True)
        return False

# Descargar audio de Kapso
def descargar_audio_kapso(media_id_o_url: str, sender: str, phone_id: str) -> tuple[Path | None, str]:
    headers = {"X-API-Key": KAPSO_API_KEY}
    download_url = media_id_o_url

    # Si es un ID de Meta/Kapso, obtener URL de descarga temporal
    if not media_id_o_url.startswith("http"):
        meta_url = f"{KAPSO_API_BASE_URL}/meta/whatsapp/v24.0/{media_id_o_url}?phone_number_id={phone_id}"
        try:
            r = requests.get(meta_url, headers=headers, timeout=12)
            if r.status_code == 200:
                data = r.json()
                download_url = data.get("url", media_id_o_url)
        except Exception as e:
            print(f"[WARN] Error obteniendo URL del media {media_id_o_url}: {e}", flush=True)

    # Descargar bytes
    timestamp_str = dt.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    dest_path = AUDIO_DIR / f"{timestamp_str}_{sender}.ogg"
    try:
        res = requests.get(download_url, headers=headers, stream=True, timeout=25)
        if res.status_code == 200:
            with open(dest_path, "wb") as f:
                for chunk in res.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"[OK] Audio guardado en: {dest_path}", flush=True)
            return dest_path, dest_path.name
    except Exception as e:
        print(f"[ERROR] Error descargando audio: {e}", flush=True)
    return None, ""

ADMIN_NUMBERS = {
    re.sub(r"\D", "", os.getenv("ADMIN_PHONE_NUMBER", "573167755887")),
    "573167755887",
    "3167755887",
}
INBOX_WHATSAPP_DIR = RAIZ / "inbox" / "whatsapp"
INBOX_WHATSAPP_DIR.mkdir(parents=True, exist_ok=True)

def es_administrador(remitente: str) -> bool:
    clean = re.sub(r"\D", "", remitente)
    # Un remitente vacío o corto no puede coincidir por sufijo con el número admin
    if len(clean) < 10:
        return False
    return any((clean.endswith(num) or num.endswith(clean)) for num in ADMIN_NUMBERS if num)

# Modo copiloto: ninguna respuesta a terceros sale sin aprobación del administrador
# (regla 7 de CLAUDE.md). El borrador se envía al admin y él responde Enviar/Editar/Descartar.
ADMIN_DESTINO = re.sub(r"\D", "", os.getenv("ADMIN_PHONE_NUMBER", "573167755887"))
LOCK_ESTADO = threading.Lock()

def guardar_borrador_y_avisar(remitente: str, mensaje_original: str, borrador: str, phone_id: str) -> None:
    with LOCK_ESTADO:
        estado = cargar_estado()
        bid = str(estado.get("siguiente_id_borrador", 1))
        estado["siguiente_id_borrador"] = int(bid) + 1
        estado.setdefault("borradores_pendientes", {})[bid] = {
            "id": bid,
            "remitente": remitente,
            "phone_id": phone_id,
            "mensaje_original": mensaje_original,
            "borrador": borrador,
            "timestamp": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        guardar_estado(estado)
    registrar_log("BORRADOR", f"inbox/whatsapp/{remitente}.md", f"Borrador #{bid} para {remitente} en espera de aprobación")
    tarjeta = (
        f"🤖 *Nuevo mensaje de contacto* [#{bid}]\n"
        f"👤 *De:* `{remitente}`\n"
        f"💬 *Dijo:* \"{mensaje_original[:500]}\"\n\n"
        f"📝 *Borrador sugerido:*\n\"{borrador}\"\n\n"
        f"👉 Responde *Enviar {bid}*, *Editar {bid}: tu texto* o *Descartar {bid}*. *Pendientes* lista la cola."
    )
    enviar_mensaje_kapso(ADMIN_DESTINO, tarjeta, phone_id=phone_id)

def procesar_comando_copiloto(texto: str) -> str | None:
    """Devuelve la respuesta para el admin si el texto es un comando de copiloto; None si no lo es."""
    t = texto.strip()
    tl = t.lower()
    m_enviar = re.match(r"^enviar(?:\s+#?(\d+))?$", tl)
    m_editar = re.match(r"^editar(?:\s+#?(\d+))?\s*:\s*(.+)$", t, re.DOTALL | re.IGNORECASE)
    m_descartar = re.match(r"^descartar(?:\s+#?(\d+))?$", tl)
    if tl in ("pendientes", "/pendientes"):
        pendientes = cargar_estado().get("borradores_pendientes", {})
        if not pendientes:
            return "ℹ️ No hay borradores pendientes."
        return "📋 *Borradores pendientes:*\n" + "\n".join(
            f"• #{bid}: `{b['remitente']}`: \"{b['mensaje_original'][:80]}\"" for bid, b in pendientes.items()
        )
    if not (m_enviar or m_editar or m_descartar):
        return None

    m = m_enviar or m_editar or m_descartar
    with LOCK_ESTADO:
        estado = cargar_estado()
        pendientes = estado.get("borradores_pendientes", {})
        if not pendientes:
            return "ℹ️ No hay borradores pendientes."
        bid = m.group(1) or sorted(pendientes.keys(), key=int)[-1]
        if bid not in pendientes:
            return f"⚠️ No encontré el borrador #{bid}. Escribe *Pendientes* para ver la cola."
        item = pendientes.pop(bid)
        guardar_estado(estado)

    if m_descartar:
        registrar_log("BORRADOR_DESCARTADO", f"inbox/whatsapp/{item['remitente']}.md", f"Borrador #{bid} descartado")
        return f"🗑️ Borrador #{bid} descartado."

    texto_final = m_editar.group(2).strip() if m_editar else item["borrador"]
    ok = enviar_mensaje_kapso(item["remitente"], texto_final, phone_id=item.get("phone_id"))
    if ok:
        registrar_log("RESPUESTA_APROBADA", f"inbox/whatsapp/{item['remitente']}.md", f"Borrador #{bid} enviado tras aprobación")
        return f"✅ *Enviado a* `{item['remitente']}`:\n\"{texto_final}\""
    with LOCK_ESTADO:
        estado = cargar_estado()
        estado.setdefault("borradores_pendientes", {})[bid] = item
        guardar_estado(estado)
    return f"❌ Error al enviar el borrador #{bid}; sigue en la cola."

def registrar_mensaje_externo(remitente: str, texto: str, tipo_msg: str = "texto", audio_file: str = "") -> None:
    try:
        ahora = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
        archivo_path = INBOX_WHATSAPP_DIR / f"{remitente}.md"
        entrada = f"\n### [{ahora}] {tipo_msg.upper()}\n"
        if audio_file:
            entrada += f"- **Audio:** `sources/audio/{audio_file}`\n"
        entrada += f"- **Mensaje:** {texto}\n"
        if not archivo_path.exists():
            archivo_path.write_text(f"# Historial WhatsApp: {remitente}\n\nCreado: {ahora}\n{entrada}", encoding="utf-8")
        else:
            with open(archivo_path, "a", encoding="utf-8") as f:
                f.write(entrada)
        registrar_log("INBOX_EXTERNO", f"inbox/whatsapp/{remitente}.md", f"Mensaje de {remitente}")
    except Exception as e:
        print(f"[WARN] No se pudo guardar en inbox externo: {e}", flush=True)

# Procesar mensaje de texto
def procesar_mensaje_texto(texto: str, remitente: str) -> str:
    t = texto.strip()
    t_lower = t.lower()
    es_admin = es_administrador(remitente)

    # Comando de ayuda técnica sólo si lo piden explícitamente
    if t_lower in ("ayuda", "/ayuda", "help", "/help", "menu", "/menu"):
        if es_admin:
            return (
                "🧠 *Second Brain (Voz de Diego Tarazona)*\n\n"
                "Mire Tomás, aquí estoy al pie del cañón:\n\n"
                "• *Charlar o pedir opiniones:* Pregúnteme sobre IA, educación, negocios o talento.\n"
                "• *Subir audios:* Envíeme notas de voz o reuniones. Yo se las transcribo, armo minutas y extraigo compromisos a open-loops.\n"
                "• *Reportar su día:* Dígame 'hoy hice tal cosa y quedé pendiente de X' y le actualizo su journal y open-loops al instante.\n"
                "• *Consultar foco:* Pregúnteme '¿cuáles son mis prioridades?' o '¿qué pendientes tengo?'."
            )
        else:
            return (
                "🎙️ *Diego Tarazona (Campuslands)*\n\n"
                "Mire, qué gusto saludarlo. Por acá estoy disponible para charlar sobre:\n\n"
                "• Inteligencia artificial, tecnología y cómo dirigirla con liderazgo.\n"
                "• Campuslands, el cohete social y oportunidades reales para los jóvenes.\n"
                "• Talento, habilidades blandas y lo que buscan las empresas hoy.\n\n"
                "Cuénteme en qué le puedo colaborar o de qué tema le gustaría que hablemos."
            )

    # Análisis con IA
    analisis = analizar_contenido_con_ia(t)
    contexto_op = ""

    # Operaciones en Second Brain: SOLO si es Tomás (es_admin)
    if es_admin:
        # Caso A: Es una reunión o acuerdos
        if analisis.get("es_reunion"):
            minuta_path, filename = guardar_minuta_reunion(analisis)
            if analisis.get("compromisos_nuevos"):
                actualizar_open_loops([], analisis["compromisos_nuevos"])
            contexto_op = (
                f"Se generó la minuta de la reunión en 'sources/reuniones/{filename}'. "
                f"Se registraron {len(analisis.get('compromisos_nuevos', []))} compromisos en meta/open-loops.md: {analisis.get('compromisos_nuevos')}."
            )

        # Caso B: Reporte explícito de actividades (hizo algo o dejó compromisos)
        elif analisis.get("tipo") == "reporte_actividades" and (analisis.get("tareas_completadas") or analisis.get("compromisos_nuevos") or analisis.get("hechos_realizados")):
            if analisis.get("tareas_completadas"):
                actualizar_open_loops(analisis.get("tareas_completadas", []), [])
            if analisis.get("compromisos_nuevos"):
                actualizar_open_loops([], analisis.get("compromisos_nuevos", []))
            registrar_reporte_en_journal(analisis, t)
            contexto_op = (
                f"Se registraron las actividades en el journal de hoy. "
                f"Tareas completadas detectadas: {analisis.get('tareas_completadas')}. "
                f"Nuevos pendientes añadidos a open-loops: {analisis.get('compromisos_nuevos')}."
            )
    else:
        # Si es un contacto externo, registrar mensaje en inbox/whatsapp/
        registrar_mensaje_externo(remitente, t, tipo_msg="texto")

    # Respuesta 100% como Diego Tarazona
    respuesta_diego = responder_como_diego(t, contexto_operacion=contexto_op, es_admin=es_admin, remitente=remitente)
    return f"🎙️ *Diego Tarazona:*\n\n{respuesta_diego}"

# Procesar nota de voz o archivo de audio
def procesar_audio(audio_path: Path, audio_filename: str, transcript: str, remitente: str) -> str:
    print(f"[INFO] Procesando transcripción con Gemini ({len(transcript)} chars)...", flush=True)
    es_admin = es_administrador(remitente)
    analisis = analizar_contenido_con_ia(transcript)
    contexto_op = ""
    detalles_accion = ""
    hoy = dt.date.today().strftime("%Y-%m-%d")

    if es_admin:
        # Caso A: Reunión o conferencia grabada
        if analisis.get("es_reunion"):
            minuta_path, filename = guardar_minuta_reunion(analisis, audio_filename=audio_filename)
            nuevos = []
            if analisis.get("compromisos_nuevos"):
                nuevos = actualizar_open_loops([], analisis["compromisos_nuevos"])
            contexto_op = (
                f"Transcribiste el audio completo de la reunión. "
                f"Generaste la minuta ejecutiva en 'sources/reuniones/{filename}'. "
                f"Registraste {len(nuevos)} compromisos en meta/open-loops.md: {nuevos}."
            )
            detalles_accion = (
                f"\n\n📁 *Minuta guardada:* `sources/reuniones/{filename}`\n"
                f"📋 *Compromisos agregados:* {len(nuevos)}"
            )

        # Caso B: Reporte de lo que hizo hoy
        elif analisis.get("tipo") == "reporte_actividades" and (analisis.get("tareas_completadas") or analisis.get("compromisos_nuevos") or analisis.get("hechos_realizados")):
            actualizar_open_loops(analisis.get("tareas_completadas", []), analisis.get("compromisos_nuevos", []))
            registrar_reporte_en_journal(analisis, transcript, audio_filename=audio_filename)
            contexto_op = (
                f"Transcribiste la nota de voz y registraste las actividades en el journal/{hoy}.md. "
                f"Tareas cerradas: {analisis.get('tareas_completadas')}. "
                f"Nuevos compromisos: {analisis.get('compromisos_nuevos')}."
            )
            detalles_accion = f"\n\n📝 *Reporte guardado en:* `journal/{hoy}.md`"

        # Caso C: Consulta / nota general por voz
        else:
            # Guardar en journal como registro histórico del audio
            journal_path = RAIZ / "journal" / f"{hoy}.md"
            hora = dt.datetime.now().strftime("%H:%M")
            bloque = f"\n\n### 🎙️ Audio WhatsApp ({hora})\n- **Audio:** `sources/audio/{audio_filename}`\n> {transcript}\n"
            if journal_path.exists():
                with open(journal_path, "a", encoding="utf-8") as f:
                    f.write(bloque)
            else:
                journal_path.parent.mkdir(parents=True, exist_ok=True)
                journal_path.write_text(f"# Journal {hoy}\n\n## Entradas del día{bloque}\n", encoding="utf-8")
            contexto_op = ""
            detalles_accion = ""
    else:
        # Contacto externo: guardar en inbox/whatsapp/{remitente}.md
        registrar_mensaje_externo(remitente, transcript, tipo_msg="audio", audio_file=audio_filename)
        contexto_op = ""
        detalles_accion = ""

    # Diego responde de manera integral
    diego_voz = responder_como_diego(transcript, contexto_operacion=contexto_op, es_admin=es_admin, remitente=remitente)

    mensaje_salida = (
        f"🎙️ *Diego Tarazona:*\n\n"
        f"{diego_voz}"
        f"{detalles_accion}"
    )
    return mensaje_salida

# Despacho en hilo secundario
def responder(remitente: str, mensaje_original: str, respuesta: str, phone_id: str) -> None:
    """Al admin se le responde directo; a terceros, solo vía borrador aprobado."""
    if es_administrador(remitente):
        enviar_mensaje_kapso(remitente, respuesta, phone_id=phone_id)
    else:
        guardar_borrador_y_avisar(remitente, mensaje_original, respuesta, phone_id)

def despachar_mensaje_asincrono(data: dict[str, Any]) -> None:
    msg = None
    remitente = ""

    # Caso 1: Payload Kapso nativo (v2)
    if "message" in data:
        msg = data["message"]
        conversation = data.get("conversation") or {}
        remitente = (
            msg.get("from")
            or msg.get("kapso", {}).get("phone_number")
            or conversation.get("phone_number")
            or ""
        )

    # Caso 2: Payload Meta estándar
    elif "entry" in data:
        try:
            entry = data["entry"][0]
            change = entry["changes"][0]
            val = change["value"]
            messages = val.get("messages", [])
            if messages:
                msg = messages[0]
                remitente = msg.get("from", "")
        except Exception:
            pass

    if not msg:
        return

    phone_id = data.get("phone_number_id") or (msg.get("kapso") or {}).get("phone_number_id") or PHONE_NUMBER_ID
    msg_id = msg.get("id") or ""
    with LOCK_ESTADO:
        estado = cargar_estado()
        procesados = estado.get("mensajes_procesados", [])
        if msg_id and msg_id in procesados:
            print(f"[INFO] Mensaje duplicado {msg_id}, ignorando.", flush=True)
            return
        if msg_id:
            procesados.append(msg_id)
            estado["mensajes_procesados"] = procesados
            guardar_estado(estado)

    tipo = msg.get("type", "")
    print(f"\n[MENSAJE ENTRANTE {phone_id}] Tipo: {tipo} | De: {remitente}", flush=True)

    # A. Audio / Voz
    if tipo in ("audio", "voice"):
        audio_info = msg.get("audio", {})
        kapso_info = msg.get("kapso", {})
        transcript = ""

        if kapso_info.get("transcript", {}).get("text"):
            transcript = kapso_info["transcript"]["text"]
        elif kapso_info.get("content") and "Transcript:" in kapso_info["content"]:
            transcript = kapso_info["content"].split("Transcript:")[-1].strip()

        media_id = audio_info.get("id") or kapso_info.get("media_url") or ""
        audio_path, audio_filename = (None, "")
        if media_id:
            audio_path, audio_filename = descargar_audio_kapso(media_id, remitente, phone_id)

        if not transcript and audio_path and audio_path.exists():
            print("[INFO] Transcribiendo con faster-whisper local...", flush=True)
            transcript = transcribir_archivo_audio(audio_path)

        if transcript:
            print(f"[TRANSCRIPCIÓN]: \"{transcript}\"", flush=True)
            respuesta = procesar_audio(audio_path, audio_filename or "audio.ogg", transcript, remitente)
            responder(remitente, f"[nota de voz] {transcript}", respuesta, phone_id)
        else:
            responder(
                remitente,
                "[nota de voz sin transcripción]",
                "🎙️ *Diego Tarazona:*\n\nMire Tomás, le recibí la nota de voz pero no logré escuchar bien el audio para transcribirlo. ¿Me lo reenvía o me cuenta por acá qué cuadramos?",
                phone_id,
            )

    # B. Mensaje de Texto
    elif tipo == "text":
        texto = msg.get("text", {}).get("body", "") or msg.get("kapso", {}).get("content", "")
        if not texto:
            return
        if es_administrador(remitente):
            respuesta_comando = procesar_comando_copiloto(texto)
            if respuesta_comando is not None:
                enviar_mensaje_kapso(remitente, respuesta_comando, phone_id=phone_id)
                return
        respuesta = procesar_mensaje_texto(texto, remitente)
        responder(remitente, texto, respuesta, phone_id)

# Rutas Flask
@app.route("/", methods=["GET"])
def home():
    return "Servidor Kapso WhatsApp Bot Activo (Voz: Diego Tarazona)", 200

@app.route("/webhook", methods=["GET"])
def verificar_webhook():
    challenge = request.args.get("hub.challenge")
    if challenge:
        return challenge, 200
    return jsonify(status="ok", timestamp=time.time()), 200

@app.route("/webhook", methods=["POST"])
def recibir_webhook():
    data = request.get_json(silent=True) or {}
    threading.Thread(target=despachar_mensaje_asincrono, args=(data,), daemon=True).start()
    return jsonify(status="received"), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print("==================================================")
    print(f" Servidor Kapso WhatsApp Bot iniciado en puerto {port}")
    print(f" Teléfono WhatsApp Activo ID: {PHONE_NUMBER_ID}")
    print(f" Voz y Personalidad: Diego Tarazona")
    print("==================================================")
    app.run(host="0.0.0.0", port=port, debug=False)
