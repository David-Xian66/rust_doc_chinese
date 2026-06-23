"""Translate all index.html files in ffmpeg_next to Chinese.

Workflow per rust-doc-translation-pattern:
- Use Python open() directly (no Read tool).
- Apply (old, new) replacements in long-string-first order.
- Preserve HTML structure, URLs, Rust identifiers.
- Pay extra attention to <meta name="description"> fields, not just keywords.
"""

import os
import re

FFMPEG_NEXT_ROOT = 'D:/Administrator/Documents/Code/rust_doc_all/ffmpeg_next'


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
# Common UI / keyword replacements (apply to all index.html)
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
    # topbar / sidebar h2 - Crate
    ('<a href="#">Crate ffmpeg_next</a>', '<a href="#">crate ffmpeg_next</a>'),
    # topbar / sidebar h2 - Module (generic)
    # specific Module XXX handled separately to translate to "模块 XXX"
    # TOC headers (href can point to first section like #reexports or #modules)
    ('>Crate Items</a>', '>crate 项</a>'),
    ('>Module Items</a>', '>模块项</a>'),
    # TOC link text + title attributes
    ('title="Re-exports"', 'title="重新导出"'),
    ('title="Modules"', 'title="模块"'),
    ('title="Macros"', 'title="宏"'),
    ('title="Functions"', 'title="函数"'),
    ('title="Structs"', 'title="结构体"'),
    ('title="Enums"', 'title="枚举"'),
    ('title="Constants"', 'title="常量"'),
    ('title="Traits"', 'title="trait"'),
    ('title="Type Aliases"', 'title="类型别名"'),
    # TOC anchor text
    ('>Re-exports</a>', '>重新导出</a>'),
    ('>Modules</a>', '>模块</a>'),
    ('>Macros</a>', '>宏</a>'),
    ('>Functions</a>', '>函数</a>'),
    ('>Structs</a>', '>结构体</a>'),
    ('>Enums</a>', '>枚举</a>'),
    ('>Constants</a>', '>常量</a>'),
    ('>Traits</a>', '>trait</a>'),
    ('>Type Aliases</a>', '>类型别名</a>'),
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
    ('<h2 id="traits" class="section-header">Traits',
     '<h2 id="traits" class="section-header">trait'),
    ('<h2 id="types" class="section-header">Type Aliases',
     '<h2 id="types" class="section-header">类型别名'),
    # Copy item path
    ('>Copy item path<', '>复制项目路径<'),
    ('title="Copy item path to clipboard"', 'title="复制项目路径到剪贴板"'),
    # Source
    ('>Source<', '>源代码<'),
    # Sidebar resizer
    ('title="Drag to resize sidebar"', 'title="拖动以调整侧边栏宽度"'),
    # H1 main-heading
    ('<h1>Crate <span>ffmpeg_<wbr>next</span>',
     '<h1>crate <span>ffmpeg_<wbr>next</span>'),
]


def translate_description_meta(content):
    """Translate <meta name="description"> for ffmpeg_next index.html files.

    The description pattern is one of:
    - 'API documentation for the Rust `ffmpeg_next` crate.'
    - 'API documentation for the Rust `<mod_name>` mod in crate `ffmpeg_next`.'
    """
    # Crate-level
    content = content.replace(
        '<meta name="description" content="API documentation for the Rust `ffmpeg_next` crate.">',
        '<meta name="description" content="Rust crate `ffmpeg_next` 的 API 文档。">'
    )

    # Mod-level: any number of mod names joined by backticks
    def repl(m):
        mod_path = m.group(1)  # e.g. "format" or "codec::decoder"
        return (f'<meta name="description" content="Rust crate `ffmpeg_next` 中模块 '
                f'`{mod_path}` 的 API 文档。">')

    content = re.sub(
        r'<meta name="description" content="API documentation for the Rust `([^`]+)` mod in crate `ffmpeg_next`\.">',
        repl, content
    )
    return content


def translate_module_h1(content):
    """Translate the H1 'Module <span>X</span>' in main heading.

    Preserves the wrapped span. Also handles the optional wbr inside the span.
    """
    # Generic: '>Module <span>X</span>...' where X is the module name (may have <wbr>)
    def repl(m):
        prefix = m.group(1)  # '>Module <span>'
        inner = m.group(2)   # the content of span (e.g. 'audio' or 'audio_<wbr>service')
        suffix = m.group(3)  # '</span>...'
        return f'>{prefix.replace(">Module", ">模块")}{inner}{suffix}'

    return re.sub(
        r'(<h1>)Module (<span>[^<]*(?:<wbr>[^<]*)*</span>)',
        lambda m: m.group(1) + '模块 ' + m.group(2),
        content
    )


