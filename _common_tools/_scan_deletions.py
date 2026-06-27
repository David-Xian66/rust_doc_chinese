#!/usr/bin/env python3
"""扫描所有已翻译 crate 与 _old 副本，定位被误删的 HTML 结构。

策略（修正版）：
1. 比较 h2 id 列表（不考虑 class，因为翻译不影响 id）
2. 比较 h3 id 列表
3. 比较 section id 列表
4. 比较关键 id 锚点（implementors-list, variants-list 等）的存在性
5. sidebar 链接 href 列表（去除 wbr 后比较）
6. h2 section-header 内的 chrome 标签（变体、实现者、字段 等）通过 id 锚点推断
"""
import os
import re
import sys
from collections import defaultdict


H2_ID_RE = re.compile(r'<h2[^>]*\bid="([^"]+)"', re.DOTALL)
H3_ID_RE = re.compile(r'<h3[^>]*\bid="([^"]+)"', re.DOTALL)
H4_ID_RE = re.compile(r'<h4[^>]*\bid="([^"]+)"', re.DOTALL)
SECTION_ID_RE = re.compile(r'<section[^>]*\bid="([^"]+)"', re.DOTALL)

# sidebar h3/h4 链接 href 列表（看链接指向的锚点）
SIDEBAR_H3_LINK_HREF_RE = re.compile(r'<h[34]>\s*<a[^>]+href="#([^"]+)"[^>]*>', re.DOTALL)
SIDEBAR_H2_LINK_HREF_RE = re.compile(r'<h2[^>]*>\s*<a[^>]+href="#([^"]+)"[^>]*>', re.DOTALL)


def find_html_files(root):
    out = []
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in ('static.files',)]
        for f in files:
            if f.endswith('.html'):
                out.append(os.path.join(dirpath, f))
    return out


def extract_structure(content):
    return {
        'h2_ids': H2_ID_RE.findall(content),
        'h3_ids': H3_ID_RE.findall(content),
        'h4_ids': H4_ID_RE.findall(content),
        'section_ids': SECTION_ID_RE.findall(content),
        'sidebar_h3_hrefs': SIDEBAR_H3_LINK_HREF_RE.findall(content),
        'sidebar_h2_hrefs': SIDEBAR_H2_LINK_HREF_RE.findall(content),
        'size': len(content),
    }


def normalize_id(s):
    return s.replace('<wbr>', '')


def main(crate_dir, crate_old_dir):
    old_files = find_html_files(crate_old_dir)
    print(f'\n{"="*80}')
    print(f'Crate: {crate_dir}  vs  {crate_old_dir}')
    print(f'{crate_old_dir} contains {len(old_files)} HTML files')

    diffs = []
    for old_path in old_files:
        rel = os.path.relpath(old_path, crate_old_dir).replace('\\', '/')
        cur_path = os.path.join(crate_dir, rel)
        if not os.path.exists(cur_path):
            diffs.append((rel, 'MISSING_FILE', '', '', '', ''))
            continue
        try:
            with open(old_path, 'rb') as f:
                old = f.read().decode('utf-8', errors='replace')
            with open(cur_path, 'rb') as f:
                cur = f.read().decode('utf-8', errors='replace')
        except Exception as e:
            diffs.append((rel, 'READ_ERROR', str(e), '', '', ''))
            continue

        os_ = extract_structure(old)
        cs = extract_structure(cur)

        # 1. h2 id 集对比
        old_h2 = set(normalize_id(x) for x in os_['h2_ids'])
        cur_h2 = set(normalize_id(x) for x in cs['h2_ids'])
        missing_h2 = old_h2 - cur_h2
        if missing_h2:
            diffs.append((rel, 'MISSING_h2_id', f'{len(old_h2)}->{len(cur_h2)}',
                          ','.join(sorted(missing_h2)[:10]), '', ''))

        # 2. h3 id 集对比
        old_h3 = set(normalize_id(x) for x in os_['h3_ids'])
        cur_h3 = set(normalize_id(x) for x in cs['h3_ids'])
        missing_h3 = old_h3 - cur_h3
        if missing_h3:
            diffs.append((rel, 'MISSING_h3_id', f'{len(old_h3)}->{len(cur_h3)}',
                          ','.join(sorted(missing_h3)[:10]), '', ''))

        # 3. section id 集对比
        old_s = set(normalize_id(x) for x in os_['section_ids'])
        cur_s = set(normalize_id(x) for x in cs['section_ids'])
        missing_s = old_s - cur_s
        if missing_s:
            diffs.append((rel, 'MISSING_section_id', f'{len(old_s)}->{len(cur_s)}',
                          ','.join(sorted(missing_s)[:10]), '', ''))

        # 4. sidebar h3/h4 href 集对比（指向的锚点）
        old_sidebar_hrefs = set(normalize_id(x) for x in os_['sidebar_h3_hrefs'])
        cur_sidebar_hrefs = set(normalize_id(x) for x in cs['sidebar_h3_hrefs'])
        missing_sidebar = old_sidebar_hrefs - cur_sidebar_hrefs
        if missing_sidebar:
            diffs.append((rel, 'MISSING_sidebar_anchor', f'{len(old_sidebar_hrefs)}->{len(cur_sidebar_hrefs)}',
                          ','.join(sorted(missing_sidebar)[:10]), '', ''))

    # 输出报告
    print(f'\nFound {len(diffs)} potential deletion issues:')
    by_type = defaultdict(list)
    for d in diffs:
        by_type[d[1]].append(d)
    for typ, items in sorted(by_type.items()):
        print(f'\n--- {typ}: {len(items)} files ---')
        for rel, _, count, missing, _, _ in items[:30]:
            line = f'  {rel}'
            if count: line += f'  count:{count}'
            if missing: line += f'  missing:[{missing}]'
            print(line)
        if len(items) > 30:
            print(f'  ... and {len(items) - 30} more')
    return diffs


if __name__ == '__main__':
    crates_with_old = [
        ('bytes', 'bytes_old'),
        ('coarsetime', 'coarsetime_old'),
        ('ffmpeg_next', 'ffmpeg_next_old'),
        ('ffmpeg_sys_next', 'ffmpeg_sys_next_old'),
        ('quinn', 'quinn_old'),
        ('rcgen', 'rcgen_old'),
        ('rustls_pki_types', 'rustls_pki_types_old'),
        ('tokio', 'tokio_old'),
    ]
    only = sys.argv[1] if len(sys.argv) > 1 else None
    all_diffs = {}
    for cur, old in crates_with_old:
        if only and cur != only:
            continue
        if not os.path.isdir(cur) or not os.path.isdir(old):
            print(f'SKIP {cur} (no _old)')
            continue
        diffs = main(cur, old)
        all_diffs[cur] = diffs
    print('\n' + '='*80)
    print('SUMMARY:')
    total = 0
    for cur, diffs in all_diffs.items():
        print(f'  {cur}: {len(diffs)} files with potential deletions')
        total += len(diffs)
    print(f'  TOTAL: {total}')