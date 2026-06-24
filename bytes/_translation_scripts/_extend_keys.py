"""Extend truncated keys to match full text."""
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('bytes/_buf_translations.json', 'r', encoding='utf-8') as f:
    T = json.load(f)

# Remove old truncated keys
old_keys = [
    'When processing a Bytes buffer with other tools, one often gets a\n&amp;[u8] which is in fact a slice of the Bytes, i.e. a subset of it.\nThis function turns that &amp;[u8] into another Bytes, as if one had\ncalled self.slice',
]
for k in old_keys:
    if k in T:
        del T[k]
        print(f'Removed old truncated: ...{k[-30:]!r}')

# Verify
for k in T:
    if 'When processing' in k:
        print(f'Remaining: ...{k[-30:]!r}')

with open('bytes/_buf_translations.json', 'w', encoding='utf-8') as f:
    json.dump(T, f, ensure_ascii=False, indent=2)

print(f'Total: {len(T)}')