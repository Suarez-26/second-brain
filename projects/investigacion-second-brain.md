---
tipo: investigacion
contexto: personal
fecha: 2026-10-12
---

# Investigación: cómo crear un second brain con IA

Síntesis de búsquedas web. La mayoría de las fuentes son blogs, foros y páginas de proveedores, no documentación oficial; tómalas como orientación y verifica los detalles de cada herramienta en su README antes de instalar. Donde algo es inferencia mía, lo marco.

## 1. Idea central
Un second brain es una memoria persistente sobre ti (contexto, decisiones, personas, proyectos) que una IA puede leer y actualizar, para no tener que re-explicarte en cada sesión. Del video de 30X: contexto "ilimitado" + agentes que ejecutan + panel de asesores + journaling como combustible.
## 2. Tres capas que casi todos los diseños comparten
1. **Fuentes crudas (inmutables):** documentos, chats, transcripciones. Aquí: `sources/`.
2. **Conocimiento compilado (lo mantiene la IA):** notas enlazadas por persona, proyecto, decisión. Aquí: `people/`, `projects/`, `journal/`.
3. **Esquema / reglas:** un archivo que le dice a la IA cómo operar. Aquí: `CLAUDE.md`.

El patrón de wiki mantenida por LLM (atribuido a Karpathy, abril 2026) añade tres operaciones: **ingest** (procesar fuentes nuevas, actualizar páginas y marcar contradicciones), **query** y **lint** (revisiones de salud). Los detalles vienen de resúmenes secundarios, no leí su texto original. [Guía de Starmorph](https://blog.starmorph.com/blog/karpathy-llm-wiki-knowledge-base-guide), [AI Builder Club](https://www.aibuilderclub.com/blog/karpathy-llm-wiki).

## 3. Metodologías de organización
| Método | Organiza por | Fortaleza | Costo |
|---|---|---|---|
| PARA / CODE (Tiago Forte) | Qué tan accionable es (Proyectos, Áreas, Recursos, Archivo) | Ligero, práctico | Puede volverse un archivo que crece sin curar |
| Zettelkasten | Conexión entre ideas, notas atómicas | Descubrimiento de ideas, compone con el tiempo | Exige disciplina y tiempo |
| LYT (mapas de contenido) | Enlaces y mapas | Término medio | Casi no encontré fuentes; verificar en el material de Nick Milo |

Se pueden combinar: PARA para lo accionable, enlaces tipo Zettelkasten para conocimiento. Con IA, la carga de mantener los enlaces baja, porque la IA los escribe. (Inferencia mía.) Fuentes: [Zain Rizvi](https://zainrizvi.io/blog/remembering-what-you-read-zettelkasten-vs-para/), [Saner.ai](https://blog.saner.ai/note-taking-methods/).

## 4. Opciones técnicas de memoria
- **Markdown + índice (recomendado para empezar):** archivos planos, transparentes, editables, versionables. Suficiente mientras el corpus quepa razonablemente en contexto o se navegue con un índice. [MindStudio: wiki vs RAG](https://www.mindstudio.ai/blog/llm-wiki-vs-rag-internal-codebase-memory).
- **Búsqueda híbrida / RAG:** súmala cuando el vault crezca. El RAG ingenuo no es un techo, pero tampoco es perfecto: en un benchmark de memoria de agentes de 2026 el baseline simple obtuvo ~38–43 % frente a ~57–59 % del método estructurado. [LongMemEval-V2](https://arxiv.org/pdf/2605.12493). Ese benchmark no compara contra markdown.
- **Capas de memoria como servicio:**
  - *Mem0:* se añade a un agente existente, rápido de adoptar, sin ventanas de validez temporal.
  - *Zep / Graphiti:* grafo temporal, bueno si importa "qué era cierto cuándo"; más trabajo operativo.
  - *Letta (MemGPT):* el agente es su memoria; implica vivir en su servidor.
  Las comparaciones vienen de proveedores y blogs afines, con precios que no coinciden entre fuentes. [Mem0 vs Zep vs Letta](https://dev.to/plur9/mem0-vs-letta-vs-zep-which-should-you-use-for-agent-memory-1n8m).
- **Criterio de división (de una fuente de AWS):** memoria a largo plazo responde "quién es el usuario y qué pasó"; RAG responde "qué dicen las fuentes confiables ahora".

## 5. Stack práctico: Obsidian + Claude
- Un vault es una carpeta de `.md`; Claude lee y edita sin integración especial. El `CLAUDE.md` raíz se lee en cada sesión. [Guía Obsidian + Claude Code](https://dev.to/joao_victorsouza_ef8ff8a/obsidian-claude-code-as-a-second-brain-1n71), [Substack](https://noahvnct.substack.com/p/how-to-build-your-ai-second-brain).
- Convenciones que se repiten: frontmatter (tipo, fecha, tags), `[[wikilinks]]` para personas/proyectos/decisiones, `index.md` como catálogo y `log.md` como bitácora, y `CLAUDE.md` adicionales por carpeta.
- Truco útil: pedirle a Claude que te **entreviste** para llenar tu contexto personal.
- Comandos propios (`/ingest`, `/query`, `/lint`) como slash commands en `.claude/commands/`. [Repo de ejemplo](https://github.com/eugeniughelbur/obsidian-second-brain).

## 6. Conectar con Claude Desktop (MCP)
- Opción simple: servidor MCP de **filesystem** apuntando al vault. Config en `%APPDATA%\Claude\claude_desktop_config.json`, requiere Node.js, usar `npx -y`, escapar `\\` o usar `/`, y reiniciar Claude Desktop por completo. [Tutorial](https://zazencodes.substack.com/p/obsidian-mcp-setup-tutorial-for-claude).
- Opción Obsidian: servidor `obsidian-mcp` con el plugin Local REST API (requiere clave API y Obsidian abierto). Más preciso, más piezas.
- Alternativa: usar **Claude Code** sobre la carpeta, sin MCP. Para edición de archivos suele ser más directo; Desktop+MCP se justifica para conectores externos.

## 7. Captura (lo que alimenta el cerebro)
Patrón: captura → transcribir con Whisper → limpiar con LLM → escribir `journal/AAAA-MM-DD.md` → sincronizar.
- Local (privado): Whisper modelo *small* en Windows. [Guía](https://voxbooster.com/blog/voice-habit-tracker-whisper-windows/).
- Automatizado: n8n con Telegram + Whisper + LLM a markdown. [Plantilla n8n](https://n8n.io/workflows/15652-convert-telegram-voice-notes-into-markdown-journals-with-groq-whisper-and-gemini/). Relevante porque ya usas n8n en wikimaster.
- Plugin de Obsidian con Whisper y posprocesado. [Plugin](https://community.obsidian.md/plugins/whisper).

## 8. Seguridad y privacidad (importante)
- **Inyección de prompts indirecta:** un documento, correo o mensaje ingestado puede traer instrucciones ocultas. [OWASP MCP06](https://owasp.org/www-project-mcp-top-10/2025/MCP06-2025–Prompt-InjectionviaContextual-Payloads).
- **Triada letal:** datos privados + contenido no confiable + canal de salida. Rómpela: no combines notas sensibles con herramientas que navegan o envían correo/mensajes. [NHIMG](https://nhimg.org/?p=32682).
- Buenas prácticas: mínimo privilegio, aprobar manualmente acciones salientes, solo servidores MCP revisados, registro de acciones, y probar con contenido malicioso plantado.
- **WhatsApp no oficial:** riesgo de bloqueo de cuenta y de exfiltración; usar número secundario y solo lectura al inicio. [Análisis](https://www.bot.space/blog/whatsapp-api-vs-unofficial-tools-a-complete-risk-reward-analysis-for-2025).
- **Datos de terceros** (p. ej. colegas): solo lo necesario para el trabajo y de fuentes a las que tengas derecho; mantener `contexto:` separado.

## 9. Riesgos de diseño propios del patrón
- Requiere mantenimiento (lint periódico); un vault muy grande rebasa el contexto. [Starmorph](https://blog.starmorph.com/blog/karpathy-llm-wiki-knowledge-base-guide).
- La IA puede alucinar: exigir cita de fuente en cada afirmación (ya está en `CLAUDE.md`).
- Complacencia del modelo: reglas explícitas de objetar (ya incluidas) y panel con voces opuestas.

## 10. Plan recomendado para este vault
1. **Semana 1:** journaling diario (texto o voz). Entrevista inicial para llenar tu contexto en `CLAUDE.md`.
2. Agregar `index.md` y `log.md`, y slash commands `/ingest`, `/query`, `/lint` en `.claude/commands/`.
3. Conectar Claude Desktop con el MCP de filesystem al vault.
4. Cargar fuentes de trabajo en `inbox/` y procesarlas con trazabilidad a `sources/`.
5. Captura por voz (Whisper local o n8n).
6. Solo después: búsqueda híbrida, conectores (correo, WhatsApp) con las salvaguardas de la sección 8.
7. Revisión mensual: lint, contradicciones y ajuste del panel de asesores.

## Preguntas abiertas
- ¿Quién y qué material de terceros (p. ej. Diego Tarazona) se puede cargar, y con qué fin?
- ¿Se usará Obsidian como visor, o solo Claude?
- ¿Cuánto material habrá en 6 meses? Define cuándo añadir búsqueda.
