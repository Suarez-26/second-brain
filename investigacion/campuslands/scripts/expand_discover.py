import json
import subprocess
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

out_dir = Path(r"c:\Users\tomas\second-brain\investigacion\campuslands\scripts")
candidates_file = out_dir / "candidates_flat.json"
candidates = {c["id"]: c for c in json.loads(candidates_file.read_text(encoding="utf-8"))}

EXTRA_QUERIES = [
    "ytsearch30:\"Diego Tarazon\"",
    "ytsearch30:Campuslands Canal TRO",
    "ytsearch30:Campuslands Santander",
    "ytsearch30:Campuslands becas",
    "ytsearch30:Campuslands graduación",
    "ytsearch30:Campuslands inteligencia artificial",
    "ytsearch30:Campuslands empleo",
    "ytsearch30:Campuslands programación",
    "ytsearch30:Campuslands Floridablanca",
    "ytsearch30:Campuslands San Gil",
    "ytsearch30:Campuslands Barranquilla",
    "ytsearch30:Campuslands Medellín",
    "ytsearch30:Campuslands Cali",
]

def run_ytdlp_flat(target):
    cmd = [sys.executable, "-m", "yt_dlp", "--dump-json", "--flat-playlist", "--no-warnings", target]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    items = []
    for line in res.stdout.splitlines():
        if line.strip():
            try:
                items.append(json.loads(line))
            except Exception:
                pass
    return items

def get_full_info(vid):
    cmd = [sys.executable, "-m", "yt_dlp", "--dump-json", "--no-warnings", "--skip-download", f"https://www.youtube.com/watch?v={vid}"]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    for line in res.stdout.splitlines():
        if line.strip():
            try:
                return json.loads(line)
            except Exception:
                pass
    return {}

# Check channel of mkjAgWwwQqw and ygRCAJzb2GI
for sv in ["mkjAgWwwQqw", "ygRCAJzb2GI"]:
    info = get_full_info(sv)
    ch_url = info.get("channel_url") or info.get("uploader_url")
    print(f"Seed {sv} -> {info.get('channel')} ({ch_url})")
    if ch_url:
        for tab in ["/videos", "/shorts", "/streams"]:
            for it in run_ytdlp_flat(ch_url + tab):
                vid = it.get("id")
                if vid and len(vid) == 11 and vid not in candidates:
                    it["source"] = f"channel:{ch_url}{tab}"
                    candidates[vid] = it
                    print(f"  + Added from channel: {vid} | {it.get('title')}")

# Also add all items from Campuslands AI Academy (UCMwqEVEZjwDrBTtiqu94fkw) and playlist PLzATz09RoEBR5T-jF4jaYrsgNEc9qK6fv
for url in [
    "https://www.youtube.com/channel/UCMwqEVEZjwDrBTtiqu94fkw/videos",
    "https://www.youtube.com/channel/UCMwqEVEZjwDrBTtiqu94fkw/streams",
    "https://www.youtube.com/channel/UCMwqEVEZjwDrBTtiqu94fkw/shorts",
    "https://www.youtube.com/playlist?list=PLzATz09RoEBR5T-jF4jaYrsgNEc9qK6fv",
    "https://www.youtube.com/playlist?list=PLzATz09RoEBRipmYhNP0CsudJ4VvxShOE",
]:
    for it in run_ytdlp_flat(url):
        vid = it.get("id")
        if vid and len(vid) == 11 and vid not in candidates:
            it["source"] = f"channel:{url}"
            candidates[vid] = it
            print(f"  + Added from {url}: {vid} | {it.get('title')}")

with ThreadPoolExecutor(max_workers=6) as ex:
    futs = {ex.submit(run_ytdlp_flat, q): q for q in EXTRA_QUERIES}
    for fut in as_completed(futs):
        q = futs[fut]
        items = fut.result()
        new_cnt = 0
        for it in items:
            vid = it.get("id")
            if vid and len(vid) == 11 and vid not in candidates:
                it["source"] = q
                candidates[vid] = it
                new_cnt += 1
                print(f"  + [{q}] {vid} | {it.get('channel') or it.get('uploader')} | {it.get('title')}")

candidates_file.write_text(json.dumps(list(candidates.values()), ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Total candidates now: {len(candidates)}")
