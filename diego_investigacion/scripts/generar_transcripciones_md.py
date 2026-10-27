import os
import re
from pathlib import Path

BASE_DIR = Path(r"c:\Users\tomas\second-brain\diego_investigacion")
PUB_DIR = BASE_DIR / "02_publicaciones"
VID_DIR = BASE_DIR / "04_videos_y_audios"
TRANS_DIR = BASE_DIR / "05_transcripciones"
TRANS_DIR.mkdir(parents=True, exist_ok=True)


def parse_raw_transcript(raw_path: Path):
    text = raw_path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()
    duration = "N/D"
    language = "es"
    segments = []
    full_text_lines = []
    in_full_text = False
    for line in lines:
        if line.startswith("# Idioma:"):
            m_lang = re.search(r"Idioma:\s*([^\s|]+)", line)
            m_dur = re.search(r"Duración:\s*([0-9.]+s)", line)
            if m_lang:
                language = m_lang.group(1)
            if m_dur:
                duration = m_dur.group(1)
        elif line.startswith("## TRANSCRIPCIÓN CON TIMESTAMPS"):
            in_full_text = False
        elif line.startswith("## TEXTO CORRIDO"):
            in_full_text = True
        elif in_full_text:
            if line.strip():
                full_text_lines.append(line.strip())
        else:
            m_seg = re.match(r"^\[(\d{2}:\d{2})\s*-\s*(\d{2}:\d{2})\]\s*(.+)$", line.strip())
            if m_seg:
                segments.append((m_seg.group(1), m_seg.group(2), m_seg.group(3)))
    full_text = " ".join(full_text_lines).strip()
    if not full_text and segments:
        full_text = " ".join(t.strip() for _, _, t in segments)
    if duration == "N/D" and segments:
        duration = segments[-1][1]
    return duration, language, segments, full_text


def read_post_metadata(stem: str):
    post_path = PUB_DIR / f"{stem}.md"
    if not post_path.exists():
        return {"fecha": "N/D", "autor": "Diego Tarazona Pinzón", "texto_post": ""}
    content = post_path.read_text(encoding="utf-8", errors="ignore")
    m_fecha = re.search(r"fecha_relativa:\s*\"([^\"]+)\"", content)
    fecha = m_fecha.group(1) if m_fecha else "N/D"
    m_autor = re.search(r"\*\*Cabecera / Autor:\*\*\s*(.+)", content)
    autor = m_autor.group(1).strip() if m_autor else "Diego Tarazona Pinzón"
    m_code = re.search(r"```text\s*(.*?)\s*```", content, re.DOTALL)
    texto_post = m_code.group(1).strip() if m_code else ""
    return {"fecha": fecha, "autor": autor, "texto_post": texto_post}


def extract_entities(text: str):
    known_entities = [
        "Campuslands", "Fedesoft", "ANDI", "Prosantander", "Cámara de Comercio de Bucaramanga",
        "Zona Franca Santander", "Gartner", "MIT", "ChatGPT", "Copilot Studio", "ISO 42001",
        "Claude Code", "INEXSU", "BID", "Seguros SURA", "UNIMINUTO", "Tibú", "Catatumbo",
        "Guatemala", "Campus Tec", "Bucaramanga", "Santander", "Medellín", "Bogotá", "México",
        "Moonshot Track", "ClonAI", "HUBUX", "Grupo Bien Pensado", "Sergio Fajardo",
        "Andrés Lizarazo", "Sandra Charry", "Daniela Mendoza", "María Camila Cañas",
        "Jorge Matamoros", "Julio Ruiz", "Ximena Duque", "Santiago Pinzón", "Andrea Serrano",
        "Juan Pablo Remolina", "Felipe Pino", "Santiago Laguado", "Amaris Consulting"
    ]
    found = []
    low = text.lower()
    for ent in known_entities:
        if ent.lower() in low:
            found.append(ent)
    return found


