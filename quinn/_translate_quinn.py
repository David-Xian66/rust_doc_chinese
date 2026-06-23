"""Master translation script for quinn rustdoc HTML.

Architecture:
- apply_common_chrome(content): applies the standard chrome translations
  (lang, skip link, IE warning, button labels, sidebar nav, trait impl
  section headers). Used by every struct/enum/trait/fn page.
- translate_file(path, *, type_kind, type_name, wbr, title, description,
  docblocks): translates one file end-to-end using common chrome + the
  file-specific title, description, H1, and docblock paragraphs.
- A function per file (e.g., translate_struct_connecting) wires the
  file-specific args into translate_file().
- main(target) takes a target name and runs exactly one translation.

Workflow per rust-doc-translation-pattern:
- Use Python open() directly (no Read tool on HTML).
- Apply (old, new) replacements; preserve HTML structure, URLs,
  Rust identifiers, and <wbr> positions.
"""

import os
import re
import sys

QUINN_ROOT = 'D:/Administrator/Documents/Code/rust_doc_all/quinn'


def verify(content, label):
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


# Common chrome used by every struct/enum/trait/fn page.
COMMON_CHROME = [
    # lang attribute
    ('<html lang="en">', '<html lang="zh-CN">'),
    # Skip link
    ('>Skip to main content<', '>跳到主要内容<'),
    # IE warning
    ('This old browser is unsupported and will most likely display funky things.',
     '此旧版浏览器不受支持，很可能会显示异常内容。'),
    # Buttons / actions
    (' title="Copy item path to clipboard"', ' title="复制项目路径到剪贴板"'),
    ('>Copy item path<', '>复制项目路径<'),
    ('>Source<', '>源代码<'),
    ('>Expand description<', '>展开描述<'),
    # Sidebar: bottom navigation
    ('>In crate quinn<', '>在 crate quinn 中<'),
    # Sidebar / body H3: trait impl sections
    ('>Trait Implementations<', '>trait 实现<'),
    ('>Auto Trait Implementations<', '>自动 trait 实现<'),
    ('>Blanket Implementations<', '>blanket 实现<'),
]


def apply_common_chrome(content, label='common'):
    """Apply the standard chrome replacements to any quinn struct/enum/trait/fn page."""
    for old, new in COMMON_CHROME:
        if old not in content:
            # Some chrome may legitimately be missing (e.g. a page without
            # a 'Source' link). Only warn so the caller can decide.
            print(f'  [INFO {label}] chrome miss (ok if expected): {old[:60]!r}')
        content = content.replace(old, new)
    return content


# Mapping of English section kind → Chinese, used in H1.
H1_KIND = {
    'Struct': '结构体',
    'Enum': '枚举',
    'Trait': 'trait',
    'Function': '函数',
    'Type': '类型',
    'Constant': '常量',
    'Macro': '宏',
    'Module': '模块',
    'Crate': 'crate',
}


def build_h1(kind, class_name, type_name, wbr_pos=None):
    """Build the H1 line for a struct/enum/trait/etc. page.

    kind: the displayed kind word, e.g. 'Struct' (English) or '结构体' (Chinese).
    class_name: the span class name (always English lowercase, e.g. 'struct').
    type_name: the displayed name, e.g. 'ZeroRttAccepted'.
    wbr_pos: optional list of split points (after-char indices) where <wbr>
        should be inserted, e.g. [4] for 'ZeroRttAccepted' -> 'Zero<wbr>RttAccepted'.

    Returns a string like '<h1>Struct <span class="struct">ZeroRttAccepted</span>'.
    """
    name_with_wbr = type_name
    if wbr_pos:
        # Insert <wbr> at each split point, from right to left so positions don't shift.
        chars = list(type_name)
        for pos in sorted(wbr_pos, reverse=True):
            chars.insert(pos, '<wbr>')
        name_with_wbr = ''.join(chars)
    return f'<h1>{kind} <span class="{class_name}">{name_with_wbr}</span>'


def translate_file(rel_path, *, type_kind, type_name, wbr_pos=None,
                  title_in_english, title_in_chinese,
                  description_old, description_new,
                  docblocks=None, h1_old=None, h1_new=None,
                  extra_replacements=None, label=None):
    """Translate one quinn HTML file.

    Args:
        rel_path: path relative to QUINN_ROOT.
        type_kind: 'Struct' | 'Enum' | 'Trait' | 'Function' | ...
        type_name: the bare type name (no <wbr>), e.g. 'ZeroRttAccepted'.
        wbr_pos: optional list of split indices for <wbr> insertion.
        title_in_english: the original <title>...</title> text (English).
        title_in_chinese: the replacement <title>...</title> text.
        description_old: the original meta description attribute value.
        description_new: the replacement.
        docblocks: list of (old_html, new_html) for docblock paragraphs.
        h1_old, h1_new: optional override for the H1 line. If omitted,
            build_h1 is used with type_kind/type_name/wbr_pos.
        extra_replacements: list of additional (old, new) pairs to apply
            before docblocks (e.g., for sidebar items specific to this file).
        label: optional label for logging.
    """
    path = os.path.join(QUINN_ROOT, rel_path)
    label = label or rel_path
    print(f'--- {rel_path} ---')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Common chrome
    content = apply_common_chrome(content, label=label)

    # 2. Extra file-specific replacements (apply BEFORE docblocks since
    #    some of them may overlap with longer strings).
    if extra_replacements:
        for old, new in extra_replacements:
            if old not in content:
                print(f'  [MISS {label}] extra: {old[:60]!r}')
            content = content.replace(old, new)

    # 3. Title
    title_old = f'<title>{title_in_english}</title>'
    title_new = f'<title>{title_in_chinese}</title>'
    if title_old not in content:
        print(f'  [MISS {label}] title: {title_in_english!r}')
    content = content.replace(title_old, title_new)

    # 4. Meta description (exact attribute match)
    desc_old_tag = f'<meta name="description" content="{description_old}">'
    desc_new_tag = f'<meta name="description" content="{description_new}">'
    if desc_old_tag not in content:
        print(f'  [MISS {label}] description: {description_old[:60]!r}')
    content = content.replace(desc_old_tag, desc_new_tag)

    # 5. H1
    if h1_old is None:
        h1_old = build_h1(type_kind, type_kind.lower(), type_name, wbr_pos)
    if h1_new is None:
        # Replace only the kind word, keep the <span class="...">...</span> intact.
        # The original H1 is e.g. 'Struct <span class="struct">ZeroRttAccepted</span>'.
        # We want '结构体 <span class="struct">ZeroRttAccepted</span>'.
        h1_new = build_h1(H1_KIND.get(type_kind, type_kind), type_kind.lower(),
                          type_name, wbr_pos)
    if h1_old not in content:
        print(f'  [MISS {label}] h1: {h1_old[:80]!r}')
    content = content.replace(h1_old, h1_new)

    # 6. Docblocks
    if docblocks:
        for old, new in docblocks:
            if old not in content:
                print(f'  [MISS {label}] docblock: {old[:60]!r}')
            content = content.replace(old, new)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    verify(content, label)
    return content


# ----------------------------------------------------------------------
# Per-file functions. Each one calls translate_file() with the right args.
# Add new ones as you progress through the crate.
# ----------------------------------------------------------------------


def translate_struct_connecting():
    """struct.Connecting - In-progress connection attempt future."""
    return translate_file(
        'struct.Connecting.html',
        type_kind='Struct',
        type_name='Connecting',
        title_in_english='Connecting in quinn - Rust',
        title_in_chinese='quinn 中的 Connecting - Rust',
        description_old='In-progress connection attempt future',
        description_new='正在进行的连接尝试的 Future',
        docblocks=[(
            '<p>In-progress connection attempt future</p>',
            '<p>正在进行的连接尝试的 Future</p>',
        )],
    )


def translate_enum_config_error():
    """enum.ConfigError - Errors in the configuration of an endpoint."""
    return translate_file(
        'enum.ConfigError.html',
        type_kind='Enum',
        type_name='ConfigError',
        wbr_pos=[6],
        title_in_english='ConfigError in quinn - Rust',
        title_in_chinese='quinn 中的 ConfigError - Rust',
        description_old='Errors in the configuration of an endpoint',
        description_new='端点配置中的错误',
        docblocks=[(
            '<p>Errors in the configuration of an endpoint</p>',
            '<p>端点配置中的错误</p>',
        )],
    )


def translate_enum_connect_error():
    return translate_file(
        'enum.ConnectError.html',
        type_kind='Enum',
        type_name='ConnectError',
        wbr_pos=[7],
        title_in_english='ConnectError in quinn - Rust',
        title_in_chinese='quinn 中的 ConnectError - Rust',
        description_old='Errors in the parameters being used to create a new connection',
        description_new='用于创建新连接的参数中的错误',
        docblocks=[(
            '<p>Errors in the parameters being used to create a new connection</p>',
            '<p>用于创建新连接的参数中的错误</p>',
        )],
    )


def translate_enum_connection_error():
    return translate_file(
        'enum.ConnectionError.html',
        type_kind='Enum',
        type_name='ConnectionError',
        wbr_pos=[10],
        title_in_english='ConnectionError in quinn - Rust',
        title_in_chinese='quinn 中的 ConnectionError - Rust',
        description_old='Reasons why a connection might be lost',
        description_new='连接可能丢失的原因',
        docblocks=[(
            '<p>Reasons why a connection might be lost</p>',
            '<p>连接可能丢失的原因</p>',
        )],
    )


