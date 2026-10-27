import sys
from playwright.sync_api import sync_playwright

def check():
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = b.contexts[0]
        pages = [pg for pg in context.pages if "instagram.com" in pg.url]
        if not pages:
            print("No se encontro pestaña de Instagram")
            return
        pg = pages[0]
        print("URL actual:", pg.url)
        print("Titulo:", pg.title())
        
        # Test search or user profile
        links = pg.evaluate('''() => {
            return Array.from(document.querySelectorAll('a[href]')).map(a => a.getAttribute('href')).slice(0, 30);
        }''')
        print("Enlaces encontrados en la barra/feed:")
        for l in links[:10]:
            print(" -", l)

if __name__ == "__main__":
    check()
