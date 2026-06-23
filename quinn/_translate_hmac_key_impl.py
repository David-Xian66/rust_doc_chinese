"""Translate 3 untranslated docblocks in quinn/crypto/trait.HmacKey.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/crypto/trait.HmacKey.html'

TRANSLATIONS = [
    ('<p>Method for signing a message</p>',
     '<p>对消息进行签名的方法</p>'),
    ('<p>Length of <code>sign</code>’s output</p>',
     '<p><code>sign</code> 输出结果的长度</p>'),
    ('<p>Method for verifying a message</p>',
     '<p>验证消息的方法</p>'),
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