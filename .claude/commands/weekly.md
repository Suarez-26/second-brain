---
description: Resumen semanal del journal con patrones, pendientes y puntos ciegos
argument-hint: [opcional: semana en formato AAAA-Wnn; por defecto la semana actual o la última completa]
---

Genera el reporte semanal. Sigue `CLAUDE.md`.

## 1. Reunir
- Determina la semana (lunes a domingo). Usa `$ARGUMENTS` si viene; si no, la última semana completa.
- Lee las entradas de `journal/` de esa semana, `meta/open-loops.md`, `meta/current-priorities.md` y `meta/decision-log.md`.
- Si faltan días, dilo: no rellenes con suposiciones. Indica cuántos días hay entrada.

## 2. Analizar (solo con base en lo escrito)
- **Resumen:** 5 a 8 líneas de lo que pasó, con enlaces `[[journal/AAAA-MM-DD]]`.
- **Patrones:** temas, emociones o conductas que se repiten, con las fechas que lo sustentan. Si solo hay un caso, no lo llames patrón.
- **Decisiones tomadas** y su estado.
- **Pendientes:** cuáles se cerraron, cuáles llevan más de 2 semanas abiertos y deberían cerrarse, delegarse o eliminarse.
- **Prioridades vs. realidad:** compara `current-priorities.md` con en qué se fue realmente el tiempo. Señala sin rodeos si no coinciden.
- **Honestidad:** una sección de "lo que estás evitando" y una pregunta de punto ciego. Sin halagos ni consuelo vacío.

## 3. Escribir
Crea `journal/resumenes/AAAA-Wnn.md` con frontmatter (`fecha`, `contexto: personal`, `tipo: resumen-semanal`, `semana`).

## 4. Actualizar
- Ajusta `meta/open-loops.md` y, si Pao confirma, `meta/current-priorities.md`.
- Propón (no apliques sin confirmar) reglas nuevas si un error se repitió.

## 5. Cierre
Resume en 5 líneas lo más importante y lista los archivos tocados.
