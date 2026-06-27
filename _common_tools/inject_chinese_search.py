"""在每个 HTML 文件的 <head> 中注入中文搜索脚本和 MiniSearch 库。
用法：
    python _common_tools/inject_chinese_search.py [--report]
    python _common_tools/inject_chinese_search.py --fix-broken-paths

注入位置：在 <meta name="rustdoc-vars"> 之后
注入片段（绝对路径，根部署下适用于所有页面深度）：
    <script src="/static.files/minisearch.min.js"></script>
    <script src="/static.files/chinese-search-3aa25361.js"></script>

要点：
- bytes 模式
- 跳过 _old/, static.files/, src/, search.index/
- 幂等：已含 minisearch.min.js 的文件跳过；已含当前 chinese-search 哈希的跳过；
  含旧哈希的则改写为新哈希（rename 兼容）。
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


# 当前 chinese-search 脚本的文件名（content hash）。每次发布新版本时改这里。
# 旧文件名必须放在 OLD_SCRIPT_NAME 中以便迁移。
SCRIPT_NAME = b'chinese-search-3aa25361.js'
OLD_SCRIPT_NAME = b'chinese-search-82c803ae.js'

# 绝对路径：根部署（Cloudflare Pages / 本地 http.server）下，深度无关地解析到 /static.files/...
SCRIPT_BLOCK = (
    b'<script src="/static.files/minisearch.min.js"></script>'
    b'<script src="/static.files/' + SCRIPT_NAME + b'"></script>'
)

# 用于 --fix-broken-paths：将已注入的错误相对路径替换为绝对路径
# 同时处理两种错误形式：
# 1. `../static.files/...`  —— 嵌套页面 (depth>=2) 解析成 /crate/static.files/... (错)
# 2. `static.files/...`     —— 缺前导 /，仅在站点根有效
# 都改为 `/static.files/...`，所有页面深度都能正确解析。
BROKEN_RE = re.compile(
    br'<script\s+src="(?:\.\./)?static\.files/(minisearch\.min\.js|chinese-search[^"]*\.js)"></script>'
)
ABSOLUTE_REPL = (
    br'<script src="/static.files/\1"></script>'
)

# 检测已注入的 chinese-search 引用（任何哈希）
INJECTED_RE = re.compile(
    br'<script src="/static\.files/chinese-search-[a-f0-9]+\.js"></script>'
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


# 检测已注入的 chinese-search 引用（任何 path 前缀形式 + 任何哈希）
CHINESE_SEARCH_REF_RE = re.compile(
    rb'<script\s+src="(?:/|\.\./)?static\.files/chinese-search-([a-f0-9]+)\.js"></script>'
)


def main():
    if '--fix-broken-paths' in sys.argv:
        fix_broken_paths()
        return

    report_only = '--report' in sys.argv
    root = '.'
    total = 0
    modified = 0
    migrated = 0
    path_fixed = 0
    skipped = 0

    current_ref = b'<script src="/static.files/' + SCRIPT_NAME + b'"></script>'
    current_hash = SCRIPT_NAME.decode('ascii').rsplit('-', 1)[-1].rsplit('.', 1)[0]

    for top, dirs, fs in os.walk(root):
        dirs[:] = [d for d in dirs if not should_skip_dir(d)]
        for fn in fs:
            if not fn.endswith('.html'):
                continue
            path = os.path.join(top, fn)
            total += 1

            with open(path, 'rb') as f:
                before = f.read()

            new_content = before
            file_migrated = False
            file_path_fixed = False

            # 1. 改写任何 chinese-search 引用：无论 path 前缀是 /、../ 还是无，
            #    无论哈希是旧的还是当前的，都归一为 `/static.files/<CURRENT>.js`。
            def normalize(m):
                nonlocal file_migrated, file_path_fixed
                old_hash = m.group(1).decode('ascii')
                if old_hash != current_hash:
                    file_migrated = True
                # 总是输出绝对路径（/static.files/...），即使之前就是
                return current_ref

            new_content = CHINESE_SEARCH_REF_RE.sub(normalize, new_content)

            # 2. 检测最终是否含当前哈希
            has_current = current_ref in new_content

            # 3. 路径修复：minisearch.min.js 也用 bare `static.files/...` 形式时
            #    （仅在 index.html 这种站点根页面出现），改为绝对路径
            if b'<script src="static.files/minisearch.min.js"></script>' in new_content and current_ref in new_content:
                # Already has current chinese-search; just fix the minisearch path
                new_content = new_content.replace(
                    b'<script src="static.files/minisearch.min.js"></script>',
                    b'<script src="/static.files/minisearch.min.js"></script>',
                )
                file_path_fixed = True

            # 4. 完全没注入过 chinese-search 但有 rustdoc-vars 且没 minisearch
            if not has_current and b'<meta name="rustdoc-vars"' in new_content and b'minisearch.min.js' not in new_content:
                anchor = b'<meta name="rustdoc-vars"'
                idx = new_content.find(anchor)
                if idx >= 0:
                    end = new_content.find(b'>', idx)
                    if end >= 0:
                        insert_pos = end + 1
                        new_content = new_content[:insert_pos] + SCRIPT_BLOCK + new_content[insert_pos:]

            if new_content == before:
                if has_current:
                    skipped += 1
                continue

            if not report_only:
                with open(path, 'wb') as f:
                    f.write(new_content)
            modified += 1
            if file_migrated:
                migrated += 1
            if file_path_fixed:
                path_fixed += 1

    print(f'Total HTML files scanned: {total}')
    if report_only:
        print('(REPORT ONLY)')
    print(f'Modified: {modified}  (hash migrated: {migrated}, path fixed: {path_fixed})')
    print(f'Already injected (current hash): {skipped}')


if __name__ == '__main__':
    main()
