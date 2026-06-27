#!/usr/bin/env python3
"""严格模块级 audit：扫描 rustdoc HTML 中容易漏译的位置：

1. <dl class="item-table"><dt>...</dt><dd>UNTRANSLATED_TEXT</dd></dl>
   —— module index 页的 struct/fn 简短描述
2. <h2 id="..." class="section-header"> 标题里的英文段落
3. <h3> 章节标题里的英文
4. 模块 docblock 内 <details class="toggle top-doc"><div class="docblock"> 整段英文

与 _strict_p_audit.py 的区别：本脚本不只检查 <div class="docblock"><p>...</p></div>，
而是扫描更广的位置，专门抓"rustdoc 模块索引里"的英文描述。

用法：
  python _common_tools/_strict_module_audit.py <crate_dir>
"""
import os
import re
import sys

# 已知的 chrome 标签（不算漏译）
CHROME_TERMS = {
    'Crate', 'Module', 'Crate Items', 'Module Items', 'Modules', 'Macros',
    'Structs', 'Enums', 'Traits', 'Functions', 'Type Definitions', 'Constants',
    'Variants', 'Fields', 'Implementations', 'Trait Implementations',
    'Required Methods', 'Provided Methods', 'Associated Types',
    'Associated Constants', 'Blanket Implementations', 'Foreign Implementations',
    'Auto Trait Implementations', 'Implementors', 'Sections',
    # H2 section header patterns we recognize
    'Tuple Fields', 'Tuple Structs', 'Trait Implementations',
    'Notable traits for &T', 'Notable traits for &[T]', 'Notable traits for &mut [T]',
    # rustdoc 自动生成的标题（不能翻译）
    'Methods from Deref<Target=[u8]>',
    'Methods from Deref<Target = [u8]>',
    'Implementations on Foreign Types',
    'Auto trait implementations',
    'Blanket implementations',
    'Implementors',
}

# Variant 段标题的判定（这些是 enum/struct variant 标识符，不应翻译）
VARIANT_H3_PATTERN = re.compile(
    r'<h3(?:\s+[^>]*)?>.*?</h3>\s*<a\s+class="variant"',
    re.DOTALL
)

# 已知忽略的 h3 模式（rustdoc 自动生成的 trait impl 标题）
H3_IGNORE_RE = re.compile(
    r'^impl\b.*for\s'         # impl Foo for Bar
    r'|^impl\b[^a-zA-Z]'      # impl Foo (no body)
    r'|^Auto trait implementations'
    r'|^Blanket implementations'
    r'|^Notable traits for'   # rustdoc 自动生成的 "Notable traits for X"
)

# h3 with class="code-header" 是代码标识符（variant/field 名），不翻译
CODE_HEADER_H3_RE = re.compile(
    r'<h3\s+class="code-header"',
)

CJK_RE = re.compile(r'[一-鿿]')


def has_cjk(s):
    return bool(CJK_RE.search(s))


def strip_tags(s):
    return re.sub(r'<[^>]+>', '', s).strip()


