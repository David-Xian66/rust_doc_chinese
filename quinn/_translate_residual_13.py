"""Translate 13 residual untranslated <p> blocks found by strict audit v2."""

import os
import re

BASE = 'D:/Administrator/Documents/Code/rust_doc_all/quinn'

JOBS = [
    # enum.ReadExactError.html
    (
        'enum.ReadExactError.html',
        [
            ('<p>A read error occurred</p>',
             '<p>发生了读取错误</p>'),
        ],
    ),
    # enum.SendDatagramError.html
    (
        'enum.SendDatagramError.html',
        [
            ('<p>The connection was lost</p>',
             '<p>连接已丢失</p>'),
        ],
    ),
    # enum.Side.html
    (
        'enum.Side.html',
        [
            ('<p>Shorthand for <code>self == Side::Server</code></p>',
             '<p>即 <code>self == Side::Server</code> 的简写</p>'),
        ],
    ),
    # struct.ConnectionId.html — fill_with
    (
        'struct.ConnectionId.html',
        [
            ('<p>This method uses a closure to create new values. If you��d rather\n<a href="https://doc.rust-lang.org/1.95.0/core/clone/trait.Clone.html" title="trait core::clone::Clone"><code>Clone</code></a> a given value, use <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.fill" title="method slice::fill"><code>fill</code></a>. If you want to use the <a href="https://doc.rust-lang.org/1.95.0/core/default/trait.Default.html" title="trait core::default::Default"><code>Default</code></a>\ntrait to generate values, you can pass <a href="https://doc.rust-lang.org/1.95.0/core/default/trait.Default.html#tymethod.default" title="associated function core::default::Default::default"><code>Default::default</code></a> as the\nargument.</p>',
             '<p>该方法使用闭包创建新值。若你更希望 <a href="https://doc.rust-lang.org/1.95.0/core/clone/trait.Clone.html" title="trait core::clone::Clone"><code>Clone</code></a> 一个给定的值，请使用 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.fill" title="method slice::fill"><code>fill</code></a>。若你希望借助 <a href="https://doc.rust-lang.org/1.95.0/core/default/trait.Default.html" title="trait core::default::Default"><code>Default</code></a> trait 来生成值，可以将 <a href="https://doc.rust-lang.org/1.95.0/core/default/trait.Default.html#tymethod.default" title="associated function core::default::Default::default"><code>Default::default</code></a> 作为参数传入。</p>'),
        ],
    ),
    # struct.RetryError.html
    (
        'struct.RetryError.html',
        [
            ('<p>Get the <a href="struct.Incoming.html" title="quinn::Incoming"><code>Incoming</code></a></p>',
             '<p>获取 <a href="struct.Incoming.html" title="quinn::Incoming"><code>Incoming</code></a></p>'),
        ],
    ),
    # struct.ServerConfig.html — incoming_buffer_size_total (2 paragraphs)
    (
        'struct.ServerConfig.html',
        [
            ('<p>An <a href="../quinn_proto/endpoint/struct.Incoming.html" title="struct quinn_proto::endpoint::Incoming"><code>Incoming</code></a> comes into existence when an incoming connection attempt\nis received and stops existing when the application either accepts it or otherwise disposes\nof it. This limit governs only packets received within that period, and does not include\nthe first packet. Packets received in excess of this limit are dropped, which may cause\n0-RTT or handshake data to have to be retransmitted.</p>\n<p>The default value is set to 100 MiB\xaca generous amount that still prevents memory\nexhaustion in most contexts.</p>',
             '<p>当收到一个入站连接尝试时，会创建一个 <a href="../quinn_proto/endpoint/struct.Incoming.html" title="struct quinn_proto::endpoint::Incoming"><code>Incoming</code></a>，并在该连接被应用层接受或以其他方式处置后消失。该限制仅作用于这段时间内收到的包，\n且不包括第一个包。超出此限制的包将被丢弃，这可能导致 0-RTT 或握手数据需要重传。</p>\n<p>默认值为 100 MiB——在大多数情况下，这一较为宽裕的数值足以防止内存耗尽。</p>'),
        ],
    ),
    # struct.TokenMemoryCache.html
    (
        'struct.TokenMemoryCache.html',
        [
            ('<p>Construct empty</p>',
             '<p>构造一个空的实例</p>'),
        ],
    ),
    # congestion/struct.ControllerMetrics.html
    (
        'congestion/struct.ControllerMetrics.html',
        [
            ('<p>Pacing rate (bits/s)</p>',
             '<p>节奏发送速率（比特/秒）</p>'),
        ],
    ),
    # congestion/trait.ControllerFactory.html
    (
        'congestion/trait.ControllerFactory.html',
        [
            ('<p>Construct a fresh <code>Controller</code></p>',
             '<p>构造一个新的 <code>Controller</code></p>'),
        ],
    ),
    # crypto/struct.KeyPair.html — structfield.remote
    (
        'crypto/struct.KeyPair.html',
        [
            ('<p>Key for decrypting data</p>',
             '<p>用于解密数据的密钥</p>'),
        ],
    ),
    # crypto/struct.Keys.html — structfield.packet
    (
        'crypto/struct.Keys.html',
        [
            ('<p>Packet protection keys</p>',
             '<p>包保护密钥</p>'),
        ],
    ),
    # crypto/trait.HandshakeTokenKey.html
    (
        'crypto/trait.HandshakeTokenKey.html',
        [
            ('<p>Derive AEAD using hkdf</p>',
             '<p>使用 HKDF 派生 AEAD</p>'),
        ],
    ),
]


def main():
    total = 0
    for rel, pairs in JOBS:
        path = os.path.join(BASE, rel)
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        orig = c
        for old, new in pairs:
            if old in c:
                c = c.replace(old, new)
        if c != orig:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(c)
            total += 1
            cjk = re.findall(r'[一-鿿]', c)
            print(f'  {rel}: CJK={len(cjk)}')
    print(f'Updated {total} files')


if __name__ == '__main__':
    main()