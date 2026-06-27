"""在每个 HTML 文件的 <head> 中注入中文搜索脚本和 MiniSearch 库。
用法：
    python _common_tools/inject_chinese_search.py [--report]
    python _common_tools/inject_chinese_search.py --fix-broken-paths

注入位置：在 <meta name="rustdoc-vars"> 之后
注入片段（绝对路径，根部署下适用于所有页面深度）：
    <script src="/static.files/minisearch.min.js"></script>
    <script src="/static.files/chinese-search-8f86f8c0.js"></script>

要点：
- bytes 模式
- 跳过 _old/, static.files/, src/, search.index/
- 幂等：含 'chinese-search.js' 的文件跳过
- 使用绝对路径（/static.files/...）以兼容嵌套子目录页面（如 /tokio/runtime/...）
  —— 之前用 ../static.files/... 在 depth>=2 的页面会解析成 /tokio/static.files/...（错）
"""
import os
import re
import sys

SKIP_DIRS = {
    'static.files', 'search.index', 'src', '_common_tools',
}


def should_skip_dir(d):
    return d.startswith('.') or d in SKIP_DIRS or d.endswith('_old')


# 绝对路径：根部署（Cloudflare Pages / 本地 http.server）下，深度无关地解析到 /static.files/...
SCRIPT_BLOCK = (
    b'<script src="/static.files/minisearch.min.js"></script>'
    b'<script src="/static.files/chinese-search-8f86f8c0.js"></script>'
)

# 用于 --fix-broken-paths：将已注入的错误相对路径替换为绝对路径
BROKEN_RE = re.compile(
    br'<script\s+src="\.\./static\.files/(minisearch\.min\.js|chinese-search\.js)"></script>'
)
ABSOLUTE_REPL = (
    br'<script src="/static.files/\1"></script>'
)


def fix_broken_paths():
    """将已注入的相对路径 ../static.files/X.js 改为绝对 /static.files/X.js。
    适用于现有 HTML 文件（之前 depth>=2 的页面路径是错的，脚本根本没加载）。"""
    total = 0
    fixed = 0
    for top, dirs, fs in os.walk('.'):
        dirs[:] = [d for d in dirs if not should_skip_dir(d)]
        for fn in fs:
            if not fn.endswith('.html'):
                continue
            path = os.path.join(top, fn)
            total += 1
            with open(path, 'rb') as f:
                content = f.read()
            if b'../static.files/' not in content:
                continue
            new_content = BROKEN_RE.sub(ABSOLUTE_REPL, content)
            if new_content != content:
                with open(path, 'wb') as f:
                    f.write(new_content)
                fixed += 1
    print(f'Total HTML files scanned: {total}')
    print(f'Fixed broken script paths: {fixed}')


def main():
    if '--fix-broken-paths' in sys.argv:
        fix_broken_paths()
        return

    report_only = '--report' in sys.argv
    root = '.'
    total = 0
    modified = 0
    skipped = 0

    for top, dirs, fs in os.walk(root):
        dirs[:] = [d for d in dirs if not should_skip_dir(d)]
        for fn in fs:
            if not fn.endswith('.html'):
                continue
            path = os.path.join(top, fn)
            total += 1

            with open(path, 'rb') as f:
                before = f.read()

            if b'chinese-search.js' in before:
                skipped += 1
                continue

            # 在 <meta name="rustdoc-vars" ...> 之后插入
            anchor = b'<meta name="rustdoc-vars"'
            idx = before.find(anchor)
            if idx < 0:
                continue  # 不含 rustdoc-vars，跳过

            # 找到该 meta 标签的结束 > （注意自闭合）
            end = before.find(b'>', idx)
            if end < 0:
                continue
            insert_pos = end + 1
            after = before[:insert_pos] + SCRIPT_BLOCK + before[insert_pos:]

            if not report_only:
                with open(path, 'wb') as f:
                    f.write(after)
            modified += 1

    print(f'Total HTML files scanned: {total}')
    if report_only:
        print('(REPORT ONLY)')
    print(f'Modified: {modified}')
    print(f'Already injected: {skipped}')


if __name__ == '__main__':
    main()
