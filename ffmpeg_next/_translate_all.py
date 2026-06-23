"""
Translate all non-index.html files in ffmpeg_next directory to Chinese.

Workflow per rust-doc-translation-pattern:
- Use Python open() directly (no Read tool).
- Apply (old, new) replacements in long-string-first order.
- Preserve HTML structure, URLs, Rust identifiers.
- Pay extra attention to <meta name="description"> fields, <title>, h1, h2 sidebar nav.
"""

import os
import re

FFMPEG_NEXT_ROOT = 'D:/Administrator/Documents/Code/rust_doc_all/ffmpeg_next'


def verify(content, label):
    line_artifacts = re.findall(r'^\d+\t', content, flags=re.MULTILINE)
    if line_artifacts:
        print(f'  [WARN] {label}: {len(line_artifacts)} cat-n line numbers')

    cjk = len(re.findall(r'[一-鿿]', content))
    bad = []
    for t in ['html', 'head', 'body', 'main', 'section', 'div', 'p',
              'a', 'span', 'h1', 'h2', 'h3', 'h4', 'ul', 'li',
              'code', 'pre', 'details', 'summary', 'dl', 'dt', 'dd']:
        opens = len(re.findall(rf'<{t}[\s>]', content))
        closes = len(re.findall(rf'</{t}>', content))
        if opens != closes:
            bad.append((t, opens, closes))
    if bad:
        for t, o, c in bad:
            print(f'  [WARN] {label}: <{t}> open={o} close={c} diff={o-c}')
    return cjk


