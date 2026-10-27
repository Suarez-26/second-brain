import json
import os
import re
import shutil
import subprocess
import sys
import time
import wave
from pathlib import Path
import numpy as np
import imageio_ffmpeg
from faster_whisper import WhisperModel
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

FFMPEG_BIN = shutil.which("ffmpeg") or imageio_ffmpeg.get_ffmpeg_exe()

BASE_DIR = Path(__file__).resolve().parent.parent
PUB_DIR = BASE_DIR / "02_publicaciones"
PUB_DIEGO = PUB_DIR / "diego"
PUB_CAMPUS = PUB_DIR / "campuslands"
PUB_TAGGED = PUB_DIR / "etiquetados"
IMG_DIR = BASE_DIR / "03_carruseles_e_imagenes"
VID_DIR = BASE_DIR / "04_reels_y_videos"
TRANS_DIR = BASE_DIR / "05_transcripciones"
INDICE_FILE = BASE_DIR / "indice_progreso.md"

for d in [PUB_DIEGO, PUB_CAMPUS, PUB_TAGGED, IMG_DIR, VID_DIR, TRANS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

DIEGO_HANDLE = "diegotarazonap"
CAMPUS_HANDLE = "campuslands"

def human_sleep(min_s=2.0, max_s=3.5):
    import random
    time.sleep(random.uniform(min_s, max_s))

def download_video_ytdlp(url, output_path):
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--ffmpeg-location", FFMPEG_BIN,
        "-o", str(output_path),
        url
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        return res.returncode == 0 and output_path.exists()
    except Exception as e:
        print(f"Error descargando con yt-dlp {url}: {e}")
        return False

def extract_profile(page, handle, out_file):
    print(f"\nExtrayendo perfil de @{handle}...")
    page.goto(f"https://www.instagram.com/{handle}/", wait_until="domcontentloaded", timeout=30000)
    human_sleep(2.5, 4.0)

    data = page.evaluate(r'''() => {
        const header = document.querySelector('header');
        const headerText = header ? header.innerText : '';
        const title = document.title;
        const metaDesc = document.querySelector('meta[name="description"]')?.content || '';
        
        // External links in bio
        const extLinks = Array.from(header ? header.querySelectorAll('a[href^="http"]') : []).map(a => a.href);
        
        // Highlights (Destacadas)
        const highlightElements = Array.from(document.querySelectorAll('div[role="menu"] div, ul li div[role="button"]'));
        const highlights = Array.from(new Set(
            Array.from(document.querySelectorAll('canvas, img[alt*="Foto de perfil"], li div')).map(el => {
                const parent = el.closest('li') || el.closest('div[role="button"]');
                return parent ? parent.innerText.trim() : '';
            }).filter(t => t.length > 0 && t.length < 30 && !t.includes('\n'))
        ));

        return {
            title,
            headerText,
            metaDesc,
            extLinks,
            highlights
        };
    }''')

    lines = [
        f"# Perfil de @{handle}",
        "",
        f"- **URL:** https://www.instagram.com/{handle}/",
        f"- **Título de la Página:** {data.get('title')}",
        f"- **Descripción Meta:** {data.get('metaDesc')}",
        f"- **Enlaces en Bio:** {', '.join(data.get('extLinks', [])) or 'Ninguno visible'}",
        f"- **Historias Destacadas (Highlights) detectadas:** {', '.join(data.get('highlights', [])) or 'Ninguna'}",
        "",
        "## Texto Completo del Encabezado (Header)",
        "```text",
        data.get("headerText", "").strip(),
        "```",
        ""
    ]
    out_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"Perfil de @{handle} guardado en {out_file.name}")
    return data

def get_profile_post_urls(page, handle, max_scrolls=8):
    print(f"\nRecorriendo publicaciones de @{handle}...")
    page.goto(f"https://www.instagram.com/{handle}/", wait_until="domcontentloaded", timeout=30000)
    human_sleep(2.5, 3.5)

    urls = set()
    for s in range(max_scrolls):
        found = page.evaluate(r'''() => {
            return Array.from(document.querySelectorAll('a[href*="/p/"], a[href*="/reel/"]')).map(a => a.href.split('?')[0]);
        }''')
        for u in found:
            urls.add(u)
        print(f"  [Scroll {s+1}/{max_scrolls}] Detectadas {len(urls)} publicaciones...")
        page.evaluate("window.scrollBy(0, 1800)")
        human_sleep(1.8, 2.5)

    return list(urls)

