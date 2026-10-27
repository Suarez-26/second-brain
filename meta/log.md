---
fecha: 2026-10-13
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
2026-10-17 | creación | automation/whatsapp-mcp/whatsapp-bridge-node/index.js, automation/claude_whatsapp_bot.py, automation/bot_config.json, automation/iniciar_whatsapp_claude.ps1, .mcp.json, PARCHES.md | puente WhatsApp en Node.js (puerto 8085), MCP en Claude Desktop/Code y bot interactivo de Claude (chat propio + copiloto/auto prospectos)
2026-10-20 | extracción e investigación exhaustiva | diego_investigacion/ (01, 01b, 01c, 02_publicaciones/ [107 posts + comentarios + reacciones + menciones], 03_imagenes/, 04_videos_y_audios/ [>50 videos], 05_transcripciones/ [4 formatos], 06_analisis_maestro_diego.md), investigacion/diego-tarazona/memoria/{perfil,cronologia,campuslands-hechos,pendientes-de-confirmar}.md, people/diego-tarazona.md | extracción 100% íntegra desde el primer al último post de Diego Tarazona en LinkedIn con Playwright, descarga 720p de videos y transcripción multimodal con Faster-Whisper
2026-10-20 | interconexión total del grafo | diego_investigacion/README.md, diego_instagram/README.md, organizaciones/ (8 notas + README), people/ (andres-lizarazo, sandra-charry, maria-camila-canas), diego_investigacion/02_publicaciones/ (337 notas conectadas), diego_investigacion/05_transcripciones/ (83 notas conectadas), diego_instagram/ (77 notas conectadas), campuslands corpus (149 notas conectadas) | eliminación de huérfanos y colapso del anillo exterior en la vista gráfica de Obsidian hacia los nodos centrales y temáticos
2026-10-20 | ingesta institucional canónica | sources/presentaciones/campus-magazine-may-2026-canva.md, presentaciones/README.md, investigacion/diego-tarazona/memoria/{cronologia,perfil,campuslands-hechos,pendientes-de-confirmar}.md, people/diego-tarazona.md | extracción íntegra de la revista de Canva (12 páginas, Equipo Hunter Mayo 2026); resolución canónica de nacimiento (1982), frase materna, primera sede (Provincia de Soto II), ecosistema de empresas (IAF, Plazoleta Digital), 4 pilares formativos y proyección Ciudadela 2027

