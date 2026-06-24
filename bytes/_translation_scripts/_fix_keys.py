"""Fix missing 'current' word in remaining/remaining_mut keys."""
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('bytes/_buf_translations.json', 'r', encoding='utf-8') as f:
    T = json.load(f)

RSQUO = '’'

# Need to fix keys: "change the Buf position" -> "change the Buf's current position"
# And same for BufMut
new_T = {}
for k, v in T.items():
    new_T[k] = v
    # Fix Buf position without apostrophe -> with apostrophe and "current"
    if "change the Buf position" in k:
        new_k = k.replace("change the Buf position", f"change the Buf{RSQUO}s current position")
        if new_k not in new_T:
            # Update value too
            new_v = v.replace("<code>Buf</code>", f"<code>Buf{RSQUO}s</code>")
            new_T[new_k] = new_v
    if "change the BufMut position" in k:
        new_k = k.replace("change the BufMut position", f"change the BufMut{RSQUO}s current position")
        if new_k not in new_T:
            new_v = v.replace("<code>BufMut</code>", f"<code>BufMut{RSQUO}s</code>")
            new_T[new_k] = new_v

with open('bytes/_buf_translations.json', 'w', encoding='utf-8') as f:
    json.dump(new_T, f, ensure_ascii=False, indent=2)

print(f'Total: {len(new_T)}')
# Verify
for k in new_T:
    if 'remaining should' in k and 'change the' in k and 'BufMut' not in k:
        print(f'  {k[:120]!r}')