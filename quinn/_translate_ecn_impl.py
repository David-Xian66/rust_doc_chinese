"""Translate 7 untranslated docblocks in quinn/enum.EcnCodepoint.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/enum.EcnCodepoint.html'

TRANSLATIONS = [
    ('<p>The ECT(0) codepoint, indicating that an endpoint is ECN-capable</p>',
     '<p>ECT(0) 码点，表示端点具备 ECN 能力</p>'),
    ('<p>The ECT(1) codepoint, indicating that an endpoint is ECN-capable</p>',
     '<p>ECT(1) 码点，表示端点具备 ECN 能力</p>'),
    ('<p>The CE codepoint, signalling that congestion was experienced</p>',
     '<p>CE 码点，表示已发生拥塞</p>'),
    ('<p>Create new object from the given bits</p>',
     '<p>由给定的位创建一个新对象</p>'),
    ('<p>Returns whether the codepoint is a CE, signalling that congestion was experienced</p>',
     '<p>返回该码点是否为 CE，即是否已发生拥塞</p>'),
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