"""
检查 rustdoc HTML 输出中的坏链接。

检测以下几类坏链接：
1. href="method@Self::xxx" — rustdoc 的 intra-doc link 占位符未解析（页面通常会有
   对应的 #method.xxx 锚点）
2. href="Type::method" (大写字母开头 + :: + 不含 .html) — rustdoc markdown-style
   source link 未解析
3. href 含 Windows 反斜杠路径（应在生成期已修复，但若仓里仍有则报错）
4. href="xxx.html" 指向不存在的文件（跨 crate 链接除外）
5. #xxx 锚点不存在
6. 其他可疑格式

用法:
    python _common_tools/check_links.py <crate_dir> [crate_name]

    crate_dir:  要扫描的 crate 目录路径（绝对或相对）
    crate_name: crate 名字（如 tokio），用于在报告中过滤跨 crate 链接的预期 404
               （默认与 crate_dir 同名）

    加 --show-anchors    列出每个文件存在的锚点 ID
    加 --show-fixed      列出可能可用的"最近替代锚点"
    加 --pattern <regex>  自定义附加检测正则

脚本只扫描 HTML，不修改任何文件。报告输出到 stdout。
"""

import re
import os
import sys
from collections import defaultdict


def collect_ids(text):
    """收集一个 HTML 文件中所有 id=... 锚点。"""
    return set(re.findall(r'id="([^"]+)"', text))


def collect_hrefs(text):
    """收集所有 href="..." 值，返回 list（保留顺序和重复）。"""
    return re.findall(r'href="([^"]*)"', text)


def find_closest_anchor(target, anchors):
    """在给定锚点集合中找最相近的（用于 'method.xxx' 类的 target）。

    匹配规则:
      - 完全相等 → 返回 target
      - target 含 'method.foo' 时，找任意 'method.xxx'（子串 / Levenshtein 太慢）
      - 否则返回 None
    """
    if target in anchors:
        return target
    # 尝试 method.* 这种短形式
    if 'method.' in target:
        suffix = target.split('method.')[-1]
        # 找相同前缀的 method 锚点
        for a in anchors:
            if a.startswith('method.') and a.endswith('.' + suffix.split('.')[-1] if '.' in suffix else suffix):
                return a
    return None


def scan_file(path, crate_name, show_anchors=False, extra_patterns=None):
    """扫描单个 HTML 文件，返回坏链接列表。

    每条坏链接形如:
        {
            'path': str,
            'kind': str,        # 坏链接类型
            'href': str,        # 原始 href
            'suggestion': str,  # 推荐的修复目标 (可能为空)
            'context': str,     # 周围 80 字符的文本（去标签后）
        }
    """
    try:
        with open(path, 'rb') as f:
            text = f.read().decode('utf-8', errors='replace')
    except OSError:
        return []

    bad = []
    ids = collect_ids(text)
    if show_anchors:
        print(f'  [anchors in {os.path.basename(path)}]: {sorted(ids)[:20]}'
              + (' ...' if len(ids) > 20 else ''))

    dirpath = os.path.dirname(path)

    for h in collect_hrefs(text):
        if not h:
            continue

        # 类别 1: method@Self::xxx 占位符
        if h.startswith('method@Self::') or h.startswith('tymethod@Self::') \
                or h.startswith('Self::') or 'method@Self::' in h:
            method_name = h.split('::')[-1]
            suggestion = f'#{h.split("@")[-1].replace("::", ".")}'  # e.g. #method.new_multi_thread
            # 验证这个锚点是不是真的存在
            target_anchor = suggestion.lstrip('#')
            if target_anchor not in ids:
                # 找最近替代
                alt = find_closest_anchor(target_anchor, ids)
                if alt:
                    suggestion = f'#{alt} (closest match)'
                else:
                    suggestion += ' (NOT FOUND on page)'
            bad.append({
                'path': path, 'kind': 'method@Self:: placeholder',
                'href': h, 'suggestion': suggestion,
            })
            continue

        # 类别 2: Type::method 占位符（大写起 + :: + 无 .html）
        if re.match(r'^[A-Z][a-zA-Z0-9_]*::[a-zA-Z_]', h) and '.html' not in h:
            # 推断锚点：type.method
            parts = h.split('::')
            type_name = parts[0].lower()
            method_name = parts[-1]
            suggestion = f'#{type_name}.{method_name} (likely not present)'
            bad.append({
                'path': path, 'kind': 'Type::method placeholder',
                'href': h, 'suggestion': suggestion,
            })
            continue

        # 类别 3: Windows 反斜杠
        if '\\' in h:
            fixed = h.replace('\\', '/')
            bad.append({
                'path': path, 'kind': 'windows backslash',
                'href': h, 'suggestion': fixed,
            })
            continue

        # 类别 4: href 指向不存在的 .html
        if h.endswith('.html') and not h.startswith('#') and not h.startswith('http'):
            # 拼绝对路径
            if h.startswith('/') or re.match(r'^[a-zA-Z]:', h):
                target = h
            else:
                # 相对路径，从文件所在目录解析
                if '/' in h:
                    target = os.path.normpath(os.path.join(dirpath, h.split('#')[0]))
                else:
                    target = os.path.join(dirpath, h.split('#')[0])
            # 跨 crate 链接忽略
            if not os.path.exists(target):
                # 检查是否跨 crate / 跨域
                is_external = any(
                    h.startswith(p) for p in ('http://', 'https://', 'mailto:', '//')
                )
                is_src_link = '/src/' in h or h.startswith('../src/')
                is_std_link = 'doc.rust-lang.org' in h
                if not (is_external or is_src_link or is_std_link):
                    bad.append({
                        'path': path, 'kind': 'broken file link',
                        'href': h, 'suggestion': 'FILE NOT FOUND: ' + target,
                    })
            continue

        # 类别 5: #xxx 锚点检查（指向同一页的）
        if h.startswith('#') and len(h) > 1:
            anchor = h[1:]
            # 处理 #foo#bar 等奇异
            anchor = anchor.split('#')[0]
            if anchor not in ids:
                # 这可能是 rustdoc 标题里 '#X' 被包成 URL fragment 的情况，跳过
                bad.append({
                    'path': path, 'kind': 'broken anchor (#xxx)',
                    'href': h, 'suggestion': f'ANCHOR #{anchor} NOT FOUND',
                })
            continue

        # 类别 6: 额外自定义正则
        if extra_patterns:
            for pat in extra_patterns:
                if re.search(pat, h):
                    bad.append({
                        'path': path, 'kind': f'custom regex match ({pat})',
                        'href': h, 'suggestion': '',
                    })
                    break

    return bad


