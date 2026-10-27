import json
import re
from pathlib import Path

def parse_json3(json3_path):
    try:
        data = json.loads(json3_path.read_text(encoding='utf-8'))
        events = data.get('events', [])
        lines = []
        for ev in events:
            t_ms = ev.get('tStartMs', 0)
            mins = t_ms // 60000
            secs = (t_ms % 60000) // 1000
            segs = ev.get('segs', [])
            txt = ''.join([s.get('utf8', '') for s in segs]).strip()
            if txt and txt != '\n':
                lines.append(f"[{mins:02d}:{secs:02d}] {txt}")
        return '\n'.join(lines)
    except Exception as e:
        return f"Error leyendo subtítulos: {e}"

def main():
    meta_p = Path('investigacion/campuslands/scripts/filtered_full_metadata.json')
    subs_dir = Path('investigacion/campuslands/scripts/subs')
    corpus_dir = Path('investigacion/campuslands/corpus_youtube_podcasts')
    corpus_dir.mkdir(parents=True, exist_ok=True)

    items = json.loads(meta_p.read_text(encoding='utf-8'))
    created = 0
    catalog_rows = []

    for vid, info in items.items():
        title = info.get('title', 'Sin título')
        clean_title = re.sub(r'[\/*?:\'"<>|]', '', title)[:50].strip().replace(' ', '-')
        date = info.get('upload_date') or '2026-00-00'
        if len(date) == 8 and date.isdigit():
            date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
        
        filename = f"{date}-{vid}-{clean_title}.md"
        out_file = corpus_dir / filename
        
        # Buscar archivo de subtítulo
        sub_file = None
        for cand in [subs_dir / f"{vid}.es.json3", subs_dir / f"{vid}.es-orig.json3", subs_dir / f"{vid}.en.json3"]:
            if cand.exists() and cand.stat().st_size > 100:
                sub_file = cand
                break
                
        has_transcript = False
        transcript_text = "Subtítulos no disponibles o video sin diálogo procesable."
        if sub_file:
            transcript_text = parse_json3(sub_file)
            has_transcript = len(transcript_text) > 100
            
        md = [
            "---",
            f'fecha: "{date}"',
            "contexto: campuslands",
            "tipo: youtube-transcripcion",
            f'video_id: "{vid}"',
            f'canal: "{info.get("channel", "Desconocido")}"',
            f'duracion: "{info.get("duration_string", "N/A")}"',
            f'vistas: {info.get("view_count", 0)}',
            f'url: "https://www.youtube.com/watch?v={vid}"',
            "---",
            "",
            f"# {title}",
            "",
            f"- **Canal:** {info.get('channel', 'Desconocido')}",
            f"- **Fecha de subida:** {date}",
            f"- **Duración:** {info.get('duration_string', 'N/A')}",
            f"- **Vistas:** {info.get('view_count', 0)}",
            f"- **URL:** https://www.youtube.com/watch?v={vid}",
            "",
            "## Descripción del Video",
            "```text",
            info.get('description', 'Sin descripción').strip(),
            "```",
            "",
            "## Transcripción de Audio / Subtítulos",
            "",
            transcript_text,
            ""
        ]
        out_file.write_text('\n'.join(md), encoding='utf-8')
        created += 1

        catalog_rows.append({
            "fecha": date,
            "id": vid,
            "title": title.replace("|", "/"),
            "channel": info.get("channel", "N/A").replace("|", "/"),
            "duration": info.get("duration_string", "N/A"),
            "views": info.get("view_count", 0),
            "file": filename,
            "trans": "Sí" if has_transcript else "No"
        })

    print(f"Archivos creados en corpus_youtube_podcasts: {created}")

    # Escribir catálogo maestro
    cat_md = [
        "---",
        "fecha: 2026-10-20",
        "contexto: campuslands",
        "tipo: catalogo-multimedia",
        "---",
        "",
        "# Catálogo Maestro de Videos y Transcripciones de YouTube (Campuslands & Diego Tarazona)",
        "",
        f"Total de videos indexados: **{len(catalog_rows)}**",
        "",
        "| Fecha | Video / Título | Canal | Duración | Vistas | Transcripción | Archivo en Vault |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
    ]
    catalog_rows.sort(key=lambda x: x["fecha"], reverse=True)
    for r in catalog_rows:
        cat_md.append(f"| {r['fecha']} | [{r['title'][:55]}](https://www.youtube.com/watch?v={r['id']}) | {r['channel'][:25]} | {r['duration']} | {r['views']} | {r['trans']} | `[[corpus_youtube_podcasts/{r['file']}]]` |")

    (Path("investigacion/campuslands/fuentes/catalogo_youtube_podcasts.md")).write_text('\n'.join(cat_md), encoding='utf-8')
    print("Catálogo catalogo_youtube_podcasts.md guardado.")

if __name__ == "__main__":
    main()
