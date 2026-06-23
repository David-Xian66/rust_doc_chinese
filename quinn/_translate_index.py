"""Translate quinn's top-level index.html to Chinese.

Workflow per rust-doc-translation-pattern:
- Use Python open() directly (no Read tool).
- Apply (old, new) replacements in long-string-first order.
- Preserve HTML structure, URLs, Rust identifiers.
"""

import os
import re

QUINN_ROOT = 'D:/Administrator/Documents/Code/rust_doc_all/quinn'


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


# Translation tables for common UI text (across rustdoc-generated pages).
COMMON = [
    # Sidebar / nav headers
    ('>All Items<', '>所有项<'),
    ('>Sections<', '>章节<'),
    ('>Crate Items<', '>crate 项<'),
    # Sidebar toc labels (title attributes used in TOC)
    (' title="All Items"', ' title="所有项"'),
    (' title="Sections"', ' title="章节"'),
    (' title="Crate Items"', ' title="crate 项"'),
    (' title="Re-exports"', ' title="重新导出"'),
    (' title="Modules"', ' title="模块"'),
    (' title="Structs"', ' title="结构体"'),
    (' title="Enums"', ' title="枚举"'),
    (' title="Traits"', ' title="trait"'),
    (' title="Functions"', ' title="函数"'),
    # Buttons / actions
    (' title="Copy item path to clipboard"', ' title="复制项目路径到剪贴板"'),
    ('>Copy item path<', '>复制项目路径<'),
    ('>Source<', '>源代码<'),
    ('>Expand description<', '>展开描述<'),
    # Skip link
    ('>Skip to main content<', '>跳到主要内容<'),
    # IE warning
    ('This old browser is unsupported and will most likely display funky things.',
     '此旧版浏览器不受支持，很可能会显示异常内容。'),
    # Section headers (H2)
    ('>Re-exports<', '>重新导出<'),
    ('>Modules<', '>模块<'),
    ('>Structs<', '>结构体<'),
    ('>Enums<', '>枚举<'),
    ('>Traits<', '>trait<'),
    ('>Functions<', '>函数<'),
    # Sidebar top bar
    ('>Crate quinn<', '>crate quinn<'),
    # Crate / module name in heading
    ('>Crate <span>quinn</span>', '>crate <span>quinn</span>'),
]


