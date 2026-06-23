"""Translate 11 untranslated docblocks in quinn/struct.VarInt.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/struct.VarInt.html'

TRANSLATIONS = [
    ('<p>The largest representable value</p>',
     '<p>可表示的最大值</p>'),
    ('<p>The largest encoded value length</p>',
     '<p>编码后的最大长度</p>'),
    ('<p>Construct a <code>VarInt</code> infallibly</p>',
     '<p>以不会失败的方式构造一个 <code>VarInt</code></p>'),
    ('<p>Succeeds iff <code>x</code> &lt; 2^62</p>',
     '<p>当且仅当 <code>x</code> &lt; 2^62 时成功</p>'),
    ('<p>Create a VarInt without ensuring it’s in range</p>\n<h5 id="safety"><a class="doc-anchor" href="#safety">§</a>Safety</h5>\n<p><code>x</code> must be less than 2^62.</p>',
     '<p>在不检查取值范围的情况下构造一个 <code>VarInt</code></p>\n<h5 id="safety"><a class="doc-anchor" href="#safety">§</a>安全性</h5>\n<p><code>x</code> 必须小于 2^62。</p>'),
    ('<p>Extract the integer value</p>',
     '<p>取出底层整数值</p>'),
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