"""
Translate all non-index.html files in enigo directory to Chinese.

Workflow per rust-doc-translation-pattern:
- Use Python open() directly (no Read tool).
- Apply (old, new) replacements in long-string-first order.
- Preserve HTML structure, URLs, Rust identifiers.
"""

import os
import re

ENIGO_ROOT = 'D:/Administrator/Documents/Code/rust_doc_all/enigo'


def verify(content, label):
    """Verify a translated HTML file."""
    line_artifacts = re.findall(r'^\d+\t', content, flags=re.MULTILINE)
    if line_artifacts:
        print(f'  [WARN] {label}: {len(line_artifacts)} lines with cat-n style line numbers')

    cjk = re.findall(r'[一-鿿]', content)
    print(f'  [INFO] {label}: {len(cjk)} CJK characters')

    tag_pairs = ['html', 'head', 'body', 'main', 'section', 'div', 'p',
                 'a', 'span', 'h1', 'h2', 'h3', 'h4', 'ul', 'li',
                 'code', 'pre', 'details', 'summary', 'dl', 'dt', 'dd']
    bad = []
    for t in tag_pairs:
        opens = len(re.findall(rf'<{t}[\s>]', content))
        closes = len(re.findall(rf'</{t}>', content))
        if opens != closes:
            bad.append((t, opens, closes))
    if bad:
        for t, o, c in bad:
            print(f'  [WARN] {label}: <{t}> open={o} close={c} diff={o-c}')


# ============================================================================
# Common UI replacements (apply to all files)
# ============================================================================
COMMON_UI = [
    # Sidebar / nav headers
    ('>Sections<', '>章节<'),
    ('>Crate Items<', '>crate 项<'),
    ('>All Items<', '>所有项<'),
    ('>Module Items<', '>模块项<'),
    ('>In crate enigo<', '>在 crate enigo 中<'),
    ('>In enigo::<wbr>agent<', '>在 enigo::<wbr>agent 中<'),
    ('>In enigo::agent<', '>在 enigo::agent 中<'),
    # Buttons
    ('>Copy item path<', '>复制项目路径<'),
    ('>Source<', '>源代码<'),
    ('>Expand description<', '>展开描述<'),
    # Skip link
    ('>Skip to main content<', '>跳到主要内容<'),
    # IE warning
    ('This old browser is unsupported and will most likely display funky things.',
     '此旧版浏览器不受支持，很可能会显示异常内容。'),
    # Section headers
    ('>Examples<', '>示例<'),
    ('>Modules<', '>模块<'),
    ('>Structs<', '>结构体<'),
    ('>Enums<', '>枚举<'),
    ('>Constants<', '>常量<'),
    ('>Traits<', '>trait<'),
    ('>Functions<', '>函数<'),
    ('>Type Aliases<', '>类型别名<'),
    ('>Trait Implementations<', '>trait 实现<'),
    ('>Auto Trait Implementations<', '>自动 trait 实现<'),
    ('>Blanket Implementations<', '>blanket 实现<'),
    ('>Required Methods<', '>必需方法<'),
    ('>Provided Methods<', '>提供方法<'),
    ('>Implementors<', '>实现者<'),
    ('>Implementations<', '>实现<'),
    ('>Methods<', '>方法<'),
    ('>Variants<', '>变体<'),
    ('>Fields<', '>字段<'),
    ('>Tuple Fields<', '>元组字段<'),
    ('>Aliased Type<', '>别名类型<'),
    ('>Associated Constants<', '>关联常量<'),
    ('>Associated Types<', '>关联类型<'),
    # Errors / safety / examples
    ('>Errors<', '>错误<'),
    ('>Panics<', '>恐慌<'),
    ('>Safety<', '>安全性<'),
    # Crate / module name in heading
    ('>Crate enigo<', '>crate enigo<'),
    ('>Module agent<', '>模块 agent<'),
    # Page heading types
    ('<h1>List of all items</h1>', '<h1>所有项列表</h1>'),
    ('<h1>All<', '<h1>全部<'),  # in topbar h2 actually
    # Crate / module name in heading for index main heading
    ('>Crate <span>enigo</span>', '>crate <span>enigo</span>'),
    ('>Module <span>agent</span>', '>模块 <span>agent</span>'),
    # title attributes
    ('title="Examples"', 'title="示例"'),
    ('title="Modules"', 'title="模块"'),
    ('title="Structs"', 'title="结构体"'),
    ('title="Enums"', 'title="枚举"'),
    ('title="Constants"', 'title="常量"'),
    ('title="Traits"', 'title="trait"'),
    ('title="Functions"', 'title="函数"'),
    ('title="Type Aliases"', 'title="类型别名"'),
    ('title="Required Methods"', 'title="必需方法"'),
    ('title="Provided Methods"', 'title="提供方法"'),
    ('title="Implementors"', 'title="实现者"'),
    ('title="Implementations"', 'title="实现"'),
    ('title="Trait Implementations"', 'title="trait 实现"'),
    ('title="Auto Trait Implementations"', 'title="自动 trait 实现"'),
    ('title="Blanket Implementations"', 'title="blanket 实现"'),
    ('title="Methods"', 'title="方法"'),
    ('title="Variants"', 'title="变体"'),
    ('title="Fields"', 'title="字段"'),
    ('title="Tuple Fields"', 'title="元组字段"'),
    ('title="Aliased Type"', 'title="别名类型"'),
    ('title="Associated Constants"', 'title="关联常量"'),
    ('title="Associated Types"', 'title="关联类型"'),
    ('title="Errors"', 'title="错误"'),
    ('title="Panics"', 'title="恐慌"'),
    ('title="Safety"', 'title="安全性"'),
    # Crate / module title attributes
    ('title="mod enigo::agent"', 'title="模块 enigo::agent"'),
    ('title="struct enigo::Enigo"', 'title="结构体 enigo::Enigo"'),
    ('title="struct enigo::Settings"', 'title="结构体 enigo::Settings"'),
    ('title="enum enigo::Axis"', 'title="枚举 enigo::Axis"'),
    ('title="enum enigo::Button"', 'title="枚举 enigo::Button"'),
    ('title="enum enigo::Coordinate"', 'title="枚举 enigo::Coordinate"'),
    ('title="enum enigo::Direction"', 'title="枚举 enigo::Direction"'),
    ('title="enum enigo::InputError"', 'title="枚举 enigo::InputError"'),
    ('title="enum enigo::Key"', 'title="枚举 enigo::Key"'),
    ('title="enum enigo::NewConError"', 'title="枚举 enigo::NewConError"'),
    ('title="constant enigo::EVENT_MARKER"', 'title="常量 enigo::EVENT_MARKER"'),
    ('title="constant enigo::EXT"', 'title="常量 enigo::EXT"'),
    ('title="trait enigo::Keyboard"', 'title="trait enigo::Keyboard"'),
    ('title="trait enigo::Mouse"', 'title="trait enigo::Mouse"'),
    ('title="fn enigo::set_dpi_awareness"', 'title="函数 enigo::set_dpi_awareness"'),
    ('title="type enigo::InputResult"', 'title="类型别名 enigo::InputResult"'),
    # Method / variant title attrs
    ('title="variant enigo::Key::Unicode"', 'title="变体 enigo::Key::Unicode"'),
    ('title="variant enigo::Key::Other"', 'title="变体 enigo::Key::Other"'),
    ('title="method enigo::Mouse::button"', 'title="方法 enigo::Mouse::button"'),
    ('title="method enigo::Keyboard::raw"', 'title="方法 enigo::Keyboard::raw"'),
    ('title="method enigo::agent::Agent::execute"', 'title="方法 enigo::agent::Agent::execute"'),
    # agent-specific
    ('title="enum enigo::agent::Token"', 'title="枚举 enigo::agent::Token"'),
    ('title="trait enigo::agent::Agent"', 'title="trait enigo::agent::Agent"'),
    # Misc title attrs
    ('title="Copy item path to clipboard"', 'title="复制项目路径到剪贴板"'),
    ('title="Drag to resize sidebar"', 'title="拖动以调整侧边栏宽度"'),
]