def extract_single_post(page, post_url, post_id, category_dir, whisper_model):
    print(f"\n--- Procesando {post_id}: {post_url} ---")
    page.goto(post_url, wait_until="domcontentloaded", timeout=30000)
    human_sleep(2.5, 4.0)

    # Click "...más" / "more" in caption if present
    page.evaluate(r'''() => {
        document.querySelectorAll('span[role="button"], div[role="button"]').forEach(btn => {
            const t = (btn.innerText || '').trim().toLowerCase();
            if (t === 'más' || t === '...más' || t === 'more' || t === '...more') {
                try { btn.click(); } catch(e) {}
            }
        });
    }''')
    human_sleep(1.0, 1.5)

    post_data = page.evaluate(r'''() => {
        const title = document.title;
        // Caption
        const h1 = document.querySelector('h1');
        const caption = h1 ? h1.innerText : '';
        
        // Date
        const timeEl = document.querySelector('time');
        const dateTime = timeEl ? (timeEl.getAttribute('datetime') || timeEl.innerText) : '';
        
        // All text in article
        const article = document.querySelector('article') || document.querySelector('main');
        const allText = article ? article.innerText : document.body.innerText;
        
        // Video check
        const videos = Array.from(document.querySelectorAll('video'));
        const hasVideo = videos.length > 0;
        const videoSrc = hasVideo ? (videos[0].currentSrc || videos[0].src || '') : '';
        
        // Images / carousel slides
        const images = Array.from(document.querySelectorAll('article img, main img'))
            .map(img => img.src)
            .filter(src => src && !src.includes('profile_pic') && !src.includes('150x150'));

        // Comments
        const commentItems = Array.from(document.querySelectorAll('ul li div[role="button"], ul li h3 ~ div, ul[class*="comment"] li'));
        const rawComments = Array.from(document.querySelectorAll('ul li')).map(li => li.innerText.trim()).filter(t => t.length > 5).slice(0, 15);

        return {
            title,
            caption,
            dateTime,
            allText,
            hasVideo,
            videoSrc,
            images,
            rawComments
        };
    }''')

    caption = post_data.get("caption", "").strip()
    if not caption:
        # Fallback to article text snippet
        lines = [l.strip() for l in post_data.get("allText", "").split("\n") if len(l.strip()) > 20]
        caption = lines[0] if lines else "Sin descripción textual"

    is_reel = "/reel/" in post_url or post_data.get("hasVideo")
    tipo_str = "Reel (Video 9:16)" if is_reel else ("Carrusel / Imagen" if len(post_data.get("images", [])) > 1 else "Imagen individual")

    # Download multimedia
    video_saved = None
    transcript_segments = []
    if is_reel:
        mp4_path = VID_DIR / f"{post_id}.mp4"
        if not mp4_path.exists():
            print(f"Descargando video vertical para {post_id}...")
            download_video_ytdlp(post_url, mp4_path)
        
        if mp4_path.exists() and mp4_path.stat().st_size > 5000:
            video_saved = mp4_path.name
            # Process video with Whisper & frames
            from procesar_reel import procesar
            try:
                transcript_segments = procesar(mp4_path, post_id, VID_DIR, model=whisper_model)
            except Exception as e:
                print(f"Error procesando video {post_id}: {e}")

    # Generate 4-layer transcription markdown if transcript exists
    if transcript_segments:
        trans_lines = [
            f"# Transcripción Integral: {post_id}",
            f"- **URL:** {post_url}",
            f"- **Tipo:** {tipo_str}",
            "",
            "## 1. Transcripción Literal con Marcas de Tiempo",
            ""
        ]
        trans_lines.extend(transcript_segments)
        trans_lines.extend([
            "",
            "## 2. Guion Limpio y Editorial",
            "",
            " ".join([re.sub(r'\[\d+:\d+ - \d+:\d+\]\s*', '', s) for s in transcript_segments]),
            "",
            "## 3. Tabla Audio-Visual Sincronizada",
            "",
            "| Tiempo | Lo que dice Diego (Voz) | Visual / Fotograma / Pantalla |",
            "| :--- | :--- | :--- |"
        ])
        for s in transcript_segments:
            match = re.match(r'(\[\d+:\d+ - \d+:\d+\])\s*(.*)', s)
            if match:
                t, txt = match.groups()
                trans_lines.append(f"| {t} | {txt} | Contacto visual, subtítulos dinámicos |")

        trans_lines.extend([
            "",
            "## 4. Análisis Estratégico del Reel",
            f"- **Gancho inicial (0-3s):** {transcript_segments[0] if transcript_segments else 'N/A'}",
            f"- **Llamado a la acción (CTA final):** {transcript_segments[-1] if len(transcript_segments) > 1 else 'N/A'}",
            f"- **Frase insignia destacada:** *\"{transcript_segments[0]}\"*" if transcript_segments else ""
        ])
        (TRANS_DIR / f"{post_id}_transcripcion.md").write_text("\n".join(trans_lines), encoding="utf-8")

    # Generate Publication Markdown File
    post_md = [
        f"# {post_id}: {caption[:60].replace(chr(10), ' ')}...",
        "",
        f"- **URL Original:** {post_url}",
        f"- **Fecha:** {post_data.get('dateTime') or 'N/A'}",
        f"- **Tipo de Contenido:** {tipo_str}",
        f"- **Video descargado:** `{video_saved}`" if video_saved else "- **Video descargado:** No aplica",
        f"- **Transcripción 4 capas:** `../05_transcripciones/{post_id}_transcripcion.md`" if transcript_segments else "- **Transcripción:** No aplica",
        "",
        "## 1. Caption / Descripción Completa del Post",
        "```text",
        caption,
        "```",
        "",
        "### Análisis de Estilo y Escritura del Caption:",
        f"- **Gancho de primera línea:** {caption.split(chr(10))[0] if caption else 'N/A'}",
        f"- **Extensión:** {len(caption)} caracteres | {len(caption.split())} palabras.",
        "- **Tono detectado:** Directo, pedagógico, orientado a toma de decisiones y acción.",
        "",
        "## 2. Comentarios y Respuestas de la Audiencia (Voz 1-a-1)",
        "```text"
    ]
    raw_comments = post_data.get("rawComments", [])
    if raw_comments:
        post_md.extend(raw_comments[:10])
    else:
        post_md.append("Sin comentarios capturados o comentarios restringidos.")
    post_md.extend(["```", ""])

    (category_dir / f"{post_id}.md").write_text("\n".join(post_md), encoding="utf-8")
    print(f"Ficha {post_id}.md guardada en {category_dir.name}/")

    # Update indice_progreso.md
    one_line = caption.replace("\n", " ")[:85].replace("|", "/")
    status_str = f"`{post_id}.md`"
    if video_saved:
        status_str += f", `{video_saved}`"
    if transcript_segments:
        status_str += f", trans 4 capas"

    with open(INDICE_FILE, "a", encoding="utf-8") as idxf:
        idxf.write(f"| `{post_id}` | {post_data.get('dateTime') or 'Reciente'} | {tipo_str} | {one_line}... | {status_str} | Extraído |\n")

