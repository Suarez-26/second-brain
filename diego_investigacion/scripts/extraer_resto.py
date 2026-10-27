import json
import sys
import time
import urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

BASE_DIR = Path(__file__).resolve().parent.parent
PUB_DIR = BASE_DIR / "02_publicaciones"
IMG_DIR = BASE_DIR / "03_imagenes"
VID_DIR = BASE_DIR / "04_videos_y_audios"
INDICE_FILE = BASE_DIR / "indice_progreso.md"

POST_CARDS_JS = """
() => {
    const listitems = Array.from(document.querySelectorAll('[role="listitem"], article, div.feed-shared-update-v2'));
    return listitems.filter(el => {
        if (el.parentElement && el.parentElement.closest('[componentkey^="update-card-focus"], div.feed-shared-update-v2')) {
            return false;
        }
        const ckey = el.getAttribute('componentkey') || '';
        const h2 = el.querySelector('h2');
        const h2Text = h2 ? h2.innerText.trim() : '';
        return ckey.startsWith('update-card-focus') || h2Text.includes('Publicación') || h2Text.includes('Feed post');
    });
}
"""


def download_file(url, dest_path):
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                "Referer": "https://www.linkedin.com/"
            }
        )
        with urllib.request.urlopen(req, timeout=60) as resp, open(dest_path, "wb") as out:
            out.write(resp.read())
        return True
    except Exception as e:
        print(f"Error descargando {url[:80]}: {e}")
        return False


