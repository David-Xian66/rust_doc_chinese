"""Translate 5 untranslated docblocks in quinn/crypto/trait.PacketKey.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/crypto/trait.PacketKey.html'

TRANSLATIONS = [
    ('<p>Encrypt the packet payload with the given packet number</p>',
     '<p>使用给定的包号加密包的有效负载</p>'),
    ('<p>Decrypt the packet payload with the given packet number</p>',
     '<p>使用给定的包号解密包的有效负载</p>'),
    ('<p>The length of the AEAD tag appended to packets on encryption</p>',
     '<p>加密时附加在包后的 AEAD tag 的长度</p>'),
    ('<p>Maximum number of packets that may be sent using a single key</p>',
     '<p>单个密钥最多可用于发送的包数量</p>'),
    ('<p>Maximum number of incoming packets that may fail decryption before the connection must be\nabandoned</p>',
     '<p>在连接被迫放弃之前，最多可允许解密失败的入站包数量</p>'),
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