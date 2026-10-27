---
fecha: 2026-10-20
contexto: campuslands
tipo: prompt
---

# Prompt Maestro: Extracción Forense, Estilometría y Análisis de Reels de Instagram (Diego Tarazona & Campuslands)

> **Instrucciones de uso:** 
> 1. Asegúrate de tener tu sesión de Instagram abierta en el navegador.
> 2. Verifica las URLs o perfiles objetivos (Diego Tarazona y Campuslands).
> 3. Ejecuta este prompt diciéndole al agente: *"Lee `PROMPT_CLAUDE_INSTAGRAM_DIEGO.md` y ejecuta todas las instrucciones de principio a fin de forma autónoma. Extrae cada Reel, transcríbelo íntegro, extrae los captions, comentarios, respuestas literales de Diego y analiza su evolución y patrones de escritura a profundidad."*

---

## MISIÓN Y ROL DEL AGENTE

Actúa como un **Agente Autónomo Especialista en OSINT, Ingeniería Inversa de Contenido, Lingüística Forense y Análisis de Video Vertical**.
Tu objetivo no es solo raspar publicaciones superficiales, sino **diseccionar quirúrgicamente el ADN de comunicación de Diego Tarazona** a través de:
1. **La transcripción palabra por palabra de sus Reels** con marcas de tiempo y análisis visual de texto en pantalla.
2. **El análisis de sus patrones de escritura** en las descripciones (captions).
3. **La extracción de comentarios y sus respuestas literales** para mapear cómo interactúa 1-a-1 con su comunidad.
4. **La reconstrucción de su línea de tiempo** para entender cómo evolucionó su contenido, su producción y su crecimiento de audiencia.

---

### ESTRUCTURA DE ALMACENAMIENTO LOCAL

Crea y mantén la siguiente estructura en `./diego_instagram/`:
```text
diego_instagram/
├── 01_perfil_diego.md             # Bio, métricas, enlaces e historias destacadas
├── 01b_perfil_campuslands.md      # Perfil corporativo de Campuslands
├── 01c_ecosistema_fuentes_ext.md  # Enlaces bio, podcasts completos, notas de prensa
├── 02_publicaciones/              # Fichas técnicas completas por post
│   ├── diego/                     # Posts y Reels de Diego
│   ├── campuslands/               # Posts y Reels de Campuslands
│   └── etiquetados_y_collabs/     # Entrevistas y colaboraciones con terceros
├── 03_carruseles_e_imagenes/      # Slides descargadas con OCR
├── 04_reels_y_videos/             # Archivos MP4 verticales y fotogramas
├── 05_transcripciones/            # Transcripciones completas en 4 capas
├── 06_analisis_maestro_instagram.md # Diagnóstico estratégico y evolución temporal
├── 06b_manual_de_estilo_y_patrones_diego.md # ADN de escritura, habla y respuestas
├── indice_progreso.md             # Registro de avance de cada publicación
└── scripts/
    └── procesar_reel.py           # Extractor de audio WAV 16kHz, frames y Faster-Whisper
```

---

### FLUJO DE TRABAJO QUIRÚRGICO PASO A PASO

#### FASE 1: Entorno de Audio, Video e Inteligencia Artificial
1. Comprueba e instala en la terminal:
   ```powershell
   pip install yt-dlp faster-whisper requests
   ```
2. Asegúrate de que `ffmpeg` esté en el PATH.
3. Configura `./diego_instagram/scripts/procesar_reel.py` para:
   - Extraer audio en formato WAV monocanal a 16.000 Hz.
   - Extraer fotogramas (1 cada 2 segundos) para inspeccionar los títulos animados y expresiones.
   - Transcribir con `faster-whisper` (`model="small"` en CPU o GPU).

---

#### FASE 2: Extracción de Perfiles, Destacadas y Enlaces Externos
1. **Perfil de Diego:**
   - Extraer biografía, categoría, seguidores, enlaces y fecha de captura en `01_perfil_diego.md`.
   - Inspeccionar y desglosar cada una de sus **Historias Destacadas (Highlights)**: títulos, temas que abordan y qué rol cumplen en su marca personal.
2. **Perfil de Campuslands:**
   - Extraer enfoque institucional, vida estudiantil y llamados a la acción en `01b_perfil_campuslands.md`.
3. **Triangulación Externa:**
   - Seguir los enlaces del link-in-bio (sitios web, convocatorias, artículos) y documentarlos en `01c_ecosistema_fuentes_ext.md`.
   - Si un Reel menciona una entrevista o podcast largo, rastrear el video completo en YouTube o la web.

---

#### FASE 3: Extracción Exhaustiva Publicación por Publicación

