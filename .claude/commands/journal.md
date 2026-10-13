---
description: Entrevista de journaling del día; crea la entrada y actualiza el vault
argument-hint: [opcional: texto o transcripción de voz del día]
---

Haz el journaling de hoy con Pao. Sigue `CLAUDE.md` (lee la Capa 1 primero).

## 1. Entrada
- Si Pao pasó texto o una transcripción en `$ARGUMENTS`, úsalo como base.
- Si no, entrevístala **de una pregunta a la vez**, en español. Empieza con "¿Cómo fue tu día?" y profundiza. No aceptes respuestas superficiales: si dice "bien" o "cansada", pregunta por qué y qué lo causó.
- Cubre: qué pasó, cómo se sintió, decisiones y pendientes, con quién habló.
- Máximo 6 preguntas, salvo que Pao quiera seguir.

## 2. Panel (solo si hay una decisión o duda)
Si aparece una decisión de dinero, tiempo o relaciones, consulta de 3 a 5 voces de `advisors/`, con al menos una que discrepe. Resume sus puntos en pocas líneas. Pao decide.

## 3. Escribir
Crea `journal/AAAA-MM-DD.md` (fecha de hoy) usando `journal/_plantilla.md`:
- Frontmatter: `fecha`, `contexto: personal`, `tipo: journal`, `estado_animo` (una palabra, solo si Pao lo dijo).
- Texto en la voz de Pao, fiel a lo que dijo. **No inventes hechos ni emociones.**
- Enlaza con `[[ ]]` a personas, proyectos y decisiones existentes.

## 4. Actualizar el vault
- **Personas:** por cada persona mencionada con información relevante, actualiza o crea `people/nombre.md` (plantilla `people/_plantilla.md`). Si hay una persona nueva, pregunta el `contexto` si no es obvio. Cada hecho nuevo lleva `[[journal/AAAA-MM-DD]]` como fuente.
- **Pendientes:** agrega a `meta/open-loops.md` los pendientes nuevos y cierra los que Pao dijo que terminó.
- **Decisiones:** si se decidió algo, regístralo en `meta/decision-log.md`.
- No dupliques información que ya está en otra nota: enlázala.

## 5. Cierre
Responde con: (a) una pregunta de **punto ciego** basada en lo que dijo hoy, formulada con honestidad, no con halagos; (b) lista de archivos creados o modificados.

## Límites
Si Pao menciona datos de terceros muy personales, anótalos solo si son necesarios para su trabajo o su vida con esa persona. Nada de credenciales ni claves.
