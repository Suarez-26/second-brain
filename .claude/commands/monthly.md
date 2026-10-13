---
description: Resumen mensual y tendencias; comprime el mes para la Capa 2
argument-hint: [opcional: mes AAAA-MM; por defecto el mes anterior completo]
---

Genera el resumen mensual. Sigue `CLAUDE.md`.

1. Mes = `$ARGUMENTS` o el mes anterior completo.
2. Lee los `journal/resumenes/AAAA-Wnn.md` de ese mes; abre entradas diarias solo si hace falta aclarar algo.
3. Escribe `journal/resumenes/AAAA-MM.md` (frontmatter: `fecha`, `contexto: personal`, `tipo: resumen-mensual`) con:
   - Resumen del mes (máx. 200 palabras).
   - Tendencias y cambios respecto al mes anterior (con enlaces a las semanas que lo sustentan).
   - Decisiones importantes y su resultado.
   - Qué se logró frente a `meta/current-priorities.md`.
   - Qué se repitió sin resolverse.
   - Una pregunta de punto ciego.
4. Revisa las notas de `areas/`: propón actualizaciones breves y aplícalas solo si Pao confirma.
5. No inventes datos: si faltan semanas, dilo.
