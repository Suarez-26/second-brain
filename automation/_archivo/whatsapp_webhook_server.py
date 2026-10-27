import os
import sys
import json
import requests
from flask import Flask, request, jsonify

# Forzar codificación UTF-8 para evitar errores de consola en Windows
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

app = Flask(__name__)

# Cargar .env de la raíz del vault (los tokens no van en el código)
ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
if os.path.exists(ENV_PATH):
    with open(ENV_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

# Configuración básica
VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "1429641633564960")
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN", "")

@app.route("/", methods=["GET"])
def home():
    return "Servidor Webhook de WhatsApp activo", 200

# 1. Verificación del Webhook por Meta (GET)
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("[INFO] Webhook verificado exitosamente por Meta!")
            return challenge, 200
        else:
            print("[WARN] Token de verificación incorrecto.")
            return "Token inválido", 403
    return "Parámetros insuficientes", 400

# 2. Recepción de mensajes y eventos de WhatsApp (POST)
@app.route("/webhook", methods=["POST"])
def receive_webhook():
    data = request.get_json()
    print("\n[EVENTO RECIBIDO]:")
    print(json.dumps(data, indent=2))

    try:
        entry = data.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])

        if messages:
            msg = messages[0]
            remitente = msg.get("from")
            tipo = msg.get("type")

            if tipo == "text":
                texto = msg.get("text", {}).get("body", "")
                print(f"\nMensaje de {remitente}: \"{texto}\"")

                # Respuesta automática de prueba (Echo bot)
                enviar_mensaje(remitente, f"¡Hola! Recibí tu mensaje: \"{texto}\" desde mi servidor local.")

    except Exception as e:
        print(f"[ERROR] Procesando mensaje: {e}")

    # Meta exige responder 200 OK inmediatamente
    return jsonify(status="ok"), 200

def enviar_mensaje(para, texto):
    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": para,
        "type": "text",
        "text": {"body": texto}
    }
    try:
        resp = requests.post(url, json=payload, headers=headers)
        if resp.status_code == 200:
            print(f"[OK] Respuesta enviada a {para}")
        else:
            print(f"[ERROR] Al enviar mensaje: {resp.status_code} - {resp.text}")
    except Exception as ex:
        print(f"[ERROR] Excepción enviando mensaje: {ex}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"[INICIADO] Servidor webhook en http://localhost:{port}/webhook")
    print(f"[TOKEN] Token de verificación: {VERIFY_TOKEN}")
    app.run(host="0.0.0.0", port=port, debug=False)