# ============================================================================
# Common free-text / descriptive phrases (apply to all files where they appear)
# ============================================================================
COMMON_TEXT = [
    # "Read more" suffix on docblocks
    ('>Read more<', '>阅读更多<'),
    # Standard rustdoc phrases
    ('Returns the argument unchanged.', '原样返回参数。'),
    ('Calls U::from(self).', '调用 U::from(self)。'),
    ('That is, this conversion is whatever the implementation of',
     '也就是说，此转换是'),
    ('chooses to do.', '实现选择执行的操作。'),
    ('Performs the conversion.', '执行该转换。'),
    ('The type returned in the event of a conversion error.',
     '转换出错时返回的类型。'),
    ('The type returned in the event of a conversion error',
     '转换出错时返回的类型'),
    # "Converts a ..."
    ('Converts a Key to a Virtual Key', '将 Key 转换为 Virtual Key'),
    # Standard traits
    ('Formats the value using the given formatter.',
     '使用给定的格式化器格式化该值。'),
    ('Executes the destructor for this type.',
     '执行该类型的析构函数。'),
    ('Immutably borrows from an owned value.',
     '从拥有的值不可变地借用。'),
    ('Mutably borrows from an owned value.',
     '从拥有的值可变地借用。'),
    ('Gets the <code>TypeId</code> of <code>self</code>.',
     '获取 <code>self</code> 的 <code>TypeId</code>。'),
    # "Read more" links inside div class docblock
    ('</div>. <a href=', '。</div> <a href='),
    # The Hash partial description (rare)
    ('FEATURE_IDX', '特性索引'),
    # port/stab
    ('Available on <strong>Windows</strong> only.', '仅在 <strong>Windows</strong> 上可用。'),
    ('Available on <strong>Linux</strong> only.', '仅在 <strong>Linux</strong> 上可用。'),
    ('Available on <strong>macOS</strong> only.', '仅在 <strong>macOS</strong> 上可用。'),
    ('Available on <strong>crate features serde</strong> only.',
     '仅在启用了 <strong>serde 特性</strong> 时可用。'),
    ('Stable since Rust version 1.0.0', '自 Rust 1.0.0 起稳定'),
    # Generic phrase
    ('Contains the success value', '包含成功值'),
    ('Contains the error value', '包含错误值'),
    # The returns argument unchanged
    ('Returns the argument unchanged', '原样返回参数'),
    # Calls U::from(self)
    ('Calls U::from(self)', '调用 U::from(self)'),
    # Trait name "for T" / "for Self" -- only in headers, leave alone
    # On Linux, this will result in a keysym,
    ('On Linux, this will result in a keysym,', '在 Linux 上将得到一个 keysym，'),
    ('On Windows, this will result in a <code>Virtual_Key</code> and',
     '在 Windows 上将得到一个 <code>Virtual_Key</code>，'),
    ('On macOS, this will yield a <code>KeyCode</code>',
     '在 macOS 上将产生一个 <code>KeyCode</code>'),
    # "Equivalent to a press followed by a release"
    ('Equivalent to a press followed by a release',
     '相当于按下后立即释放'),
    # "Converts a Key to a Virtual Key" already handled
    # Hash docblocks
    ('Implemented the same way as ', '与 '),
    # Some common descriptions
    ('Move the mouse cursor to the specified x and y coordinates.',
     '将鼠标光标移动到指定的 x 和 y 坐标。'),
    # Mouse trait - move_mouse / scroll description (trait.Mouse.html)
    ('You can specify absolute coordinates or relative from the current\nposition.',
     '你可以指定绝对坐标，或相对于当前位置的相对坐标。'),
    ('If you use absolute coordinates, the top left corner of your monitor\nscreen is x=0 y=0. Move the cursor down the screen by increasing the y\nand to the right by increasing x coordinate.',
     '若使用绝对坐标，显示器屏幕左上角为 x=0 y=0。增大 y 坐标使光标下移，增大 x 坐标使光标右移。'),
    ('If you use relative coordinates, a positive x value moves the mouse\ncursor <code>x</code> pixels to the right. A negative value for <code>x</code> moves the mouse\ncursor to the left. A positive value of y moves the mouse cursor down, a\nnegative one moves the mouse cursor up.',
     '若使用相对坐标，<code>x</code> 为正值时鼠标光标向右移动相应像素；为负值时向左移动。y 为正值时光标下移，为负值时光标上移。'),
    ('With Axis::Vertical, a positive length will result in scrolling down\nand negative ones up. With Axis::Horizontal, a positive length\nwill result in scrolling to the right and negative ones to the left.',
     '对于 Axis::Vertical，正长度值向下滚动，负长度值向上滚动。对于 Axis::Horizontal，正长度值向右滚动，负长度值向左滚动。'),
    ('Send a mouse scroll event', '发送鼠标滚轮事件'),
    ('Get the (width, height) of the main display in pixels. This currently\nonly works on the main display',
     '获取主显示屏的（宽度，高度）像素值。目前仅支持主显示屏'),
    ('Get the location of the mouse in pixels', '获取鼠标位置的像素坐标'),
    # Settings for ...
    ('Settings for creating the Enigo struct and it’s behavior',
     '用于创建 Enigo 结构体及其行为的设置'),
    # Description for EVENT_MARKER
    ('Arbitrary value to be able to distinguish events created by enigo',
     '用于区分由 enigo 创建的事件的任意值'),
    # Main Enigo struct desc
    ('The main struct for handling the event emitting', '用于处理事件发送的主结构体'),
    # Keyboard trait desc
    ('Contains functions to simulate key presses/releases and to input text.',
     '包含模拟按键按下/释放和输入文本的函数。'),
    # Long Keyboard trait docblock
    ('For entering text, the ', '对于输入文本，'),
    ('function is best.', '函数是最佳选择。'),
    ('If you want to enter a key without having to worry about the layout or the\nkeymap, use the ',
     '如果希望输入按键而无需关心布局或键位映射，请使用 '),
    ('function. If you want a\nspecific (physical) key to be pressed (e.g WASD for games), use the',
     '函数。如果希望按下某个特定的（物理）按键（例如游戏中常用的 WASD），请使用'),
    ('function. The resulting keysym will depend\non the layout/keymap.',
     '函数。最终得到的 keysym 取决于布局/键位映射。'),
    # Keyboard::key method
    ('Sends an individual key event. It will enter the keysym (virtual key).\nHave a look at the ',
     '发送单个按键事件。它会输入 keysym（虚拟键）。如需输入 keycode，请参考 '),
    ('function, if you\nwant to enter a keycode.', '函数。'),
    ('Some of the keys are specific to a platform.', '某些按键是平台特有的。'),
    ('Have a look at the documentation of ',
     '请参考 '),
    ('to see under which\nconditions an error will be returned.',
     '的文档以了解在哪些情况下会返回错误。'),
    ('to see under which other conditions an\nerror will be returned.',
     '的文档以了解在哪些其他情况下会返回错误。'),
    # Keyboard::raw method
    ('Sends a raw keycode. The keycode may or may not be mapped on the current\nlayout. You have to make sure of that yourself. This can be useful if\nyou want to simulate a press regardless of the layout (WASD on video\ngames). Have a look at the ',
     '发送原始 keycode。keycode 在当前布局下可能已映射或未映射，你需要自行确认。如果你希望无论布局如何都模拟同一个按键（如游戏中常用的 WASD），此函数非常有用。请参考 '),
    ('function,\nif you just want to enter a specific key and don’t want to worry about\nthe layout/keymap.',
     '函数，如果你只想输入某个特定按键而无需关心布局/键位映射。'),
    ('Windows only: If you want to enter the keycode\n(scancode) of an extended key, you need to set extra bits. You can\nfor example do: ',
     '仅 Windows：如果你希望输入扩展按键的 keycode（扫描码），需要设置额外的位。例如可以这样：'),
    # Keyboard::text method
    ('Enter the text\nUse a fast method to enter the text, if it is available. You can use\nunicode here like: ❤️. This works regardless of the current keyboard\nlayout. You cannot use this function for entering shortcuts or\nsomething similar. For shortcuts, use the',
     '输入文本\n如果可用，使用快速方法输入文本。你可以在这里使用 Unicode 字符，例如：❤️。这与当前键盘布局无关。不能使用此函数输入快捷键或类似的组合。输入快捷键请使用'),
    ('method instead.', '方法。'),
    ('The text should not contain any NULL bytes (', '文本不能包含 NULL 字节（'),
    ('). Have a look at the\ndocumentation of ',
     '）。请参考'),
    ('to see under which other conditions an\nerror will be returned.', '的文档以了解在哪些其他情况下会返回错误。'),
    # Key enum general description
    ('Contains the available keycodes\n',
     '包含所有可用的按键码。\n'),
    ('to enter arbitrary Unicode chars.\n',
     '输入任意 Unicode 字符。\n'),
    ('If a key is missing, please open an issue in our repo and we will quickly\nadd it. In the mean time, you can simulate that key by using ',
     '如果缺少某个按键，请在我们的仓库中提交 issue，我们会尽快添加。同时，你可以通过 '),
    ('or the\n', '或\n'),
    ('function. Some of the keys are only\navailable on a specific platform. Use conditional compilation to use them.',
     '函数模拟该按键。某些按键仅在特定平台上可用，请使用条件编译来使用它们。'),
    # Key variants
    ('alt key on Linux and Windows (option key on macOS)',
     'Linux 和 Windows 上的 Alt 键（macOS 上的 Option 键）'),
    ('backspace key', '退格键（Backspace）'),
    ('caps lock key', '大写锁定键（CapsLock）'),
    ('control key', '控制键（Control）'),
    ('delete key', '删除键（Delete）'),
    ('down arrow key', '下方向键'),
    ('end key', 'End 键'),
    ('escape key (esc)', '退出键（Esc）'),
    ('F1 key', 'F1 键'),
    ('F2 key', 'F2 键'),
    ('F3 key', 'F3 键'),
    ('F4 key', 'F4 键'),
    ('F5 key', 'F5 键'),
    ('F6 key', 'F6 键'),
    ('F7 key', 'F7 键'),
    ('F8 key', 'F8 键'),
    ('F9 key', 'F9 键'),
    ('F10 key', 'F10 键'),
    ('F11 key', 'F11 键'),
    ('F12 key', 'F12 键'),
    ('F13 key', 'F13 键'),
    ('F14 key', 'F14 键'),
    ('F15 key', 'F15 键'),
    ('F16 key', 'F16 键'),
    ('F17 key', 'F17 键'),
    ('F18 key', 'F18 键'),
    ('F19 key', 'F19 键'),
    ('F20 key', 'F20 键'),
    ('F21 key', 'F21 键'),
    ('F22 key', 'F22 键'),
    ('F23 key', 'F23 键'),
    ('F24 key', 'F24 键'),
    ('home key', 'Home 键'),
    ('left arrow key', '左方向键'),
    ('meta key (also known as “windows”, “super”, and “command”)',
     'Meta 键（也称为"windows"、"super"和"command"）'),
    ('option key on macOS (alt key on Linux and Windows)',
     'macOS 上的 Option 键（Linux 和 Windows 上的 Alt 键）'),
    ('page down key', '向下翻页键（PageDown）'),
    ('page up key', '向上翻页键（PageUp）'),
    ('Take a screenshot', '截屏键（PrintScreen）'),
    ('return key', '回车键（Return）'),
    ('right arrow key', '右方向键'),
    ('shift key', 'Shift 键'),
    ('space key', '空格键'),
    ('tab key (tabulator)', 'Tab 键（制表符）'),
    ('up arrow key', '上方向键'),
    ('Unicode character', 'Unicode 字符'),
    # Key::Other long description
    ('Use this for keys that are not listed here that you know the\nvalue of. Let us know if you think the key should be listed so\nwe can add it',
     '对于此处未列出但你已知其取值的按键，请使用此项。如果你认为某个按键应该被列出，请告知我们，我们会尽快添加。'),
    ('Yield a keycode, see the <a href="enum.Key.html#variant.Other"',
     '产生一个 keycode，请参阅 <a href="enum.Key.html#variant.Other"'),
    # Axis enum
    ('Specifies the axis for scrolling', '指定滚动的轴'),
    # Button enum
    ('Represents a mouse button and is used in e.g',
     '表示鼠标按键，用于例如'),
    ('Left mouse button', '鼠标左键'),
    ('Middle mouse button', '鼠标中键'),
    ('Right mouse button', '鼠标右键'),
    ('4th mouse button. Typically performs the same function as Browser_Back',
     '第 4 个鼠标按键。通常执行与 Browser_Back 相同的功能'),
    ('5th mouse button. Typically performs the same function as Browser_Forward',
     '第 5 个鼠标按键。通常执行与 Browser_Forward 相同的功能'),
    ('Scroll up button. It is better to use the ',
     '向上滚动按键。最好使用 '),
    ('Scroll down button. It is better to use the ',
     '向下滚动按键。最好使用 '),
    ('Scroll left button. It is better to use the ',
     '向左滚动按键。最好使用 '),
    ('Scroll right button. It is better to use the ',
     '向右滚动按键。最好使用 '),
    ('method to scroll.', '方法来滚动。'),
    # Coordinate enum
    ('Specifies if a coordinate is relative or absolute', '指定坐标是相对坐标还是绝对坐标'),
    # Direction enum
    ('The direction of a key or button', '按键或按钮的方向'),
    # InputError enum
    ('Error when simulating input', '模拟输入时的错误'),
    ('Mapping a keycode to a keysym failed', '将 keycode 映射到 keysym 失败'),
    ('Unmapping a keycode failed', '取消 keycode 映射失败'),
    ('There was no space to map any keycodes', '没有可用空间来映射任何 keycode'),
    ('There was an error with the protocol', '协议出错'),
    ('The input you want to simulate is invalid',
     '你想要模拟的输入无效'),
    ('This happens for example if you want to enter text that contains NULL bytes (',
     '例如当你尝试输入包含 NULL 字节（'),
    # NewConError enum
    ('Error when establishing a new connection', '建立新连接时的错误'),
    ('Error while creating the connection', '创建连接时出错'),
    ('The application does not have the permission to simulate input',
     '应用没有模拟输入的权限'),
    ('Error when receiving a reply', '接收响应时出错'),
    ('The keymap is full, so there was no space to map any keycodes to keysyms',
     '键位映射已满，没有空间将任何 keycode 映射到 keysym'),
    # set_dpi_awareness
    ('Sets the current process to a specified dots per inch (dpi) awareness\ncontext ',
     '将当前进程设置为指定的每英寸点数 (dpi) 感知上下文 '),
    ('>see official documentation<', '>参见官方文档<'),
    ('If you want your applications to respect the users scaling, you need to set\nthis. Otherwise the mouse coordinates and screen dimensions will be off.',
     '如果希望应用程序遵循用户的缩放比例，则需要设置此项。否则鼠标坐标和屏幕尺寸将不准确。'),
    ('It is recommended that you set the process-default DPI awareness via\napplication manifest, not an API call. See ',
     '建议通过应用程序清单设置进程的默认 DPI 感知，而不是通过 API 调用。详见 '),
    (' for more information. Setting the process-default DPI\nawareness via API call can lead to unexpected application behavior.\nIt also needs to be set before any APIs are used that depend on the DPI and\nbefore a UI is created.\nEnigo is a library and should not set this, because\nit will lead to unexpected scaling of the application. Only use it for\nexamples or if you know about the consequences',
     ' 以获取更多信息。通过 API 调用设置进程默认 DPI 感知可能导致应用程序出现意外行为。还需在任何依赖 DPI 的 API 被使用以及 UI 被创建之前完成设置。Enigo 是一个库，不应设置此项，因为这会导致应用程序的缩放出现异常。仅在示例中使用，或在你了解其后果时才使用。'),
    ('An error is thrown if the default API awareness mode for the process has\nalready been set (via a previous API call or within the application\nmanifest)',
     '如果进程的默认 API 感知模式已被设置（通过先前的 API 调用或在应用程序清单中设置），则会抛出错误。'),
    # Agent::execute
    ('Execute the action associated with the token. A ',
     '执行与 token 关联的动作。'),
    ('will\nenter text, a ', ' 将输入文本，'),
    ('will scroll and so forth. Have a look at\nthe documentation of the ',
     ' 将触发滚动，依此类推。更多信息请参考 '),
    ('enum for more information.', '枚举的文档。'),
    ('Same as the individual functions. Have a look at ',
     '与各单独函数相同。请参考 '),
    ('for a\nlist of possible errors', '以获取可能的错误列表。'),
    # Token variants
    ('Call the ', '调用 '),
    ('fn with the string as text', ' 函数，传入字符串作为文本'),
    ('fn with the given key and direction', ' 函数，传入给定的 key 和 direction'),
    ('fn with the given keycode and direction', ' 函数，传入给定的 keycode 和 direction'),
    ('fn with the given mouse button and direction', ' 函数，传入给定的鼠标按键和 direction'),
    ('fn. The first i32 is the value to move on the x-axis and the second i32 is the value to move on the y-axis. The coordinate defines if the given coordinates are absolute of relative to the current position of the mouse.',
     ' 函数。第一个 i32 是沿 x 轴移动的值，第二个 i32 是沿 y 轴移动的值。coordinate 决定给定的坐标是相对于当前鼠标位置的相对坐标还是绝对坐标。'),
    ('fn.', ' 函数。'),
    ('fn and compare the return values with the values of this enum. Log an error if they are not equal. This variant contains the EXPECTED location of the mouse',
     ' 函数并将其返回值与本枚举的值进行比较。若不相等则记录错误。本变体包含鼠标的预期位置。'),
    ('fn and compare the return values with the values of this enum. Log an error if they are not equal. This variant contains the EXPECTED size of the main display',
     ' 函数并将其返回值与本枚举的值进行比较。若不相等则记录错误。本变体包含主显示屏的预期尺寸。'),
    # Agent trait
    ('See the documentation of the ', '请参阅 '),
    (' for a list of possible errors', '的文档以获取可能的错误列表。'),
    # struct.Enigo methods
    ('Create a new Enigo struct to establish the connection to simulate input\nwith the specified settings',
     '创建一个新的 Enigo 结构体，以使用指定的设置建立连接来模拟输入'),
    ('Returns a list of all currently pressed keys',
     '返回当前所有被按下的按键列表'),
    ('Returns the value that enigo’s events are marked with',
     '返回 enigo 事件标记所使用的值'),
    # struct.Enigo Mouse trait impl
    ('Enter the whole text string instead of entering individual keys\nThis is much faster if you type longer text at the cost of keyboard\nshortcuts not getting recognized',
     '一次性输入完整文本字符串，而非逐个按键。输入较长文本时这种方法更快，但代价是无法识别键盘快捷键。'),
    ('Sends a key event to the X11 server via ', '通过 '),
    ('extension', ' 扩展向 X11 服务器发送按键事件。'),
    # struct.Enigo Mouse methods
    ('Sends an individual mouse button event. You can use this for example to\nsimulate a click of the left mouse key. Some of the buttons are specific\nto a platform.',
     '发送单个鼠标按键事件。例如你可以用此方法模拟左键点击。某些按键是平台特有的。'),
    ('Move the mouse cursor to the specified x and y coordinates.',
     '将鼠标光标移动到指定的 x 和 y 坐标。'),
    ('Send a mouse scroll event', '发送鼠标滚轮事件'),
    ('Get the (width, height) of the main display in pixels. This currently\nonly works on the main display',
     '获取主显示屏的（宽度，高度），单位为像素。目前仅支持主显示屏。'),
    ('Get the location of the mouse in pixels', '获取鼠标位置的像素坐标'),
    # struct.Settings fields
    ('Sleep delay on Linux X11', 'Linux X11 上的睡眠延迟'),
    ('Display name to connect to when using Linux X11', '使用 Linux X11 时要连接的显示名称'),
    ('Display name to connect to when using Linux Wayland', '使用 Linux Wayland 时要连接的显示名称'),
    ('All events will be marked with this value in the dwExtraInfo field',
     '所有事件都会在 dwExtraInfo 字段中标记此值'),
    ('All events will be marked with this value in the\n<code>EVENT_SOURCE_USER_DATA</code> field',
     '所有事件都会在 <code>EVENT_SOURCE_USER_DATA</code> 字段中标记此值'),
    ('Set this to true if you want all held keys to get released when Enigo\ngets dropped. The default is true.',
     '如果希望在 Enigo 被 drop 时释放所有按住的按键，请将此值设置为 true。默认值为 true。'),
    ('Open a prompt to ask the user for the permission to simulate input if\nthey are missing. This only works on macOS. The default is true.',
     '在缺少模拟输入权限时打开一个提示，向用户请求该权限。仅在 macOS 上可用。默认值为 true。'),
    ('The simulated input is independent from the pressed keys on the\nphysical keyboard. This only works on macOS.',
     '模拟输入与物理键盘上按下的按键无关。仅在 macOS 上可用。'),
    ('The default is true. If the Shift key for example is pressed,\nfollowing simulated input will not be capitalized.',
     '默认值为 true。例如当 Shift 键被按下时，后续模拟的输入不会被大写化。'),
    ('If this is set to true, the relative mouse motion will be subject to the\nsettings for mouse speed and acceleration level. An end user sets\nthese values using the Mouse application in Control Panel. An\napplication obtains and sets these values with the',
     '如果设置为 true，相对鼠标移动将受到鼠标速度和加速度级别设置的影响。最终用户可以在控制面板的"鼠标"应用中设置这些值。应用程序可以通过 '),
    ('function. The default value is false.',
     ' 函数获取和设置这些值。默认值为 false。'),
    # Mouse trait docblock
    ('Contains functions to control the mouse and to get the size of the display.\nEnigo uses a cartesian coordinate system for specifying coordinates. The\norigin in this system is located in the top-left corner of the current\nscreen, with positive values extending along the axes down and to the\nright of the origin point and it is measured in pixels. The same coordinate\nsystem is used on all operating systems.',
     '包含控制鼠标和获取显示屏尺寸的函数。\nEnigo 使用笛卡尔坐标系来指定坐标。该坐标系的原点位于当前屏幕的左上角，正值沿坐标轴向下和向右延伸，单位为像素。所有操作系统均使用相同的坐标系。'),
    # Mouse methods
    ('Sends an individual mouse button event. You can use this for example to\nsimulate a click of the left mouse key. Some of the buttons are specific\nto a platform.',
     '发送单个鼠标按键事件。例如你可以用此方法模拟左键点击。某些按键是平台特有的。'),
    # agent description (in agent/enum.Token.html, agent/trait.Agent.html main docblock)
    ('This crate contains the ', '本 crate 包含 '),
    (' struct and the\n', ' 枚举和\n'),
    (' trait. A token is an instruction for the ', ' trait。Token 是用于让 '),
    ('\nstruct to do something. If you want Enigo to simulate input, you then have\nto tell the enigo struct to ',
     '\n结构体执行某些操作的指令。如果希望 Enigo 模拟输入，则需要让 enigo 结构体 '),
    (' the token. Have\na look at the ', ' 该 token。如果想阅读相关代码，可以查看 '),
    (' example if you’d like to read some code to see how it\nworks.',
     ' 示例了解其工作原理。'),
    # Stabilized info (rare)
    ('1.95.0', '1.95.0'),  # keep version
]


