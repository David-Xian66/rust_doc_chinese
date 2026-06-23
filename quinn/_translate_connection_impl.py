"""Translate all impl-section method docblocks in quinn/struct.Connection.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/struct.Connection.html'

# Use the docblock <div>...</div> block as old/new pair.
TRANSLATIONS = [
    # 1. open_uni (2 paragraphs)
    (
        '<div class="docblock"><p>Initiate a new outgoing unidirectional stream.</p>\n<p>Streams are cheap and instantaneous to open unless blocked by flow control. As a\nconsequence, the peer won’t be notified that a stream has been opened until the stream is\nactually used.</p>',
        '<div class="docblock"><p>发起一个新的出站单向流。</p>\n<p>流的打开操作非常廉价且几乎是瞬时的，除非被流控阻塞。因此，在流真正被使用之前，对端并不会被通知该流已被打开。</p>',
    ),
    # 2. open_bi (2 paragraphs)
    (
        '<div class="docblock"><p>Initiate a new outgoing bidirectional stream.</p>\n<p>Streams are cheap and instantaneous to open unless blocked by flow control. As a\nconsequence, the peer won’t be notified that a stream has been opened until the stream is\nactually used. Calling <a href="struct.Connection.html#method.open_bi" title="method quinn::Connection::open_bi"><code>open_bi()</code></a> then waiting on the <a href="struct.RecvStream.html" title="struct quinn::RecvStream"><code>RecvStream</code></a> without writing\nanything to <a href="struct.SendStream.html" title="struct quinn::SendStream"><code>SendStream</code></a> will never succeed.</p>',
        '<div class="docblock"><p>发起一个新的出站双向流。</p>\n<p>流的打开操作非常廉价且几乎是瞬时的，除非被流控阻塞。因此，在流真正被使用之前，对端并不会被通知该流已被打开。调用 <a href="struct.Connection.html#method.open_bi" title="method quinn::Connection::open_bi"><code>open_bi()</code></a> 后，如果不在 <a href="struct.SendStream.html" title="struct quinn::SendStream"><code>SendStream</code></a> 上写入任何内容就等待 <a href="struct.RecvStream.html" title="struct quinn::RecvStream"><code>RecvStream</code></a>，那么将永远无法成功。</p>',
    ),
    # 3. accept_uni
    (
        '<div class="docblock"><p>Accept the next incoming uni-directional stream</p>',
        '<div class="docblock"><p>接受下一条入站的单向流</p>',
    ),
    # 4. accept_bi (2 paragraphs)
    (
        '<div class="docblock"><p>Accept the next incoming bidirectional stream</p>\n<p><strong>Important Note</strong>: The <code>Connection</code> that calls <a href="struct.Connection.html#method.open_bi" title="method quinn::Connection::open_bi"><code>open_bi()</code></a> must write to its <a href="struct.SendStream.html" title="struct quinn::SendStream"><code>SendStream</code></a>\nbefore the other <code>Connection</code> is able to <code>accept_bi()</code>. Calling <a href="struct.Connection.html#method.open_bi" title="method quinn::Connection::open_bi"><code>open_bi()</code></a> then\nwaiting on the <a href="struct.RecvStream.html" title="struct quinn::RecvStream"><code>RecvStream</code></a> without writing anything to <a href="struct.SendStream.html" title="struct quinn::SendStream"><code>SendStream</code></a> will never succeed.</p>',
        '<div class="docblock"><p>接受下一条入站的双向流</p>\n<p><strong>重要提示</strong>：调用 <a href="struct.Connection.html#method.open_bi" title="method quinn::Connection::open_bi"><code>open_bi()</code></a> 的那个 <code>Connection</code> 必须先在自己的 <a href="struct.SendStream.html" title="struct quinn::SendStream"><code>SendStream</code></a> 上写入数据，另一端的 <code>Connection</code> 才能 <code>accept_bi()</code> 成功。调用 <a href="struct.Connection.html#method.open_bi" title="method quinn::Connection::open_bi"><code>open_bi()</code></a> 之后，如果不在 <a href="struct.SendStream.html" title="struct quinn::SendStream"><code>SendStream</code></a> 上写入任何内容就等待 <a href="struct.RecvStream.html" title="struct quinn::RecvStream"><code>RecvStream</code></a>，将永远无法成功。</p>',
    ),
    # 5. read_datagram
    (
        '<div class="docblock"><p>Receive an application datagram</p>',
        '<div class="docblock"><p>接收一个应用数据报</p>',
    ),
    # 6. closed (2 paragraphs)
    (
        '<div class="docblock"><p>Wait for the connection to be closed for any reason</p>\n<p>Despite the return type’s name, closed connections are often not an error condition at the\napplication layer. Cases that might be routine include <a href="enum.ConnectionError.html#variant.LocallyClosed" title="variant quinn::ConnectionError::LocallyClosed"><code>ConnectionError::LocallyClosed</code></a>\nand <a href="enum.ConnectionError.html#variant.ApplicationClosed" title="variant quinn::ConnectionError::ApplicationClosed"><code>ConnectionError::ApplicationClosed</code></a>.</p>',
        '<div class="docblock"><p>等待该连接因任何原因而关闭</p>\n<p>尽管返回类型的名字带有“closed”，但连接关闭本身在应用层并不一定意味着错误。常见的常规情况包括 <a href="enum.ConnectionError.html#variant.LocallyClosed" title="variant quinn::ConnectionError::LocallyClosed"><code>ConnectionError::LocallyClosed</code></a> 和 <a href="enum.ConnectionError.html#variant.ApplicationClosed" title="variant quinn::ConnectionError::ApplicationClosed"><code>ConnectionError::ApplicationClosed</code></a>。</p>',
    ),
    # 7. close_reason (2 paragraphs)
    (
        '<div class="docblock"><p>If the connection is closed, the reason why.</p>\n<p>Returns <code>None</code> if the connection is still open.</p>',
        '<div class="docblock"><p>若连接已关闭，则返回其关闭原因。</p>\n<p>若连接仍然处于打开状态，则返回 <code>None</code>。</p>',
    ),
    # 8. close (complex, with H5 section)
    (
        '<div class="docblock"><p>Close the connection immediately.</p>\n<p>Pending operations will fail immediately with <a href="enum.ConnectionError.html#variant.LocallyClosed" title="variant quinn::ConnectionError::LocallyClosed"><code>ConnectionError::LocallyClosed</code></a>. No\nmore data is sent to the peer and the peer may drop buffered data upon receiving\nthe CONNECTION_CLOSE frame.</p>\n<p><code>error_code</code> and <code>reason</code> are not interpreted, and are provided directly to the peer.</p>\n<p><code>reason</code> will be truncated to fit in a single packet with overhead; to improve odds that it\nis preserved in full, it should be kept under 1KiB.</p>\n<h5 id="gracefully-closing-a-connection"><a class="doc-anchor" href="#gracefully-closing-a-connection">§</a>Gracefully closing a connection</h5>\n<p>Only the peer last receiving application data can be certain that all data is\ndelivered. The only reliable action it can then take is to close the connection,\npotentially with a custom error code. The delivery of the final CONNECTION_CLOSE\nframe is very likely if both endpoints stay online long enough, and\n<a href="struct.Endpoint.html#method.wait_idle" title="method quinn::Endpoint::wait_idle"><code>Endpoint::wait_idle()</code></a> can be used to provide sufficient time. Otherwise, the\nremote peer will time out the connection, provided that the idle timeout is not\ndisabled.</p>\n<p>The sending side can not guarantee all stream data is delivered to the remote\napplication. It only knows the data is delivered to the QUIC stack of the remote\nendpoint. Once the local side sends a CONNECTION_CLOSE frame in response to calling\n<a href="struct.Connection.html#method.close" title="method quinn::Connection::close"><code>close()</code></a> the remote endpoint may drop any data it received but is as yet\nundelivered to the application, including data that was acknowledged as received to\nthe local endpoint.</p>',
        '<div class="docblock"><p>立即关闭该连接。</p>\n<p>所有挂起的操作都会立刻失败，并返回 <a href="enum.ConnectionError.html#variant.LocallyClosed" title="variant quinn::ConnectionError::LocallyClosed"><code>ConnectionError::LocallyClosed</code></a>。不会再向对端发送任何数据，对端在收到 CONNECTION_CLOSE 帧时也可能会丢弃其缓冲区中的数据。</p>\n<p><code>error_code</code> 与 <code>reason</code> 不会被解释，会原样传递给对端。</p>\n<p><code>reason</code> 会被截断以适应单个数据包（包括开销）；为提高它被完整保留的概率，建议将其长度控制在 1KiB 以内。</p>\n<h5 id="gracefully-closing-a-connection"><a class="doc-anchor" href="#gracefully-closing-a-connection">§</a>优雅地关闭连接</h5>\n<p>只有最后接收到应用数据的那一端才能确认所有数据已经被送达。它随后能采取的可靠动作就是关闭连接（可以带上自定义错误码）。如果两端都保持在线足够长的时间，那么最终的 CONNECTION_CLOSE 帧大概率能够送达；可以使用 <a href="struct.Endpoint.html#method.wait_idle" title="method quinn::Endpoint::wait_idle"><code>Endpoint::wait_idle()</code></a> 来提供这段等待时间。否则，远端将会在空闲超时（前提是未禁用空闲超时）后让连接超时。</p>\n<p>发送方无法保证所有的流数据都已经被送达远端应用，它只能确认数据已经送达远端的 QUIC 协议栈。一旦本端在调用 <a href="struct.Connection.html#method.close" title="method quinn::Connection::close"><code>close()</code></a> 后发送了 CONNECTION_CLOSE 帧，远端就可以丢弃任何它已收到但尚未交付给应用的数据——包括那些已经向本端确认收到的数据。</p>',
    ),
    # 9. send_datagram (3 paragraphs)
    (
        '<div class="docblock"><p>Transmit <code>data</code> as an unreliable, unordered application datagram</p>\n<p>Application datagrams are a low-level primitive. They may be lost or delivered out of order,\nand <code>data</code> must both fit inside a single QUIC packet and be smaller than the maximum\ndictated by the peer.</p>\n<p>Previously queued datagrams which are still unsent may be discarded to make space for this\ndatagram, in order of oldest to newest.</p>',
        '<div class="docblock"><p>将 <code>data</code> 作为不可靠、无序的应用数据报发送出去</p>\n<p>应用数据报是一个底层原语。它可能会丢失，也可能乱序到达；并且 <code>data</code> 必须既能容纳在单个 QUIC 数据包之内，又要小于对端所规定的最大值。</p>\n<p>为了腾出空间容纳本数据报，已经排队但尚未发出、且比本数据报更早入队的数据报可能会被按从旧到新的顺序丢弃。</p>',
    ),
    # 10. send_datagram_wait
    (
        '<div class="docblock"><p>Transmit <code>data</code> as an unreliable, unordered application datagram</p>\n<p>Unlike <a href="struct.Connection.html#method.send_datagram" title="method quinn::Connection::send_datagram"><code>send_datagram()</code></a>, this method will wait for buffer space during congestion\nconditions, which effectively prioritizes old datagrams over new datagrams.</p>\n<p>See <a href="struct.Connection.html#method.send_datagram" title="method quinn::Connection::send_datagram"><code>send_datagram()</code></a> for caveats regarding datagram size and reliability.</p>',
        '<div class="docblock"><p>将 <code>data</code> 作为不可靠、无序的应用数据报发送出去</p>\n<p>与 <a href="struct.Connection.html#method.send_datagram" title="method quinn::Connection::send_datagram"><code>send_datagram()</code></a> 不同，本方法在拥塞导致缓冲区不足时会等待空闲空间，因此实际上是优先发送旧的数据报而非新的。</p>\n<p>关于数据报大小与可靠性的注意事项，请参阅 <a href="struct.Connection.html#method.send_datagram" title="method quinn::Connection::send_datagram"><code>send_datagram()</code></a>。</p>',
    ),
    # 11. max_datagram_size (4 paragraphs)
    (
        '<div class="docblock"><p>Compute the maximum size of datagrams that may be passed to <a href="struct.Connection.html#method.send_datagram" title="method quinn::Connection::send_datagram"><code>send_datagram()</code></a>.</p>\n<p>Returns <code>None</code> if datagrams are unsupported by the peer or disabled locally.</p>\n<p>This may change over the lifetime of a connection according to variation in the path MTU\nestimate. The peer can also enforce an arbitrarily small fixed limit, but if the peer’s\nlimit is large this is guaranteed to be a little over a kilobyte at minimum.</p>\n<p>Not necessarily the maximum size of received datagrams.</p>',
        '<div class="docblock"><p>计算可传递给 <a href="struct.Connection.html#method.send_datagram" title="method quinn::Connection::send_datagram"><code>send_datagram()</code></a> 的数据报最大尺寸。</p>\n<p>若对端不支持数据报，或本端禁用了数据报，则返回 <code>None</code>。</p>\n<p>该值在连接生命周期内可能会随路径 MTU 估值的变化而变化。对端也可以强制施加一个任意小的固定上限；但只要对端的上限比较大，则该值保证至少略大于 1 KiB。</p>\n<p>该值不一定等于接收到的数据报的最大尺寸。</p>',
    ),
    # 12. datagram_send_buffer_space (2 paragraphs)
    (
        '<div class="docblock"><p>Bytes available in the outgoing datagram buffer</p>\n<p>When greater than zero, calling <a href="struct.Connection.html#method.send_datagram" title="method quinn::Connection::send_datagram"><code>send_datagram()</code></a> with a datagram of\nat most this size is guaranteed not to cause older datagrams to be dropped.</p>',
        '<div class="docblock"><p>出站数据报缓冲区中可用的字节数</p>\n<p>当该值大于零时，调用 <a href="struct.Connection.html#method.send_datagram" title="method quinn::Connection::send_datagram"><code>send_datagram()</code></a> 发送一个不超过此大小的数据报，可以保证不会导致旧的数据报被丢弃。</p>',
    ),
    # 13. side
    (
        '<div class="docblock"><p>The side of the connection (client or server)</p>',
        '<div class="docblock"><p>连接所处的角色（客户端或服务器）</p>',
    ),
    # 14. remote_address (2 paragraphs)
    (
        '<div class="docblock"><p>The peer’s UDP address</p>\n<p>If <code>ServerConfig::migration</code> is <code>true</code>, clients may change addresses at will, e.g. when\nswitching to a cellular internet connection.</p>',
        '<div class="docblock"><p>对端的 UDP 地址</p>\n<p>若 <code>ServerConfig::migration</code> 被设为 <code>true</code>，客户端可以随时更换地址，例如在切换到蜂窝网络连接时。</p>',
    ),
    # 15. local_ip (3 paragraphs)
    (
        '<div class="docblock"><p>The local IP address which was used when the peer established\nthe connection</p>\n<p>This can be different from the address the endpoint is bound to, in case\nthe endpoint is bound to a wildcard address like <code>0.0.0.0</code> or <code>::</code>.</p>\n<p>This will return <code>None</code> for clients, or when the platform does not expose this\ninformation. See <a href="../quinn_udp/struct.RecvMeta.html#structfield.dst_ip" title="field quinn_udp::RecvMeta::dst_ip"><code>quinn_udp::RecvMeta::dst_ip</code></a> for a list of\nsupported platforms when using <a href="../quinn_udp/index.html" title="mod quinn_udp"><code>quinn_udp</code></a> for I/O, which is the default.</p>',
        '<div class="docblock"><p>对端建立该连接时所使用的本地 IP 地址</p>\n<p>当端点绑定到 <code>0.0.0.0</code> 或 <code>::</code> 这样的通配地址时，该地址可能与端点绑定的地址不同。</p>\n<p>对于客户端，或者当平台不提供该信息时，该方法会返回 <code>None</code>。在使用 <a href="../quinn_udp/index.html" title="mod quinn_udp"><code>quinn_udp</code></a>（默认）作为 I/O 实现时，所支持的平台列表见 <a href="../quinn_udp/struct.RecvMeta.html#structfield.dst_ip" title="field quinn_udp::RecvMeta::dst_ip"><code>quinn_udp::RecvMeta::dst_ip</code></a>。</p>',
    ),
    # 16. rtt
    (
        '<div class="docblock"><p>Current best estimate of this connection’s latency (round-trip-time)</p>',
        '<div class="docblock"><p>该连接延迟（往返时间）的当前最佳估计值</p>',
    ),
    # 17. stats
    (
        '<div class="docblock"><p>Returns connection statistics</p>',
        '<div class="docblock"><p>返回该连接的统计信息</p>',
    ),
    # 18. congestion_state
    (
        '<div class="docblock"><p>Current state of the congestion control algorithm, for debugging purposes</p>',
        '<div class="docblock"><p>拥塞控制算法的当前状态，仅供调试使用</p>',
    ),
    # 19. handshake_data (2 paragraphs)
    (
        '<div class="docblock"><p>Parameters negotiated during the handshake</p>\n<p>Guaranteed to return <code>Some</code> on fully established connections or after\n<a href="struct.Connecting.html#method.handshake_data" title="method quinn::Connecting::handshake_data"><code>Connecting::handshake_data()</code></a> succeeds. See that method’s documentations for details on\nthe returned value.</p>',
        '<div class="docblock"><p>在握手阶段协商得到的参数</p>\n<p>对于已完全建立的连接，或在 <a href="struct.Connecting.html#method.handshake_data" title="method quinn::Connecting::handshake_data"><code>Connecting::handshake_data()</code></a> 成功之后，该方法保证返回 <code>Some</code>。关于返回值的详细信息，请参阅该方法的文档。</p>',
    ),
    # 20. peer_identity (2 paragraphs)
    (
        '<div class="docblock"><p>Cryptographic identity of the peer</p>\n<p>The dynamic type returned is determined by the configured\n<a href="crypto/trait.Session.html" title="trait quinn::crypto::Session"><code>Session</code></a>. For the default <code>rustls</code> session, the return value can\nbe <a href="https://doc.rust-lang.org/1.95.0/alloc/boxed/struct.Box.html#method.downcast" title="method alloc::boxed::Box::downcast"><code>downcast</code></a> to a <code>Vec&lt;<a href="../rustls_pki_types/struct.CertificateDer.html" title="struct rustls_pki_types::CertificateDer">rustls::pki_types::CertificateDer</a>&gt;</code></p>',
        '<div class="docblock"><p>对端的密码学身份</p>\n<p>返回值的具体动态类型由所配置的 <a href="crypto/trait.Session.html" title="trait quinn::crypto::Session"><code>Session</code></a> 决定。对于默认的 <code>rustls</code> 会话，返回值可以被 <a href="https://doc.rust-lang.org/1.95.0/alloc/boxed/struct.Box.html#method.downcast" title="method alloc::boxed::Box::downcast"><code>downcast</code></a> 为 <code>Vec&lt;<a href="../rustls_pki_types/struct.CertificateDer.html" title="struct rustls_pki_types::CertificateDer">rustls::pki_types::CertificateDer</a>&gt;</code>。</p>',
    ),
    # 21. stable_id (2 paragraphs)
    (
        '<div class="docblock"><p>A stable identifier for this connection</p>\n<p>Peer addresses and connection IDs can change, but this value will remain\nfixed for the lifetime of the connection.</p>',
        '<div class="docblock"><p>该连接的一个稳定标识符</p>\n<p>对端地址和连接 ID 都可能变化，但该值在连接的生命周期内始终保持不变。</p>',
    ),
    # 22. force_key_update (2 paragraphs)
    (
        '<div class="docblock"><p>Update traffic keys spontaneously</p>\n<p>This primarily exists for testing purposes.</p>',
        '<div class="docblock"><p>主动更新流量密钥</p>\n<p>该方法主要为了测试目的而存在。</p>',
    ),
    # 23. export_keying_material (3 paragraphs)
    (
        '<div class="docblock"><p>Derive keying material from this connection’s TLS session secrets.</p>\n<p>When both peers call this method with the same <code>label</code> and <code>context</code>\narguments and <code>output</code> buffers of equal length, they will get the\nsame sequence of bytes in <code>output</code>. These bytes are cryptographically\nstrong and pseudorandom, and are suitable for use as keying material.</p>\n<p>See <a href="https://tools.ietf.org/html/rfc5705">RFC5705</a> for more information.</p>',
        '<div class="docblock"><p>从该连接的 TLS 会话密钥中派生密钥材料。</p>\n<p>当两端使用相同的 <code>label</code>、<code>context</code> 参数以及等长的 <code>output</code> 缓冲区来调用本方法时，它们将在 <code>output</code> 中得到相同的字节序列。这些字节具有密码学强度且是伪随机的，适合直接用作密钥材料。</p>\n<p>更多信息请参阅 <a href="https://tools.ietf.org/html/rfc5705">RFC5705</a>。</p>',
    ),
    # 24. set_max_concurrent_uni_streams (2 paragraphs)
    (
        '<div class="docblock"><p>Modify the number of remotely initiated unidirectional streams that may be concurrently open</p>\n<p>No streams may be opened by the peer unless fewer than <code>count</code> are already open. Large\n<code>count</code>s increase both minimum and worst-case memory consumption.</p>',
        '<div class="docblock"><p>修改对端发起的、可以同时处于打开状态的单向流数量上限</p>\n<p>只有当已经打开的对端单向流数量少于 <code>count</code> 时，对端才能再打开新的流。较大的 <code>count</code> 会同时提高最小内存占用和最坏情况下的内存占用。</p>',
    ),
    # 25. set_send_window
    (
        '<div class="docblock"><p>See <a href="struct.TransportConfig.html#method.send_window" title="method quinn::TransportConfig::send_window"><code>proto::TransportConfig::send_window()</code></a></p>',
        '<div class="docblock"><p>参见 <a href="struct.TransportConfig.html#method.send_window" title="method quinn::TransportConfig::send_window"><code>proto::TransportConfig::send_window()</code></a></p>',
    ),
    # 26. set_receive_window
    (
        '<div class="docblock"><p>See <a href="struct.TransportConfig.html#method.receive_window" title="method quinn::TransportConfig::receive_window"><code>proto::TransportConfig::receive_window()</code></a></p>',
        '<div class="docblock"><p>参见 <a href="struct.TransportConfig.html#method.receive_window" title="method quinn::TransportConfig::receive_window"><code>proto::TransportConfig::receive_window()</code></a></p>',
    ),
    # 27. set_max_concurrent_bi_streams (2 paragraphs)
    (
        '<div class="docblock"><p>Modify the number of remotely initiated bidirectional streams that may be concurrently open</p>\n<p>No streams may be opened by the peer unless fewer than <code>count</code> are already open. Large\n<code>count</code>s increase both minimum and worst-case memory consumption.</p>',
        '<div class="docblock"><p>修改对端发起的、可以同时处于打开状态的双向流数量上限</p>\n<p>只有当已经打开的对端双向流数量少于 <code>count</code> 时，对端才能再打开新的流。较大的 <code>count</code> 会同时提高最小内存占用和最坏情况下的内存占用。</p>',
    ),
]


def main():
    with open(PATH, 'r', encoding='utf-8') as f:
        c = f.read()

    found = 0
    missed = []
    for old, new in TRANSLATIONS:
        if old in c:
            c = c.replace(old, new)
            found += 1
        else:
            missed.append(old[:80])

    with open(PATH, 'w', encoding='utf-8') as f:
        f.write(c)

    cjk = re.findall(r'[一-鿿]', c)
    print(f'Found: {found}/{len(TRANSLATIONS)} docblocks')
    print(f'CJK: {len(cjk)}')
    if missed:
        print('Missed:')
        for m in missed:
            print(f'  {m!r}')


if __name__ == '__main__':
    main()