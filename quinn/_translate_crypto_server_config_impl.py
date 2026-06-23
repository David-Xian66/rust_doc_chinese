"""Translate 3 untranslated docblocks in quinn/crypto/trait.ServerConfig.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/crypto/trait.ServerConfig.html'

TRANSLATIONS = [
    ('<p>Create the initial set of keys given the client’s initial destination ConnectionId</p>',
     '<p>根据客户端的初始目标 ConnectionId 创建初始密钥集合</p>'),
    ('<p>Generate the integrity tag for a retry packet</p>\n<p>Never called if <code>initial_keys</code> rejected <code>version</code>.</p>',
     '<p>为 retry 包生成完整性 tag</p>\n<p>若 <code>initial_keys</code> 拒绝了 <code>version</code>，则不会调用此方法。</p>'),
    ('<p>Start a server session with this configuration</p>\n<p>Never called if <code>initial_keys</code> rejected <code>version</code>.</p>',
     '<p>使用该配置启动一个服务器会话</p>\n<p>若 <code>initial_keys</code> 拒绝了 <code>version</code>，则不会调用此方法。</p>'),
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