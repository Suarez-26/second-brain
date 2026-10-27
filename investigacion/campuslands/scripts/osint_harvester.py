import os
import re
import json
import urllib.request
import urllib.parse
import ssl
from concurrent.futures import ThreadPoolExecutor

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,application/json,*/*;q=0.8",
    "Accept-Language": "es-CO,es;q=0.9,en;q=0.8"
}

OUT_DIR = r"c:\Users\tomas\second-brain\sources\prensa_y_web"
os.makedirs(OUT_DIR, exist_ok=True)

def fetch_url(url, timeout=15):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            final_url = resp.geturl()
            raw = resp.read()
            text = raw.decode("utf-8", errors="replace")
            return {"url": url, "final_url": final_url, "status": resp.status, "text": text}
    except Exception as e:
        return {"url": url, "final_url": url, "status": 0, "error": str(e), "text": ""}

def clean_html(html):
    # Remove scripts and styles for readable text
    t = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.DOTALL | re.IGNORECASE)
    t = re.sub(r"<style[^>]*>.*?</style>", " ", t, flags=re.DOTALL | re.IGNORECASE)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

# 1. Crawl campuslands.com pages and JS chunks
campus_routes = [
    "https://campuslands.com/",
    "https://campuslands.com/camper",
    "https://campuslands.com/nosotros",
    "https://campuslands.com/privacidad",
    "https://campuslands.com/terminos",
    "https://campuslands.com/servicios/ia-academy",
    "https://campuslands.com/servicios/staffing",
    "https://campuslands.com/servicios/emplea",
    "https://campuslands.com/servicios/fullservice",
    "https://campuslands.com/servicios/internacional",
    "https://campuslands.com/robots.txt",
    "https://campuslands.com/sitemap.xml",
    "https://camper.campuslands.com/login"
]

print("--- Fetching campuslands.com routes ---")
campus_data = {}
js_chunks = set()
for r in campus_routes:
    res = fetch_url(r)
    campus_data[r] = {
        "final_url": res["final_url"],
        "status": res["status"],
        "clean_text": clean_html(res["text"])[:20000],
        "raw_len": len(res["text"])
    }
    # Extract _next/static/chunks/*.js
    for m in re.findall(r"/_next/static/chunks/[^\"'\s]+\.js", res["text"]):
        js_chunks.add("https://campuslands.com" + m)
    # Save raw html
    slug = re.sub(r"[^a-zA-Z0-9_-]", "_", r.replace("https://", ""))
    with open(os.path.join(OUT_DIR, f"campus_{slug}.html"), "w", encoding="utf-8") as f:
        f.write(res["text"])

print(f"Found {len(js_chunks)} JS chunks on campuslands.com")
chunk_Creation_findings = []
for jc in sorted(js_chunks):
    res = fetch_url(jc)
    txt = res["text"]
    # Look for strings of interest in chunks: NIT, emails, phone numbers, addresses, URLs, numbers
    interesting = re.findall(r"(?:901[\.\d-]+|[a-zA-Z0-9_.+-]+@campuslands\.com|Zona Franca|Guatemala|Bogot[áa]|Medell[íi]n|Cali|Tibu|C[úu]cuta|camper\.campuslands|https?://[^\s\"'`<>]+)", txt, flags=re.IGNORECASE)
    # Also extract long Spanish text literals
    spanish_strings = re.findall(r'["\']([^"\']{40,500})["\']', txt)
    filtered_str = [s for s in spanish_strings if not s.startswith("http") and not "function" in s and not "className" in s and not "M0 " in s and any(w in s.lower() for w in ["campus", "talento", "sede", "nit", "carrera", "anillo", "zona", "horas", "meses", "empresas", "graduados", "camper", "colombia", "guatemala", "méxico", "bogotá", "bucaramanga", "floridablanca", "datos", "privacidad", "legal", "sociedad", "bic"])]
    if interesting or filtered_str:
        chunk_Creation_findings.append({
            "chunk": jc,
            "matches": list(set(interesting))[:100],
            "strings": list(set(filtered_str))[:150]
        })

with open(os.path.join(OUT_DIR, "campuslands_site_dump.json"), "w", encoding="utf-8") as f:
    json.dump({"routes": campus_data, "chunks": chunk_Creation_findings}, f, ensure_ascii=False, indent=2)

# 2. Reddit Search & Thread Downloader
print("--- Searching Reddit ---")
reddit_queries = [
    "campuslands",
    "\"campus programmers\"",
    "\"diego tarazona\""
]
reddit_threads = {}
for q in reddit_queries:
    u = f"https://www.reddit.com/search.json?q={urllib.parse.quote(q)}&limit=50&sort=relevance"
    res = fetch_url(u)
    if res["status"] == 200 and res["text"]:
        try:
            data = json.loads(res["text"])
            for child in data.get("data", {}).get("children", []):
                post = child.get("data", {})
                permalink = post.get("permalink")
                if permalink and permalink not in reddit_threads:
                    reddit_threads[permalink] = {
                        "title": post.get("title"),
                        "subreddit": post.get("subreddit_name_prefixed"),
                        "author": post.get("author"),
                        "created_utc": post.get("created_utc"),
                        "score": post.get("score"),
                        "num_comments": post.get("num_comments"),
                        "selftext": post.get("selftext"),
                        "url": "https://www.reddit.com" + permalink,
                        "comments": []
                    }
        except Exception as e:
            print("Reddit parse err:", e)

for permalink in list(reddit_threads.keys()):
    u = f"https://www.reddit.com{permalink}.json?limit=200"
    res = fetch_url(u)
    if res["status"] == 200 and res["text"]:
        try:
            tdata = json.loads(res["text"])
            if isinstance(tdata, list) and len(tdata) > 1:
                def extract_comments(children):
                    out = []
                    for c in children:
                        cd = c.get("data", {})
                        if cd.get("body"):
                            out.append({
                                "author": cd.get("author"),
                                "score": cd.get("score"),
                                "created_utc": cd.get("created_utc"),
                                "body": cd.get("body")
                            })
                        replies = cd.get("replies")
                        if isinstance(replies, dict):
                            out.extend(extract_comments(replies.get("data", {}).get("children", [])))
                    return out
                reddit_threads[permalink]["comments"] = extract_comments(tdata[1].get("data", {}).get("children", []))
        except Exception as e:
            print("Reddit thread err:", e)

with open(os.path.join(OUT_DIR, "reddit_campuslands.json"), "w", encoding="utf-8") as f:
    json.dump(reddit_threads, f, ensure_ascii=False, indent=2)
print(f"Saved {len(reddit_threads)} Reddit threads")

# 3. GitHub API Search
print("--- Searching GitHub ---")
gh_results = {}
for ep in [
    "https://api.github.com/search/users?q=campuslands&per_page=50",
    "https://api.github.com/search/repositories?q=campuslands&sort=stars&per_page=100",
    "https://api.github.com/search/repositories?q=%22campus+programmers%22&per_page=50"
]:
    res = fetch_url(ep)
    if res["status"] == 200:
        try:
            gh_results[ep] = json.loads(res["text"])
        except Exception:
            pass

with open(os.path.join(OUT_DIR, "github_campuslands.json"), "w", encoding="utf-8") as f:
    json.dump(gh_results, f, ensure_ascii=False, indent=2)
print("Saved GitHub search results")
