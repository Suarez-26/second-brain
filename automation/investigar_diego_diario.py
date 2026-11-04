"""Investigación y extracción diaria autónoma 360° sobre Diego Tarazona y Campuslands.

Canales monitoreados en automático (sin requerir intervención manual):
1. LINKEDIN EN TIEMPO REAL:
   - Perfil personal de Diego Tarazona (https://co.linkedin.com/in/diegotarazonapinzon)
   - Página oficial de Campuslands (https://co.linkedin.com/company/campuslands)
   - Extrae: fecha exacta ISO-8601, texto íntegro, imágenes, videos, reacciones y COMENTARIOS de la audiencia.
   - Guarda fichas en diego_investigacion/02_publicaciones/ y en investigacion/diego-tarazona/fuentes/redes-sociales.md.
2. INSTAGRAM EN TIEMPO REAL (@diegotarazonap y @campuslands):
   - Extrae publicaciones y Reels recientes vía Chrome Headless + metadatos OpenGraph.
   - Si es un Reel/Video, lo descarga con yt-dlp y lo envía a Gemini Multimodal (video/mp4) para ver y escuchar el video, transcribiendo con timestamps [mm:ss] lo que dice Diego.
   - Guarda fichas en diego_instagram/02_publicaciones/ y en fuentes/video-podcast.md.
3. YOUTUBE, PODCASTS, CHARLAS Y REDES DE VIDEO (TikTok / Facebook / X):
   - Busca videos y entrevistas con yt-dlp, extrae subtítulos con marcas de tiempo [mm:ss] (o analiza el audio/video con Gemini Multimodal) y extrae citas textuales y posturas de Diego.
4. PRENSA, PERIÓDICOS, REVISTAS Y RADIOS:
   - Monitorea medios nacionales y regionales (Vanguardia, Caracol Radio, Portafolio, El País, La Opinión, Metropolitano).
   - Extrae declaraciones de Diego e hitos corporativos.
5. CONSOLIDACIÓN EN EL SECOND BRAIN:
   - Todo se escribe vía vault_io (con bloqueo, registro en meta/log.md y commit en Git).
   - Actualiza memoria/temas-y-posturas.md y memoria/campuslands-hechos.md.
   - Reindexa el buscador FTS5 (indice.py) para que el bot de WhatsApp responda al instante con los datos del día.
"""

from __future__ import annotations

import base64
import datetime as dt
import html
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import requests

AUTOMATION_DIR = Path(__file__).resolve().parent
RAIZ = AUTOMATION_DIR.parent
sys.path.insert(0, str(AUTOMATION_DIR))

import audio_processor  # noqa: E402
import indice  # noqa: E402
import vault_io  # noqa: E402

HISTORIAL_FILE = AUTOMATION_DIR / ".historico_investigacion_diego.json"
CORPUS_DIR = RAIZ / "investigacion" / "diego-tarazona" / "corpus"
CORPUS_DIR.mkdir(parents=True, exist_ok=True)

FB_BOT_UA = "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)"
CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]


def encontrar_chrome() -> str | None:
    for c in CHROME_CANDIDATES:
        if os.path.exists(c):
            return c
    return None


