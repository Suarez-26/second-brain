import json
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

out_dir = Path(r"c:\Users\tomas\second-brain\investigacion\campuslands\scripts")
candidates = json.loads((out_dir / "candidates_flat.json").read_text(encoding="utf-8"))

print("=== ITEMS 1 to 18 ===")
for i, c in enumerate(candidates[:18]):
    vid = c.get("id")
    title = c.get("title", "")
    channel = c.get("channel") or c.get("uploader") or ""
    dur = c.get("duration")
    src = c.get("source", "")
    print(f"[{i+1:03d}] {vid} | {channel[:28]:28s} | {str(dur):6s} | {title} ({src})")

def get_full_info(vid):
    cmd = [sys.executable, "-m", "yt_dlp", "--dump-json", "--no-warnings", "--skip-download", f"https://www.youtube.com/watch?v={vid}"]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    for line in res.stdout.splitlines():
        if line.strip():
            return json.loads(line)
    return {}

def get_flat_list(url):
    cmd = [sys.executable, "-m", "yt_dlp", "--dump-json", "--flat-playlist", "--no-warnings", url]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return [json.loads(line) for line in res.stdout.splitlines() if line.strip()]

seed_vids = ["w3l3AoGyhdk", "w0uOLg8jvNs", "FUnyFBcmTVk", "it8SPBH8cWo"]
for sv in seed_vids:
    info = get_full_info(sv)
    ch_url = info.get("channel_url") or info.get("uploader_url")
    ch_name = info.get("channel") or info.get("uploader")
    print(f"\nSeed {sv} -> Channel: {ch_name} ({ch_url})")
    if ch_url:
        for tab in ["/videos", "/shorts", "/streams"]:
            items = get_flat_list(ch_url + tab)
            if items:
                print(f"  {tab}: {len(items)} items")
                for it in items[:30]:
                    print(f"    - {it.get('id')} | {it.get('duration')}s | {it.get('title')}")
