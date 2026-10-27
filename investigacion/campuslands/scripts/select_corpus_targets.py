import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

out_dir = Path(r"c:\Users\tomas\second-brain\investigacion\campuslands\scripts")
meta = json.loads((out_dir / "filtered_full_metadata.json").read_text(encoding="utf-8"))
flat = {c["id"]: c for c in json.loads((out_dir / "candidates_flat.json").read_text(encoding="utf-8"))}

EXISTING_19 = {
    "F-AvmYM2k8k", "s8CMhCGFI6U", "kANZD8FTN5Y", "uArGKWxb0jU",
    "wuc9sv84B6o", "ZjS85xqQSn4", "KEbYZ0X7Aec", "I-3waHqlUPk",
    "Oc1K_vHu3Uc", "fH8WmSSFjEs", "f_DFCoVgYV0", "Bc7kNy7yuvc",
    "4LkwD59y_Vs", "NxyrHzFu5oU", "MByGeiB1y2Y", "zVj6Nezq7u0",
    "xc1YnHqihrw", "AnWiyruHz1I", "Ns7T2mGXx-A"
}

# Check which OK items are genuinely about Campuslands or Diego Fernando Tarazona Pinzón
relevant_new = []
relevant_existing = []
relevant_unavailable = []

for vid, d in meta.items():
    if "error" in d:
        # Check flat metadata
        fc = flat.get(vid, {})
        title = (fc.get("title") or d.get("title") or "").strip()
        ch = (fc.get("channel") or fc.get("uploader") or "").strip()
        tl = (title + " " + ch).lower()
        if any(w in tl for w in ["campusland", "campus land", "campulans", "alquilartemis", "fundación et", "fundacion et"]) or vid in {"mOWFj0N5Z_s", "ygRCAJzb2GI"}:
            relevant_unavailable.append({
                "id": vid,
                "title": title,
                "channel": ch,
                "duration": fc.get("duration"),
                "error": d["error"]
            })
        continue

    title = (d.get("title") or "").strip()
    ch = (d.get("channel") or "").strip()
    desc = (d.get("description") or "").strip()
    blob = (title + " " + ch + " " + desc).lower()

    if vid in EXISTING_19:
        relevant_existing.append(d)
        continue

    # Exclude false positives
    # Homonym Diego Tarazona (musician, MMA fighter, student at UNAL/UPN/UNAD, Chocoblueberry Peru, etc.)
    if vid in {
        "l5c4bo1N2Nk", "ZKqJ__wwhWA", "KHysGFdWdUc", "AYIqbjsdpiQ",
        "uxAo6E2V2mQ", "I6w6KM9ESLg", "wQ-zli363Kc", "T5ex5NquvPs",
        "whdLfVc2yHU", "EmBav-64rpw", "s30NMirXmRo",
        "N4p4Ee5CGmY", "lzysbZ9xlrU", "7XzhMm4h0Mw", "b4kA6xgAtc4",
        "urfdF1jkzZk", "0mtOQ3wIFBg", "V9aUR9_QXnI", "WMlmFilafUA",
        "tEpFyMpQ5u0", "Bf1nEucnDc4", "Bng8FhkUrNs", "lIFVIL_Vhro",
        "FfnsjPXWAGw", "pDBSggZYqGY", "dfpT2MEfZ2w", "g1sHhNGQxjA",
        "94xN1yVCesA", "FvlEu4WZz7k"
    }:
        # Double check if any of these mention campuslands in description
        if not any(w in blob for w in ["campusland", "campus land", "campulans", "tarazona pinz", "campus 5.0"]):
            continue

    # Check if it mentions campuslands, campus land, campulans, campus programmers, diego tarazona (campuslands), or is from a campuslands channel
    if any(w in blob for w in ["campusland", "campus land", "campulans", "campus programmers", "diego tarazon", "campus 2023", "alquilartemis"]) or vid in {
        "zGi65oaB9dA", "PasWbp5FGbE", "8l31wVP6C2M", "3av_YtMXvbc",
        "k8-ByiClnq8", "fs2isMnSQ0o", "bfdR98QqbIs", "eRy285TpfvI",
        "koi_Rm-E3Lw", "i0BMIxyM46w", "ZtHMUxd9XSw", "n4lp2MQMEwQ",
        "30GuYjIjUhY", "JBA1gdRs8DI", "Hj-ApbBtb6Y", "AAAwSmenc20",
        "9hWBSxysdmk", "uqK5QJ45dVg", "3m_j7pfFiqk", "VuYGYgRkxiY",
        "8U8ks1oXVaQ", "epCYfITtzMo", "0cNKTgD2gDY", "k6BsrFrKZUc"
    }:
        relevant_new.append(d)

print(f"Relevant EXISTING (19): {len(relevant_existing)}")
print(f"Relevant NEW (available): {len(relevant_new)}")
for i, d in enumerate(sorted(relevant_new, key=lambda x: x.get("upload_date") or "")):
    print(f"  [{i+1:02d}] {d['id']} | {d.get('upload_date')} | {str(d.get('duration')):>5s}s | {str(d.get('channel'))[:25]:25s} | {d.get('title')}")

print(f"\nRelevant UNAVAILABLE/PRIVATE on YT (with flat metadata): {len(relevant_unavailable)}")
for i, d in enumerate(relevant_unavailable):
    print(f"  [{i+1:02d}] {d['id']} | {str(d.get('duration')):>5s}s | {str(d.get('channel'))[:25]:25s} | {d.get('title')}")

(out_dir / "selected_new_videos.json").write_text(json.dumps(relevant_new, ensure_ascii=False, indent=2), encoding="utf-8")
(out_dir / "selected_unavailable_videos.json").write_text(json.dumps(relevant_unavailable, ensure_ascii=False, indent=2), encoding="utf-8")
