import sys
import io
from playwright.sync_api import sync_playwright

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

def inspect_bios():
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        pg = [x for x in b.contexts[0].pages if "instagram.com" in x.url][0]
        
        output = []
        for h in ["diegotarazonap", "diegotarazona", "campuslands"]:
            pg.goto(f"https://www.instagram.com/{h}/", wait_until="domcontentloaded", timeout=20000)
            pg.wait_for_timeout(2500)
            header_text = pg.evaluate('''() => {
                const header = document.querySelector('header');
                return header ? header.innerText : document.body.innerText.slice(0, 500);
            }''')
            output.append(f"=== PERFIL @{h} ===\n{header_text}\n" + "-" * 50)
        
        with open("diego_instagram/scripts/bios_info.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(output))
        print("Bios guardadas en diego_instagram/scripts/bios_info.txt")

if __name__ == "__main__":
    inspect_bios()
