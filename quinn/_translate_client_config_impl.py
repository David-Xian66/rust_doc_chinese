"""Translate 10 untranslated docblocks in quinn/struct.ClientConfig.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/struct.ClientConfig.html'

TRANSLATIONS = [
    ('<p>Create a default config with a particular cryptographic config</p>',
     '<p>使用特定的加密配置创建一个默认配置</p>'),
    ('<p>Configure how to populate the destination CID of the initial packet when attempting to\nestablish a new connection</p>\n<p>By default, it’s populated with random bytes with reasonable length, so unless you have\na good reason, you do not need to change it.</p>\n<p>When prefer to override the default, please note that the generated connection ID MUST be\nat least 8 bytes long and unpredictable, as per section 7.2 of RFC 9000.</p>',
     '<p>配置在尝试建立新连接时，如何填充初始包的目标 CID</p>\n<p>默认情况下，它会被填充为长度合适的随机字节，因此除非有合理理由，否则无需修改。</p>\n<p>若决定覆盖默认值，请注意根据 RFC 9000 第 7.2 节，所生成的连接 ID 必须至少 8 字节且不可预测。</p>'),
    ('<p>Set a custom <a href="struct.TransportConfig.html" title="struct quinn::TransportConfig"><code>TransportConfig</code></a></p>',
     '<p>设置一个自定义的 <a href="struct.TransportConfig.html" title="struct quinn::TransportConfig"><code>TransportConfig</code></a></p>'),
    ('<p>Set a custom <a href="trait.TokenStore.html" title="trait quinn::TokenStore"><code>TokenStore</code></a></p>\n<p>Defaults to <a href="struct.TokenMemoryCache.html" title="struct quinn::TokenMemoryCache"><code>TokenMemoryCache</code></a>, which is suitable for most internet applications.</p>',
     '<p>设置一个自定义的 <a href="trait.TokenStore.html" title="trait quinn::TokenStore"><code>TokenStore</code></a></p>\n<p>默认为 <a href="struct.TokenMemoryCache.html" title="struct quinn::TokenMemoryCache"><code>TokenMemoryCache</code></a>，适用于大多数互联网应用。</p>'),
    ('<p>Set the QUIC version to use</p>',
     '<p>设置要使用的 QUIC 版本</p>'),
    ('<p>Create a client configuration that trusts the platform’s native roots</p>',
     '<p>创建一个信任平台原生根证书的客户端配置</p>'),
    ('<p>Create a client configuration that trusts the platform’s native roots</p>',
     '<p>创建一个信任平台原生根证书的客户端配置</p>'),
    ('<p>Create a client configuration that trusts specified trust anchors</p>',
     '<p>创建一个信任指定信任锚的客户端配置</p>'),
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
            # The "platform's native roots" line appears in 2 places
            count = c.count(old)
            c = c.replace(old, new)
            found += count
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