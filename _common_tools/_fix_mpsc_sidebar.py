"""修复 tokio/sync/mpsc/index.html 中 sidebar TOC 链接里的英文。

侧边栏 <a href="#disconnection" title="Disconnection">Disconnection</a>
要同时改 title 与 link 文本为中文。
"""
import sys
import os

PATH = 'tokio/sync/mpsc/index.html'

# (anchor, en_text, zh_text)
PAIRS = [
    ('disconnection', 'Disconnection', '断开连接'),
    ('clean-shutdown', 'Clean Shutdown', '优雅关闭'),
    ('communicating-between-sync-and-async-code',
     'Communicating between sync and async code', '同步与异步代码之间的通信'),
    ('multiple-runtimes', 'Multiple runtimes', '多个 runtime'),
    ('allocation-behavior', 'Allocation behavior', '内存分配行为'),
]


def main():
    if not os.path.isfile(PATH):
        print(f'Not found: {PATH}')
        return 1

    with open(PATH, 'rb') as f:
        raw = f.read()

    changed = 0
    for anchor, en, zh in PAIRS:
        # Sidebar TOC entry: <a href="#anchor" title="EN">EN</a>
        old = f'<a href="#{anchor}" title="{en}">{en}</a>'.encode('utf-8')
        new = f'<a href="#{anchor}" title="{zh}">{zh}</a>'.encode('utf-8')
        if old in raw:
            raw = raw.replace(old, new)
            print(f'  [{anchor}] sidebar translated')
            changed += 1
        else:
            print(f'  [{anchor}] NOT FOUND in sidebar')

    if changed == 0:
        print('No changes made.')
        return 1

    with open(PATH, 'wb') as f:
        f.write(raw)
    print(f'\nWrote {PATH} ({changed} changes)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
