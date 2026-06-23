"""Translate 6 untranslated docblocks in quinn/struct.BloomTokenLog.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/struct.BloomTokenLog.html'

TRANSLATIONS = [
    ('<p>Construct with an approximate maximum memory usage and expected number of validation token\nusages per expiration period</p>\n<p>Calculates the optimal bloom filter k number automatically.</p>',
     '<p>使用一个近似最大内存占用以及每个过期周期内预期的校验 token 使用次数进行构造</p>\n<p>会自动计算出最优的布隆过滤器 k 值。</p>'),
    ('<p>Construct with an approximate maximum memory usage and a <a href="https://en.wikipedia.org/wiki/Bloom_filter">bloom filter k number</a></p>\n<p>If choosing a custom k number, note that <code>BloomTokenLog</code> always maintains two filters\nbetween them and divides the allocation budget of <code>max_bytes</code> evenly between them. As such,\neach bloom filter will contain <code>max_bytes * 4</code> bits.</p>',
     '<p>使用一个近似最大内存占用以及一个 <a href="https://en.wikipedia.org/wiki/Bloom_filter">布隆过滤器 k 值</a>进行构造</p>\n<p>若选择自定义 k 值，请注意 <code>BloomTokenLog</code> 始终同时维护两个过滤器，并将 <code>max_bytes</code> 的分配预算在两者之间平均分配。因此，每个布隆过滤器将包含 <code>max_bytes * 4</code> 个比特位。</p>'),
    ('<p>Default to 20 MiB max memory consumption and expected one million hits</p>',
     '<p>默认为最大 20 MiB 内存占用，并预期一百万次命中</p>'),
    ('<p>With the default validation token lifetime of 2 weeks, this corresponds to one token usage per\n1.21 seconds.</p>',
     '<p>在默认的 2 周校验 token 有效期内，这相当于每 1.21 秒使用一次 token。</p>'),
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