def cargar_historial() -> set[str]:
    if HISTORIAL_FILE.exists():
        try:
            data = json.loads(HISTORIAL_FILE.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return set(data)
        except Exception:
            pass
    return set()


def guardar_historial(items: set[str]) -> None:
    try:
        HISTORIAL_FILE.write_text(json.dumps(sorted(list(items)), indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception as e:
        print(f"[WARN] Error guardando historial: {e}", flush=True)


def limpiar_html(texto_html: str) -> str:
    t = re.sub(r"(?is)<script.*?</script>", " ", texto_html)
    t = re.sub(r"(?is)<style.*?</style>", " ", t)
    t = re.sub(r"(?is)<head.*?</head>", " ", t)
    t = re.sub(r"(?is)<!--.*?-->", " ", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def limpiar_vtt_a_timestamps(vtt_content: str) -> str:
    lines = []
    for block in re.split(r"\n\s*\n", vtt_content):
        m = re.search(r"(\d{2}:\d{2}):\d{2}\.\d{3}\s*-->", block)
        if m:
            ts = m.group(1)
            clean_text = re.sub(r"<[^>]+>", "", block)
            clean_text = re.sub(r"\d{2}:\d{2}:\d{2}\.\d{3}.*", "", clean_text)
            text_lines = [l.strip() for l in clean_text.splitlines() if l.strip()]
            if text_lines:
                last_line = text_lines[-1]
                if not lines or lines[-1][1] != last_line:
                    lines.append((ts, last_line))

    grouped: dict[str, list[str]] = {}
    for ts, text in lines:
        grouped.setdefault(ts, []).append(text)

    return "\n".join(f"[{ts}] " + " ".join(txts) for ts, txts in grouped.items())


# --- Utilidad Multimodal Gemini (Ver y escuchar videos MP4) --------------------------

def analizar_video_mp4_con_gemini(mp4_path: Path, contexto_titulo: str) -> dict[str, Any] | None:
    """Envía un archivo MP4 a Gemini Multimodal para transcribir y analizar lo que dice Diego."""
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key or not mp4_path.exists():
        return None
    size_mb = mp4_path.stat().st_size / (1024 * 1024)
    if size_mb > 18:
        print(f"[INFO] Video {mp4_path.name} ({size_mb:.1f} MB) excede límite inline.", flush=True)
        return None

    b64_video = base64.b64encode(mp4_path.read_bytes()).decode("ascii")
    prompt = (
        f"Analiza este video/reel ({contexto_titulo}). "
        "1. Transcribe con marcas de tiempo [mm:ss] lo que se dice en el video (especialmente si habla Diego Tarazona). "
        "2. Describe brevemente qué se ve visualmente en pantalla. "
        "3. Extrae las citas textuales más importantes y las posturas o ideas clave. "
        "Responde en JSON con claves: "
        '{"habla_diego": true/false, "descripcion_visual": "...", '
        '"transcripcion_completa": "[00:00] ...", '
        '"citas_textuales": ["[mm:ss] cita..."], '
        '"resumen_lo_que_dice": "...", "posturas_clave": ["..."]}'
    )
    payload = {
        "contents": [{
            "parts": [
                {"inlineData": {"mimeType": "video/mp4", "data": b64_video}},
                {"text": prompt}
            ]
        }],
        "generationConfig": {"temperature": 0.1, "responseMimeType": "application/json"}
    }
    headers = {"x-goog-api-key": key, "Content-Type": "application/json"}
    for modelo in audio_processor.GEMINI_MODELOS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"
        try:
            r = requests.post(url, json=payload, headers=headers, timeout=50)
            if r.status_code == 200:
                txt = r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
                return json.loads(txt)
        except Exception as e:
            print(f"[WARN] Gemini multimodal ({modelo}): {e}", flush=True)
    return None


# --- Canal 1: LinkedIn en Tiempo Real (Diego + Campuslands + Comentarios) ------------

def extraer_post_linkedin_detalle(post_url: str) -> dict[str, Any] | None:
    """Obtiene el JSON-LD completo de una publicación de LinkedIn (fecha, texto, autor, comentarios, multimedia)."""
    try:
        r = requests.get(post_url, headers={"User-Agent": FB_BOT_UA}, timeout=15)
        if r.status_code != 200:
            return None
        ld_blocks = re.findall(r'(?is)<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', r.text)
        for b in ld_blocks:
            try:
                d = json.loads(b.strip())
                if d.get("@type") in ("SocialMediaPosting", "DiscussionForumPosting", "Article", "VideoObject"):
                    author_obj = d.get("author") or {}
                    autor = author_obj.get("name", "Diego Tarazona / Campuslands") if isinstance(author_obj, dict) else "LinkedIn"
                    fecha_iso = d.get("datePublished", "")
                    texto = d.get("articleBody") or d.get("text") or d.get("description") or ""
                    headline = d.get("headline") or ""

                    # Extraer comentarios
                    comentarios = []
                    for c in d.get("comment") or []:
                        if isinstance(c, dict):
                            c_aut = (c.get("author") or {}).get("name", "Usuario")
                            c_txt = c.get("text", "")
                            c_date = c.get("datePublished", "")[:10]
                            if c_txt:
                                comentarios.append(f"[{c_date}] {c_aut}: \"{c_txt}\"")

                    # Extraer likes
                    likes = 0
                    stats = d.get("interactionStatistic") or []
                    if isinstance(stats, dict):
                        stats = [stats]
                    for st in stats:
                        if "LikeAction" in str(st.get("interactionType", "")):
                            likes = st.get("userInteractionCount", 0)

                    # Extraer imágenes y video
                    imgs = []
                    img_field = d.get("image")
                    if isinstance(img_field, list):
                        imgs = [x.get("url") for x in img_field if isinstance(x, dict) and x.get("url")]
                    elif isinstance(img_field, dict) and img_field.get("url"):
                        imgs = [img_field["url"]]

                    video_url = None
                    vid_field = d.get("video") or d.get("sharedContent")
                    if isinstance(vid_field, dict):
                        video_url = vid_field.get("contentUrl") or vid_field.get("embedUrl")

                    if texto:
                        return {
                            "url": d.get("@id") or post_url,
                            "autor": autor,
                            "fecha_iso": fecha_iso,
                            "fecha_corta": fecha_iso[:10] if fecha_iso else dt.date.today().isoformat(),
                            "titulo": headline,
                            "texto": texto.strip(),
                            "likes": likes,
                            "comentarios": comentarios,
                            "imagenes": imgs,
                            "video_url": video_url,
                        }
            except Exception:
                pass
    except Exception as e:
        print(f"[WARN] Error leyendo post LinkedIn {post_url[:60]}: {e}", flush=True)
    return None


def rastrear_linkedin_vivo(historial: set[str]) -> list[dict[str, Any]]:
    """Extrae las últimas publicaciones de Diego Tarazona y Campuslands en LinkedIn sin requerir login."""
    nuevos_posts = []
    urls_candidatas = []

    for origen, url_perfil in [
        ("Diego Tarazona", "https://co.linkedin.com/in/diegotarazonapinzon"),
        ("Campuslands", "https://co.linkedin.com/company/campuslands"),
    ]:
        print(f"Consultando LinkedIn en tiempo real ({origen}): {url_perfil}...", flush=True)
        try:
            r = requests.get(url_perfil, headers={"User-Agent": FB_BOT_UA}, timeout=15)
            if r.status_code == 200:
                encontradas = list(dict.fromkeys(
                    re.findall(r'https://[a-z]+\.linkedin\.com/posts/[^"\'\s?<>]+', r.text)
                ))
                # Priorizar posts de diegotarazonapinzon y campuslands
                propias = [u for u in encontradas if "diegotarazonapinzon" in u or "campuslands" in u]
                otras = [u for u in encontradas if u not in propias][:4]
                for u in propias[:8] + otras:
                    if u not in urls_candidatas and u not in historial:
                        urls_candidatas.append(u)
        except Exception as e:
            print(f"[WARN] Error consultando perfil LinkedIn {origen}: {e}", flush=True)

    print(f"Publicaciones nuevas de LinkedIn detectadas para extraer: {len(urls_candidatas)}", flush=True)
    for u in urls_candidatas:
        historial.add(u)
        detalle = extraer_post_linkedin_detalle(u)
        if not detalle:
            continue
        print(f"  [OK LinkedIn] {detalle['fecha_corta']} | {detalle['autor']}: {detalle['texto'][:65].replace(chr(10), ' ')}...", flush=True)

        # Analizar con Gemini qué plantea Diego / Campuslands y si hay comentarios relevantes
        prompt = f"""Analiza esta publicación de LinkedIn y sus comentarios para el Second Brain de Diego Tarazona y Campuslands.

AUTOR: {detalle['autor']}
FECHA: {detalle['fecha_iso']}
TEXTO:
\"\"\"{detalle['texto'][:4000]}\"\"\"

COMENTARIOS DE LA AUDIENCIA:
{chr(10).join(detalle['comentarios']) if detalle['comentarios'] else 'Sin comentarios'}

Devuelve un JSON con:
- "resumen_ejecutivo": síntesis en 2-3 líneas de lo que dice o propone la publicación
- "citas_clave": hasta 2 frases textuales destacadas (<25 palabras)
- "postura_diego": si refleja una postura filosófica o estratégica de Diego sobre IA, educación, liderazgo o talento, descríbela en 1 línea; si no, null
- "analisis_comentarios": síntesis de qué opina o pregunta la gente en los comentarios (si hay comentarios)
"""
        resp_ia = audio_processor.llamar_gemini(prompt, json_mode=True, temperature=0.1)
        if resp_ia:
            try:
                detalle["analisis_ia"] = json.loads(resp_ia)
            except Exception:
                detalle["analisis_ia"] = {}
        else:
            detalle["analisis_ia"] = {}

        nuevos_posts.append(detalle)
        time.sleep(0.8)

    return nuevos_posts


# --- Canal 2: Instagram en Tiempo Real (@diegotarazonap y @campuslands + Reels) ------

def rastrear_instagram_vivo(historial: set[str]) -> list[dict[str, Any]]:
    """Extrae posts y Reels recientes de Instagram y analiza los videos con Gemini Multimodal."""
    chrome_exe = encontrar_chrome()
    if not chrome_exe:
        print("[WARN] No se encontró Chrome/Edge para listar perfiles de Instagram.", flush=True)
        return []

    urls_ig = []
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(
                executable_path=chrome_exe,
                headless=True,
                args=["--headless=new", "--disable-blink-features=AutomationControlled"]
            )
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                locale="es-CO"
            )
            page = context.new_page()
            for handle in ["diegotarazonap", "campuslands"]:
                url = f"https://www.instagram.com/{handle}/"
                print(f"Consultando Instagram en tiempo real (@{handle})...", flush=True)
                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=30000)
                    time.sleep(3.5)
                    links = page.evaluate("""
                    () => Array.from(document.querySelectorAll('a[href*="/p/"], a[href*="/reel/"]')).map(a => a.href)
                    """)
                    for l in links[:6]:
                        if l not in urls_ig and l not in historial:
                            urls_ig.append(l)
                except Exception as e:
                    print(f"[WARN] Error abriendo IG @{handle}: {e}", flush=True)
            browser.close()
    except Exception as e:
        print(f"[WARN] Playwright Instagram: {e}", flush=True)

    print(f"Publicaciones/Reels nuevos de Instagram para procesar: {len(urls_ig)}", flush=True)
    nuevos_ig = []

    for u in urls_ig:
        historial.add(u)
        try:
            r = requests.get(u, headers={"User-Agent": FB_BOT_UA}, timeout=12)
            if r.status_code != 200:
                continue
            title_m = re.search(r'<meta[^>]*property="og:title"[^>]*content="([^"]+)"', r.text)
            desc_m = re.search(r'<meta[^>]*property="og:description"[^>]*content="([^"]+)"', r.text)
            title = html.unescape(title_m.group(1)) if title_m else ""
            desc = html.unescape(desc_m.group(1)) if desc_m else ""
            if not title and not desc:
                continue

            es_reel = "/reel/" in u
            shortcode_m = re.search(r"/(?:p|reel)/([A-Za-z0-9_-]+)/", u)
            shortcode = shortcode_m.group(1) if shortcode_m else f"ig_{int(time.time())}"

            # Extraer fecha aproximada de og:description (ej: "on October 21, 2026:")
            fecha_m = re.search(r"on\s+([A-Za-z]+\s+\d{1,2},\s+\d{4}):", desc)
            fecha_str = fecha_m.group(1) if fecha_m else dt.date.today().isoformat()

            item_ig: dict[str, Any] = {
                "url": u,
                "shortcode": shortcode,
                "es_reel": es_reel,
                "fecha": fecha_str,
                "titulo": title,
                "descripcion": desc,
                "analisis_video": None,
            }
            print(f"  [OK Instagram] ({'REEL' if es_reel else 'POST'}) {shortcode} - {fecha_str}: {title[:65]}...", flush=True)

            # Si es un Reel, descargarlo con yt-dlp y analizar video+audio con Gemini Multimodal
            if es_reel:
                tmp_mp4 = Path(tempfile.gettempdir()) / f"ig_reel_{shortcode}.mp4"
                if tmp_mp4.exists():
                    tmp_mp4.unlink()
                cmd = [sys.executable, "-m", "yt_dlp", "-f", "mp4", "-o", str(tmp_mp4), u]
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=45)
                if res.returncode == 0 and tmp_mp4.exists():
                    print(f"    -> Analizando video y voz del Reel {shortcode} con Gemini Multimodal...", flush=True)
                    av = analizar_video_mp4_con_gemini(tmp_mp4, title)
                    if av:
                        item_ig["analisis_video"] = av
                        # Guardar transcripción en corpus/
                        if av.get("transcripcion_completa"):
                            (CORPUS_DIR / f"ig_reel_{shortcode}_transcripcion.txt").write_text(
                                str(av["transcripcion_completa"]), encoding="utf-8"
                            )
                    try:
                        tmp_mp4.unlink()
                    except Exception:
                        pass

            nuevos_ig.append(item_ig)
        except Exception as e:
            print(f"[WARN] Error procesando IG {u}: {e}", flush=True)

    return nuevos_ig


# --- Canal 3: YouTube, Podcasts y Conferencias ---------------------------------------

def buscar_videos_youtube(queries: list[str], max_por_query: int = 2) -> list[dict[str, Any]]:
    videos = []
    ids_vistos = set()

    for q in queries:
        print(f"Buscando en YouTube: '{q}'...", flush=True)
        cmd = [
            sys.executable, "-m", "yt_dlp",
            f"ytsearch{max_por_query}:{q}",
            "--dump-json",
            "--skip-download",
        ]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if res.returncode == 0 and res.stdout:
                for line in res.stdout.strip().splitlines():
                    if not line.startswith("{"):
                        continue
                    try:
                        info = json.loads(line)
                        vid_id = info.get("id")
                        if vid_id and vid_id not in ids_vistos:
                            ids_vistos.add(vid_id)
                            duration_s = info.get("duration") or 0
                            m, s = divmod(int(duration_s), 60)
                            videos.append({
                                "id": vid_id,
                                "titulo": info.get("title", ""),
                                "canal": info.get("uploader", "") or info.get("channel", ""),
                                "url": f"https://www.youtube.com/watch?v={vid_id}",
                                "duracion": f"{m:02d}:{s:02d}",
                                "fecha_pub": info.get("upload_date", ""),
                                "descripcion": info.get("description", "")[:1000],
                            })
                    except Exception:
                        pass
        except Exception as e:
            print(f"[WARN] Error yt-dlp YouTube: {e}", flush=True)
        time.sleep(0.8)

    return videos


def extraer_transcripcion_video(url: str, video_id: str) -> str:
    out_template = str(CORPUS_DIR / f"{video_id}.%(ext)s")
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--skip-download",
        "--write-auto-sub",
        "--sub-lang", "es",
        "--convert-subs", "vtt",
        "-o", out_template,
        url,
    ]
    try:
        subprocess.run(cmd, capture_output=True, text=True, timeout=25)
        vtt_file = CORPUS_DIR / f"{video_id}.es.vtt"
        if vtt_file.exists():
            vtt_content = vtt_file.read_text(encoding="utf-8", errors="replace")
            texto_limpio = limpiar_vtt_a_timestamps(vtt_content)
            txt_file = CORPUS_DIR / f"{video_id}_transcripcion.txt"
            txt_file.write_text(texto_limpio, encoding="utf-8")
            return texto_limpio
    except Exception as e:
        print(f"[WARN] Error extrayendo subtítulos de {url}: {e}", flush=True)
    return ""


