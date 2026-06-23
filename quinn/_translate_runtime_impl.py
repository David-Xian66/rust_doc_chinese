"""Translate 4 untranslated docblocks in quinn/trait.Runtime.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/trait.Runtime.html'

TRANSLATIONS = [
    ('<p>Construct a timer that will expire at <code>i</code></p>',
     '<p>构造一个将在 <code>i</code> 时刻触发的定时器</p>'),
    ('<p>Drive <code>future</code> to completion in the background</p>',
     '<p>在后台将 <code>future</code> 驱动至完成</p>'),
    ('<p>Convert <code>t</code> into the socket type used by this runtime</p>',
     '<p>将 <code>t</code> 转换为本运行时所使用的套接字类型</p>'),
    ('<p>Look up the current time</p>\n<p>Allows simulating the flow of time for testing.</p>',
     '<p>查询当前时间</p>\n<p>允许在测试中模拟时间的流逝。</p>'),
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