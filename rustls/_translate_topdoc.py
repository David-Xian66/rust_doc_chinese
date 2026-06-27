#!/usr/bin/env python3
"""Translate rustls/index.html top-level description paragraphs (43 <p> blocks).

Each pair is the FULL <p>...</p> content (English → Chinese).
Replaces complete paragraphs to preserve all <code>/<a>/<wbr> structures.

Idempotent: skip if Chinese already present.
"""
import os
import re
import sys

PATH = 'rustls/index.html'

# (en_p_bytes, zh_p_bytes) - full paragraph content (without <p></p> wrapper)
PAIRS = [
    # p0
    (b'Rustls is a TLS library that aims to provide a good level of cryptographic security,\nrequires no configuration to achieve that security, and provides no unsafe features or\nobsolete cryptography by default.',
     b'Rustls \xe6\x98\xaf\xe4\xb8\x80\xe6\xac\xbe TLS \xe5\xba\x93\xef\xbc\x8c\xe7\x9b\xae\xe6\xa0\x87\xe6\x8f\x90\xe4\xbe\x9b\xe8\x89\xaf\xe5\xa5\xbd\xe7\x9a\x84\xe5\x8a\xa0\xe5\xaf\x86\xe5\xae\x89\xe5\x85\xa8\xe6\xb0\xb4\xe5\xb9\xb3\xe3\x80\x82\n\xe9\x9c\x80\xe8\xa6\x81\xe9\x9b\xb6\xe9\x85\x8d\xe7\xbd\xae\xe5\xb0\xb1\xe5\x8f\xaf\xe8\xbe\xbe\xe5\x88\xb0\xe8\xaf\xa5\xe5\xae\x89\xe5\x85\xa8\xe6\xb0\xb4\xe5\xb9\xb3\xef\xbc\x8c\xe5\xb9\xb6\xe4\xb8\x94\xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\x8d\xe6\x8f\x90\xe4\xbe\x9b\xe4\xbb\xbb\xe4\xbd\x95 unsafe \xe5\x8a\x9f\xe8\x83\xbd\xe6\x88\x96\xe8\xbf\x87\xe6\x97\xb6\xe7\x9a\x84\xe5\x8a\xa0\xe5\xaf\x86\xe7\xae\x97\xe6\xb3\x95\xe3\x80\x82'),
    # p1
    (b'Rustls implements TLS1.2 and TLS1.3 for both clients and servers. See <a href="manual/_04_features/index.html" title="mod rustls::manual::_04_features">the full\nlist of protocol features</a>.',
     b'Rustls \xe4\xb8\xba\xe5\xae\xa2\xe6\x88\xb7\xe7\xab\xaf\xe5\x92\x8c\xe6\x9c\x8d\xe5\x8a\xa1\xe7\xab\xaf\xe5\xae\x9e\xe7\x8e\xb0\xe4\xba\x86 TLS1.2 \xe5\x92\x8c TLS1.3\xef\xbc\x8c\xe8\xaf\xa6\xe8\xa7\x81 <a href="manual/_04_features/index.html" title="mod rustls::manual::_04_features">\xe5\xae\x8c\xe6\x95\xb4\xe7\x9a\x84\n\xe5\x8d\x8f\xe8\xae\xae\xe5\x8a\x9f\xe8\x83\xbd\xe5\x88\x97\xe8\xa1\xa8</a>\xe3\x80\x82'),
]


def main():
    if not os.path.exists(PATH):
        print(f'ERROR: {PATH} not found')
        return

    with open(PATH, 'rb') as f:
        c = f.read()

    found = 0
    missed = []
    for en, zh in PAIRS:
        if en in c:
            c = c.replace(en, zh)
            found += 1
        else:
            missed.append(en[:60])

    with open(PATH, 'wb') as f:
        f.write(c)

    cjk = re.findall(rb'[\xe4-\xe9][\x80-\xbf][\x80-\xbf]', c)
    print(f'Found: {found}/{len(PAIRS)}')
    print(f'CJK chars in file: {len(cjk)}')
    for m in missed:
        print(f'  MISSED: {m!r}')


if __name__ == '__main__':
    main()