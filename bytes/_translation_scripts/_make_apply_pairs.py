"""Build LF-normalized pairs for apply."""
import json

with open('bytes/_pairs_v2.json', 'r', encoding='utf-8') as f:
    pairs = json.load(f)

# Normalize CRLF to LF (replace_in_files.py reads in text mode)
normalized = []
for old, new in pairs:
    old_n = old.replace('\r\n', '\n')
    new_n = new.replace('\r\n', '\n')
    normalized.append([old_n, new_n])

with open('bytes/_pairs_apply.json', 'w', encoding='utf-8') as f:
    json.dump(normalized, f, ensure_ascii=False, indent=2)

print(f'Wrote {len(normalized)} normalized pairs')