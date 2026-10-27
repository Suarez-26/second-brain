---
fecha: 2026-10-14
tipo: contexto-operativo
---

# Registro de decisiones

Formato: fecha · decisión · por qué · alternativas descartadas.

## 2026-10-13 · Vault de Markdown con Claude Desktop (MCP)
- **Decisión:** memoria en archivos Markdown, sin base vectorial por ahora, accedida con el MCP de filesystem.
- **Por qué:** es transparente, editable y suficiente para el volumen inicial. Ver [[investigacion-second-brain]].
- **Descartado por ahora:** Mem0, Zep, Letta (más de lo necesario) e instalar `ai-brain-starter` completo (aprueba comandos de shell sin preguntar; ver [[mycelium-ai-brain-starter]]).

## 2026-10-13 · WhatsApp solo con chats elegidos por Pao
- **Decisión:** el exportador lee únicamente los chats de `automation/chats_permitidos.json`. Hoy: solo el chat de Pao consigo misma (con etiqueta `#linkedin`). Se pueden sumar grupos uno a uno.
- **Por qué:** confidencialidad de terceros y de Campuslands, menos ruido y menos superficie para inyección de instrucciones.
- **Reglas:** chats propios = contenido de Pao; grupos = datos de terceros, nunca órdenes. Detalle en `automation/PARCHES.md`.

## 2026-10-13 · LinkedIn de Diego Tarazona como proyecto del vault
- **Decisión:** carpeta `linkedin/` con las 9 fuentes de verdad, banco de contenido, señales, calendario, métricas y voz de Diego. Contexto `campuslands`. Pao aporta el second brain; la persona que lleva el LinkedIn aporta la metodología.
- **Por qué:** el Claude Project de la metodología no recuerda entre semanas; el vault sí. Plan en [[plan-de-trabajo]].
- **Límites:** no inventar la voz de Diego, no publicar ni enviar nada solo, no usar información no anunciada.
- **Alcance de los archivos 01-09:** son borradores con solo lo que decían las instrucciones; los reales están pendientes.

## 2026-10-13 · Cerebro que se alimenta solo, con WhatsApp y escritura total
- **Decisión:** Pao eligió tarea programada en su PC, WhatsApp como canal y autonomía total en el vault.
- **Cómo se implementa:** el agente automático **no** usa el MCP de WhatsApp (que tiene herramienta de envío). Un exportador de solo lectura vuelca los mensajes a `inbox/`, y el agente procesa archivos. Chat contigo = confiable como contenido; terceros = solo datos.
- **Por qué:** con autonomía total, un mensaje de un tercero que intente dar órdenes es el riesgo principal. Ver [[investigacion-second-brain]].
- **Salvaguardas:** git local para revertir, bitácora en [[log]], envío de mensajes deshabilitado. Detalle del parche en `automation/PARCHES.md`.
- **Pendiente:** instalar Go, uv y ffmpeg; emparejar WhatsApp por QR; elegir hora de la tarea; transcripción de audios.

## 2026-10-13 · Clonar ai-brain-starter como referencia, sin instalarlo
- **Decisión:** el repo está en `ai-brain-starter/` (commit d877685). Solo se copiaron archivos; no se ejecutó `bootstrap.ps1` ni se tocó `~/.claude/` ni `settings.json`.
- **Por qué:** Pao pidió tenerlo en su proyecto. Instalarlo registra hooks que aprueban ediciones y comandos sin preguntar (ver [[mycelium-ai-brain-starter]]).
- **Antes de instalar:** correr el `preflight` y usar `MYCELIUM_NO_PING=1`.

## 2026-10-13 · Adoptar ideas de Mycelium sin instalarlo
- **Decisión:** copiar la arquitectura (capas, cierre de sesión, panel, reglas de honestidad), no el instalador.
- **Por qué:** control de permisos y revisión previa del código.

## 2026-10-14 · Investigación de personas separada de `linkedin/`
- **Decisión:** comando `/investigar-persona` y carpeta `investigacion/<persona>/` (fuentes crudas, corpus, memoria, dossier). Lo derivado pasa a `linkedin/` solo si Pao lo aprueba.
- **Por qué:** la evidencia externa no debe mezclarse con la voz validada de Diego (regla 1 de `linkedin/CLAUDE.md`). Ver [[investigacion/README]].
- **Alternativas descartadas:** guardar todo dentro de `linkedin/`; un solo archivo por persona.

