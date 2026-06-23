"""Stage 1: translate common chrome (lang/title/H1/UI) for all 60 files.

Idempotent: each replacement is checked before writing.
"""

import os
import re

BASE = 'D:/Administrator/Documents/Code/rust_doc_all/rustls_pki_types'

# Common chrome translations (long-string-first to avoid prefix collisions)
COMMON = [
    # lang
    ('<html lang="en">', '<html lang="zh-CN">'),
    # title
    (' - rustls_pki_types', ' - rustls_pki_types'),
    # body class
    ('<body class="rustdoc">', '<body class="rustdoc">'),
    # H1 types (do not touch identifier span)
    ('<h1>Struct <span class="struct">', '<h1>结构体 <span class="struct">'),
    ('<h1>Enum <span class="enum">', '<h1>枚举 <span class="enum">'),
    ('<h1>Trait <span class="trait">', '<h1>特性 <span class="trait">'),
    ('<h1>Type <span class="type">', '<h1>类型 <span class="type">'),
    ('<h1>Constant <span class="constant">', '<h1>常量 <span class="constant">'),
    ('<h1>Function <span class="fn">', '<h1>函数 <span class="fn">'),
    ('<h1>Module <span class="mod">', '<h1>模块 <span class="mod">'),
    ('<h1>Macro <span class="macro">', '<h1>宏 <span class="macro">'),
    # Navigation
    ('Crate rustls_pki_types', 'Crate rustls_pki_types'),
    # section headers
    ('<h2 id="fields" class="fields section-header">Fields', '<h2 id="fields" class="fields section-header">字段'),
    ('<h2 id="variants" class="variants section-header">Variants', '<h2 id="variants" class="variants section-header">变体'),
    ('<h2 id="implementations" class="section-header">Implementations', '<h2 id="implementations" class="section-header">实现'),
    ('<h3 id="trait-implementations" class="section-header">Trait Implementations', '<h3 id="trait-implementations" class="section-header">trait 实现'),
    ('<h3 id="synthetic-implementations" class="section-header">Auto Trait Implementations', '<h3 id="synthetic-implementations" class="section-header">自动 trait 实现'),
    ('<h3 id="blanket-implementations" class="section-header">Blanket Implementations', '<h3 id="blanket-implementations" class="section-header">blanket 实现'),
    # Sidebar / navigation
    ('Settings<span class="sidebar-angle">', '设置<span class="sidebar-angle">'),
    ('Theme<span class="sidebar-angle">', '主题<span class="sidebar-angle">'),
    ('Theme choose', '主题选择'),
    ('light theme', '浅色主题'),
    ('dark theme', '深色主题'),
    ('system theme', '跟随系统'),
    ('All crates', '所有 crate'),
    ('>Sections<', '>章节<'),
    # Topbar
    ('Skip to main content', '跳到主要内容'),
    ('Copy item path', '复制项目路径'),
    ('Expand description', '展开描述'),
    ('Collapse description', '折叠描述'),
    # Code blocks chrome
    ('<a class="src rightside" ', '<a class="src rightside" '),
    ('>源代码<', '>源代码<'),
    ('>Examples<', '>示例<'),
    # Footer
    ('This old browser is unsupported', '此旧版浏览器不受支持'),
    # Misc
    ('In rustls_pki_types', '在 rustls_pki_types 中'),
]


def main():
    files = []
    for root, _, fs in os.walk(BASE):
        for f in fs:
            if f.endswith('.html'):
                files.append(os.path.join(root, f))

    n_files = 0
    n_total = 0
    for path in files:
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        orig = c
        n_this = 0
        for old, new in COMMON:
            if old != new and old in c:
                # 避免把已经翻译过的内容再翻译
                # 但我们这里的 key 几乎都是英文独有，所以没事
                c = c.replace(old, new)
                n_this += 1
        if c != orig:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(c)
            n_files += 1
            n_total += n_this
    print(f'Chrome: {n_files} files updated, {n_total} replacements')


if __name__ == '__main__':
    main()