def apply_pairs(content, pairs, label=''):
    """Apply a list of (old, new) replacements, tracking misses."""
    missed = []
    for old, new in pairs:
        if old not in content:
            missed.append(old)
        content = content.replace(old, new)
    if missed:
        for m in missed[:5]:
            print(f'  [MISS] {label}: {m[:60]!r}')
        if len(missed) > 5:
            print(f'  [MISS] {label}: ... and {len(missed)-5} more')
    return content


def translate_redirect(content):
    """For platform/win_impl/* and keycodes/* redirect stubs."""
    pairs = [
        ('<html lang="en">', '<html lang="zh-CN">'),
        ('<title>Redirection</title>', '<title>重定向</title>'),
        ('Redirecting to ', '正在重定向到 '),
        ('...', '……'),
    ]
    return apply_pairs(content, pairs, 'redirect')


def translate_all_html(content):
    """Translate the all.html file."""
    pairs = [
        ('<html lang="en">', '<html lang="zh-CN">'),
        ('<meta name="description" content="List of all items in this crate">',
         '<meta name="description" content="本 crate 中的所有项列表">'),
        ('<title>List of all items in this crate</title>',
         '<title>本 crate 中所有项的列表</title>'),
    ]
    content = apply_pairs(content, pairs, 'all meta')
    content = apply_pairs(content, COMMON_UI, 'all common ui')
    content = apply_pairs(content, COMMON_TEXT, 'all common text')
    return content


