import time
from pathlib import Path
from playwright.sync_api import sync_playwright

urls = [
    ("reddit_estafa", "https://www.reddit.com/r/bucaramanga/comments/1v037ud/campuslands_es_una_estafa_no_se_metan_all%C3%A1/"),
    ("reddit_campusland", "https://www.reddit.com/r/bucaramanga/comments/1bj3jrq/campusland/"),
    ("reddit_experiencia", "https://www.reddit.com/r/bucaramanga/comments/1om29x8/experiencia_con_campusland/")
]

def main():
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.new_page()
        for key, u in urls:
            print(f"Navegando a {key}: {u}...")
            try:
                page.goto(u, wait_until="domcontentloaded", timeout=30000)
                time.sleep(3.5)
                for _ in range(5):
                    page.evaluate("window.scrollBy(0, 1500)")
                    time.sleep(1.2)
                post_text = page.evaluate("() => document.body.innerText")
                out_txt = f"# HILO REDDIT: {u}\n\n{post_text}"
                Path(f"sources/prensa_y_web/foro_{key}.txt").write_text(out_txt, encoding="utf-8")
                print(f"OK: foro_{key}.txt guardado con éxito ({len(post_text)} caracteres).")
            except Exception as e:
                print(f"Error en {key}: {e}")
        page.close()

if __name__ == "__main__":
    main()
