import os
import re
import json
import urllib.request
import ssl
from concurrent.futures import ThreadPoolExecutor

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

OUT_DIR = r"c:\Users\tomas\second-brain\sources\prensa_y_web"

with open(os.path.join(OUT_DIR, "campuslands_site_dump.json"), "r", encoding="utf-8") as f:
    site_dump = json.load(f)

lines = []
lines.append("=== CAMPUSLANDS ROUTES ===")
for r, info in site_dump["routes"].items():
    lines.append(f"\n--- URL: {r} | Status: {info['status']} | Len: {info['raw_len']} ---")
    lines.append(info["clean_text"])

lines.append("\n=== CAMPUSLANDS CHUNKS FINDINGS ===")
all_matches = set()
all_strings = set()
for c in site_dump["chunks"]:
    all_matches.update(c["matches"])
    all_strings.update(c["strings"])

lines.append("Matches: " + json.dumps(sorted(all_matches), ensure_ascii=False))
lines.append("\nStrings:")
for s in sorted(all_strings):
    lines.append(" - " + s)

with open(os.path.join(OUT_DIR, "github_campuslands.json"), "r", encoding="utf-8") as f:
    gh_dump = json.load(f)

lines.append("\n=== GITHUB USERS/ORGS ===")
users_ep = "https://api.github.com/search/users?q=campuslands&per_page=50"
if users_ep in gh_dump:
    lines.append(f"Total users/orgs: {gh_dump[users_ep].get('total_count')}")
    for u in gh_dump[users_ep].get("items", []):
        lines.append(f" - {u['login']} ({u['type']}): {u['html_url']}")

lines.append("\n=== GITHUB REPOS ===")
for ep, data in gh_dump.items():
    if "repositories" in ep:
        lines.append(f"Endpoint: {ep} | Total: {data.get('total_count')}")
        for repo in data.get("items", [])[:60]:
            lines.append(f" - {repo['full_name']} | Stars: {repo['stargazers_count']} | Desc: {repo['description']} | Created: {repo['created_at']} | URL: {repo['html_url']}")

step19 = r"C:\Users\tomas\.gemini\antigravity\brain\d625c55b-4874-406e-a291-4a5db5402bdb\.system_generated\steps\19\content.md"
if os.path.exists(step19):
    with open(step19, "r", encoding="utf-8", errors="replace") as f:
        raw19 = f.read()
    paras = re.findall(r"<p[^>]*>(.*?)</p>", raw19, flags=re.DOTALL | re.IGNORECASE)
    lines.append("\n=== COMPITE PARAGRAPHS ===")
    for p in paras:
        clean_p = re.sub(r"<[^>]+>", " ", p).strip()
        if len(clean_p) > 20:
            lines.append("P: " + clean_p)

with open(os.path.join(OUT_DIR, "summary_dump_utf8.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("Wrote summary_dump_utf8.txt successfully, total lines:", len(lines))
