---
fecha: 2026-10-27
tipo: contexto-operativo
---

# Última sesión (2026-10-27)

## Qué se hizo
- **Auditoría y refactorización del pipeline de automatización** (ver [[automation/PARCHES]], sección 2026-10-27).
- **Seguridad:**
  - Token de Meta fuera del código, en `.env` (falta rotarlo: OL-013).
  - El webhook de Kapso exige firma HMAC y escucha solo en localhost.
  - La key de Gemini va en header.
  - El bot de prueba que contestaba lo mismo que recibía quedó archivado.
- **Integridad:**
  - Todo escribe por `automation/vault_io.py` (bloqueo, escritura atómica, log y commit git automático).
  - Cola SQLite con reintentos en lugar de los JSON.
  - `open-loops.md` lleva IDs `[OL-nnn]`; el LLM solo propone y Pao aprueba con `Aceptar N`.
- **Terceros:**
  - Copiloto obligatorio en los dos bots; el modo auto quedó desactivado.
  - Borradores firmados "Equipo Campuslands", no como Diego.
  - Mensajes de terceros en `inbox/whatsapp/otros/`.
- **Recuperación:**
  - Índice local FTS5 (`automation/indice.py`) y servidor MCP `second-brain-buscar`, registrado en `.mcp.json` con rutas relativas.
  - Se instaló el SDK `mcp`.
- **Datos:**
  - Esquema de frontmatter con `calidad` (crudo | resumido | verificado) y validador: 0 de 123 notas con problemas.
  - Fuente canónica sobre Diego declarada en `CLAUDE.md`.
  - Resúmenes [[2026-W42]] y [[2026-W43]].
- **Pruebas:** 13 pruebas automáticas en `automation/tests/` (vault temporal), todas pasan. El bot arrancó en local y rechazó POST sin firma.
- Commit de restauración `995fff0` antes de los cambios.

## Quedó a medias
- No se probó contra WhatsApp real (OL-017): todo el flujo de Kapso se verificó con simulaciones.
- `faster-whisper` no está instalado en este equipo; los audios dependen de la transcripción de Kapso.
- `.obsidian/workspace.json` todavía guarda rutas de `C:\Users\tomas` (lo regenera Obsidian solo).

## Siguiente paso
- Rotar el token (OL-013) y confirmar si OL-012 fue una reunión real.
- Arrancar `iniciar_bot.bat` y probar un ciclo real con un número de prueba (OL-017).
- Dejar la infraestructura quieta y usar el sistema: journal propio y 3 piezas para `linkedin/banco-de-contenido/`.