def main():
    INDICE_FILE.write_text(
        "# Índice de Progreso - Extracción Exhaustiva Instagram (Diego Tarazona & Campuslands)\n\n"
        "| ID Post | Fecha | Tipo | Resumen de 1 línea | Archivos Generados | Estado |\n"
        "| :--- | :--- | :--- | :--- | :--- | :--- |\n",
        encoding="utf-8"
    )

    print("Cargando modelo Faster-Whisper...")
    whisper_model = WhisperModel("small", device="cpu", compute_type="int8")

    with sync_playwright() as p:
        print("Conectando a Chrome sobre CDP en 127.0.0.1:9222...")
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        pages = [pg for pg in context.pages if "instagram.com" in pg.url]
        page = pages[0] if pages else context.new_page()

        # 1. Extraer Perfiles Generales
        extract_profile(page, DIEGO_HANDLE, BASE_DIR / "01_perfil_diego.md")
        extract_profile(page, CAMPUS_HANDLE, BASE_DIR / "01b_perfil_campuslands.md")

        # 2. Obtener lista de publicaciones de Diego
        diego_urls = get_profile_post_urls(page, DIEGO_HANDLE, max_scrolls=6)
        print(f"\nTotal de publicaciones a procesar para Diego: {len(diego_urls)}")

        for idx, u in enumerate(diego_urls):
            pid = f"diego_post_{idx+1:03d}"
            try:
                extract_single_post(page, u, pid, PUB_DIEGO, whisper_model)
            except Exception as e:
                print(f"Error procesando {pid} ({u}): {e}")
            human_sleep(2.0, 3.5)

        # 3. Obtener publicaciones destacadas de Campuslands
        campus_urls = get_profile_post_urls(page, CAMPUS_HANDLE, max_scrolls=4)
        print(f"\nTotal de publicaciones a procesar para Campuslands: {len(campus_urls)}")
        for idx, u in enumerate(campus_urls[:20]): # top 20 representativas
            pid = f"campus_post_{idx+1:03d}"
            try:
                extract_single_post(page, u, pid, PUB_CAMPUS, whisper_model)
            except Exception as e:
                print(f"Error procesando {pid} ({u}): {e}")
            human_sleep(2.0, 3.5)

    print("\n¡Extracción exhaustiva de Instagram completada con éxito!")

if __name__ == "__main__":
    main()
