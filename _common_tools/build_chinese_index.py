"""从已翻译的 HTML 抽取中文文档内容，构建 MiniSearch 索引。

用法：
    python _common_tools/build_chinese_index.py [--report]

输出：
    static.files/chinese-index/<crate>.json  每 crate 一个
    static.files/chinese-index/all.json      合并所有 crate
    static.files/chinese-index/manifest.json 总条目数 + 每 crate 数量

抽取规则（按文件粒度）：
- 每个 HTML 文件对应一条索引记录
- 抽取字段：
    url:           "quinn/struct.Endpoint.html"  (相对站点根)
    crate:         "quinn"
    title:         从 H1 提取的标识符 (去掉 <wbr> 和类型前缀)
    section:       从 body class 提取 ("struct"/"enum"/"fn"/...)
    desc:          该文件所有 docblock 的纯文本（剥 HTML 标签）
    module_doc:    顶层 docblock 的第一个 <p>
    section_headers: 所有 H2/H3 标题

跳过：
- *_old/ 备份
- static.files/、search.index/、src/、_common_tools/
- 文件名 == all.html（重复目录索引）
- 不含 docblock 的纯重定向页
"""
import os
import re
import sys
import json

# 这些目录要跳过
SKIP_DIRS = {
    'static.files', 'search.index', 'src', '_common_tools',
}

# 这些文件名跳过
SKIP_FILES = {'all.html', 'index.html'}  # index.html 是 crate 入口，已包含在子页面里


def strip_html(s):
    """剥掉 HTML 标签，保留文本。"""
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'&lt;', '<', s)
    s = re.sub(r'&gt;', '>', s)
    s = re.sub(r'&amp;', '&', s)
    s = re.sub(r'&quot;', '"', s)
    s = re.sub(r'&#39;', "'", s)
    s = re.sub(r'&nbsp;', ' ', s)
    s = re.sub(r'<wbr>', '', s)  # 残留下来的 <wbr> 标签
    return s


def extract_title(html):
    """从 <h1> 提取标识符。
    形如：<h1>Struct <span class="struct">End<wbr>point</span>&nbsp;...</h1>
    需要处理 <wbr> 标签。
    """
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    if not m:
        return None
    h1 = m.group(1)
    # 移除所有 <wbr> 和其他标签，只保留 <span>...</span> 内容
    # 先去掉 <wbr> 标签（rustdoc 自动分词）
    h1 = re.sub(r'<wbr\s*/?>', '', h1)
    # 找第一个 <span class="...">...</span>
    span = re.search(r'<span\s+class="[^"]+">([^<]*)</span>', h1)
    if span:
        title = span.group(1).strip()
        # title 中可能还有 <wbr> 残片
        title = re.sub(r'<[^>]+>', '', title)
        return title if title else None
    # 否则取全部文本（去掉 "Struct "/"Enum " 等前缀）
    text = strip_html(h1).strip()
    text = re.sub(r'^(Struct|Enum|Trait|Function|Type|Macro|Module|Union|Constant|Keyword|Attribute|Attribute Macro|Derive Macro|Extern Crate|Impl|Trait Alias|Variant)\s+', '', text)
    return text.split()[0] if text else None


def extract_section(html):
    """从 <body class="rustdoc ..."> 提取类型种类。"""
    m = re.search(r'<body\s+class="rustdoc\s+([^"]+)"', html)
    if not m:
        return ''
    classes = m.group(1).split()
    # 取最后一个作为类型（rustdoc mod crate / rustdoc struct / ...）
    for c in classes:
        if c in ('struct', 'enum', 'trait', 'fn', 'type', 'macro',
                 'mod', 'union', 'constant', 'primitive', 'keyword',
                 'attr', 'derive', 'externcrate', 'traitalias'):
            return c
    return classes[-1] if classes else ''


def extract_docblocks(html):
    """提取所有 docblock div 的纯文本。
    过滤掉未翻译的英文 docblock（一般是 stdlib trait 的默认模板）。
    """
    out = []
    for m in re.finditer(r'<div class=[\'"]docblock[\'"]>', html):
        start = m.end()
        depth = 1
        pos = start
        while pos < len(html) and depth > 0:
            next_open = html.find('<div', pos)
            next_close = html.find('</div>', pos)
            if next_close == -1:
                break
            if next_open != -1 and next_open < next_close:
                depth += 1
                pos = next_open + 4
            else:
                depth -= 1
                pos = next_close + 6
        if depth == 0:
            inner = html[start:pos - 6]
            text = strip_html(inner)
            text = re.sub(r'\s+', ' ', text).strip()
            if text and len(text) > 5:
                # 过滤掉未翻译的英文 docblock（纯英文、无 CJK 字符）
                # 这些通常是 stdlib trait 的默认英文模板，搜中文无意义
                has_cjk = re.search(r'[一-鿿]', text)
                if has_cjk:
                    out.append(text)
    return out


