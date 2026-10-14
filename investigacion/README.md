---
fecha: 2026-10-14
contexto: campuslands
tipo: indice
---

# Investigación de personas (Capa 3)

Dossiers sobre la trayectoria **pública y profesional** de una persona. Separado de `linkedin/` a propósito: aquí vive la evidencia externa; `linkedin/` solo recibe lo que Pao apruebe.

## Estructura
```
investigacion/<slug>/
  dossier.md        entregable (lo que se lee)
  verificacion.md   cruce de fechas y contradicciones
  memoria/          perfil · cronologia · temas-y-posturas · campuslands-hechos · pendientes-de-confirmar (lo limpio, se lee primero)
  corpus/           transcripciones completas (Capa 3, uso privado, no se republican)
  fuentes/          prensa.md · video-podcast.md · trayectoria.md · empresa.md (crudo, con URL y fecha)
```
Ficha corta en `people/<slug>.md`. Procedimiento: `.claude/commands/investigar-persona.md`.

## Personas
- [[diego-tarazona]] (memoria: [[memoria/README]]; dossier: [[investigacion/diego-tarazona/dossier]]) — objetivo: alimentar [[linkedin-diego-tarazona]].

## Límites
Solo información pública y profesional, siempre con fuente. Lo que Diego dijo en público no es su voz validada (ver `linkedin/CLAUDE.md`). Plantillas: `_plantilla-dossier.md`, `_plantilla-fuente.md`.