# ===========================================================================
# COMMON_UI: applied to every non-index file (.html)
# ===========================================================================
COMMON_UI = [
    # lang
    ('<html lang="en">', '<html lang="zh-CN">'),
    # skip link
    ('>Skip to main content<', '>跳到主要内容<'),
    # IE warning
    ('This old browser is unsupported and will most likely display funky things.',
     '此旧版浏览器不受支持，很可能会显示异常内容。'),
    # Sidebar resizer
    ('title="Drag to resize sidebar"', 'title="拖动以调整侧边栏宽度"'),
    # Copy item path
    ('>Copy item path<', '>复制项目路径<'),
    ('title="Copy item path to clipboard"', 'title="复制项目路径到剪贴板"'),
    # Source
    ('>Source<', '>源代码<'),
    # /* private fields */
    ('/* private fields */', '/* 私有字段 */'),

    # Sidebar h3 / h2 nav section labels (TOC link text)
    ('>Trait Implementations</a>', '>trait 实现</a>'),
    ('>Auto Trait Implementations</a>', '>自动 trait 实现</a>'),
    ('>Blanket Implementations</a>', '>blanket 实现</a>'),
    ('>Implementations on Foreign Types</a>', '>对外部类型的实现</a>'),
    ('>Implementations</a>', '>实现</a>'),
    ('>Implementors</a>', '>实现者</a>'),
    ('>Required Methods</a>', '>必需方法</a>'),
    ('>Provided Methods</a>', '>提供方法</a>'),
    ('>Methods</a>', '>方法</a>'),
    ('>Variants</a>', '>变体</a>'),
    ('>Fields</a>', '>字段</a>'),
    ('>Tuple Fields</a>', '>元组字段</a>'),
    ('>Associated Constants</a>', '>关联常量</a>'),
    ('>Associated Types</a>', '>关联类型</a>'),
    ('>Dyn Compatibility</a>', '>Dyn 兼容性</a>'),

    # Main content section headers (<h2 id="..." class="section-header">)
    ('<h2 id="trait-implementations" class="section-header">Trait Implementations',
     '<h2 id="trait-implementations" class="section-header">trait 实现'),
    ('<h2 id="synthetic-implementations" class="section-header">Auto Trait Implementations',
     '<h2 id="synthetic-implementations" class="section-header">自动 trait 实现'),
    ('<h2 id="blanket-implementations" class="section-header">Blanket Implementations',
     '<h2 id="blanket-implementations" class="section-header">blanket 实现'),
    ('<h2 id="foreign-impls" class="section-header">Implementations on Foreign Types',
     '<h2 id="foreign-impls" class="section-header">对外部类型的实现'),
    ('<h2 id="implementations" class="section-header">Implementations',
     '<h2 id="implementations" class="section-header">实现'),
    ('<h2 id="implementors" class="section-header">Implementors',
     '<h2 id="implementors" class="section-header">实现者'),
    ('<h2 id="required-methods" class="section-header">Required Methods',
     '<h2 id="required-methods" class="section-header">必需方法'),
    ('<h2 id="provided-methods" class="section-header">Provided Methods',
     '<h2 id="provided-methods" class="section-header">提供方法'),
    ('<h2 id="variants" class="section-header">Variants',
     '<h2 id="variants" class="section-header">变体'),
    ('<h2 id="fields" class="section-header">Fields',
     '<h2 id="fields" class="section-header">字段'),
    ('<h2 id="associated-constants" class="section-header">Associated Constants',
     '<h2 id="associated-constants" class="section-header">关联常量'),
    ('<h2 id="associated-types" class="section-header">Associated Types',
     '<h2 id="associated-types" class="section-header">关联类型'),
    ('<h2 id="dyn-compatibility" class="section-header">Dyn Compatibility',
     '<h2 id="dyn-compatibility" class="section-header">Dyn 兼容性'),

    # Title attrs
    ('title="Trait Implementations"', 'title="trait 实现"'),
    ('title="Auto Trait Implementations"', 'title="自动 trait 实现"'),
    ('title="Blanket Implementations"', 'title="blanket 实现"'),
    ('title="Implementations on Foreign Types"', 'title="对外部类型的实现"'),
    ('title="Implementations"', 'title="实现"'),
    ('title="Implementors"', 'title="实现者"'),
    ('title="Required Methods"', 'title="必需方法"'),
    ('title="Provided Methods"', 'title="提供方法"'),
    ('title="Methods"', 'title="方法"'),
    ('title="Variants"', 'title="变体"'),
    ('title="Fields"', 'title="字段"'),
    ('title="Tuple Fields"', 'title="元组字段"'),
    ('title="Associated Constants"', 'title="关联常量"'),
    ('title="Associated Types"', 'title="关联类型"'),
    ('title="Dyn Compatibility"', 'title="Dyn 兼容性"'),
    ('title="Notable traits for "', 'title="值得注意的 trait："'),

    # Section anchors with embedded text (Read more, etc.)
    ('>Read more</a>', '>阅读更多</a>'),

    # Toggle / expand controls
    ('>Expand description<', '>展开描述<'),
    ('>Collapse description<', '>折叠描述<'),

    # Notable traits popup
    ('Notable traits for ', '值得注意的 trait：'),

    # Misc section names that appear in docblocks
    ('>Errors</a>', '>错误</a>'),
    ('>Panics</a>', '>恐慌</a>'),
    ('>Safety</a>', '>安全性</a>'),
    ('>Examples</a>', '>示例</a>'),
    ('id="errors"', 'id="errors"'),  # no-op, keep anchor
]


