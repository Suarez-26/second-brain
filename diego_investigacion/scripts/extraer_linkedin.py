import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright

try:
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
except Exception:
    pass

BASE_DIR = Path(__file__).resolve().parent.parent
PUB_DIR = BASE_DIR / "02_publicaciones"
IMG_DIR = BASE_DIR / "03_imagenes"
VID_DIR = BASE_DIR / "04_videos_y_audios"
TRANS_DIR = BASE_DIR / "05_transcripciones"
PROFILE_DIR = BASE_DIR / ".chrome_profile"
INDICE_FILE = BASE_DIR / "indice_progreso.md"

for d in [PUB_DIR, IMG_DIR, VID_DIR, TRANS_DIR, PROFILE_DIR]:
    d.mkdir(parents=True, exist_ok=True)

TARGET_PROFILE = "https://www.linkedin.com/in/diegotarazonapinzon/"
TARGET_COMPANY = "https://www.linkedin.com/company/campuslands/"
MAX_DIEGO_POSTS = 25
MAX_COMPANY_POSTS = 15


def human_sleep(min_s=1.8, max_s=3.0):
    import random
    time.sleep(random.uniform(min_s, max_s))


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


POST_CARDS_JS = """
() => {
    const listitems = Array.from(document.querySelectorAll('[role="listitem"], article, div.feed-shared-update-v2'));
    return listitems.filter(el => {
        // Avoid nested cards inside another card
        if (el.parentElement && el.parentElement.closest('[componentkey^="update-card-focus"], div.feed-shared-update-v2')) {
            return false;
        }
        const ckey = el.getAttribute('componentkey') || '';
        const h2 = el.querySelector('h2');
        const h2Text = h2 ? h2.innerText.trim() : '';
        const urn = el.getAttribute('data-urn') || el.getAttribute('data-id') || '';
        return (
            ckey.startsWith('update-card-focus') ||
            h2Text.includes('Publicación') ||
            h2Text.includes('Feed post') ||
            urn.startsWith('urn:li:activity:') ||
            urn.startsWith('urn:li:ugcPost:') ||
            el.classList.contains('feed-shared-update-v2')
        );
    });
}
"""


def expand_all_see_more(page):
    try:
        return page.evaluate("""
        () => {
            let clicked = 0;
            document.querySelectorAll('button, span[role="button"]').forEach(btn => {
                const t = (btn.innerText || '').trim().toLowerCase();
                if (t === '...más' || t === '…más' || t === '… más' || t === '... más' || t === '...more' || t === '…more' || t === '… see more') {
                    try {
                        btn.click();
                        clicked++;
                    } catch (e) {}
                }
            });
            return clicked;
        }
        """)
    except Exception:
        return 0


