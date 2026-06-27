#!/usr/bin/env python3
"""扫描所有已翻译 crate 与 _old 副本，定位被误删的文本段落（<p>/<pre>/<div> 等）。

策略：对每个 HTML 文件，从 cur 中提取所有 <p>/<pre>/<li> 等内容块，在 old 中查找匹配。
翻译后的中文段落不会有英文原文匹配，但如果旧段落里包含 HTML 标签（如 <code>xxx</code>），
可能被结构破坏的标签包裹。
"""
import os
import re
import sys
from collections import defaultdict


# 提取整段 <p>...</p> 文本块（保留结构）
P_RE = re.compile(r'<p[^>]*>([\s\S]*?)</p>', re.DOTALL)
PRE_RE = re.compile(r'<pre[^>]*>([\s\S]*?)</pre>', re.DOTALL)
LI_RE = re.compile(r'<li[^>]*>([\s\S]*?)</li>', re.DOTALL)
# docblock 内部段落
DOCBLOCK_P_RE = re.compile(r'<div class="docblock"[^>]*>([\s\S]*?)</div>(?=\s*<)', re.DOTALL)


def normalize_text(t):
    """归一化 HTML 文本：去除标签、空白归一。"""
    # 解码 HTML 实体
    t = t.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    t = t.replace('&quot;', '"').replace('&#39;', "'")
    # 去除所有 HTML 标签
    t = re.sub(r'<[^>]+>', '', t)
    # 归一空白
    t = re.sub(r'\s+', ' ', t).strip()
    return t


def extract_docblock_paragraphs(content):
    """提取 docblock 内的每个 <p> 文本（归一化后）。"""
    out = []
    for m in DOCBLOCK_P_RE.finditer(content):
        block = m.group(1)
        for p in P_RE.finditer(block):
            out.append(normalize_text(p.group(1)))
    return out


def extract_li_texts(content):
    """提取 sidebar 中的 li 文本。"""
    out = []
    # Only take sidebar TOC
    sb = re.search(r'<section id="rustdoc-toc">([\s\S]*?)</section>', content)
    if not sb:
        return out
    for m in LI_RE.finditer(sb.group(1)):
        out.append(normalize_text(m.group(1)))
    return out


def extract_pre_texts(content):
    """提取 <pre> 内的代码块。"""
    out = []
    for m in PRE_RE.finditer(content):
        out.append(normalize_text(m.group(1)))
    return out


def compare_text_sets(old_texts, cur_texts, label):
    """比较两组文本，找出在 old 但不在 cur 的（结构破坏的可能是子串匹配）。"""
    old_set = set(t for t in old_texts if len(t) > 20)  # 过滤掉太短的无意义片段
    cur_set = set(t for t in cur_texts if len(t) > 20)
    # 中文段落是翻译后的，不在 old_set 里，所以我们需要反向：从 cur 找英文原文
    # 但用户的诉求是"被删"，所以从 old 找 cur 中没有的
    missing = old_set - cur_set
    return missing


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

        # 1. 比较 docblock 内的 <p>
        old_doc_ps = extract_docblock_paragraphs(old)
        cur_doc_ps = extract_docblock_paragraphs(cur)
        # 翻译后段落会有 CJK，所以简单的 set 比较不合适
        # 改为：检查 cur 的 docblock 数量是否显著少于 old（说明有 docblock 整个被删）
        if len(old_doc_ps) - len(cur_doc_ps) > 0:
            # 找出具体哪些 <p> 在 old 里有但 cur 里没有（按纯英文段落过滤）
            # 由于翻译会把英文变成中文，我们只能用 old 里的英文 <p> 在 cur 中查找匹配
            missing_ps = []
            for p in old_doc_ps:
                if not p or len(p) < 30:
                    continue
                # 在 cur 的所有 docblock <p> 里检查
                # 由于 cur 是中文，所以简单的 str in 不会工作
                # 但如果某个 <p> 在 old 里是纯英文，且在 cur 里完全找不到对应（数量减少）
                pass
            # 简单报告数量差异
            if len(cur_doc_ps) < len(old_doc_ps) * 0.95:  # 减少超过 5%
                diffs.append((rel, 'DOCBLOCK_P_COUNT_DROP',
                              f'{len(old_doc_ps)}->{len(cur_doc_ps)}', '', '', ''))

        # 2. 比较 sidebar li 数量（中文 chrome 标签会改文本，只看数量）
        old_lis = extract_li_texts(old)
        cur_lis = extract_li_texts(cur)
        # 只在数量真正减少时报告
        if len(cur_lis) < len(old_lis):
            diffs.append((rel, 'MISSING_sidebar_li', f'{len(old_lis)}->{len(cur_lis)}',
                          '', '', ''))

        # 3. 比较 <pre> 代码块数量（不应该减少）
        old_pres = extract_pre_texts(old)
        cur_pres = extract_pre_texts(cur)
        if len(cur_pres) < len(old_pres):
            diffs.append((rel, 'MISSING_pre',
                          f'{len(old_pres)}->{len(cur_pres)}', '', '', ''))

        # 4. 比较 sidebar 章节数（数量级）
        old_h3_count = len(re.findall(r'<h3[^>]*>', old))
        cur_h3_count = len(re.findall(r'<h3[^>]*>', cur))
        if cur_h3_count < old_h3_count:
            diffs.append((rel, 'MISSING_sidebar_h3', f'{old_h3_count}->{cur_h3_count}',
                          '', '', ''))

        # 5. 比较 docblock 数量级
        old_db_count = len(re.findall(r'<div class="docblock"', old))
        cur_db_count = len(re.findall(r'<div class="docblock"', cur))
        if cur_db_count < old_db_count:
            diffs.append((rel, 'MISSING_docblock', f'{old_db_count}->{cur_db_count}',
                          '', '', ''))

    # 输出报告
    print(f'\nFound {len(diffs)} potential content deletion issues:')
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