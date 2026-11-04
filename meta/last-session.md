---
fecha: 2026-11-04
tipo: contexto-operativo
---

# Última sesión (2026-11-04)

## Qué se hizo
- **Eliminación total de rutas de archivos y avisos de propuestas en WhatsApp:**
  - Removido el bloque `extra` en `kapso_whatsapp_bot.py` (`procesar_mensaje_texto`, `procesar_audio`, `procesar_imagen`) que adjuntaba `📝 Journal: journal/...`, `📁 Minuta: sources/...`, `📷 Imagen: journal/...` y `📋 1 propuesta(s) para open-loops`.
  - Las respuestas por WhatsApp ahora son 100% limpias, humanas y conversacionales, sin metadatos internos del sistema ni rutas de archivos.
- **Corrección de clasificación de retroalimentación conversacional (evitar tareas falsas):**
  - Identificada la causa por la cual decir *"esta publicación ya la hice"* agendaba una tarea en `journal/2026-11-03.md`: el clasificador interpretaba "ya la hice" como un reporte de actividades completadas.
  - Implementada la función de protección `_es_feedback_conversacional` en `kapso_whatsapp_bot.py` y reforzado el prompt de clasificación en `audio_processor.py` (`analizar_contenido_con_ia`) para catalogar comentarios, correcciones y cambios de idea estrictamente como `consulta_general` con listas vacías de tareas y compromisos.
  - Eliminada la entrada errónea de actividad en `journal/2026-11-03.md`.
- **Regla de originalidad y generación automática de propuestas alternativas para LinkedIn:**
  - Corregido el problema donde el bot repetía textualmente publicaciones anteriores encontradas en el vault (ej: el panel de Econova / Innovaética).
  - En `audio_processor.py`, las publicaciones previas indexadas ahora se marcan explícitamente como antecedentes históricos para no repetirlas.
  - Al recibir una solicitud de post o retroalimentación indicando que un post ya se publicó ("esta publicación ya la hice"), el bot ahora reconoce con calidez en una sola frase breve y entrega de inmediato una nueva propuesta completa para LinkedIn con un enfoque fresco, hook provocador y estructura canonical Hunter.
- **Reinicio del bot en vivo:**
  - Detenidos los procesos anteriores y levantado `iniciar_kapso_bot.ps1` con túnel activo y webhook sincronizado en Kapso.
  - Validación de frontmatter al 100% (0 de 134 notas con problemas).

## Quedó a medias
- Validar con Diego y el equipo los campos marcados como `[COMPLETAR]` en el documento institucional de Campuslands (detalles específicos de programas y organigrama).
- Continuar con las pruebas de WhatsApp real (OL-017) y rotación de token (OL-013).

## Siguiente paso
- Reenviar la imagen o una nueva foto por WhatsApp para confirmar que se descargue y se responda de inmediato.
