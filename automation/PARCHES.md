# Parches locales a whatsapp-mcp

Origen: https://github.com/lharries/whatsapp-mcp (commit 7d6a06d). Revisado el 2026-10-13.
La carpeta `whatsapp-mcp/` está en `.gitignore`; este archivo documenta lo que se cambió.

## Hallazgos de la revisión
1. El bridge (`whatsapp-bridge/main.go`) escuchaba en `:8080`, es decir **en todas las interfaces de red**, y `/api/send` **no tiene autenticación**. Cualquiera en la misma red podría haber enviado mensajes desde tu WhatsApp.
2. No encontré telemetría ni llamadas a servidores de terceros; solo la conexión a WhatsApp (librería whatsmeow) y SQLite local.
3. Los mensajes se guardan **sin cifrar** en `store/messages.db`.

## Cambios hechos
- `startRESTServer`: ahora escucha en `127.0.0.1:<puerto>`.
- `/api/send`: devuelve 403 siempre. El envío queda deshabilitado; el cerebro solo lee.
- Sin cambios en `/api/download` (se necesita para bajar notas de voz).

## Qué ve el cerebro (lista de chats permitidos)
- El bridge guarda en `store/messages.db` los mensajes de **todos** los chats que recibe (límite de la herramienta).
- `exportar_whatsapp.py` solo lee los chats de `chats_permitidos.json`. Lo demás **no se lee ni llega al vault**.
- Comandos: `--listar-chats` (solo nombres), `--agregar "Nombre" --destino grupos/x`, `"activo": false` para pausar.
- Mejora posible: parchear el bridge para que ni siquiera **guarde** los chats no permitidos.

## Riesgos que siguen
- Es una API **no oficial** de WhatsApp: riesgo de restricción o bloqueo de la cuenta.
- Cualquier programa local puede llamar a `127.0.0.1:8080/api/download`.
- `store/` contiene tus chats en claro: no sincronizar con la nube ni subir a git.
- La sesión caduca (re-escanear el QR cada tanto).
