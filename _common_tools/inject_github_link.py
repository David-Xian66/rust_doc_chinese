"""在每个含侧边栏的 HTML 文件中注入 GitHub 仓库链接。

用法：
    python _common_tools/inject_github_link.py [--report]

要点（参考 inject_search_button.py）：
- bytes 模式读写，避免 Python 文本模式规范化 CRLF 破坏 UTF-8 多字节字符
- 跳过 <crate>_old/ 备份目录（这些不会被部署）
- 跳过 static.files/、search.index/、src/、_common_tools/ 等资源/工具目录
- 只对含 <nav class="sidebar"> 的文件注入（其他是 redirect stub 等）
- 幂等：含 'sidebar-github-link' 的文件跳过

注入位置：在 <nav class="sidebar"> 起始标签之后立即插入 GitHub 仓库链接块。
注入片段：
    <div class="sidebar-github-link" style="...">
      <a href="https://github.com/David-Xian66/rust_doc_chinese" target="_blank" rel="noopener noreferrer" title="...">
        <svg ...>...</svg>
        <span>GitHub 仓库</span>
      </a>
    </div>
"""
import os
import re
import sys

GITHUB_URL = b'https://github.com/David-Xian66/rust_doc_chinese'

# 字节模式串：注入片段
# 注意：\xe6\x88\x91\xe4\xbb\xac 的我们 / \xe8\xae\xbf\xe9\x97\xae 的访问 / \xe4\xbb\x93\xe5\xba\x93 的仓库
GITHUB_BLOCK = (
    b'<div class="sidebar-github-link" style="padding:6px 16px;border-bottom:1px solid #ddd;margin-bottom:8px;display:flex;align-items:center;gap:6px">'
    b'<a href="' + GITHUB_URL + b'" target="_blank" rel="noopener noreferrer" '
    b'title="\xe8\xae\xbf\xe9\x97\xae\xe6\x88\x91\xe4\xbb\xac\xe7\x9a\x84 GitHub \xe4\xbb\x93\xe5\xba\x93" '
    b'style="display:inline-flex;align-items:center;gap:6px;color:#333;text-decoration:none;font-size:14px;line-height:1">'
    b'<svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="currentColor" style="flex-shrink:0">'
    b'<path d="M12 .5C5.65.5.5 5.65.5 12c0 5.08 3.29 9.39 7.86 10.91.58.1.79-.25.79-.56v-2.16c-3.2.7-3.87-1.37-3.87-1.37-.52-1.33-1.27-1.68-1.27-1.68-1.04-.71.08-.7.08-.7 1.15.08 1.76 1.18 1.76 1.18 1.02 1.76 2.69 1.25 3.34.95.1-.74.4-1.25.72-1.54-2.55-.29-5.24-1.28-5.24-5.7 0-1.26.45-2.29 1.18-3.1-.12-.29-.51-1.46.11-3.04 0 0 .96-.31 3.15 1.18a10.94 10.94 0 0 1 5.74 0c2.18-1.49 3.14-1.18 3.14-1.18.63 1.58.23 2.75.11 3.04.74.81 1.18 1.84 1.18 3.1 0 4.43-2.7 5.4-5.27 5.69.41.36.78 1.06.78 2.14v3.17c0 .31.21.67.8.56C20.21 21.39 23.5 17.08 23.5 12 23.5 5.65 18.35.5 12 .5z"/>'
    b'</svg>'
    b'<span>GitHub \xe4\xbb\x93\xe5\xba\x93</span>'
    b'</a>'
    b'</div>'
)

NAV_SIDEBAR = b'<nav class="sidebar">'
SIDEBAR_GH_CLASS = b'class="sidebar-github-link"'

# 跳过这些顶层目录
SKIP_TOP_DIRS = {
    'static.files',
    'search.index',
    'src',
    '_common_tools',
    '__pycache__',
    '.git',
}

# 跳过名字包含 _old 的目录
def should_skip_dir(dirname):
    if dirname.startswith('.'):
        return True
    if dirname in SKIP_TOP_DIRS:
        return True
    if dirname.endswith('_old'):
        return True
    return False


def inject_github_link(html_bytes):
    """在每个 <nav class="sidebar"> 起始标签之后插入 GitHub 链接块。
    返回 (new_bytes, modified_bool, reason)。
    """
    if NAV_SIDEBAR not in html_bytes:
        return html_bytes, False, 'no-sidebar'
    if SIDEBAR_GH_CLASS in html_bytes:
        return html_bytes, False, 'already-injected'

    # 找到 <nav class="sidebar"> 的结束 > 位置（注意该标签本身可能含其他属性，但 nav class=sidebar 的形式固定）
    idx = html_bytes.find(NAV_SIDEBAR)
    end = html_bytes.find(b'>', idx)
    if end < 0:
        return html_bytes, False, 'malformed-nav'
    insert_pos = end + 1
    new_bytes = html_bytes[:insert_pos] + GITHUB_BLOCK + html_bytes[insert_pos:]
    return new_bytes, True, 'injected'


def main():
    report_only = '--report' in sys.argv
    root = '.'

    total_files = 0
    modified = 0
    skipped_no_sidebar = 0
    skipped_already = 0
    skipped_malformed = 0

    for top, dirs, fs in os.walk(root):
        dirs[:] = [d for d in dirs if not should_skip_dir(d)]

        for fn in fs:
            if not fn.endswith('.html'):
                continue
            path = os.path.join(top, fn)
            total_files += 1

            with open(path, 'rb') as f:
                before = f.read()

            after, was_modified, reason = inject_github_link(before)

            if not was_modified:
                if reason == 'already-injected':
                    skipped_already += 1
                elif reason == 'no-sidebar':
                    skipped_no_sidebar += 1
                elif reason == 'malformed-nav':
                    skipped_malformed += 1
                continue

            if not report_only:
                with open(path, 'wb') as f:
                    f.write(after)
            modified += 1

    print(f'Total HTML files scanned: {total_files}')
    if report_only:
        print('(REPORT ONLY — no files modified)')
    print(f'Modified: {modified}')
    print(f'Already had github link: {skipped_already}')
    print(f'No <nav class="sidebar"> (likely redirect stub): {skipped_no_sidebar}')
    if skipped_malformed:
        print(f'Malformed nav (unable to inject): {skipped_malformed}')


if __name__ == '__main__':
    main()