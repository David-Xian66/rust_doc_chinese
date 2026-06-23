"""Translate 4 untranslated docblocks in quinn/enum.StoppedError.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/enum.StoppedError.html'

TRANSLATIONS = [
    ('<p>The connection was lost</p>',
     '<p>连接已丢失</p>'),
    ('<p>This was a 0-RTT stream and the server rejected it</p>\n<p>Can only occur on clients for 0-RTT streams, which can be opened using\n<a href="struct.Connecting.html#method.into_0rtt" title="method quinn::Connecting::into_0rtt"><code>Connecting::into_0rtt()</code></a>.</p>',
     '<p>该流为 0-RTT 流，但服务器拒绝了它</p>\n<p>仅对客户端的 0-RTT 流可能发生，可通过 <a href="struct.Connecting.html#method.into_0rtt" title="method quinn::Connecting::into_0rtt"><code>Connecting::into_0rtt()</code></a> 打开 0-RTT 流。</p>'),
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