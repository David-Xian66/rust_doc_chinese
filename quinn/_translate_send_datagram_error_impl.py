"""Translate 5 untranslated docblocks in quinn/enum.SendDatagramError.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/enum.SendDatagramError.html'

TRANSLATIONS = [
    ('<p>The peer does not support receiving datagram frames</p>',
     '<p>对端不支持接收 datagram 帧</p>'),
    ('<p>Datagram support is disabled locally</p>',
     '<p>datagram 支持在本地被禁用</p>'),
    ('<p>The datagram is larger than the connection can currently accommodate</p>\n<p>Indicates that the path MTU minus overhead or the limit advertised by the peer has been\nexceeded.</p>',
     '<p>该 datagram 大于连接当前能够承载的大小</p>\n<p>表示已超出路径 MTU 减去协议开销后的值，或对端所通告的限制。</p>'),
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