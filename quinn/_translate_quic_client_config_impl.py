"""Translate 3 untranslated docblocks in quinn/crypto/rustls/struct.QuicClientConfig.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/crypto/rustls/struct.QuicClientConfig.html'

TRANSLATIONS = [
    ('<p>Initialize a QUIC-compatible TLS client configuration with a separate initial cipher suite</p>\n<p>This is useful if you want to avoid the initial cipher suite for traffic encryption.</p>',
     '<p>使用单独的初始密码套件初始化一个兼容 QUIC 的 TLS 客户端配置</p>\n<p>当你希望避免将初始密码套件用于业务流量加密时，这很有用。</p>'),
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