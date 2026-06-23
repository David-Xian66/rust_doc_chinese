"""在每个 HTML 文件的 <head> 中注入中文搜索脚本和 MiniSearch 库。

用法：
    python _common_tools/inject_chinese_search.py [--report]

注入位置：在 <meta name="rustdoc-vars"> 之后，<script src="../static.files/storage-..."> 之前
注入片段：
    <script src="../static.files/minisearch.min.js"></script>
    <script src="../static.files/chinese-search.js"></script>

要点：
- bytes 模式
- 跳过 _old/, static.files/, src/, search.index/
- 幂等：含 'chinese-search.js' 的文件跳过
"""
import os
import sys

SKIP_DIRS = {
    'static.files', 'search.index', 'src', '_common_tools',
}


def should_skip_dir(d):
    return d.startswith('.') or d in SKIP_DIRS or d.endswith('_old')


SCRIPT_BLOCK = (
    b'<script src="../static.files/minisearch.min.js"></script>'
    b'<script src="../static.files/chinese-search.js"></script>'
)


def main():
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