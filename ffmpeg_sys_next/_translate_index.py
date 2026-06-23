"""Translate index.html files in ffmpeg_sys_next to Chinese.

Workflow per rust-doc-translation-pattern:
- Use Python open() directly (no Read tool).
- Apply (old, new) replacements in long-string-first order.
- Preserve HTML structure, URLs, Rust identifiers.
- Translate both keywords and <meta name="description"> fields.
"""

import os
import re

FFMPEG_SYS_NEXT_ROOT = 'D:/Administrator/Documents/Code/rust_doc_all/ffmpeg_sys_next'


def verify(content, label):
    """Verify a translated HTML file: tag balance, line-number pollution, CJK density."""
    line_artifacts = re.findall(r'^\d+\t', content, flags=re.MULTILINE)
    if line_artifacts:
        print(f'  [WARN] {label}: {len(line_artifacts)} lines with cat-n style line numbers')

    cjk = re.findall(r'[一-鿿]', content)
    print(f'  [INFO] {label}: {len(cjk)} CJK characters')

    tag_pairs = ['html', 'head', 'body', 'main', 'section', 'div', 'p',
                 'a', 'span', 'h1', 'h2', 'h3', 'h4', 'ul', 'li',
                 'code', 'pre', 'details', 'summary', 'dl', 'dt', 'dd']
    for t in tag_pairs:
        opens = len(re.findall(rf'<{t}[\s>]', content))
        closes = len(re.findall(rf'</{t}>', content))
        if opens != closes:
            print(f'  [WARN] {label}: <{t}> open={opens} close={closes} diff={opens-closes}')


# ============================================================================
# Common UI / keyword replacements
# ============================================================================
COMMON_UI = [
    # lang
    ('<html lang="en">', '<html lang="zh-CN">'),
    # skip link
    ('>Skip to main content<', '>跳到主要内容<'),
    # IE warning
    ('This old browser is unsupported and will most likely display funky things.',
     '此旧版浏览器不受支持，很可能会显示异常内容。'),
    # sidebar
    ('>All Items<', '>所有项<'),
    # topbar h2 - Crate
    ('<a href="#">Crate ffmpeg_sys_next</a>',
     '<a href="#">crate ffmpeg_sys_next</a>'),
    # TOC headers
    ('>Crate Items</a>', '>crate 项</a>'),
    ('>Module Items</a>', '>模块项</a>'),
    # TOC title attributes
    ('title="Re-exports"', 'title="重新导出"'),
    ('title="Modules"', 'title="模块"'),
    ('title="Macros"', 'title="宏"'),
    ('title="Functions"', 'title="函数"'),
    ('title="Structs"', 'title="结构体"'),
    ('title="Enums"', 'title="枚举"'),
    ('title="Constants"', 'title="常量"'),
    ('title="Statics"', 'title="静态项"'),
    ('title="Traits"', 'title="trait"'),
    ('title="Type Aliases"', 'title="类型别名"'),
    ('title="Unions"', 'title="联合体"'),
    # TOC anchor text
    ('>Re-exports</a>', '>重新导出</a>'),
    ('>Modules</a>', '>模块</a>'),
    ('>Macros</a>', '>宏</a>'),
    ('>Functions</a>', '>函数</a>'),
    ('>Structs</a>', '>结构体</a>'),
    ('>Enums</a>', '>枚举</a>'),
    ('>Constants</a>', '>常量</a>'),
    ('>Statics</a>', '>静态项</a>'),
    ('>Traits</a>', '>trait</a>'),
    ('>Type Aliases</a>', '>类型别名</a>'),
    ('>Unions</a>', '>联合体</a>'),
    # H2 section headers (in main content)
    ('<h2 id="reexports" class="section-header">Re-exports',
     '<h2 id="reexports" class="section-header">重新导出'),
    ('<h2 id="modules" class="section-header">Modules',
     '<h2 id="modules" class="section-header">模块'),
    ('<h2 id="macros" class="section-header">Macros',
     '<h2 id="macros" class="section-header">宏'),
    ('<h2 id="functions" class="section-header">Functions',
     '<h2 id="functions" class="section-header">函数'),
    ('<h2 id="structs" class="section-header">Structs',
     '<h2 id="structs" class="section-header">结构体'),
    ('<h2 id="enums" class="section-header">Enums',
     '<h2 id="enums" class="section-header">枚举'),
    ('<h2 id="constants" class="section-header">Constants',
     '<h2 id="constants" class="section-header">常量'),
    ('<h2 id="statics" class="section-header">Statics',
     '<h2 id="statics" class="section-header">静态项'),
    ('<h2 id="traits" class="section-header">Traits',
     '<h2 id="traits" class="section-header">trait'),
    ('<h2 id="types" class="section-header">Type Aliases',
     '<h2 id="types" class="section-header">类型别名'),
    ('<h2 id="unions" class="section-header">Unions',
     '<h2 id="unions" class="section-header">联合体'),
    # Copy item path
    ('>Copy item path<', '>复制项目路径<'),
    ('title="Copy item path to clipboard"', 'title="复制项目路径到剪贴板"'),
    # Source
    ('>Source<', '>源代码<'),
    # Sidebar resizer
    ('title="Drag to resize sidebar"', 'title="拖动以调整侧边栏宽度"'),
    # H1 main-heading (for ffmpeg_sys_next the span has 2 wbr markers)
    ('<h1>Crate <span>ffmpeg_<wbr>sys_<wbr>next</span>',
     '<h1>crate <span>ffmpeg_<wbr>sys_<wbr>next</span>'),
]


