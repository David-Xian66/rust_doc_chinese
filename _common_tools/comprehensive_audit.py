"""Comprehensive audit (通用版): 三段审计 — chrome + OWN docblock + top-doc.

用法:
    python _common_tools/comprehensive_audit.py <crate_dir>

输出: 三段审计报告, 包括 chrome 可见文本残留、未翻译 OWN docblock、未翻译 top-doc 描述.
"""

import os
import re
import sys


def main():
    if len(sys.argv) < 2:
        print('Usage: comprehensive_audit.py <crate_dir>')
        sys.exit(1)
    base = sys.argv[1]
    files = []
    for root, _, fs in os.walk(base):
        for f in fs:
            if f.endswith('.html'):
                files.append(os.path.join(root, f))

    print('=== CHROME SCAN ===')
    chrome_keywords = ['Help', 'Sidebar', 'Theme', 'Settings', 'Sections', 'Keywords',
                       'Fields', 'Variants', 'Methods', 'Implementations',
                       'Trait Implementations', 'Auto Trait Implementations',
                       'Blanket Implementations', 'Required Methods', 'Provided Methods',
                       'Foreign Types', 'Re-exports', 'Modules', 'Macros', 'Enums',
                       'Structs', 'Traits', 'Type Aliases', 'Functions', 'Constants',
                       'Statics', 'Implementors', 'Aliased Type', 'Dyn Compatibility',
                       'List of all items', 'Crate Items', 'Module Items']
    chrome_hits = []
    for path in files:
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        rel = os.path.relpath(path, base)
        # Strip script and style
        stripped = re.sub(r'<script[^>]*>.*?</script>', '', c, flags=re.DOTALL)
        stripped = re.sub(r'<style[^>]*>.*?</style>', '', stripped, flags=re.DOTALL)
        for w in chrome_keywords:
            for m in re.finditer(rf'>{re.escape(w)}<', stripped):
                chrome_hits.append((rel, w, m.start()))
    print(f'Chrome hits: {len(chrome_hits)}')
    for rel, w, pos in chrome_hits[:50]:
        print(f'  {rel}: {w!r}')

    # OWN docblock audit (uses strict audit logic)
    print('\n=== OWN DOCBLOCK AUDIT ===')
    DOCBLOCK_RE = re.compile(r"<div class=['\"]docblock['\"]>(.*?)</div>", re.DOTALL)
    SECTION_RE = re.compile(
        r"<section[^>]*id=['\"]([^\"']+)['\"][^>]*class=['\"]([^'\"]+)['\"][^>]*>(.*?)</section>",
        re.DOTALL,
    )
    SRC_RE = re.compile(r'<a class="src rightside"[^>]+href="([^"]+)"')
    crate_name = os.path.basename(base.rstrip('/\\'))

    untranslated_docblock = []
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
                untranslated_docblock.append((rel, sec_id, text[:300]))

    print(f'OWN untranslated: {len(untranslated_docblock)}')
    for rel, anchor, p in untranslated_docblock[:30]:
        print(f'  {rel} | {anchor}')
        print(f'    {p}')

    # Top-doc audit
    print('\n=== TOP-DOC AUDIT ===')
    top_untranslated = []
    for path in files:
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        rel = os.path.relpath(path, base)
        h1_match = re.search(r'<h1[^>]*>.*?</h1>', c, flags=re.DOTALL)
        if not h1_match:
            continue
        rest = c[h1_match.end():]
        db_match = re.search(r"<div class=['\"]docblock['\"][^>]*>(.*?)</div>", rest, flags=re.DOTALL)
        if not db_match:
            continue
        docblock = db_match.group(1)
        for p in re.findall(r"<p[^>]*>(.*?)</p>", docblock, flags=re.DOTALL):
            stripped = re.sub(r'<[^>]+>', '', p)
            if not re.search(r'[一-鿿]', stripped) and len(stripped.strip()) > 5:
                top_untranslated.append((rel, stripped.strip()[:300]))

    print(f'Top-doc untranslated: {len(top_untranslated)}')
    for rel, p in top_untranslated[:20]:
        print(f'  {rel}')
        print(f'    {p}')


if __name__ == '__main__':
    main()