# ===========================================================================
# COMMON_TEXT: standard rustdoc auto-generated phrases (boilerplate)
# ===========================================================================
COMMON_TEXT = [
    # ==== Standard trait method descriptions ====
    ('Returns the argument unchanged.', '原样返回参数。'),
    ('Calls U::from(self).', '调用 U::from(self)。'),
    ('That is, this conversion is whatever the implementation of ',
     '也就是说，此转换是 '),
    (' chooses to do.', ' 实现选择执行的操作。'),
    ('Performs the conversion.', '执行该转换。'),
    ('The type returned in the event of a conversion error.',
     '转换出错时返回的类型。'),
    ('Formats the value using the given formatter.',
     '使用给定的格式化器格式化该值。'),
    ('Executes the destructor for this type.', '执行该类型的析构函数。'),
    ('Immutably borrows from an owned value.', '从拥有的值不可变地借用。'),
    ('Mutably borrows from an owned value.', '从拥有的值可变地借用。'),
    ('Gets the <code>TypeId</code> of <code>self</code>.',
     '获取 <code>self</code> 的 <code>TypeId</code>。'),
    ('This method tests for <code>self</code> and <code>other</code> values to be equal, and is used by <code>==</code>.',
     '该方法测试 <code>self</code> 和 <code>other</code> 是否相等，由 <code>==</code> 使用。'),
    ('Tests for <code>!=</code>. The default implementation is almost always sufficient,\nand should not be overridden without very good reason.',
     '测试 <code>!=</code>。默认实现几乎总是足够的，没有充分理由不应被重写。'),
    ('Tests for <code>!=</code>.', '测试 <code>!=</code>。'),
    ('This method tests for self and other values to be equal, and is used\nby ==.',
     '该方法测试 self 与 other 是否相等，由 == 使用。'),
    ('Returns a copy of the value.', '返回该值的副本。'),
    ('Performs copy-assignment from <code>source</code>.',
     '从 <code>source</code> 执行拷贝赋值。'),
    ('Performs copy-assignment from <code>source</code>',
     '从 <code>source</code> 执行拷贝赋值'),
    # CloneToUninit
    ('Performs copy-assignment from <code>self</code> to <code>dest</code>.',
     '从 <code>self</code> 执行拷贝赋值到 <code>dest</code>。'),
    ('Performs copy-assignment from <code>self</code>\nto <code>dest</code>.',
     '从 <code>self</code> 执行拷贝赋值到 <code>dest</code>。'),
    # Deref
    ('The resulting type after dereferencing.', '解引用之后得到的类型。'),
    ('Dereferences the value.', '解引用该值。'),
    # ToOwned
    ('The resulting type after obtaining ownership.', '获取所有权后得到的类型。'),
    ('Creates owned data from borrowed data, usually by cloning.',
     '通常通过克隆，从借用数据创建拥有的数据。'),
    ('Uses borrowed data to replace owned data, usually by cloning.',
     '通常通过克隆，使用借用数据替换拥有的数据。'),
    # TryFrom / TryInto
    ('The type returned in the event of a conversion error',
     '转换出错时返回的类型'),
    ('Performs the conversion', '执行该转换'),
    # Into
    ('Converts this type into the (usually inferred) input type.',
     '将该类型转换为（通常被推断的）输入类型。'),
    # Borrow / BorrowMut
    ('Immutably borrows from an owned value.', '从拥有的值不可变地借用。'),
    ('Mutably borrows from an owned value.', '从拥有的值可变地借用。'),
    # PartialOrd / Ord
    ('This method returns an ordering between <code>self</code> and <code>other</code> values if one exists.',
     '如果存在的话，该方法返回 <code>self</code> 与 <code>other</code> 之间的顺序。'),
    ('This method returns an <a class="enum"',
     '该方法返回一个 <a class="enum"'),
    ('Tests less than (for <code>self</code> and <code>other</code>) and is used by the <code>&lt;</code> operator.',
     '测试小于（对于 <code>self</code> 与 <code>other</code>），由 <code>&lt;</code> 运算符使用。'),
    ('Tests less than or equal to (for <code>self</code> and <code>other</code>) and is used by the <code>&lt;=</code>\noperator.',
     '测试小于等于（对于 <code>self</code> 与 <code>other</code>），由 <code>&lt;=</code> 运算符使用。'),
    ('Tests greater than (for <code>self</code> and <code>other</code>) and is used by the <code>&gt;</code>\noperator.',
     '测试大于（对于 <code>self</code> 与 <code>other</code>），由 <code>&gt;</code> 运算符使用。'),
    ('Tests greater than or equal to (for <code>self</code> and <code>other</code>) and is used by\nthe <code>&gt;=</code> operator.',
     '测试大于等于（对于 <code>self</code> 与 <code>other</code>），由 <code>&gt;=</code> 运算符使用。'),
    # Hash
    ('Feeds this value into the given <code>Hasher</code>.',
     '将该值送入给定的 <code>Hasher</code>。'),
    ('Feeds a slice of this type into the given <code>Hasher</code>.',
     '将该类型的切片送入给定的 <code>Hasher</code>。'),
    # IntoIterator
    ('The type of the elements being iterated over.', '被迭代的元素类型。'),
    ('Which kind of iterator are we turning this into?',
     '我们将其转换为哪种迭代器？'),
    ('Creates an iterator from a value.', '从值创建一个迭代器。'),
    # Iterator
    ('Advances the iterator and returns the next value.',
     '推进迭代器并返回下一个值。'),
    ('Returns the bounds on the remaining length of the iterator.',
     '返回迭代器剩余长度的边界。'),
    # Default
    ('Returns the “default value” for a type.', '返回类型的"默认值"。'),
    # Display / Debug
    ('Formats the value using the given formatter.\n', '使用给定的格式化器格式化该值。\n'),
    # Sub / Add / etc -- usually identifier-only
    # Send / Sync auto traits -- no doc text
    # Misc
    ('Read more', '阅读更多'),
    ('>1.0.0<', '>1.0.0<'),  # version, keep
    # Stability
    ('Stable since Rust version 1.0.0', '自 Rust 1.0.0 起稳定'),
    # Notable traits popup body
    ('struct ', 'struct '),  # keep
]