def translate_description_meta(content):
    """Translate <meta name="description"> for ffmpeg_sys_next.

    The pattern is: 'API documentation for the Rust `ffmpeg_sys_next` crate.'
    """
    return content.replace(
        '<meta name="description" content="API documentation for the Rust `ffmpeg_sys_next` crate.">',
        '<meta name="description" content="Rust crate `ffmpeg_sys_next` 的 API 文档。">'
    )


def translate_index_html(content):
    content = translate_description_meta(content)
    for old, new in COMMON_UI:
        content = content.replace(old, new)
    return content


def main():
    targets = []
    for dp, _, fns in os.walk(FFMPEG_SYS_NEXT_ROOT):
        for fn in fns:
            if fn == 'index.html':
                targets.append(os.path.join(dp, fn))
    targets.sort()

    print(f'Found {len(targets)} index.html files\n')

    total_cjk = 0
    fail_count = 0
    for path in targets:
        rel = os.path.relpath(path, FFMPEG_SYS_NEXT_ROOT)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content = translate_index_html(content)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        # verify
        line_artifacts = re.findall(r'^\d+\t', new_content, flags=re.MULTILINE)
        cjk = len(re.findall(r'[一-鿿]', new_content))
        total_cjk += cjk

        # check meta desc translated
        m = re.search(r'<meta name="description" content="([^"]+)"', new_content)
        if m and 'API documentation for the Rust' in m.group(1):
            print(f'  [FAIL] {rel}: description still in English')
            fail_count += 1

        # check title attr untranslated
        untranslated = []
        for kw in ('title="Re-exports"', 'title="Modules"', 'title="Macros"',
                   'title="Functions"', 'title="Structs"', 'title="Enums"',
                   'title="Constants"', 'title="Statics"', 'title="Traits"',
                   'title="Type Aliases"', 'title="Unions"'):
            if kw in new_content:
                untranslated.append(kw)
        if untranslated:
            print(f'  [FAIL] {rel}: untranslated title attrs: {untranslated}')
            fail_count += 1

        if cjk < 30:
            print(f'  [WARN] {rel}: only {cjk} CJK chars')
        if line_artifacts:
            print(f'  [FAIL] {rel}: {len(line_artifacts)} line-number artifacts')
            fail_count += 1

        # Tag balance check
        for t in ['html', 'head', 'body', 'main', 'section', 'div', 'p',
                  'a', 'span', 'h1', 'h2', 'h3', 'h4', 'ul', 'li']:
            opens = len(re.findall(rf'<{t}[\s>]', new_content))
            closes = len(re.findall(rf'</{t}>', new_content))
            if opens != closes:
                print(f'  [WARN] {rel}: <{t}> open={opens} close={closes}')

        print(f'  --- {rel} --- CJK={cjk}')

    print(f'\n=== Summary ===')
    print(f'Files: {len(targets)}')
    print(f'Total CJK: {total_cjk}')
    print(f'Failures: {fail_count}')


if __name__ == '__main__':
    main()