def translate_quinn_index(content):
    # Apply common UI replacements first
    for old, new in COMMON:
        if old not in content:
            print(f'  [MISS] common: {old[:60]!r}')
        content = content.replace(old, new)

    # Meta description
    old_meta = '<meta name="description" content="QUIC transport protocol implementation">'
    new_meta = '<meta name="description" content="QUIC 传输协议实现">'
    content = content.replace(old_meta, new_meta)

    # lang attribute
    content = content.replace('<html lang="en">', '<html lang="zh-CN">')

    # ---- Docblock (main intro) ----
    intro_pairs = [
        # Para 1
        ('<p>QUIC transport protocol implementation</p>',
         '<p>QUIC 传输协议实现</p>'),
        # Para 2
        ('<p><a href="https://en.wikipedia.org/wiki/QUIC">QUIC</a> is a modern transport protocol addressing\nshortcomings of TCP, such as head-of-line blocking, poor security, slow handshakes, and\ninefficient congestion control. This crate provides a portable userspace implementation. It\nbuilds on top of quinn-proto, which implements protocol logic independent of any particular\nruntime.</p>',
         '<p><a href="https://en.wikipedia.org/wiki/QUIC">QUIC</a> 是一种现代传输协议，针对 TCP 的不足之处进行了改进，例如队头阻塞、安全性弱、握手慢以及拥塞控制效率低下等。本 crate 提供了一套可移植的用户态实现。它构建于 quinn-proto 之上，后者实现了与具体运行时无关的协议逻辑。</p>'),
        # Para 3
        ('<p>The entry point of this crate is the <a href="struct.Endpoint.html" title="struct quinn::Endpoint"><code>Endpoint</code></a>.</p>',
         '<p>本 crate 的入口点是 <a href="struct.Endpoint.html" title="struct quinn::Endpoint"><code>Endpoint</code></a>。</p>'),
        # H2 About QUIC
        ('<h2 id="about-quic">',
         '<h2 id="about-quic">'),
        # Para "A QUIC connection is an association..." - keep long string together
        ('<p>A QUIC connection is an association between two endpoints. The endpoint which initiates the\nconnection is termed the client, and the endpoint which accepts it is termed the server. A\nsingle endpoint may function as both client and server for different connections, for example\nin a peer-to-peer application. To communicate application data, each endpoint may open streams\nup to a limit dictated by its peer. Typically, that limit is increased as old streams are\nfinished.</p>',
         '<p>QUIC 连接是两个端点之间的关联。发起连接的端点称为客户端，接受连接的端点称为服务器。单个端点可以针对不同连接同时充当客户端和服务器，例如在对等应用中。为了传输应用数据，每个端点都可以打开流，但流的数量受对端限制。通常该限制会随着旧流的结束而增加。</p>'),
        # Para streams unidirectional / bidirectional
        ('<p>Streams may be unidirectional or bidirectional, and are cheap to create and disposable. For\nexample, a traditionally datagram-oriented application could use a new stream for every\nmessage it wants to send, no longer needing to worry about MTUs. Bidirectional streams behave\nmuch like a traditional TCP connection, and are useful for sending messages that have an\nimmediate response, such as an HTTP request. Stream data is delivered reliably, and there is no\nordering enforced between data on different streams.</p>',
         '<p>流可以是单向或双向的，创建开销很低且用完即可丢弃。例如，传统面向数据报的应用可以为每条要发送的消息使用一个新流，而无需再考虑 MTU 问题。双向流的行为与传统 TCP 连接非常相似，适合发送需要立即响应的消息，例如 HTTP 请求。流数据是可靠交付的，不同流之间的数据不保证顺序。</p>'),
        # Para head-of-line blocking
        ('<p>By avoiding head-of-line blocking and providing unified congestion control across all streams\nof a connection, QUIC is able to provide higher throughput and lower latency than one or\nmultiple TCP connections between the same two hosts, while providing more useful behavior than\nraw UDP sockets.</p>',
         '<p>通过避免队头阻塞并在同一连接的所有流之间提供统一的拥塞控制，QUIC 能够在相同两个主机之间的一条或多条 TCP 连接之上提供更高的吞吐量和更低的延迟，同时相比原始 UDP 套接字提供更有用的语义。</p>'),
        # Para datagrams
        ('<p>Quinn also exposes unreliable datagrams, which are a low-level primitive preferred when\nautomatic fragmentation and retransmission of certain data is not desired.</p>',
         '<p>Quinn 还提供不可靠的数据报接口，这是一种底层原语，适合在不需要对某些数据进行自动分片和重传时使用。</p>'),
        # Para TLS 1.3
        ('<p>QUIC uses encryption and identity verification built directly on TLS 1.3. Just as with a TLS\nserver, it is useful for a QUIC server to be identified by a certificate signed by a trusted\nauthority. If this is infeasible–for example, if servers are short-lived or not associated\nwith a domain name–then as with TLS, self-signed certificates can be used to provide\nencryption alone.</p>',
         '<p>QUIC 直接基于 TLS 1.3 构建加密与身份验证机制。正如 TLS 服务器一样，QUIC 服务器最好使用由可信机构签发的证书来标识身份。如果这一点难以做到——例如服务器是短生命周期的或不绑定域名——那么与 TLS 一样，可以使用自签名证书来单纯提供加密。</p>'),
    ]
    for old, new in intro_pairs:
        if old not in content:
            print(f'  [MISS] intro: {old[:60]!r}')
        content = content.replace(old, new)

    # ---- Modules section ----
    module_pairs = [
        ('<dd>Logic for controlling the rate at which data is sent</dd>',
         '<dd>控制数据发送速率的逻辑</dd>'),
        ('<dd>Traits and implementations for the QUIC cryptography protocol</dd>',
         '<dd>QUIC 加密协议的 trait 与实现</dd>'),
    ]
    for old, new in module_pairs:
        if old not in content:
            print(f'  [MISS] module: {old[:60]!r}')
        content = content.replace(old, new)

    # ---- Structs section ----
    struct_pairs = [
        ('<dd>Future produced by <a href="struct.Endpoint.html#method.accept" title="method quinn::Endpoint::accept"><code>Endpoint::accept</code></a></dd>',
         '<dd>由 <a href="struct.Endpoint.html#method.accept" title="method quinn::Endpoint::accept"><code>Endpoint::accept</code></a> 产生的 Future</dd>'),
        ('<dd>Future produced by <a href="struct.Connection.html#method.accept_bi" title="method quinn::Connection::accept_bi"><code>Connection::accept_bi</code></a></dd>',
         '<dd>由 <a href="struct.Connection.html#method.accept_bi" title="method quinn::Connection::accept_bi"><code>Connection::accept_bi</code></a> 产生的 Future</dd>'),
        ('<dd>Future produced by <a href="struct.Connection.html#method.accept_uni" title="method quinn::Connection::accept_uni"><code>Connection::accept_uni</code></a></dd>',
         '<dd>由 <a href="struct.Connection.html#method.accept_uni" title="method quinn::Connection::accept_uni"><code>Connection::accept_uni</code></a> 产生的 Future</dd>'),
        ('<dd>Parameters for controlling the peer’s acknowledgement frequency</dd>',
         '<dd>用于控制对端确认（ACK）频率的参数</dd>'),
        ('<dd>Reason given by an application for closing the connection</dd>',
         '<dd>应用层给出的关闭连接的原因</dd>'),
        ('<dd>Bloom filter-based <a href="trait.TokenLog.html" title="trait quinn::TokenLog"><code>TokenLog</code></a></dd>',
         '<dd>基于布隆过滤器的 <a href="trait.TokenLog.html" title="trait quinn::TokenLog"><code>TokenLog</code></a></dd>'),
        ('<dd>A chunk of data from the receive stream</dd>',
         '<dd>来自接收流的一块数据</dd>'),
        ('<dd>Configuration for outgoing connections</dd>',
         '<dd>出站连接的配置</dd>'),
        ('<dd>Error indicating that a stream has not been opened or has already been finished or reset</dd>',
         '<dd>表示流尚未打开或已经结束 / 重置的错误</dd>'),
        ('<dd>In-progress connection attempt future</dd>',
         '<dd>正在进行的连接尝试的 Future</dd>'),
        ('<dd>A QUIC connection.</dd>',
         '<dd>一个 QUIC 连接。</dd>'),
        ('<dd>Reason given by the transport for closing the connection</dd>',
         '<dd>传输层给出的关闭连接的原因</dd>'),
        ('<dd>Protocol-level identifier for a connection.</dd>',
         '<dd>连接的协议级标识符。</dd>'),
        ('<dd>Connection statistics</dd>',
         '<dd>连接统计信息</dd>'),
        ('<dd>A QUIC endpoint.</dd>',
         '<dd>一个 QUIC 端点。</dd>'),
        ('<dd>Global configuration for the endpoint, affecting all connections</dd>',
         '<dd>端点的全局配置，会影响所有连接</dd>'),
        ('<dd>Statistics on <a href="struct.Endpoint.html" title="struct quinn::Endpoint">Endpoint</a> activity</dd>',
         '<dd>关于 <a href="struct.Endpoint.html" title="struct quinn::Endpoint">Endpoint</a> 活动的统计信息</dd>'),
        ('<dd>Number of frames transmitted or received of each frame type</dd>',
         '<dd>每种帧类型已发送或已接收的数量</dd>'),
        ('<dd>A QUIC frame type</dd>',
         '<dd>QUIC 帧类型</dd>'),
        ('<dd>Maximum duration of inactivity to accept before timing out the connection</dd>',
         '<dd>在使连接超时之前所允许的最大空闲时长</dd>'),
        ('<dd>An incoming connection for which the server has not yet begun its part of the handshake</dd>',
         '<dd>一个尚未由服务器开始其握手部分的入站连接</dd>'),
        ('<dd>Basic adapter to let <a href="struct.Incoming.html" title="struct quinn::Incoming"><code>Incoming</code></a> be <code>await</code>-ed like a <a href="struct.Connecting.html" title="struct quinn::Connecting"><code>Connecting</code></a></dd>',
         '<dd>一个基础适配器，让 <a href="struct.Incoming.html" title="struct quinn::Incoming"><code>Incoming</code></a> 能够像 <a href="struct.Connecting.html" title="struct quinn::Connecting"><code>Connecting</code></a> 一样被 <code>await</code></dd>'),
        ('<dd>Parameters governing MTU discovery.</dd>',
         '<dd>控制 MTU 探测的参数。</dd>'),
        ('<dd>Null implementation of <a href="trait.TokenLog.html" title="trait quinn::TokenLog"><code>TokenLog</code></a>, which never accepts tokens</dd>',
         '<dd><a href="trait.TokenLog.html" title="trait quinn::TokenLog"><code>TokenLog</code></a> 的空实现，从不接受任何 token</dd>'),
        ('<dd>Null implementation of <a href="trait.TokenStore.html" title="trait quinn::TokenStore"><code>TokenStore</code></a>, which does not store any tokens</dd>',
         '<dd><a href="trait.TokenStore.html" title="trait quinn::TokenStore"><code>TokenStore</code></a> 的空实现，不存储任何 token</dd>'),
        ('<dd>Future produced by <a href="struct.Connection.html#method.open_bi" title="method quinn::Connection::open_bi"><code>Connection::open_bi</code></a></dd>',
         '<dd>由 <a href="struct.Connection.html#method.open_bi" title="method quinn::Connection::open_bi"><code>Connection::open_bi</code></a> 产生的 Future</dd>'),
        ('<dd>Future produced by <a href="struct.Connection.html#method.open_uni" title="method quinn::Connection::open_uni"><code>Connection::open_uni</code></a></dd>',
         '<dd>由 <a href="struct.Connection.html#method.open_uni" title="method quinn::Connection::open_uni"><code>Connection::open_uni</code></a> 产生的 Future</dd>'),
        ('<dd>Statistics related to a transmission path</dd>',
         '<dd>与某条传输路径相关的统计信息</dd>'),
        ('<dd>Future produced by <a href="struct.Connection.html#method.read_datagram" title="method quinn::Connection::read_datagram"><code>Connection::read_datagram</code></a></dd>',
         '<dd>由 <a href="struct.Connection.html#method.read_datagram" title="method quinn::Connection::read_datagram"><code>Connection::read_datagram</code></a> 产生的 Future</dd>'),
        ('<dd>A stream that can only be used to receive data</dd>',
         '<dd>只能用于接收数据的流</dd>'),
        ('<dd>Error for attempting to retry an <a href="struct.Incoming.html" title="struct quinn::Incoming"><code>Incoming</code></a> which already bears a token from a previous retry</dd>',
         '<dd>尝试重试一个 <a href="struct.Incoming.html" title="struct quinn::Incoming"><code>Incoming</code></a> 时产生的错误，因为它已带有一个先前重试留下的 token</dd>'),
        ('<dd>Future produced by <a href="struct.Connection.html#method.send_datagram_wait" title="method quinn::Connection::send_datagram_wait"><code>Connection::send_datagram_wait</code></a></dd>',
         '<dd>由 <a href="struct.Connection.html#method.send_datagram_wait" title="method quinn::Connection::send_datagram_wait"><code>Connection::send_datagram_wait</code></a> 产生的 Future</dd>'),
        ('<dd>A stream that can only be used to send data</dd>',
         '<dd>只能用于发送数据的流</dd>'),
        ('<dd>Parameters governing incoming connections</dd>',
         '<dd>控制入站连接的参数</dd>'),
        ('<dd>Default implementation of <a href="trait.TimeSource.html" title="trait quinn::TimeSource"><code>TimeSource</code></a></dd>',
         '<dd><a href="trait.TimeSource.html" title="trait quinn::TimeSource"><code>TimeSource</code></a> 的默认实现</dd>'),
        ('<dd>Identifier for a stream within a particular connection</dd>',
         '<dd>特定连接中某条流的标识符</dd>'),
        ('<dd><code>TokenStore</code> implementation that stores up to <code>N</code> tokens per server name for up to a\nlimited number of server names, in-memory</dd>',
         '<dd><code>TokenStore</code> 的一个实现：在内存中为有限数量的服务器名称各存储最多 <code>N</code> 个 token</dd>'),
        ('<dd>Error for when a validation token may have been reused</dd>',
         '<dd>校验 token 疑似被复用时产生的错误</dd>'),
        ('<dd>A Quinn runtime for Tokio</dd>',
         '<dd>用于 Tokio 的 Quinn 运行时</dd>'),
        ('<dd>An outgoing packet</dd>',
         '<dd>一个出站数据包</dd>'),
        ('<dd>Parameters governing the core QUIC state machine</dd>',
         '<dd>控制 QUIC 核心状态机的参数</dd>'),
        ('<dd>Transport-level error code</dd>',
         '<dd>传输层错误码</dd>'),
        ('<dd>Statistics about UDP datagrams transmitted or received on a connection</dd>',
         '<dd>连接上已发送或已接收的 UDP 数据报统计信息</dd>'),
        ('<dd>Configuration for sending and handling validation tokens in incoming connections</dd>',
         '<dd>用于在入站连接中发送和处理校验 token 的配置</dd>'),
        ('<dd>An integer less than 2^62</dd>',
         '<dd>一个小于 2^62 的整数</dd>'),
        ('<dd>Error returned when constructing a <code>VarInt</code> from a value &gt;= 2^62</dd>',
         '<dd>当使用大于等于 2^62 的值构造 <code>VarInt</code> 时返回的错误</dd>'),
        ('<dd>Indicates how many bytes and chunks had been transferred in a write operation</dd>',
         '<dd>指示一次写入操作中已传输的字节数和块数</dd>'),
        ('<dd>Future that completes when a connection is fully established</dd>',
         '<dd>在连接完全建立时完成的 Future</dd>'),
    ]
    for old, new in struct_pairs:
        if old not in content:
            print(f'  [MISS] struct: {old[:60]!r}')
        content = content.replace(old, new)

    # ---- Enums section ----
    enum_pairs = [
        ('<dd>Errors in the configuration of an endpoint</dd>',
         '<dd>端点配置中的错误</dd>'),
        ('<dd>Errors in the parameters being used to create a new connection</dd>',
         '<dd>用于创建新连接的参数中的错误</dd>'),
        ('<dd>Reasons why a connection might be lost</dd>',
         '<dd>连接可能丢失的原因</dd>'),
        ('<dd>Whether a stream communicates data in both directions or only from the initiator</dd>',
         '<dd>流是双向通信还是仅由发起方单向通信</dd>'),
        ('<dd>Explicit congestion notification codepoint</dd>',
         '<dd>显式拥塞通知 (ECN) 码点</dd>'),
        ('<dd>Errors that arise from reading from a stream.</dd>',
         '<dd>从流读取时产生的错误。</dd>'),
        ('<dd>Errors from <a href="struct.RecvStream.html#method.read_to_end" title="method quinn::RecvStream::read_to_end"><code>RecvStream::read_to_end</code></a></dd>',
         '<dd>由 <a href="struct.RecvStream.html#method.read_to_end" title="method quinn::RecvStream::read_to_end"><code>RecvStream::read_to_end</code></a> 产生的错误</dd>'),
        ('<dd>Errors that arise while waiting for a stream to be reset</dd>',
         '<dd>在等待流被重置时产生的错误</dd>'),
        ('<dd>Errors that can arise when sending a datagram</dd>',
         '<dd>发送数据报时可能产生的错误</dd>'),
        ('<dd>Whether an endpoint was the initiator of a connection</dd>',
         '<dd>端点是连接的发起方还是接收方</dd>'),
        ('<dd>Errors that arise while monitoring for a send stream stop from the peer</dd>',
         '<dd>在监视对端停止发送流时产生的错误</dd>'),
        ('<dd>Errors that arise from writing to a stream</dd>',
         '<dd>向流写入时产生的错误</dd>'),
    ]
    for old, new in enum_pairs:
        if old not in content:
            print(f'  [MISS] enum: {old[:60]!r}')
        content = content.replace(old, new)

    # ---- Traits section ----
    trait_pairs = [
        ('<dd>Abstract implementation of an async timer for runtime independence</dd>',
         '<dd>异步定时器的抽象实现，用于运行时无关性</dd>'),
        ('<dd>Abstract implementation of a UDP socket for runtime independence</dd>',
         '<dd>UDP 套接字的抽象实现，用于运行时无关性</dd>'),
        ('<dd>Generates connection IDs for incoming connections</dd>',
         '<dd>为入站连接生成连接 ID</dd>'),
        ('<dd>Abstracts I/O and timer operations for runtime independence</dd>',
         '<dd>对 I/O 与定时器操作的抽象，用于运行时无关性</dd>'),
        ('<dd>Object to get current <a href="https://doc.rust-lang.org/1.95.0/std/time/struct.SystemTime.html" title="struct std::time::SystemTime"><code>SystemTime</code></a></dd>',
         '<dd>用于获取当前 <a href="https://doc.rust-lang.org/1.95.0/std/time/struct.SystemTime.html" title="struct std::time::SystemTime"><code>SystemTime</code></a> 的对象</dd>'),
        ('<dd>Responsible for limiting clients’ ability to reuse validation tokens</dd>',
         '<dd>负责限制客户端复用校验 token 的能力</dd>'),
        ('<dd>Responsible for storing validation tokens received from servers and retrieving them for use in\nsubsequent connections</dd>',
         '<dd>负责存储从服务器接收到的校验 token，并在后续连接中取出使用</dd>'),
        ('<dd>An object polled to detect when an associated <a href="trait.AsyncUdpSocket.html" title="trait quinn::AsyncUdpSocket"><code>AsyncUdpSocket</code></a> is writable</dd>',
         '<dd>通过轮询检测关联的 <a href="trait.AsyncUdpSocket.html" title="trait quinn::AsyncUdpSocket"><code>AsyncUdpSocket</code></a> 是否可写</dd>'),
    ]
    for old, new in trait_pairs:
        if old not in content:
            print(f'  [MISS] trait: {old[:60]!r}')
        content = content.replace(old, new)

    # ---- Functions section ----
    func_pairs = [
        ('<dd>Automatically select an appropriate runtime from those enabled at compile time</dd>',
         '<dd>从编译时启用的运行时中自动选择一个合适的运行时</dd>'),
    ]
    for old, new in func_pairs:
        if old not in content:
            print(f'  [MISS] func: {old[:60]!r}')
        content = content.replace(old, new)

    return content


def main():
    path = os.path.join(QUINN_ROOT, 'index.html')
    print(f'--- {path} ---')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = translate_quinn_index(content)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    rel = os.path.relpath(path, QUINN_ROOT)
    verify(new_content, rel)
    print()


if __name__ == '__main__':
    main()
