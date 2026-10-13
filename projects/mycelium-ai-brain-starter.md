---
tipo: investigacion
contexto: personal
fecha: 2026-10-13
---

# Mycelium / ai-brain-starter (Adelaida Díaz-Roa)

Fuentes públicas: [GitHub de adelaidasofia](https://github.com/adelaidasofia), [repo ai-brain-starter](https://github.com/mycelium-hq/ai-brain-starter), su Substack ([cómo lo construyó](https://adelaidadiazroa.substack.com/p/how-i-built-a-second-brain-that-actually), [primera semana](https://adelaidadiazroa.substack.com/p/your-first-week-with-your-second), [infraestructura para pensar](https://adelaidadiazroa.substack.com/p/it-stopped-being-a-second-brain)) y la [página del programa 30X](https://30x.com/ai-second-brain).
Nota: el nombre correcto es **Mycelium** (no "Myelium").

## Qué es
Capa de configuración para Claude Code (licencia MIT) que arma un vault de Obsidian con memoria, journaling, rendición de cuentas y panel de asesores. No usa base vectorial; usa tu suscripción de Claude.

## Cómo funciona
- **Vault = fuente de verdad.** `CLAUDE.md` se carga cada sesión.
- **Tres capas de memoria:** (1) 5 notas de contexto operativo leídas siempre (Start Here, Current Priorities, Open Loops, Last Session, CLAUDE.md); (2) resúmenes por área (~200-400 palabras) y resúmenes mensuales del journal; (3) archivo profundo (~5.000 notas) solo cuando hace falta. Principio: comprimir primero, buscar después.
- **Hooks:** guardas deterministas antes de escribir (frontmatter obligatorio, etc.) y rutina de cierre de sesión que archiva decisiones, pendientes e ideas.
- **Comandos:** `/journal`, `/coaching`, `/weekly`, `/monthly`, `/patterns`, `/graphify`, `/meeting-todos`, `/optimize-brain`, `/second-brain-mapping`.
- **Panel de asesores:** 3 a 5 voces por decisión, al menos una que discrepe.
- **15 reglas de rendición de cuentas** en `CLAUDE.md` ("dime la verdad aunque duela").
- **MCP complementarios:** WhatsApp (`whatsapp-mcp`, Go), Google Workspace, Slack, Substack; con confirmación antes de escribir y registro de auditoría.

## Aprendizajes de ella
- La arquitectura importa más que las herramientas.
- La IA por defecto es complaciente: hay que pedirle honestidad explícita.
- Un grafo con ruido es peor que ninguno; notas sin enlaces gastan tokens.
- La personalización (qué preguntas, calibrar el panel) no se delega.

## Seguridad: advertencias
- El instalador registra hooks que **aprueban ediciones de archivos y comandos de shell sin preguntar**.
- Instalación por script descargado: revisar el repo antes.
- Envía un ping anónimo de instalación (`MYCELIUM_NO_PING=1` lo desactiva).
- En Windows el bootstrap instala menos cosas (los packs de skills de terceros no están portados).
- Requiere Claude Code 2.1.133+ y cuenta de pago.
- Su artículo no trata los riesgos de privacidad de cargar años de diarios y datos de relaciones.

## Programa 30X "AI Second Brain"
3 semanas, virtual. Instructoras/es: Adelaida Díaz-Roa, Danny Bravo (co-creador), Nelly Ortiz (mentora invitada, cofundadora de MyceliumAI). La página no publica temario, precio ni requisitos.
