import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

def get_posts_list():
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        pg = [x for x in b.contexts[0].pages if "instagram.com" in x.url][0]
        
        pg.goto("https://www.instagram.com/diegotarazonap/", wait_until="domcontentloaded", timeout=20000)
        pg.wait_for_timeout(3000)
        
        # Scroll once or twice to ensure all 26 posts are loaded
        for _ in range(4):
            pg.evaluate("window.scrollBy(0, 1500)")
            pg.wait_for_timeout(1500)
            
        post_links = pg.evaluate('''() => {
            const anchors = Array.from(document.querySelectorAll('a[href*="/p/"], a[href*="/reel/"]'));
            const set = new Set();
            return anchors.map(a => a.href).filter(href => {
                const clean = href.split('?')[0];
                if (set.has(clean)) return false;
                set.add(clean);
                return true;
            });
        }''')
        
        print(f"Total publicaciones/reels detectados en @diegotarazonap: {len(post_links)}")
        for i, link in enumerate(post_links):
            print(f"[{i+1:02d}] {link}")

if __name__ == "__main__":
    get_posts_list()
