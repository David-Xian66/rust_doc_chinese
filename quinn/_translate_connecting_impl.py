"""Translate 6 untranslated docblocks in quinn/struct.Connecting.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/struct.Connecting.html'

TRANSLATIONS = [
    ('<p>Convert into a 0-RTT or 0.5-RTT connection at the cost of weakened security</p>\n<p>Returns <code>Ok</code> immediately if the local endpoint is able to attempt sending 0/0.5-RTT data.\nIf so, the returned <a href="struct.Connection.html" title="struct quinn::Connection"><code>Connection</code></a> can be used to send application data without waiting for\nthe rest of the handshake to complete, at the cost of weakened cryptographic security\nguarantees. The returned <a href="struct.ZeroRttAccepted.html" title="struct quinn::ZeroRttAccepted"><code>ZeroRttAccepted</code></a> future resolves when the handshake does\ncomplete, at which point subsequently opened streams and written data will have full\ncryptographic protection.</p>\n<h6 id="outgoing"><a class="doc-anchor" href="#outgoing">§</a>Outgoing</h6>\n<p>For outgoing connections, the initial attempt to convert to a <a href="struct.Connection.html" title="struct quinn::Connection"><code>Connection</code></a> which sends\n0-RTT data will proceed if the <a href="crypto/trait.ClientConfig.html" title="trait quinn::crypto::ClientConfig"><code>crypto::ClientConfig</code></a>\nattempts to resume a previous TLS session. However, <strong>the remote endpoint may not actually\n<em>accept</em> the 0-RTT data</strong>–yet still accept the connection attempt in general. This\npossibility is conveyed through the <a href="struct.ZeroRttAccepted.html" title="struct quinn::ZeroRttAccepted"><code>ZeroRttAccepted</code></a> future–when the handshake\ncompletes, it resolves to true if the 0-RTT data was accepted and false if it was rejected.\nIf it was rejected, the existence of streams opened and other application data sent prior\nto the handshake completing will not be conveyed to the remote application, and local\noperations on them will return <code>ZeroRttRejected</code> errors.</p>\n<p>A server may reject 0-RTT data at its discretion, but accepting 0-RTT data requires the\nrelevant resumption state to be stored in the server, which servers may limit or lose for\nvarious reasons including not persisting resumption state across server restarts.</p>\n<p>If manually providing a <a href="crypto/trait.ClientConfig.html" title="trait quinn::crypto::ClientConfig"><code>crypto::ClientConfig</code></a>, check your\nimplementation’s docs for 0-RTT pitfalls.</p>\n<h6 id="incoming"><a class="doc-anchor" href="#incoming">§</a>Incoming</h6>\n<p>For incoming connections, conversion to 0.5-RTT will always fully succeed. <code>into_0rtt</code> will\nalways return <code>Ok</code> and the <a href="struct.ZeroRttAccepted.html" title="struct quinn::ZeroRttAccepted"><code>ZeroRttAccepted</code></a> will always resolve to true.</p>\n<p>If manually providing a <a href="crypto/trait.ServerConfig.html" title="trait quinn::crypto::ServerConfig"><code>crypto::ServerConfig</code></a>, check your\nimplementation’s docs for 0-RTT pitfalls.</p>\n<h6 id="security"><a class="doc-anchor" href="#security">§</a>Security</h6>\n<p>On outgoing connections, this enables transmission of 0-RTT data, which is vulnerable to\nreplay attacks, and should therefore never invoke non-idempotent operations.</p>\n<p>On incoming connections, this enables transmission of 0.5-RTT data, which may be sent\nbefore TLS client authentication has occurred, and should therefore not be used to send\ndata for which client authentication is being used.</p>',
     '<p>以牺牲一定的安全性为代价，转换为一个 0-RTT 或 0.5-RTT 连接</p>\n<p>若本地端点能够尝试发送 0/0.5-RTT 数据，本方法会立即返回 <code>Ok</code>。返回的 <a href="struct.Connection.html" title="struct quinn::Connection"><code>Connection</code></a> 可用于在握手完成之前发送应用数据，代价是密码学安全保证被削弱。返回的 <a href="struct.ZeroRttAccepted.html" title="struct quinn::ZeroRttAccepted"><code>ZeroRttAccepted</code></a> future 在握手完成时求解，此后新打开的流与新写入的数据将获得完整的密码学保护。</p>\n<h6 id="outgoing"><a class="doc-anchor" href="#outgoing">§</a>出站连接</h6>\n<p>对于出站连接，若 <a href="crypto/trait.ClientConfig.html" title="trait quinn::crypto::ClientConfig"><code>crypto::ClientConfig</code></a> 尝试恢复之前的 TLS 会话，则初次将连接转换为发送 0-RTT 数据的 <a href="struct.Connection.html" title="struct quinn::Connection"><code>Connection</code></a> 的尝试会进行下去。然而，<strong>远端实际可能并不会<em>接受</em>这些 0-RTT 数据</strong>，但仍会接受此次连接尝试。这种可能性通过 <a href="struct.ZeroRttAccepted.html" title="struct quinn::ZeroRttAccepted"><code>ZeroRttAccepted</code></a> future 表达——握手完成时，若 0-RTT 数据被接受则解析为 true，被拒绝则解析为 false。若被拒绝，在握手完成之前已打开的流与已发送的应用数据不会传达给远端应用，且本地的相关操作将返回 <code>ZeroRttRejected</code> 错误。</p>\n<p>服务器可以自行决定是否拒绝 0-RTT 数据；而接受 0-RTT 数据则要求服务器保存相应的恢复状态，服务器可能出于各种原因对恢复状态进行限制或丢失，包括不跨服务器重启持久化恢复状态。</p>\n<p>若自行提供 <a href="crypto/trait.ClientConfig.html" title="trait quinn::crypto::ClientConfig"><code>crypto::ClientConfig</code></a>，请查阅其实现文档中关于 0-RTT 的注意事项。</p>\n<h6 id="incoming"><a class="doc-anchor" href="#incoming">§</a>入站连接</h6>\n<p>对于入站连接，转换为 0.5-RTT 总能完全成功。<code>into_0rtt</code> 始终返回 <code>Ok</code>，且 <a href="struct.ZeroRttAccepted.html" title="struct quinn::ZeroRttAccepted"><code>ZeroRttAccepted</code></a> 始终解析为 true。</p>\n<p>若自行提供 <a href="crypto/trait.ServerConfig.html" title="trait quinn::crypto::ServerConfig"><code>crypto::ServerConfig</code></a>，请查阅其实现文档中关于 0-RTT 的注意事项。</p>\n<h6 id="security"><a class="doc-anchor" href="#security">§</a>安全性</h6>\n<p>对于出站连接，此方法启用 0-RTT 数据的发送，而 0-RTT 数据容易遭受重放攻击，因此永远不应触发非幂等操作。</p>\n<p>对于入站连接，此方法启用 0.5-RTT 数据的发送，这类数据可能在 TLS 客户端认证完成之前就已发出，因此不应发送依赖客户端认证才可信的数据。</p>'),
    ('<p>Parameters negotiated during the handshake</p>\n<p>The dynamic type returned is determined by the configured\n<a href="crypto/trait.Session.html" title="trait quinn::crypto::Session"><code>Session</code></a>. For the default <code>rustls</code> session, the return value can\nbe <a href="https://doc.rust-lang.org/1.95.0/alloc/boxed/struct.Box.html#method.downcast" title="method alloc::boxed::Box::downcast"><code>downcast</code></a> to a\n<a href="crypto/rustls/struct.HandshakeData.html" title="struct quinn::crypto::rustls::HandshakeData"><code>crypto::rustls::HandshakeData</code></a>.</p>',
     '<p>握手期间协商出的参数</p>\n<p>返回值的动态类型由所配置的 <a href="crypto/trait.Session.html" title="trait quinn::crypto::Session"><code>Session</code></a> 决定。对于默认的 <code>rustls</code> 会话，返回值可以 <a href="https://doc.rust-lang.org/1.95.0/alloc/boxed/struct.Box.html#method.downcast" title="method alloc::boxed::Box::downcast"><code>downcast</code></a> 为 <a href="crypto/rustls/struct.HandshakeData.html" title="struct quinn::crypto::rustls::HandshakeData"><code>crypto::rustls::HandshakeData</code></a>。</p>'),
    ('<p>The local IP address which was used when the peer established\nthe connection</p>\n<p>This can be different from the address the endpoint is bound to, in case\nthe endpoint is bound to a wildcard address like <code>0.0.0.0</code> or <code>::</code>.</p>\n<p>This will return <code>None</code> for clients, or when the platform does not expose this\ninformation. See <a href="../quinn_udp/struct.RecvMeta.html#structfield.dst_ip" title="field quinn_udp::RecvMeta::dst_ip"><code>quinn_udp::RecvMeta::dst_ip</code></a> for a list of\nsupported platforms when using <a href="../quinn_udp/index.html" title="mod quinn_udp"><code>quinn_udp</code></a> for I/O, which is the default.</p>\n<p>Will panic if called after <code>poll</code> has returned <code>Ready</code>.</p>',
     '<p>对端建立连接时所使用的本地 IP 地址</p>\n<p>当端点绑定到通配地址（如 <code>0.0.0.0</code> 或 <code>::</code>）时，该地址可能与端点所绑定的地址不同。</p>\n<p>对客户端或当平台未暴露此信息时返回 <code>None</code>。使用 <a href="../quinn_udp/index.html" title="mod quinn_udp"><code>quinn_udp</code></a>（默认）作为 I/O 时，支持的平台列表请参阅 <a href="../quinn_udp/struct.RecvMeta.html#structfield.dst_ip" title="field quinn_udp::RecvMeta::dst_ip"><code>quinn_udp::RecvMeta::dst_ip</code></a>。</p>\n<p>若在 <code>poll</code> 返回 <code>Ready</code> 之后调用会 panic。</p>'),
    ('<p>The peer’s UDP address</p>\n<p>Will panic if called after <code>poll</code> has returned <code>Ready</code>.</p>',
     '<p>对端的 UDP 地址</p>\n<p>若在 <code>poll</code> 返回 <code>Ready</code> 之后调用会 panic。</p>'),
    ('</h4></section></summary><div class="docblock"><p>Returns the argument unchanged.</p>',
     '</h4></section></summary><div class="docblock"><p>原样返回该参数。</p>'),
    ('<p>Calls <code>U::from(self)</code>.</p>\n<p>That is, this conversion is whatever the implementation of\n<code><a href="https://doc.rust-lang.org/1.95.0/core/convert/trait.From.html" title="trait core::convert::From">From</a>&lt;T&gt; for U</code> chooses to do.</p>',
     '<p>调用 <code>U::from(self)</code>。</p>\n<p>也就是说，此转换行为完全由\n<code><a href="https://doc.rust-lang.org/1.95.0/core/convert/trait.From.html" title="trait core::convert::From">From</a>&lt;T&gt; for U</code> 的实现决定。</p>'),
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
        print('Missed docblocks:')
        for m in missed:
            print(f'  {m!r}')


if __name__ == '__main__':
    main()