def translate_enum_dir():
    return translate_file(
        'enum.Dir.html',
        type_kind='Enum',
        type_name='Dir',
        title_in_english='Dir in quinn - Rust',
        title_in_chinese='quinn 中的 Dir - Rust',
        description_old='Whether a stream communicates data in both directions or only from the initiator',
        description_new='流是双向通信还是仅由发起方单向通信',
        docblocks=[(
            '<p>Whether a stream communicates data in both directions or only from the initiator</p>',
            '<p>流是双向通信还是仅由发起方单向通信</p>',
        )],
    )


def translate_enum_ecn_codepoint():
    return translate_file(
        'enum.EcnCodepoint.html',
        type_kind='Enum',
        type_name='EcnCodepoint',
        title_in_english='EcnCodepoint in quinn - Rust',
        title_in_chinese='quinn 中的 EcnCodepoint - Rust',
        description_old='Explicit congestion notification codepoint',
        description_new='显式拥塞通知 (ECN) 码点',
        docblocks=[(
            '<p>Explicit congestion notification codepoint</p>',
            '<p>显式拥塞通知 (ECN) 码点</p>',
        )],
    )


def translate_enum_read_error():
    return translate_file(
        'enum.ReadError.html',
        type_kind='Enum',
        type_name='ReadError',
        wbr_pos=[4],
        title_in_english='ReadError in quinn - Rust',
        title_in_chinese='quinn 中的 ReadError - Rust',
        description_old='Errors that arise from reading from a stream.',
        description_new='从流读取时产生的错误。',
        docblocks=[(
            '<p>Errors that arise from reading from a stream.</p>',
            '<p>从流读取时产生的错误。</p>',
        )],
    )


def translate_enum_read_exact_error():
    return translate_file(
        'enum.ReadExactError.html',
        type_kind='Enum',
        type_name='ReadExactError',
        wbr_pos=[4, 9],
        title_in_english='ReadExactError in quinn - Rust',
        title_in_chinese='quinn 中的 ReadExactError - Rust',
        description_old='Errors that arise from reading from a stream.',
        description_new='从流读取时产生的错误。',
        docblocks=[(
            '<p>Errors that arise from reading from a stream.</p>',
            '<p>从流读取时产生的错误。</p>',
        )],
    )


def translate_enum_read_to_end_error():
    return translate_file(
        'enum.ReadToEndError.html',
        type_kind='Enum',
        type_name='ReadToEndError',
        wbr_pos=[4, 9],
        title_in_english='ReadToEndError in quinn - Rust',
        title_in_chinese='quinn 中的 ReadToEndError - Rust',
        description_old='Errors from `RecvStream::read_to_end`',
        description_new='由 `RecvStream::read_to_end` 产生的错误',
        docblocks=[(
            '<p>Errors from <a href="struct.RecvStream.html#method.read_to_end" title="method quinn::RecvStream::read_to_end"><code>RecvStream::read_to_end</code></a></p>',
            '<p>由 <a href="struct.RecvStream.html#method.read_to_end" title="method quinn::RecvStream::read_to_end"><code>RecvStream::read_to_end</code></a> 产生的错误</p>',
        )],
    )


def translate_enum_reset_error():
    return translate_file(
        'enum.ResetError.html',
        type_kind='Enum',
        type_name='ResetError',
        wbr_pos=[5],
        title_in_english='ResetError in quinn - Rust',
        title_in_chinese='quinn 中的 ResetError - Rust',
        description_old='Errors that arise while waiting for a stream to be reset',
        description_new='在等待流被重置时产生的错误',
        docblocks=[(
            '<p>Errors that arise while waiting for a stream to be reset</p>',
            '<p>在等待流被重置时产生的错误</p>',
        )],
    )


def translate_enum_send_datagram_error():
    return translate_file(
        'enum.SendDatagramError.html',
        type_kind='Enum',
        type_name='SendDatagramError',
        wbr_pos=[4, 12],
        title_in_english='SendDatagramError in quinn - Rust',
        title_in_chinese='quinn 中的 SendDatagramError - Rust',
        description_old='Errors that can arise when sending a datagram',
        description_new='发送数据报时可能产生的错误',
        docblocks=[(
            '<p>Errors that can arise when sending a datagram</p>',
            '<p>发送数据报时可能产生的错误</p>',
        )],
    )


def translate_enum_side():
    return translate_file(
        'enum.Side.html',
        type_kind='Enum',
        type_name='Side',
        title_in_english='Side in quinn - Rust',
        title_in_chinese='quinn 中的 Side - Rust',
        description_old='Whether an endpoint was the initiator of a connection',
        description_new='端点是连接的发起方还是接收方',
        docblocks=[(
            '<p>Whether an endpoint was the initiator of a connection</p>',
            '<p>端点是连接的发起方还是接收方</p>',
        )],
    )


def translate_enum_stopped_error():
    return translate_file(
        'enum.StoppedError.html',
        type_kind='Enum',
        type_name='StoppedError',
        wbr_pos=[7],
        title_in_english='StoppedError in quinn - Rust',
        title_in_chinese='quinn 中的 StoppedError - Rust',
        description_old='Errors that arise while monitoring for a send stream stop from the peer',
        description_new='在监视对端停止发送流时产生的错误',
        docblocks=[(
            '<p>Errors that arise while monitoring for a send stream stop from the peer</p>',
            '<p>在监视对端停止发送流时产生的错误</p>',
        )],
    )


def translate_enum_write_error():
    return translate_file(
        'enum.WriteError.html',
        type_kind='Enum',
        type_name='WriteError',
        wbr_pos=[5],
        title_in_english='WriteError in quinn - Rust',
        title_in_chinese='quinn 中的 WriteError - Rust',
        description_old='Errors that arise from writing to a stream',
        description_new='向流写入时产生的错误',
        docblocks=[(
            '<p>Errors that arise from writing to a stream</p>',
            '<p>向流写入时产生的错误</p>',
        )],
    )


def translate_trait_async_timer():
    return translate_file(
        'trait.AsyncTimer.html',
        type_kind='Trait',
        type_name='AsyncTimer',
        wbr_pos=[5],
        title_in_english='AsyncTimer in quinn - Rust',
        title_in_chinese='quinn 中的 AsyncTimer - Rust',
        description_old='Abstract implementation of an async timer for runtime independence',
        description_new='异步定时器的抽象实现，用于运行时无关性',
        docblocks=[(
            '<p>Abstract implementation of an async timer for runtime independence</p>',
            '<p>异步定时器的抽象实现，用于运行时无关性</p>',
        )],
    )


def translate_trait_async_udp_socket():
    return translate_file(
        'trait.AsyncUdpSocket.html',
        type_kind='Trait',
        type_name='AsyncUdpSocket',
        wbr_pos=[5],
        title_in_english='AsyncUdpSocket in quinn - Rust',
        title_in_chinese='quinn 中的 AsyncUdpSocket - Rust',
        description_old='Abstract implementation of a UDP socket for runtime independence',
        description_new='UDP 套接字的抽象实现，用于运行时无关性',
        docblocks=[(
            '<p>Abstract implementation of a UDP socket for runtime independence</p>',
            '<p>UDP 套接字的抽象实现，用于运行时无关性</p>',
        )],
    )


def translate_trait_connection_id_generator():
    return translate_file(
        'trait.ConnectionIdGenerator.html',
        type_kind='Trait',
        type_name='ConnectionIdGenerator',
        wbr_pos=[10],
        title_in_english='ConnectionIdGenerator in quinn - Rust',
        title_in_chinese='quinn 中的 ConnectionIdGenerator - Rust',
        description_old='Generates connection IDs for incoming connections',
        description_new='为入站连接生成连接 ID',
        docblocks=[(
            '<p>Generates connection IDs for incoming connections</p>',
            '<p>为入站连接生成连接 ID</p>',
        )],
    )


def translate_trait_runtime():
    return translate_file(
        'trait.Runtime.html',
        type_kind='Trait',
        type_name='Runtime',
        title_in_english='Runtime in quinn - Rust',
        title_in_chinese='quinn 中的 Runtime - Rust',
        description_old='Abstracts I/O and timer operations for runtime independence',
        description_new='对 I/O 与定时器操作的抽象，用于运行时无关性',
        docblocks=[(
            '<p>Abstracts I/O and timer operations for runtime independence</p>',
            '<p>对 I/O 与定时器操作的抽象，用于运行时无关性</p>',
        )],
    )


def translate_trait_time_source():
    return translate_file(
        'trait.TimeSource.html',
        type_kind='Trait',
        type_name='TimeSource',
        wbr_pos=[4],
        title_in_english='TimeSource in quinn - Rust',
        title_in_chinese='quinn 中的 TimeSource - Rust',
        description_old='Object to get current `SystemTime`',
        description_new='用于获取当前 `SystemTime` 的对象',
        docblocks=[(
            '<p>Object to get current <a href="https://doc.rust-lang.org/1.95.0/std/time/struct.SystemTime.html" title="struct std::time::SystemTime"><code>SystemTime</code></a></p>',
            '<p>用于获取当前 <a href="https://doc.rust-lang.org/1.95.0/std/time/struct.SystemTime.html" title="struct std::time::SystemTime"><code>SystemTime</code></a> 的对象</p>',
        )],
    )


def translate_trait_token_log():
    return translate_file(
        'trait.TokenLog.html',
        type_kind='Trait',
        type_name='TokenLog',
        wbr_pos=[5],
        title_in_english='TokenLog in quinn - Rust',
        title_in_chinese='quinn 中的 TokenLog - Rust',
        description_old='Responsible for limiting clients’ ability to reuse validation tokens',
        description_new='负责限制客户端复用校验 token 的能力',
        docblocks=[(
            '<p>Responsible for limiting clients’ ability to reuse validation tokens</p>',
            '<p>负责限制客户端复用校验 token 的能力</p>',
        )],
    )


