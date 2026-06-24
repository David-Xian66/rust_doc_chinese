"""Add U+2019 apostrophes to Buf/BufMut keys to match source."""
import json

with open('bytes/_buf_translations.json', 'r', encoding='utf-8') as f:
    T = json.load(f)

# Add U+2019 variant of remaining/remaining_mut entries
RSQUO = '’'
new_T = {}

for k, v in T.items():
    new_T[k] = v
    # Add U+2019 variants
    if "Buf position" in k and "U+2019" not in k:
        new_k = k.replace("Buf position", f"Buf{RSQUO}s position")
        new_T[new_k] = v.replace("Buf", f"Buf{RSQUO}s") if "Buf" in v else v
    if "BufMut position" in k and "U+2019" not in k:
        new_k = k.replace("BufMut position", f"BufMut{RSQUO}s position")
        new_T[new_k] = v.replace("BufMut", f"BufMut{RSQUO}s") if "BufMut" in v else v

with open('bytes/_buf_translations.json', 'w', encoding='utf-8') as f:
    json.dump(new_T, f, ensure_ascii=False, indent=2)

print(f'Total: {len(new_T)}')
# Check if both exist
for k in new_T:
    if "remaining should" in k:
        print(f'  {k[:100]!r}')