def analizar_video_con_gemini(video_info: dict[str, Any], transcripcion: str) -> dict[str, Any] | None:
    prompt = f"""Eres el investigador principal del Second Brain analizando una pieza audiovisual de YouTube/Podcast.
Tu objetivo es analizar estrictamente LO QUE DICE DIEGO TARAZONA (CEO y cofundador de Campuslands).

DATOS DE LA PIEZA:
- Título: {video_info.get('titulo')}
- Canal/Medio: {video_info.get('canal')}
- Duración: {video_info.get('duracion')}
- URL: {video_info.get('url')}

TRANSCRIPCIÓN CON TIMESTAMPS:
\"\"\"{transcripcion[:10000]}\"\"\"

INSTRUCCIONES:
1. Verifica si Diego Tarazona habla en esta pieza o es el sujeto central.
2. Si NO aparece Diego ni Campuslands, responde: {{"relevante": false}}
3. Si ES relevante, extrae:
   - "relevante": true
   - "resumen_lo_que_dice": qué plantea Diego en 3-4 líneas
   - "citas_textuales": lista de citas textuales de Diego con su timestamp exacto (máximo 4 citas de <25 palabras)
   - "posturas_clave": lista de posturas de Diego sobre temas clave (IA, educación, talento, empresas)
   - "confianza": "alta"

Responde ÚNICAMENTE un objeto JSON válido."""

    resp = audio_processor.llamar_gemini(prompt, json_mode=True, temperature=0.1)
    if not resp:
        return None
    try:
        data = json.loads(resp)
        if data.get("relevante"):
            return data
    except Exception:
        pass
    return None


