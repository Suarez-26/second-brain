import json
import subprocess
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

EXISTING_IDS = {
    "F-AvmYM2k8k", "s8CMhCGFI6U", "kANZD8FTN5Y", "uArGKWxb0jU",
    "wuc9sv84B6o", "ZjS85xqQSn4", "KEbYZ0X7Aec", "I-3waHqlUPk",
    "Oc1K_vHu3Uc", "fH8WmSSFjEs", "f_DFCoVgYV0", "Bc7kNy7yuvc",
    "4LkwD59y_Vs", "NxyrHzFu5oU", "MByGeiB1y2Y", "zVj6Nezq7u0",
    "xc1YnHqihrw", "AnWiyruHz1I", "Ns7T2mGXx-A"
}

EXPLICIT_IDS = [
    "zGi65oaB9dA", "PasWbp5FGbE", "8l31wVP6C2M", "3av_YtMXvbc",
    "k8-ByiClnq8", "fs2isMnSQ0o", "bfdR98QqbIs", "mOWFj0N5Z_s",
    "s8CMhCGFI6U"
]

QUERIES = [
    "ytsearch80:Campuslands",
    "ytsearch40:\"Campus Programmers Land\"",
    "ytsearch50:\"Diego Tarazona\"",
    "ytsearch40:\"Diego Tarazona\" Campuslands",
    "ytsearch40:\"The Human Code\" Campuslands",
    "ytsearch30:Campuslands Bucaramanga",
    "ytsearch30:Campuslands Guatemala",
    "ytsearch30:Campuslands Tibú",
    "ytsearch30:Campuslands Bogotá",
    "ytsearch30:Campuslands Fedesoft",
    "ytsearch30:Campuslands MinTIC",
    "ytsearch30:Campuslands Zona Franca",
    "ytsearch30:Campuslands Premios Ingenio",
    "ytsearch30:Campuslands SOFTIC",
    "ytsearch30:Campuslands CENS",
    "ytsearch30:Campuslands Cámara de Comercio",
    "ytsearch30:Campuslands UNAB",
    "ytsearch30:Campuslands UDI",
    "ytsearch30:Campuslands UTS",
    "ytsearch30:Campuslands UIS",
    "ytsearch30:Campuslands Cajasan",
    "ytsearch30:Campuslands Ecopetrol",
    "ytsearch30:\"Campus Land\" programación",
    "ytsearch30:\"Diego Fernando Tarazona\"",
    "ytsearch30:Campuslands podcast",
    "ytsearch30:Campuslands entrevista",
    "ytsearch30:Campuslands campers",
]

def run_ytdlp_flat(target):
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--dump-json", "--flat-playlist", "--no-warnings",
        target
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    items = []
    for line in res.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            items.append(json.loads(line))
        except Exception:
            pass
    return items

def run_ytdlp_full(video_id):
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--dump-json", "--no-warnings", "--skip-download",
        f"https://www.youtube.com/watch?v={video_id}"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    for line in res.stdout.splitlines():
        line = line.strip()
        if line:
            try:
                return json.loads(line)
            except Exception:
                pass
    return None

def main():
    out_dir = Path(r"c:\Users\tomas\second-brain\investigacion\campuslands\scripts")
    out_dir.mkdir(parents=True, exist_ok=True)

    print("1. Inspecting explicit IDs and finding official Campuslands channel...")
    info_s8 = run_ytdlp_full("s8CMhCGFI6U")
    channels_to_scrape = set()
    if info_s8:
        ch_url = info_s8.get("channel_url") or info_s8.get("uploader_url")
        print(f"Found Campuslands channel from s8CMhCGFI6U: {info_s8.get('channel')} -> {ch_url}")
        if ch_url:
            channels_to_scrape.add(ch_url + "/videos")
            channels_to_scrape.add(ch_url + "/shorts")
            channels_to_scrape.add(ch_url + "/streams")
            channels_to_scrape.add(ch_url + "/podcasts")

    all_flat = {}
    for vid in EXPLICIT_IDS:
        all_flat[vid] = {"id": vid, "source": "explicit"}

    # Scrape official channel tabs
    for ch_tab in channels_to_scrape:
        print(f"Scraping channel tab: {ch_tab}")
        items = run_ytdlp_flat(ch_tab)
        print(f"  -> {len(items)} items from {ch_tab}")
        for it in items:
            vid = it.get("id")
            if vid and len(vid) == 11:
                it["source"] = f"channel:{ch_tab}"
                all_flat[vid] = it

    # Run all search queries in parallel
    print(f"2. Running {len(QUERIES)} search queries in parallel...")
    with ThreadPoolExecutor(max_workers=6) as ex:
        future_to_q = {ex.submit(run_ytdlp_flat, q): q for q in QUERIES}
        for fut in as_completed(future_to_q):
            q = future_to_q[fut]
            try:
                items = fut.result()
                print(f"  Query '{q}' returned {len(items)} results")
                for it in items:
                    vid = it.get("id")
                    if vid and len(vid) == 11 and vid not in all_flat:
                        it["source"] = q
                        all_flat[vid] = it
            except Exception as e:
                print(f"  Query '{q}' failed: {e}")

    print(f"Total unique candidate video IDs found: {len(all_flat)}")
    raw_file = out_dir / "candidates_flat.json"
    raw_file.write_text(json.dumps(list(all_flat.values()), ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved flat candidates to {raw_file}")

if __name__ == "__main__":
    main()
