#!/usr/bin/env python3
"""build_sitemap.py - 生成站点根 sitemap.xml

遍历仓库下所有 .html 文件（跳过 _old/、static.files/、search.index/、trait.impl/、src/），
按路径深度设置 priority 与 changefreq，输出 sitemap.xml 到仓库根。

用法：
    python _common_tools/build_sitemap.py
"""

import os
import datetime
import sys

ROOT = r'D:\Administrator\Documents\Code\rust_doc_all'
DOMAIN = 'https://rustdoc.p-cat.fun/'

# 跳过的目录名（不参与 URL 收录）
SKIP_DIRS = {
    'static.files',
    'search.index',
    'trait.impl',
    'src',
    '__pycache__',
    '.git',
    '_common_tools',
}


def should_skip_dir(d):
    if d in SKIP_DIRS:
        return True
    if d.endswith('_old') or d.startswith('_'):
        return True
    return False


def classify(rel):
    """根据相对路径分类，返回 (priority, changefreq)"""
    parts = rel.split('/')
    if rel == 'index.html':
        return '1.0', 'daily'
    if len(parts) == 2 and parts[1] == 'index.html':
        # <crate>/index.html - crate 文档首页
        return '0.9', 'weekly'
    if len(parts) == 2:
        # <crate>/xxx.html - crate 内顶层页（如 all.html）
        return '0.7', 'monthly'
    if len(parts) >= 3:
        # <crate>/<sub>/xxx.html - 子模块页
        return '0.5', 'monthly'
    return '0.5', 'monthly'


def main():
    urls = []
    skipped = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # 过滤：原地修改 dirnames 影响 os.walk 行为
        dirnames[:] = [d for d in dirnames if not should_skip_dir(d)]
        for f in filenames:
            if not f.endswith('.html'):
                continue
            # 跳过 help.html（rustdoc 默认帮助页，无 SEO 价值）
            if f == 'help.html':
                continue
            path = os.path.join(dirpath, f)
            rel = os.path.relpath(path, ROOT).replace(os.sep, '/')
            prio, freq = classify(rel)
            urls.append((DOMAIN + rel, prio, freq))

    # 按 URL 排序输出
    urls.sort()
    today = datetime.date.today().isoformat()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for url, prio, freq in urls:
        lines.append('  <url>')
        lines.append(f'    <loc>{url}</loc>')
        lines.append(f'    <lastmod>{today}</lastmod>')
        lines.append(f'    <changefreq>{freq}</changefreq>')
        lines.append(f'    <priority>{prio}</priority>')
        lines.append('  </url>')
    lines.append('</urlset>')

    out_path = os.path.join(ROOT, 'sitemap.xml')
    with open(out_path, 'w', encoding='utf-8') as fp:
        fp.write('\n'.join(lines) + '\n')
    print(f'Wrote {len(urls)} URLs to {out_path}')


if __name__ == '__main__':
    main()
