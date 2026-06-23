"""Translate 5 untranslated docblocks in quinn/struct.ValidationTokenConfig.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/struct.ValidationTokenConfig.html'

TRANSLATIONS = [
    ('<p>Duration after an address validation token was issued for which it’s considered valid</p>\n<p>This refers only to tokens sent in NEW_TOKEN frames, in contrast to retry tokens.</p>\n<p>Defaults to 2 weeks.</p>',
     '<p>一个地址校验 token 自签发起被认为有效的持续时间</p>\n<p>这里仅指通过 NEW_TOKEN 帧发送的 token，不包括 retry token。</p>\n<p>默认为 2 周。</p>'),
    ('<p>Set a custom <a href="trait.TokenLog.html" title="trait quinn::TokenLog"><code>TokenLog</code></a></p>\n<p>If the <code>bloom</code> feature is enabled (which it is by default), defaults to a default\n<a href="struct.BloomTokenLog.html" title="struct quinn::BloomTokenLog"><code>BloomTokenLog</code></a>, which is suitable for most internet applications.</p>\n<p>If the <code>bloom</code> feature is disabled, defaults to <a href="struct.NoneTokenLog.html" title="struct quinn::NoneTokenLog"><code>NoneTokenLog</code></a>,\nwhich makes the server ignore all address validation tokens (that is, tokens originating\nfrom NEW_TOKEN frames–retry tokens are not affected).</p>',
     '<p>设置自定义的 <a href="trait.TokenLog.html" title="trait quinn::TokenLog"><code>TokenLog</code></a></p>\n<p>若启用了 <code>bloom</code> feature（默认启用），默认为一个内置的 <a href="struct.BloomTokenLog.html" title="struct quinn::BloomTokenLog"><code>BloomTokenLog</code></a>，适用于大多数互联网应用。</p>\n<p>若禁用了 <code>bloom</code> feature，则默认为 <a href="struct.NoneTokenLog.html" title="struct quinn::NoneTokenLog"><code>NoneTokenLog</code></a>，它会使服务器忽略所有地址校验 token（即源自 NEW_TOKEN 帧的 token；retry token 不受影响）。</p>'),
    ('<p>Number of address validation tokens sent to a client when its path is validated</p>\n<p>This refers only to tokens sent in NEW_TOKEN frames, in contrast to retry tokens.</p>\n<p>If the <code>bloom</code> feature is enabled (which it is by default), defaults to 2. Otherwise,\ndefaults to 0.</p>',
     '<p>在客户端路径校验通过时发送给它的地址校验 token 数量</p>\n<p>这里仅指通过 NEW_TOKEN 帧发送的 token，不包括 retry token。</p>\n<p>若启用了 <code>bloom</code> feature（默认启用），默认为 2；否则默认为 0。</p>'),
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