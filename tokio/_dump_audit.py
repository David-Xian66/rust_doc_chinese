#!/usr/bin/env python3
"""Dump remaining untranslated <p> in tokio AsyncReadExt.html"""
import re

CJK = re.compile('[一-鿿]'.encode())

with open('tokio/io/trait.AsyncReadExt.html', 'rb') as f:
    c = f.read()

ps = re.findall(rb'<p[^>]*>(.+?)</p>', c, flags=re.DOTALL)
print(f'Total <p>: {len(ps)}')
for p in ps:
    text = re.sub(rb'<[^>]+>', b' ', p).strip()
    if text and not CJK.search(text) and len(text) > 10:
        print(text[:300].decode('utf-8', errors='replace'))
        print('---')