# Module name translation map for breadcrumbs and topbar
# Format: (en_word, zh_word) - kept as plain Chinese
MODULE_NAMES = {
    # Top-level kind label
    'Struct': '结构体',
    'Enum': '枚举',
    'Trait': 'trait',
    'Function': '函数',
    'Constant': '常量',
    'Macro': '宏',
    'Module': '模块',
    'Type Alias': '类型别名',
}


def apply_pairs(content, pairs):
    for old, new in pairs:
        content = content.replace(old, new)
    return content


def translate_meta_and_h1(content, filename):
    """Translate <meta name="description"> for {name} (struct|enum|...) and
    main heading H1 'Struct <span class="struct">Name</span>'.
    """
    # Map filename prefix → (kind_en, kind_zh, html_class)
    KIND_MAP = {
        'struct': ('struct', '结构体', 'struct'),
        'enum': ('enum', '枚举', 'enum'),
        'trait': ('trait', 'trait', 'trait'),
        'fn': ('fn', '函数', 'fn'),
        'constant': ('constant', '常量', 'constant'),
        'macro': ('macro', '宏', 'macro'),
        'type': ('type', '类型别名', 'type'),
    }
    base = os.path.basename(filename)
    m = re.match(r'^([a-z]+)\.', base)
    if not m or m.group(1) not in KIND_MAP:
        return content
    prefix = m.group(1)
    kind_en, kind_zh, css = KIND_MAP[prefix]

    # The H1 prefix label, e.g. "Struct" → "结构体"
    h1_label_map = {
        'struct': 'Struct',
        'enum': 'Enum',
        'trait': 'Trait',
        'fn': 'Function',
        'constant': 'Constant',
        'macro': 'Macro',
        'type': 'Type Alias',
    }
    h1_en = h1_label_map[prefix]
    h1_zh = kind_zh

    # Meta description: 'API documentation for the Rust `NAME` <kind_en> in crate `ffmpeg_next`.'
    # → 'Rust crate `ffmpeg_next` 中 `NAME` <kind_zh> 的 API 文档。'
    def meta_repl(m):
        name = m.group(1)
        return (f'<meta name="description" content="Rust crate `ffmpeg_next` 中 '
                f'`{name}` {kind_zh}的 API 文档。">')

    content = re.sub(
        r'<meta name="description" content="API documentation for the Rust `([^`]+)` '
        + re.escape(kind_en) + r' in crate `ffmpeg_next`\.">',
        meta_repl, content
    )

    # H1 label: '<h1>Struct <span class="struct">NAME</span>' → '<h1>结构体 <span class="struct">NAME</span>'
    content = re.sub(
        r'<h1>' + re.escape(h1_en) + r' (<span class="' + re.escape(css) + r'">)',
        f'<h1>{h1_zh} \\1',
        content
    )
    return content


def translate_breadcrumb_in(content):
    """Translate sidebar modnav breadcrumb '<h2><a href="...">In ffmpeg_<wbr>next::X</a></h2>'
    to '<h2><a href="...">在 ffmpeg_<wbr>next::X 中</a></h2>'."""
    def repl(m):
        href = m.group(1)
        inner = m.group(2)
        return f'<h2><a href="{href}">在 {inner} 中</a></h2>'

    return re.sub(
        r'<h2><a href="([^"]+)">In (ffmpeg_<wbr>next(?:::<wbr>[^<]*(?:<wbr>[^<]*)*)?)</a></h2>',
        repl, content
    )