def translate_constant(content, name):
    """Translate a constant HTML file."""
    pairs = [
        ('<html lang="en">', '<html lang="zh-CN">'),
    ]
    content = apply_pairs(content, pairs, f'constant {name} lang')
    content = apply_pairs(content, COMMON_UI, f'constant {name} ui')
    content = apply_pairs(content, COMMON_TEXT, f'constant {name} text')
    # Constant-specific
    if name == 'EVENT_MARKER':
        pairs2 = [
            ('<meta name="description" content="Arbitrary value to be able to distinguish events created by enigo">',
             '<meta name="description" content="用于区分由 enigo 创建的事件的任意值">'),
            ('<title>EVENT_MARKER in enigo - Rust</title>',
             '<title>EVENT_MARKER in enigo - Rust</title>'),
            ('>EVENT_MARKER<', '>EVENT_MARKER<'),  # keep identifier
            ('Constant <span class="constant">EVENT_<wbr>MARKER</span>',
             '常量 <span class="constant">EVENT_<wbr>MARKER</span>'),
        ]
        content = apply_pairs(content, pairs2, 'EVENT_MARKER specific')
    elif name == 'EXT':
        pairs2 = [
            ('<meta name="description" content="API documentation for the Rust `EXT` constant in crate `enigo`.">',
             '<meta name="description" content="Rust crate `enigo` 中 `EXT` 常量的 API 文档。">'),
            ('<title>EXT in enigo - Rust</title>', '<title>EXT in enigo - Rust</title>'),
            ('Constant <span class="constant">EXT</span>',
             '常量 <span class="constant">EXT</span>'),
        ]
        content = apply_pairs(content, pairs2, 'EXT specific')
    return content