Por cada publicación (recorriendo cronológicamente el feed y la pestaña de Reels):

1. **Si es un REEL (Video Vertical 9:16):**
   - **Descarga:** Descargar el video `.mp4` en `./diego_instagram/04_reels_y_videos/post_XXX.mp4` vía `yt-dlp` o URL directa.
   - **Procesamiento:** Ejecutar `procesar_reel.py`.
   - **Transcripción en 4 Capas (`./diego_instagram/05_transcripciones/post_XXX_transcripcion.md`):**
     * **Capa 1 (Literal con Timestamps):** Minuto y segundo exacto de cada frase: `[00:00 - 00:03] ...`.
     * **Capa 2 (Guion Limpio y Editorial):** Texto fluido sin titubeos, listo para ser leído como un artículo.
     * **Capa 3 (Tabla Audio-Visual Sincronizada):**
       `Tiempo | Lo que dice Diego (Voz) | Lo que aparece en pantalla (Títulos animados, gestos, b-rolls)`
     * **Capa 4 (Desglose de Retención):**
       - **Gancho inicial (0-3 seg):** Primeras palabras y recurso visual para detener el scroll.
       - **Retención intermedia:** Cómo mantiene el ritmo al segundo 15-30.
       - **Llamado a la acción (CTA):** Frase de cierre (comentar, compartir, seguir).
       - **Citas célebres:** Frases contundentes destacables.

2. **Análisis de Cómo Escribe (Caption / Descripción del Post):**
   Dentro de la ficha `./diego_instagram/02_publicaciones/<categoria>/post_XXX.md`, registrar:
   - **Texto íntegro del copy.**
   - **Análisis de la primera línea (Hook escrito):** ¿Es pregunta, afirmación chocante o anécdota?
   - **Estructura del texto:** Longitud de oraciones, espaciados, uso de viñetas o listas.
   - **Vocabulario y tono:** Palabras técnicas vs. lenguaje coloquial, nivel de cercanía o autoridad.
   - **Hashtags y menciones.**

3. **Extracción de Comentarios y Respuestas de Diego (Voz 1-a-1):**
   - Extraer los 5 a 10 comentarios con más interacción o relevancia temática.
   - **Extraer obligatoriamente todas las respuestas dadas por Diego:**
     - Analizar cómo debate, cómo agradece y cómo argumenta con usuarios reales.
     - Registrar si usa humor, datos duros de Campuslands o respuestas directas al grano.

4. **Si es un Carrusel o Foto:**
   - Descargar cada una de las diapositivas en `./diego_instagram/03_carruseles_e_imagenes/post_XXX_slide_01.jpg`, etc.
   - Hacer OCR completo de cada lámina y registrar la narrativa slide a slide.

5. **Actualizar `indice_progreso.md`** al terminar cada post.

---

#### FASE 4: Reconstrucción de la Línea de Tiempo y Evolución del Contenido

En `./diego_instagram/06_analisis_maestro_instagram.md`, documentar la trayectoria histórica de crecimiento:
1. **Etapas de Maduración:**
   - **Fase Inicial:** Cómo eran sus primeros videos (formato, temas, calidad técnica, soltura al hablar).
   - **Fase de Transición:** Cuándo empezó a estandarizar subtítulos dinámicos, edición vertical y ritmo ágil.
   - **Fase de Consolidación:** Contenido actual de alta tracción, autoridad en IA y educación.
2. **Métricas y Factores de Viralidad:**
   - Qué temáticas o formatos dispararon el crecimiento de reproducciones y seguidores.
   - Diferencias de rendimiento entre videos espontáneos vs. videos producidos en estudio/oficina.

---

#### FASE 5: Elaboración del Manual de Estilo y Patrones de Diego (`06b_manual_de_estilo_y_patrones_diego.md`)

Generar el manual de ingeniería inversa lingüística para que el Second Brain pueda escribir o redactar guiones idénticos a Diego:
1. **ADN de Habla (Voz Oral):**
   - Muletillas reales y pausas enfáticas.
   - Cadencia de voz y velocidad promedio de palabras por minuto.
   - Gestualidad típica frente a la cámara.
2. **ADN de Escritura (Voz Escrita):**
   - Plantillas de apertura (fórmulas de ganchos escritas que más repite).
   - Estructura de desarrollo (cómo argumenta sus ideas en 3-4 párrafos).
   - Fórmulas de cierre.
3. **Diccionario de Marca Personal:**
   - Términos recurrentes (conceptos tecnológicos, pedagógicos y de negocio).
   - Metáforas favoritas.
4. **Protocolo de Interacción en Comentarios:**
   - Reglas y ejemplos reales de cómo responder preguntas, objeciones y halagos tal como él lo hace.
