"""Translate enigo's cargo doc index.html files to Chinese.

Workflow per rust-doc-translation-pattern:
- Use Python open() directly (no Read tool).
- Apply (old, new) replacements in long-string-first order.
- Preserve HTML structure, URLs, Rust identifiers.
"""

import os
import re

ENIGO_ROOT = 'D:/Administrator/Documents/Code/rust_doc_all/enigo'


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


# Translation tables for common UI text
COMMON = [
    # Sidebar / nav headers
    ('>Sections<', '>章节<'),
    ('>Crate Items<', '>crate 项<'),
    ('>All Items<', '>所有项<'),
    ('>Module Items<', '>模块项<'),
    ('>In crate enigo<', '>在 crate enigo 中<'),
    # Buttons
    ('>Copy item path<', '>复制项目路径<'),
    ('>Source<', '>源代码<'),
    ('>Expand description<', '>展开描述<'),
    # Skip link
    ('>Skip to main content<', '>跳到主要内容<'),
    # IE warning
    ('This old browser is unsupported and will most likely display funky things.',
     '此旧版浏览器不受支持，很可能会显示异常内容。'),
    # Section headers (H2 inside doc and H3 in TOC)
    ('>Examples<', '>示例<'),
    ('>Modules<', '>模块<'),
    ('>Structs<', '>结构体<'),
    ('>Enums<', '>枚举<'),
    ('>Constants<', '>常量<'),
    ('>Traits<', '>trait<'),
    ('>Functions<', '>函数<'),
    ('>Type Aliases<', '>类型别名<'),
    # Crate / module name in heading
    ('>Crate enigo<', '>crate enigo<'),
    ('>Module agent<', '>模块 agent<'),
    ('>Crate <span>enigo</span>', '>crate <span>enigo</span>'),
    ('>Module <span>agent</span>', '>模块 <span>agent</span>'),
]


