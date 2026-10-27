import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

out_dir = Path(r"c:\Users\tomas\second-brain\investigacion\campuslands\scripts")
meta = json.loads((out_dir / "filtered_full_metadata.json").read_text(encoding="utf-8"))

ok_items = [d for d in meta.values() if "error" not in d]
for i, d in enumerate(ok_items[:85]):
    print(f"[{i+1:02d}] {d['id']} | {d.get('upload_date')} | {str(d.get('duration')):>5s}s | {str(d.get('channel'))[:25]:25s} | {d.get('title')} | subs={len(d.get('subtitles',[]))} auto={len(d.get('automatic_captions',[]))}")
