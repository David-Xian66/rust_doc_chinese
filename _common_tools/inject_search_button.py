"""在每个 HTML 文件的 <rustdoc-topbar> 中插入搜索按钮。

用法：
    python _common_tools/inject_search_button.py [--report]

要点（CLAUDE.md 已记录的坑）：
- bytes 模式读写，避免 Python 文本模式规范化 CRLF 破坏 UTF-8 多字节字符
- 跳过 <crate>_old/ 备份目录（这些不会被部署）
- 跳过 static.files/（资源目录）
- 跳过搜索索引目录（它们不是 HTML）
- 跳过 src/（源代码 HTML）
- 跳过 search.index/（碎片数据）
- 幂等：含 'id="search-button"' 的文件跳过

注入片段（在 </rustdoc-topbar> 之前）：
    <div class="search-menu"><a id="search-button" href="?search#">搜索</a></div>
"""
import os
import re
import sys

TOPBAR_RE = re.compile(b'<rustdoc-topbar>.*?</rustdoc-topbar>', re.DOTALL)
ID_TAG = b'id="search-button"'
SEARCH_LINK = b'<div class="search-menu"><a id="search-button" href="?search#">\xe6\x90\x9c\xe7\xb4\xa2</a></div></rustdoc-topbar>'

# 跳过这些顶层目录
SKIP_TOP_DIRS = {
    '_old',
    'static.files',
    'search.index',
    'src',
    '_common_tools',
    '_redirects',  # 不存在但是兜底
    '_headers',    # 不存在但是兜底
}

# 跳过名字包含 _old 的目录（如 enigo_old、quinn_old）
def should_skip_dir(dirname):
    if dirname.startswith('.'):
        return True
    if dirname in SKIP_TOP_DIRS:
        return True
    if dirname.endswith('_old'):
        return True
    return False


def inject_search_button(html_bytes):
    """在每个 <rustdoc-topbar> 里加搜索按钮。返回 (new_bytes, modified_bool)。"""
    if ID_TAG in html_bytes:
        return html_bytes, False  # 已注入，跳过

    def replace_topbar(m):
        original = m.group(0)
        # 在 </rustdoc-topbar> 之前插入搜索按钮
        if b'</rustdoc-topbar>' in original:
            return original.replace(b'</rustdoc-topbar>', SEARCH_LINK)
        return original

    new_bytes = TOPBAR_RE.sub(replace_topbar, html_bytes)
    return new_bytes, new_bytes != html_bytes


def main():
    report_only = '--report' in sys.argv
    root = '.'

    total_files = 0
    modified = 0
    skipped_already = 0
    skipped_topbar_absent = 0

    for top, dirs, fs in os.walk(root):
        # 过滤要进入的目录（修改 dirs 列表）
        dirs[:] = [d for d in dirs if not should_skip_dir(d)]

        for fn in fs:
            if not fn.endswith('.html'):
                continue
            path = os.path.join(top, fn)
            total_files += 1

            with open(path, 'rb') as f:
                before = f.read()

            after, was_modified = inject_search_button(before)

            if not was_modified:
                if b'<rustdoc-topbar>' in before and ID_TAG in before:
                    skipped_already += 1
                elif b'<rustdoc-topbar>' in before:
                    skipped_topbar_absent += 1
                else:
                    pass  # redirect stub 等
                continue

            if not report_only:
                with open(path, 'wb') as f:
                    f.write(after)
            modified += 1

    print(f'Total HTML files scanned: {total_files}')
    if report_only:
        print('(REPORT ONLY — no files modified)')
    print(f'Modified: {modified}')
    print(f'Already had search button: {skipped_already}')
    print(f'No <rustdoc-topbar> (likely redirect stub): {skipped_topbar_absent}')


if __name__ == '__main__':
    main()