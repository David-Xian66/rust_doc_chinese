"""Translate all impl-section docblocks in quinn/struct.ServerConfig.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/struct.ServerConfig.html'

TRANSLATIONS = [
    # 1. Transport configuration struct field
    ('<p>Transport configuration to use for incoming connections</p>',
     '<p>用于入站连接的传输配置</p>'),
    # 2. crypto field
    ('<p>TLS configuration used for incoming connections</p>\n<p>Must be set to use TLS 1.3 only.</p>',
     '<p>用于入站连接的 TLS 配置</p>\n<p>必须设置为仅使用 TLS 1.3。</p>'),
    # 3. validation_token field
    ('<p>Configuration for sending and handling validation tokens</p>',
     '<p>用于发送和处理验证令牌（validation token）的配置</p>'),
    # 4. handshake_token_key method
    ('<p>Create a default config with a particular handshake token key</p>',
     '<p>使用指定的握手令牌密钥创建一个默认配置</p>'),
    # 5. transport_config
    ('<p>Set a custom <a href="struct.TransportConfig.html" title="struct quinn::TransportConfig"><code>TransportConfig</code></a></p>',
     '<p>设置自定义的 <a href="struct.TransportConfig.html" title="struct quinn::TransportConfig"><code>TransportConfig</code></a></p>'),
    # 6. validation_token_config
    ('<p>Set a custom <a href="struct.ValidationTokenConfig.html" title="struct quinn::ValidationTokenConfig"><code>ValidationTokenConfig</code></a></p>',
     '<p>设置自定义的 <a href="struct.ValidationTokenConfig.html" title="struct quinn::ValidationTokenConfig"><code>ValidationTokenConfig</code></a></p>'),
    # 7. token_key
    ('<p>Private key used to authenticate data included in handshake tokens</p>',
     '<p>用于认证握手令牌中所包含数据的私钥</p>'),
    # 8. retry_token_lifetime
    ('<p>Duration after a retry token was issued for which it’s considered valid</p>\n<p>Defaults to 15 seconds.</p>',
     '<p>重试令牌在签发后被视为有效的时长</p>\n<p>默认为 15 秒。</p>'),
    # 9. migration
    ('<p>Whether to allow clients to migrate to new addresses</p>\n<p>Improves behavior for clients that move between different internet connections or suffer NAT\nrebinding. Enabled by default.</p>',
     '<p>是否允许客户端迁移到新的地址</p>\n<p>可改善在切换网络连接或遭遇 NAT 重绑时客户端的行为。默认开启。</p>'),
    # 10. preferred_address_v4
    ('<p>The preferred IPv4 address that will be communicated to clients during handshaking</p>\n<p>If the client is able to reach this address, it will switch to it.</p>',
     '<p>在握手期间将向客户端通告的优先 IPv4 地址</p>\n<p>若客户端能到达该地址，便会切换到该地址。</p>'),
    # 11. preferred_address_v6
    ('<p>The preferred IPv6 address that will be communicated to clients during handshaking</p>\n<p>If the client is able to reach this address, it will switch to it.</p>',
     '<p>在握手期间将向客户端通告的优先 IPv6 地址</p>\n<p>若客户端能到达该地址，便会切换到该地址。</p>'),
    # 12. max_incoming
    ('<p>Maximum number of <a href="../quinn_proto/endpoint/struct.Incoming.html" title="struct quinn_proto::endpoint::Incoming"><code>Incoming</code></a> to allow to exist at a time</p>\n<p>An <a href="../quinn_proto/endpoint/struct.Incoming.html" title="struct quinn_proto::endpoint::Incoming"><code>Incoming</code></a> comes into existence when an incoming connection attempt\nis received and stops existing when the application either accepts it or otherwise disposes\nof it. While this limit is reached, new incoming connection attempts are immediately\nrefused. Larger values have greater worst-case memory consumption, but accommodate greater\napplication latency in handling incoming connection attempts.</p>\n<p>The default value is set to 65536. With a typical Ethernet MTU of 1500 bytes, this limits\nmemory consumption from this to under 100 MiB–a generous amount that still prevents memory\nexhaustion in most contexts.</p>',
     '<p>同时允许存在的 <a href="../quinn_proto/endpoint/struct.Incoming.html" title="struct quinn_proto::endpoint::Incoming"><code>Incoming</code></a> 数量上限</p>\n<p>当服务端收到入站连接尝试时，会创建一个 <a href="../quinn_proto/endpoint/struct.Incoming.html" title="struct quinn_proto::endpoint::Incoming"><code>Incoming</code></a>；当应用程序接受该连接或以其他方式处理掉它时，<code>Incoming</code> 即消失。达到此上限后，新的入站连接尝试将被立即拒绝。该值越大最坏情况下的内存占用越高，但允许应用程序以更大的延迟处理入站连接尝试。</p>\n<p>默认值为 65536。以典型的 1500 字节以太网 MTU 计算，这会把该部分内存占用控制在 100 MiB 以内——在大多数场景下既慷慨又能防止内存耗尽。</p>'),
    # 13. incoming_buffer_size
    ('<p>Maximum number of received bytes to buffer for each <a href="../quinn_proto/endpoint/struct.Incoming.html" title="struct quinn_proto::endpoint::Incoming"><code>Incoming</code></a></p>\n<p>An <a href="../quinn_proto/endpoint/struct.Incoming.html" title="struct quinn_proto::endpoint::Incoming"><code>Incoming</code></a> comes into existence when an incoming connection attempt\nis received and stops existing when the application either accepts it or otherwise disposes\nof it. This limit governs only packets received within that period, and does not include\nthe first packet. Packets received in excess of this limit are dropped, which may cause\n0-RTT or handshake data to have to be retransmitted.</p>\n<p>The default value is set to 10 MiB–an amount such that in most situations a client would\nnot transmit that much 0-RTT data faster than the server handles the corresponding\n<a href="../quinn_proto/endpoint/struct.Incoming.html" title="struct quinn_proto::endpoint::Incoming"><code>Incoming</code></a>.</p>',
     '<p>为每个 <a href="../quinn_proto/endpoint/struct.Incoming.html" title="struct quinn_proto::endpoint::Incoming"><code>Incoming</code></a> 缓冲的已接收字节数上限</p>\n<p>当服务端收到入站连接尝试时，会创建一个 <a href="../quinn_proto/endpoint/struct.Incoming.html" title="struct quinn_proto::endpoint::Incoming"><code>Incoming</code></a>；当应用程序接受该连接或以其他方式处理掉它时，<code>Incoming</code> 即消失。该上限仅约束此期间内收到的数据包，不包括第一个包。超过此限制的数据包将被丢弃，可能导致 0-RTT 或握手数据需要重传。</p>\n<p>默认值为 10 MiB——在大多数情况下，客户端在服务端处理相应 <a href="../quinn_proto/endpoint/struct.Incoming.html" title="struct quinn_proto::endpoint::Incoming"><code>Incoming</code></a> 之前不会发送这么多 0-RTT 数据。</p>'),
    # 14. incoming_buffer_total (likely uses different text — search)
    ('<p>Maximum number of received bytes to buffer for all <a href="../quinn_proto/endpoint/struct.Incoming.html" title="struct quinn_proto::endpoint::Incoming"><code>Incoming</code></a>\ncollectively</p>',
     '<p>为所有 <a href="../quinn_proto/endpoint/struct.Incoming.html" title="struct quinn_proto::endpoint::Incoming"><code>Incoming</code></a> 合计缓冲的已接收字节数上限</p>'),
    # 15. time_source
    ('<p>Object to get current <a href="https://doc.rust-lang.org/1.95.0/std/time/struct.SystemTime.html" title="struct std::time::SystemTime"><code>SystemTime</code></a></p>\n<p>This exists to allow system time to be mocked in tests, or wherever else desired.</p>\n<p>Defaults to <a href="struct.StdSystemTime.html" title="struct quinn::StdSystemTime"><code>StdSystemTime</code></a>, which simply calls <a href="https://doc.rust-lang.org/1.95.0/std/time/struct.SystemTime.html#method.now" title="associated function std::time::SystemTime::now"><code>SystemTime::now()</code></a>.</p>',
     '<p>用于获取当前 <a href="https://doc.rust-lang.org/1.95.0/std/time/struct.SystemTime.html" title="struct std::time::SystemTime"><code>SystemTime</code></a> 的对象</p>\n<p>提供此设置是为了在测试或其他需要时能够模拟系统时间。</p>\n<p>默认为 <a href="struct.StdSystemTime.html" title="struct quinn::StdSystemTime"><code>StdSystemTime</code></a>，后者直接调用 <a href="https://doc.rust-lang.org/1.95.0/std/time/struct.SystemTime.html#method.now" title="associated function std::time::SystemTime::now"><code>SystemTime::now()</code></a>。</p>'),
    # 16. with_single_cert (impl - this version may not exist; verify later)
    ('<p>Create a server config with the given certificate chain to be presented to clients</p>\n<p>Uses a randomized handshake token key.</p>',
     '<p>使用给定的证书链创建一个服务器配置，该证书链将向客户端出示</p>\n<p>使用一个随机生成的握手令牌密钥。</p>'),
    # 17. with_crypto
    ('<p>Create a server config with the given <a href="crypto/trait.ServerConfig.html" title="trait quinn::crypto::ServerConfig"><code>crypto::ServerConfig</code></a></p>\n<p>Uses a randomized handshake token key.</p>',
     '<p>使用给定的 <a href="crypto/trait.ServerConfig.html" title="trait quinn::crypto::ServerConfig"><code>crypto::ServerConfig</code></a> 创建一个服务器配置</p>\n<p>使用一个随机生成的握手令牌密钥。</p>'),
    # 18. From impl (boilerplate)
    ('<p>Returns the argument unchanged.</p>',
     '<p>原样返回该参数。</p>'),
    # 19. From impl - other variant
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