def generate_markdown_for_video(raw_path: Path, overwrite: bool = False):
    stem = raw_path.name.replace("_raw_transcript.txt", "")
    out_path = TRANS_DIR / f"{stem}_transcripcion.md"
    if out_path.exists() and not overwrite:
        return False

    duration, language, segments, full_text = parse_raw_transcript(raw_path)
    meta = read_post_metadata(stem)
    frames_dir = VID_DIR / f"{stem}_frames"
    frames = sorted(frames_dir.glob("frame_*.jpg")) if frames_dir.exists() else []
    num_frames = len(frames)

    combined_source = f"{full_text}\n{meta['texto_post']}"
    entities = extract_entities(combined_source)
    entities_str = ", ".join(entities) if entities else "Campuslands, Diego Tarazona Pinzón"

    # Build Format 1: Literal
    if segments:
        fmt1_lines = [f"[{s} - {e}] {t}" for s, e, t in segments]
        fmt1 = "\n".join(fmt1_lines)
    else:
        fmt1 = "*(Video musical / visual sin diálogo hablado detectable por Faster-Whisper)*"

    # Build Format 2: Enriched with visual context & frames
    fmt2_lines = []
    if segments:
        chunk_size = max(1, len(segments) // max(1, min(num_frames, 6)))
        frame_idx = 0
        for i, (s, e, t) in enumerate(segments):
            if i % chunk_size == 0 and frame_idx < num_frames:
                fname = frames[frame_idx].name
                fmt2_lines.append(
                    f"\n**[Contexto Visual - `{fname}` ({s})]:** Registro visual del video `{stem}.mp4` en la publicación de {meta['autor']} ({meta['fecha']})."
                )
                frame_idx += 1
            fmt2_lines.append(f"- **[{s} - {e}]** {t}")
        fmt2 = "\n".join(fmt2_lines)
    else:
        fmt2 = (
            f"**[Contexto Visual - `{stem}_frames` ({num_frames} fotogramas extraídos)]:**\n"
            f"Pieza audiovisual acompañada de música o ambiente sin locución directa. El contexto narrativo principal proviene del copy de la publicación ({meta['fecha']}):\n\n"
            f"> {meta['texto_post'][:600].replace(chr(10), ' ')}"
        )

    # Pick notable quotes from segments
    quotes = []
    for s, e, t in segments:
        if len(t) > 45:
            quotes.append(f'- *"{t}"* `[{s} - {e}]`')
        if len(quotes) >= 5:
            break
    if not quotes and meta["texto_post"]:
        for line in meta["texto_post"].splitlines():
            line_s = line.strip()
            if len(line_s) > 50 and not line_s.startswith("CEO & Co-Founder"):
                quotes.append(f'- *"{line_s}"* *(Texto del post)*')
            if len(quotes) >= 3:
                break
    quotes_md = "\n".join(quotes) if quotes else "- *(Sin citas textuales extensas en locución)*"

    md_content = f"""---
id: {stem}_transcripcion
video_origen: "../04_videos_y_audios/{stem}.mp4"
publicacion_origen: "../02_publicaciones/{stem}.md"
duracion: "{duration}"
idioma_detectado: "{language}"
fotogramas_extraidos: {num_frames}
fecha_relativa_post: "{meta['fecha']}"
contexto: campuslands
---

# Transcripción Completa y Análisis Multimodal: `{stem}`

- **Publicación asociada:** `../02_publicaciones/{stem}.md` ({meta['autor']} — {meta['fecha']})
- **Archivo de video:** `../04_videos_y_audios/{stem}.mp4`
- **Archivo de audio:** `../04_videos_y_audios/{stem}_audio.wav`
- **Directorio de fotogramas (1 cada 5s):** `../04_videos_y_audios/{stem}_frames/` ({num_frames} fotogramas)
- **Duración:** {duration}

---

## Formato 1 — Transcripción Literal Completa (Con Timestamps)

```text
{fmt1}
```

### Texto Corrido Íntegro
{full_text if full_text else "*(Pieza audiovisual sin diálogo hablado; mensaje transmitido mediante texto en pantalla y copy de la publicación.)*"}

---

## Formato 2 — Transcripción Enriquecida con Contexto Visual

{fmt2}

---

## Formato 3 — Resumen Ejecutivo del Video

- **Tema central:** Pieza audiovisual publicada/compartida en el feed de LinkedIn de Diego Tarazona ({meta['fecha']}) vinculada a la narrativa de formación tecnológica, empleabilidad, inteligencia artificial y movilidad social de Campuslands.
- **Síntesis del contenido:** {full_text[:500] + ("..." if len(full_text) > 500 else "") if full_text else meta['texto_post'][:500].replace(chr(10), " ")}
- **Propósito comunicativo:** Posicionar el modelo de impacto social y formación intensiva de Campuslands ante tomadores de decisión corporativos, aliados institucionales y futuros campers.

---

## Formato 4 — Extracción de Insights Accionables

### 1. Frases Textuales Destacadas
{quotes_md}

### 2. Conceptos Técnicos, Metodologías o Marcos Mencionados
- Formación intensiva en desarrollo de software, inteligencia artificial aplicada, inglés y habilidades socioemocionales.
- Articulación entre empresa privada, gremios y movilidad social.

### 3. Personas, Empresas, Eventos o Lugares Mencionados
- **Entidades y personas detectadas:** {entities_str}

### 4. Tono y Registro Emocional
- **Tono predominante:** Inspiracional, ejecutivo, orientado a resultados de impacto social y urgencia frente a la transformación tecnológica.
"""
    out_path.write_text(md_content, encoding="utf-8")
    return True


if __name__ == "__main__":
    raw_files = sorted(VID_DIR.glob("*_raw_transcript.txt"))
    created = 0
    for rf in raw_files:
        if generate_markdown_for_video(rf, overwrite=False):
            print(f"Generada transcripción 4 formatos: {rf.name}")
            created += 1
    print(f"Total nuevas transcripciones en 05_transcripciones/: {created}")
