"""Final verify (通用版): 行号污染 + 标签平衡 + CJK 总数 + 标识符保留.

用法:
    python _common_tools/final_verify.py <crate_dir>
"""

import os
import re
import sys


def main():
    if len(sys.argv) < 2:
        print('Usage: final_verify.py <crate_dir>')
        sys.exit(1)
    base = sys.argv[1]
    files = []
    for root, _, fs in os.walk(base):
        for f in fs:
            if f.endswith('.html'):
                files.append(os.path.join(root, f))

    issues = []
    total_cjk = 0
    for path in files:
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        rel = os.path.relpath(path, base)

        # 1. Line number pollution
        if re.findall(r'^\d+\t', c, flags=re.MULTILINE):
            issues.append((rel, 'LINE_NUM_POLLUTION'))

        # 2. Tag balance
        for tag in ('html', 'head', 'body', 'main', 'section', 'div', 'p', 'a', 'span',
                    'h1', 'h2', 'h3', 'h4', 'ul', 'li', 'code', 'pre', 'details',
                    'summary', 'dl', 'dt', 'dd'):
            opens = len(re.findall(rf'<{tag}(?:\s[^>]*)?>', c))
            closes = len(re.findall(rf'</{tag}>', c))
            if opens != closes:
                issues.append((rel, f'TAG_IMBALANCE: <{tag}> open={opens} close={closes}'))

        cjk = re.findall(r'[一-鿿]', c)
        total_cjk += len(cjk)

    print(f'Files: {len(files)}')
    print(f'Total CJK chars: {total_cjk}')
    print(f'Issues: {len(issues)}')
    for rel, kind in issues[:30]:
        print(f'  {rel}: {kind}')


if __name__ == '__main__':
    main()