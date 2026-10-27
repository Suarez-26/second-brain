import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

out_dir = Path(r"c:\Users\tomas\second-brain\investigacion\campuslands\scripts")
meta = json.loads((out_dir / "filtered_full_metadata.json").read_text(encoding="utf-8"))

ok_items = []
err_items = []
for vid, d in meta.items():
    if "error" in d:
        err_items.append(d)
    else:
        ok_items.append(d)

print(f"OK: {len(ok_items)} | ERR: {len(err_items)}")
print("\n=== OK ITEMS ===")
for d in ok_items:
    print(f"  {d['id']} | {d.get('upload_date')} | {str(d.get('duration')):>5s}s | {str(d.get('channel'))[:25]:25s} | {d.get('title')} | subs={len(d.get('subtitles',[]))} auto={len(d.get('automatic_captions',[]))}")

print("\n=== ERR ITEMS ===")
for d in err_items:
    print(f"  {d['id']} | {d.get('title')} | {d['error'][:90]}")