2026-10-22 11:47 | AUDIO_INGEST | journal/2026-10-22.md | Audio transcripto (audio.ogg)
2026-10-22 11:50 | AUDIO_INGEST | journal/2026-10-22.md | Audio transcripto (audio.ogg)
2026-10-22 12:51 | TASK_ADD | meta/open-loops.md | Nuevo loop: Elaborar un análisis sobre el impacto y futuro de la inteligencia artificial y los agentes
2026-10-22 12:51 | JOURNAL_REPORT | journal/2026-10-22.md | Actividades registradas (12:51)
2026-10-22 12:52 | MEETING_MINUTES | sources/reuniones/2026-10-22_acuerdo-del-cohete-social-para-estratos-.md | Minuta: Acuerdo del cohete social para estratos 1 y 2
2026-10-22 12:52 | TASK_ADD | meta/open-loops.md | Nuevo loop: Enviar la propuesta formal el viernes
2026-10-22 13:13 | TASK_ADD | meta/open-loops.md | Nuevo loop: Buscar y recomendar cursos de Python para principiantes
2026-10-22 13:13 | JOURNAL_REPORT | journal/2026-10-22.md | Actividades registradas (13:13)
2026-10-22 15:45 | INBOX_EXTERNO | inbox/whatsapp/573001234567.md | Mensaje de 573001234567
2026-10-22 16:02 | INBOX_EXTERNO | inbox/whatsapp/573173769917.md | Mensaje de 573173769917
2026-10-22 16:02 | INBOX_EXTERNO | inbox/whatsapp/573173769917.md | Mensaje de 573173769917
2026-10-24 10:41 | INBOX_EXTERNO | inbox/whatsapp/573247571239.md | Mensaje de 573247571239
2026-10-24 10:41 | INBOX_EXTERNO | inbox/whatsapp/573247571239.md | Mensaje de 573247571239
2026-10-24 10:43 | INBOX_EXTERNO | inbox/whatsapp/573247571239.md | Mensaje de 573247571239
2026-10-24 10:46 | INBOX_EXTERNO | inbox/whatsapp/573247571239.md | Mensaje de 573247571239
2026-10-24 10:47 | INBOX_EXTERNO | inbox/whatsapp/573247571239.md | Mensaje de 573247571239
2026-10-24 10:47 | INBOX_EXTERNO | inbox/whatsapp/573247571239.md | Mensaje de 573247571239
2026-10-24 11:35 | INBOX_EXTERNO | inbox/whatsapp/573247571239.md | Mensaje de 573247571239
2026-10-24 11:37 | INBOX_EXTERNO | inbox/whatsapp/573247571239.md | Mensaje de 573247571239
2026-10-24 12:19 | INBOX_EXTERNO | inbox/whatsapp/573247571239.md | Mensaje de 573247571239
2026-10-24 12:19 | INBOX_EXTERNO | inbox/whatsapp/573247571239.md | Mensaje de 573247571239
2026-10-24 12:21 | INBOX_EXTERNO | inbox/whatsapp/573247571239.md | Mensaje de 573247571239
2026-10-24 12:22 | INBOX_EXTERNO | inbox/whatsapp/573247571239.md | Mensaje de 573247571239
2026-10-24 12:23 | INBOX_EXTERNO | inbox/whatsapp/573247571239.md | Mensaje de 573247571239
2026-10-24 12:23 | INBOX_EXTERNO | inbox/whatsapp/573247571239.md | Mensaje de 573247571239
2026-10-24 12:24 | INBOX_EXTERNO | inbox/whatsapp/573247571239.md | Mensaje de 573247571239
2026-10-24 12:25 | INBOX_EXTERNO | inbox/whatsapp/573247571239.md | Mensaje de 573247571239
2026-10-24 12:26 | INBOX_EXTERNO | inbox/whatsapp/573247571239.md | Mensaje de 573247571239
2026-10-24 12:53 | INBOX_EXTERNO | inbox/whatsapp/573247571239.md | Mensaje de 573247571239
2026-10-27 | cambio | automation/whatsapp_webhook_server.py | Token de acceso y verify token de Meta sacados del código a .env; Pao rotará el token (sesión manual)
2026-10-27 | cambio | .gitignore | Ignorados medios pesados (mp4/wav/ogg, imágenes y videos de diego_*), __pycache__, *.log y estado del bot (sesión manual)
2026-10-27 | cambio | automation/kapso_whatsapp_bot.py | Respuestas a terceros pasan a modo copiloto (borrador al admin: Enviar/Editar/Descartar); remitente vacío ya no cuenta como admin (sesión manual)
2026-10-27 09:46 | cambio | meta/open-loops.md | IDs estables OL-nnn para los pendientes abiertos
2026-10-27 09:52 | cambio | automation/ | Refactorización: vault_io, cola SQLite, pendientes con propuestas, índice FTS5, MCP buscar, HMAC en webhook Kapso (sesión manual)
2026-10-27 09:52 | cambio | automation/claude_whatsapp_bot.py | Modo auto desactivado: terceros siempre por copiloto (sesión manual)
2026-10-27 09:52 | cambio | meta/open-loops.md | IDs OL-001..OL-012 asignados; nuevos OL-013..OL-018 (sesión manual)
2026-10-27 09:52 | cambio | journal/2026-10-24.md | Movido a automation/_archivo/pruebas_journal/: era prueba del bot (sesión manual)
2026-10-27 09:52 | cambio | inbox/whatsapp/ | 3 historiales de terceros movidos a inbox/whatsapp/otros/ (sesión manual)
2026-10-27 09:52 | cambio | varios | Frontmatter completado en 32 notas (fecha desde git o fecha de creación conocida; contexto empresarial -> campuslands) (sesión manual)
2026-10-27 09:52 | cambio | journal/resumenes/ | Creados 2026-W42 y 2026-W43 (sesión manual)
2026-10-27 11:02 | INBOX_EXTERNO | inbox/whatsapp/otros/15551234567.md | Mensaje de 15551234567
2026-10-27 11:02 | BORRADOR | inbox/whatsapp/otros/15551234567.md | Borrador #1 en espera de aprobación
2026-10-27 11:02 | INBOX_EXTERNO | inbox/whatsapp/otros/573167755887.md | Mensaje de 573167755887
2026-10-27 11:03 | BORRADOR | inbox/whatsapp/otros/573167755887.md | Borrador #2 en espera de aprobación
2026-10-27 11:07 | INBOX_EXTERNO | inbox/whatsapp/otros/15551234567.md | Mensaje de 15551234567
2026-10-27 11:08 | INBOX_EXTERNO | inbox/whatsapp/otros/15551234567.md | Mensaje de 15551234567
2026-10-27 11:08 | BORRADOR | inbox/whatsapp/otros/15551234567.md | Borrador #3 en espera de aprobación
2026-10-27 11:11 | INBOX_EXTERNO | inbox/whatsapp/otros/15551234567.md | Mensaje de 15551234567
2026-10-27 11:12 | BORRADOR | inbox/whatsapp/otros/15551234567.md | Borrador #4 en espera de aprobación
2026-10-27 11:37 | cambio | automation/audio_processor.py, automation/claude_whatsapp_bot.py, linkedin/voz-diego/logica-de-razonamiento-diego.md, .claude/commands/responder-prospecto.md | Ajuste de modo de respuesta a tono neutro, simple y directo a la pregunta, ceñido estrictamente al guion validado (sesión manual)
2026-10-27 11:41 | INBOX_EXTERNO | inbox/whatsapp/otros/15551234567.md | Mensaje de 15551234567
2026-10-27 11:41 | BORRADOR | inbox/whatsapp/otros/15551234567.md | Borrador #5 en espera de aprobación
2026-10-27 11:42 | INBOX_EXTERNO | inbox/whatsapp/otros/15551234567.md | Mensaje de 15551234567
2026-10-27 11:43 | BORRADOR | inbox/whatsapp/otros/15551234567.md | Borrador #6 en espera de aprobación
