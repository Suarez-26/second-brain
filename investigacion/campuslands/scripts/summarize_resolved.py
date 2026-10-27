import os
import re
import json

OUT_DIR = r"c:\Users\tomas\second-brain\sources\prensa_y_web"

with open(os.path.join(OUT_DIR, "resolved_articles_index.json"), "r", encoding="utf-8") as f:
    resolved = json.load(f)

report = []
report.append("=== RESOLVED URLS SUMMARY ===")
for item in resolved:
    report.append(f"\n[{item['key']}] Status: {item.get('status')} | Len: {item.get('len', 0)} | Error: {item.get('error', '')}")
    report.append(f"Final URL: {item.get('final_url')}")
    if item.get("snippet"):
        report.append(f"Snippet: {item['snippet'][:800]}")

with open(os.path.join(OUT_DIR, "reddit_resolved_threads.json"), "r", encoding="utf-8") as f:
    reddit = json.load(f)

report.append("\n\n=== REDDIT RESOLVED THREADS ===")
for ru, rdata in reddit.items():
    report.append(f"\nThread URL: {ru}")
    if "error" in rdata:
        report.append(f"Error: {rdata['error']}")
    else:
        report.append(f"Title: {rdata.get('title')} | Subreddit: {rdata.get('subreddit')} | Author: {rdata.get('author')} | Score: {rdata.get('score')} | Created: {rdata.get('created_utc')}")
        report.append(f"Selftext: {rdata.get('selftext')}")
        report.append(f"Comments ({len(rdata.get('comments', []))}):")
        for c in rdata.get("comments", []):
            report.append(f"  - [{c.get('author')} | score:{c.get('score')}]: {c.get('body')}")

# Also search step19 for "Campuslands"
step19 = r"C:\Users\tomas\.gemini\antigravity\brain\d625c55b-4874-406e-a291-4a5db5402bdb\.system_generated\steps\19\content.md"
if os.path.exists(step19):
    with open(step19, "r", encoding="utf-8", errors="replace") as f:
        raw19 = f.read()
    report.append("\n\n=== COMPITE MATCHES FOR CAMPUSLANDS ===")
    for m in re.finditer(r".{0,300}Campuslands.{0,600}", raw19, flags=re.IGNORECASE):
        clean_m = re.sub(r"<[^>]+>", " ", m.group(0))
        clean_m = re.sub(r"\s+", " ", clean_m).strip()
        report.append("Match: " + clean_m)

with open(os.path.join(OUT_DIR, "resolved_summary_utf8.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(report))

print("Wrote resolved_summary_utf8.txt, lines:", len(report))
