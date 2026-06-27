#!/usr/bin/env python3
"""收集 crate 内所有未翻译的英文文本（来自 _strict_module_audit 的位置分类）。
输出为 JSON 列表 [(category, text, file, position)]，便于批量翻译。
用法：python _common_tools/_collect_untranslated.py <crate_dir> [--json] [--dedup]
"""
import json
import os
import re
import sys

# Reuse audit logic
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _strict_module_audit import audit_file  # noqa


def main():
    if len(sys.argv) < 2:
        print('Usage: _collect_untranslated.py <crate_dir> [--json] [--dedup]')
        sys.exit(1)
    crate_dir = sys.argv[1]
    dedup = '--dedup' in sys.argv
    as_json = '--json' in sys.argv

    issues = []
    seen = set()
    for top, dirs, fs in os.walk(crate_dir):
        dirs[:] = [d for d in dirs if not d.endswith('_old') and not d.startswith('.')]
        for fn in fs:
            if not fn.endswith('.html'):
                continue
            path = os.path.join(top, fn)
            for cat, text, p, pos in audit_file(path):
                key = (cat, text)
                if dedup and key in seen:
                    continue
                seen.add(key)
                issues.append({'category': cat, 'text': text, 'file': p, 'pos': pos})

    if as_json:
        print(json.dumps(issues, ensure_ascii=False, indent=2))
    else:
        # Human-readable
        by_cat = {}
        for i in issues:
            by_cat.setdefault(i['category'], []).append(i)
        for cat, items in sorted(by_cat.items()):
            print(f'\n=== {cat}: {len(items)} ===')
            for item in items:
                text = item['text'][:120].replace('\n', ' ')
                print(f'  [{item["file"]}] {text}')


if __name__ == '__main__':
    main()