def translate_fn_set_dpi(content):
    pairs = [
        ('<html lang="en">', '<html lang="zh-CN">'),
        ('<meta name="description" content="Sets the current process to a specified dots per inch (dpi) awareness context see official documentation If you want your applications to respect the users scaling, you need to set this. Otherwise the mouse coordinates and screen dimensions will be off.">',
         '<meta name="description" content="将当前进程设置为指定的每英寸点数 (dpi) 感知上下文，参见官方文档。如果希望应用程序遵循用户的缩放比例，则需要设置此项。否则鼠标坐标和屏幕尺寸将不准确。">'),
        ('<title>set_dpi_awareness in enigo - Rust</title>',
         '<title>set_dpi_awareness in enigo - Rust</title>'),
        ('Function <span class="fn">set_<wbr>dpi_<wbr>awareness</span>',
         '函数 <span class="fn">set_<wbr>dpi_<wbr>awareness</span>'),
        ('>set_<wbr>dpi_<wbr>awareness<', '>set_<wbr>dpi_<wbr>awareness<'),
    ]
    content = apply_pairs(content, pairs, 'set_dpi_awareness specific')
    content = apply_pairs(content, COMMON_UI, 'set_dpi_awareness ui')
    content = apply_pairs(content, COMMON_TEXT, 'set_dpi_awareness text')
    return content


