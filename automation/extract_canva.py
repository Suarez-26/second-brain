import os
import json
import time
from playwright.sync_api import sync_playwright

url = "https://www.canva.com/design/DAHJLknEvYM/d_RNv87C_CM_gVPIPvENcg/view"
out_dir = "presentaciones/canva_slides"
os.makedirs(out_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome", headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    print("Navegando a Canva...")
    page.goto(url, wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(5000)

    try:
        page.get_by_text("Aceptar todas las cookies").click(timeout=3000)
    except Exception:
        pass

    # Tomar captura inicial
    page.screenshot(path=os.path.join(out_dir, "slide_01.png"))

    # Intentar buscar elementos de diapositiva o desplazarse
    # Canva en view suele tener flechas de navegación o scroll
    # Revisemos botones de siguiente página o navegación
    buttons = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('button')).map(b => ({
            aria: b.getAttribute('aria-label'),
            text: b.innerText,
            classes: b.className
        }));
    }""")
    print("Botones encontrados:", len(buttons))

    # Scroll para cargar todo
    for i in range(12):
        page.mouse.wheel(0, 1080)
        page.wait_for_timeout(1000)
        page.screenshot(path=os.path.join(out_dir, f"scroll_{i+1:02d}.png"))

    # Extraer texto completo estructurado
    elements = page.evaluate("""() => {
        const results = [];
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        let node;
        while (node = walker.nextNode()) {
            const val = node.nodeValue.trim();
            if (val.length > 0 && !val.includes('cookies') && !val.includes('Canva')) {
                results.push(val);
            }
        }
        return results;
    }""")

    with open(os.path.join(out_dir, "textos_crudos.json"), "w", encoding="utf-8") as f:
        json.dump(elements, f, ensure_ascii=False, indent=2)

    print(f"Extracción completada. Textos extraídos: {len(elements)}")
    browser.close()
