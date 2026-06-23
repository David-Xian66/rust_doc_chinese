"""Strict audit v2: only check <p> in quinn's own methods/structs.

For each <section id="method.NAME" ...> block or struct field/tymethod block,
extract the immediately following <div class="docblock"> and check every <p>.
"""

import os
import re

BASE = 'D:/Administrator/Documents/Code/rust_doc_all/quinn'


def check_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    bad = []
    # 抓所有 <div class="docblock">...</div>
    for m in re.finditer(r'<div class="docblock">(.*?)</div>', c, flags=re.DOTALL):
        block = m.group(1)
        # 找该 docblock 之前最近的 id
        prefix = c[:m.start()]
        last_id = re.findall(r'id="(method\.[^"]+|tymethod\.[^"]+|variant\.[^"]+|structfield\.[^"]+|impl-[^"]+|associatedtype\.[^"]+|associatedconst\.[^"]+)"', prefix)
        if not last_id:
            continue  # 不在 quinn 自己声明的块内，跳过
        last_id = last_id[-1]
        # 找该 docblock 内每个 <p>
        for p in re.findall(r'<p[^>]*>(.*?)</p>', block, flags=re.DOTALL):
            stripped = re.sub(r'<[^>]+>', '', p)
            stripped = re.sub(r'&[a-z#0-9]+;', ' ', stripped)
            if not re.search(r'[一-鿿]', stripped):
                if len(stripped.strip()) > 5:
                    bad.append((last_id, p))
    return bad


def main():
    total = 0
    for root, _, files in os.walk(BASE):
        for f in files:
            if f.endswith('.html'):
                p = os.path.join(root, f)
                rel = os.path.relpath(p, BASE)
                bad = check_file(p)
                if bad:
                    total += len(bad)
                    print(f'=== {rel}: {len(bad)} untranslated <p> ===')
                    for ident, p in bad:
                        # 截掉过长的内容
                        print(f'  [{ident}] {p[:300]}{"..." if len(p) > 300 else ""}')
    print(f'\nTotal untranslated <p>: {total}')


if __name__ == '__main__':
    main()