def translate_all_html(content):
    """Translate the all.html file (list of all items)."""
    pairs = [
        ('<meta name="description" content="List of all items in this crate">',
         '<meta name="description" content="本 crate 中的所有项列表">'),
        ('<title>List of all items in this crate</title>',
         '<title>本 crate 中所有项的列表</title>'),
        ('<h1>List of all items</h1>', '<h1>所有项列表</h1>'),
        # h3 section headers in all.html
        ('<h3 id="structs">Structs', '<h3 id="structs">结构体'),
        ('<h3 id="enums">Enums', '<h3 id="enums">枚举'),
        ('<h3 id="traits">Traits', '<h3 id="traits">trait'),
        ('<h3 id="macros">Macros', '<h3 id="macros">宏'),
        ('<h3 id="functions">Functions', '<h3 id="functions">函数'),
        ('<h3 id="constants">Constants', '<h3 id="constants">常量'),
        # Topbar h2 (just "All Items")
        ('<rustdoc-topbar><h2><a href="#">All Items</a></h2>',
         '<rustdoc-topbar><h2><a href="#">所有项</a></h2>'),
        # Sidebar h2 location
        ('<h2 class="location"><a href="#">Crate ffmpeg_<wbr>next</a></h2>',
         '<h2 class="location"><a href="#">crate ffmpeg_<wbr>next</a></h2>'),
        ('>Crate Items</a>', '>crate 项</a>'),
        # Sidebar h2 (Crate ffmpeg_next at top)
        ('>Crate ffmpeg_<wbr>next<', '>crate ffmpeg_<wbr>next<'),
        # title attrs in all.html
        ('title="Structs"', 'title="结构体"'),
        ('title="Enums"', 'title="枚举"'),
        ('title="Traits"', 'title="trait"'),
        ('title="Macros"', 'title="宏"'),
        ('title="Functions"', 'title="函数"'),
        ('title="Constants"', 'title="常量"'),
        # sidebar h3 anchors
        ('>Structs</a>', '>结构体</a>'),
        ('>Enums</a>', '>枚举</a>'),
        ('>Traits</a>', '>trait</a>'),
        ('>Macros</a>', '>宏</a>'),
        ('>Functions</a>', '>函数</a>'),
        ('>Constants</a>', '>常量</a>'),
    ]
    content = apply_pairs(content, pairs)
    content = apply_pairs(content, COMMON_UI)
    return content


def translate_topbar(content):
    """The topbar h2 contains a plain identifier (e.g. <h2><a href="#">Audio</a></h2>).
    Leave the identifier alone — just nothing to translate here.
    """
    return content


def translate_sidebar_location(content):
    """h2.location holds the type identifier, sometimes plain like 'Audio'.
    The literal pattern <h2 class="location"><a href="#">IDENT</a></h2> is kept as-is.
    But sidebar-crate h2 has the crate name with wbr — leave that.
    """
    return content


def translate_non_index(content, filepath):
    """Main translation pipeline for any non-index, non-special HTML file."""
    content = translate_meta_and_h1(content, filepath)
    content = translate_breadcrumb_in(content)
    content = apply_pairs(content, COMMON_UI)
    content = apply_pairs(content, COMMON_TEXT)
    return content


def translate_redirect(content):
    """Translate small redirect-stub HTML files."""
    pairs = [
        ('<title>Redirection</title>', '<title>重定向</title>'),
        ('>Redirecting to ', '>正在重定向到 '),
    ]
    return apply_pairs(content, pairs)


def main():
    targets = []
    for dp, _, fns in os.walk(FFMPEG_NEXT_ROOT):
        for fn in fns:
            if fn.endswith('.html') and fn != 'index.html':
                targets.append(os.path.join(dp, fn))
    targets.sort()

    print(f'Found {len(targets)} non-index HTML files\n')

    total_cjk = 0
    fails = 0
    for path in targets:
        rel = os.path.relpath(path, FFMPEG_NEXT_ROOT)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        base = os.path.basename(path)
        if base == 'all.html':
            new_content = translate_all_html(content)
        elif 'http-equiv="refresh"' in content:
            new_content = translate_redirect(content)
        else:
            new_content = translate_non_index(content, path)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        cjk = verify(new_content, rel)
        total_cjk += cjk
        if cjk < 5 and 'http-equiv="refresh"' not in content:
            print(f'  [LOW] {rel}: only {cjk} CJK chars')
            fails += 1

    print(f'\n=== Summary ===')
    print(f'Files: {len(targets)}')
    print(f'Total CJK: {total_cjk}')
    print(f'Low-CJK files: {fails}')


if __name__ == '__main__':
    main()
