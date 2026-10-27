import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

out_dir = Path(r"c:\Users\tomas\second-brain\investigacion\campuslands\scripts")
candidates = json.loads((out_dir / "candidates_flat.json").read_text(encoding="utf-8"))

for i, c in enumerate(candidates):
    vid = c.get("id")
    title = c.get("title", "")
    channel = c.get("channel") or c.get("uploader") or ""
    dur = c.get("duration")
    src = c.get("source", "")
    print(f"[{i+1:03d}] {vid} | {channel[:28]:28s} | {str(dur):6s} | {title} ({src})")
