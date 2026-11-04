---
fecha: 2026-10-14
tipo: contexto-operativo
---

# Registro de decisiones

Formato: fecha · decisión · por qué · alternativas descartadas.

## 2026-11-04 · Eliminación de rutas de archivos en WhatsApp y corrección de feedback de publicaciones
- **Decisión:** 
  1. Supresión total de rutas de archivo (`journal/...`, `sources/...`, `.md`), etiquetas de minutaje y avisos de open-loops en las respuestas de WhatsApp para el administrador (`kapso_whatsapp_bot.py`).
  2. Clasificación estricta de retroalimentación conversacional (ej: "esta publicación ya la hice", "dame otra idea", "cambia el enfoque"): clasificado como `consulta_general` con listas de tareas y hechos vacías, impidiendo la creación de tareas no deseadas en el journal.
  3. Instrucción de originalidad para redes sociales: los posts previos del Second Brain se etiquetan como antecedentes históricos para no repetirlos, y ante pedidos de alternativas o publicaciones previas se entrega de inmediato una nueva propuesta con ángulo fresco y hook diferente.
- **Por qué:** Pao solicitó expresamente no recibir rutas técnicas ni avisos de propuestas en su chat, corregir el error donde decir que ya había publicado se guardaba como tarea, y asegurar que el agente ofrezca nuevas ideas de post en lugar de repetir publicaciones viejas o quedarse en preguntas pasivas.
- **Alternativas descartadas:** dejar las rutas como pie de página; requerir confirmación antes de redactar otra propuesta de post.

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


## 2026-10-27 · Un solo escritor del vault y aprobación humana para la Capa 1
- **Decisión:** toda la automatización escribe con `automation/vault_io.py` (bloqueo entre procesos, escritura atómica, log y commit por lote). `meta/` solo cambia con aprobación explícita: el LLM crea propuestas en `state.db` y Pao responde `Aceptar N`. Los pendientes llevan ID estable `[OL-nnn]`.
- **Por qué:** tres procesos reescribían `open-loops.md` sin coordinarse, y el bot cerraba pendientes por coincidencia de palabras. Además había 11 días sin commit, así que la reversión con git que se autorizó el 13-oct no existía en la práctica.
- **Descartado:** mantener el cierre automático con un umbral más alto (sigue siendo un falso positivo silencioso en la Capa 1).

## 2026-10-27 · Terceros solo con borrador aprobado y sin suplantar a Diego
- **Decisión:** los dos bots responden a terceros solo con un borrador aprobado (`Enviar N`); el modo auto queda desactivado. Los borradores van firmados por `FIRMA_EXTERNOS` ("Equipo Campuslands") y no niegan ser una IA. El webhook de Kapso exige firma HMAC.
- **Por qué:** regla 7. El bot de Kapso respondía solo, como "Diego Tarazona", a cualquier número, y el webhook aceptaba payloads sin autenticar, incluido un remitente admin falsificado.
- **Pendiente:** si Diego autoriza hablar en su nombre (OL-016), basta con cambiar `FIRMA_EXTERNOS`.

## 2026-10-27 · Búsqueda local sin embeddings externos
- **Decisión:** índice FTS5 (BM25, sin distinguir acentos, con filtros de capa, contexto y calidad), expuesto por MCP. No hay embeddings.
- **Por qué:** los embeddings con una API externa sacarían el contenido del vault del equipo, y uno local pide dependencias pesadas. Con ~800 notas, BM25 con filtros resuelve la mayoría de las búsquedas. Se puede revisar si el vault crece.
- **Descartado:** revertir el enlazado automático del 20-oct: los enlaces por mención son útiles; el corpus queda marcado `crudo`.

