import json
import subprocess
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

out_dir = Path(r"c:\Users\tomas\second-brain\investigacion\campuslands\scripts")
meta_path = out_dir / "filtered_full_metadata.json"
meta = json.loads(meta_path.read_text(encoding="utf-8"))

RETRY_IDS = [
    "ygRCAJzb2GI", "2MH_5XVGlkQ", "zyTZIrwROyQ", "RAA9F_2uxyo",
    "KXCFpHBgaWA", "OKMsheDmK8Q", "9c-LnWdswd4", "tt_90kYch38",
    "G90ewgq_6W4", "au6BKD6uDUk", "QGi7-WeEgmc", "On31AKplUKg",
    "aTlX8jSbIP0", "OooT4eKWZt8", "VV_5JIUofXw", "mkjAgWwwQqw",
    "it8SPBH8cWo", "lcQJwzLtajU", "na4wZjMu74Q", "DTQWVBdoC4U",
    "Al0cJzeSpQI", "fwUZIkS8t7Y", "EUdSaX8-DC0", "RvXxjgnw_pk",
    "FfnsjPXWAGw", "eNwU7Kd1hiY", "MByGeiB1y2Y", "xc1YnHqihrw",
    "mYVvyQZ5DFY", "MmNt6CZJuMg", "_OwwNPxhJlU", "HCU4_4m4nwU",
    "wv_FObQKan0", "OKOpMOqt0Vs", "iUSNGjPNWN0", "vGpTPzcVtoo",
    "mOWFj0N5Z_s"
]

def fetch_one(vid):
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--extractor-args", "youtube:player_client=tv,android_vr,mweb",
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
    return {"id": vid, "error": res.stderr.strip()[:300]}

with ThreadPoolExecutor(max_workers=4) as ex:
    futs = {ex.submit(fetch_one, vid): vid for vid in RETRY_IDS}
    for fut in as_completed(futs):
        vid = futs[fut]
        data = fut.result()
        if "error" in data and not data.get("title"):
            print(f"[STILL ERR] {vid}: {data['error'][:120]}")
        else:
            meta[vid] = {
                "id": vid,
                "title": data.get("title"),
                "channel": data.get("channel") or data.get("uploader"),
                "channel_id": data.get("channel_id"),
                "channel_url": data.get("channel_url") or data.get("uploader_url"),
                "upload_date": data.get("upload_date"),
                "duration": data.get("duration"),
                "duration_string": data.get("duration_string"),
                "view_count": data.get("view_count"),
                "like_count": data.get("like_count"),
                "description": data.get("description", ""),
                "tags": data.get("tags", []),
                "categories": data.get("categories", []),
                "subtitles": list((data.get("subtitles") or {}).keys()),
                "automatic_captions": list((data.get("automatic_captions") or {}).keys()),
                "webpage_url": data.get("webpage_url") or f"https://www.youtube.com/watch?v={vid}",
                "source": meta.get(vid, {}).get("source", "retry"),
                "in_existing_19": vid in {"MByGeiB1y2Y", "xc1YnHqihrw"},
            }
            print(f"[RECOVERED] {vid} | {meta[vid]['upload_date']} | {meta[vid]['channel']} | {meta[vid]['title']}")

meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