# --- Canal 4: Prensa, Radios y Periódicos -------------------------------------------

def buscar_bing_news(query: str) -> list[dict[str, str]]:
    q_encoded = urllib.parse.quote(query)
    url = f"https://www.bing.com/news/search?q={q_encoded}&format=rss"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    resultados = []
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code == 200:
            root = ET.fromstring(resp.content)
            for item in root.findall(".//item"):
                title_elem = item.find("title")
                link_elem = item.find("link")
                pubdate_elem = item.find("pubDate")

                title = title_elem.text.strip() if title_elem is not None and title_elem.text else ""
                raw_link = link_elem.text.strip() if link_elem is not None and link_elem.text else ""
                pubdate = pubdate_elem.text.strip() if pubdate_elem is not None and pubdate_elem.text else ""

                real_url = raw_link
                if "url=" in raw_link:
                    parsed = urllib.parse.urlparse(raw_link)
                    qs = urllib.parse.parse_qs(parsed.query)
                    real_url = qs.get("url", [raw_link])[0]

                if real_url and title:
                    resultados.append({
                        "titulo": title,
                        "url": real_url,
                        "fecha_pub": pubdate,
                    })
    except Exception as e:
        print(f"[WARN] Error consultando Bing News ({query}): {e}", flush=True)
    return resultados


