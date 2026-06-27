"""Dump all untranslated docblocks and chrome hits from a crate, in a flat text format,
to help design translation pairs.

Usage: python _common_tools/_scan_remaining_zh.py <crate_dir>
"""
import os
import re
import sys


def find_docblocks(content, max_depth=8):
    """Find all <div class="docblock">...</div> with proper depth tracking."""
    DOCBLOCK_RE = re.compile(rb'<div class=["\']docblock["\']>')
    out = []
    pos = 0
    while True:
        m = DOCBLOCK_RE.search(content, pos)
        if not m:
            break
        start = m.end()
        depth = 1
        i = start
        while i < len(content) and depth > 0:
            if content[i:i + 5] == b'<div ' or content[i:i + 5] == b'<div>':
                depth += 1
                i += 5
            elif content[i:i + 6] == b'</div>':
                depth -= 1
                if depth == 0:
                    out.append((m.start(), content[start:i]))
                    pos = i + 6
                    break
                i += 6
            else:
                i += 1
        else:
            break
    return out


def main():
    if len(sys.argv) < 2:
        print('Usage: _scan_remaining_zh.py <crate_dir>')
        sys.exit(1)
    base = sys.argv[1]

    files = []
    for root, _, fs in os.walk(base):
        for f in fs:
            if f.endswith('.html'):
                files.append(os.path.join(root, f))

    # 收集所有未翻译 docblock
    out_lines = []
    for path in files:
        rel = os.path.relpath(path, base)
        with open(path, 'rb') as f:
            c = f.read()
        for m_start, db in find_docblocks(c):
            # 找前一个 method/tymethod/variant/structfield 锚点
            prefix = c[:m_start]
            ids = re.findall(rb'id="(method\.[^"]+|tymethod\.[^"]+|variant\.[^"]+|structfield\.[^"]+|impl-[^"]+)"', prefix)
            if not ids:
                continue
            last_id = ids[-1].decode('utf-8', errors='replace')
            # 检查 docblock 中每个 <p> 是否含 CJK
            for p in re.findall(rb'<p(?:>|\s[^>]*>)([\s\S]*?)</p>', db):
                stripped = re.sub(rb'<[^>]+>', b'', p).decode('utf-8', errors='replace').strip()
                if not re.search(r'[一-鿿]', stripped) and len(stripped) > 5:
                    out_lines.append(f'=== {rel} | {last_id} ===')
                    out_lines.append(stripped[:500])
                    out_lines.append('')
    print('\n'.join(out_lines))


if __name__ == '__main__':
    main()
