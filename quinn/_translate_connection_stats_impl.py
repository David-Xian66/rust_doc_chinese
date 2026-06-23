"""Translate 8 untranslated docblocks in quinn/struct.ConnectionStats.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/struct.ConnectionStats.html'

TRANSLATIONS = [
    ('Non-exhaustive structs could have additional fields added in future. Therefore, non-exhaustive structs cannot be constructed in external crates using the traditional <code>Struct { .. }</code> syntax; cannot be matched against without a wildcard <code>..</code>; and struct update syntax will not work.',
     '非穷尽结构体将来可能添加额外的字段。因此，外部 crate 不能使用传统的 <code>Struct { .. }</code> 语法构造非穷尽结构体；进行模式匹配时必须包含通配 <code>..</code>；结构体更新语法也无法使用。'),
    ('<p>Statistics about UDP datagrams transmitted on a connection</p>',
     '<p>关于该连接上发送的 UDP 数据报的统计信息</p>'),
    ('<p>Statistics about UDP datagrams received on a connection</p>',
     '<p>关于该连接上接收的 UDP 数据报的统计信息</p>'),
    ('<p>Statistics about frames transmitted on a connection</p>',
     '<p>关于该连接上发送的帧的统计信息</p>'),
    ('<p>Statistics about frames received on a connection</p>',
     '<p>关于该连接上接收的帧的统计信息</p>'),
    ('<p>Statistics related to the current transmission path</p>',
     '<p>与当前传输路径相关的统计信息</p>'),
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