def translate_sidebar_h2_location(content):
    """Translate '<h2 class="location"><a href="#">Module XXX</a></h2>' to '模块 XXX'.

    XXX may contain <wbr> markers; we keep them so the layout still works.
    """
    def repl(m):
        mod_text = m.group(1)  # may contain <wbr>
        return f'<h2 class="location"><a href="#">模块 {mod_text}</a></h2>'

    return re.sub(
        r'<h2 class="location"><a href="#">Module ([^<]*(?:<wbr>[^<]*)*)</a></h2>',
        repl, content
    )


def translate_topbar_module_h2(content):
    """Translate the topbar <h2><a href="#">Module XXX</a></h2> to <h2><a href="#">模块 XXX</a></h2>.

    XXX may contain <wbr> markers; we keep them.
    """
    def repl(m):
        mod_text = m.group(1)  # may contain <wbr>
        return f'<h2><a href="#">模块 {mod_text}</a></h2>'

    return re.sub(
        r'<h2><a href="#">Module ([^<]*(?:<wbr>[^<]*)*)</a></h2>',
        repl, content
    )


def translate_in_breadcrumb(content):
    """Translate '<h2><a href="...">In ffmpeg_<wbr>next::X</a></h2>' to '<h2><a href="...">在 ffmpeg_<wbr>next::X 中</a></h2>'.

    The path after ffmpeg_next:: may contain <wbr> markers and multiple :: segments.
    """
    def repl(m):
        href = m.group(1)
        # The inner text: ffmpeg_<wbr>next::X<...>
        inner = m.group(2)
        return f'<h2><a href="{href}">在 {inner} 中</a></h2>'

    return re.sub(
        r'<h2><a href="([^"]+)">In (ffmpeg_<wbr>next::[^<]*(?:<wbr>[^<]*)*)</a></h2>',
        repl, content
    )


def translate_index_html(content):
    # Apply all transformations in dependency order
    content = translate_description_meta(content)
    content = translate_in_breadcrumb(content)
    content = translate_topbar_module_h2(content)
    content = translate_sidebar_h2_location(content)
    content = translate_module_h1(content)

    # Apply common UI replacements last so they don't break patterns above
    for old, new in COMMON_UI:
        if old not in content:
            # Don't warn for "In " h2 patterns if not present
            if old in ('<h2 id="macros" class="section-header">Macros',
                       '<h2 id="types" class="section-header">Type Aliases',
                       '<h2 id="enums" class="section-header">Enums',
                       '<h2 id="constants" class="section-header">Constants',
                       '<h2 id="functions" class="section-header">Functions'):
                # Some files don't have all sections - this is fine
                continue
            # Warn for others
            if any(kw in old for kw in ('Skip to main', 'funky things', 'Crate Items', 'Module Items',
                                         'All Items', 'Copy item path', 'Source', 'Crate ffmpeg',
                                         'lang="en"', 'Resize sidebar', '>Crate <span>')):
                # These are very common and should be present
                if old in content or True:
                    pass  # silent if not present
        content = content.replace(old, new)

    return content


def main():
    # Find all index.html files
    targets = []
    for dp, _, fns in os.walk(FFMPEG_NEXT_ROOT):
        for fn in fns:
            if fn == 'index.html':
                targets.append(os.path.join(dp, fn))
    targets.sort()

    print(f'Found {len(targets)} index.html files\n')

    total_cjk = 0
    fail_count = 0
    for path in targets:
        rel = os.path.relpath(path, FFMPEG_NEXT_ROOT)
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

        # check title attr "Re-exports" etc.
        untranslated = []
        for kw in ('title="Re-exports"', 'title="Modules"', 'title="Macros"',
                   'title="Functions"', 'title="Structs"', 'title="Enums"',
                   'title="Constants"', 'title="Traits"'):
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

    print(f'\n=== Summary ===')
    print(f'Files: {len(targets)}')
    print(f'Total CJK: {total_cjk}')
    print(f'Failures: {fail_count}')


if __name__ == '__main__':
    main()