def extract_posts_from_feed(page, feed_url, prefix="post", max_posts=25):
    print(f"\nNavegando al feed de publicaciones: {feed_url}")
    page.goto(feed_url, wait_until="domcontentloaded", timeout=60000)
    human_sleep(3.5, 5.0)

    # Scroll until at least max_posts are loaded
    last_count = 0
    stagnant_rounds = 0
    while True:
        count = page.evaluate(f"({POST_CARDS_JS})().length")
        print(f"Publicaciones cargadas en DOM ({prefix}): {count}/{max_posts}")
        if count >= max_posts:
            break
        if count == last_count:
            stagnant_rounds += 1
            if stagnant_rounds >= 5:
                print("Fin de publicaciones disponibles o límite de scroll alcanzado.")
                break
        else:
            stagnant_rounds = 0
            last_count = count

        page.mouse.wheel(0, 1600)
        human_sleep(2.2, 3.5)
        expand_all_see_more(page)

    # Tag the cards with data-extract-idx
    total_tagged = page.evaluate(f"""
    (maxPosts) => {{
        const cards = ({POST_CARDS_JS})();
        const seenKeys = new Set();
        let idx = 0;
        for (const card of cards) {{
            const key = card.getAttribute('componentkey') || card.getAttribute('data-urn') || card.innerText.slice(0, 120);
            if (seenKeys.has(key)) continue;
            seenKeys.add(key);
            card.setAttribute('data-extract-idx', String(idx));
            idx++;
            if (idx >= maxPosts) break;
        }}
        return idx;
    }}
    """, max_posts)

    print(f"Procesando {total_tagged} publicaciones ({prefix})...")

    for idx in range(total_tagged):
        post_num = idx + 1
        post_id = f"{prefix}_{post_num:03d}"
        print(f"\n--- Procesando {post_id} ({post_num}/{total_tagged}) ---")

        locator = page.locator(f'[data-extract-idx="{idx}"]').first
        try:
            locator.scroll_into_view_if_needed(timeout=10000)
            human_sleep(1.2, 2.0)
        except Exception as e:
            print(f"Aviso scroll {post_id}: {e}")

        # Expand "... más" inside this card
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

        # Extract details + Video.js MP4 URLs
        post_info = page.evaluate("""
        (idx) => {
            const node = document.querySelector(`[data-extract-idx="${idx}"]`);
            if (!node) return null;

            const ckey = node.getAttribute('componentkey') || node.getAttribute('data-urn') || '';
            const fullText = node.innerText.trim();

            // Images (excluding avatars/logos of 100x100)
            const imgs = Array.from(node.querySelectorAll('img'))
                .filter(im => {
                    const src = im.src || '';
                    if (!src || src.startsWith('data:')) return false;
                    if (src.includes('profile-displayphoto') || src.includes('company-logo_100_100') || src.includes('static.licdn.com')) return false;
                    return true;
                })
                .map(im => im.src);

            // Videos via Video.js player API or <video> tags
            const videoMp4s = [];
            const vjsNodes = Array.from(node.querySelectorAll('.video-js, video'));
            let hasVideo = vjsNodes.length > 0 || imgs.some(u => u.includes('playlist/vid') || u.includes('videocover'));
            vjsNodes.forEach(el => {
                const pEl = el.classList && el.classList.contains('video-js') ? el : (el.closest('.video-js') || el.parentElement);
                if (pEl && pEl.player && typeof pEl.player.currentSources === 'function') {
                    try {
                        const srcs = pEl.player.currentSources() || [];
                        srcs.forEach(s => {
                            if (s && s.src && (s.type === 'video/mp4' || s.src.includes('mp4-'))) {
                                videoMp4s.push(s.src);
                            }
                        });
                    } catch (e) {}
                }
                if (el.tagName === 'VIDEO') {
                    if (el.src && el.src.startsWith('http') && !el.src.startsWith('blob:')) videoMp4s.push(el.src);
                    const ds = el.getAttribute('data-sources');
                    if (ds) {
                        try {
                            JSON.parse(ds).forEach(p => { if (p.src) videoMp4s.push(p.src); });
                        } catch (e) {}
                    }
                }
            });

            // Document / Carousel detection
            const iframes = Array.from(node.querySelectorAll('iframe')).map(f => f.src).filter(Boolean);
            const hasDocument = iframes.some(u => u.includes('document') || u.includes('native-document')) ||
                                node.querySelectorAll('.ssplayer-carousel, .feed-shared-document, .update-components-document').length > 0;

            // Links inside post
            const links = Array.from(node.querySelectorAll('a[href]'))
                .map(a => a.href)
                .filter(h => h && !h.includes('linkedin.com/in/') && !h.includes('linkedin.com/company/') && !h.includes('/feed/hashtag/'));

            return {
                ckey,
                fullText,
                imgs: Array.from(new Set(imgs)),
                hasVideo,
                videoMp4s: Array.from(new Set(videoMp4s)),
                hasDocument,
                iframes,
                links: Array.from(new Set(links))
            };
        }
        """, idx)

        if not post_info:
            continue

        # Take screenshot of the post card
        card_img_path = IMG_DIR / f"{post_id}_card.png"
        try:
            locator.screenshot(path=str(card_img_path))
        except Exception as e:
            print(f"Aviso screenshot card {post_id}: {e}")

        # Download images
        saved_images = []
        for img_i, img_url in enumerate(post_info["imgs"], start=1):
            img_path = IMG_DIR / f"{post_id}_img_{img_i:02d}.jpg"
            if download_file(img_url, img_path):
                saved_images.append(img_path.name)

        # Download video if present
        saved_video = None
        if post_info["hasVideo"]:
            if not post_info["videoMp4s"]:
                # Try clicking play button to initialize Video.js player
                try:
                    play_btn = locator.locator('button[aria-label*="Reproducir"], button[aria-label*="Play"], .vjs-big-play-button, video').first
                    play_btn.click(timeout=4000)
                    time.sleep(2.0)
                    more_mp4s = page.evaluate("""
                    (idx) => {
                        const node = document.querySelector(`[data-extract-idx="${idx}"]`);
                        if (!node) return [];
                        const out = [];
                        node.querySelectorAll('.video-js, video').forEach(el => {
                            const pEl = el.classList && el.classList.contains('video-js') ? el : (el.closest('.video-js') || el.parentElement);
                            if (pEl && pEl.player && typeof pEl.player.currentSources === 'function') {
                                try {
                                    (pEl.player.currentSources() || []).forEach(s => {
                                        if (s && s.src && (s.type === 'video/mp4' || s.src.includes('mp4-'))) out.push(s.src);
                                    });
                                    pEl.player.pause();
                                } catch (e) {}
                            }
                            if (el.tagName === 'VIDEO') {
                                try { el.pause(); } catch (e) {}
                            }
                        });
                        return out;
                    }
                    """, idx)
                    post_info["videoMp4s"].extend(more_mp4s)
                except Exception as e:
                    print(f"Aviso inicializar video {post_id}: {e}")

            if post_info["videoMp4s"]:
                # Pick highest quality (usually last in Video.js sources: 720p)
                best_mp4 = post_info["videoMp4s"][-1]
                for candidate in post_info["videoMp4s"]:
                    if "720p" in candidate or "1080p" in candidate:
                        best_mp4 = candidate
                vid_path = VID_DIR / f"{post_id}.mp4"
                print(f"Descargando video MP4 de {post_id}...")
                if download_file(best_mp4, vid_path):
                    saved_video = vid_path.name
                    print(f"¡Video guardado: {saved_video}!")

        # Parse fullText lines to extract clean metadata
        lines = [ln.strip() for ln in post_info["fullText"].splitlines() if ln.strip()]
        # Remove leading "Publicación en el feed"
        if lines and ("Publicación" in lines[0] or "Feed post" in lines[0]):
            lines = lines[1:]

        header_line = lines[0] if lines else ""
        date_line = ""
        for ln in lines[:8]:
            if any(tok in ln for tok in ["días", "día", "sem", "mes", "año", " h", "min", "Editado"]):
                if len(ln) < 35:
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
            f"fecha_extraccion: 2026-10-20",
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

        # Update indice_progreso.md
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

        human_sleep(1.5, 2.5)


