---
tipo: bitacora
---

# Bitácora de cambios

Formato: `AAAA-MM-DD HH:MM | acción | archivo | fuente`. La escribe la corrida automática y las sesiones manuales. Las alertas llevan `ALERTA`.

2026-10-13 | creación | automation/, inbox/whatsapp/, .claude/commands/ingest.md, diario-automatico.md | sesión con Pao
2026-10-13 | creación | linkedin/ (9 fuentes, plantillas, plan), projects/linkedin-diego-tarazona.md | sesión con Pao
2026-10-13 | cambio | automation/exportar_whatsapp.py, chats_permitidos.json, ingest.md | lista de chats permitidos
2026-10-14 | creación | .claude/commands/investigar-persona.md, investigacion/ (README, plantillas, diego-tarazona/), people/diego-tarazona.md | sesión con Pao
2026-10-14 | creación | investigacion/diego-tarazona/fuentes/{prensa,video-podcast,trayectoria,empresa}.md | 4 agentes /investigar-persona
2026-10-14 | creación | investigacion/diego-tarazona/verificacion.md | agente verificador
2026-10-14 | cambio | investigacion/diego-tarazona/dossier.md, people/diego-tarazona.md | síntesis fase 1
2026-10-14 | ALERTA | investigacion/diego-tarazona/fuentes/trayectoria.md | WebFetch reportó texto dirigido a agentes en nota de Metropolitano 2026-10-09; probable eco del prompt, no se obedeció nada
2026-10-14 | creación | investigacion/diego-tarazona/memoria/ (README, perfil, cronologia, temas-y-posturas, campuslands-hechos, pendientes-de-confirmar) | dossier y fuentes de la fase 1
2026-10-14 | cambio | .claude/commands/investigar-persona.md, investigacion/README.md, people/diego-tarazona.md | higiene del orquestador y memoria separada
