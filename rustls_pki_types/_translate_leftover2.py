"""rustls_pki_types 第二轮补译：处理含 <code> 和 <a> 内嵌的 <p>"""
import os
import re

PAIRS = [
    # variant.Io: 含 <code>std::io</code>
    ('I/O errors, from APIs that accept <code>std::io</code> types.',
     'I/O 错误，来自接受 <code>std::io</code> 类型的 API。'),

    # variant.EchConfigList: 含 <a href>
    ('An EchConfigList structure, as specified in\r\n<a href="https://www.ietf.org/archive/id/draft-farrell-tls-pemesni-05.html">https://www.ietf.org/archive/id/draft-farrell-tls-pemesni-05.html</a>.',
     '一个 EchConfigList 结构，如\r\n<a href="https://www.ietf.org/archive/id/draft-farrell-tls-pemesni-05.html">https://www.ietf.org/archive/id/draft-farrell-tls-pemesni-05.html</a> 所规定。'),
    ('An EchConfigList structure, as specified in\n<a href="https://www.ietf.org/archive/id/draft-farrell-tls-pemesni-05.html">https://www.ietf.org/archive/id/draft-farrell-tls-pemesni-05.html</a>.',
     '一个 EchConfigList 结构，如\n<a href="https://www.ietf.org/archive/id/draft-farrell-tls-pemesni-05.html">https://www.ietf.org/archive/id/draft-farrell-tls-pemesni-05.html</a> 所规定。'),

    # method.into: 含 <code><a href>From</a>&lt;T&gt; for U</code>
    ('That is, this conversion is whatever the implementation of\r\n<code><a href="https://doc.rust-lang.org/1.95.0/core/convert/trait.From.html" title="trait core::convert::From">From</a>&lt;T&gt; for U</code> chooses to do.',
     '即此转换的实际行为取决于\r\n<code><a href="https://doc.rust-lang.org/1.95.0/core/convert/trait.From.html" title="trait core::convert::From">From</a>&lt;T&gt; for U</code> 的实现。'),
    ('That is, this conversion is whatever the implementation of\n<code><a href="https://doc.rust-lang.org/1.95.0/core/convert/trait.From.html" title="trait core::convert::From">From</a>&lt;T&gt; for U</code> chooses to do.',
     '即此转换的实际行为取决于\n<code><a href="https://doc.rust-lang.org/1.95.0/core/convert/trait.From.html" title="trait core::convert::From">From</a>&lt;T&gt; for U</code> 的实现。'),
]


def apply(text):
    applied = []
    for en, zh in PAIRS:
        if en in text:
            text = text.replace(en, zh)
            applied.append(en[:80])
    return text, applied


total = 0
mod = 0
per_file = {}
for root, dirs, fs in os.walk('rustls_pki_types'):
    for fn in fs:
        if not fn.endswith('.html'):
            continue
        path = os.path.join(root, fn)
        with open(path, 'rb') as f:
            before = f.read().decode('utf-8')
        after, applied = apply(before)
        if after != before:
            with open(path, 'wb') as f:
                f.write(after.encode('utf-8'))
            mod += 1
            total += len(applied)
            per_file[os.path.relpath(path, 'rustls_pki_types')] = applied

print(f'Modified {mod} files, {total} replacements')
for f in sorted(per_file):
    print(f'\n{f}:')
    for a in per_file[f]:
        print(f'  - {a}')