"""Translate 10 untranslated docblocks in quinn/congestion/trait.Controller.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/congestion/trait.Controller.html'

TRANSLATIONS = [
    ('<p>Packets were deemed lost or marked congested</p>\n<p><code>in_persistent_congestion</code> indicates whether all packets sent within the persistent\ncongestion threshold period ending when the most recent packet in this batch was sent were\nlost.\n<code>lost_bytes</code> indicates how many bytes were lost. This value will be 0 for ECN triggers.</p>',
     '<p>数据包被判定为丢失或被标记为拥塞</p>\n<p><code>in_persistent_congestion</code> 表示在该批次中最近一个包发送之前“持续拥塞阈值”时间段内发送的所有包是否都已丢失。<code>lost_bytes</code> 表示丢失的字节数。对于 ECN 触发，该值为 0。</p>'),
    ('<p>The known MTU for the current network path has been updated</p>',
     '<p>当前网络路径的已知 MTU 已更新</p>'),
    ('<p>Number of ack-eliciting bytes that may be in flight</p>',
     '<p>允许处于飞行中的可触发 ACK 的字节数</p>'),
    ('<p>Duplicate the controller’s state</p>',
     '<p>复制一份本控制器状态</p>'),
    ('<p>Initial congestion window</p>',
     '<p>初始拥塞窗口</p>'),
    ('<p>Returns Self for use in down-casting to extract implementation details</p>',
     '<p>返回 Self，供向下转型以提取实现细节使用</p>'),
    ('<p>One or more packets were just sent</p>',
     '<p>刚刚发送了一个或多个包</p>'),
    ('<p>Packet deliveries were confirmed</p>\n<p><code>app_limited</code> indicates whether the connection was blocked on outgoing\napplication data prior to receiving these acknowledgements.</p>',
     '<p>数据包的送达已得到确认</p>\n<p><code>app_limited</code> 表示在收到这些确认之前，连接是否因外发应用数据而被阻塞。</p>'),
    ('<p>Packets are acked in batches, all with the same <code>now</code> argument. This indicates one of those batches has completed.</p>',
     '<p>包以批次的形式被确认，每个批次使用同一个 <code>now</code> 参数。此方法表示其中某个批次已处理完毕。</p>'),
    ('<p>Retrieve implementation-specific metrics used to populate <code>qlog</code> traces when they are enabled</p>',
     '<p>获取实现特有的指标，用于在启用 <code>qlog</code> trace 时填充相关字段</p>'),
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