#!/usr/bin/env python3
"""扫描所有 crate 的未翻译 dd/h2/h3，并把它们从文件中提取为 raw HTML（含 <code> 标签）。
输出为可直接复制粘贴到 _translate_module_descriptions.py 的 (en, zh) 占位条目。

用法：
    python _common_tools/_extract_untranslated_raw.py <crate_dir> [--json]
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _strict_module_audit import audit_file  # noqa


def main():
    if len(sys.argv) < 2:
        print('Usage: _extract_untranslated_raw.py <crate_dir> [--json]')
        sys.exit(1)
    crate_dir = sys.argv[1]
    as_json = '--json' in sys.argv

    # 收集所有 (cat, raw_html, file)
    pairs_by_key = {}  # text → raw_html

    for top, dirs, fs in os.walk(crate_dir):
        dirs[:] = [d for d in dirs if not d.endswith('_old') and not d.startswith('.')]
        for fn in fs:
            if not fn.endswith('.html'):
                continue
            path = os.path.join(top, fn)
            try:
                with open(path, 'rb') as f:
                    raw = f.read()
            except Exception:
                continue

            issues = audit_file(path)
            for cat, text, p, pos in issues:
                if cat == 'item-table-dd':
                    # 找 dd 的 raw HTML
                    dd_re = re.compile(rb'<dd>(.*?)</dd>', re.DOTALL)
                    for dd_m in dd_re.finditer(raw, pos):
                        raw_html = dd_m.group(1).decode('utf-8', errors='replace')
                        # 去掉 dd 起始/结束位置
                        stripped_text = re.sub(r'<[^>]+>', '', raw_html).strip()
                        if stripped_text == text or stripped_text.startswith(text[:50]):
                            key = stripped_text
                            if key not in pairs_by_key:
                                pairs_by_key[key] = raw_html
                            break
                elif cat in ('h3-heading', 'h2-section-header'):
                    # h3/h2 raw HTML
                    header_re = re.compile(rb'<h[23](?:\s+[^>]*)?>(.*?)</h[23]>', re.DOTALL)
                    for h_m in header_re.finditer(raw, pos):
                        raw_html = h_m.group(0).decode('utf-8', errors='replace')
                        stripped_text = re.sub(r'<[^>]+>', '', raw_html).strip()
                        if stripped_text == text or stripped_text.startswith(text[:50]):
                            key = stripped_text
                            if key not in pairs_by_key:
                                pairs_by_key[key] = raw_html
                            break

    if as_json:
        print(json.dumps(
            [{'text': k, 'raw_html': v} for k, v in sorted(pairs_by_key.items())],
            ensure_ascii=False, indent=2))
    else:
        for k, v in sorted(pairs_by_key.items()):
            print(f'# {k!r}')
            print(f'    ({v!r},')
            print(f"     '<中文翻译>'),")
            print()


if __name__ == '__main__':
    main()