def descargar_contenido_url(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        if resp.status_code == 200:
            return limpiar_html(resp.text)[:12000]
    except Exception:
        pass
    return ""


def analizar_noticia_con_gemini(item: dict[str, str], contenido: str) -> dict[str, Any] | None:
    prompt = f"""Eres un investigador analizando prensa y radio para el Second Brain de Campuslands.
El objetivo es extraer hechos verificables y citas textuales de Diego Tarazona (CEO de Campuslands).

DATOS DE LA FUENTE:
- Título: {item.get('titulo', '')}
- Fecha aproximada: {item.get('fecha_pub', '')}
- URL: {item.get('url', '')}

TEXTO DEL MEDIO:
\"\"\"{contenido[:7000]}\"\"\"

INSTRUCCIONES:
1. Determina si el texto realmente menciona a Diego Tarazona o Campuslands.
2. Si NO es relevante, responde: {{"relevante": false}}
3. Si ES relevante, extrae:
   - "relevante": true
   - "medio_nombre": nombre del medio (ej. Vanguardia, Caracol Radio, Portafolio)
   - "fecha_publicacion": fecha aproximada YYYY-MM-DD
   - "titular_limpio": titular del artículo
   - "hecho": qué declara o hace Diego / qué logró Campuslands (máximo 80 palabras)
   - "cita": cita textual exacta de Diego Tarazona si existe; si no, null
   - "confianza": "alta" o "media"
   - "tipo": "hecho" u "opinión"
   - "es_hito_corporativo": true si anuncia apertura de sede, expansión o alianza de alto impacto

Responde ÚNICAMENTE un objeto JSON válido."""

    resp = audio_processor.llamar_gemini(prompt, json_mode=True, temperature=0.1)
    if not resp:
        return None
    try:
        data = json.loads(resp)
        if data.get("relevante"):
            return data
    except Exception:
        pass
    return None


# --- Notificación WhatsApp ------------------------------------------------------------

def notificar_whatsapp(mensaje: str) -> None:
    admin_num = os.getenv("ADMIN_PHONE_NUMBER", "").split(",")[0].strip()
    clean_admin = re.sub(r"\D", "", admin_num)
    phone_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
    api_key = os.getenv("KAPSO_API_KEY", "")
    base_url = os.getenv("KAPSO_API_BASE_URL", "https://api.kapso.ai").rstrip("/")

    if not (clean_admin and phone_id and api_key):
        return

    url = f"{base_url}/meta/whatsapp/v24.0/{phone_id}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": clean_admin,
        "type": "text",
        "text": {"body": mensaje[:4000]}
    }
    try:
        requests.post(url, json=payload, headers={"X-API-Key": api_key}, timeout=15)
    except Exception:
        pass


