---
fecha: 2026-10-20
contexto: campuslands
tipo: prompt
---

# Prompt Maestro para Claude: Agente Extractor y Transcriptor de LinkedIn (Diego)

> **Instrucciones de uso:** 
> 1. Rellena el nombre completo o la URL del perfil de Diego en la sección **OBJETIVO PRINCIPAL**.
> 2. Asegúrate de tener tu sesión de LinkedIn abierta en el navegador.
> 3. Copia todo el bloque de abajo (o dile a Claude: *"Lee el archivo `PROMPT_CLAUDE_LINKEDIN_DIEGO.md` y ejecuta todas las instrucciones de principio a fin"*).

---

## INSTRUCCIONES PARA CLAUDE

Actúa como un **Agente Autónomo de Investigación, Extracción Multimedia y Análisis de Contenido**.
Tienes permiso total y explícito del usuario para:
1. Controlar e interactuar con el navegador donde ya está iniciada la sesión de LinkedIn.
2. Usar la terminal (PowerShell / Bash / Python) para crear carpetas, instalar paquetes, descargar videos/imágenes y ejecutar scripts de transcripción.

### OBJETIVO PRINCIPAL
- **Perfil objetivo:** `https://www.linkedin.com/in/diegotarazonapinzon/` (y página de empresa `https://co.linkedin.com/company/campuslands`)
- **Alcance:** Extraer toda la información de su perfil + sus últimas **25 publicaciones** completas (texto, imágenes, carruseles/PDFs y videos con sus respectivas transcripciones en 4 formatos) + generar un análisis maestro final.

---

### REGLAS DE AUTONOMÍA (OBLIGATORIAS)
1. **Cero interrupciones:** NO te detengas a pedir confirmación después de cada paso o publicación. Ejecuta el flujo completo de forma autónoma hasta terminar las publicaciones asignadas.
2. **Navegación segura (Simulación Humana):** Haz pausas naturales de 2 a 4 segundos entre clics y desplazamientos (scroll) para proteger la cuenta de LinkedIn.
3. **Persistencia inmediata en disco:** Nunca acumules la información en tu ventana de contexto. Apenas proceses una publicación, guárdala en su archivo correspondiente y actualiza `indice_progreso.md`.
4. **Resiliencia ante errores:** Si un método de descarga de video falla, aplica inmediatamente el método alternativo indicado abajo sin detener el flujo.

---

### FLUJO DE TRABAJO PASO A PASO

#### FASE 1: Preparación del Entorno Local
1. En el directorio de trabajo actual, crea la siguiente estructura de carpetas:
   ```text
   ./diego_investigacion/
   ├── 01_perfil_general.md
   ├── 02_publicaciones/
   ├── 03_imagenes/
   ├── 04_videos_y_audios/
   ├── 05_transcripciones/
   ├── 06_analisis_maestro_diego.md
   ├── indice_progreso.md
   └── scripts/
       └── procesar_video.py
   ```
2. Verifica en la terminal que estén disponibles `python`, `ffmpeg`, `yt-dlp` y `faster-whisper`. Si falta alguno, instálalo automáticamente ejecutando:
   ```powershell
   pip install yt-dlp faster-whisper requests
   ```
3. Crea el script auxiliar `./diego_investigacion/scripts/procesar_video.py` con el siguiente código para automatizar la extracción de audio, fotogramas y transcripción con marcas de tiempo:
   ```python
   import sys
   import os
   import subprocess
   from faster_whisper import WhisperModel

   def procesar(video_path, post_id, output_dir):
       audio_path = os.path.join(output_dir, f"{post_id}.wav")
       frames_dir = os.path.join(output_dir, f"{post_id}_frames")
       os.makedirs(frames_dir, exist_ok=True)

       # 1. Extraer audio en WAV 16kHz para Whisper
       subprocess.run([
           "ffmpeg", "-y", "-i", video_path,
           "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", audio_path
       ], check=True)

       # 2. Extraer 1 fotograma cada 5 segundos para análisis visual
       subprocess.run([
           "ffmpeg", "-y", "-i", video_path,
           "-vf", "fps=1/5", os.path.join(frames_dir, "frame_%03d.jpg")
       ], check=True)

       # 3. Transcribir con Faster-Whisper
       model = WhisperModel("small", device="cpu", compute_type="int8")
       segments, info = model.transcribe(audio_path, language="es", beam_size=5)

       raw_out = os.path.join(output_dir, f"{post_id}_raw_transcript.txt")
       with open(raw_out, "w", encoding="utf-8") as f:
           for seg in segments:
               mins, secs = divmod(int(seg.start), 60)
               end_m, end_s = divmod(int(seg.end), 60)
               f.write(f"[{mins:02d}:{secs:02d} - {end_m:02d}:{end_s:02d}] {seg.text.strip()}\n")

       print(f"OK: Transcripción guardada en {raw_out} y fotogramas en {frames_dir}")

   if __name__ == "__main__":
       procesar(sys.argv[1], sys.argv[2], sys.argv[3])
   ```

---

#### FASE 2: Extracción del Perfil General
1. Navega al perfil de LinkedIn de Diego.
2. Extrae toda la información visible (desplegando "ver más" en cada sección) y guárdala estructurada en `./diego_investigacion/01_perfil_general.md`:
   - Nombre completo, Titular (Headline), Ubicación, Número de seguidores y contactos.
   - Sección **"Acerca de" (About)** íntegra.
   - Sección **"Destacados" (Featured)** con enlaces y descripciones.
   - **Experiencia laboral** completa (fechas, cargos, empresas, descripciones).
   - **Educación, Licencias/Certificaciones y Aptitudes**.

