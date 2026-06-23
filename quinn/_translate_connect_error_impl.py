"""Translate 8 untranslated docblocks in quinn/enum.ConnectError.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/enum.ConnectError.html'

TRANSLATIONS = [
    ('<p>The endpoint can no longer create new connections</p>\n<p>Indicates that a necessary component of the endpoint has been dropped or otherwise disabled.</p>',
     '<p>端点无法再创建新连接</p>\n<p>表示端点的某个必要组件已被丢弃或被禁用。</p>'),
    ('<p>The connection could not be created because not enough of the CID space is available</p>\n<p>Try using longer connection IDs</p>',
     '<p>由于可用的 CID 空间不足，无法创建连接</p>\n<p>可尝试使用更长的连接 ID</p>'),
    ('<p>The given server name was malformed</p>',
     '<p>给定的服务器名称格式错误</p>'),
    ('<p>The remote <a href="https://doc.rust-lang.org/1.95.0/core/net/socket_addr/enum.SocketAddr.html" title="enum core::net::socket_addr::SocketAddr"><code>SocketAddr</code></a> supplied was malformed</p>\n<p>Examples include attempting to connect to port 0, or using an inappropriate address family.</p>',
     '<p>所提供的远端 <a href="https://doc.rust-lang.org/1.95.0/core/net/socket_addr/enum.SocketAddr.html" title="enum core::net::socket_addr::SocketAddr"><code>SocketAddr</code></a> 格式错误</p>\n<p>例如尝试连接 0 端口，或使用了不匹配的地址族。</p>'),
    ('<p>No default client configuration was set up</p>\n<p>Use <code>Endpoint::connect_with</code> to specify a client configuration.</p>',
     '<p>未设置默认的客户端配置</p>\n<p>请使用 <code>Endpoint::connect_with</code> 来指定一个客户端配置。</p>'),
    ('<p>The local endpoint does not support the QUIC version specified in the client configuration</p>',
     '<p>本地端点不支持客户端配置中指定的 QUIC 版本</p>'),
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