def translate_trait_token_store():
    return translate_file(
        'trait.TokenStore.html',
        type_kind='Trait',
        type_name='TokenStore',
        wbr_pos=[5],
        title_in_english='TokenStore in quinn - Rust',
        title_in_chinese='quinn 中的 TokenStore - Rust',
        description_old='Responsible for storing validation tokens received from servers and retrieving them for use in\nsubsequent connections',
        description_new='负责存储从服务器接收到的校验 token，并在后续连接中取出使用',
        docblocks=[(
            '<p>Responsible for storing validation tokens received from servers and retrieving them for use in\nsubsequent connections</p>',
            '<p>负责存储从服务器接收到的校验 token，并在后续连接中取出使用</p>',
        )],
    )


def translate_trait_udp_poller():
    return translate_file(
        'trait.UdpPoller.html',
        type_kind='Trait',
        type_name='UdpPoller',
        title_in_english='UdpPoller in quinn - Rust',
        title_in_chinese='quinn 中的 UdpPoller - Rust',
        description_old='An object polled to detect when an associated `AsyncUdpSocket` is writable',
        description_new='通过轮询检测关联的 `AsyncUdpSocket` 是否可写',
        docblocks=[(
            '<p>An object polled to detect when an associated <a href="trait.AsyncUdpSocket.html" title="trait quinn::AsyncUdpSocket"><code>AsyncUdpSocket</code></a> is writable</p>',
            '<p>通过轮询检测关联的 <a href="trait.AsyncUdpSocket.html" title="trait quinn::AsyncUdpSocket"><code>AsyncUdpSocket</code></a> 是否可写</p>',
        )],
    )


# ----------------------------------------------------------------------
# Simple struct pages (single-paragraph top docblock).
# ----------------------------------------------------------------------

def translate_struct_accept_uni():
    return translate_file(
        'struct.AcceptUni.html',
        type_kind='Struct',
        type_name='AcceptUni',
        wbr_pos=[6],
        title_in_english='AcceptUni in quinn - Rust',
        title_in_chinese='quinn 中的 AcceptUni - Rust',
        description_old='Future produced by `Connection::accept_uni`',
        description_new='由 `Connection::accept_uni` 产生的 Future',
        docblocks=[(
            '<p>Future produced by <a href="struct.Connection.html#method.accept_uni" title="method quinn::Connection::accept_uni"><code>Connection::accept_uni</code></a></p>',
            '<p>由 <a href="struct.Connection.html#method.accept_uni" title="method quinn::Connection::accept_uni"><code>Connection::accept_uni</code></a> 产生的 Future</p>',
        )],
    )


def translate_struct_application_close():
    return translate_file(
        'struct.ApplicationClose.html',
        type_kind='Struct',
        type_name='ApplicationClose',
        wbr_pos=[11],
        title_in_english='ApplicationClose in quinn - Rust',
        title_in_chinese='quinn 中的 ApplicationClose - Rust',
        description_old='Reason given by an application for closing the connection',
        description_new='应用层给出的关闭连接的原因',
        docblocks=[(
            '<p>Reason given by an application for closing the connection</p>',
            '<p>应用层给出的关闭连接的原因</p>',
        )],
    )


def translate_struct_chunk():
    return translate_file(
        'struct.Chunk.html',
        type_kind='Struct',
        type_name='Chunk',
        title_in_english='Chunk in quinn - Rust',
        title_in_chinese='quinn 中的 Chunk - Rust',
        description_old='A chunk of data from the receive stream',
        description_new='来自接收流的一块数据',
        docblocks=[(
            '<p>A chunk of data from the receive stream</p>',
            '<p>来自接收流的一块数据</p>',
        )],
    )


def translate_struct_closed_stream():
    return translate_file(
        'struct.ClosedStream.html',
        type_kind='Struct',
        type_name='ClosedStream',
        wbr_pos=[6],
        title_in_english='ClosedStream in quinn - Rust',
        title_in_chinese='quinn 中的 ClosedStream - Rust',
        description_old='Error indicating that a stream has not been opened or has already been finished or reset',
        description_new='表示流尚未打开或已经结束 / 重置的错误',
        docblocks=[(
            '<p>Error indicating that a stream has not been opened or has already been finished or reset</p>',
            '<p>表示流尚未打开或已经结束 / 重置的错误</p>',
        )],
    )


def translate_struct_connection_close():
    return translate_file(
        'struct.ConnectionClose.html',
        type_kind='Struct',
        type_name='ConnectionClose',
        wbr_pos=[10],
        title_in_english='ConnectionClose in quinn - Rust',
        title_in_chinese='quinn 中的 ConnectionClose - Rust',
        description_old='Reason given by the transport for closing the connection',
        description_new='传输层给出的关闭连接的原因',
        docblocks=[(
            '<p>Reason given by the transport for closing the connection</p>',
            '<p>传输层给出的关闭连接的原因</p>',
        )],
    )


def translate_struct_connection_stats():
    return translate_file(
        'struct.ConnectionStats.html',
        type_kind='Struct',
        type_name='ConnectionStats',
        wbr_pos=[10],
        title_in_english='ConnectionStats in quinn - Rust',
        title_in_chinese='quinn 中的 ConnectionStats - Rust',
        description_old='Connection statistics',
        description_new='连接统计信息',
        docblocks=[(
            '<p>Connection statistics</p>',
            '<p>连接统计信息</p>',
        )],
    )


def translate_struct_frame_stats():
    return translate_file(
        'struct.FrameStats.html',
        type_kind='Struct',
        type_name='FrameStats',
        wbr_pos=[5],
        title_in_english='FrameStats in quinn - Rust',
        title_in_chinese='quinn 中的 FrameStats - Rust',
        description_old='Number of frames transmitted or received of each frame type',
        description_new='每种帧类型已发送或已接收的数量',
        docblocks=[(
            '<p>Number of frames transmitted or received of each frame type</p>',
            '<p>每种帧类型已发送或已接收的数量</p>',
        )],
    )


def translate_struct_frame_type():
    return translate_file(
        'struct.FrameType.html',
        type_kind='Struct',
        type_name='FrameType',
        wbr_pos=[5],
        title_in_english='FrameType in quinn - Rust',
        title_in_chinese='quinn 中的 FrameType - Rust',
        description_old='A QUIC frame type',
        description_new='QUIC 帧类型',
        docblocks=[(
            '<p>A QUIC frame type</p>',
            '<p>QUIC 帧类型</p>',
        )],
    )


def translate_struct_incoming():
    return translate_file(
        'struct.Incoming.html',
        type_kind='Struct',
        type_name='Incoming',
        title_in_english='Incoming in quinn - Rust',
        title_in_chinese='quinn 中的 Incoming - Rust',
        description_old='An incoming connection for which the server has not yet begun its part of the handshake',
        description_new='一个尚未由服务器开始其握手部分的入站连接',
        docblocks=[(
            '<p>An incoming connection for which the server has not yet begun its part of the handshake</p>',
            '<p>一个尚未由服务器开始其握手部分的入站连接</p>',
        )],
    )


def translate_struct_incoming_future():
    return translate_file(
        'struct.IncomingFuture.html',
        type_kind='Struct',
        type_name='IncomingFuture',
        wbr_pos=[8],
        title_in_english='IncomingFuture in quinn - Rust',
        title_in_chinese='quinn 中的 IncomingFuture - Rust',
        description_old='Basic adapter to let `Incoming` be `await`-ed like a `Connecting`',
        description_new='一个基础适配器，让 `Incoming` 能够像 `Connecting` 一样被 `await`',
        docblocks=[(
            '<p>Basic adapter to let <a href="struct.Incoming.html" title="struct quinn::Incoming"><code>Incoming</code></a> be <code>await</code>-ed like a <a href="struct.Connecting.html" title="struct quinn::Connecting"><code>Connecting</code></a></p>',
            '<p>一个基础适配器，让 <a href="struct.Incoming.html" title="struct quinn::Incoming"><code>Incoming</code></a> 能够像 <a href="struct.Connecting.html" title="struct quinn::Connecting"><code>Connecting</code></a> 一样被 <code>await</code></p>',
        )],
    )


def translate_struct_none_token_log():
    return translate_file(
        'struct.NoneTokenLog.html',
        type_kind='Struct',
        type_name='NoneTokenLog',
        wbr_pos=[4, 9],
        title_in_english='NoneTokenLog in quinn - Rust',
        title_in_chinese='quinn 中的 NoneTokenLog - Rust',
        description_old='Null implementation of `TokenLog`, which never accepts tokens',
        description_new='`TokenLog` 的空实现，从不接受任何 token',
        docblocks=[(
            '<p>Null implementation of <a href="trait.TokenLog.html" title="trait quinn::TokenLog"><code>TokenLog</code></a>, which never accepts tokens</p>',
            '<p><a href="trait.TokenLog.html" title="trait quinn::TokenLog"><code>TokenLog</code></a> 的空实现，从不接受任何 token</p>',
        )],
    )


