"""replace_in_files.py (通用版): 批量应用 (old, new) 替换列表到所有 .html 文件.

用法:
    python _common_tools/replace_in_files.py <crate_dir> --pairs "old1|||new1" "old2|||new2"

或者把 pairs 写到一个 JSON 文件:
    python _common_tools/replace_in_files.py <crate_dir> --json pairs.json

JSON 格式:
    [["old1", "new1"], ["old2", "new2"]]

默认 dry-run 模式 (只打印会替换的次数不写文件). 加 --apply 才真改文件.

字符串替换时优先匹配长字符串 (按 pairs 长度降序). 用户传入 pairs 时按传入顺序.
"""

import json
import os
import re
import sys


def main():
    if len(sys.argv) < 2:
        print('Usage: replace_in_files.py <crate_dir> [--pairs "old|||new" ...] [--json file.json] [--apply]')
        sys.exit(1)

    base = sys.argv[1]
    args = sys.argv[2:]
    pairs = []
    apply = False
    i = 0
    while i < len(args):
        a = args[i]
        if a == '--apply':
            apply = True
            i += 1
        elif a == '--pairs':
            while i + 1 < len(args) and not args[i + 1].startswith('--'):
                i += 1
                # split on "|||" since docblock text contains many chars
                if '|||' not in args[i]:
                    print(f'WARNING: pair missing "|||": {args[i][:80]}')
                    continue
                old, new = args[i].split('|||', 1)
                pairs.append((old, new))
            i += 1
        elif a == '--json':
            i += 1
            with open(args[i], 'r', encoding='utf-8') as f:
                pairs = json.load(f)
            i += 1
        else:
            print(f'Unknown arg: {a}')
            sys.exit(1)

    # Sort pairs by old length desc (long-string-first to avoid prefix collisions)
    pairs_sorted = sorted(pairs, key=lambda p: -len(p[0]))

    files = []
    for root, _, fs in os.walk(base):
        for f in fs:
            if f.endswith('.html'):
                files.append(os.path.join(root, f))

    n_files = 0
    n_total = 0
    for path in files:
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        orig = c
        n_this = 0
        for old, new in pairs_sorted:
            if old in c:
                c = c.replace(old, new)
                n_this += 1
                n_total += 1
        if c != orig:
            if apply:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(c)
                n_files += 1
            else:
                n_files += 1

    mode = 'APPLY' if apply else 'DRY-RUN'
    print(f'{mode}: {n_files} files updated, {n_total} replacements (out of {len(pairs)} pairs)')


if __name__ == '__main__':
    main()