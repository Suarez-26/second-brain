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
2026-10-14 | instalación | yt-dlp 2026.08.19 (pip --user, fuera del vault) | permiso de Pao
2026-10-14 | creación | investigacion/diego-tarazona/corpus/ (19 transcripciones auto de YouTube) | agente video-podcast
2026-10-14 | cambio | memoria/{perfil,cronologia,temas-y-posturas,campuslands-hechos,pendientes-de-confirmar}.md, fuentes/video-podcast.md, dossier.md | segunda tanda, un agente por nota
2026-10-14 | cambio | memoria/cronologia.md | se quitó una edad exacta (dato personal) colada por un agente
2026-10-14 | creación | investigacion/diego-tarazona/memoria/resumenes/ (11 resúmenes de transcripciones) | 4 agentes
2026-10-14 | creación | investigacion/diego-tarazona/memoria/cifras-y-contradicciones-propias.md | agente consolidador
2026-10-14 | cambio | memoria/temas-y-posturas.md (29 filas, 12 citas, cambios de postura), memoria/README.md | agente consolidador
2026-10-14 | creación | investigacion/diego-tarazona/memoria/resumenes/ (6 resúmenes más, total 17) | 3 agentes
2026-10-14 | cambio | memoria/temas-y-posturas.md (+27 temas, +12 citas, 4 cambios de postura), memoria/cifras-y-contradicciones-propias.md (+~35 filas) | agente consolidador
2026-10-14 | cierre | meta/last-session.md, decision-log.md, open-loops.md | cierre de sesión
2026-10-16 | creación | prospectos/ (README, base-de-conocimiento), .claude/commands/responder-prospecto.md, inbox/prospectos/ | sesión con Pao
2026-10-16 | optimización | sources/linkedin/ (9 fuentes archivadas), linkedin/ (9 fuentes validadas e integradas), eliminación Linkedln/, .gitignore (*.exe), areas/ (campuslands, second-brain), meta/ (start-here, current-priorities, last-session, decision-log, open-loops), presentaciones/README.md, journal/2026-10-16.md | consolidación del vault a nivel 10/10