def translate_struct_none_token_store():
    return translate_file(
        'struct.NoneTokenStore.html',
        type_kind='Struct',
        type_name='NoneTokenStore',
        wbr_pos=[4, 9],
        title_in_english='NoneTokenStore in quinn - Rust',
        title_in_chinese='quinn 中的 NoneTokenStore - Rust',
        description_old='Null implementation of `TokenStore`, which does not store any tokens',
        description_new='`TokenStore` 的空实现，不存储任何 token',
        docblocks=[(
            '<p>Null implementation of <a href="trait.TokenStore.html" title="trait quinn::TokenStore"><code>TokenStore</code></a>, which does not store any tokens</p>',
            '<p><a href="trait.TokenStore.html" title="trait quinn::TokenStore"><code>TokenStore</code></a> 的空实现，不存储任何 token</p>',
        )],
    )


def translate_struct_path_stats():
    return translate_file(
        'struct.PathStats.html',
        type_kind='Struct',
        type_name='PathStats',
        wbr_pos=[4],
        title_in_english='PathStats in quinn - Rust',
        title_in_chinese='quinn 中的 PathStats - Rust',
        description_old='Statistics related to a transmission path',
        description_new='与某条传输路径相关的统计信息',
        docblocks=[(
            '<p>Statistics related to a transmission path</p>',
            '<p>与某条传输路径相关的统计信息</p>',
        )],
    )


def translate_struct_retry_error():
    return translate_file(
        'struct.RetryError.html',
        type_kind='Struct',
        type_name='RetryError',
        wbr_pos=[5],
        title_in_english='RetryError in quinn - Rust',
        title_in_chinese='quinn 中的 RetryError - Rust',
        description_old='Error for attempting to retry an `Incoming` which already bears a token from a previous retry',
        description_new='尝试重试一个 `Incoming` 时产生的错误，因为它已带有一个先前重试留下的 token',
        docblocks=[(
            '<p>Error for attempting to retry an <a href="struct.Incoming.html" title="struct quinn::Incoming"><code>Incoming</code></a> which already bears a token from a previous retry</p>',
            '<p>尝试重试一个 <a href="struct.Incoming.html" title="struct quinn::Incoming"><code>Incoming</code></a> 时产生的错误，因为它已带有一个先前重试留下的 token</p>',
        )],
    )


def translate_struct_stream_id():
    return translate_file(
        'struct.StreamId.html',
        type_kind='Struct',
        type_name='StreamId',
        wbr_pos=[5],
        title_in_english='StreamId in quinn - Rust',
        title_in_chinese='quinn 中的 StreamId - Rust',
        description_old='Identifier for a stream within a particular connection',
        description_new='特定连接中某条流的标识符',
        docblocks=[(
            '<p>Identifier for a stream within a particular connection</p>',
            '<p>特定连接中某条流的标识符</p>',
        )],
    )


def translate_struct_token_reuse_error():
    return translate_file(
        'struct.TokenReuseError.html',
        type_kind='Struct',
        type_name='TokenReuseError',
        wbr_pos=[5, 10],
        title_in_english='TokenReuseError in quinn - Rust',
        title_in_chinese='quinn 中的 TokenReuseError - Rust',
        description_old='Error for when a validation token may have been reused',
        description_new='校验 token 疑似被复用时产生的错误',
        docblocks=[(
            '<p>Error for when a validation token may have been reused</p>',
            '<p>校验 token 疑似被复用时产生的错误</p>',
        )],
    )


def translate_struct_tokio_runtime():
    return translate_file(
        'struct.TokioRuntime.html',
        type_kind='Struct',
        type_name='TokioRuntime',
        wbr_pos=[5],
        title_in_english='TokioRuntime in quinn - Rust',
        title_in_chinese='quinn 中的 TokioRuntime - Rust',
        description_old='A Quinn runtime for Tokio',
        description_new='用于 Tokio 的 Quinn 运行时',
        docblocks=[(
            '<p>A Quinn runtime for Tokio</p>',
            '<p>用于 Tokio 的 Quinn 运行时</p>',
        )],
    )


def translate_struct_transmit():
    return translate_file(
        'struct.Transmit.html',
        type_kind='Struct',
        type_name='Transmit',
        title_in_english='Transmit in quinn - Rust',
        title_in_chinese='quinn 中的 Transmit - Rust',
        description_old='An outgoing packet',
        description_new='一个出站数据包',
        docblocks=[(
            '<p>An outgoing packet</p>',
            '<p>一个出站数据包</p>',
        )],
    )


def translate_struct_transport_error_code():
    return translate_file(
        'struct.TransportErrorCode.html',
        type_kind='Struct',
        type_name='TransportErrorCode',
        wbr_pos=[8, 13],
        title_in_english='TransportErrorCode in quinn - Rust',
        title_in_chinese='quinn 中的 TransportErrorCode - Rust',
        description_old='Transport-level error code',
        description_new='传输层错误码',
        docblocks=[(
            '<p>Transport-level error code</p>',
            '<p>传输层错误码</p>',
        )],
    )


def translate_struct_var_int():
    return translate_file(
        'struct.VarInt.html',
        type_kind='Struct',
        type_name='VarInt',
        title_in_english='VarInt in quinn - Rust',
        title_in_chinese='quinn 中的 VarInt - Rust',
        description_old='An integer less than 2^62',
        description_new='一个小于 2^62 的整数',
        docblocks=[(
            '<p>An integer less than 2^62</p>',
            '<p>一个小于 2^62 的整数</p>',
        )],
    )


def translate_struct_var_int_bounds_exceeded():
    return translate_file(
        'struct.VarIntBoundsExceeded.html',
        type_kind='Struct',
        type_name='VarIntBoundsExceeded',
        wbr_pos=[6, 12],
        title_in_english='VarIntBoundsExceeded in quinn - Rust',
        title_in_chinese='quinn 中的 VarIntBoundsExceeded - Rust',
        description_old='Error returned when constructing a `VarInt` from a value &gt;= 2^62',
        description_new='当使用大于等于 2^62 的值构造 `VarInt` 时返回的错误',
        docblocks=[(
            '<p>Error returned when constructing a <code>VarInt</code> from a value &gt;= 2^62</p>',
            '<p>当使用大于等于 2^62 的值构造 <code>VarInt</code> 时返回的错误</p>',
        )],
    )


def translate_struct_written():
    return translate_file(
        'struct.Written.html',
        type_kind='Struct',
        type_name='Written',
        title_in_english='Written in quinn - Rust',
        title_in_chinese='quinn 中的 Written - Rust',
        description_old='Indicates how many bytes and chunks had been transferred in a write operation',
        description_new='指示一次写入操作中已传输的字节数和块数',
        docblocks=[(
            '<p>Indicates how many bytes and chunks had been transferred in a write operation</p>',
            '<p>指示一次写入操作中已传输的字节数和块数</p>',
        )],
    )


def translate_struct_endpoint_stats():
    return translate_file(
        'struct.EndpointStats.html',
        type_kind='Struct',
        type_name='EndpointStats',
        wbr_pos=[8],
        title_in_english='EndpointStats in quinn - Rust',
        title_in_chinese='quinn 中的 EndpointStats - Rust',
        description_old='Statistics on `Endpoint` activity',
        description_new='关于 `Endpoint` 活动的统计信息',
        docblocks=[(
            '<p>Statistics on <a href="struct.Endpoint.html" title="struct quinn::Endpoint">Endpoint</a> activity</p>',
            '<p>关于 <a href="struct.Endpoint.html" title="struct quinn::Endpoint">Endpoint</a> 活动的统计信息</p>',
        )],
    )


def translate_struct_token_memory_cache():
    return translate_file(
        'struct.TokenMemoryCache.html',
        type_kind='Struct',
        type_name='TokenMemoryCache',
        wbr_pos=[5, 11],
        title_in_english='TokenMemoryCache in quinn - Rust',
        title_in_chinese='quinn 中的 TokenMemoryCache - Rust',
        description_old='`TokenStore` implementation that stores up to `N` tokens per server name for up to a limited number of server names, in-memory',
        description_new='`TokenStore` 的一个实现：在内存中为有限数量的服务器名称各存储最多 `N` 个 token',
        docblocks=[(
            '<p><code>TokenStore</code> implementation that stores up to <code>N</code> tokens per server name for up to a\nlimited number of server names, in-memory</p>',
            '<p><code>TokenStore</code> 的一个实现：在内存中为有限数量的服务器名称各存储最多 <code>N</code> 个 token</p>',
        )],
    )


def translate_struct_client_config():
    return translate_file(
        'struct.ClientConfig.html',
        type_kind='Struct',
        type_name='ClientConfig',
        wbr_pos=[6],
        title_in_english='ClientConfig in quinn - Rust',
        title_in_chinese='quinn 中的 ClientConfig - Rust',
        description_old='Configuration for outgoing connections',
        description_new='出站连接的配置',
        docblocks=[(
            '<p>Configuration for outgoing connections</p>\n<p>Default values should be suitable for most internet applications.</p>',
            '<p>出站连接的配置</p>\n<p>默认值应该适合大多数互联网应用。</p>',
        )],
    )


def translate_struct_endpoint_config():
    return translate_file(
        'struct.EndpointConfig.html',
        type_kind='Struct',
        type_name='EndpointConfig',
        wbr_pos=[8],
        title_in_english='EndpointConfig in quinn - Rust',
        title_in_chinese='quinn 中的 EndpointConfig - Rust',
        description_old='Global configuration for the endpoint, affecting all connections',
        description_new='端点的全局配置，会影响所有连接',
        docblocks=[(
            '<p>Global configuration for the endpoint, affecting all connections</p>\n<p>Default values should be suitable for most internet applications.</p>',
            '<p>端点的全局配置，会影响所有连接</p>\n<p>默认值应该适合大多数互联网应用。</p>',
        )],
    )