def translate_type(content):
    pairs = [
        ('<html lang="en">', '<html lang="zh-CN">'),
        ('<meta name="description" content="API documentation for the Rust `InputResult` type in crate `enigo`.">',
         '<meta name="description" content="Rust crate `enigo` 中 `InputResult` 类型别名的 API 文档。">'),
        ('<title>InputResult in enigo - Rust</title>',
         '<title>InputResult in enigo - Rust</title>'),
        ('Type Alias <span class="type">Input<wbr>Result</span>',
         '类型别名 <span class="type">Input<wbr>Result</span>'),
    ]
    content = apply_pairs(content, pairs, 'InputResult specific')
    content = apply_pairs(content, COMMON_UI, 'InputResult ui')
    content = apply_pairs(content, COMMON_TEXT, 'InputResult text')
    return content


def translate_trait(content, name):
    """Translate a trait HTML file."""
    pairs = [
        ('<html lang="en">', '<html lang="zh-CN">'),
    ]
    if name == 'Keyboard':
        pairs += [
            ('<meta name="description" content="Contains functions to simulate key presses/releases and to input text.">',
             '<meta name="description" content="包含模拟按键按下/释放和输入文本的函数。">'),
            ('<title>Keyboard in enigo - Rust</title>',
             '<title>Keyboard in enigo - Rust</title>'),
            ('Trait <span class="trait">Keyboard</span>',
             'trait <span class="trait">Keyboard</span>'),
        ]
    elif name == 'Mouse':
        pairs += [
            ('<meta name="description" content="Contains functions to control the mouse and to get the size of the display.\nEnigo uses a cartesian coordinate system for specifying coordinates. The\norigin in this system is located in the top-left corner of the current\nscreen, with positive values extending along the axes down and to the\nright of the origin point and it is measured in pixels. The same coordinate\nsystem is used on all operating systems.">',
             '<meta name="description" content="包含控制鼠标和获取显示屏尺寸的函数。Enigo 使用笛卡尔坐标系来指定坐标。该坐标系的原点位于当前屏幕的左上角，正值沿坐标轴向下和向右延伸，单位为像素。所有操作系统均使用相同的坐标系。">'),
            ('<title>Mouse in enigo - Rust</title>',
             '<title>Mouse in enigo - Rust</title>'),
            ('Trait <span class="trait">Mouse</span>',
             'trait <span class="trait">Mouse</span>'),
        ]
    content = apply_pairs(content, pairs, f'trait {name} specific')
    content = apply_pairs(content, COMMON_UI, f'trait {name} ui')
    content = apply_pairs(content, COMMON_TEXT, f'trait {name} text')
    return content


