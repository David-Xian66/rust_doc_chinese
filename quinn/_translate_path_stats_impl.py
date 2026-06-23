"""Translate 13 untranslated docblocks in quinn/struct.PathStats.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/struct.PathStats.html'

TRANSLATIONS = [
    ('Non-exhaustive structs could have additional fields added in future. Therefore, non-exhaustive structs cannot be constructed in external crates using the traditional <code>Struct { .. }</code> syntax; cannot be matched against without a wildcard <code>..</code>; and struct update syntax will not work.',
     '非穷尽结构体将来可能添加额外的字段。因此，外部 crate 不能使用传统的 <code>Struct { .. }</code> 语法构造非穷尽结构体；进行模式匹配时必须包含通配 <code>..</code>；结构体更新语法也无法使用。'),
    ('<p>Current best estimate of this connection’s latency (round-trip-time)</p>',
     '<p>该连接延迟（往返时间）的当前最佳估计值</p>'),
    ('<p>Current congestion window of the connection</p>',
     '<p>该连接当前的拥塞窗口</p>'),
    ('<p>Congestion events on the connection</p>',
     '<p>该连接上发生的拥塞事件数</p>'),
    ('<p>The amount of packets lost on this path</p>',
     '<p>在该路径上丢失的数据包数量</p>'),
    ('<p>The amount of bytes lost on this path</p>',
     '<p>在该路径上丢失的字节数</p>'),
    ('<p>The amount of packets sent on this path</p>',
     '<p>在该路径上发送的数据包数量</p>'),
    ('<p>The amount of PLPMTUD probe packets sent on this path (also counted by <code>sent_packets</code>)</p>',
     '<p>在该路径上发送的 PLPMTUD 探测包数量（也计入 <code>sent_packets</code>）</p>'),
    ('<p>The amount of PLPMTUD probe packets lost on this path (ignored by <code>lost_packets</code> and\n<code>lost_bytes</code>)</p>',
     '<p>在该路径上丢失的 PLPMTUD 探测包数量（不计入 <code>lost_packets</code> 与 <code>lost_bytes</code>）</p>'),
    ('<p>The number of times a black hole was detected in the path</p>',
     '<p>在该路径上检测到“黑洞”的次数</p>'),
    ('<p>Largest UDP payload size the path currently supports</p>',
     '<p>该路径当前支持的最大 UDP 有效负载大小</p>'),
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