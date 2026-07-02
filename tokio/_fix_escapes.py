#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix \\xe2\\x80\\x99 (escape text) to actual UTF-8 byte sequence in _translate_subagent_*.py files."""
import os
import re

ROOT = r'D:\Administrator\Documents\Code\rust_doc_all\tokio'

# Find literal text "\xe2\x80\x99" in source files - which is 12 ASCII chars:
# \ x e 2 \ x 8 0 \ x 9 9
# In Python literal: 4 backslashes -> 2 backslashes per pair
OLD_LITERAL = b'\\\\xe2\\\\x80\\\\x99'  # this is bytes: \\xe2\\x80\\x99 (12 chars)

NEW_BYTES = '’'.encode('utf-8')  # proper UTF-8 for U+2019 (3 bytes: \xe2\x80\x99)

# Wait, OLD_LITERAL needs to be: 12 ASCII chars matching text in source file
# Actual chars: \ x e 2 \ x 8 0 \ x 9 9
# Each \ in Python escape needs \\ in source string:
# Raw string r'\\xe2\\x80\\x99' = 6 bytes: \ x e 2 \ x 8 0 \ x 9 9? No.
# Let me use a regular string with escapes:
OLD_LITERAL = b'\\xe2\\x80\\x99'  # 6 bytes: \xe2\x80\x99 (which is wrong... hmm)

# OK let me just construct via bytes via ord/chr
OLD_LITERAL = bytes([0x5C, 0x78, 0x65, 0x32, 0x5C, 0x78, 0x38, 0x30, 0x5C, 0x78, 0x39, 0x39])
print('OLD_LITERAL bytes:', OLD_LITERAL, 'len:', len(OLD_LITERAL))
print('NEW_BYTES bytes:', NEW_BYTES, 'len:', len(NEW_BYTES))

for fname in ['_translate_subagent_process.py']:
    path = os.path.join(ROOT, fname)
    with open(path, 'rb') as f:
        raw = f.read()
    n = raw.count(OLD_LITERAL)
    print(f'{fname}: {n} matches')
    raw = raw.replace(OLD_LITERAL, NEW_BYTES)
    with open(path, 'wb') as f:
        f.write(raw)
