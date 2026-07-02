#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix double-quote escapes: \\xe2\\x80\\x9c and \\xe2\\x80\\x9d should be valid U+201C / U+201D chars."""
import os

ROOT = r'D:\Administrator\Documents\Code\rust_doc_all\tokio'

# In source: \xe2\x80\x9c (12 ASCII chars)
LIT_LDQUO = bytes([0x5C, 0x78, 0x65, 0x32, 0x5C, 0x78, 0x38, 0x30, 0x5C, 0x78, 0x39, 0x63])
LIT_RDQUO = bytes([0x5C, 0x78, 0x65, 0x32, 0x5C, 0x78, 0x38, 0x30, 0x5C, 0x78, 0x39, 0x64])

LDQUO = '“'.encode('utf-8')  # "
RDQUO = '”'.encode('utf-8')  # "

print('LIT_LDQUO:', LIT_LDQUO, len(LIT_LDQUO))
print('LDQUO:', LDQUO, len(LDQUO))
print('LIT_RDQUO:', LIT_RDQUO, len(LIT_RDQUO))
print('RDQUO:', RDQUO, len(RDQUO))

# Apply to _translate_subagent_process.py
path = os.path.join(ROOT, '_translate_subagent_process.py')
with open(path, 'rb') as f:
    raw = f.read()

n1 = raw.count(LIT_LDQUO)
n2 = raw.count(LIT_RDQUO)
print(f'Found: ldquo={n1} rdquo={n2}')

raw = raw.replace(LIT_LDQUO, LDQUO)
raw = raw.replace(LIT_RDQUO, RDQUO)

with open(path, 'wb') as f:
    f.write(raw)
print('Done')
