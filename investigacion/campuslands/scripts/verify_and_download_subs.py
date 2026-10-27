import json
import subprocess
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

out_dir = Path(r"c:\Users\tomas\second-brain\investigacion\campuslands\scripts")
subs_dir = out_dir / "subs"
subs_dir.mkdir(parents=True, exist_ok=True)

meta_path = out_dir / "filtered_full_metadata.json"
meta = json.loads(meta_path.read_text(encoding="utf-8"))

# First fetch x_52MJVLKBs
def fetch_one(vid):
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--js-runtimes", "node",
        "--extractor-args", "youtube:player_client=android_vr,ios,android,mweb;player_skip=webpage",
        "--dump-json", "--no-warnings", "--skip-download",
        f"https://www.youtube.com/watch?v={vid}"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    for line in res.stdout.splitlines():
        if line.strip():
            try:
                return json.loads(line)
            except Exception:
                pass
    return None

if "x_52MJVLKBs" not in meta or "error" in meta["x_52MJVLKBs"]:
    d = fetch_one("x_52MJVLKBs")
    if d:
        meta["x_52MJVLKBs"] = {
            "id": "x_52MJVLKBs",
            "title": d.get("title"),
            "channel": d.get("channel") or d.get("uploader"),
            "channel_id": d.get("channel_id"),
            "channel_url": d.get("channel_url") or d.get("uploader_url"),
            "upload_date": d.get("upload_date"),
            "duration": d.get("duration"),
            "duration_string": d.get("duration_string"),
            "view_count": d.get("view_count"),
            "like_count": d.get("like_count"),
            "description": d.get("description", ""),
            "tags": d.get("tags", []),
            "categories": d.get("categories", []),
            "subtitles": list((d.get("subtitles") or {}).keys()),
            "automatic_captions": list((d.get("automatic_captions") or {}).keys()),
            "webpage_url": d.get("webpage_url") or "https://www.youtube.com/watch?v=x_52MJVLKBs",
            "source": "channel:ET_CAMPUSLANDS",
            "in_existing_19": False,
        }
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

EXISTING_19 = {
    "F-AvmYM2k8k", "s8CMhCGFI6U", "kANZD8FTN5Y", "uArGKWxb0jU",
    "wuc9sv84B6o", "ZjS85xqQSn4", "KEbYZ0X7Aec", "I-3waHqlUPk",
    "Oc1K_vHu3Uc", "fH8WmSSFjEs", "f_DFCoVgYV0", "Bc7kNy7yuvc",
    "4LkwD59y_Vs", "NxyrHzFu5oU", "MByGeiB1y2Y", "zVj6Nezq7u0",
    "xc1YnHqihrw", "AnWiyruHz1I", "Ns7T2mGXx-A"
}

EXCLUDE_FALSE_POSITIVES = {
    "l5c4bo1N2Nk", "ZKqJ__wwhWA", "KHysGFdWdUc", "AYIqbjsdpiQ",
    "uxAo6E2V2mQ", "I6w6KM9ESLg", "wQ-zli363Kc", "T5ex5NquvPs",
    "whdLfVc2yHU", "EmBav-64rpw", "s30NMirXmRo",
    "N4p4Ee5CGmY", "lzysbZ9xlrU", "7XzhMm4h0Mw", "b4kA6xgAtc4",
    "urfdF1jkzZk", "0mtOQ3wIFBg", "V9aUR9_QXnI", "WMlmFilafUA",
    "tEpFyMpQ5u0", "Bf1nEucnDc4", "Bng8FhkUrNs", "lIFVIL_Vhro",
    "FfnsjPXWAGw", "pDBSggZYqGY", "dfpT2MEfZ2w", "g1sHhNGQxjA",
    "94xN1yVCesA", "FvlEu4WZz7k", "RvXxjgnw_pk"
}

targets = []
for vid, d in meta.items():
    if "error" in d or vid in EXISTING_19 or vid in EXCLUDE_FALSE_POSITIVES:
        continue
    targets.append(d)

print(f"Total target videos for subtitle extraction: {len(targets)}")
(out_dir / "final_targets.json").write_text(json.dumps(targets, ensure_ascii=False, indent=2), encoding="utf-8")

def download_sub(d):
    vid = d["id"]
    # Check if already downloaded
    existing = list(subs_dir.glob(f"{vid}.*"))
    if existing:
        return vid, "cached", [p.name for p in existing]

    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--js-runtimes", "node",
        "--extractor-args", "youtube:player_client=android_vr,ios,android,mweb;player_skip=webpage",
        "--write-sub", "--write-auto-sub",
        "--sub-lang", "es.*,es,en.*,en",
        "--sub-format", "json3/vtt",
        "--skip-download",
        "--no-warnings",
        "-o", str(subs_dir / "%(id)s.%(ext)s"),
        f"https://www.youtube.com/watch?v={vid}"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    files = list(subs_dir.glob(f"{vid}.*"))
    if files:
        return vid, "ok", [p.name for p in files]
    return vid, "no_subs", res.stderr.strip()[:200]

with ThreadPoolExecutor(max_workers=4) as ex:
    futs = {ex.submit(download_sub, d): d for d in targets}
    for fut in as_completed(futs):
        d = futs[fut]
        vid, status, info = fut.result()
        print(f"[{status:7s}] {vid} | {d.get('title')[:55]:55s} | {info}")
