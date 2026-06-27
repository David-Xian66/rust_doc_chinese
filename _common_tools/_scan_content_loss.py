#!/usr/bin/env python3
"""扫描所有已翻译 crate 与 _old 副本，定位被误删的文本段落（更稳健的版本）。

策略：对每个 HTML 文件，从 docblock 内累计可见文本字符数（剥离标签），
如果 cur 显著少于 old，报告为内容损失候选。
"""
import os
import re
import sys
from collections import defaultdict


def get_visible_text(text):
    """剥离所有 HTML 标签，返回可见文本。"""
    return re.sub(r'<[^>]+>', ' ', text)


def extract_docblock_contents(content):
    """提取所有 docblock 内的可见文本（剥离标签后归一化）。"""
    out = []
    DOCBLOCK_RE = re.compile(r'<div class="docblock"[^>]*>([\s\S]*?)</div>', re.DOTALL)
    for m in DOCBLOCK_RE.finditer(content):
        block = m.group(1)
        # Find the closing </div> by depth tracking (since docblock may contain nested divs)
        # For simplicity here, we use a simple heuristic: stop at first </div></details>
        # Actually, let's just count visible text in the block
        # Don't worry about nested divs for now since rustdoc docblocks rarely have them
        # But to be safe, find deepest balanced </div>
        inner = block
        # Quick check: most docblocks have well-formed content
        visible = get_visible_text(inner)
        visible = re.sub(r'\s+', ' ', visible).strip()
        if visible:
            out.append(visible)
    return out


def get_pre_code(content):
    """提取所有 <pre> 内的可见文本。"""
    out = []
    PRE_RE = re.compile(r'<pre[^>]*>([\s\S]*?)</pre>', re.DOTALL)
    for m in PRE_RE.finditer(content):
        inner = get_visible_text(m.group(1)).strip()
        if inner:
            out.append(inner)
    return out


def find_html_files(root):
    out = []
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in ('static.files',)]
        for f in files:
            if f.endswith('.html'):
                out.append(os.path.join(dirpath, f))
    return out


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
            continue
        try:
            with open(old_path, 'rb') as f:
                old = f.read().decode('utf-8', errors='replace')
            with open(cur_path, 'rb') as f:
                cur = f.read().decode('utf-8', errors='replace')
        except Exception as e:
            continue

        # 1. docblock 总可见文本字符数对比
        old_doc = extract_docblock_contents(old)
        cur_doc = extract_docblock_contents(cur)
        old_total = sum(len(t) for t in old_doc)
        cur_total = sum(len(t) for t in cur_doc)
        # 翻译后可能 CJK 字符比英文短（每个汉字 1 字符 vs 每个英文单词 5+ 字符）
        # 容忍度：如果 cur_total < old_total * 0.3，认为可能是真实丢失
        if old_total > 0 and cur_total < old_total * 0.3:
            diffs.append((rel, 'DOCBLOCK_TEXT_LOSS',
                          f'{old_total}->{cur_total}', '', '', ''))

        # 2. <pre> 代码块数量对比
        old_pres = get_pre_code(old)
        cur_pres = get_pre_code(cur)
        if len(cur_pres) < len(old_pres):
            diffs.append((rel, 'MISSING_pre',
                          f'{len(old_pres)}->{len(cur_pres)}', '', '', ''))

        # 3. <pre> 代码块总字符数对比（代码字符不应大幅减少）
        old_pre_chars = sum(len(p) for p in old_pres)
        cur_pre_chars = sum(len(p) for p in cur_pres)
        if old_pre_chars > 0 and cur_pre_chars < old_pre_chars * 0.5:
            diffs.append((rel, 'PRE_TEXT_LOSS',
                          f'{old_pre_chars}->{cur_pre_chars}', '', '', ''))

    print(f'\nFound {len(diffs)} potential content deletion issues:')
    by_type = defaultdict(list)
    for d in diffs:
        by_type[d[1]].append(d)
    for typ, items in sorted(by_type.items()):
        print(f'\n--- {typ}: {len(items)} files ---')
        for rel, _, count, _, _, _ in items[:30]:
            print(f'  {rel}  count:{count}')
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
            continue
        diffs = main(cur, old)
        all_diffs[cur] = diffs
    print('\n' + '='*80)
    print('SUMMARY:')
    total = 0
    for cur, diffs in all_diffs.items():
        print(f'  {cur}: {len(diffs)} potential content deletions')
        total += len(diffs)
    print(f'  TOTAL: {total}')