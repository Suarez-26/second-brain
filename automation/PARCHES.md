# Parches locales y Arquitectura de WhatsApp + Claude

Origen: https://github.com/lharries/whatsapp-mcp (commit 7d6a06d). Revisado el 2026-10-13 y actualizado el 2026-10-17.
La carpeta `whatsapp-mcp/` está en `.gitignore`; este archivo documenta la configuración vigente.

## Cambios del 2026-10-17 (Interacción bidireccional con Claude)
1. **Puente Node.js compatible con Control Inteligente de Aplicaciones de Windows (`automation/whatsapp-mcp/whatsapp-bridge-node/index.js`):**
   - El ejecutable compilado en Go (`whatsapp-bridge.exe`) era bloqueado por la directiva de Control de Aplicaciones de Windows y carecía de CGO para SQLite.
   - Se implementó el puente sobre `node.exe` firmado (Node v24 con `node:sqlite` nativo y `@whiskeysockets/baileys`), escribiendo exactamente en la misma base SQLite (`store/messages.db` y `store/whatsapp.db`).
2. **Puerto `127.0.0.1:8085` y `/api/send` habilitado:**
   - Se movió el puerto local de `8080` a `8085` (`http://127.0.0.1:8085`) para no colisionar con Docker Desktop / WSL (`wikimaster`).
   - Se habilitó `POST /api/send` únicamente en `127.0.0.1:8085` para que el servidor MCP de Claude y el bot interactivo puedan responder mensajes.
   - Se añadió `GET http://127.0.0.1:8085/qr` para escanear el código QR cómodamente desde el navegador.
3. **Servidor MCP de WhatsApp (`automation/whatsapp-mcp/whatsapp-mcp-server/main.py`):**
   - Actualizado para compatibilidad con `mcp` 2.x (`MCPServer`) y `127.0.0.1:8085`.
   - Registrado en `.mcp.json` (para Claude Code) y en `claude_desktop_config.json` (junto con el MCP `second-brain` de filesystem).
4. **Bot Interactivo de Claude en WhatsApp (`automation/claude_whatsapp_bot.py` + `automation/bot_config.json`):**
   - **Chat propio de Pao:** Pao puede escribir en su propio chat de WhatsApp (o con `@claude`) y recibir respuestas conectadas a su Second Brain.
   - **Modo Copiloto (`copiloto`):** Cuando escribe un prospecto/contacto, Claude redacta el borrador con `prospectos/base-de-conocimiento.md` y lo envía al chat propio de Pao; solo sale al prospecto cuando Pao responde `Enviar` o `Editar: <texto>`.
   - **Modo Automático (`auto`):** Si Pao envía `/modo auto` en su chat, Claude responde directamente a los prospectos usando únicamente la información validada y notifica a Pao.
   - **Anti-inyección:** Mensajes de terceros con patrones de inyección de prompts se bloquean y registran como `ALERTA` en `meta/log.md`.