def translate_struct_server_config():
    return translate_file(
        'struct.ServerConfig.html',
        type_kind='Struct',
        type_name='ServerConfig',
        wbr_pos=[6],
        title_in_english='ServerConfig in quinn - Rust',
        title_in_chinese='quinn 中的 ServerConfig - Rust',
        description_old='Parameters governing incoming connections',
        description_new='控制入站连接的参数',
        docblocks=[(
            '<p>Parameters governing incoming connections</p>\n<p>Default values should be suitable for most internet applications.</p>',
            '<p>控制入站连接的参数</p>\n<p>默认值应该适合大多数互联网应用。</p>',
        )],
    )


def translate_struct_std_system_time():
    return translate_file(
        'struct.StdSystemTime.html',
        type_kind='Struct',
        type_name='StdSystemTime',
        wbr_pos=[3, 9],
        title_in_english='StdSystemTime in quinn - Rust',
        title_in_chinese='quinn 中的 StdSystemTime - Rust',
        description_old='Default implementation of `TimeSource`',
        description_new='`TimeSource` 的默认实现',
        docblocks=[(
            '<p>Default implementation of <a href="trait.TimeSource.html" title="trait quinn::TimeSource"><code>TimeSource</code></a></p>\n<p>Implements <code>now</code> by calling <a href="https://doc.rust-lang.org/1.95.0/std/time/struct.SystemTime.html#method.now" title="associated function std::time::SystemTime::now"><code>SystemTime::now()</code></a>.</p>',
            '<p><a href="trait.TimeSource.html" title="trait quinn::TimeSource"><code>TimeSource</code></a> 的默认实现</p>\n<p>通过调用 <a href="https://doc.rust-lang.org/1.95.0/std/time/struct.SystemTime.html#method.now" title="associated function std::time::SystemTime::now"><code>SystemTime::now()</code></a> 来实现 <code>now</code>。</p>',
        )],
    )


def translate_struct_udp_stats():
    return translate_file(
        'struct.UdpStats.html',
        type_kind='Struct',
        type_name='UdpStats',
        title_in_english='UdpStats in quinn - Rust',
        title_in_chinese='quinn 中的 UdpStats - Rust',
        description_old='Statistics about UDP datagrams transmitted or received on a connection',
        description_new='连接上已发送或已接收的 UDP 数据报统计信息',
        docblocks=[(
            '<p>Statistics about UDP datagrams transmitted or received on a connection</p>\n<p>All QUIC packets are carried by UDP datagrams. Hence, these statistics cover all traffic on a connection.</p>',
            '<p>连接上已发送或已接收的 UDP 数据报统计信息</p>\n<p>所有 QUIC 数据包都由 UDP 数据报承载，因此这些统计覆盖了连接上的所有流量。</p>',
        )],
    )


def translate_struct_connection_id():
    return translate_file(
        'struct.ConnectionId.html',
        type_kind='Struct',
        type_name='ConnectionId',
        wbr_pos=[10],
        title_in_english='ConnectionId in quinn - Rust',
        title_in_chinese='quinn 中的 ConnectionId - Rust',
        description_old='Protocol-level identifier for a connection.',
        description_new='连接的协议级标识符。',
        docblocks=[(
            '<p>Protocol-level identifier for a connection.</p>\n<p>Mainly useful for identifying this connection’s packets on the wire with tools like Wireshark.</p>',
            '<p>连接的协议级标识符。</p>\n<p>主要用于通过 Wireshark 之类的工具在链路上识别该连接的数据包。</p>',
        )],
    )


def translate_struct_ack_frequency_config():
    return translate_file(
        'struct.AckFrequencyConfig.html',
        type_kind='Struct',
        type_name='AckFrequencyConfig',
        wbr_pos=[3, 14],
        title_in_english='AckFrequencyConfig in quinn - Rust',
        title_in_chinese='quinn 中的 AckFrequencyConfig - Rust',
        description_old='Parameters for controlling the peer’s acknowledgement frequency',
        description_new='用于控制对端确认（ACK）频率的参数',
        docblocks=[(
            '<p>Parameters for controlling the peer’s acknowledgement frequency</p>\n<p>The parameters provided in this config will be sent to the peer at the beginning of the\nconnection, so it can take them into account when sending acknowledgements (see each parameter’s\ndescription for details on how it influences acknowledgement frequency).</p>\n<p>Quinn’s implementation follows the fourth draft of the\n<a href="https://datatracker.ietf.org/doc/html/draft-ietf-quic-ack-frequency-04">QUIC Acknowledgement Frequency extension</a>.\nThe defaults produce behavior slightly different than the behavior without this extension,\nbecause they change the way reordered packets are handled (see\n<a href="struct.AckFrequencyConfig.html#method.reordering_threshold" title="method quinn::AckFrequencyConfig::reordering_threshold"><code>AckFrequencyConfig::reordering_threshold</code></a> for details).</p>',
            '<p>用于控制对端确认（ACK）频率的参数</p>\n<p>本配置中提供的参数会在连接开始时发送给对端，以便其在发送确认时将这些参数考虑在内（每个参数的具体描述中说明了其如何影响确认频率）。</p>\n<p>Quinn 的实现遵循第四版\n<a href="https://datatracker.ietf.org/doc/html/draft-ietf-quic-ack-frequency-04">QUIC Acknowledgement Frequency extension</a> 草案。\n默认值所表现出的行为与不启用此扩展时略有不同，因为它们改变了乱序数据包的处理方式（详见\n<a href="struct.AckFrequencyConfig.html#method.reordering_threshold" title="method quinn::AckFrequencyConfig::reordering_threshold"><code>AckFrequencyConfig::reordering_threshold</code></a>）。</p>',
        )],
    )


def translate_struct_bloom_token_log():
    return translate_file(
        'struct.BloomTokenLog.html',
        type_kind='Struct',
        type_name='BloomTokenLog',
        wbr_pos=[5, 10],
        title_in_english='BloomTokenLog in quinn - Rust',
        title_in_chinese='quinn 中的 BloomTokenLog - Rust',
        description_old='Bloom filter-based `TokenLog`',
        description_new='基于布隆过滤器的 `TokenLog`',
        docblocks=[(
            '<p>Bloom filter-based <a href="trait.TokenLog.html" title="trait quinn::TokenLog"><code>TokenLog</code></a></p>\n<p>Parameterizable over an approximate maximum number of bytes to allocate. Starts out by storing\nused tokens in a hash set. Once the hash set becomes too large, converts it to a bloom filter.\nThis achieves a memory profile of linear growth with an upper bound.</p>\n<p>Divides time into periods based on <code>lifetime</code> and stores two filters at any given moment, for\neach of the two periods currently non-expired tokens could expire in. As such, turns over\nfilters as time goes on to avoid bloom filter false positive rate increasing infinitely over\ntime.</p>',
            '<p>基于布隆过滤器的 <a href="trait.TokenLog.html" title="trait quinn::TokenLog"><code>TokenLog</code></a></p>\n<p>可以参数化一个近似的最大分配字节数。最初将已使用的 token 存入一个哈希集合；一旦哈希集合过大，便会转换为一个布隆过滤器。这样可以实现内存占用随规模线性增长且有上限的形态。</p>\n<p>基于 <code>lifetime</code> 将时间划分为若干时段，并在任意时刻为当前可能令未过期 token 过期的两个时段各维护一个过滤器。随着时间推移会不断轮换过滤器，以避免布隆过滤器的误判率随时间无限增长。</p>',
        )],
    )


def translate_struct_endpoint():
    return translate_file(
        'struct.Endpoint.html',
        type_kind='Struct',
        type_name='Endpoint',
        title_in_english='Endpoint in quinn - Rust',
        title_in_chinese='quinn 中的 Endpoint - Rust',
        description_old='A QUIC endpoint.',
        description_new='一个 QUIC 端点。',
        docblocks=[(
            '<p>A QUIC endpoint.</p>\n<p>An endpoint corresponds to a single UDP socket, may host many connections, and may act as both\nclient and server for different connections.</p>\n<p>May be cloned to obtain another handle to the same endpoint.</p>',
            '<p>一个 QUIC 端点。</p>\n<p>一个端点对应一个 UDP 套接字，可以承载多个连接，并且对于不同连接可以同时充当客户端和服务器。</p>\n<p>可以通过克隆来获得指向同一端点的另一个句柄。</p>',
        )],
    )


def translate_struct_transport_config():
    return translate_file(
        'struct.TransportConfig.html',
        type_kind='Struct',
        type_name='TransportConfig',
        wbr_pos=[9],
        title_in_english='TransportConfig in quinn - Rust',
        title_in_chinese='quinn 中的 TransportConfig - Rust',
        description_old='Parameters governing the core QUIC state machine',
        description_new='控制 QUIC 核心状态机的参数',
        docblocks=[(
            '<p>Parameters governing the core QUIC state machine</p>\n<p>Default values should be suitable for most internet applications. Applications protocols which\nforbid remotely-initiated streams should set <code>max_concurrent_bidi_streams</code> and\n<code>max_concurrent_uni_streams</code> to zero.</p>\n<p>In some cases, performance or resource requirements can be improved by tuning these values to\nsuit a particular application and/or network connection. In particular, data window sizes can be\ntuned for a particular expected round trip time, link capacity, and memory availability. Tuning\nfor higher bandwidths and latencies increases worst-case memory consumption, but does not impair\nperformance at lower bandwidths and latencies. The default configuration is tuned for a 100Mbps\nlink with a 100ms round trip time.</p>',
            '<p>控制 QUIC 核心状态机的参数</p>\n<p>默认值应该适合大多数互联网应用。对于禁止对端主动开启流的协议，应将 <code>max_concurrent_bidi_streams</code> 和 <code>max_concurrent_uni_streams</code> 设为 0。</p>\n<p>在某些情况下，可以通过针对特定应用和/或网络连接调整这些值来改善性能或资源需求。尤其是数据窗口大小可以针对期望的往返时间、链路容量和可用内存进行调优。调高带宽和延迟会增加最坏情况下的内存消耗，但不会影响较低带宽和延迟下的性能。默认配置针对的是 100Mbps 带宽、100ms 往返时间的链路进行调优。</p>',
        )],
    )