---

#### FASE 3: Extracción de Publicaciones, Imágenes y Videos
1. Navega a la sección de publicaciones de Diego: `.../recent-activity/all/`.
2. Recorre las publicaciones en orden cronológico inverso. Asigna a cada una un identificador secuencial: `post_001`, `post_002`, etc.
3. En cada publicación:
   - Haz clic en `...más` para desplegar el texto completo.
   - Extrae el texto íntegro, fecha relativa, cantidad de reacciones, comentarios y compartidos.
   - Guarda los datos base en `./diego_investigacion/02_publicaciones/post_XXX.md`.

   #### 🖼️ SI LA PUBLICACIÓN TIENE IMÁGENES, INFOGRAFÍAS O CARRUSEL (PDF):
   1. Captura o descarga la imagen en `./diego_investigacion/03_imagenes/post_XXX_img_01.png`.
   2. Si es un documento/carrusel de varias páginas, haz clic en la flecha siguiente para capturar cada diapositiva (`img_01`, `img_02`, etc.).
   3. Analiza visualmente cada imagen y añade en `./diego_investigacion/02_publicaciones/post_XXX.md`:
      - **Texto Extraído (OCR completo):** Todo el texto escrito dentro de la imagen o diapositivas.
      - **Análisis Visual:** Descripción de diagramas, tablas, diseño visual, colores y qué idea transmite la imagen en conjunto con el post.

   #### 🎬 SI LA PUBLICACIÓN TIENE UN VIDEO:
   1. **Extracción del archivo de video (ejecuta en este orden de prioridad):**
      - **Opción A (Directa desde el DOM - Más rápida y sin bloqueo):** Asegúrate de que el video se haya cargado haciendo clic en reproducir/pausa, abre la consola o ejecuta JavaScript en la página para extraer el atributo `src` de la etiqueta `<video>`:
        ```javascript
        Array.from(document.querySelectorAll('video')).map(v => v.src || v.currentSrc)
        ```
        Descarga esa URL directamente a `./diego_investigacion/04_videos_y_audios/post_XXX.mp4` usando `curl -L "<URL_MP4>" -o "./diego_investigacion/04_videos_y_audios/post_XXX.mp4"` o `requests` en Python.
      - **Opción B (Vía enlace del post con yt-dlp):** Haz clic en los tres puntos `(...)` del post -> *"Copiar enlace a la publicación"* y ejecuta:
        ```powershell
        yt-dlp "<URL_DEL_POST>" -o "./diego_investigacion/04_videos_y_audios/post_XXX.%(ext)s"
        ```
   2. **Ejecución del procesamiento:**
      Ejecuta el script de Python creado en la Fase 1:
      ```powershell
      python ./diego_investigacion/scripts/procesar_video.py "./diego_investigacion/04_videos_y_audios/post_XXX.mp4" "post_XXX" "./diego_investigacion/04_videos_y_audios"
      ```
   3. **Inspección de fotogramas + texto y creación de las 4 Transcripciones:**
      Lee el archivo `post_XXX_raw_transcript.txt` generado y revisa los fotogramas en `post_XXX_frames/`. Luego crea el archivo `./diego_investigacion/05_transcripciones/post_XXX_transcripcion.md` con **estas 4 secciones obligatorias**:
      - **Forma 1: Transcripción Literal con Marcas de Tiempo (`[MM:SS - MM:SS]`)**: Todo lo que dice palabra por palabra con su tiempo exacto.
      - **Forma 2: Transcripción Limpia y Editorial**: El discurso redactado de forma fluida, sin muletillas ni repeticiones, dividido por párrafos temáticos y listo para leerse como un artículo.
      - **Forma 3: Guion Audio-Visual Sincronizado (Tabla)**: Una tabla con columnas `Tiempo | Lo que dice Diego (Audio) | Lo que aparece en pantalla (Visual / Texto en video / Gestos)`.
      - **Forma 4: Extracción Estratégica y Resumen**:
        - **Gancho (Hook):** Cómo capta la atención en los primeros 5 segundos.
        - **Ideas principales (Bullet points):** Resumen ejecutivo de las enseñanzas del video.
        - **Llamado a la acción (CTA):** Qué pide al final del video.
        - **Frases textuales destacables (Quotes):** Las mejores citas del video.

4. **Registro de progreso:** Al terminar cada publicación, añade una fila en `./diego_investigacion/indice_progreso.md` indicando: `ID | Fecha | Tipo (Texto/Imagen/Video) | Resumen de 1 línea | Estado (Completado)`.

---

#### FASE 4: Síntesis y Análisis Maestro de Diego (`06_analisis_maestro_diego.md`)
Una vez procesadas todas las publicaciones e información del perfil, analiza todo el material recopilado y genera `./diego_investigacion/06_analisis_maestro_diego.md` incluyendo:
1. **Quién es Diego y cuál es su propuesta de valor:** Resumen de su trayectoria, autoridad y posicionamiento.
2. **Pilares de Contenido y Temas Recurrentes:** De qué habla más y qué problemas resuelve.
3. **Anatomía de sus Publicaciones Escritas:** Cómo estructura sus posts (tipos de ganchos, longitud, formato de listas, tono de voz, cierres).
4. **Anatomía de sus Imágenes y Carruseles:** Qué tipo de recursos visuales utiliza y cómo sintetiza información compleja.
5. **Anatomía de sus Videos:** Ritmo, estilo de habla, estructura de sus guiones, edición visual y cómo retiene la atención.
6. **Base de Conocimiento Extraída:** Compendio de las mejores herramientas, metodologías, frameworks o consejos técnicos compartidos por Diego en todas sus publicaciones.
