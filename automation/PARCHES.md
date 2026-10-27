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

## Refactorización del 2026-10-27 (integridad, seguridad y recuperación)

### Arquitectura
```
Kapso ─POST /webhook (HMAC X-Webhook-Signature)─► cola SQLite (state.db) ─► worker (reintentos)
Puente WhatsApp Web ─► store/messages.db ─► claude_whatsapp_bot.py (polling)
exportar_whatsapp.py ─► inbox/whatsapp/{yo,otros}/
              todo escribe a través de ▼
vault_io.py: bloqueo entre procesos + escritura atómica + meta/log.md + commit git por lote
      journal/, sources/reuniones/, inbox/  → libre
      meta/ (Capa 1) y el resto           → solo con aprobación explícita
indice.py (FTS5) ◄─ mcp_buscar.py (MCP: buscar, leer_nota, estado_pendientes)
```

### Módulos
- `vault_io.py`: único escritor del vault. Ningún script escribe Markdown por su cuenta.
- `cola.py`: `state.db` (ignorado por git) con la cola de mensajes (deduplicación por id, 3 reintentos con espera de 30 s, 2 min y 10 min; lo interrumpido se recupera al arrancar), los borradores del copiloto y las propuestas sobre open-loops.
- `pendientes.py`: los pendientes llevan ID estable (`[OL-012]`). El LLM **solo propone** agregar o cerrar; nada cambia en `meta/open-loops.md` hasta que el administrador responde `Aceptar N`.
- `indice.py`: índice local (`index.db`, BM25, sin distinguir acentos, incremental). El corpus crudo (`diego_*`, `inbox/`, `sources/`) se indexa marcado `crudo` y no sale por defecto.
- `mcp_buscar.py`: servidor MCP de solo lectura sobre el índice.
- `validar_frontmatter.py`: reporte del esquema de metadatos (no reescribe).
- `tests/test_pipeline.py`: `python -m unittest discover -s automation/tests` (vault temporal, no toca el real).

### Bot de Kapso (`kapso_whatsapp_bot.py`)
- Escucha solo en `127.0.0.1`; el túnel de Cloudflare entra por localhost.
- Rechaza todo POST sin firma HMAC válida. `iniciar_kapso_bot.ps1` guarda el secreto de cada webhook en `automation/.secretos/` (ignorado por git). Para pruebas locales sin Kapso: `KAPSO_WEBHOOK_INSECURE=1`.
- El remitente solo se toma como administrador si la firma es válida y el número coincide con `ADMIN_PHONE_NUMBER`.
- Terceros: su mensaje va a `inbox/whatsapp/otros/<número>.md` y la respuesta queda como borrador. El borrador va firmado por `FIRMA_EXTERNOS` (por defecto "Equipo Campuslands"), no como Diego.
- Comandos del administrador: `Ayuda`, `Estado`, `Borradores`, `Enviar N`, `Editar N: texto`, `Descartar N`, `Propuestas`, `Aceptar N`, `Rechazar N`.
- Limitación de WhatsApp: el texto libre al administrador solo llega dentro de las 24 h siguientes a su último mensaje al número del bot.

### Otros cambios
- Gemini: la key va en el header `x-goog-api-key` (nunca en la URL); cadena de modelos configurable con `GEMINI_MODELOS` y tiempo límite total `GEMINI_TIMEOUT_TOTAL` (40 s).
- Whisper se carga una vez por proceso (`WHISPER_MODELO`, por defecto `base`).
- Lanzadores con `python` del PATH (o `SECOND_BRAIN_PYTHON`); corregido el uso de `$pid` (variable reservada de PowerShell), que impedía registrar los webhooks.
- Archivados en `automation/_archivo/`: el bot de prueba `whatsapp_webhook_server.py` y los scripts manuales `test_*.py`.
