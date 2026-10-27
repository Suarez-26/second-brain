import json
import os
import re
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
        return ckey.startsWith('update-card-focus') || h2Text.includes('Publicación') || h2Text.includes('Feed post') || el.classList.contains('feed-shared-update-v2');
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


def scroll_to_bottom_exhaustively(page, label="", max_rounds=80):
    print(f"Haciendo scroll exhaustivo en {label} hasta llegar al final absoluto...")
    last_count = 0
    stagnant = 0
    for r in range(max_rounds):
        count = page.evaluate(f"({POST_CARDS_JS})().length")
        if r % 3 == 0 or count != last_count:
            print(f"  [{label}] Ronda scroll {r+1}: {count} elementos cargados")
        if count == last_count:
            stagnant += 1
            # Try clicking any "Mostrar más resultados" / "Show more results" button
            clicked_more = page.evaluate("""
            () => {
                let c = 0;
                document.querySelectorAll('button').forEach(b => {
                    const t = (b.innerText || '').trim().toLowerCase();
                    if (t.includes('mostrar más') || t.includes('show more') || t.includes('ver más resultados')) {
                        try { b.click(); c++; } catch(e) {}
                    }
                });
                return c;
            }
            """)
            if clicked_more:
                print(f"  [{label}] Clic en botón 'Mostrar más resultados'")
                stagnant = 0
            if stagnant >= 7:
                print(f"  [{label}] Final absoluto alcanzado con {count} elementos.")
                break
        else:
            stagnant = 0
            last_count = count

        page.evaluate("""
        () => {
            const m = document.querySelector('main');
            if (m) m.scrollBy(0, 2800);
            window.scrollBy(0, 2800);
            const items = Array.from(document.querySelectorAll('[componentkey^="update-card-focus"], [role="listitem"]'));
            if (items.length > 0) items[items.length - 1].scrollIntoView();
        }
        """)
        time.sleep(2.2)
    return page.evaluate(f"({POST_CARDS_JS})().length")


def extract_extra_profile_sections(page):
    print("\n=== 1. Extrayendo TODAS las subpáginas adicionales del perfil de Diego ===")
    base = "https://www.linkedin.com/in/diegotarazonapinzon"
    extra_urls = {
        "contacto": f"{base}/overlay/contact-info/",
        "acerca_de_este_perfil": f"{base}/overlay/about-this-profile/",
        "recomendaciones": f"{base}/details/recommendations/",
        "intereses": f"{base}/details/interests/",
        "certificaciones": f"{base}/details/certifications/",
        "voluntariado": f"{base}/details/volunteering-experiences/",
        "organizaciones": f"{base}/details/organizations/",
        "publicaciones_editoriales": f"{base}/details/publications/",
        "proyectos": f"{base}/details/projects/",
        "idiomas": f"{base}/details/languages/",
        "cursos": f"{base}/details/courses/",
    }
    results = {}
    for name, url in extra_urls.items():
        try:
            print(f"Consultando {name}: {url}")
            page.goto(url, wait_until="domcontentloaded", timeout=45000)
            time.sleep(2.8)
            # If there are tabs inside recommendations or interests, extract all tabs
            text = page.evaluate("""
            () => {
                const dialog = document.querySelector('[role="dialog"], .artdeco-modal');
                const main = document.querySelector('main') || document.body;
                return (dialog ? dialog.innerText : main.innerText).trim();
            }
            """)
            # For recommendations or interests, also click secondary tabs if present
            tab_texts = [text]
            tabs_count = page.evaluate("""
            () => {
                const tabs = Array.from(document.querySelectorAll('[role="tab"]'));
                return tabs.length;
            }
            """)
            if tabs_count > 1:
                for t_idx in range(1, min(tabs_count, 6)):
                    try:
                        page.evaluate(f"() => {{ const tabs = document.querySelectorAll('[role=\"tab\"]'); if (tabs[{t_idx}]) tabs[{t_idx}].click(); }}")
                        time.sleep(2.0)
                        t_text = page.evaluate("() => (document.querySelector('main') || document.body).innerText.trim()")
                        tab_texts.append(f"--- PESTAÑA {t_idx + 1} ---\n" + t_text)
                    except Exception:
                        pass
            results[name] = "\n\n".join(tab_texts)
        except Exception as e:
            print(f"Aviso en {name}: {e}")

    md_lines = [
        "---",
        "fecha: 2026-10-20",
        "contexto: campuslands",
        "tipo: perfil-linkedin-completo-extra",
        "persona: diego-tarazona",
        "---",
        "",
        "# Secciones Adicionales del Perfil de LinkedIn de Diego Tarazona",
        "(Contacto, Acerca del perfil, Recomendaciones, Intereses, Certificaciones, Voluntariado, Proyectos, Idiomas)",
        ""
    ]
    for k, v in results.items():
        # Strip footer boilerplate
        cleaned = v.split("Más perfiles para ti")[0].split("Seleccionar idioma")[0].strip()
        md_lines.append(f"## {k.replace('_', ' ').title()}")
        md_lines.append("```text")
        md_lines.append(cleaned)
        md_lines.append("```")
        md_lines.append("")

    (BASE_DIR / "01c_perfil_secciones_extra.md").write_text("\n".join(md_lines), encoding="utf-8")
    print("Guardado 01c_perfil_secciones_extra.md exitosamente.")