def translate_struct(content, name):
    """Translate a struct HTML file."""
    pairs = [
        ('<html lang="en">', '<html lang="zh-CN">'),
    ]
    if name == 'Enigo':
        pairs += [
            ('<meta name="description" content="The main struct for handling the event emitting">',
             '<meta name="description" content="用于处理事件发送的主结构体">'),
            ('<title>Enigo in enigo - Rust</title>',
             '<title>Enigo in enigo - Rust</title>'),
            ('Struct <span class="struct">Enigo</span>',
             '结构体 <span class="struct">Enigo</span>'),
            ('/* private fields */', '/* 私有字段 */'),
        ]
    elif name == 'Settings':
        pairs += [
            ('<meta name="description" content="Settings for creating the Enigo struct and it’s behavior">',
             '<meta name="description" content="用于创建 Enigo 结构体及其行为的设置">'),
            ('<title>Settings in enigo - Rust</title>',
             '<title>Settings in enigo - Rust</title>'),
            ('Struct <span class="struct">Settings</span>',
             '结构体 <span class="struct">Settings</span>'),
        ]
    content = apply_pairs(content, pairs, f'struct {name} specific')
    content = apply_pairs(content, COMMON_UI, f'struct {name} ui')
    content = apply_pairs(content, COMMON_TEXT, f'struct {name} text')
    return content


def translate_enum(content, name):
    """Translate an enum HTML file."""
    pairs = [
        ('<html lang="en">', '<html lang="zh-CN">'),
    ]
    title_map = {
        'Axis': ('Specifies the axis for scrolling', '指定滚动的轴'),
        'Button': ('Represents a mouse button and is used in e.g Mouse::button .',
                   '表示鼠标按键，用于例如 Mouse::button。'),
        'Coordinate': ('Specifies if a coordinate is relative or absolute',
                       '指定坐标是相对坐标还是绝对坐标'),
        'Direction': ('The direction of a key or button', '按键或按钮的方向'),
        'InputError': ('Error when simulating input', '模拟输入时的错误'),
        'Key': ('Contains the available keycodes',
                '包含所有可用的按键码'),
        'NewConError': ('Error when establishing a new connection',
                        '建立新连接时的错误'),
    }
    if name in title_map:
        old, new = title_map[name]
        pairs += [
            (f'<meta name="description" content="{old}">',
             f'<meta name="description" content="{new}">'),
            (f'<title>{name} in enigo - Rust</title>',
             f'<title>{name} in enigo - Rust</title>'),
            (f'Enum <span class="enum">{name}</span>',
             f'枚举 <span class="enum">{name}</span>'),
        ]
    content = apply_pairs(content, pairs, f'enum {name} specific')
    content = apply_pairs(content, COMMON_UI, f'enum {name} ui')
    content = apply_pairs(content, COMMON_TEXT, f'enum {name} text')
    return content


