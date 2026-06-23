"""Scan all quinn HTML files and report ones with untranslated docblocks."""

import os
import re
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

QUINN_DIR = 'D:/Administrator/Documents/Code/rust_doc_all/quinn'


def count_docblock_cjk(content):
    """Return (total_docblocks, untranslated_count, untranslated_names) for content."""
    # Find all <div class="docblock"> blocks (non-greedy until </div></div></details> or </div></div>)
    # Match the typical pattern: <div class="docblock"> ... </div>  followed by closing detail
    # Use a simpler approach: find <div class="docblock"> then count CJK within next ~3000 chars
    blocks = re.findall(r'<div class="docblock">(.*?)(?=<div class="docblock">|<h[12]|</section>)',
                        content, flags=re.DOTALL)
    if not blocks:
        return 0, 0, []

    total = len(blocks)
    untranslated = []
    for b in blocks:
        # Strip HTML tags and code examples
        text = re.sub(r'<pre.*?</pre>', '', b, flags=re.DOTALL)
        text = re.sub(r'<code>.*?</code>', 'X', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', '', text)
        # Detect mostly English
        cjk = re.findall(r'[一-鿿]', text)
        latin = re.findall(r'[a-zA-Z]', text)
        if len(cjk) < 5 and len(latin) > 20:
            untranslated.append((len(b), b[:100].replace('\n', ' ')))
    return total, len(untranslated), untranslated


def main():
    results = []
    for root, dirs, files in os.walk(QUINN_DIR):
        # Skip sidebar-items.js-like files
        for fn in files:
            if not fn.endswith('.html'):
                continue
            path = os.path.join(root, fn)
            rel = os.path.relpath(path, QUINN_DIR)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    c = f.read()
            except Exception as e:
                print(f'  [ERROR] {rel}: {e}')
                continue
            total, un, _ = count_docblock_cjk(c)
            if un > 0:
                results.append((rel, total, un))

    results.sort(key=lambda x: -x[2])
    print(f'\n=== Files with untranslated docblocks: {len(results)} ===\n')
    for rel, total, un in results:
        print(f'  {rel}: {un}/{total} untranslated')
    return results


if __name__ == '__main__':
    main()