# --- Orquestador Principal 360° -------------------------------------------------------

def ejecutar_investigacion_multicanal() -> dict[str, Any]:
    print("=" * 70, flush=True)
    print(f"[{dt.datetime.now():%Y-%m-%d %H:%M}] INVESTIGACIÓN 360°: DIEGO TARAZONA & CAMPUSLANDS", flush=True)
    print("=" * 70, flush=True)

    historial = cargar_historial()
    novedades_linkedin = []
    novedades_instagram = []
    novedades_video = []
    novedades_prensa = []
    hitos_corporativos = []
    nuevas_posturas = []

    # 1. CANAL LINKEDIN EN TIEMPO REAL (Diego + Campuslands + Comentarios)
    print("\n[1/4] Rastreando LinkedIn en tiempo real (Diego Tarazona & Campuslands)...", flush=True)
    novedades_linkedin = rastrear_linkedin_vivo(historial)
    for post_li in novedades_linkedin:
        ia = post_li.get("analisis_ia") or {}
        if ia.get("postura_diego"):
            nuevas_posturas.append(f"[LinkedIn {post_li['fecha_corta']}] {ia['postura_diego']}")

    # 2. CANAL INSTAGRAM EN TIEMPO REAL (@diegotarazonap & @campuslands + Reels con IA Multimodal)
    print("\n[2/4] Rastreando Instagram y Reels en tiempo real (@diegotarazonap & @campuslands)...", flush=True)
    novedades_instagram = rastrear_instagram_vivo(historial)
    for item_ig in novedades_instagram:
        av = item_ig.get("analisis_video") or {}
        if av.get("posturas_clave"):
            for p in av["posturas_clave"]:
                nuevas_posturas.append(f"[Instagram Reel {item_ig['shortcode']}] {p}")

    # 3. CANAL YOUTUBE, PODCASTS Y CONFERENCIAS
    print("\n[3/4] Rastreando YouTube, Podcasts y Conferencias...", flush=True)
    video_queries = [
        '"Diego Tarazona" Campuslands',
        'Diego Tarazona entrevista "Campuslands"',
        'Diego Tarazona "inteligencia artificial" Santander',
        'Campuslands "Diego Tarazona" podcast',
    ]
    candidatos_video = buscar_videos_youtube(video_queries, max_por_query=2)
    for vid in candidatos_video:
        vid_id = vid["id"]
        if vid_id in historial:
            continue
        historial.add(vid_id)

        print(f"  Descargando transcripción de YouTube: '{vid['titulo'][:55]}...' ({vid['duracion']})", flush=True)
        transcripcion = extraer_transcripcion_video(vid["url"], vid_id)
        if not transcripcion or len(transcripcion) < 150:
            continue

        analisis_vid = analizar_video_con_gemini(vid, transcripcion)
        if analisis_vid:
            print(f"  [OK YouTube] {vid['titulo'][:65]}", flush=True)
            novedades_video.append((vid, analisis_vid))
            if analisis_vid.get("posturas_clave"):
                nuevas_posturas.extend(analisis_vid["posturas_clave"])

    # 4. CANAL PRENSA, MEDIOS Y RADIOS
    print("\n[4/4] Rastreando Prensa, Periódicos y Radios...", flush=True)
    prensa_queries = [
        '"Diego Tarazona" Campuslands',
        '"Diego Tarazona" Santander',
        'Campuslands Bucaramanga',
        '"Campuslands" Guatemala',
    ]
    candidatos_prensa = []
    for q in prensa_queries:
        for item in buscar_bing_news(q):
            if item["url"] not in historial and item["url"] not in [x["url"] for x in candidatos_prensa]:
                candidatos_prensa.append(item)
        time.sleep(0.5)

    for item in candidatos_prensa:
        url = item["url"]
        historial.add(url)
        contenido = descargar_contenido_url(url)
        if not contenido or len(contenido) < 200:
            continue

        analisis_art = analizar_noticia_con_gemini(item, contenido)
        if analisis_art:
            print(f"  [OK Prensa] {analisis_art.get('titular_limpio')} ({analisis_art.get('medio_nombre')})", flush=True)
            novedades_prensa.append((item, analisis_art))
            if analisis_art.get("es_hito_corporativo"):
                hitos_corporativos.append(analisis_art)

    # 5. CONSOLIDACIÓN Y ESCRITURA EN EL SECOND BRAIN (VAULT_IO)
    total_novedades = (
        len(novedades_linkedin)
        + len(novedades_instagram)
        + len(novedades_video)
        + len(novedades_prensa)
    )
    print(f"\nConsolidando {total_novedades} novedades en el Second Brain...", flush=True)

    if total_novedades > 0:
        hoy = dt.date.today().isoformat()
        with vault_io.lote(f"Investigación automática 360° Diego Tarazona ({total_novedades} novedades)"):

            # A. Guardar LinkedIn + Instagram en investigacion/diego-tarazona/fuentes/redes-sociales.md
            if novedades_linkedin or novedades_instagram:
                plantilla_redes = (
                    f"---\nfecha: {hoy}\ncontexto: campuslands\ntipo: fuentes-redes-sociales\npersona: diego-tarazona\n---\n\n"
                    "# Redes Sociales en Vivo (LinkedIn e Instagram): Diego Tarazona & Campuslands\n\n"
                    "Dossier: [[investigacion/diego-tarazona/dossier|dossier]] · [[people/diego-tarazona|Diego Tarazona]]\n"
                )
                bloque_redes = f"\n\n## Actualización automática ({hoy})\n"

                if novedades_linkedin:
                    bloque_redes += "\n### LinkedIn (Publicaciones y Comentarios)\n"
                    for p_li in novedades_linkedin:
                        ia = p_li.get("analisis_ia") or {}
                        bloque_redes += (
                            f"\n- **[{p_li['fecha_corta']}] {p_li['autor']}: \"{p_li['titulo'] or p_li['texto'][:70]}...\"** — {p_li['url']}\n"
                            f"  - Fecha exacta ISO: `{p_li['fecha_iso']}` | Reacciones: {p_li['likes']} | Comentarios: {len(p_li['comentarios'])}\n"
                            f"  - Síntesis de lo que plantea: {ia.get('resumen_ejecutivo') or p_li['texto'][:250]}\n"
                        )
                        for c_clave in ia.get("citas_clave") or []:
                            bloque_redes += f"  - Cita textual: \"{c_clave}\"\n"
                        if p_li["comentarios"]:
                            bloque_redes += "  - Comentarios de la comunidad:\n"
                            for com in p_li["comentarios"][:5]:
                                bloque_redes += f"    * {com}\n"
                        bloque_redes += f"  - Texto íntegro:\n    > {p_li['texto'].replace(chr(10), ' ')}\n"

                        # También crear ficha en diego_investigacion/02_publicaciones/
                        slug_id = re.sub(r"[^0-9]", "", p_li["url"][-25:])[:12] or f"{int(time.time())}"
                        ruta_ficha_li = f"diego_investigacion/02_publicaciones/auto_li_{p_li['fecha_corta']}_{slug_id}.md"
                        ficha_md = (
                            f"---\nfecha: {p_li['fecha_corta']}\nfecha_iso: \"{p_li['fecha_iso']}\"\n"
                            f"autor: \"{p_li['autor']}\"\ntipo: linkedin-post\ncontexto: campuslands\nurl: \"{p_li['url']}\"\n---\n\n"
                            f"# Publicación LinkedIn ({p_li['fecha_corta']}) — {p_li['autor']}\n\n"
                            f"- **URL:** {p_li['url']}\n"
                            f"- **Fecha exacta:** `{p_li['fecha_iso']}`\n"
                            f"- **Likes:** {p_li['likes']} | **Comentarios:** {len(p_li['comentarios'])}\n\n"
                            f"## Contenido Íntegro\n\n{p_li['texto']}\n\n"
                            f"## Comentarios\n\n" + ("\n".join(f"- {c}" for c in p_li["comentarios"]) if p_li["comentarios"] else "Sin comentarios.") + "\n\n"
                            f"Enlaces: [[people/diego-tarazona|Diego Tarazona]] · [[areas/campuslands|Campuslands]]\n"
                        )
                        vault_io.crear(ruta_ficha_li, ficha_md, f"Post LinkedIn {p_li['fecha_corta']}", aprobado=True, accion="LINKEDIN_POST")

                if novedades_instagram:
                    bloque_redes += "\n### Instagram (Posts y Reels Analizados con IA Multimodal)\n"
                    for ig in novedades_instagram:
                        av = ig.get("analisis_video") or {}
                        tipo_ig = "REEL (Video Analizado)" if ig["es_reel"] else "POST"
                        bloque_redes += (
                            f"\n- **[{ig['fecha']}] ({tipo_ig}) `{ig['shortcode']}`** — {ig['url']}\n"
                            f"  - Descripción/Caption: {ig['descripcion'][:400]}\n"
                        )
                        if av:
                            bloque_redes += f"  - Lo que se ve en el video: {av.get('descripcion_visual', '')}\n"
                            bloque_redes += f"  - Lo que dice en el audio: {av.get('resumen_lo_que_dice', '')}\n"
                            for c_vid in av.get("citas_textuales") or []:
                                bloque_redes += f"  - Cita en video: \"{c_vid}\"\n"

                vault_io.anexar(
                    "investigacion/diego-tarazona/fuentes/redes-sociales.md",
                    bloque_redes,
                    f"Actualización LinkedIn ({len(novedades_linkedin)}) e Instagram ({len(novedades_instagram)})",
                    plantilla=plantilla_redes,
                    aprobado=True,
                    accion="REDES_INVESTIGACION",
                )

            # B. Guardar Videos y Reels en investigacion/diego-tarazona/fuentes/video-podcast.md
            reels_con_video = [ig for ig in novedades_instagram if ig.get("analisis_video")]
            if novedades_video or reels_con_video:
                bloque_video = f"\n\n### Actualización audiovisual ({hoy})\n"
                for vid, av in novedades_video:
                    bloque_video += f"\n- **\"{vid['titulo']}\" / {vid['canal']} / {vid['duracion']}** — {vid['url']}\n"
                    bloque_video += f"  - Lo que dice Diego: {av.get('resumen_lo_que_dice')}\n"
                    for c in av.get("citas_textuales") or []:
                        bloque_video += f"    * {c}\n"
                    bloque_video += "  - Confianza: alta | Tipo: hecho (declaración audiovisual directa)\n"

                for ig in reels_con_video:
                    av = ig["analisis_video"]
                    bloque_video += f"\n- **[Instagram Reel `{ig['shortcode']}`] {ig['fecha']}** — {ig['url']}\n"
                    bloque_video += f"  - Análisis visual: {av.get('descripcion_visual', '')}\n"
                    bloque_video += f"  - Lo que dice en el Reel: {av.get('resumen_lo_que_dice', '')}\n"
                    for c in av.get("citas_textuales") or []:
                        bloque_video += f"    * {c}\n"

                vault_io.anexar(
                    "investigacion/diego-tarazona/fuentes/video-podcast.md",
                    bloque_video,
                    f"Nuevas piezas de video/reels ({len(novedades_video) + len(reels_con_video)})",
                    aprobado=True,
                    accion="VIDEO_INVESTIGACION",
                )

            # C. Guardar Prensa en investigacion/diego-tarazona/fuentes/prensa.md
            if novedades_prensa:
                bloque_prensa = f"\n\n### Actualización prensa ({hoy})\n"
                for item, ap in novedades_prensa:
                    bloque_prensa += f"\n- **\"{ap.get('titular_limpio')}\" / {ap.get('medio_nombre')} / {ap.get('fecha_publicacion', hoy)}** — {item['url']}\n"
                    bloque_prensa += f"  - Hecho: {ap.get('hecho')}\n"
                    if ap.get("cita"):
                        bloque_prensa += f"  - Cita: \"{ap['cita']}\"\n"
                    bloque_prensa += f"  - Confianza: {ap.get('confianza', 'alta')} | Tipo: {ap.get('tipo', 'hecho')}\n"

                vault_io.anexar(
                    "investigacion/diego-tarazona/fuentes/prensa.md",
                    bloque_prensa,
                    f"Nuevas notas de prensa ({len(novedades_prensa)})",
                    aprobado=True,
                    accion="PRENSA_INVESTIGACION",
                )

            # D. Actualizar hitos corporativos y posturas en memoria canónica
            for hito in hitos_corporativos:
                linea_hito = f"\n- **{hito.get('fecha_publicacion', hoy)} ({hito.get('medio_nombre')}):** {hito.get('hecho')}\n"
                vault_io.anexar(
                    "investigacion/diego-tarazona/memoria/campuslands-hechos.md",
                    linea_hito,
                    f"Hito corporativo: {hito.get('titular_limpio')}",
                    aprobado=True,
                    accion="HITO_CAMPUSLANDS",
                )

            if nuevas_posturas:
                bloque_posturas = f"\n\n### Posturas extraídas ({hoy})\n"
                bloque_posturas += "\n".join(f"- {p}" for p in dict.fromkeys(nuevas_posturas)) + "\n"
                vault_io.anexar(
                    "investigacion/diego-tarazona/memoria/temas-y-posturas.md",
                    bloque_posturas,
                    f"Nuevas posturas de Diego ({len(nuevas_posturas)})",
                    aprobado=True,
                    accion="POSTURAS_DIEGO",
                )

        # Reindexar BM25
        print("Reindexando índice local BM25...", flush=True)
        res_idx = indice.actualizar()
        print(f"Índice actualizado: {res_idx}", flush=True)

        # Notificar por WhatsApp
        resumen_wp = (
            f"🌐 *Investigación 360°: Diego Tarazona & Campuslands*\n\n"
            f"• Publicaciones de LinkedIn + comentarios: *{len(novedades_linkedin)}*\n"
            f"• Posts y Reels de Instagram (con video IA): *{len(novedades_instagram)}*\n"
            f"• Videos de YouTube/Podcasts: *{len(novedades_video)}*\n"
            f"• Artículos de prensa y radio: *{len(novedades_prensa)}*\n\n"
            f"Todo ha sido guardado y reindexado en el Second Brain."
        )
        notificar_whatsapp(resumen_wp)

    guardar_historial(historial)
    print(f"\n[FIN] Investigación 360° completada. Total novedades: {total_novedades}", flush=True)
    return {
        "status": "ok",
        "linkedin": len(novedades_linkedin),
        "instagram": len(novedades_instagram),
        "youtube": len(novedades_video),
        "prensa": len(novedades_prensa),
        "total": total_novedades,
    }


if __name__ == "__main__":
    resultado = ejecutar_investigacion_multicanal()
    print("Resultado:", resultado, flush=True)
