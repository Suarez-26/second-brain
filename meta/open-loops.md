---
fecha: 2026-10-27
tipo: contexto-operativo
---

# Pendientes abiertos

Formato: `- [ ] [OL-nnn] pendiente (origen: [[nota]], desde AAAA-MM-DD)`. El ID es estable: la automatización cierra o agrega solo por propuesta aprobada (`Aceptar N`).

- [x] ~~Aclarar qué material sobre Diego Tarazona se carga~~ → resuelto 2026-10-13: es la estrategia de LinkedIn de Diego, ver [[linkedin/README]] y [[plan-de-trabajo]]
- [ ] [OL-001] Consultar a mano RUES (3 NIT), Cámara de Comercio, listado de El País y Fedesoft; confirmar con Diego universidad y año de fundación (ver [[pendientes-de-confirmar]], desde 2026-10-14)
- [ ] [OL-002] Verificar las citas contra el audio antes de reutilizarlas (subtítulo automático; las 19 transcripciones ya tienen resumen propio; ver [[temas-y-posturas]], desde 2026-10-14)
- [ ] [OL-003] Preguntar a Diego: cambio de postura sobre IA (2024 vs 2026), año de origen, gratuito vs pago diferido (ver [[cifras-y-contradicciones-propias]], desde 2026-10-14)
- [ ] [OL-004] Pedir a Diego sus enlaces oficiales (LinkedIn, Instagram, YouTube, X) (desde 2026-10-14)
- [ ] [OL-005] Decidir si el objetivo del dossier pasa de `linkedin-diego` a `perfil-completo` (desde 2026-10-14)
- [ ] [OL-006] Revisar a mano la alerta del agente sobre la nota de Metropolitano 2026-10-09 (probable falso positivo; desde 2026-10-14)
- [ ] [OL-007] Que Campuslands valide la base de conocimiento de prospectos: costo y pago, admisión, cohortes, empleabilidad y canal oficial (ver [[prospectos/base-de-conocimiento]], desde 2026-10-16)
- [ ] [OL-008] Decidir si las skills de Kapso se quedan en el vault: hoy están instaladas en `.claude/skills/` y `.agents/skills/`, y `iniciar_kapso_bot.ps1` las usa (revisadas el 2026-10-16; instaladas después sin registro de decisión)
- [ ] [OL-009] Profundizar detalles biográficos personales en `start-here.md` mediante entrevista (contexto operativo base completado 2026-10-16)
- [x] ~~Conectar Claude Desktop al vault con el MCP de filesystem~~ → conectado junto con el MCP de WhatsApp y bot interactivo (2026-10-17, ver [[automation/PARCHES]])
- [ ] [OL-010] Revisar el código de ai-brain-starter antes de instalar nada (ver [[mycelium-ai-brain-starter]])
- [ ] [OL-011] Seguimiento de meta financiera: ahorro de $2.800.000 para portátil a fin de año (origen: [[projects/ahorro-portatil-2026]], desde 2026-10-21)

- [ ] [OL-012] Enviar la propuesta formal el viernes (vía WhatsApp 2026-10-22). **Confirmar si la reunión fue real o una prueba del bot**; el viernes era el 24-oct (ver [[2026-W43]])
- [ ] [OL-013] Rotar el token de acceso de Meta (WhatsApp Cloud API) y actualizar `WHATSAPP_ACCESS_TOKEN` en `.env` (estuvo escrito en el código; desde 2026-10-27)
- [ ] [OL-014] Borrar `diego_investigacion/.chrome_profile/` (cookies de la sesión de LinkedIn) cuando termine la extracción (desde 2026-10-27)
- [ ] [OL-015] Decidir qué hacer con 4 `.txt` de `sources/prensa_y_web/` que suman 80 MB y parecen descargas fallidas, p. ej. `art_vanguardia_leeche.txt` con 56 MB (desde 2026-10-27)
- [ ] [OL-016] Acordar con Diego si el bot puede hablar en su nombre con terceros; hoy los borradores salen firmados "Equipo Campuslands" (ver [[automation/PARCHES]], desde 2026-10-27)
- [ ] [OL-017] Arrancar el bot con `iniciar_bot.bat` y probar el ciclo real: mensaje de un tercero → borrador → `Enviar N` (probado solo con simulaciones; desde 2026-10-27)
- [ ] [OL-018] Confirmar quién es el administrador del bot (`ADMIN_PHONE_NUMBER`, el código lo llama "Tomás") y quién opera este vault (desde 2026-10-27)

## Cerrados
- [x] ~~Reunirse con la persona que lleva el LinkedIn de Diego y conseguir los 9 archivos reales~~ → integrados en `linkedin/` y archivados intactos en `sources/linkedin/` (2026-10-16)
- [x] ~~Definir pilares editoriales, territorios y reglas visuales de Diego~~ → resuelto con la integración de los archivos 02, 03 y 08 oficiales (2026-10-16)
- [x] ~~Instalar `yt-dlp` para subtítulos~~ → instalado 2026-10-14 (ver [[decision-log]])
- [x] ~~Segunda tanda de video, podcasts y transcripciones de Diego~~ → hecha 2026-10-14

Ver [[current-priorities]].