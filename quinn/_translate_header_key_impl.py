"""Translate 3 untranslated docblocks in quinn/crypto/trait.HeaderKey.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/crypto/trait.HeaderKey.html'

TRANSLATIONS = [
    ('<p>Decrypt the given packet’s header</p>',
     '<p>解密给定包的包头</p>'),
    ('<p>Encrypt the given packet’s header</p>',
     '<p>加密给定包的包头</p>'),
    ('<p>The sample size used for this key’s algorithm</p>',
     '<p>此密钥算法所使用的采样长度</p>'),
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