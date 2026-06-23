"""严格 per-`<p>` 审计：检查每个 docblock 内每个 <p> 是否单独含 CJK。

为什么需要这个：
现有的 comprehensive_audit.py 检查整个 docblock 是否含 CJK，前几个 <p> 有 CJK 就过了。
但当 docblock 内有 4 个 <p>，前 3 个译了最后 1 个漏译，整个 docblock 仍含 CJK，
audit 不会报错。这是已发现的漏译漏洞。

修复：对每个 <p> 单独检查。

用法：
    python _common_tools/_strict_p_audit.py <crate_dir>

输出：未翻译 <p> 的列表（含所在文件、上下文、文本）。
"""
import re
import os
import sys


def find_docblocks(text):
    """找所有 docblock div。class 可能 'docblock' 或 "docblock"。

    返回 [(start, end, inner)] 列表。

    注意：rustdoc 的 docblock 内可能嵌套 <div class="example-wrap"> 包含 <pre>，
    所以结尾 </div> 必须用 lazy 匹配配合 docblock 边界检测。
    """
    results = []
    # 用 lazy 匹配 — 但需要确认 <div> 嵌套深度
    pattern = re.compile(r'<div class=[\'"]docblock[\'"]>', re.DOTALL)
    for m in pattern.finditer(text):
        start = m.end()
        # 从 start 开始追踪 <div> 和 </div> 嵌套深度
        depth = 1
        pos = start
        while pos < len(text) and depth > 0:
            next_open = text.find('<div', pos)
            next_close = text.find('</div>', pos)
            if next_close == -1:
                break
            if next_open != -1 and next_open < next_close:
                depth += 1
                pos = next_open + 4
            else:
                depth -= 1
                pos = next_close + 6
        if depth == 0:
            results.append((m.start(), pos, text[start:pos - 6]))
    return results


def find_preceding_id(text, pos):
    """找 pos 之前最近的 id 锚点（如 method.X、tymethod.X 等）。

    排除来自标准库的方法（rustdoc 的 src 链接指向 doc.rust-lang.org）。
    """
    prefix = text[:pos]
    ids = re.findall(
        r'id="(method\.[^"]+|tymethod\.[^"]+|variant\.[^"]+|structfield\.[^"]+|impl-[^"]+)"',
        prefix,
    )
    if not ids:
        return None
    last_id = ids[-1]

    # 找 id 出现位置
    id_pos = prefix.rfind(f'id="{last_id}"')

    # 关键修复：限制搜索范围到当前 section（下一个 id 之前）
    # 否则可能匹配到下一段的 src href
    rest = text[id_pos:]
    next_id_match = re.search(
        r'id="(?:method\.|tymethod\.|variant\.|structfield\.|impl-)[^"]+"',
        rest[len(f'id="{last_id}"'):],
    )
    if next_id_match:
        section_end = id_pos + len(f'id="{last_id}"') + next_id_match.start()
        after = text[id_pos:section_end]
    else:
        after = text[id_pos:id_pos + 2000]

    src_match = re.search(r'<a class="src(?:\s+rightside)?"[^>]+href="([^"]+)"', after)
    if src_match:
        href = src_match.group(1)
        if 'doc.rust-lang.org' in href:
            return None  # STD lib 来源，跳过
        if href.endswith('.rs.html'):
            # 是 own crate 的源（如 ../src/quinn/...）？
            # quinn: ../src/quinn/...
            # tokio: ../src/tokio/...
            # rustls_pki_types: ../src/rustls_pki_types/...
            # 看 href 含不含有意义的 crate 标识
            if not any(c in href for c in ('/src/quinn/', '/src/tokio/',
                                            '/src/rustls_pki_types/')):
                return None
    return last_id


def strip_html(s):
    """剥掉 HTML 标签，保留文本。"""
    return re.sub(r'<[^>]+>', '', s).strip()


def has_cjk(s):
    return bool(re.search(r'[一-鿿]', s))


def audit_crate(crate_dir):
    """扫描整个 crate，输出每个未翻译 <p> 的位置。"""
    issues = []

    for root, dirs, files in os.walk(crate_dir):
        for fn in files:
            if not fn.endswith('.html'):
                continue
            path = os.path.join(root, fn)
            with open(path, 'rb') as f:
                text = f.read().decode('utf-8')

            for db_start, db_end, db_inner in find_docblocks(text):
                # 找最近的方法/字段 id（排除 STD 来源）
                ctx_id = find_preceding_id(text, db_start)
                if not ctx_id:
                    continue

                # 每个 <p> - rustdoc 的 <p> 是裸标签 <p> (无属性)，也可能是 <p class="...">
                # 必须排除 <pre>、<param>、<path>、<polygon> 等以 <p 起头的标签
                # 用 <p(>|[\s]) 限定：<p> 后接空白字符或 >，但不接 'r','a','a','o'
                for p in re.findall(r'<p(?:>|\s[^>]*>)([\s\S]*?)</p>', db_inner):
                    stripped = strip_html(p)
                    if len(stripped) < 5:
                        continue
                    if not has_cjk(stripped) and len(re.findall(r'[A-Za-z]', stripped)) > 15:
                        issues.append({
                            'path': os.path.relpath(path, crate_dir),
                            'id': ctx_id,
                            'text': stripped,
                            'full_p': p,
                        })

    return issues


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    crate_dir = sys.argv[1]
    issues = audit_crate(crate_dir)

    print(f'Audited {crate_dir}')
    print(f'Found {len(issues)} untranslated <p> in docblocks:\n')

    # 按文件聚合
    by_file = {}
    for i in issues:
        by_file.setdefault(i['path'], []).append(i)

    for f in sorted(by_file):
        print(f'=== {f} ({len(by_file[f])} issues) ===')
        for issue in by_file[f][:10]:
            print(f"  [{issue['id']}]")
            print(f"    {issue['text'][:200]}")
            if len(issue['text']) > 200:
                print(f"    ... ({len(issue['text'])} chars total)")
        if len(by_file[f]) > 10:
            print(f'  ... and {len(by_file[f]) - 10} more in this file')
        print()

    return 0 if not issues else 1


if __name__ == '__main__':
    sys.exit(main())