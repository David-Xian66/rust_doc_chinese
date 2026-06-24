"""Normalize apostrophe in translation table to match U+2019 in source."""
import json
import re

with open('bytes/_buf_translations.json', 'r', encoding='utf-8') as f:
    T = json.load(f)

# Replace ASCII ' with U+2019 in keys only
new_T = {}
for k, v in T.items():
    # U+2019 in source = U+2019 in key
    # First, convert ASCII ' in key to U+2019
    new_k = k.replace("'", "’")
    # But not in middle of contractions - we want to find places where source has Buf's or BytesMut's
    # Actually: simple replace is fine if source consistently uses U+2019
    new_T[new_k] = v

with open('bytes/_buf_translations.json', 'w', encoding='utf-8') as f:
    json.dump(new_T, f, ensure_ascii=False, indent=2)

print(f'Normalized {len(new_T)} keys')
# Show one
for k in list(new_T.keys())[:3]:
    print(repr(k))