def scan_crate(crate_dir, crate_name=None, show_anchors=False,
               extra_patterns=None, file_filter=None):
    """扫描整个 crate 目录。"""
    crate_name = crate_name or os.path.basename(crate_dir.rstrip('/\\'))
    results = []
    file_count = 0

    for root, dirs, files in os.walk(crate_dir):
        for fn in files:
            if not fn.endswith('.html'):
                continue
            if file_filter and not file_filter(fn):
                continue
            full = os.path.join(root, fn)
            file_count += 1
            bad = scan_file(full, crate_name,
                            show_anchors=show_anchors,
                            extra_patterns=extra_patterns)
            for b in bad:
                b['path'] = os.path.relpath(full, crate_dir)
            results.extend(bad)

    return results, file_count


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    crate_dir = sys.argv[1]
    crate_name = sys.argv[2] if len(sys.argv) > 2 else None

    show_anchors = '--show-anchors' in sys.argv
    extra_patterns = []
    if '--pattern' in sys.argv:
        i = sys.argv.index('--pattern')
        if i + 1 < len(sys.argv):
            extra_patterns.append(sys.argv[i + 1])

    results, file_count = scan_crate(
        crate_dir, crate_name,
        show_anchors=show_anchors,
        extra_patterns=extra_patterns or None,
    )

    print(f'Scanned {file_count} HTML files in {crate_dir}')

    if not results:
        print('No broken links found.')
        return 0

    # 按类型 + 文件聚合
    by_kind = defaultdict(lambda: defaultdict(list))
    for r in results:
        by_kind[r['kind']][r['path']].append(r)

    for kind in sorted(by_kind):
        files_with_kind = by_kind[kind]
        total = sum(len(v) for v in files_with_kind.values())
        print(f'\n=== {kind}: {total} occurrences in {len(files_with_kind)} files ===')
        for f in sorted(files_with_kind)[:50]:
            entries = by_kind[kind][f]
            for e in entries[:3]:  # 每文件最多显示 3 个示例
                sug = f'  → {e["suggestion"]}' if e['suggestion'] else ''
                print(f'  {f}: href="{e["href"]}"{sug}')
            if len(entries) > 3:
                print(f'    ... and {len(entries) - 3} more in this file')
        if len(files_with_kind) > 50:
            print(f'  ... and {len(files_with_kind) - 50} more files')

    return 1 if results else 0


if __name__ == '__main__':
    sys.exit(main())