def translate_enigo_index(content):
    # Apply common UI replacements first
    for old, new in COMMON:
        if old not in content:
            print(f'  [MISS] enigo common: {old[:60]!r}')
        content = content.replace(old, new)

    # Meta description (single line)
    old_desc = '<meta name="description" content="Enigo lets you simulate mouse and keyboard input-events as if they were made by the actual hardware. It is available on Linux (X11), macOS and Windows.">'
    new_desc = '<meta name="description" content="Enigo 可以让你模拟鼠标和键盘输入事件，效果如同真实硬件产生的事件。它支持 Linux (X11)、macOS 和 Windows。">'
    content = content.replace(old_desc, new_desc)

    # Title
    content = content.replace('<title>enigo - Rust</title>', '<title>enigo - Rust</title>')
    content = content.replace('<html lang="en">', '<html lang="zh-CN">')

    # ---- Docblock (main intro) ----
    intro_pairs = [
        # Para 1
        ('<p>Enigo lets you simulate mouse and keyboard input-events as if they were\nmade by the actual hardware. It is available on Linux (X11), macOS and\nWindows.</p>',
         '<p>Enigo 可以让你模拟鼠标和键盘输入事件，效果如同真实硬件产生的事件。它支持 Linux (X11)、macOS 和 Windows。</p>'),
        # Para 2
        ('<p>It can be used for testing user interfaces on different platforms, building\nremote control applications or just automating tasks for user interfaces\nunaccessible by a public API or scripting language.</p>',
         '<p>它可以用于跨平台测试用户界面、构建远程控制应用，或自动化那些没有公开 API 或脚本语言无法访问的用户界面任务。</p>'),
        # Para 3
        ('<p>This library is in an early alpha status, the API will change in\nin the future.</p>',
         '<p>本库尚处于早期 alpha 状态，API 在未来可能会发生变化。</p>'),
        # Para 4
        ('<p>In order to use the library, you only have to know about three\nthings:</p>',
         '<p>要使用本库，你只需要了解三件事：</p>'),
        # List items
        ('(trait): used to simulate a key click, enter text or\nsomething similar',
         '（trait）：用于模拟按键点击、输入文本或类似操作'),
        ('(trait): do something with the mouse or you find out the display\nsize',
         '（trait）：用于操作鼠标或获取显示屏尺寸'),
        ('(struct): implements the two traits',
         '（结构体）：实现了上述两个 trait'),
        # Para 5 (DSL -> serde). The DSL paragraph is one <p> block; translate word groups.
        ('This crate previously included a simple DSL. This is no longer the case.',
         '本 crate 此前包含一个简单的 DSL，但现已移除。'),
        ('In order to simplify the codebase and also allow serializing objects, you can now serialize and deserialize most enums and structs of this crate. You can use this instead of the DSL.',
         '为了简化代码并支持对象序列化，你现在可以对本 crate 中的大多数枚举和结构体进行序列化和反序列化，以替代原来的 DSL。'),
        ('This feature is hidden behind the',
         '该功能通过'),
        ('feature. Have a look at the',
         '特性启用。可以查看'),
        ('example to see how to use it to serialize Tokens in the',
         '示例了解如何使用它以'),
        ('format.',
         '格式序列化 Token。'),
    ]
    for old, new in intro_pairs:
        if old not in content:
            print(f'  [MISS] enigo intro: {old[:60]!r}')
        content = content.replace(old, new)

    # ---- Code comments in example block ----
    code_comment_pairs = [
        ('<span class="comment">// Paste\n</span>', '<span class="comment">// 粘贴\n</span>'),
        ('<span class="comment">// Do things with the mouse\n</span>', '<span class="comment">// 操作鼠标\n</span>'),
        ('<span class="comment">// Enter text\n</span>', '<span class="comment">// 输入文本\n</span>'),
    ]
    for old, new in code_comment_pairs:
        if old not in content:
            print(f'  [MISS] enigo index code comment: {old[:60]!r}')
        content = content.replace(old, new)

    # ---- Item descriptions ----
    item_pairs = [
        # Structs
        ('<dd>The main struct for handling the event emitting</dd>',
         '<dd>用于处理事件发送的主结构体</dd>'),
        ('<dd>Settings for creating the Enigo struct and it’s behavior</dd>',
         '<dd>用于创建 Enigo 结构体及其行为的设置</dd>'),
        # Enums
        ('<dd>Specifies the axis for scrolling</dd>',
         '<dd>指定滚动的轴</dd>'),
        ('<dd>Represents a mouse button and is used in e.g\n',
         '<dd>表示鼠标按键，用于例如\n'),
        ('<dd>Specifies if a coordinate is relative or absolute</dd>',
         '<dd>指定坐标是相对坐标还是绝对坐标</dd>'),
        ('<dd>The direction of a key or button</dd>',
         '<dd>按键或按钮的方向</dd>'),
        ('<dd>Error when simulating input</dd>',
         '<dd>模拟输入时的错误</dd>'),
        ('<dd>Error when establishing a new connection</dd>',
         '<dd>建立新连接时的错误</dd>'),
        # Key enum - long description (use line-based replacements to preserve links)
        ('<dd>Contains the available keycodes\n',
         '<dd>包含所有可用的按键码。\n'),
        ('Use ', '使用 '),
        ('to enter arbitrary Unicode chars.\n',
         '输入任意 Unicode 字符。\n'),
        ('If a key is missing, please open an issue in our repo and we will quickly\nadd it. In the mean time, you can simulate that key by using ',
         '如果缺少某个按键，请在我们的仓库中提交 issue，我们会尽快添加。同时，你可以通过 '),
        ('or the\n', '或\n'),
        ('function. Some of the keys are only\navailable on a specific platform. Use conditional compilation to use them.',
         '函数模拟该按键。某些按键仅在特定平台上可用，请使用条件编译来使用它们。'),
        # Constants
        ('<dd>Arbitrary value to be able to distinguish events created by enigo</dd>',
         '<dd>用于区分由 enigo 创建的事件的任意值</dd>'),
        # Traits
        ('<dd>Contains functions to simulate key presses/releases and to input text.</dd>',
         '<dd>包含模拟按键按下/释放和输入文本的函数。</dd>'),
        # Mouse trait - long
        ('<dd>Contains functions to control the mouse and to get the size of the display.\n',
         '<dd>包含控制鼠标和获取显示屏尺寸的函数。\n'),
        ('Enigo uses a cartesian coordinate system for specifying coordinates. The\norigin in this system is located in the top-left corner of the current\nscreen, with positive values extending along the axes down and to the\nright of the origin point and it is measured in pixels. The same coordinate\nsystem is used on all operating systems.',
         'Enigo 使用笛卡尔坐标系来指定坐标。该坐标系的原点位于当前屏幕的左上角，正值沿坐标轴向下和向右延伸，单位为像素。所有操作系统均使用相同的坐标系。'),
        # Functions
        ('<dd>Sets the current process to a specified dots per inch (dpi) awareness\ncontext ',
         '<dd>将当前进程设置为指定的每英寸点数 (dpi) 感知上下文 '),
        ('>see official documentation<',
         '>参见官方文档<'),
        ('If you want your applications to respect the users scaling, you need to set\nthis. Otherwise the mouse coordinates and screen dimensions will be off.',
         '如果希望应用程序遵循用户的缩放比例，则需要设置此项。否则鼠标坐标和屏幕尺寸将不准确。'),
        # agent module description (inside the Modules <dl>)
        # The <dd> starts with "This crate contains the" and has multiple sentences with embedded links.
        ('<dd>This crate contains the ',
         '<dd>本 crate 包含 '),
        (' struct and the\n', ' 枚举和\n'),
        (' trait. A token is an instruction for the ', ' trait。Token 是用于让 '),
        ('\nstruct to do something. If you want Enigo to simulate input, you then have\nto tell the enigo struct to ',
         '\n结构体执行某些操作的指令。如果希望 Enigo 模拟输入，则需要让 enigo 结构体 '),
        (' the token. Have\na look at the ',
         ' 该 token。如果想阅读相关代码，可以查看 '),
        (' example if you’d like to read some code to see how it\nworks.',
         ' 示例了解其工作原理。'),
    ]
    for old, new in item_pairs:
        if old not in content:
            print(f'  [MISS] enigo item: {old[:60]!r}')
        content = content.replace(old, new)

    return content