def translate_struct_idle_timeout():
    return translate_file(
        'struct.IdleTimeout.html',
        type_kind='Struct',
        type_name='IdleTimeout',
        wbr_pos=[4],
        title_in_english='IdleTimeout in quinn - Rust',
        title_in_chinese='quinn 中的 IdleTimeout - Rust',
        description_old='Maximum duration of inactivity to accept before timing out the connection',
        description_new='在使连接超时之前所允许的最大空闲时长',
        docblocks=[(
            '<p>Maximum duration of inactivity to accept before timing out the connection</p>\n<p>This wraps an underlying <a href="struct.VarInt.html" title="struct quinn::VarInt"><code>VarInt</code></a>, representing the duration in milliseconds. Values can be\nconstructed by converting directly from <code>VarInt</code>, or using <code>TryFrom&lt;Duration&gt;</code>.</p>',
            '<p>在使连接超时之前所允许的最大空闲时长</p>\n<p>它包装了一个底层的 <a href="struct.VarInt.html" title="struct quinn::VarInt"><code>VarInt</code></a>，以毫秒表示时长。可以通过直接从 <code>VarInt</code> 转换来构造值，也可以使用 <code>TryFrom&lt;Duration&gt;</code>。</p>',
        )],
        # The example code block contains Rust code that should remain in English
        # (the comment markers are translated in the source's code-block comment,
        # but we leave the example block untouched to keep code semantics intact).
    )


def translate_struct_connection():
    return translate_file(
        'struct.Connection.html',
        type_kind='Struct',
        type_name='Connection',
        title_in_english='Connection in quinn - Rust',
        title_in_chinese='quinn 中的 Connection - Rust',
        description_old='A QUIC connection.',
        description_new='一个 QUIC 连接。',
        docblocks=[(
            '<p>A QUIC connection.</p>\n<p>If all references to a connection (including every clone of the <code>Connection</code> handle, streams of\nincoming streams, and the various stream types) have been dropped, then the connection will be\nautomatically closed with an <code>error_code</code> of 0 and an empty <code>reason</code>. You can also close the\nconnection explicitly by calling <a href="struct.Connection.html#method.close" title="method quinn::Connection::close"><code>Connection::close()</code></a>.</p>\n<p>Closing the connection immediately abandons efforts to deliver data to the peer.  Upon\nreceiving CONNECTION_CLOSE the peer <em>may</em> drop any stream data not yet delivered to the\napplication. <a href="struct.Connection.html#method.close" title="method quinn::Connection::close"><code>Connection::close()</code></a> describes in more detail how to gracefully close a\nconnection without losing application data.</p>\n<p>May be cloned to obtain another handle to the same connection.</p>',
            '<p>一个 QUIC 连接。</p>\n<p>如果一个连接的所有引用（包括每个 <code>Connection</code> 句柄的克隆、各类入站流以及各种流类型）都被释放，则该连接会自动关闭，<code>error_code</code> 为 0 且 <code>reason</code> 为空。你也可以通过调用 <a href="struct.Connection.html#method.close" title="method quinn::Connection::close"><code>Connection::close()</code></a> 来显式关闭连接。</p>\n<p>关闭连接会立即放弃向对端投递数据的尝试。对端在收到 CONNECTION_CLOSE 时<em>可能</em>会丢弃尚未交付给应用的任何流数据。<a href="struct.Connection.html#method.close" title="method quinn::Connection::close"><code>Connection::close()</code></a> 中更详细地介绍了如何在不丢失应用数据的前提下优雅地关闭连接。</p>\n<p>可以通过克隆来获得指向同一连接的另一个句柄。</p>',
        )],
    )


def translate_struct_mtu_discovery_config():
    return translate_file(
        'struct.MtuDiscoveryConfig.html',
        type_kind='Struct',
        type_name='MtuDiscoveryConfig',
        wbr_pos=[12],
        title_in_english='MtuDiscoveryConfig in quinn - Rust',
        title_in_chinese='quinn 中的 MtuDiscoveryConfig - Rust',
        description_old='Parameters governing MTU discovery.',
        description_new='控制 MTU 探测的各个参数。',
        docblocks=[(
            '<p>Parameters governing MTU discovery.</p>\n<h2 id="the-why-of-mtu-discovery"><a class="doc-anchor" href="#the-why-of-mtu-discovery">§</a>The why of MTU discovery</h2>\n<p>By design, QUIC ensures during the handshake that the network path between the client and the\nserver is able to transmit unfragmented UDP packets with a body of 1200 bytes. In other words,\nonce the connection is established, we know that the network path’s maximum transmission unit\n(MTU) is of at least 1200 bytes (plus IP and UDP headers). Because of this, a QUIC endpoint can\nsplit outgoing data in packets of 1200 bytes, with confidence that the network will be able to\ndeliver them (if the endpoint were to send bigger packets, they could prove too big and end up\nbeing dropped).</p>\n<p>There is, however, a significant overhead associated to sending a packet. If the same\ninformation can be sent in fewer packets, that results in higher throughput. The amount of\npackets that need to be sent is inversely proportional to the MTU: the higher the MTU, the\nbigger the packets that can be sent, and the fewer packets that are needed to transmit a given\namount of bytes.</p>\n<p>Most networks have an MTU higher than 1200. Through MTU discovery, endpoints can detect the\npath’s MTU and, if it turns out to be higher, start sending bigger packets.</p>\n<h2 id="mtu-discovery-internals"><a class="doc-anchor" href="#mtu-discovery-internals">§</a>MTU discovery internals</h2>\n<p>Quinn implements MTU discovery through DPLPMTUD (Datagram Packetization Layer Path MTU\nDiscovery), described in <a href="https://www.rfc-editor.org/rfc/rfc9000.html#section-14.3">section 14.3 of RFC\n9000</a>. This method consists of sending\nQUIC packets padded to a particular size (called PMTU probes), and waiting to see if the remote\npeer responds with an ACK. If an ACK is received, that means the probe arrived at the remote\npeer, which in turn means that the network path’s MTU is of at least the packet’s size. If the\nprobe is lost, it is sent another 2 times before concluding that the MTU is lower than the\npacket’s size.</p>\n<p>MTU discovery runs on a schedule (e.g. every 600 seconds) specified through\n<a href="struct.MtuDiscoveryConfig.html#method.interval" title="method quinn::MtuDiscoveryConfig::interval"><code>MtuDiscoveryConfig::interval</code></a>. The first run happens right after the handshake, and\nsubsequent discoveries are scheduled to run when the interval has elapsed, starting from the\nlast time when MTU discovery completed.</p>\n<p>Since the search space for MTUs is quite big (the smallest possible MTU is 1200, and the highest\nis 65527), Quinn performs a binary search to keep the number of probes as low as possible. The\nlower bound of the search is equal to <a href="struct.TransportConfig.html#method.initial_mtu" title="method quinn::TransportConfig::initial_mtu"><code>TransportConfig::initial_mtu</code></a> in the\ninitial MTU discovery run, and is equal to the currently discovered MTU in subsequent runs. The\nupper bound is determined by the minimum of <a href="struct.MtuDiscoveryConfig.html#method.upper_bound" title="method quinn::MtuDiscoveryConfig::upper_bound"><code>MtuDiscoveryConfig::upper_bound</code></a> and the\n<code>max_udp_payload_size</code> transport parameter received from the peer during the handshake.</p>\n<h2 id="black-hole-detection"><a class="doc-anchor" href="#black-hole-detection">§</a>Black hole detection</h2>\n<p>If, at some point, the network path no longer accepts packets of the detected size, packet loss\nwill eventually trigger black hole detection and reset the detected MTU to 1200. In that case,\nMTU discovery will be triggered after <a href="struct.MtuDiscoveryConfig.html#method.black_hole_cooldown" title="method quinn::MtuDiscoveryConfig::black_hole_cooldown"><code>MtuDiscoveryConfig::black_hole_cooldown</code></a> (ignoring the\ntimer that was set based on <a href="struct.MtuDiscoveryConfig.html#method.interval" title="method quinn::MtuDiscoveryConfig::interval"><code>MtuDiscoveryConfig::interval</code></a>).</p>\n<h2 id="interaction-between-peers"><a class="doc-anchor" href="#interaction-between-peers">§</a>Interaction between peers</h2>\n<p>There is no guarantee that the MTU on the path between A and B is the same as the MTU of the\npath between B and A. Therefore, each peer in the connection needs to run MTU discovery\nindependently in order to discover the path’s MTU.</p>',
            '<p>控制 MTU 探测的各个参数。</p>\n<h2 id="the-why-of-mtu-discovery"><a class="doc-anchor" href="#the-why-of-mtu-discovery">§</a>为什么要做 MTU 探测</h2>\n<p>QUIC 在设计上有意保证：在握手阶段，客户端与服务器之间的网络路径能够传输有效载荷为 1200 字节且不分片的 UDP 数据包。换句话说，连接建立后我们就知道该路径的最大传输单元（MTU）至少为 1200 字节（再加上 IP 与 UDP 头部）。因此，QUIC 端点可以放心地把待发数据切成 1200 字节的数据包（如果端点发送更大的包，可能会因过大而被丢弃）。</p>\n<p>然而，发送数据包本身会带来显著的开销。如果同样一份信息能用更少的包发完，就能获得更高的吞吐。所需发送的数据包数量与 MTU 成反比：MTU 越大，单包可承载的字节越多，传输给定数据量所需的包数也就越少。</p>\n<p>大多数网络的 MTU 都大于 1200 字节。通过 MTU 探测，端点可以探知路径的 MTU；若发现 MTU 更大，便可开始发送更大的数据包。</p>\n<h2 id="mtu-discovery-internals"><a class="doc-anchor" href="#mtu-discovery-internals">§</a>MTU 探测的实现细节</h2>\n<p>Quinn 通过 DPLPMTUD（Datagram Packetization Layer Path MTU Discovery）实现 MTU 探测，详见 <a href="https://www.rfc-editor.org/rfc/rfc9000.html#section-14.3">RFC 9000 第 14.3 节</a>。该方法会发送填充到特定大小的 QUIC 数据包（称为 PMTU probe），然后观察对端是否回应 ACK。如果收到 ACK，则说明该探测包成功到达对端，也即该路径的 MTU 至少为该包的大小。如果探测包丢失，会再重发 2 次；3 次都失败时，便认定该路径的 MTU 小于该包的大小。</p>\n<p>MTU 探测按一定周期运行（默认每 600 秒一次），该周期通过 <a href="struct.MtuDiscoveryConfig.html#method.interval" title="method quinn::MtuDiscoveryConfig::interval"><code>MtuDiscoveryConfig::interval</code></a> 指定。第一次探测发生在握手刚结束后；后续探测的调度起点是上一次探测完成的时间，到达 interval 之后再次运行。</p>\n<p>由于 MTU 的搜索空间非常大（最小为 1200，最大为 65527），Quinn 采用二分查找以尽量减少探测次数。首次探测时，搜索下界为 <a href="struct.TransportConfig.html#method.initial_mtu" title="method quinn::TransportConfig::initial_mtu"><code>TransportConfig::initial_mtu</code></a>；后续探测时，下界为当前已探测到的 MTU。上界则取 <a href="struct.MtuDiscoveryConfig.html#method.upper_bound" title="method quinn::MtuDiscoveryConfig::upper_bound"><code>MtuDiscoveryConfig::upper_bound</code></a> 与握手阶段从对端收到的 <code>max_udp_payload_size</code> 传输参数中的较小者。</p>\n<h2 id="black-hole-detection"><a class="doc-anchor" href="#black-hole-detection">§</a>黑洞检测</h2>\n<p>如果在某个时刻网络路径不再接受探测到的那个尺寸的数据包，那么丢包最终会触发黑洞检测，并将探测到的 MTU 重置为 1200。此时将等待 <a href="struct.MtuDiscoveryConfig.html#method.black_hole_cooldown" title="method quinn::MtuDiscoveryConfig::black_hole_cooldown"><code>MtuDiscoveryConfig::black_hole_cooldown</code></a> 时间后再次触发 MTU 探测（忽略原先基于 <a href="struct.MtuDiscoveryConfig.html#method.interval" title="method quinn::MtuDiscoveryConfig::interval"><code>MtuDiscoveryConfig::interval</code></a> 设置的定时器）。</p>\n<h2 id="interaction-between-peers"><a class="doc-anchor" href="#interaction-between-peers">§</a>对端之间的相互作用</h2>\n<p>A 到 B 的路径 MTU 与 B 到 A 的路径 MTU 不一定相同。因此，连接中的每个对端都需要独立地运行 MTU 探测，才能发现各自方向的路径 MTU。</p>',
        )],
    )