## 2026-10-28 · Ingesta de fuentes canónicas de Campuslands, Cultura Hunter, Prexxa y Formación de Startups / CEO
- **Decisión:** Ingestar íntegramente los documentos fuentes en `sources/` organizados por dominio: `sources/campuslands/` (`asi-somos-los-hunters-v10.md` y `contexto-campuslands-sas-bic.md`), `sources/management/` (`las-5-disfunciones-de-un-equipo-prexxa.md`), y `sources/formacion/` (`escuela-de-startups-platzi.md` y `curso-de-ceo-platzi.md`). Sincronizar la Capa 2 actualizando `areas/campuslands.md` con las 7 líneas de negocio, sedes territoriales y estándares TIC; crear la nota de área `areas/cultura-hunter.md` para sintetizar el marco de desempeño de 24 días y rituales; dar de alta en `organizaciones/` a `prexxa.md`, `platzi.md` y `unidrogas.md` actualizando `organizaciones/README.md`; y robustecer `people/paola-granados.md` como líder de Talento y Cultura Hunter.
- **Por qué:** Cumple con la regla de tres capas (fuente íntegra en Capa 3, síntesis operativa en Capa 2), evita duplicación o dispersión de la verdad oficial de Campuslands, y provee el marco estructurado de cultura, liderazgo y escalamiento que Pao gestiona directamente en la organización.
- **Alternativas descartadas:** Dejar los documentos como notas sueltas en la raíz o en `inbox/` sin procesar ni conectar al grafo de Obsidian.

## 2026-10-28 · Integración del Brandbook Oficial de Campuslands 2023
- **Decisión:** Ingestar el Brandbook oficial completo en `sources/campuslands/brandbook-oficial-2023.md` con su especificación técnica completa (paleta cromática HEX/CMYK, roles tipográficos Poppins/Roboto Mono/Nutmeg, concepto del casco de astronauta, slogan `GOFORIT!`, submarcas coworking/radio, mascota oficial 3D, y merchandising de Campers y Hunters). Vincular bidireccionalmente con `sources/campuslands/contexto-campuslands-sas-bic.md`, `areas/campuslands.md`, `areas/cultura-camper.md` y `areas/cultura-hunter.md`.
- **Por qué:** Resuelve directamente el pendiente `[COMPLETAR]` sobre el brandbook oficial y garantiza que cualquier material visual, presentación, publicación o respuesta generada por el Second Brain respete los lineamientos cromáticos y de identidad corporativa.

## 2026-10-28 · Estructura canónica obligatoria para generación de contenido en redes sociales
- **Decisión:** Formalizar la Regla 10 en `CLAUDE.md` y actualizar `automation/audio_processor.py` en `responder_como_diego` para que al solicitar ideas, borradores o guiones de redes sociales (LinkedIn, TikTok, Instagram, Reels), el sistema NUNCA devuelva resúmenes planos de 1 párrafo. Debe estructurar obligatoriamente según el ADN y publicaciones previas de Diego y Campuslands documentadas en `diego_investigacion/06_analisis_maestro_diego.md` y `linkedin/03_Sistema_Editorial_y_Pilares_de_Thought_Leadership.md`.
- **Por qué:** La captura de WhatsApp demostró que el bot recortaba las ideas a párrafos cortos de respuesta rápida perdiendo todo el impacto, ritmo visual, tensión narrativa y llamados de acción propios de la voz de Diego.

## 2026-10-28 · Humanización de respuestas, postura real de Campuslands y protocolo de contención emocional
- **Decisión:** Ajustar utomation/audio_processor.py para erradicar respuestas robóticas ('No tengo esa información en mis registros actuales') ante saludos o preguntas familiares, respondiendo con calidez y cercanía natural; anclar la respuesta ante el desinterés ('¿Qué haces cuando alguien no quiere Campus?') en la postura oficial del Manifiesto Hunter ('Esto no es para todos, y está bien; no rogamos ni convencemos a nadie, nos enfocamos en quienes tienen hambre de aprender'); e implementar un protocolo prioritario de seguridad y contención emocional con líneas oficiales de ayuda en Colombia ante palabras de autolesión o crisis ('que me mate'), impidiendo que el motor devuelva fragmentos aleatorios del corpus corporativo.
- **Por qué:** Una captura de WhatsApp de un número externo evidenció respuestas frías ('mis registros actuales'), paternalistas y, críticamente, una respuesta corporativa sobre Tibú ante una frase de riesgo personal ('que me mate').