def translate_agent_index(content):
    for old, new in COMMON:
        if old not in content:
            print(f'  [MISS] agent common: {old[:60]!r}')
        content = content.replace(old, new)

    # Meta description
    old_meta = '<meta name="description" content="This crate contains the `crate::agent::Token` struct and the `crate::agent::Agent` trait. A token is an instruction for the `Enigo` struct to do something. If you want Enigo to simulate input, you then have to tell the enigo struct to `crate::agent::Agent::execute` the token. Have a look at the `serde` example if you’d like to read some code to see how it works.">'
    new_meta = '<meta name="description" content="本 crate 包含 `crate::agent::Token` 枚举和 `crate::agent::Agent` trait。Token 是用于让 `Enigo` 结构体执行某些操作的指令。如果希望 Enigo 模拟输入，则需要让 enigo 结构体 `crate::agent::Agent::execute` 该 token。如果想阅读相关代码，可以查看 `serde` 示例了解其工作原理。">'
    content = content.replace(old_meta, new_meta)

    # Title
    content = content.replace('<title>enigo::agent - Rust</title>', '<title>enigo::agent - Rust</title>')
    content = content.replace('<html lang="en">', '<html lang="zh-CN">')

    # Docblock description
    desc_pairs = [
        ('This crate contains the ',
         '本 crate 包含 '),
        (' struct and the\n',
         ' 枚举和\n'),
        (' trait. A token is an instruction for the ',
         ' trait。Token 是用于让 '),
        ('\nstruct to do something. If you want Enigo to simulate input, you then have\nto tell the enigo struct to ',
         '\n结构体执行某些操作的指令。如果希望 Enigo 模拟输入，则需要让 enigo 结构体 '),
        (' the token. Have\na look at the ',
         ' 该 token。如果想阅读相关代码，可以查看 '),
        (' example if you’d like to read some code to see how it\nworks.',
         ' 示例了解其工作原理。'),
    ]
    for old, new in desc_pairs:
        if old not in content:
            print(f'  [MISS] agent desc: {old[:60]!r}')
        content = content.replace(old, new)

    return content


def main():
    targets = [
        (os.path.join(ENIGO_ROOT, 'index.html'), translate_enigo_index),
        (os.path.join(ENIGO_ROOT, 'agent', 'index.html'), translate_agent_index),
    ]
    for path, fn in targets:
        print(f'--- {path} ---')
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        new_content = fn(content)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        rel = os.path.relpath(path, ENIGO_ROOT)
        verify(new_content, rel)
        print()


if __name__ == '__main__':
    main()