def translate_struct_recv_stream():
    return translate_file(
        'struct.RecvStream.html',
        type_kind='Struct',
        type_name='RecvStream',
        wbr_pos=[4],
        title_in_english='RecvStream in quinn - Rust',
        title_in_chinese='quinn 中的 RecvStream - Rust',
        description_old='A stream that can only be used to receive data',
        description_new='仅可用于接收数据的流',
        docblocks=[(
            '<p>A stream that can only be used to receive data</p>\n<p><code>stop(0)</code> is implicitly called on drop unless:</p>\n<ul>\n<li>A variant of <a href="enum.ReadError.html" title="enum quinn::ReadError"><code>ReadError</code></a> has been yielded by a read call</li>\n<li><a href="struct.RecvStream.html#method.stop" title="method quinn::RecvStream::stop"><code>stop()</code></a> was called explicitly</li>\n</ul>\n<h2 id="cancellation"><a class="doc-anchor" href="#cancellation">§</a>Cancellation</h2>\n<p>A <code>read</code> method is said to be <em>cancel-safe</em> when dropping its future before the future becomes\nready cannot lead to loss of stream data. This is true of methods which succeed immediately when\nany progress is made, and is not true of methods which might need to perform multiple reads\ninternally before succeeding. Each <code>read</code> method documents whether it is cancel-safe.</p>\n<h2 id="common-issues"><a class="doc-anchor" href="#common-issues">§</a>Common issues</h2><h3 id="data-never-received-on-a-locally-opened-stream"><a class="doc-anchor" href="#data-never-received-on-a-locally-opened-stream">§</a>Data never received on a locally-opened stream</h3>\n<p>Peers are not notified of streams until they or a later-numbered stream are used to send\ndata. If a bidirectional stream is locally opened but never used to send, then the peer may\nnever see it. Application protocols should always arrange for the endpoint which will first\ntransmit on a stream to be the endpoint responsible for opening it.</p>\n<h3 id="data-never-received-on-a-remotely-opened-stream"><a class="doc-anchor" href="#data-never-received-on-a-remotely-opened-stream">§</a>Data never received on a remotely-opened stream</h3>\n<p>Verify that the stream you are receiving is the same one that the server is sending on, e.g. by\nlogging the <a href="struct.RecvStream.html#method.id" title="method quinn::RecvStream::id"><code>id</code></a> of each. Streams are always accepted in the same order as they are created,\ni.e. ascending order by <a href="struct.StreamId.html" title="struct quinn::StreamId"><code>StreamId</code></a>. For example, even if a sender first transmits on\nbidirectional stream 1, the first stream yielded by <a href="struct.Connection.html#method.accept_bi" title="method quinn::Connection::accept_bi"><code>Connection::accept_bi</code></a> on the receiver\nwill be bidirectional stream 0.</p>',
            '<p>仅可用于接收数据的流</p>\n<p>在以下情况之外，析构时会隐式调用 <code>stop(0)</code>：</p>\n<ul>\n<li>某次读取调用返回了 <a href="enum.ReadError.html" title="enum quinn::ReadError"><code>ReadError</code></a> 中的一个变体</li>\n<li>显式调用了 <a href="struct.RecvStream.html#method.stop" title="method quinn::RecvStream::stop"><code>stop()</code></a></li>\n</ul>\n<h2 id="cancellation"><a class="doc-anchor" href="#cancellation">§</a>取消</h2>\n<p>当某个 <code>read</code> 方法的 future 在尚未就绪时被丢弃，但不会造成流数据丢失时，称该方法是<em>可安全取消的（cancel-safe）</em>。只要有任意的进展就能立即成功的方法属于可安全取消的；而那些内部可能需要执行多次读才能成功的方法则不属于。每个 <code>read</code> 方法的文档都会注明它是否可安全取消。</p>\n<h2 id="common-issues"><a class="doc-anchor" href="#common-issues">§</a>常见问题</h2><h3 id="data-never-received-on-a-locally-opened-stream"><a class="doc-anchor" href="#data-never-received-on-a-locally-opened-stream">§</a>在本地打开的流上始终收不到数据</h3>\n<p>对端在真正被用来发送数据（无论是它本身还是与它编号相同或更大的某条流）之前，并不会被通知该流的存在。如果一条双向流是在本地打开但始终未被用于发送，那么对端可能永远看不到这条流。应用协议应始终把“将先在该流上发送数据”的那一端安排为打开该流的一方。</p>\n<h3 id="data-never-received-on-a-remotely-opened-stream"><a class="doc-anchor" href="#data-never-received-on-a-remotely-opened-stream">§</a>在远端打开的流上始终收不到数据</h3>\n<p>请确认你正在接收的流与服务器正在发送数据的流是同一条，例如记录每条流的 <a href="struct.RecvStream.html#method.id" title="method quinn::RecvStream::id"><code>id</code></a>。流被接受的顺序与它们被创建的顺序完全一致，即按 <a href="struct.StreamId.html" title="struct quinn::StreamId"><code>StreamId</code></a> 升序排列。例如，即便发送方先在双向流 1 上传输数据，接收端从 <a href="struct.Connection.html#method.accept_bi" title="method quinn::Connection::accept_bi"><code>Connection::accept_bi</code></a> 中拿到的第一条流仍是双向流 0。</p>',
        )],
    )


