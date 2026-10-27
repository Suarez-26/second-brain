import json
import subprocess
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

out_dir = Path(r"c:\Users\tomas\second-brain\investigacion\campuslands\scripts")
candidates = json.loads((out_dir / "candidates_flat.json").read_text(encoding="utf-8"))

EXISTING_19 = {
    "F-AvmYM2k8k", "s8CMhCGFI6U", "kANZD8FTN5Y", "uArGKWxb0jU",
    "wuc9sv84B6o", "ZjS85xqQSn4", "KEbYZ0X7Aec", "I-3waHqlUPk",
    "Oc1K_vHu3Uc", "fH8WmSSFjEs", "f_DFCoVgYV0", "Bc7kNy7yuvc",
    "4LkwD59y_Vs", "NxyrHzFu5oU", "MByGeiB1y2Y", "zVj6Nezq7u0",
    "xc1YnHqihrw", "AnWiyruHz1I", "Ns7T2mGXx-A"
}

EXPLICIT_KEEP = {
    "zGi65oaB9dA", "PasWbp5FGbE", "8l31wVP6C2M", "3av_YtMXvbc",
    "k8-ByiClnq8", "fs2isMnSQ0o", "bfdR98QqbIs", "mOWFj0N5Z_s",
    "ygRCAJzb2GI", "n4lp2MQMEwQ", "30GuYjIjUhY", "JBA1gdRs8DI",
    "Hj-ApbBtb6Y", "AAAwSmenc20", "eRy285TpfvI", "koi_Rm-E3Lw",
    "i0BMIxyM46w", "ZtHMUxd9XSw"
}

# Pre-filter obvious unrelated videos from flat list
BAD_CHANNELS = {
    "Campusland Oberösterreich", "Diego Tarazona R", "diego fernando tarazona chaparro",
    "Free Audiobook", "Zika Dialogues", "KPIX | CBS NEWS BAY AREA", "BildungsTV",
    "Club Campusland", "Florida State University Panama City", "UH West O‘ahu",
}

def is_candidate_worth_checking(c):
    vid = c.get("id")
    if vid in EXISTING_19 or vid in EXPLICIT_KEEP:
        return True
    ch = (c.get("channel") or c.get("uploader") or "").strip()
    title = (c.get("title") or "").strip()
    tl = title.lower()
    chl = ch.lower()

    if ch in BAD_CHANNELS:
        return False
    if "scott johnston" in tl or "oberösterreich" in tl or "campusland oö" in tl:
        return False
    if "diego tarazona r" in chl or "diego fernando tarazona chap" in chl:
        return False
    # Check if channel or title has relevant Colombian/Campuslands/Santander/Tech keywords
    keywords = [
        "campusland", "campus land", "campulans", "campus programmers",
        "human code", "tarazona", "vanguardia", "metropolitano", "zona franca",
        "santander", "bucaramanga", "floridablanca", "san gil", "telesangil",
        "redmás", "redmas", "caracol", "mintic", "ministerio tic", "ean",
        "uts", "udi", "unab", "uis", "cámara de comercio", "camara de comercio",
        "fuckup", "try catch", "voxel51", "tatanfue", "fundación et", "fundacion et",
        "camper", "alquilartemis", "bilingüe", "bilingual", "guatemala", "antigua",
        "inversion y desarrollo", "paloma valencia", "soto norte", "colombia compite",
        "alianza por la inclusión", "oro noticias", "cajasan", "profe pachón", "enlace operativo"
    ]
    for kw in keywords:
        if kw in tl or kw in chl:
            # Exclude homonym singer Diego Tarazona songs
            if chl == "diego tarazona" and not any(x in tl for x in ["campus", "program", "ia", "tec", "empres"]):
                return False
            return True
    return False

filtered = [c for c in candidates if is_candidate_worth_checking(c)]
print(f"Filtered {len(candidates)} down to {len(filtered)} candidates for full metadata inspection.")

def fetch_full(vid):
    cmd = [
        sys.executable, "-m", "yt_dlp",
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

full_meta = {}
with ThreadPoolExecutor(max_workers=8) as ex:
    futs = {ex.submit(fetch_full, c["id"]): c for c in filtered}
    for fut in as_completed(futs):
        c = futs[fut]
        vid = c["id"]
        data = fut.result()
        if "error" in data and not data.get("title"):
            print(f"[ERR] {vid}: {data['error']}")
            full_meta[vid] = {"id": vid, "title": c.get("title"), "error": data["error"], "source": c.get("source")}
        else:
            full_meta[vid] = {
                "id": vid,
                "title": data.get("title"),
                "channel": data.get("channel") or data.get("uploader"),
                "channel_id": data.get("channel_id"),
                "channel_url": data.get("channel_url") or data.get("uploader_url"),
                "upload_date": data.get("upload_date"),
                "duration": data.get("duration"),
                " duration_string": data.get("duration_string"),
                "view_count": data.get("view_count"),
                "like_count": data.get("like_count"),
                "description": data.get("description", ""),
                "tags": data.get("tags", []),
                "categories": data.get("categories", []),
                "subtitles": list((data.get("subtitles") or {}).keys()),
                "automatic_captions": list((data.get("automatic_captions") or {}).keys()),
                "webpage_url": data.get("webpage_url") or f"https://www.youtube.com/watch?v={vid}",
                "source": c.get("source"),
                "in_existing_19": vid in EXISTING_19,
            }
            print(f"[OK] {vid} | {full_meta[vid]['upload_date']} | {full_meta[vid]['channel']} | {full_meta[vid]['title']}")

meta_path = out_dir / "filtered_full_metadata.json"
meta_path.write_text(json.dumps(full_meta, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Saved {len(full_meta)} full metadata records to {meta_path}")