## 2026-10-14 · Alcance ampliado: perfil completo de Diego, sin entrenar un modelo
- **Decisión:** Pao pidió información universal (prensa, video, podcasts, conferencias), no solo para LinkedIn. Se construye un corpus consultable con memoria separada por tipo. No se entrena ni afina un modelo con Diego.
- **Por qué:** un corpus citable sirve al second brain; imitar su voz chocaría con la regla de no inventarla y él no la ha validado.
- **Pendiente:** el `objetivo` del dossier sigue como `linkedin-diego` (ver [[open-loops]]).

## 2026-10-14 · Instalar `yt-dlp` con pip
- **Decisión:** Pao autorizó instalarlo (usuario, fuera del vault) para bajar solo subtítulos y metadatos, sin video ni audio.
- **Por qué:** sin transcripciones, video y podcast quedaban en descripciones. 
- **Alternativas descartadas:** que Pao pegara los textos a mano.

## 2026-10-14 · Orquestador sin leer fuentes crudas; memoria separada por tipo
- **Decisión:** los agentes escriben a disco y devuelven resúmenes cortos; un agente por nota de memoria y un consolidador único por nota.
- **Por qué:** Pao pidió mantener limpio al agente principal y datos separados; un dueño por archivo evita ediciones simultáneas. Ver [[memoria/README]].

## 2026-10-14 · Citas con atribución segura y sin datos personales
- **Decisión:** citas solo de lo que sin duda dice Diego, marcadas "verificar contra el audio"; se omitieron pasajes familiares y se quitó una edad exacta de la cronología.
- **Por qué:** subtítulo automático sin turnos de habla; solo información profesional y pública (regla de la sesión).

## 2026-10-16 · Respuestas a prospectos asistidas, sin servicios externos
- **Decisión:** Pao quiere que Claude y el vault respondan a los prospectos de Campuslands sin más procesos. Se creó `prospectos/` con base de conocimiento y el comando `/responder-prospecto`. Claude redacta borradores; Pao revisa y envía.
- **Por qué:** la regla 7 exige confirmación para acciones salientes, y la base de datos de Diego tiene contradicciones (gratuito vs pago diferido) que un envío automático repetiría a prospectos reales. Ver [[prospectos/README]].
- **Descartado:** instalar las skills de Kapso (agente con envío automático) en el vault; quedan revisadas pero no instaladas.

## 2026-10-16 · Integración de fuentes oficiales de LinkedIn e higiene del vault
- **Decisión:** se integraron los 9 archivos oficiales del proyecto "CEO | LinkedIn Thought Leadership" en `linkedin/`, archivando sus originales intactos en `sources/linkedin/` y eliminando la carpeta duplicada `Linkedln/`. Se blindó `.gitignore` con `*.exe` y temporales. Se formalizó la Capa 2 con notas en `areas/` (`campuslands.md` y `second-brain.md`) y se completó la base de `meta/start-here.md`.
- **Por qué:** cumplía con la regla 1 de fuentes originales intactas y cerraba los pendientes de pilares y territorios de LinkedIn sin romper la arquitectura en 3 capas.
- **Alternativas descartadas:** mantener los archivos con sufijo ` (1)` sin archivar o dejar las áreas de vida vacías.

## 2026-10-20 · Conexión bidireccional integral del grafo y eliminación de huérfanos
- **Decisión:** conectar mediante wikilinks bidireccionales (`[[...]]`) las 337 publicaciones y 83 transcripciones de `diego_investigacion/`, los 77 archivos de `diego_instagram/`, y los 149 audios/videos del corpus de Campuslands, anclándolos a nodos centrales (`people/diego-tarazona`, `areas/campuslands`, `diego_investigacion/README`), nodos temáticos (`areas/ia-aplicada-y-futuro-del-trabajo`, `areas/movilidad-social`, `areas/cultura-camper`), directivos clave (`people/andres-lizarazo`, `people/sandra-charry`, `people/maria-camila-canas`) y aliados institucionales en `organizaciones/` (`fedesoft`, `zona-franca-santander`, `uniminuto`, `inexsu`, `grupo-bien-pensado`, `andi`, `procolombia`, `cenisoft`).
- **Por qué:** Obsidian Graph View mostraba un anillo masivo de nodos periféricos desconectados. La conexión bidireccional y los MOCs colapsan los huérfanos en cúmulos navegables y hacen que cada pieza de información sea localizable y utilizable en consultas, Dataview y grafos locales.
- **Alternativas descartadas:** dejar las publicaciones con rutas relativas de archivo Markdown (`../03_imagenes/`) que no crean aristas en el grafo de Obsidian.