def translate_struct_validation_token_config():
    return translate_file(
        'struct.ValidationTokenConfig.html',
        type_kind='Struct',
        type_name='ValidationTokenConfig',
        wbr_pos=[10, 15],
        title_in_english='ValidationTokenConfig in quinn - Rust',
        title_in_chinese='quinn 中的 ValidationTokenConfig - Rust',
        description_old='Configuration for sending and handling validation tokens in incoming connections',
        description_new='对入站连接中校验 token 的发送与处理进行配置',
        docblocks=[(
            '<p>Configuration for sending and handling validation tokens in incoming connections</p>\n<p>Default values should be suitable for most internet applications.</p>\n<h3 id="quic-tokens"><a class="doc-anchor" href="#quic-tokens">§</a>QUIC Tokens</h3>\n<p>The QUIC protocol defines a concept of “<a href="https://www.rfc-editor.org/rfc/rfc9000.html#section-8">address validation</a>”. Essentially, one side of a\nQUIC connection may appear to be receiving QUIC packets from a particular remote UDP address,\nbut it will only consider that remote address “validated” once it has convincing evidence that\nthe address is not being <a href="https://en.wikipedia.org/wiki/IP_address_spoofing">spoofed</a>.</p>\n<p>Validation is important primarily because of QUIC’s “anti-amplification limit.” This limit\nprevents a QUIC server from sending a client more than three times the number of bytes it has\nreceived from the client on a given address until that address is validated. This is designed\nto mitigate the ability of attackers to use QUIC-based servers as reflectors in <a href="https://en.wikipedia.org/wiki/Denial-of-service_attack#Amplification">amplification\nattacks</a>.</p>\n<p>A path may become validated in several ways. The server is always considered validated by the\nclient. The client usually begins in an unvalidated state upon first connecting or migrating,\nbut then becomes validated through various mechanisms that usually take one network round trip.\nHowever, in some cases, a client which has previously attempted to connect to a server may have\nbeen given a one-time use cryptographically secured “token” that it can send in a subsequent\nconnection attempt to be validated immediately.</p>\n<p>There are two ways these tokens can originate:</p>\n<ul>\n<li>If the server responds to an incoming connection with <code>retry</code>, a “retry token” is minted and\nsent to the client, which the client immediately uses to attempt to connect again. Retry\ntokens operate on short timescales, such as 15 seconds.</li>\n<li>If a client’s path within an active connection is validated, the server may send the client\none or more “validation tokens,” which the client may store for use in later connections to\nthe same server. Validation tokens may be valid for much longer lifetimes than retry token.</li>\n</ul>\n<p>The usage of validation tokens is most impactful in situations where 0-RTT data is also being\nused–in particular, in situations where the server sends the client more than three times more\n0.5-RTT data than it has received 0-RTT data. Since the successful completion of a connection\nhandshake implicitly causes the client’s address to be validated, transmission of 0.5-RTT data\nis the main situation where a server might be sending application data to an address that could\nbe validated by token usage earlier than it would become validated without token usage.</p>\n<p>These tokens should not be confused with “stateless reset tokens,” which are similarly named\nbut entirely unrelated.</p>',
            '<p>对入站连接中校验 token 的发送与处理进行配置</p>\n<p>默认值应该适合大多数互联网应用。</p>\n<h3 id="quic-tokens"><a class="doc-anchor" href="#quic-tokens">§</a>QUIC Token</h3>\n<p>QUIC 协议定义了一个“<a href="https://www.rfc-editor.org/rfc/rfc9000.html#section-8">地址校验（address validation）</a>”的概念。简单来说，QUIC 连接的一端虽然看起来在从一个特定的远端 UDP 地址接收 QUIC 数据包，但它只有在掌握充分证据证明该地址不是被“伪造”的之后，才会认为该远端地址是“已校验的”。</p>\n<p>校验之所以重要，主要是因为 QUIC 的“反放大限制”（anti-amplification limit）。该限制规定：在某个地址被校验之前，QUIC 服务器向该客户端发送的字节数不能超过它从该客户端在同一个地址上收到的字节数的三倍。这一机制是为了削弱攻击者把基于 QUIC 的服务器当作放大攻击中的反射器的可能。</p>\n<p>路径可以通过多种方式被校验。对客户端而言，服务器始终被视为已校验。客户端在首次连接或迁移后通常处于未校验状态，但随后会通过若干通常需要一次网络往返即可完成的机制被校验。然而，在某些情况下，先前曾尝试连接某服务器的客户端可能已经获得了一个一次性使用的、经过加密签名的“token”，它可以把这个 token 附加在下一次连接尝试中以被立即校验。</p>\n<p>这些 token 有两种来源：</p>\n<ul>\n<li>若服务器以 <code>retry</code> 来响应一条入站连接，就会生成一个“retry token”并发送给客户端，客户端会立即用该 token 再次发起连接。retry token 的有效时间很短，例如 15 秒。</li>\n<li>若客户端在某条活跃连接内的路径已被校验，服务器可以向客户端发送一个或多个“validation token”，客户端可以将它们保存下来以供后续向同一服务器建立连接时使用。validation token 的有效时长可以远长于 retry token。</li>\n</ul>\n<p>validation token 最能发挥作用的场景是同时在使用 0-RTT 数据的场合——尤其是当服务器向客户端发送的 0.5-RTT 数据量已经达到它收到的 0-RTT 数据量三倍以上时。由于连接握手的成功完成本身就意味着客户端地址被隐式地校验，0.5-RTT 数据的发送正是服务器最有可能向一个“本来要等更久才能通过 token 校验”的地址上发送应用数据的主要场景。</p>\n<p>这些 token 不要与“stateless reset token”混淆，虽然它们名字相近，但完全是两码事。</p>',
        )],
    )


# ----------------------------------------------------------------------
# Dispatch: run ONE target per invocation.
# ----------------------------------------------------------------------

TARGETS = {
    'struct.Connecting': translate_struct_connecting,
    'enum.ConfigError': translate_enum_config_error,
    'enum.ConnectError': translate_enum_connect_error,
    'enum.ConnectionError': translate_enum_connection_error,
    'enum.Dir': translate_enum_dir,
    'enum.EcnCodepoint': translate_enum_ecn_codepoint,
    'enum.ReadError': translate_enum_read_error,
    'enum.ReadExactError': translate_enum_read_exact_error,
    'enum.ReadToEndError': translate_enum_read_to_end_error,
    'enum.ResetError': translate_enum_reset_error,
    'enum.SendDatagramError': translate_enum_send_datagram_error,
    'enum.Side': translate_enum_side,
    'enum.StoppedError': translate_enum_stopped_error,
    'enum.WriteError': translate_enum_write_error,
    'trait.AsyncTimer': translate_trait_async_timer,
    'trait.AsyncUdpSocket': translate_trait_async_udp_socket,
    'trait.ConnectionIdGenerator': translate_trait_connection_id_generator,
    'trait.Runtime': translate_trait_runtime,
    'trait.TimeSource': translate_trait_time_source,
    'trait.TokenLog': translate_trait_token_log,
    'trait.TokenStore': translate_trait_token_store,
    'trait.UdpPoller': translate_trait_udp_poller,
    'struct.AcceptUni': translate_struct_accept_uni,
    'struct.ApplicationClose': translate_struct_application_close,
    'struct.Chunk': translate_struct_chunk,
    'struct.ClosedStream': translate_struct_closed_stream,
    'struct.ConnectionClose': translate_struct_connection_close,
    'struct.ConnectionStats': translate_struct_connection_stats,
    'struct.FrameStats': translate_struct_frame_stats,
    'struct.FrameType': translate_struct_frame_type,
    'struct.Incoming': translate_struct_incoming,
    'struct.IncomingFuture': translate_struct_incoming_future,
    'struct.NoneTokenLog': translate_struct_none_token_log,
    'struct.NoneTokenStore': translate_struct_none_token_store,
    'struct.PathStats': translate_struct_path_stats,
    'struct.RetryError': translate_struct_retry_error,
    'struct.StreamId': translate_struct_stream_id,
    'struct.TokenReuseError': translate_struct_token_reuse_error,
    'struct.TokioRuntime': translate_struct_tokio_runtime,
    'struct.Transmit': translate_struct_transmit,
    'struct.TransportErrorCode': translate_struct_transport_error_code,
    'struct.VarInt': translate_struct_var_int,
    'struct.VarIntBoundsExceeded': translate_struct_var_int_bounds_exceeded,
    'struct.Written': translate_struct_written,
    'struct.EndpointStats': translate_struct_endpoint_stats,
    'struct.TokenMemoryCache': translate_struct_token_memory_cache,
    'struct.ClientConfig': translate_struct_client_config,
    'struct.EndpointConfig': translate_struct_endpoint_config,
    'struct.ServerConfig': translate_struct_server_config,
    'struct.StdSystemTime': translate_struct_std_system_time,
    'struct.UdpStats': translate_struct_udp_stats,
    'struct.ConnectionId': translate_struct_connection_id,
    'struct.AckFrequencyConfig': translate_struct_ack_frequency_config,
    'struct.BloomTokenLog': translate_struct_bloom_token_log,
    'struct.Endpoint': translate_struct_endpoint,
    'struct.TransportConfig': translate_struct_transport_config,
    'struct.IdleTimeout': translate_struct_idle_timeout,
    'struct.Connection': translate_struct_connection,
    'struct.MtuDiscoveryConfig': translate_struct_mtu_discovery_config,
    'struct.RecvStream': translate_struct_recv_stream,
    'struct.ValidationTokenConfig': translate_struct_validation_token_config,
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in TARGETS:
        print(f'usage: python _translate_quinn.py <target>')
        print(f'known targets: {", ".join(sorted(TARGETS))}')
        sys.exit(2)
    TARGETS[sys.argv[1]]()
    print()


if __name__ == '__main__':
    main()