## 2026-10-28 · Respuestas siempre simples, concisas y naturales en WhatsApp (eliminación de descontextualización)
- **Decisión:** 
  1. Simplificar de forma estricta las instrucciones de `audio_processor.py`: fijar longitud de 1 a 3 oraciones cortas (o viñetas directas si se piden listas como sedes), prohibir preámbulos vacíos, anécdotas no pedidas y cierres repetitivos.
  2. Corregir el disparador de saludos: ante mensajes como "Hola" o cortesías simples, responder únicamente con un saludo cálido y breve de 1 oración ("¡Hola Pao! ¿Cómo vas? ¿En qué te ayudo hoy?"), prohibiendo terminantemente discursos no solicitados sobre familia, salud o retos de Campuslands.
  3. Prevenir contaminación contextual en FTS: filtrar palabras vacías (stop words) y omitir búsquedas ruidosas (`OR`) en `index.db` cuando la consulta no tiene términos sustantivos, evitando inyectar transcripciones masivas o ajenas en saludos o instrucciones.
  4. Agilizar mensajes de texto en `kapso_whatsapp_bot.py`: detectar saludos simples de inmediato para responder sin demoras innecesarias.
- **Por qué:** El bot se salía de contexto al recibir un simple "Hola" o una instrucción, devolviendo párrafos enteros sobre su familia, salud o transcripciones de podcasts de YouTube debido a ejemplos sobrecargados en el prompt y recuperación indiscriminada de FTS.

## 2026-11-04 · Recepción y análisis visual multimodal de imágenes en WhatsApp
- **Decisión:** Implementar soporte nativo para imágenes (`image`) en `kapso_whatsapp_bot.py` y `audio_processor.py`:
  1. Descarga automática de imágenes a `sources/imagenes/` respetando formatos (`.jpg`, `.png`, `.webp`, `.gif`).
  2. Análisis visual con Gemini (`analizar_imagen_con_ia`): extracción de OCR, descripción concisa del contenido, clasificación del tipo de imagen (documento, pizarra, comprobante, captura, foto) y extracción de compromisos o tareas terminadas hacia el sistema de propuestas de `pendientes.py`.
  3. Registro estructurado en `journal/AAAA-MM-DD.md` para administradores (`registrar_imagen_en_journal`) y en `inbox/whatsapp/otros/` para terceros.
  4. Generación de respuesta con visión directa en `responder_como_diego` enviando la imagen inline vía REST a Gemini (`inline_data`), respondiendo de forma simple, concisa y natural en 1 a 3 oraciones.
  5. Optimización de la cadena de modelos en `GEMINI_MODELOS` priorizando `gemini-3-flash-preview` y `gemini-3.5-flash` para menor latencia.
- **Por qué:** Pao requería que el bot pudiera recibir y comprender tanto notas de voz como imágenes (fotos de tableros, capturas, comprobantes o fotos de eventos) para integrarlas automáticamente al Second Brain sin perder la naturalidad en la respuesta.

## 2026-11-04 · Eliminación del encabezado/firma "🎙️ Diego Tarazona:" en respuestas de WhatsApp
- **Decisión:** Remover el prefijo `🎙️ *Diego Tarazona:*\n\n` de todas las respuestas generadas por `kapso_whatsapp_bot.py` (`procesar_mensaje_texto`, `procesar_audio`, `procesar_imagen`).
- **Por qué:** La firma o banner generaba ruido visual y hacía que los mensajes se sintieran artificiales o robóticos en lugar de una conversación fluida, directa y personal en WhatsApp.

## 2026-11-04 · Corrección en la descarga de imágenes y medios de Kapso
- **Decisión:** 
  1. Priorizar las URLs directas pre-firmadas proporcionadas por Kapso (`kapso_info.get("media_url")`, `(kapso_info.get("media_data") or {}).get("url")`, `img_info.get("link")`) por encima del `id` numérico de Meta.
  2. Implementar `_hacer_descarga` para gestionar las cabeceras HTTP adecuadamente: enviar `X-API-Key` solo a `api.kapso.ai`, enviar `Authorization: Bearer` si es `lookaside.fbsbx.com`, y descargar URLs de ActiveStorage/S3 sin cabeceras que provoquen rechazos.
- **Por qué:** La imagen enviada por Pao arrojaba el mensaje de error de descarga porque el bot seleccionó el `id` de Meta, solicitó la URL de lookaside de Facebook y luego intentó descargarla enviando la cabecera `X-API-Key` de Kapso a los servidores de Facebook, lo que devolvía un error `401 Unauthorized`. Al priorizar el enlace directo de Kapso, la imagen se descarga en menos de 1 segundo de forma limpia.
