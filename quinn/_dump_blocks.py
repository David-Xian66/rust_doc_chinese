"""Dump all untranslated docblocks from a quinn HTML file."""

import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def dump(path):
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    blocks = re.findall(r'<div class="docblock">(.*?)(?=<div class="docblock">|<h[12]|</section>)',
                        c, flags=re.DOTALL)
    out = []
    for b in blocks:
        text = re.sub(r'<pre.*?</pre>', '', b, flags=re.DOTALL)
        text = re.sub(r'<code>.*?</code>', 'X', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', '', text)
        cjk = re.findall(r'[一-鿿]', text)
        latin = re.findall(r'[a-zA-Z]', text)
        if len(cjk) < 5 and len(latin) > 20:
            out.append(b)
    return out, len(blocks)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: dump_blocks.py <path>')
        sys.exit(1)
    path = sys.argv[1]
    blocks, total = dump(path)
    print(f'=== {path}: {len(blocks)}/{total} untranslated ===')
    for b in blocks:
        print('---')
        print(b)
