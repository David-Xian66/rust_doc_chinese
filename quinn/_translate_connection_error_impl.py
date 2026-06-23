"""Translate 10 untranslated docblocks in quinn/enum.ConnectionError.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/enum.ConnectionError.html'

TRANSLATIONS = [
    ('<p>The peer doesn’t implement any supported version</p>',
     '<p>对端未实现任何受支持的版本</p>'),
    ('<p>The peer violated the QUIC specification as understood by this implementation</p>',
     '<p>对端违反了本实现所理解的 QUIC 规范</p>'),
    ('<p>The peer’s QUIC stack aborted the connection automatically</p>',
     '<p>对端的 QUIC 协议栈自动中止了连接</p>'),
    ('<p>The peer closed the connection</p>',
     '<p>对端关闭了连接</p>'),
    ('<p>The peer is unable to continue processing this connection, usually due to having restarted</p>',
     '<p>对端无法继续处理该连接，通常是因为已经重启</p>'),
    ('<p>Communication with the peer has lapsed for longer than the negotiated idle timeout</p>\n<p>If neither side is sending keep-alives, a connection will time out after a long enough idle\nperiod even if the peer is still reachable. See also <a href="struct.TransportConfig.html#method.max_idle_timeout" title="method quinn::TransportConfig::max_idle_timeout"><code>TransportConfig::max_idle_timeout()</code></a>\nand <a href="struct.TransportConfig.html#method.keep_alive_interval" title="method quinn::TransportConfig::keep_alive_interval"><code>TransportConfig::keep_alive_interval()</code></a>.</p>',
     '<p>与对端的通信空闲时间已超过协商的最大空闲超时</p>\n<p>即便对端仍可达，只要双方都不发送 keep-alive，连接在足够长的空闲期后仍会超时。另请参阅 <a href="struct.TransportConfig.html#method.max_idle_timeout" title="method quinn::TransportConfig::max_idle_timeout"><code>TransportConfig::max_idle_timeout()</code></a> 与 <a href="struct.TransportConfig.html#method.keep_alive_interval" title="method quinn::TransportConfig::keep_alive_interval"><code>TransportConfig::keep_alive_interval()</code></a>。</p>'),
    ('<p>The local application closed the connection</p>',
     '<p>本地应用程序关闭了连接</p>'),
    ('<p>The connection could not be created because not enough of the CID space is available</p>\n<p>Try using longer connection IDs.</p>',
     '<p>由于可用的 CID 空间不足，无法创建连接</p>\n<p>可尝试使用更长的连接 ID。</p>'),
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