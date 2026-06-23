"""Re-attempt the 3 files that didn't match the first pass."""

import os
import re

BASE = 'D:/Administrator/Documents/Code/rust_doc_all/quinn'

# ConnectionId.html — exact raw bytes contain U+2019
CID_OLD = ('<p>This method uses a closure to create new values. If you\xe2\x80\x99d rather\n'
           '<a href="https://doc.rust-lang.org/1.95.0/core/clone/trait.Clone.html" title="trait core::clone::Clone"><code>Clone</code></a> a given value, use <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.fill" title="method slice::fill"><code>fill</code></a>. If you want to use the <a href="https://doc.rust-lang.org/1.95.0/core/default/trait.Default.html" title="trait core::default::Default"><code>Default</code></a>\n'
           'trait to generate values, you can pass <a href="https://doc.rust-lang.org/1.95.0/core/default/trait.Default.html#tymethod.default" title="associated function core::default::Default::default"><code>Default::default</code></a> as the\n'
           'argument.</p>')
CID_NEW = ('<p>该方法使用闭包创建新值。若你更希望 <a href="https://doc.rust-lang.org/1.95.0/core/clone/trait.Clone.html" title="trait core::clone::Clone"><code>Clone</code></a> 一个给定的值，请使用 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.fill" title="method slice::fill"><code>fill</code></a>。若你希望借助 <a href="https://doc.rust-lang.org/1.95.0/core/default/trait.Default.html" title="trait core::default::Default"><code>Default</code></a> trait 来生成值，可以将 <a href="https://doc.rust-lang.org/1.95.0/core/default/trait.Default.html#tymethod.default" title="associated function core::default::Default::default"><code>Default::default</code></a> 作为参数传入。</p>')

# RetryError.html — title is "struct quinn::Incoming"
RETRY_OLD = '<p>Get the <a href="struct.Incoming.html" title="struct quinn::Incoming"><code>Incoming</code></a></p>'
RETRY_NEW = '<p>获取 <a href="struct.Incoming.html" title="struct quinn::Incoming"><code>Incoming</code></a></p>'

# ServerConfig.html — both paragraphs together
SRV_OLD = ('<p>An <a href="../quinn_proto/endpoint/struct.Incoming.html" title="struct quinn_proto::endpoint::Incoming"><code>Incoming</code></a> comes into existence when an incoming connection attempt\n'
           'is received and stops existing when the application either accepts it or otherwise disposes\n'
           'of it. This limit governs only packets received within that period, and does not include\n'
           'the first packet. Packets received in excess of this limit are dropped, which may cause\n'
           '0-RTT or handshake data to have to be retransmitted.</p>\n'
           '<p>The default value is set to 100 MiB\xef\xbf\xbdCa generous amount that still prevents memory\n'
           'exhaustion in most contexts.</p>')
SRV_NEW = ('<p>当收到一个入站连接尝试时，会创建一个 <a href="../quinn_proto/endpoint/struct.Incoming.html" title="struct quinn_proto::endpoint::Incoming"><code>Incoming</code></a>，并在该连接被应用层接受或以其他方式处置后消失。该限制仅作用于这段时间内收到的包，\n'
           '且不包括第一个包。超出此限制的包将被丢弃，这可能导致 0-RTT 或握手数据需要重传。</p>\n'
           '<p>默认值为 100 MiB——这一较为宽裕的数值在大多数情况下足以防止内存耗尽。</p>')


def main():
    for rel, old, new in [
        ('struct.ConnectionId.html', CID_OLD, CID_NEW),
        ('struct.RetryError.html', RETRY_OLD, RETRY_NEW),
        ('struct.ServerConfig.html', SRV_OLD, SRV_NEW),
    ]:
        path = os.path.join(BASE, rel)
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        if old in c:
            c = c.replace(old, new)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(c)
            cjk = re.findall(r'[一-鿿]', c)
            print(f'  {rel}: OK CJK={len(cjk)}')
        else:
            print(f'  {rel}: NOT FOUND')
            # 尝试找出实际差异
            # 在 ServerConfig 中尝试单独匹配第一段
            if rel == 'struct.ServerConfig.html':
                part1 = old.split('\n')[0]
                print(f'    part1 in c: {part1 in c}')
                part2 = '<p>The default value is set to 100 MiB'
                print(f'    part2 prefix in c: {part2 in c}')
                idx = c.find(part2)
                if idx > 0:
                    print(f'    around part2: {c[idx:idx+100]!r}')


if __name__ == '__main__':
    main()