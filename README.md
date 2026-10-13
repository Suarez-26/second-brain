# second-brain

Second brain personal basado en un vault de Markdown, inspirado en el podcast de 30X con Adelaida Díaz-Roa.

## Uso con Claude Desktop (MCP)
Claude Desktop accede al vault mediante el servidor MCP de sistema de archivos
(`@modelcontextprotocol/server-filesystem`) apuntando a esta carpeta.
Ejemplo para `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "second-brain": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:\\Users\\tomas\\second-brain"]
    }
  }
}
```

Pega el contenido de `CLAUDE.md` como instrucciones del proyecto en Claude Desktop para que aplique las reglas.

## Próximos pasos
1. Empezar el journaling (`journal/_plantilla.md`).
2. Cargar el material de contexto en `inbox/` y procesarlo.
3. Ajustar el panel en `advisors/`.
4. Conectores adicionales (WhatsApp, correo) cuando estén definidos.