def main():
    # Reset indice_progreso.md header cleanly
    INDICE_FILE.write_text(
        "# Índice de Progreso - Investigación LinkedIn (Diego Tarazona & Campuslands)\n\n"
        "| ID Post | Fecha Relativa | Tipo | Resumen de 1 línea | Archivos Generados | Estado |\n"
        "| :--- | :--- | :--- | :--- | :--- | :--- |\n",
        encoding="utf-8"
    )

    with sync_playwright() as p:
        print("Conectando Playwright vía CDP al Chrome visible...")
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        valid_pages = [pg for pg in context.pages if pg.url.startswith("http") and "linkedin.com" in pg.url]
        if not valid_pages:
            valid_pages = [pg for pg in context.pages if not pg.url.startswith("chrome://")]
        page = valid_pages[0] if valid_pages else context.new_page()

        extract_posts_from_feed(
            page,
            f"{TARGET_PROFILE.rstrip('/')}/recent-activity/all/",
            prefix="post",
            max_posts=MAX_DIEGO_POSTS
        )
        extract_posts_from_feed(
            page,
            f"{TARGET_COMPANY.rstrip('/')}/posts/?feedView=all",
            prefix="campuslands",
            max_posts=MAX_COMPANY_POSTS
        )

        print("\n¡Extracción de publicaciones, imágenes y videos completada!")


if __name__ == "__main__":
    main()
