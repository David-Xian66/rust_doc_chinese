"""Translate 7 untranslated docblocks in quinn/struct.Transmit.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/struct.Transmit.html'

TRANSLATIONS = [
    ('<p>The socket this datagram should be sent to</p>',
     '<p>该数据报应发送到的套接字</p>'),
    ('<p>Explicit congestion notification bits to set on the packet</p>',
     '<p>在该包上设置的显式拥塞通知位</p>'),
    ('<p>Amount of data written to the caller-supplied buffer</p>',
     '<p>已写入调用方提供的缓冲区的数据量</p>'),
    ('<p>The segment size if this transmission contains multiple datagrams.\nThis is <code>None</code> if the transmit only contains a single datagram</p>',
     '<p>若本次传输包含多个数据报，则为分段大小。若本次传输仅包含单个数据报，则为 <code>None</code>。</p>'),
    ('<p>Optional source IP address for the datagram</p>',
     '<p>该数据报的可选源 IP 地址</p>'),
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