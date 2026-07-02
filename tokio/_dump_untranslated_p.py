#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dump untranslated <p> blocks from given file - bytes-formatted."""
import sys
import re


def dump(path):
    with open(path, 'rb') as f:
        content = f.read()

    def has_cjk(b):
        return bool(re.search(rb'[\xe4-\xe9][\x80-\xbf][\x80-\xbf]', b))

    def find_docblocks(text):
        i = 0
        while True:
            idx = text.find(b'<div class="docblock">', i)
            if idx < 0:
                return
            depth = 1
            j = idx + len(b'<div class="docblock">')
            while j < len(text) and depth > 0:
                next_open = text.find(b'<div', j)
                next_close = text.find(b'</div>', j)
                if next_close < 0:
                    return
                if next_open >= 0 and next_open < next_close:
                    depth += 1
                    j = next_open + 4
                else:
                    depth -= 1
                    j = next_close + 6
                    if depth == 0:
                        yield (idx, j)
                        i = j
                        break
            else:
                i = idx + 1
                continue

    def last_id(prefix):
        ids = re.findall(rb'id="(method\.[^"]+|tymethod\.[^"]+|variant\.[^"]+|structfield\.[^"]+|impl-[^"]+)"', prefix)
        return ids[-1] if ids else None

    # Write to stdout
    out = sys.stdout
    for ds, de in find_docblocks(content):
        inner = content[ds:de]
        lid = last_id(content[:ds])
        for p in re.finditer(rb'<p(?:>|\s[^>]*>)([\s\S]*?)</p>', inner):
            text = re.sub(rb'<[^>]+>', b'', p.group(0)).strip()
            if not has_cjk(text) and len(text) > 15:
                id_str = lid.decode() if lid else '?'
                out.write('### id=' + id_str + '\n')
                # Use repr of bytes for safe extraction
                out.write(repr(p.group(0)) + '\n')
                out.write('\n')


if __name__ == '__main__':
    dump(sys.argv[1])
