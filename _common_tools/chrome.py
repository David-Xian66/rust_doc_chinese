"""chrome.py (通用版): 翻译所有 .html 的 lang / title / H1 / sidebar / footer.

用法:
    python _common_tools/chrome.py <crate_dir>

长字符串优先匹配以避免前缀冲突。脚本是幂等的 (每次替换前会判断是否已翻译).

术语表参考: COMMON 一节里的内容。修改该节即可调整翻译策略。
"""

import os
import sys


COMMON = [
    # lang
    ('<html lang="en">', '<html lang="zh-CN">'),
    # title (rustdoc 默认后缀是 " - Rust"; crate-specific 的 " - <crate>" 通常要替换)
    (' - Rust</title>', ' - {CRATE}</title>'),  # 占位符, 实际运行时替换
    # body class
    ('<body class="rustdoc">', '<body class="rustdoc">'),
    # H1 types
    ('<h1>Struct <span class="struct">', '<h1>结构体 <span class="struct">'),
    ('<h1>Enum <span class="enum">', '<h1>枚举 <span class="enum">'),
    ('<h1>Trait <span class="trait">', '<h1>特性 <span class="trait">'),
    ('<h1>Type <span class="type">', '<h1>类型 <span class="type">'),
    ('<h1>Constant <span class="constant">', '<h1>常量 <span class="constant">'),
    ('<h1>Function <span class="fn">', '<h1>函数 <span class="fn">'),
    ('<h1>Module <span class="mod">', '<h1>模块 <span class="mod">'),
    ('<h1>Macro <span class="macro">', '<h1>宏 <span class="macro">'),
    # Section headers (h2/h3)
    ('<h2 id="fields" class="fields section-header">Fields', '<h2 id="fields" class="fields section-header">字段'),
    ('<h2 id="variants" class="variants section-header">Variants', '<h2 id="variants" class="variants section-header">变体'),
    ('<h2 id="implementations" class="section-header">Implementations', '<h2 id="implementations" class="section-header">实现'),
    ('<h3 id="trait-implementations" class="section-header">Trait Implementations',
     '<h3 id="trait-implementations" class="section-header">trait 实现'),
    ('<h3 id="synthetic-implementations" class="section-header">Auto Trait Implementations',
     '<h3 id="synthetic-implementations" class="section-header">自动 trait 实现'),
    ('<h3 id="blanket-implementations" class="section-header">Blanket Implementations',
     '<h3 id="blanket-implementations" class="section-header">blanket 实现'),
    # Sidebar / nav
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
    ('>源代码<', '>源代码<'),  # placeholder, may be different per rustdoc version
    ('>Examples<', '>示例<'),  # placeholder
    # Footer
    ('This old browser is unsupported', '此旧版浏览器不受支持'),
    # Misc
    ('In {CRATE}', '在 {CRATE} 中'),  # placeholder
]


def main():
    if len(sys.argv) < 2:
        print('Usage: chrome.py <crate_dir>')
        sys.exit(1)
    base = sys.argv[1]
    crate_name = os.path.basename(base.rstrip('/\\'))

    files = []
    for root, _, fs in os.walk(base):
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
            # Substitute placeholders
            old2 = old.replace('{CRATE}', crate_name)
            new2 = new.replace('{CRATE}', crate_name)
            if old2 != new2 and old2 in c:
                c = c.replace(old2, new2)
                n_this += 1
        if c != orig:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(c)
            n_files += 1
            n_total += n_this
    print(f'Chrome: {n_files} files updated, {n_total} replacements')


if __name__ == '__main__':
    main()