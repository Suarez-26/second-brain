import json, glob, os

d = json.load(open(r'c:\Users\tomas\second-brain\sources\prensa_y_web\curl_and_arctic_results.json', encoding='utf-8'))
out = []
for v in d.get('curl', []):
    out.append(f"=== CURL: {v.get('key')} (status={v.get('status')}) URL={v.get('final_url')} ===\n{v.get('text','')[:8000]}")
for k, v in d.get('arctic', {}).items():
    out.append(f"=== ARCTIC: {k} ===\n{json.dumps(v, indent=2, ensure_ascii=False)[:8000]}")

with open(r'c:\Users\tomas\second-brain\sources\prensa_y_web\curl_arctic_readable.txt', 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(out))

art_files = sorted(glob.glob(r'c:\Users\tomas\second-brain\sources\prensa_y_web\art_*.txt'))
print("Total art files:", len(art_files))
for af in art_files:
    print(os.path.basename(af), os.path.getsize(af))