def audit_module_index(html, path):
    """扫描 module index 页的 <dl class="item-table"> 与 <h2/h3> 标题。
    返回 [(category, original_text, file, position)] 列表。
    """
    issues = []

    # 1) <dl class="item-table"><dt>...<dd>UNTRANSLATED</dd></dl>
    dl_pattern = re.compile(
        r'<dl\s+class="item-table">(.*?)</dl>', re.DOTALL
    )
    dd_pattern = re.compile(
        r'<dt>(.*?)</dt>\s*<dd>(.*?)</dd>', re.DOTALL
    )
    for dl in dl_pattern.finditer(html):
        for dd in dd_pattern.finditer(dl.group(1)):
            dt_text = strip_tags(dd.group(1))
            dd_raw = dd.group(2)
            dd_text = strip_tags(dd_raw)
            # 跳过 chrome 标签
            if dt_text in CHROME_TERMS:
                continue
            # 跳过全 CJK 的
            if has_cjk(dd_text):
                continue
            # 跳过短文本（标题等）
            if len(dd_text) < 5:
                continue
            # 跳过纯代码或链接
            if dd_text.startswith('[') and dd_text.endswith(']'):
                continue
            # 检查 dd 内部是否含 std 链入（trait method 的 src 链接）—— 跳过
            # 这里 dt 是 type 名（如 OwnedPermit），所以都是 own
            issues.append(('item-table-dd', dd_text, path, dd.start()))

    # 2) <h2 id="..." class="section-header"> 标题里的英文
    h2_pattern = re.compile(
        r'<h2\s+id="([^"]+)"\s+class="[^"]*section-header[^"]*"[^>]*>(.*?)</h2>',
        re.DOTALL
    )
    for m in h2_pattern.finditer(html):
        anchor = m.group(1)
        body = strip_tags(m.group(2)).strip()
        # 'trait' / 'Variant name' / etc. 都是 chrome 标签
        if anchor in CHROME_TERMS or body in CHROME_TERMS:
            continue
        if not body or has_cjk(body):
            continue
        if len(body) < 3:
            continue
        # 这是 section title，已经在 chrome 翻译范围内
        issues.append(('h2-section-header', body, path, m.start()))

    # 3) <h3>...</h3> 章节标题（排除 trait impl 标题 + variant 标题）
    h3_pattern = re.compile(
        r'<h3(?:\s+[^>]*)?>(.*?)</h3>', re.DOTALL
    )
    for m in h3_pattern.finditer(html):
        body = strip_tags(m.group(1)).strip()
        if not body or has_cjk(body):
            continue
        if len(body) < 3:
            continue
        # 跳过 chrome 标签（重复检测）
        if body in CHROME_TERMS:
            continue
        # 跳过 trait impl 标题（impl X for Y）
        if H3_IGNORE_RE.match(body):
            continue
        # 跳过有 <a class="src" href=...> 的（trait method heading）
        if 'class="src"' in m.group(0):
            continue
        # 跳过 code-header h3（variant/field 标识符，不翻译）
        if CODE_HEADER_H3_RE.search(m.group(0)):
            continue
        # 跳过 h3 里有 <a class="mod"> 或 <a class="struct"> 链入的（auto-derived）
        h3_full = m.group(0)
        if re.search(r'class="(mod|struct|trait|enum|fn|primitive|macro|associatedtype|associatedconstant|tymethod|method|field|variant)"', h3_full):
            # 检查是否有 where 字样（impl 的 where 子句）
            if 'where' in body or ' for ' in body:
                continue
        # 跳过 variant 段（<a class="variant" ...> 紧跟其后）
        # 因为 variant 名是标识符（如 Client/Server/Burst），不应翻译
        end_pos = m.end()
        if VARIANT_H3_PATTERN.match(html[m.start():m.start()+500]):
            continue
        # 跳过 h3 内含 <code>xxx</code> 的（这些是模块名/类型名 + 普通词的组合，如 "oneshot channel"）
        if re.search(r'<code>[^<]+</code>', h3_full):
            continue
        issues.append(('h3-heading', body, path, m.start()))

    # 4) 模块级 docblock <details class="toggle top-doc"> 内的整段 <p>
    top_doc_pattern = re.compile(
        r'<details\s+class="toggle\s+top-doc"[^>]*>(.*?)</details>',
        re.DOTALL
    )
    for m in top_doc_pattern.finditer(html):
        body = m.group(1)
        for p in re.finditer(r'<p[^>]*>(.*?)</p>', body, re.DOTALL):
            text = strip_tags(p.group(1))
            if not has_cjk(text) and len(text) > 15:
                # 跳过 p 含 <code> 子节点（视为代码示例）
                p_html = p.group(0)
                if re.search(r'<code[\s>]', p_html):
                    continue
                # 跳过看似代码的（; { = 等代码标记多）
                code_markers = sum(text.count(c) for c in [';', '{', '}', '::', '(', ')'])
                if code_markers >= 3:
                    continue
                issues.append(('top-doc-p', text, path, p.start()))

    return issues


def audit_file(path):
    """扫描单个 HTML 文件的 module index 类漏译。仅扫描 module index 页（含 item-table 的）。"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
    except Exception:
        return []

    # 只扫含 <dl class="item-table"> 或 <details class="toggle top-doc"> 的文件
    if 'class="item-table"' not in html and 'toggle top-doc' not in html:
        return []

    return audit_module_index(html, path)


def main():
    if len(sys.argv) < 2:
        print('Usage: _strict_module_audit.py <crate_dir>')
        sys.exit(1)
    crate_dir = sys.argv[1]
    if not os.path.isdir(crate_dir):
        print(f'Not a directory: {crate_dir}')
        sys.exit(1)

    total_issues = 0
    by_category = {}
    files_with_issues = set()

    for top, dirs, fs in os.walk(crate_dir):
        # 跳过 _old 备份
        dirs[:] = [d for d in dirs if not d.endswith('_old') and not d.startswith('.')]
        for fn in fs:
            if not fn.endswith('.html'):
                continue
            path = os.path.join(top, fn)
            issues = audit_file(path)
            if issues:
                files_with_issues.add(path)
                for cat, text, p, pos in issues:
                    by_category.setdefault(cat, []).append((text, p, pos))
                    total_issues += 1

    print(f'Audited {crate_dir}')
    print(f'Files with issues: {len(files_with_issues)}')
    print(f'Total issues: {total_issues}')
    print()
    for cat, items in sorted(by_category.items()):
        print(f'\n=== {cat}: {len(items)} occurrences ===')
        # 去重
        seen = set()
        for text, p, pos in items:
            key = (text[:80], p)
            if key in seen:
                continue
            seen.add(key)
            print(f'  {p}: {text[:120]}')

    return 0 if total_issues == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
