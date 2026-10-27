import json
import time
from playwright.sync_api import sync_playwright

def search_profiles():
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = b.contexts[0]
        pages = [pg for pg in context.pages if "instagram.com" in pg.url]
        pg = pages[0]
        
        # Test direct URLs or search
        test_handles = ["diegotarazonap", "diegotarazonapinzon", "diegotarazona", "campuslands", "campuslandsoficial"]
        results = {}
        for handle in test_handles:
            url = f"https://www.instagram.com/{handle}/"
            pg.goto(url, wait_until="domcontentloaded", timeout=20000)
            time.sleep(2)
            title = pg.title()
            text = pg.inner_text("body")[:400].replace("\n", " ")
            exists = "Esta página no está disponible" not in text and "Sorry, this page isn't available" not in text and "Page Not Found" not in title
            results[handle] = {"url": url, "exists": exists, "title": title}
            print(f"Handle @{handle}: exists={exists} | title={title}")
        
        with open("diego_instagram/scripts/perfiles_encontrados.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

if __name__ == "__main__":
    search_profiles()
