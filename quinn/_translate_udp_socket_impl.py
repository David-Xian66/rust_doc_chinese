"""Translate 7 untranslated docblocks in quinn/trait.AsyncUdpSocket.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/trait.AsyncUdpSocket.html'

TRANSLATIONS = [
    ('<p>Create a <a href="trait.UdpPoller.html" title="trait quinn::UdpPoller"><code>UdpPoller</code></a> that can register a single task for write-readiness notifications</p>\n<p>A <code>poll_send</code> method on a single object can usually store only one <a href="https://doc.rust-lang.org/1.95.0/core/task/wake/struct.Waker.html" title="struct core::task::wake::Waker"><code>Waker</code></a> at a time,\ni.e. allow at most one caller to wait for an event. This method allows any number of\ninterested tasks to construct their own <a href="trait.UdpPoller.html" title="trait quinn::UdpPoller"><code>UdpPoller</code></a> object. They can all then wait for the\nsame event and be notified concurrently, because each <a href="trait.UdpPoller.html" title="trait quinn::UdpPoller"><code>UdpPoller</code></a> can store a separate\n<a href="https://doc.rust-lang.org/1.95.0/core/task/wake/struct.Waker.html" title="struct core::task::wake::Waker"><code>Waker</code></a>.</p>',
     '<p>创建一个 <a href="trait.UdpPoller.html" title="trait quinn::UdpPoller"><code>UdpPoller</code></a>，可以为一个任务注册“写就绪”通知</p>\n<p>单个对象上的 <code>poll_send</code> 方法通常一次只能保存一个 <a href="https://doc.rust-lang.org/1.95.0/core/task/wake/struct.Waker.html" title="struct core::task::wake::Waker"><code>Waker</code></a>，即最多允许一个调用者等待事件。本方法允许任意数量的感兴趣任务各自构造一个 <a href="trait.UdpPoller.html" title="trait quinn::UdpPoller"><code>UdpPoller</code></a> 对象，它们可以同时等待同一事件并被并发唤醒，因为每个 <a href="trait.UdpPoller.html" title="trait quinn::UdpPoller"><code>UdpPoller</code></a> 都可以独立存储一个 <a href="https://doc.rust-lang.org/1.95.0/core/task/wake/struct.Waker.html" title="struct core::task::wake::Waker"><code>Waker</code></a>。</p>'),
    ('<p>Send UDP datagrams from <code>transmits</code>, or return <code>WouldBlock</code> and clear the underlying\nsocket’s readiness, or return an I/O error</p>\n<p>If this returns <a href="https://doc.rust-lang.org/1.95.0/std/io/error/enum.ErrorKind.html#variant.WouldBlock" title="variant std::io::error::ErrorKind::WouldBlock"><code>io::ErrorKind::WouldBlock</code></a>, <a href="trait.UdpPoller.html#tymethod.poll_writable" title="method quinn::UdpPoller::poll_writable"><code>UdpPoller::poll_writable</code></a> must be called\nto register the calling task to be woken when a send should be attempted again.</p>',
     '<p>从 <code>transmits</code> 发送 UDP 数据报；若不能立即发送则返回 <code>WouldBlock</code> 并清除底层套接字的就绪状态；若出错则返回 I/O 错误</p>\n<p>若返回 <a href="https://doc.rust-lang.org/1.95.0/std/io/error/enum.ErrorKind.html#variant.WouldBlock" title="variant std::io::error::ErrorKind::WouldBlock"><code>io::ErrorKind::WouldBlock</code></a>，则必须调用 <a href="trait.UdpPoller.html#tymethod.poll_writable" title="method quinn::UdpPoller::poll_writable"><code>UdpPoller::poll_writable</code></a>，以便在可以再次尝试发送时唤醒当前任务。</p>'),
    ('<p>Receive UDP datagrams, or register to be woken if receiving may succeed in the future</p>',
     '<p>接收 UDP 数据报，若当前无法接收则注册任务以便后续可能被唤醒</p>'),
    ('<p>Look up the local IP address and port used by this socket</p>',
     '<p>查询该套接字所使用的本地 IP 地址与端口</p>'),
    ('<p>Maximum number of datagrams that a <a href="../quinn_udp/struct.Transmit.html" title="struct quinn_udp::Transmit"><code>Transmit</code></a> may encode</p>',
     '<p>一个 <a href="../quinn_udp/struct.Transmit.html" title="struct quinn_udp::Transmit"><code>Transmit</code></a> 最多可承载的数据报数量</p>'),
    ('<p>Maximum number of datagrams that might be described by a single <a href="../quinn_udp/struct.RecvMeta.html" title="struct quinn_udp::RecvMeta"><code>RecvMeta</code></a></p>',
     '<p>单个 <a href="../quinn_udp/struct.RecvMeta.html" title="struct quinn_udp::RecvMeta"><code>RecvMeta</code></a> 最多可描述的数据报数量</p>'),
    ('<p>Whether datagrams might get fragmented into multiple parts</p>\n<p>Sockets should prevent this for best performance. See e.g. the <code>IPV6_DONTFRAG</code> socket\noption.</p>',
     '<p>数据报是否可能被拆分为多个片段</p>\n<p>为获得最佳性能，套接字应避免这种情况。可参考 <code>IPV6_DONTFRAG</code> 套接字选项。</p>'),
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