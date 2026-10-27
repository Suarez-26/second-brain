import os
import json
import time
import urllib.parse
from pathlib import Path
from playwright.sync_api import sync_playwright

VAULT_DIR = Path(r"C:\Users\tomas\second-brain")
OUT_DIR = VAULT_DIR / "investigacion" / "campuslands" / "fuentes"
SOURCES_DIR = VAULT_DIR / "sources" / "prensa_y_web"
OUT_DIR.mkdir(parents=True, exist_ok=True)
SOURCES_DIR.mkdir(parents=True, exist_ok=True)

def main():
    with sync_playwright() as p:
        print("Conectando a Chrome en 127.0.0.1:9222...")
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = browser.contexts[0]

        yt_page = None
        web_page = None
        for pg in ctx.pages:
            if "youtube.com" in pg.url:
                yt_page = pg
            elif pg.url == "about:blank" or "google.com" in pg.url or "campuslands.com" in pg.url or "reddit.com" in pg.url:
                web_page = pg

        if not yt_page:
            yt_page = ctx.new_page()
        if not web_page:
            web_page = ctx.new_page()

        # Traer primero la pestaña de Google/Web al frente y cargarle contenido de inmediato para que no esté en blanco
        web_page.bring_to_front()
        web_page.goto("https://www.google.com/search?q=%22Diego+Tarazona%22+%22Campuslands%22&hl=es", wait_until="domcontentloaded", timeout=30000)

        yt_queries = [
            "Campuslands",
            "Diego Tarazona Campuslands",
            "Diego Fernando Tarazona Pinzon",
            "The Human Code Campuslands",
            "Campuslands Bucaramanga",
            "Campuslands Guatemala",
            "Campuslands Tibu",
            "Campuslands Fedesoft",
            "Campuslands MinTIC",
            "Campus Programmers Land"
        ]

        google_queries = [
            '"Diego Tarazona" "Campuslands"',
            '"Diego Fernando Tarazona Pinzón"',
            '"Campuslands" Bucaramanga OR Guatemala OR Tibú OR Bogotá',
            '"Campus Programmers Land" Bancolombia OR Bucaramanga',
            'site:reddit.com "campuslands" OR "campus programmers"',
            'site:github.com "campuslands"',
            '"Campuslands" Fedesoft OR "Premios Ingenio" OR SOFTIC',
            '"Campuslands" "Zona Franca Santander" OR "Gobernación de Santander"'
        ]

        all_yt_found = []
        all_google_found = []

        # Intercalamos las búsquedas en ambas pestañas (YouTube y Google/Web) trayéndolas al frente para que se vea la actividad en vivo
        max_len = max(len(yt_queries), len(google_queries))
        for i in range(max_len):
            if i < len(yt_queries):
                q = yt_queries[i]
                url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(q)}"
                print(f"[Pestaña YouTube] Buscando: {q}")
                try:
                    yt_page.bring_to_front()
                    yt_page.goto(url, wait_until="domcontentloaded", timeout=30000)
                    time.sleep(2.0)
                    for _ in range(3):
                        yt_page.evaluate("window.scrollBy(0, 1400)")
                        time.sleep(1.0)
                    videos = yt_page.evaluate("""() => {
                        return Array.from(document.querySelectorAll('ytd-video-renderer, ytd-rich-item-renderer')).map(el => {
                            const a = el.querySelector('a#video-title, a#video-title-link');
                            const ch = el.querySelector('ytd-channel-name a, #channel-info a');
                            const meta = el.querySelector('#metadata-line');
                            return {
                                title: a ? a.innerText.trim() : '',
                                url: a ? a.href : '',
                                channel: ch ? ch.innerText.trim() : '',
                                meta: meta ? meta.innerText.replace(/\\n/g, ' | ').trim() : ''
                            };
                        }).filter(v => v.title && v.url);
                    }""")
                    print(f"  -> {len(videos)} videos en YouTube para '{q}'")
                    for v in videos:
                        v["query"] = q
                        all_yt_found.append(v)
                except Exception as e:
                    print(f"Error en YouTube '{q}': {e}")

            if i < len(google_queries):
                gq = google_queries[i]
                g_url = f"https://www.google.com/search?q={urllib.parse.quote(gq)}&hl=es"
                print(f"[Pestaña Google/Foros] Buscando: {gq}")
                try:
                    web_page.bring_to_front()
                    web_page.goto(g_url, wait_until="domcontentloaded", timeout=30000)
                    time.sleep(2.0)
                    web_page.evaluate("window.scrollBy(0, 1200)")
                    time.sleep(1.2)
                    results = web_page.evaluate("""() => {
                        return Array.from(document.querySelectorAll('div.g, div[data-sokoban-container]')).map(el => {
                            const a = el.querySelector('a[href^="http"]');
                            const h3 = el.querySelector('h3');
                            return {
                                title: h3 ? h3.innerText.trim() : '',
                                url: a ? a.href : '',
                                snippet: el.innerText.trim().slice(0, 400)
                            };
                        }).filter(r => r.title && r.url);
                    }""")
                    print(f"  -> {len(results)} resultados en Google para '{gq}'")
                    for r in results:
                        r["query"] = gq
                        all_google_found.append(r)
                except Exception as e:
                    print(f"Error en Google '{gq}': {e}")

        (SOURCES_DIR / "youtube_visual_search_results.json").write_text(
            json.dumps(all_yt_found, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        (SOURCES_DIR / "google_visual_search_results.json").write_text(
            json.dumps(all_google_found, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        # Ahora recorremos visualmente sitios clave, foros y canales en ambas pestañas
        key_web_sites = [
            "https://campuslands.com/",
            "https://www.reddit.com/search/?q=campuslands",
            "https://github.com/search?q=campuslands&type=repositories",
            "https://www.vanguardia.com/busquedas/-/search/campuslands",
            "https://metropolitano.com.co/?s=campuslands"
        ]
        key_yt_pages = [
            "https://www.youtube.com/@Campuslands/videos",
            "https://www.youtube.com/watch?v=s8CMhCGFI6U",
            "https://www.youtube.com/watch?v=kANZD8FTN5Y",
            "https://www.youtube.com/watch?v=wuc9sv84B6o"
        ]

        for idx in range(max(len(key_web_sites), len(key_yt_pages))):
            if idx < len(key_web_sites):
                try:
                    web_page.bring_to_front()
                    web_page.goto(key_web_sites[idx], wait_until="domcontentloaded", timeout=30000)
                    time.sleep(2.5)
                    web_page.evaluate("window.scrollBy(0, 1200)")
                    time.sleep(1.5)
                except Exception as e:
                    print(f"Aviso visitando web {key_web_sites[idx]}: {e}")
            if idx < len(key_yt_pages):
                try:
                    yt_page.bring_to_front()
                    yt_page.goto(key_yt_pages[idx], wait_until="domcontentloaded", timeout=30000)
                    time.sleep(2.5)
                    yt_page.evaluate("window.scrollBy(0, 1200)")
                    time.sleep(1.5)
                except Exception as e:
                    print(f"Aviso visitando YT {key_yt_pages[idx]}: {e}")

        print("¡Recorrido visual completado!")

if __name__ == "__main__":
    main()