def extract_cards_from_current_page(page, prefix, start_idx=0, expand_comments=True):
    total_tagged = page.evaluate(f"""
    () => {{
        const cards = ({POST_CARDS_JS})();
        const seenKeys = new Set();
        let idx = 0;
        for (const card of cards) {{
            const key = card.getAttribute('componentkey') || card.innerText.slice(0, 140);
            if (seenKeys.has(key)) continue;
            seenKeys.add(key);
            card.setAttribute('data-extract-idx', String(idx));
            idx++;
        }}
        return idx;
    }}
    """)
    print(f"Total de tarjetas únicas en página para '{prefix}': {total_tagged} (extrayendo desde {start_idx + 1})")

    for idx in range(start_idx, total_tagged):
        post_num = idx + 1
        post_id = f"{prefix}_{post_num:03d}"
        print(f"--- Procesando {post_id} ({post_num}/{total_tagged}) ---")

        locator = page.locator(f'[data-extract-idx="{idx}"]').first
        try:
            locator.scroll_into_view_if_needed(timeout=8000)
            time.sleep(1.2)
        except Exception:
            pass

        # Expand "... más" and optionally click comment button to load comments
        page.evaluate("""
        (args) => {
            const node = document.querySelector(`[data-extract-idx="${args.idx}"]`);
            if (!node) return;
            node.querySelectorAll('button, span[role="button"]').forEach(btn => {
                const t = (btn.innerText || '').trim().toLowerCase();
                const al = (btn.getAttribute('aria-label') || '').toLowerCase();
                if (t === '...más' || t === '…más' || t === '… más' || t === '... más' || t === '...more' || t === '…more') {
                    try { btn.click(); } catch (e) {}
                }
                if (args.expandComments && (al.includes('comentario') || al.includes('comment') || (t.includes('comentario') && t.length < 25))) {
                    try { btn.click(); } catch (e) {}
                }
            });
        }
        """, {"idx": idx, "expandComments": expand_comments})
        time.sleep(1.0)

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
        if post_info["hasVideo"]:
            if not post_info["videoMp4s"]:
                try:
                    play_btn = locator.locator('button[aria-label*="Reproducir"], button[aria-label*="Play"], .vjs-big-play-button, video').first
                    play_btn.click(timeout=3500)
                    time.sleep(1.8)
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
                except Exception:
                    pass

            if post_info["videoMp4s"]:
                best_mp4 = post_info["videoMp4s"][-1]
                for c in post_info["videoMp4s"]:
                    if "720p" in c or "1080p" in c:
                        best_mp4 = c
                vid_path = VID_DIR / f"{post_id}.mp4"
                if not vid_path.exists():
                    if download_file(best_mp4, vid_path):
                        saved_video = vid_path.name
                        print(f"¡Video guardado: {saved_video}!")
                else:
                    saved_video = vid_path.name

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
            "## Contenido Íntegro Extraído (Incluyendo Comentarios Visibles)",
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
        time.sleep(1.0)


