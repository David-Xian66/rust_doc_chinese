"""Dump top docblock for each file."""
import os
import re
import sys

if len(sys.argv) < 2:
    print('Usage: _dump_topdoc.py <crate_dir>')
    sys.exit(1)
base = sys.argv[1]

files = []
for root, _, fs in os.walk(base):
    for f in fs:
        if f.endswith('.html'):
            files.append(os.path.join(root, f))
files.sort()

for fp in files:
    rel = os.path.relpath(fp, base)
    with open(fp, 'rb') as f: c = f.read()
    m = re.search(rb'</h1>(.*?)<h2', c, flags=re.DOTALL)
    if not m: continue
    section = m.group(1)
    db = re.search(rb'<div class="docblock">(.*?)</div>', section, flags=re.DOTALL)
    if not db: continue
    raw = db.group(1)
    text = re.sub(rb'<[^>]+>', b' ', raw).decode('utf-8', errors='replace').strip()
    text = re.sub(r'\s+', ' ', text)
    if text:
        print(f'### {rel} ###')
        print(text)
        print()
