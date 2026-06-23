"""Translate 12 untranslated docblocks in quinn/struct.Incoming.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/struct.Incoming.html'

TRANSLATIONS = [
    ('<p>Attempt to accept this incoming connection (an error may still occur)</p>',
     '<p>尝试接受此入站连接（仍可能发生错误）</p>'),
    ('<p>Accept this incoming connection using a custom configuration</p>\n<p>See <a href="struct.Incoming.html#method.accept" title="method quinn::Incoming::accept"><code>accept()</code></a> for more details.</p>',
     '<p>使用自定义配置接受此入站连接</p>\n<p>详见 <a href="struct.Incoming.html#method.accept" title="method quinn::Incoming::accept"><code>accept()</code></a>。</p>'),
    ('<p>Reject this incoming connection attempt</p>',
     '<p>拒绝此次入站连接尝试</p>'),
    ('<p>Respond with a retry packet, requiring the client to retry with address validation</p>\n<p>Errors if <code>may_retry()</code> is false.</p>',
     '<p>回送一个 retry 包，要求客户端带地址校验后重试</p>\n<p>若 <code>may_retry()</code> 为 false，则会出错。</p>'),
    ('<p>Ignore this incoming connection attempt, not sending any packet in response</p>',
     '<p>忽略此次入站连接尝试，不回送任何包</p>'),
    ('<p>The local IP address which was used when the peer established the connection</p>',
     '<p>对端建立连接时所使用的本地 IP 地址</p>'),
    ('<p>The peer’s UDP address</p>',
     '<p>对端的 UDP 地址</p>'),
    ('<p>Whether the socket address that is initiating this connection has been validated</p>\n<p>This means that the sender of the initial packet has proved that they can receive traffic\nsent to <code>self.remote_address()</code>.</p>\n<p>If <code>self.remote_address_validated()</code> is false, <code>self.may_retry()</code> is guaranteed to be true.\nThe inverse is not guaranteed.</p>',
     '<p>发起此次连接的套接字地址是否已通过验证</p>\n<p>这表示初始包的发送者已证明自己能够接收发往 <code>self.remote_address()</code> 的数据。</p>\n<p>若 <code>self.remote_address_validated()</code> 为 false，则 <code>self.may_retry()</code> 一定为 true；反之则不一定。</p>'),
    ('<p>Whether it is legal to respond with a retry packet</p>\n<p>If <code>self.remote_address_validated()</code> is false, <code>self.may_retry()</code> is guaranteed to be true.\nThe inverse is not guaranteed.</p>',
     '<p>是否可以合法地回送 retry 包</p>\n<p>若 <code>self.remote_address_validated()</code> 为 false，则 <code>self.may_retry()</code> 一定为 true；反之则不一定。</p>'),
    ('<p>The original destination CID when initiating the connection</p>',
     '<p>发起该连接时使用的原始目标 CID</p>'),
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