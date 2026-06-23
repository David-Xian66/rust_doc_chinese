"""Translate 6 untranslated docblocks in quinn/struct.MtuDiscoveryConfig.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/struct.MtuDiscoveryConfig.html'

TRANSLATIONS = [
    ('<p>Specifies the time to wait after completing MTU discovery before starting a new MTU\ndiscovery run.</p>\n<p>Defaults to 600 seconds, as recommended by <a href="https://www.rfc-editor.org/rfc/rfc8899">RFC\n8899</a>.</p>',
     '<p>指定在完成 MTU 探测之后，需等待多长时间才会开启新一轮 MTU 探测。</p>\n<p>默认为 600 秒，符合 <a href="https://www.rfc-editor.org/rfc/rfc8899">RFC 8899</a> 的建议。</p>'),
    ('<p>Specifies the upper bound to the max UDP payload size that MTU discovery will search for.</p>\n<p>Defaults to 1452, to stay within Ethernet’s MTU when using IPv4 and IPv6. The highest\nallowed value is 65527, which corresponds to the maximum permitted UDP payload on IPv6.</p>\n<p>It is safe to use an arbitrarily high upper bound, regardless of the network path’s MTU. The\nonly drawback is that MTU discovery might take more time to finish.</p>',
     '<p>指定 MTU 探测所搜索的最大 UDP 有效负载大小的上限。</p>\n<p>默认为 1452，以保证在使用 IPv4 与 IPv6 时不超过以太网的 MTU。允许的最大值为 65527，对应 IPv6 上允许的最大 UDP 有效负载。</p>\n<p>无论实际网络路径的 MTU 如何，使用一个任意大的上限都是安全的，唯一的代价是 MTU 探测可能需要更长时间才能完成。</p>'),
    ('<p>Specifies the amount of time that MTU discovery should wait after a black hole was detected\nbefore running again. Defaults to one minute.</p>\n<p>Black hole detection can be spuriously triggered in case of congestion, so it makes sense to\ntry MTU discovery again after a short period of time.</p>',
     '<p>指定在检测到“黑洞”之后，MTU 探测需等待多长时间才会再次运行。默认为一分钟。</p>\n<p>在发生拥塞时，黑洞检测可能被误触发，因此在一段较短时间后再次尝试 MTU 探测是合理的。</p>'),
    ('<p>Specifies the minimum MTU change to stop the MTU discovery phase.\nDefaults to 20.</p>',
     '<p>指定用以终止 MTU 探测阶段的最小 MTU 变化量。默认为 20。</p>'),
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