def extract_activity_tab_consolidated(page, url, out_filename, title):
    print(f"\n=== Extrayendo pestaña completa: {title} ({url}) ===")
    page.goto(url, wait_until="domcontentloaded", timeout=60000)
    time.sleep(3.5)
    scroll_to_bottom_exhaustively(page, label=title, max_rounds=40)
    # Expand all "... más"
    page.evaluate("""
    () => {
        document.querySelectorAll('button, span[role="button"]').forEach(btn => {
            const t = (btn.innerText || '').trim().toLowerCase();
            if (t === '...más' || t === '…más' || t === '… más' || t === '... más' || t === '...more' || t === '…more') {
                try { btn.click(); } catch (e) {}
            }
        });
    }
    """)
    time.sleep(1.5)
    items = page.evaluate(f"""
    () => {{
        const cards = ({POST_CARDS_JS})();
        return cards.map((c, idx) => ({{
            idx: idx + 1,
            ckey: c.getAttribute('componentkey') || '',
            text: c.innerText.trim()
        }}));
    }}
    """)
    md = [
        "---",
        "fecha: 2026-10-20",
        "contexto: campuslands",
        f"url: \"{url}\"",
        "---",
        "",
        f"# {title} (Total: {len(items)})",
        ""
    ]
    for it in items:
        md.append(f"## Item #{it['idx']}")
        md.append("```text")
        md.append(it["text"])
        md.append("```")
        md.append("")
    (PUB_DIR / out_filename).write_text("\n".join(md), encoding="utf-8")
    print(f"Guardado {out_filename} con {len(items)} registros.")


def main():
    with sync_playwright() as p:
        print("Conectando a Chrome en puerto 9222 para extracción exhaustiva total...")
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        pg = [x for x in ctx.pages if "linkedin.com" in x.url][0]

        # 1. Extra profile sections (Recommendations, Interests, Contact Info, About Profile, Certifications, Volunteering, etc.)
        extract_extra_profile_sections(pg)

        # 2. ALL remaining posts of Diego from #26 down to the very first post ever published
        print("\n=== 2. Extrayendo TODAS las publicaciones históricas de Diego (desde la #26 hasta la primera) ===")
        pg.goto("https://www.linkedin.com/in/diegotarazonapinzon/recent-activity/all/", wait_until="domcontentloaded", timeout=60000)
        time.sleep(4.0)
        scroll_to_bottom_exhaustively(pg, label="Diego All Activity", max_rounds=80)
        extract_cards_from_current_page(pg, prefix="post", start_idx=25, expand_comments=True)

        # 3. ALL Comments made by Diego on LinkedIn
        extract_activity_tab_consolidated(
            pg,
            "https://www.linkedin.com/in/diegotarazonapinzon/recent-activity/comments/",
            "00_comentarios_diego.md",
            "Historial Completo de Comentarios de Diego Tarazona en LinkedIn"
        )

        # 4. ALL Reactions made by Diego on LinkedIn
        extract_activity_tab_consolidated(
            pg,
            "https://www.linkedin.com/in/diegotarazonapinzon/recent-activity/reactions/",
            "00_reacciones_diego.md",
            "Historial Completo de Reacciones de Diego Tarazona en LinkedIn"
        )

        # 5. ALL Mentions of "Diego Tarazona" by third parties across LinkedIn
        print("\n=== 5. Buscando TODAS las menciones a 'Diego Tarazona' en LinkedIn ===")
        search_url = "https://www.linkedin.com/search/results/content/?keywords=%22Diego%20Tarazona%22&origin=GLOBAL_SEARCH_HEADER"
        pg.goto(search_url, wait_until="domcontentloaded", timeout=60000)
        time.sleep(4.0)
        scroll_to_bottom_exhaustively(pg, label="Menciones Diego Tarazona", max_rounds=45)
        extract_cards_from_current_page(pg, prefix="mencion", start_idx=0, expand_comments=True)

        # 6. ALL remaining posts of Campuslands from #16 down to the first
        print("\n=== 6. Extrayendo resto de publicaciones históricas de Campuslands ===")
        pg.goto("https://www.linkedin.com/company/campuslands/posts/?feedView=all", wait_until="domcontentloaded", timeout=60000)
        time.sleep(4.0)
        scroll_to_bottom_exhaustively(pg, label="Campuslands Posts", max_rounds=50)
        extract_cards_from_current_page(pg, prefix="campuslands", start_idx=15, expand_comments=True)

        print("\n¡¡EXTRACCIÓN EXHAUSTIVA TOTAL FINALIZADA!!")


if __name__ == "__main__":
    main()
