"""Translate 4 untranslated docblocks in quinn/crypto/rustls/struct.HandshakeData.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/crypto/rustls/struct.HandshakeData.html'

TRANSLATIONS = [
    ('<p>The negotiated application protocol, if ALPN is in use</p>\n<p>Guaranteed to be set if a nonempty list of protocols was specified for this connection.</p>',
     '<p>已协商的应用层协议（若启用了 ALPN）</p>\n<p>只要为该连接指定了非空的协议列表，该字段就保证被设置。</p>'),
    ('<p>The server name specified by the client, if any</p>\n<p>Always <code>None</code> for outgoing connections</p>',
     '<p>由客户端指定的服务器名称（如有）</p>\n<p>对于出站连接，该值始终为 <code>None</code></p>'),
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