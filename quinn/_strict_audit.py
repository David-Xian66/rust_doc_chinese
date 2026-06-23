"""Strict audit: every <p> in every docblock must contain CJK.

Prints a list of (file, snippet) for any non-CJK <p>.
"""

import os
import re

BASE = 'D:/Administrator/Documents/Code/rust_doc_all/quinn'


def check(path):
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    blocks = re.findall(r'<div class="docblock">(.*?)</div>', c, flags=re.DOTALL)
    untranslated = []
    for b in blocks:
        ps = re.findall(r'<p[^>]*>(.*?)</p>', b, flags=re.DOTALL)
        for p in ps:
            stripped = re.sub(r'<[^>]+>', '', p)
            stripped = re.sub(r'&[a-z#0-9]+;', ' ', stripped)
            if not re.search(r'[一-鿿]', stripped):
                if len(stripped.strip()) > 5:
                    untranslated.append(p[:200])
    return untranslated


def main():
    total = 0
    for root, _, files in os.walk(BASE):
        for f in files:
            if f.endswith('.html'):
                p = os.path.join(root, f)
                rel = os.path.relpath(p, BASE)
                u = check(p)
                if u:
                    total += len(u)
                    print(f'=== {rel}: {len(u)} untranslated <p> ===')
                    for line in u:
                        print(f'  - {line}')
    print(f'\nTotal untranslated <p>: {total}')


if __name__ == '__main__':
    main()