"""quinn 第 3 阶段：翻译剩余 53 个 trait docblock

剩余的：
- Deref::deref / DerefMut::deref_mut
- Decoder::decode / Encoder::encode
- TryFrom::try_from: Performs the conversion.
- SystemTime::now
- Runtime trait methods (spawn, new_timer, wrap_udp_socket)
- congestion control: on_sent, on_end_acks, on_mtu_update, window, metrics,
  clone_box, initial_window, into_any, build
- 还有一些杂项
"""
import os
import re
import subprocess

PAIRS = [
    # Deref
    ('Dereferences the value.', '解引用此值。'),
    ('Mutably dereferences the value.', '以可变方式解引用此值。'),

    # Decoder / Encoder (tokio_util::codec 或 quinn 自定义)
    ('Decode a Self from the provided buffer, if the buffer is large enough',
     '如果缓冲区足够大，则从提供的缓冲区解码一个 Self'),
    ('Append the encoding of self to the provided buffer',
     '将 self 的编码追加到提供的缓冲区'),

    # TryFrom
    ('Performs the conversion.', '执行转换。'),

    # SystemTime::now
    ('Get SystemTime::now() or the mocked equivalent',
     '获取 SystemTime::now() 或其模拟等价物'),

    # Runtime trait methods
    ('Construct a timer that will expire at i',
     '构造一个将在指定时间过期的定时器'),
    ('Drive future to completion in the background',
     '在后台驱动 Future 完成'),
    ('Convert t into the socket type used by this runtime',
     '将 t 转换为此运行时使用的套接字类型'),

    # congestion Controller trait
    ('One or more packets were just sent',
     '刚发送了一个或多个数据包'),
    ('Packets are acked in batches, all with the same now argument. This indicates one of those batches has completed.',
     '数据包以批量形式被确认，所有包使用相同的 now 参数。这表示其中某一批已完成。'),
    ('The known MTU for the current network path has been updated',
     '当前网络路径的已知 MTU 已更新'),
    ('Number of ack-eliciting bytes that may be in flight',
     '处于飞行中的可触发 ACK 的字节数'),
    ('Retrieve implementation-specific metrics used to populate qlog traces when they are enabled',
     '检索实现特有的指标，用于在启用 qlog 时填充追踪记录'),
    ('Duplicate the controller\'s state',
     '复制此控制器的状态'),
    ('Initial congestion window',
     '初始拥塞窗口'),
    ('Returns Self for use in down-casting to extract implementation details',
     '返回 Self，用于向下转型以提取实现细节'),
    ('Construct a fresh Controller',
     '构造一个新的 Controller'),

    # 各 Bbr/Cubic/Controller 共通
    ('Number of ack-eliciting packets that may be in flight',
     '处于飞行中的可触发 ACK 的数据包数'),

    # generic "Construct a" patterns
    ('Construct a fresh Controller from this configuration',
     '从此配置构造一个新的 Controller'),

    # 默认值
    ('Returns the default value',
     '返回默认值'),
]


def apply_pairs(text):
    applied = []
    for en, zh in PAIRS:
        if en in text:
            text = text.replace(en, zh)
            applied.append(en[:60])
    # Read more 也再处理一遍
    if '>Read more</a>' in text:
        count = text.count('>Read more</a>')
        text = text.replace('>Read more</a>', '>更多信息</a>')
        applied.append(f'Read more x {count}')
    return text, applied


total = 0
modified = 0
for root, dirs, fs in os.walk('quinn'):
    for fn in fs:
        if not fn.endswith('.html'):
            continue
        path = os.path.join(root, fn)
        with open(path, 'rb') as f:
            before = f.read().decode('utf-8')
        after, applied = apply_pairs(before)
        if after != before:
            with open(path, 'wb') as f:
                f.write(after.encode('utf-8'))
            modified += 1
            total += len(applied)

print(f'Modified {modified} files, {total} replacements')

# 再 audit
result = subprocess.run(['python', '_common_tools/comprehensive_audit.py', 'quinn', 'quinn'],
                       capture_output=True, text=True)
for line in result.stdout.split('\n')[:30]:
    print(line)