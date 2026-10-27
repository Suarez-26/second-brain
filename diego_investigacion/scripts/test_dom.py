import json
import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

with sync_playwright() as p:
    b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    pg = [x for x in b.contexts[0].pages if "linkedin.com" in x.url][0]
    info = pg.evaluate("""
    () => {
        const m = document.querySelector('main');
        const h2s = Array.from(m.querySelectorAll('h2, h3')).map(h => ({tag: h.tagName, text: h.innerText.trim(), parentRole: h.parentElement ? h.parentElement.getAttribute('role') : '', gpRole: h.parentElement && h.parentElement.parentElement ? h.parentElement.parentElement.getAttribute('role') : ''}));
        const ckeys = Array.from(m.querySelectorAll('[componentkey]')).map(el => ({tag: el.tagName, role: el.getAttribute('role'), ckey: el.getAttribute('componentkey').slice(0, 50), len: (el.innerText||'').length})).filter(x => x.len > 150);
        return { h2s: h2s.slice(0, 30), ckeys: ckeys.slice(0, 30) };
    }
    """)
    print(json.dumps(info, ensure_ascii=False, indent=2))
