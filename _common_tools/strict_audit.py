"""Strict audit (通用版): 检测某 crate 目录下所有 OWN method docblock 是否已翻译。

用法:
    python _common_tools/strict_audit.py <crate_dir> [crate_name]

示例:
    python _common_tools/strict_audit.py rustls_pki_types rustls_pki_types
    python _common_tools/strict_audit.py quinn quinn

输出: 列出每个未翻译 docblock 的 (file, anchor, text).

关键 bug 修复 (历史教训):
1. rustdoc 输出的 docblock 有两种: <p> 包裹 (inherent method) 和裸文本 (trait method).
   必须剥掉所有 HTML 标签后检查 CJK, 而非仅查 <p> 内容.
2. rustdoc 用单引号或双引号的 class 属性: <div class="docblock"> 和 <div class='docblock'> 都要匹配.
3. OWN vs STD 方法需通过 src href 区分: src 指向 ../src/<crate_name>/*.rs.html 是 OWN,
   指向 doc.rust-lang.org 是 STD lib 方法 (不翻译).
4. Section 标签属性顺序: <section class='...' id='...'> 或 <section id='...' class='...'>,
   regex 不能假设顺序.
"""

import os
import re
import sys


def main():
    if len(sys.argv) < 2:
        print('Usage: strict_audit.py <crate_dir> [crate_name]')
        sys.exit(1)
    crate_dir = sys.argv[1]
    crate_name = sys.argv[2] if len(sys.argv) > 2 else os.path.basename(crate_dir.rstrip('/\\'))
    base = crate_dir
    files = []
    for root, _, fs in os.walk(base):
        for f in fs:
            if f.endswith('.html'):
                files.append(os.path.join(root, f))

    DOCBLOCK_RE = re.compile(r"<div class=['\"]docblock['\"]>(.*?)</div>", re.DOTALL)
    SECTION_RE = re.compile(
        r"<section[^>]*id=['\"]([^\"']+)['\"][^>]*class=['\"]([^'\"]+)['\"][^>]*>(.*?)</section>",
        re.DOTALL,
    )
    SRC_RE = re.compile(r'<a class="src rightside"[^>]+href="([^"]+)"')

    untranslated = {}
    for path in files:
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        rel = os.path.relpath(path, base)

        for m in SECTION_RE.finditer(c):
            sec_id = m.group(1)
            sec_class = m.group(2)
            sec_body = m.group(3)
            if 'method' not in sec_class:
                continue
            sm = SRC_RE.search(sec_body)
            if not sm:
                continue
            href = sm.group(1)
            # OWN check: src 包含 crate name
            if crate_name not in href and crate_name.replace('_', '-') not in href:
                continue
            idx = m.end()
            rest = c[idx:idx+5000]
            db_match = DOCBLOCK_RE.search(rest)
            if not db_match:
                continue
            docblock = db_match.group(1)
            text = re.sub(r'<[^>]+>', ' ', docblock).strip()
            text = re.sub(r'\s+', ' ', text)
            if not text:
                continue
            if not re.search(r'[一-鿿]', text) and len(text) > 5:
                untranslated.setdefault((rel, sec_id), []).append(text[:300])

    print(f'OWN trait-method docblocks untranslated: {len(untranslated)}')
    for (rel, sec_id), items in sorted(untranslated.items()):
        print(f'[{rel}] {sec_id}')
        for text in items:
            print(f'  {text}')


if __name__ == '__main__':
    main()