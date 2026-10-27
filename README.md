# second-brain

Second brain personal basado en un vault de Markdown, inspirado en el podcast de 30X con Adelaida Díaz-Roa.
Las reglas de trabajo están en [CLAUDE.md](CLAUDE.md).

## Instalación
```
python -m pip install -r automation/requirements.txt
python automation/indice.py --reconstruir
python -m unittest discover -s automation/tests
```

## Claude Code
`.mcp.json` registra dos servidores (rutas relativas a esta carpeta, usan el `python` del PATH):
- `second-brain-buscar`: búsqueda en el vault (`buscar`, `leer_nota`, `estado_pendientes`).
- `whatsapp`: lectura y envío de WhatsApp vía el puente local en `127.0.0.1:8085`.

## Claude Desktop
En `claude_desktop_config.json`, apunta los servidores a la ruta de esta carpeta en tu equipo:

```json
{
  "mcpServers": {
    "second-brain": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:\\RUTA\\A\\second-brain"]
    },
    "second-brain-buscar": {
      "command": "python",
      "args": ["C:\\RUTA\\A\\second-brain\\automation\\mcp_buscar.py"]
    }
  }
}
```

Pega el contenido de `CLAUDE.md` como instrucciones del proyecto en Claude Desktop para que aplique las reglas.

## Automatización
Arquitectura, comandos del bot y operación: [automation/PARCHES.md](automation/PARCHES.md).
- `iniciar_bot.bat`: bot de Kapso con túnel de Cloudflare.
- `automation/iniciar_whatsapp_claude.ps1`: puente de WhatsApp Web y bot de Claude.