def extract_range(page, feed_url, prefix, start_idx, max_posts):
    print(f"\nNavegando a {feed_url} para extraer desde {start_idx + 1} hasta {max_posts}...")
    if page.url.rstrip("/") != feed_url.rstrip("/"):
        page.goto(feed_url, wait_until="domcontentloaded", timeout=60000)
        time.sleep(4)

    # Scroll <main> AND last card into view to trigger infinite scroll
    for _ in range(12):
        count = page.evaluate(f"({POST_CARDS_JS})().length")
        print(f"Cargadas ({prefix}): {count}/{max_posts}")
        if count >= max_posts:
            break
        page.evaluate("""
        () => {
            const m = document.querySelector('main');
            if (m) m.scrollBy(0, 2200);
            window.scrollBy(0, 2200);
            const items = Array.from(document.querySelectorAll('[componentkey^="update-card-focus"]'));
            if (items.length > 0) items[items.length - 1].scrollIntoView();
        }
        """)
        time.sleep(2.5)

    total_tagged = page.evaluate(f"""
    (maxPosts) => {{
        const cards = ({POST_CARDS_JS})();
        const seenKeys = new Set();
        let idx = 0;
        for (const card of cards) {{
            const key = card.getAttribute('componentkey') || card.innerText.slice(0, 120);
            if (seenKeys.has(key)) continue;
            seenKeys.add(key);
            card.setAttribute('data-extract-idx', String(idx));
            idx++;
            if (idx >= maxPosts) break;
        }}
        return idx;
    }}
    """, max_posts)

    for idx in range(start_idx, total_tagged):
        post_num = idx + 1
        post_id = f"{prefix}_{post_num:03d}"
        print(f"--- Procesando {post_id} ({post_num}/{total_tagged}) ---")
        locator = page.locator(f'[data-extract-idx="{idx}"]').first
        try:
            locator.scroll_into_view_if_needed(timeout=10000)
            time.sleep(1.5)
        except Exception:
            pass

        page.evaluate("""
        (idx) => {
            const node = document.querySelector(`[data-extract-idx="${idx}"]`);
            if (!node) return;
            node.querySelectorAll('button, span[role="button"]').forEach(btn => {
                const t = (btn.innerText || '').trim().toLowerCase();
                if (t === '...más' || t === '…más' || t === '… más' || t === '... más' || t === '...more' || t === '…more') {
                    try { btn.click(); } catch (e) {}
                }
            });
        }
        """, idx)
        time.sleep(0.8)

        post_info = page.evaluate("""
        (idx) => {
            const node = document.querySelector(`[data-extract-idx="${idx}"]`);
            if (!node) return null;
            const ckey = node.getAttribute('componentkey') || '';
            const fullText = node.innerText.trim();
            const imgs = Array.from(node.querySelectorAll('img'))
                .filter(im => {
                    const src = im.src || '';
                    if (!src || src.startsWith('data:')) return false;
                    if (src.includes('profile-displayphoto') || src.includes('company-logo_100_100') || src.includes('static.licdn.com')) return false;
                    return true;
                })
                .map(im => im.src);

            const videoMp4s = [];
            const vjsNodes = Array.from(node.querySelectorAll('.video-js, video'));
            let hasVideo = vjsNodes.length > 0 || imgs.some(u => u.includes('playlist/vid') || u.includes('videocover'));
            vjsNodes.forEach(el => {
                const pEl = el.classList && el.classList.contains('video-js') ? el : (el.closest('.video-js') || el.parentElement);
                if (pEl && pEl.player && typeof pEl.player.currentSources === 'function') {
                    try {
                        (pEl.player.currentSources() || []).forEach(s => {
                            if (s && s.src && (s.type === 'video/mp4' || s.src.includes('mp4-'))) videoMp4s.push(s.src);
                        });
                    } catch (e) {}
                }
            });

            const iframes = Array.from(node.querySelectorAll('iframe')).map(f => f.src).filter(Boolean);
            const hasDocument = iframes.some(u => u.includes('document') || u.includes('native-document'));
            const links = Array.from(node.querySelectorAll('a[href]')).map(a => a.href).filter(h => h && !h.includes('linkedin.com/in/') && !h.includes('linkedin.com/company/') && !h.includes('/feed/hashtag/'));

            return { ckey, fullText, imgs: Array.from(new Set(imgs)), hasVideo, videoMp4s: Array.from(new Set(videoMp4s)), hasDocument, iframes, links: Array.from(new Set(links)) };
        }
        """, idx)

        if not post_info:
            continue

        try:
            locator.screenshot(path=str(IMG_DIR / f"{post_id}_card.png"))
        except Exception:
            pass

        saved_images = []
        for img_i, img_url in enumerate(post_info["imgs"], start=1):
            img_path = IMG_DIR / f"{post_id}_img_{img_i:02d}.jpg"
            if download_file(img_url, img_path):
                saved_images.append(img_path.name)

        saved_video = None
        if post_info["hasVideo"] and post_info["videoMp4s"]:
            best_mp4 = post_info["videoMp4s"][-1]
            for c in post_info["videoMp4s"]:
                if "720p" in c or "1080p" in c:
                    best_mp4 = c
            vid_path = VID_DIR / f"{post_id}.mp4"
            if download_file(best_mp4, vid_path):
                saved_video = vid_path.name
                print(f"¡Video guardado: {saved_video}!")

        lines = [ln.strip() for ln in post_info["fullText"].splitlines() if ln.strip()]
        if lines and ("Publicación" in lines[0] or "Feed post" in lines[0]):
            lines = lines[1:]
        header_line = lines[0] if lines else ""
        date_line = ""
        for ln in lines[:8]:
            if any(tok in ln for tok in ["días", "día", "sem", "mes", "año", " h", "min", "Editado"]) and len(ln) < 35:
                date_line = ln
                break

        tipos = ["Texto"]
        if post_info["hasVideo"]:
            tipos.append("Video")
        if post_info["hasDocument"]:
            tipos.append("Carrusel/PDF")
        elif saved_images:
            tipos.append("Imagen")
        tipo_str = " + ".join(tipos)

        post_info["saved_images"] = saved_images
        post_info["saved_video"] = saved_video
        post_info["fecha_relativa"] = date_line
        post_info["tipo"] = tipo_str

        (PUB_DIR / f"{post_id}.json").write_text(json.dumps(post_info, ensure_ascii=False, indent=2), encoding="utf-8")
        md_content = [
            "---",
            f"id: {post_id}",
            f"componentkey: \"{post_info['ckey']}\"",
            "fecha_extraccion: 2026-10-20",
            f"fecha_relativa: \"{date_line}\"",
            f"tipo: \"{tipo_str}\"",
            "contexto: campuslands",
            "---",
            "",
            f"# Publicación `{post_id}`",
            "",
            f"- **Cabecera / Autor:** {header_line}",
            f"- **Fecha relativa:** {date_line or 'Ver texto'}",
            f"- **Tipo de contenido:** {tipo_str}",
            f"- **Captura visual de la publicación:** `../03_imagenes/{post_id}_card.png`",
            f"- **Imágenes descargadas:** {', '.join(saved_images) if saved_images else 'Ninguna'}",
            f"- **Video descargado:** `{saved_video}`" if saved_video else f"- **Video descargado:** {'Sin MP4 directo' if post_info['hasVideo'] else 'No aplica'}",
            "",
            "## Contenido Íntegro Extraído",
            "",
            "```text",
            post_info["fullText"],
            "```",
            ""
        ]
        (PUB_DIR / f"{post_id}.md").write_text("\n".join(md_content), encoding="utf-8")

        summary_candidates = [ln for ln in lines if len(ln) > 40 and "CEO & Co-Founder" not in ln and "Seguir" not in ln]
        one_line = (summary_candidates[0] if summary_candidates else header_line)[:90].replace("|", "/")
        files_gen = f"`{post_id}.md`"
        if saved_images:
            files_gen += f", {len(saved_images)} img"
        if saved_video:
            files_gen += f", `{saved_video}`"
        row = f"| `{post_id}` | {date_line or 'N/A'} | {tipo_str} | {one_line}... | {files_gen} | Extraído |\n"
        with open(INDICE_FILE, "a", encoding="utf-8") as idxf:
            idxf.write(row)
        time.sleep(1.5)


with sync_playwright() as p:
    b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    pg = [x for x in b.contexts[0].pages if "linkedin.com" in x.url][0]
    # Currently on campuslands posts! Extract 4..15 first
    extract_range(pg, "https://www.linkedin.com/company/campuslands/posts/?feedView=all", "campuslands", 3, 15)
    # Then Diego's 21..25
    extract_range(pg, "https://www.linkedin.com/in/diegotarazonapinzon/recent-activity/all/", "post", 20, 25)
    print("¡Extracción complementaria terminada!")
