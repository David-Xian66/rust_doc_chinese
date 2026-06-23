"""Stage 8 v4: replace text in docblocks using stripped-text detection.

Strategy:
1. Find each OWN trait method docblock.
2. Extract its inner HTML.
3. Strip HTML tags to get visible text.
4. If the stripped text starts with a known English prefix, replace the text
   nodes (preserving <a> tags) with the Chinese version.

This handles the complex HTML like '<a href="..."><code>Hasher</code></a>'.

We use BeautifulSoup-style logic without dependencies: walk through tags.
"""

import os
import re

BASE = 'D:/Administrator/Documents/Code/rust_doc_all/rustls_pki_types'

# Map: stripped-text-prefix (with leading context to disambiguate) -> Chinese replacement (with placeholders for inline tags)
# We use a different approach: find specific inner HTML patterns and replace.

# Patterns where the inner HTML contains ONLY text + <a> tags + optional <code>.
# We replace inner text nodes only, preserving <a>/<code> structure.

# Actually simpler: directly match known inner HTML snippets.
JOBS_RAW = [
    # Feeds this value into the given <a href="..."><code>Hasher</code></a>. <a href="...">Read more</a>
    (
        'Feeds this value into the given <a href="https://doc.rust-lang.org/1.95.0/core/hash/trait.Hasher.html" title="trait core::hash::Hasher"><code>Hasher</code></a>. <a href="https://doc.rust-lang.org/1.95.0/core/hash/trait.Hash.html#tymethod.hash">Read more</a>',
        '将该值送入给定的 <a href="https://doc.rust-lang.org/1.95.0/core/hash/trait.Hasher.html" title="trait core::hash::Hasher"><code>Hasher</code></a> 中。<a href="https://doc.rust-lang.org/1.95.0/core/hash/trait.Hash.html#tymethod.hash">更多信息</a>'
    ),
    # Feeds this value into the given <a href="..."><code>Hasher</code></a>.  (no Read more - if any)
    # Conversion from a PEM <a href="pem/enum.SectionKind.html" title="..."><code>SectionKind</code></a> and body data. <a href="pem/trait.PemObject.html#tymethod.from_pem">Read more</a>
    (
        'Conversion from a PEM <a href="pem/enum.SectionKind.html" title="enum rustls_pki_types::pem::SectionKind"><code>SectionKind</code></a> and body data. <a href="pem/trait.PemObject.html#tymethod.from_pem">Read more</a>',
        '从 PEM 的 <a href="pem/enum.SectionKind.html" title="enum rustls_pki_types::pem::SectionKind"><code>SectionKind</code></a> 与 body 数据进行转换。<a href="pem/trait.PemObject.html#tymethod.from_pem">更多信息</a>'
    ),
    # Decode the first section of this type from PEM read from an <a href="https://doc.rust-lang.org/.../std/io/trait.Read.html" ...><code>io::Read</code></a>.
    (
        'Decode the first section of this type from PEM read from an <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.Read.html" title="trait std::io::Read"><code>io::Read</code></a>.',
        '从某个 <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.Read.html" title="trait std::io::Read"><code>io::Read</code></a> 读取的 PEM 中，解码出本类型的第一个 section。'
    ),
    # Iterate over all sections of this type from PEM present in an <a href="..."><code>io::Read</code></a>.
    (
        'Iterate over all sections of this type from PEM present in an <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.Read.html" title="trait std::io::Read"><code>io::Read</code></a>.',
        '从某个 <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.Read.html" title="trait std::io::Read"><code>io::Read</code></a> 中的 PEM 数据里，迭代出本类型的所有 section。'
    ),
    # This method returns an <a href="..."><code>Ordering</code></a> between <code>self</code> and <code>other</code>. <a href="...">Read more</a>
    # Find this in raw
    (
        'This method returns an <a href="https://doc.rust-lang.org/1.95.0/core/cmp/enum.Ordering.html" title="enum core::cmp::Ordering"><code>Ordering</code></a> between <code>self</code> and <code>other</code>. <a href="https://doc.rust-lang.org/1.95.0/core/cmp/trait.Ord.html#tymethod.cmp">Read more</a>',
        '该方法返回 <code>self</code> 与 <code>other</code> 之间的 <a href="https://doc.rust-lang.org/1.95.0/core/cmp/enum.Ordering.html" title="enum core::cmp::Ordering"><code>Ordering</code></a>。<a href="https://doc.rust-lang.org/1.95.0/core/cmp/trait.Ord.html#tymethod.cmp">更多信息</a>'
    ),
]


def main():
    files = []
    for root, _, fs in os.walk(BASE):
        for f in fs:
            if f.endswith('.html'):
                files.append(os.path.join(root, f))

    n_files = 0
    n_total = 0
    for path in files:
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        orig = c
        n_this = 0
        for old, new in JOBS_RAW:
            if old in c:
                c = c.replace(old, new)
                n_this += 1
                n_total += 1
        if c != orig:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(c)
            n_files += 1
    print(f'Stage 8 v4: {n_files} files updated, {n_total} replacements')


if __name__ == '__main__':
    main()