def extract_section_headers(html):
    """提取 H2 章节标题（rustdoc chrome section-header）。"""
    out = []
    # 只用 H2 + class 含 section-header 的（即 chrome 章节标题）
    for m in re.finditer(r'<h2\s+id="([^"]+)"\s+class="([^"]+section-header[^"]*)"[^>]*>(.*?)</h2>', html, re.DOTALL):
        title = strip_html(m.group(3)).strip()
        # 去掉末尾的锚点 §
        title = re.sub(r'\s*§\s*$', '', title)
        if title and title not in out:
            out.append(title)
    return out


def extract_module_doc(html):
    """顶层 docblock（crate index 页或 module index 页的第一个大段描述）。"""
    # 找第一个 <div class="docblock"> 后跟的所有 <p>
    m = re.search(r'<div class=[\'"]docblock[\'"]>([\s\S]*?)</div>', html)
    if not m:
        return ''
    paras = re.findall(r'<p(?:>|\s[^>]*>)([\s\S]*?)</p>', m.group(1))
    text = ' '.join(strip_html(p).strip() for p in paras)
    return re.sub(r'\s+', ' ', text).strip()


def should_skip_dir(d):
    return d.startswith('.') or d in SKIP_DIRS or d.endswith('_old')


def build_index_for_crate(crate_dir, crate_name):
    """抽取一个 crate 下所有 HTML 文件的索引。"""
    entries = []
    for root, dirs, fs in os.walk(crate_dir):
        dirs[:] = [d for d in dirs if not should_skip_dir(d)]
        for fn in fs:
            if not fn.endswith('.html'):
                continue
            if fn in SKIP_FILES:
                continue
            path = os.path.join(root, fn)
            with open(path, 'rb') as f:
                html = f.read().decode('utf-8', errors='ignore')

            docblocks = extract_docblocks(html)
            if not docblocks:
                continue

            title = extract_title(html)
            section = extract_section(html)
            rel = os.path.relpath(path, '.').replace('\\', '/')
            desc = ' '.join(docblocks)
            module_doc = extract_module_doc(html)
            section_headers = extract_section_headers(html)

            entries.append({
                'url': rel,
                'crate': crate_name,
                'title': title or '',
                'section': section,
                'desc': desc[:2000],  # 限制长度，避免单文件索引过大
                'module_doc': module_doc[:500],
                'section_headers': section_headers,
            })
    return entries


def main():
    report_only = '--report' in sys.argv

    # 找所有翻译 crate 目录
    crate_dirs = []
    for d in sorted(os.listdir('.')):
        if should_skip_dir(d):
            continue
        if os.path.isdir(d) and d not in SKIP_DIRS and not d.endswith('_old'):
            crate_dirs.append(d)

    print(f'Found {len(crate_dirs)} crates: {crate_dirs}')
    print()

    all_entries = []
    output_dir = os.path.join('static.files', 'chinese-index')
    os.makedirs(output_dir, exist_ok=True)

    for crate_name in crate_dirs:
        entries = build_index_for_crate(crate_name, crate_name)
        all_entries.extend(entries)
        if entries:
            out_path = os.path.join(output_dir, f'{crate_name}.json')
            if not report_only:
                with open(out_path, 'w', encoding='utf-8') as f:
                    json.dump(entries, f, ensure_ascii=False, separators=(',', ':'))
            print(f'  {crate_name}: {len(entries)} entries -> {out_path}')

    print(f'\nTotal entries: {len(all_entries)}')

    # 写合并文件
    if not report_only:
        all_path = os.path.join(output_dir, 'all.json')
        with open(all_path, 'w', encoding='utf-8') as f:
            json.dump(all_entries, f, ensure_ascii=False, separators=(',', ':'))
        manifest = {
            'total': len(all_entries),
            'crates': {c: sum(1 for e in all_entries if e['crate'] == c) for c in crate_dirs},
        }
        manifest_path = os.path.join(output_dir, 'manifest.json')
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        print(f'\nMerged index: {all_path}')
        print(f'Manifest: {manifest_path}')
    else:
        print('\n(REPORT ONLY — no files written)')


if __name__ == '__main__':
    main()