def translate_agent_trait(content):
    """Translate agent/trait.Agent.html"""
    pairs = [
        ('<html lang="en">', '<html lang="zh-CN">'),
        ('<meta name="description" content="API documentation for the Rust `Agent` trait in crate `enigo`.">',
         '<meta name="description" content="Rust crate `enigo` 中 `Agent` trait 的 API 文档。">'),
        ('<title>Agent in enigo::agent - Rust</title>',
         '<title>Agent in enigo::agent - Rust</title>'),
        ('Trait <span class="trait">Agent</span>',
         'trait <span class="trait">Agent</span>'),
    ]
    content = apply_pairs(content, pairs, 'agent trait specific')
    content = apply_pairs(content, COMMON_UI, 'agent trait ui')
    content = apply_pairs(content, COMMON_TEXT, 'agent trait text')
    return content


def translate_agent_enum_token(content):
    """Translate agent/enum.Token.html"""
    pairs = [
        ('<html lang="en">', '<html lang="zh-CN">'),
        ('<meta name="description" content="API documentation for the Rust `Token` enum in crate `enigo`.">',
         '<meta name="description" content="Rust crate `enigo` 中 `Token` 枚举的 API 文档。">'),
        ('<title>Token in enigo::agent - Rust</title>',
         '<title>Token in enigo::agent - Rust</title>'),
        ('Enum <span class="enum">Token</span>',
         '枚举 <span class="enum">Token</span>'),
    ]
    content = apply_pairs(content, pairs, 'agent enum.Token specific')
    content = apply_pairs(content, COMMON_UI, 'agent enum.Token ui')
    content = apply_pairs(content, COMMON_TEXT, 'agent enum.Token text')
    return content


def main():
    targets = [
        # Redirect stubs
        (os.path.join(ENIGO_ROOT, 'platform', 'win_impl', 'fn.set_dpi_awareness.html'), translate_redirect, 'platform/fn.set_dpi_awareness'),
        (os.path.join(ENIGO_ROOT, 'platform', 'win_impl', 'constant.EXT.html'), translate_redirect, 'platform/constant.EXT'),
        (os.path.join(ENIGO_ROOT, 'platform', 'win_impl', 'struct.Enigo.html'), translate_redirect, 'platform/struct.Enigo'),
        (os.path.join(ENIGO_ROOT, 'keycodes', 'enum.Key.html'), translate_redirect, 'keycodes/enum.Key'),
        # all.html
        (os.path.join(ENIGO_ROOT, 'all.html'), translate_all_html, 'all.html'),
        # constants
        (os.path.join(ENIGO_ROOT, 'constant.EVENT_MARKER.html'), lambda c: translate_constant(c, 'EVENT_MARKER'), 'constant.EVENT_MARKER'),
        (os.path.join(ENIGO_ROOT, 'constant.EXT.html'), lambda c: translate_constant(c, 'EXT'), 'constant.EXT'),
        # functions
        (os.path.join(ENIGO_ROOT, 'fn.set_dpi_awareness.html'), translate_fn_set_dpi, 'fn.set_dpi_awareness'),
        # type alias
        (os.path.join(ENIGO_ROOT, 'type.InputResult.html'), translate_type, 'type.InputResult'),
        # agent
        (os.path.join(ENIGO_ROOT, 'agent', 'trait.Agent.html'), translate_agent_trait, 'agent/trait.Agent'),
        (os.path.join(ENIGO_ROOT, 'agent', 'enum.Token.html'), translate_agent_enum_token, 'agent/enum.Token'),
        # traits
        (os.path.join(ENIGO_ROOT, 'trait.Keyboard.html'), lambda c: translate_trait(c, 'Keyboard'), 'trait.Keyboard'),
        (os.path.join(ENIGO_ROOT, 'trait.Mouse.html'), lambda c: translate_trait(c, 'Mouse'), 'trait.Mouse'),
        # structs
        (os.path.join(ENIGO_ROOT, 'struct.Enigo.html'), lambda c: translate_struct(c, 'Enigo'), 'struct.Enigo'),
        (os.path.join(ENIGO_ROOT, 'struct.Settings.html'), lambda c: translate_struct(c, 'Settings'), 'struct.Settings'),
        # enums
        (os.path.join(ENIGO_ROOT, 'enum.Axis.html'), lambda c: translate_enum(c, 'Axis'), 'enum.Axis'),
        (os.path.join(ENIGO_ROOT, 'enum.Button.html'), lambda c: translate_enum(c, 'Button'), 'enum.Button'),
        (os.path.join(ENIGO_ROOT, 'enum.Coordinate.html'), lambda c: translate_enum(c, 'Coordinate'), 'enum.Coordinate'),
        (os.path.join(ENIGO_ROOT, 'enum.Direction.html'), lambda c: translate_enum(c, 'Direction'), 'enum.Direction'),
        (os.path.join(ENIGO_ROOT, 'enum.InputError.html'), lambda c: translate_enum(c, 'InputError'), 'enum.InputError'),
        (os.path.join(ENIGO_ROOT, 'enum.Key.html'), lambda c: translate_enum(c, 'Key'), 'enum.Key'),
        (os.path.join(ENIGO_ROOT, 'enum.NewConError.html'), lambda c: translate_enum(c, 'NewConError'), 'enum.NewConError'),
    ]
    for path, fn, label in targets:
        print(f'--- {label} ---')
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        new_content = fn(content)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        verify(new_content, label)
        print()


if __name__ == '__main__':
    main()