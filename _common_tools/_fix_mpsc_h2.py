"""修复 tokio/sync/mpsc/index.html 中漏译的 h2 章节标题 + div.warning 提示。

用户原报告的 6 处漏译：
  1. <h2 id="disconnection">Disconnection</h2> → 断开连接
  2. <h2 id="clean-shutdown">Clean Shutdown</h2> → 优雅关闭
  3. <h2 id="communicating-between-sync-and-async-code">Communicating between sync and async code</h2> → 同步与异步代码之间的通信
  4. <h2 id="multiple-runtimes">Multiple runtimes</h2> → 多个 runtime
  5. <h2 id="allocation-behavior">Allocation behavior</h2> → 内存分配行为
  6. <div class="warning">The implementation details described in this section may change in future\nTokio releases.</div> → 本节所述的实现细节在未来的 Tokio 版本中可能发生变化。

使用 bytes 模式保留 CRLF。
"""
import sys
import os

PATH = 'tokio/sync/mpsc/index.html'

# (h2_id_or_marker, en_text, zh_text)
H2_PAIRS = [
    ('disconnection', 'Disconnection', '断开连接'),
    ('clean-shutdown', 'Clean Shutdown', '优雅关闭'),
    ('communicating-between-sync-and-async-code',
     'Communicating between sync and async code', '同步与异步代码之间的通信'),
    ('multiple-runtimes', 'Multiple runtimes', '多个 runtime'),
    ('allocation-behavior', 'Allocation behavior', '内存分配行为'),
]

# 警告提示（注意：源文件是 div.warning，文本跨行）
WARNING_OLD = b'<div class="warning">The implementation details described in this section may change in future\r\nTokio releases.</div>'
WARNING_NEW = '<div class="warning">本节所述的实现细节在未来的 Tokio 版本中可能发生变化。</div>'.encode('utf-8')


def main():
    if not os.path.isfile(PATH):
        print(f'Not found: {PATH}')
        return 1

    with open(PATH, 'rb') as f:
        raw = f.read()

    changed = 0
    for hid, en, zh in H2_PAIRS:
        # <h2 id="hid"><a class="doc-anchor" href="#hid">§</a>EN_TEXT</h2>
        old = f'<h2 id="{hid}"><a class="doc-anchor" href="#{hid}">§</a>{en}</h2>'.encode('utf-8')
        new = f'<h2 id="{hid}"><a class="doc-anchor" href="#{hid}">§</a>{zh}</h2>'.encode('utf-8')
        if old in raw:
            raw = raw.replace(old, new)
            print(f'  [h2-{hid}] translated: {en!r} -> {zh!r}')
            changed += 1
        else:
            print(f'  [h2-{hid}] NOT FOUND: {en!r}')

    # 处理 div.warning
    if WARNING_OLD in raw:
        raw = raw.replace(WARNING_OLD, WARNING_NEW)
        print('  [div.warning] translated')
        changed += 1
    else:
        # Try with just LF (in case CRLF was normalized)
        warn_lf = b'<div class="warning">The implementation details described in this section may change in future\nTokio releases.</div>'
        if warn_lf in raw:
            raw = raw.replace(warn_lf, WARNING_NEW)
            print('  [div.warning] translated (LF form)')
            changed += 1
        else:
            print('  [div.warning] NOT FOUND')

    if changed == 0:
        print('No changes made.')
        return 1

    with open(PATH, 'wb') as f:
        f.write(raw)
    print(f'\nWrote {PATH} ({changed} changes)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
