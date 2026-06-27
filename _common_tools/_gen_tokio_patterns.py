#!/usr/bin/env python3
"""Generate regex-based patterns for tokio untranslated dd blocks.

The challenge: many <dd> items contain HTML <code> and <a href="..."><code>X</code></a>
tags mixed with English description text. We want to translate the description but
preserve the HTML tags.

Strategy: For each <dd> block, identify the text nodes (text between HTML tags) and
translate them, leaving the tags intact.

Implementation:
1. Parse each <dd>...</dd> with BeautifulSoup (or simple regex)
2. Walk text nodes, translate them
3. Reassemble HTML

This script just GENERATES the dict of (raw_dd_text, translated_dd_text) pairs that
translate_module_descriptions.py can apply as byte-for-byte replacements.
"""
import json
import os
import re

# ====== Translation pairs for tokio dd content (preserving <code> tags) ======
# Each entry: (raw_english_dd_content, raw_chinese_dd_content)

PAIRS = [
    # === tokio/net/index.html ===
    # TcpSocket: A TCP socket that has not yet been converted to a <code>TcpStream</code> or
    # <code>TcpListener</code>.
    (
        'A TCP socket that has not yet been converted to a <code>TcpStream</code> or\r\n<code>TcpListener</code>.',
        '一个尚未转换为 <code>TcpStream</code> 或 <code>TcpListener</code> 的 TCP socket。',
    ),
    (
        'A TCP socket that has not yet been converted to a <code>TcpStream</code> or\n<code>TcpListener</code>.',
        '一个尚未转换为 <code>TcpStream</code> 或 <code>TcpListener</code> 的 TCP socket。',
    ),
    # ToSocketAddrs: Converts or resolves without blocking to one or more <code>SocketAddr</code> values.
    (
        'Converts or resolves without blocking to one or more <code>SocketAddr</code> values.',
        '非阻塞地转换或解析出一个或多个 <code>SocketAddr</code> 值。',
    ),

    # === tokio/net/tcp/index.html ===
    # OwnedReadHalf
    (
        'Owned read half of a <a href="../struct.TcpStream.html" title="struct tokio::net::TcpStream"><code>TcpStream</code></a>, created by <a href="../struct.TcpStream.html#method.into_split" title="method tokio::net::TcpStream::into_split"><code>into_split</code></a>.',
        '<a href="../struct.TcpStream.html" title="struct tokio::net::TcpStream"><code>TcpStream</code></a> 的 owned 读半部，由 <a href="../struct.TcpStream.html#method.into_split" title="method tokio::net::TcpStream::into_split"><code>into_split</code></a> 创建。',
    ),
    # OwnedWriteHalf
    (
        'Owned write half of a <a href="../struct.TcpStream.html" title="struct tokio::net::TcpStream"><code>TcpStream</code></a>, created by <a href="../struct.TcpStream.html#method.into_split" title="method tokio::net::TcpStream::into_split"><code>into_split</code></a>.',
        '<a href="../struct.TcpStream.html" title="struct tokio::net::TcpStream"><code>TcpStream</code></a> 的 owned 写半部，由 <a href="../struct.TcpStream.html#method.into_split" title="method tokio::net::TcpStream::into_split"><code>into_split</code></a> 创建。',
    ),
    # ReadHalf
    (
        'Borrowed read half of a <a href="../struct.TcpStream.html" title="struct tokio::net::TcpStream"><code>TcpStream</code></a>, created by <a href="../struct.TcpStream.html#method.split" title="method tokio::net::TcpStream::split"><code>split</code></a>.',
        '<a href="../struct.TcpStream.html" title="struct tokio::net::TcpStream"><code>TcpStream</code></a> 的 borrowed 读半部，由 <a href="../struct.TcpStream.html#method.split" title="method tokio::net::TcpStream::split"><code>split</code></a> 创建。',
    ),
    # WriteHalf
    (
        'Borrowed write half of a <a href="../struct.TcpStream.html" title="struct tokio::net::TcpStream"><code>TcpStream</code></a>, created by <a href="../struct.TcpStream.html#method.split" title="method tokio::net::TcpStream::split"><code>split</code></a>.',
        '<a href="../struct.TcpStream.html" title="struct tokio::net::TcpStream"><code>TcpStream</code></a> 的 borrowed 写半部，由 <a href="../struct.TcpStream.html#method.split" title="method tokio::net::TcpStream::split"><code>split</code></a> 创建。',
    ),

    # === tokio/net/windows/named_pipe/index.html ===
    (
        'A <a href="https://docs.microsoft.com/en-us/windows/win32/ipc/named-pipes">Windows named pipe</a> client.',
        '一个 <a href="https://docs.microsoft.com/en-us/windows/win32/ipc/named-pipes">Windows 命名管道</a> 客户端。',
    ),
    (
        'A <a href="https://docs.microsoft.com/en-us/windows/win32/ipc/named-pipes">Windows named pipe</a> server.',
        '一个 <a href="https://docs.microsoft.com/en-us/windows/win32/ipc/named-pipes">Windows 命名管道</a> 服务端。',
    ),
    # === tokio/net/windows/index.html ===
    (
        'Tokio support for <a href="https://docs.microsoft.com/en-us/windows/win32/ipc/named-pipes">Windows named pipes</a>.',
        'Tokio 对 <a href="https://docs.microsoft.com/en-us/windows/win32/ipc/named-pipes">Windows 命名管道</a> 的支持。',
    ),

    # === tokio/runtime/index.html ===
    (
        '<a href="struct.LocalRuntime.html" title="struct tokio::runtime::LocalRuntime"><code>LocalRuntime</code></a>-only config options',
        '<a href="struct.LocalRuntime.html" title="struct tokio::runtime::LocalRuntime"><code>LocalRuntime</code></a> 专用配置选项',
    ),
    (
        'Tokio runtime。',
        'Tokio 运行时。',
    ),
    (
        'Error returned by <code>try_current</code> when no Runtime has been started',
        '当没有 Runtime 启动时，由 <code>try_current</code> 返回的错误',
    ),
    (
        'The flavor of a <code>Runtime</code>.',
        '<code>Runtime</code> 的运行模式（flavor）。',
    ),

    # === tokio/sync/index.html ===
    (
        'A multi-producer, single-consumer queue for sending values between\r\nasynchronous tasks.',
        '用于在异步任务之间发送值的多生产者、单消费者队列。',
    ),
    (
        'A multi-producer, single-consumer queue for sending values between\nasynchronous tasks.',
        '用于在异步任务之间发送值的多生产者、单消费者队列。',
    ),
    # oneshot
    (
        'A one-shot channel is used for sending a single message between\r\nasynchronous tasks. The <a href="oneshot/fn.channel.html" title="fn tokio::sync::oneshot::channel"><code>channel</code></a> function is used to create a\r\n<a href="oneshot/struct.Sender.html" title="struct tokio::sync::oneshot::Sender"><code>Sender</code></a> and\r\n<a href="oneshot/struct.Receiver.html" title="struct tokio::sync::oneshot::Receiver"><code>Receiver</code></a>.',
        'oneshot channel 用于在异步任务之间发送单个消息。可使用 <a href="oneshot/fn.channel.html" title="fn tokio::sync::oneshot::channel"><code>channel</code></a> 函数创建 <a href="oneshot/struct.Sender.html" title="struct tokio::sync::oneshot::Sender"><code>Sender</code></a> 和 <a href="oneshot/struct.Receiver.html" title="struct tokio::sync::oneshot::Receiver"><code>Receiver</code></a>。',
    ),
    (
        'A one-shot channel is used for sending a single message between\r\nasynchronous tasks. The <a href="oneshot/fn.channel.html" title="fn tokio::sync::oneshot::channel"><code>channel</code></a> function is used to create a\r\n<a href="oneshot/struct.Sender.html" title="struct tokio::sync::oneshot::Sender"><code>Sender</code></a> and <a href="oneshot/struct.Receiver.html" title="struct tokio::sync::oneshot::Receiver"><code>Receiver</code></a> handle pair that form the channel.',
        'oneshot channel 用于在异步任务之间发送单个消息。可使用 <a href="oneshot/fn.channel.html" title="fn tokio::sync::oneshot::channel"><code>channel</code></a> 函数创建 <a href="oneshot/struct.Sender.html" title="struct tokio::sync::oneshot::Sender"><code>Sender</code></a> 和 <a href="oneshot/struct.Receiver.html" title="struct tokio::sync::oneshot::Receiver"><code>Receiver</code></a> 句柄对，二者构成该 channel。',
    ),
    # watch
    (
        'A multi-producer, multi-consumer channel that only retains the <em>last</em> sent\r\nvalue.',
        '一个多生产者、多消费者的 channel，仅保留最近一次发送的值。',
    ),
    (
        'A multi-producer, multi-consumer channel that only retains the <em>last</em> sent\nvalue.',
        '一个多生产者、多消费者的 channel，仅保留最近一次发送的值。',
    ),
    # AcquireError
    (
        'Error returned from the <a href="struct.Semaphore.html#method.acquire" title="method tokio::sync::Semaphore::acquire"><code>Semaphore::acquire</code></a> function.',
        '由 <a href="struct.Semaphore.html#method.acquire" title="method tokio::sync::Semaphore::acquire"><code>Semaphore::acquire</code></a> 函数返回的错误。',
    ),
    # BarrierWaitResult
    (
        'A <code>BarrierWaitResult</code> is returned by <code>wait</code> when all tasks in the <code>Barrier</code> have rendezvoused.',
        '当 <code>Barrier</code> 中所有 task 都在 <code>wait</code> 处汇合时，<code>wait</code> 返回一个 <code>BarrierWaitResult</code>。',
    ),
    # MappedMutexGuard
    (
        'A handle to a held <code>Mutex</code> that has had a function applied to it via <a href="struct.MutexGuard.html#method.map" title="associated function tokio::sync::MutexGuard::map"><code>MutexGuard::map</code></a>.',
        '对持有的 <code>Mutex</code> 通过 <a href="struct.MutexGuard.html#method.map" title="associated function tokio::sync::MutexGuard::map"><code>MutexGuard::map</code></a> 应用函数后得到的句柄。',
    ),
    # Mutex
    (
        'An asynchronous <code>Mutex</code>-like type.',
        '一个异步的、类似 <code>Mutex</code> 的类型。',
    ),
    # MutexGuard
    (
        'A handle to a held <code>Mutex</code>. The guard can be held across any <code>.await</code> point\r\nas it is <a href="https://doc.rust-lang.org/1.95.0/core/marker/trait.Send.html" title="trait core::marker::Send"><code>Send</code></a>.',
        '持有的 <code>Mutex</code> 的句柄。由于实现了 <a href="https://doc.rust-lang.org/1.95.0/core/marker/trait.Send.html" title="trait core::marker::Send"><code>Send</code></a>，可以在任意 <code>.await</code> 点持有该 guard。',
    ),
    (
        'A handle to a held <code>Mutex</code>. The guard can be held across any <code>.await</code> point\nas it is <a href="https://doc.rust-lang.org/1.95.0/core/marker/trait.Send.html" title="trait core::marker::Send"><code>Send</code></a>.',
        '持有的 <code>Mutex</code> 的句柄。由于实现了 <a href="https://doc.rust-lang.org/1.95.0/core/marker/trait.Send.html" title="trait core::marker::Send"><code>Send</code></a>，可以在任意 <code>.await</code> 点持有该 guard。',
    ),
    # OwnedMappedMutexGuard
    (
        'A owned handle to a held <code>Mutex</code> that has had a function applied to it via\r\n<a href="struct.OwnedMutexGuard.html#method.map" title="associated function tokio::sync::OwnedMutexGuard::map"><code>OwnedMutexGuard::map</code></a>.',
        '对持有的 <code>Mutex</code> 通过 <a href="struct.OwnedMutexGuard.html#method.map" title="associated function tokio::sync::OwnedMutexGuard::map"><code>OwnedMutexGuard::map</code></a> 应用函数后得到的 owned 句柄。',
    ),
    (
        'A owned handle to a held <code>Mutex</code> that has had a function applied to it via\n<a href="struct.OwnedMutexGuard.html#method.map" title="associated function tokio::sync::OwnedMutexGuard::map"><code>OwnedMutexGuard::map</code></a>.',
        '对持有的 <code>Mutex</code> 通过 <a href="struct.OwnedMutexGuard.html#method.map" title="associated function tokio::sync::OwnedMutexGuard::map"><code>OwnedMutexGuard::map</code></a> 应用函数后得到的 owned 句柄。',
    ),
    # OwnedMutexGuard
    (
        'An owned handle to a held <code>Mutex</code>.',
        '持有的 <code>Mutex</code> 的 owned 句柄。',
    ),
    # OwnedRwLockMappedWriteGuard
    (
        'Owned RAII structure used to release the exclusive write access of a lock when\r\ndropped.',
        'Owned RAII 结构，在 drop 时释放锁的独占写访问。',
    ),
    (
        'Owned RAII structure used to release the exclusive write access of a lock when\ndropped.',
        'Owned RAII 结构，在 drop 时释放锁的独占写访问。',
    ),
    # OwnedRwLockReadGuard
    (
        'Owned RAII structure used to release the shared read access of a lock when\r\ndropped.',
        'Owned RAII 结构，在 drop 时释放锁的共享读访问。',
    ),
    (
        'Owned RAII structure used to release the shared read access of a lock when\ndropped.',
        'Owned RAII 结构，在 drop 时释放锁的共享读访问。',
    ),
    # RwLockMappedWriteGuard / RwLockWriteGuard
    (
        'RAII structure used to release the exclusive write access of a lock when\r\ndropped.',
        'RAII 结构，在 drop 时释放锁的独占写访问。',
    ),
    (
        'RAII structure used to release the exclusive write access of a lock when\ndropped.',
        'RAII 结构，在 drop 时释放锁的独占写访问。',
    ),
    # RwLockReadGuard
    (
        'RAII structure used to release the shared read access of a lock when\r\ndropped.',
        'RAII 结构，在 drop 时释放锁的共享读访问。',
    ),
    (
        'RAII structure used to release the shared read access of a lock when\ndropped.',
        'RAII 结构，在 drop 时释放锁的共享读访问。',
    ),
    # SetOnceError
    (
        'Error that can be returned from <a href="struct.SetOnce.html#method.set" title="method tokio::sync::SetOnce::set"><code>SetOnce::set</code></a>.',
        '可由 <a href="struct.SetOnce.html#method.set" title="method tokio::sync::SetOnce::set"><code>SetOnce::set</code></a> 返回的错误。',
    ),
    # TryLockError
    (
        'Error returned from the <a href="struct.Mutex.html#method.try_lock" title="method tokio::sync::Mutex::try_lock"><code>Mutex::try_lock</code></a>, <a href="struct.RwLock.html#method.try_read" title="method tokio::sync::RwLock::try_read"><code>RwLock::try_read</code></a> and\r\n<a href="struct.RwLock.html#method.try_write" title="method tokio::sync::RwLock::try_write"><code>RwLock::try_write</code></a> functions.',
        '由 <a href="struct.Mutex.html#method.try_lock" title="method tokio::sync::Mutex::try_lock"><code>Mutex::try_lock</code></a>、<a href="struct.RwLock.html#method.try_read" title="method tokio::sync::RwLock::try_read"><code>RwLock::try_read</code></a> 和 <a href="struct.RwLock.html#method.try_write" title="method tokio::sync::RwLock::try_write"><code>RwLock::try_write</code></a> 函数返回的错误。',
    ),
    (
        'Error returned from the <a href="struct.Mutex.html#method.try_lock" title="method tokio::sync::Mutex::try_lock"><code>Mutex::try_lock</code></a>, <a href="struct.RwLock.html#method.try_read" title="method tokio::sync::RwLock::try_read"><code>RwLock::try_read</code></a> and\n<a href="struct.RwLock.html#method.try_write" title="method tokio::sync::RwLock::try_write"><code>RwLock::try_write</code></a> functions.',
        '由 <a href="struct.Mutex.html#method.try_lock" title="method tokio::sync::Mutex::try_lock"><code>Mutex::try_lock</code></a>、<a href="struct.RwLock.html#method.try_read" title="method tokio::sync::RwLock::try_read"><code>RwLock::try_read</code></a> 和 <a href="struct.RwLock.html#method.try_write" title="method tokio::sync::RwLock::try_write"><code>RwLock::try_write</code></a> 函数返回的错误。',
    ),
    # SetError
    (
        'Errors that can be returned from <a href="struct.OnceCell.html#method.set" title="method tokio::sync::OnceCell::set"><code>OnceCell::set</code></a>.',
        '可由 <a href="struct.OnceCell.html#method.set" title="method tokio::sync::OnceCell::set"><code>OnceCell::set</code></a> 返回的错误。',
    ),
    # TryAcquireError
    (
        'Error returned from the <a href="struct.Semaphore.html#method.try_acquire" title="method tokio::sync::Semaphore::try_acquire"><code>Semaphore::try_acquire</code></a> function.',
        '由 <a href="struct.Semaphore.html#method.try_acquire" title="method tokio::sync::Semaphore::try_acquire"><code>Semaphore::try_acquire</code></a> 函数返回的错误。',
    ),

    # === tokio/sync/broadcast/index.html ===
    (
        'Receiving-half of the <a href="index.html" title="mod tokio::sync::broadcast"><code>broadcast</code></a> channel.',
        '<a href="index.html" title="mod tokio::sync::broadcast"><code>broadcast</code></a> channel 的接收端。',
    ),
    (
        'Sending-half of the <a href="index.html" title="mod tokio::sync::broadcast"><code>broadcast</code></a> channel.',
        '<a href="index.html" title="mod tokio::sync::broadcast"><code>broadcast</code></a> channel 的发送端。',
    ),
    (
        'Create a bounded, multi-producer, multi-consumer channel where each sent\r\nvalue is broadcasted to all active receivers.',
        '创建一个有界的、多生产者、多消费者的 channel，每个发送的值都会广播给所有活跃的接收者。',
    ),
    (
        'Create a bounded, multi-producer, multi-consumer channel where each sent\nvalue is broadcasted to all active receivers.',
        '创建一个有界的、多生产者、多消费者的 channel，每个发送的值都会广播给所有活跃的接收者。',
    ),

    # === tokio/sync/broadcast/error/index.html ===
    (
        'Error returned by the <a href="../struct.Sender.html#method.send" title="method tokio::sync::broadcast::Sender::send"><code>send</code></a> function on a <a href="../struct.Sender.html" title="struct tokio::sync::broadcast::Sender"><code>Sender</code></a>.',
        '<a href="../struct.Sender.html#method.send" title="method tokio::sync::broadcast::Sender::send"><code>send</code></a> 函数在 <a href="../struct.Sender.html" title="struct tokio::sync::broadcast::Sender"><code>Sender</code></a> 上调用时返回的错误。',
    ),
    (
        'An error returned from the <a href="../struct.Receiver.html#method.recv" title="method tokio::sync::broadcast::Receiver::recv"><code>recv</code></a> function on a <a href="../struct.Receiver.html" title="struct tokio::sync::broadcast::Receiver"><code>Receiver</code></a>.',
        '<a href="../struct.Receiver.html#method.recv" title="method tokio::sync::broadcast::Receiver::recv"><code>recv</code></a> 函数在 <a href="../struct.Receiver.html" title="struct tokio::sync::broadcast::Receiver"><code>Receiver</code></a> 上调用时返回的错误。',
    ),
    (
        'An error returned from the <a href="../struct.Receiver.html#method.try_recv" title="method tokio::sync::broadcast::Receiver::try_recv"><code>try_recv</code></a> function on a <a href="../struct.Receiver.html" title="struct tokio::sync::broadcast::Receiver"><code>Receiver</code></a>.',
        '<a href="../struct.Receiver.html#method.try_recv" title="method tokio::sync::broadcast::Receiver::try_recv"><code>try_recv</code></a> 函数在 <a href="../struct.Receiver.html" title="struct tokio::sync::broadcast::Receiver"><code>Receiver</code></a> 上调用时返回的错误。',
    ),

    # === tokio/sync/futures/index.html ===
    (
        'Future returned from <a href="../struct.Notify.html#method.notified" title="method tokio::sync::Notify::notified"><code>Notify::notified()</code></a>.',
        '由 <a href="../struct.Notify.html#method.notified" title="method tokio::sync::Notify::notified"><code>Notify::notified()</code></a> 返回的 future。',
    ),
    (
        'Future returned from <a href="../struct.Notify.html#method.notified_owned" title="method tokio::sync::Notify::notified_owned"><code>Notify::notified_owned()</code></a>.',
        '由 <a href="../struct.Notify.html#method.notified_owned" title="method tokio::sync::Notify::notified_owned"><code>Notify::notified_owned()</code></a> 返回的 future。',
    ),

    # === tokio/sync/mpsc/index.html (USER REPORTED) ===
    (
        'An <a href="https://doc.rust-lang.org/1.95.0/core/iter/traits/iterator/trait.Iterator.html" title="trait core::iter::traits::iterator::Iterator"><code>Iterator</code></a> of <a href="struct.Permit.html" title="struct tokio::sync::mpsc::Permit"><code>Permit</code></a> that can be used to hold <code>n</code> slots in the channel.',
        '<a href="https://doc.rust-lang.org/1.95.0/core/iter/traits/iterator/trait.Iterator.html" title="trait core::iter::traits::iterator::Iterator"><code>Iterator</code></a>，对 <a href="struct.Permit.html" title="struct tokio::sync::mpsc::Permit"><code>Permit</code></a> 进行迭代，可用于在 channel 中持有 <code>n</code> 个槽位。',
    ),
    (
        'Receives values from the associated <code>Sender</code>.',
        '从关联的 <code>Sender</code> 接收值。',
    ),
    (
        'Sends values to the associated <code>Receiver</code>.',
        '向关联的 <code>Receiver</code> 发送值。',
    ),
    (
        'Receive values from the associated <code>UnboundedSender</code>.',
        '从关联的 <code>UnboundedSender</code> 接收值。',
    ),
    (
        'Send values to the associated <code>UnboundedReceiver</code>.',
        '向关联的 <code>UnboundedReceiver</code> 发送值。',
    ),
    (
        'Creates a bounded mpsc channel for communicating between asynchronous tasks\r\nwith backpressure.',
        '创建一个有界 mpsc channel，用于在异步任务之间通过背压（backpressure）进行通信。',
    ),
    (
        'Creates a bounded mpsc channel for communicating between asynchronous tasks\nwith backpressure.',
        '创建一个有界 mpsc channel，用于在异步任务之间通过背压（backpressure）进行通信。',
    ),
    (
        'Creates an unbounded mpsc channel for communicating between asynchronous\r\ntasks without backpressure.',
        '创建一个无界 mpsc channel，用于在异步任务之间通信（不提供背压）。',
    ),
    (
        'Creates an unbounded mpsc channel for communicating between asynchronous\ntasks without backpressure.',
        '创建一个无界 mpsc channel，用于在异步任务之间通信（不提供背压）。',
    ),

    # === tokio/sync/mpsc/error/index.html ===
    (
        'Error returned by <a href="../struct.Sender.html#method.send" title="method tokio::sync::mpsc::Sender::send"><code>Sender::send</code></a>.',
        '由 <a href="../struct.Sender.html#method.send" title="method tokio::sync::mpsc::Sender::send"><code>Sender::send</code></a> 返回的错误。',
    ),
    (
        'Error returned by <a href="../struct.Sender.html#method.send_timeout" title="method tokio::sync::mpsc::Sender::send_timeout"><code>Sender::send_timeout</code></a>.',
        '由 <a href="../struct.Sender.html#method.send_timeout" title="method tokio::sync::mpsc::Sender::send_timeout"><code>Sender::send_timeout</code></a> 返回的错误。',
    ),
    (
        'Error returned by <a href="../struct.Receiver.html#method.try_recv" title="method tokio::sync::mpsc::Receiver::try_recv"><code>Receiver::try_recv</code></a>.',
        '由 <a href="../struct.Receiver.html#method.try_recv" title="method tokio::sync::mpsc::Receiver::try_recv"><code>Receiver::try_recv</code></a> 返回的错误。',
    ),
    (
        'Error returned by <a href="../struct.Sender.html#method.try_send" title="method tokio::sync::mpsc::Sender::try_send"><code>Sender::try_send</code></a>.',
        '由 <a href="../struct.Sender.html#method.try_send" title="method tokio::sync::mpsc::Sender::try_send"><code>Sender::try_send</code></a> 返回的错误。',
    ),

    # === tokio/sync/oneshot/index.html ===
    (
        '<code>Oneshot</code> error types.',
        '<code>Oneshot</code> 错误类型。',
    ),
    (
        'Receives a value from the associated <a href="struct.Sender.html" title="struct tokio::sync::oneshot::Sender"><code>Sender</code></a>.',
        '从关联的 <a href="struct.Sender.html" title="struct tokio::sync::oneshot::Sender"><code>Sender</code></a> 接收一个值。',
    ),
    (
        'Sends a value to the associated <a href="struct.Receiver.html" title="struct tokio::sync::oneshot::Receiver"><code>Receiver</code></a>.',
        '向关联的 <a href="struct.Receiver.html" title="struct tokio::sync::oneshot::Receiver"><code>Receiver</code></a> 发送一个值。',
    ),
    (
        'Creates a new one-shot channel for sending single values across asynchronous\r\ntasks.',
        '创建一个新的 one-shot channel，用于在异步任务之间发送单个值。',
    ),
    (
        'Creates a new one-shot channel for sending single values across asynchronous\ntasks.',
        '创建一个新的 one-shot channel，用于在异步任务之间发送单个值。',
    ),

    # === tokio/sync/oneshot/error/index.html ===
    (
        'Error returned by the <code>Future</code> implementation for <code>Receiver</code>.',
        '由 <code>Receiver</code> 的 <code>Future</code> 实现返回的错误。',
    ),
    (
        'Error returned by the <code>try_recv</code> function on <code>Receiver</code>.',
        '由 <code>Receiver</code> 上的 <code>try_recv</code> 函数返回的错误。',
    ),

    # === tokio/sync/watch/index.html ===
    (
        'Receives values from the associated <a href="struct.Sender.html" title="struct tokio::sync::watch::Sender"><code>Sender</code></a>.',
        '从关联的 <a href="struct.Sender.html" title="struct tokio::sync::watch::Sender"><code>Sender</code></a> 接收值。',
    ),
    (
        'Sends values to the associated <a href="struct.Receiver.html" title="struct tokio::sync::watch::Receiver"><code>Receiver</code></a>.',
        '向关联的 <a href="struct.Receiver.html" title="struct tokio::sync::watch::Receiver"><code>Receiver</code></a> 发送值。',
    ),

    # === tokio/task/index.html ===
    (
        'An opaque ID that uniquely identifies a task relative to all other currently\r\nrunning tasks.',
        '一个不透明的 ID，用于在所有当前运行的 task 中唯一标识某个 task。',
    ),
    (
        'An opaque ID that uniquely identifies a task relative to all other currently\nrunning tasks.',
        '一个不透明的 ID，用于在所有当前运行的 task 中唯一标识某个 task。',
    ),
    (
        'A collection of tasks spawned on a Tokio runtime。',
        '在 Tokio runtime 上生成的一组 task。',
    ),
    (
        'Context guard for <code>LocalSet</code>',
        '<code>LocalSet</code> 的上下文守护',
    ),
    (
        'Returns the <a href="struct.Id.html" title="struct tokio::task::Id"><code>Id</code></a> of the currently running task.',
        '返回当前正在运行的 task 的 <a href="struct.Id.html" title="struct tokio::task::Id"><code>Id</code></a>。',
    ),
    (
        'Spawns a new asynchronous task, returning a\r\n<a href="struct.JoinHandle.html" title="struct tokio::task::JoinHandle"><code>JoinHandle</code></a> for it.',
        '生成一个新的异步 task，返回一个 <a href="struct.JoinHandle.html" title="struct tokio::task::JoinHandle"><code>JoinHandle</code></a>。',
    ),
    (
        'Spawns a new asynchronous task, returning a\n<a href="struct.JoinHandle.html" title="struct tokio::task::JoinHandle"><code>JoinHandle</code></a> for it.',
        '生成一个新的异步 task，返回一个 <a href="struct.JoinHandle.html" title="struct tokio::task::JoinHandle"><code>JoinHandle</code></a>。',
    ),
    (
        'Spawns a <code>!Send</code> future on the current <a href="struct.LocalSet.html" title="struct tokio::task::LocalSet"><code>LocalSet</code></a> or <a href="../runtime/struct.LocalRuntime.html" title="struct tokio::runtime::LocalRuntime"><code>LocalRuntime</code></a>.',
        '在当前 <a href="struct.LocalSet.html" title="struct tokio::task::LocalSet"><code>LocalSet</code></a> 或 <a href="../runtime/struct.LocalRuntime.html" title="struct tokio::runtime::LocalRuntime"><code>LocalRuntime</code></a> 上生成一个 <code>!Send</code> future。',
    ),
    (
        'Returns the <a href="struct.Id.html" title="struct tokio::task::Id"><code>Id</code></a> of the currently running task, or <code>None</code> if called outside\r\nof a task.',
        '返回当前正在运行的 task 的 <a href="struct.Id.html" title="struct tokio::task::Id"><code>Id</code></a>；若在 task 之外调用则返回 <code>None</code>。',
    ),
    (
        'Returns the <a href="struct.Id.html" title="struct tokio::task::Id"><code>Id</code></a> of the currently running task, or <code>None</code> if called outside\nof a task.',
        '返回当前正在运行的 task 的 <a href="struct.Id.html" title="struct tokio::task::Id"><code>Id</code></a>；若在 task 之外调用则返回 <code>None</code>。',
    ),
    (
        'Yields execution back to the Tokio runtime。',
        '将执行权交回 Tokio runtime。',
    ),

    # === tokio/task/coop/index.html ===
    (
        'Future wrapper to ensure cooperative scheduling created by <a href="fn.cooperative.html" title="fn tokio::task::coop::cooperative"><code>cooperative</code></a>.',
        '由 <a href="fn.cooperative.html" title="fn tokio::task::coop::cooperative"><code>cooperative</code></a> 创建的、用于保证协作式调度的 future 包装器。',
    ),
    (
        'Value returned by the <a href="fn.poll_proceed.html" title="fn tokio::task::coop::poll_proceed"><code>poll_proceed</code></a> method.',
        '由 <a href="fn.poll_proceed.html" title="fn tokio::task::coop::poll_proceed"><code>poll_proceed</code></a> 方法返回的值。',
    ),
    (
        'Future for the <a href="fn.unconstrained.html" title="fn tokio::task::coop::unconstrained"><code>unconstrained</code></a> method.',
        '<a href="fn.unconstrained.html" title="fn tokio::task::coop::unconstrained"><code>unconstrained</code></a> 方法对应的 future。',
    ),
    (
        'Consumes a unit of budget and returns the execution back to the Tokio\r\nruntime <em>if</em> the task’s coop budget was exhausted.',
        '消耗一个单位的预算；若 task 的协作预算已耗尽，则将执行权交回 Tokio runtime。',
    ),
    (
        'Consumes a unit of budget and returns the execution back to the Tokio\nruntime <em>if</em> the task’s coop budget was exhausted.',
        '消耗一个单位的预算；若 task 的协作预算已耗尽，则将执行权交回 Tokio runtime。',
    ),
    (
        'Returns <code>true</code> if there is still budget left on the task.',
        '如果 task 上还有剩余预算，则返回 <code>true</code>。',
    ),
    (
        'Decrements the task budget and returns <a href="https://doc.rust-lang.org/1.95.0/core/task/poll/enum.Poll.html#variant.Pending" title="variant core::task::poll::Poll::Pending"><code>Poll::Pending</code></a> if the budget is depleted.\r\nThis indicates that the task should yield to the scheduler. Other',
        '减少 task 预算；若预算已耗尽，则返回 <a href="https://doc.rust-lang.org/1.95.0/core/task/poll/enum.Poll.html#variant.Pending" title="variant core::task::poll::Poll::Pending"><code>Poll::Pending</code></a>。这表示 task 应让出（yield）给调度器。其他',
    ),
    (
        'Decrements the task budget and returns <a href="https://doc.rust-lang.org/1.95.0/core/task/poll/enum.Poll.html#variant.Pending" title="variant core::task::poll::Poll::Pending"><code>Poll::Pending</code></a> if the budget is depleted.\nThis indicates that the task should yield to the scheduler. Other',
        '减少 task 预算；若预算已耗尽，则返回 <a href="https://doc.rust-lang.org/1.95.0/core/task/poll/enum.Poll.html#variant.Pending" title="variant core::task::poll::Poll::Pending"><code>Poll::Pending</code></a>。这表示 task 应让出（yield）给调度器。其他',
    ),
    (
        'Turn off cooperative scheduling for a future. The future will never be forced to yield by\r\nTokio. Using this exposes your service to starvation if the unconstrained future never yields\r\notherwise.',
        '关闭某个 future 的协作式调度。该 future 永远不会被 Tokio 强制让出。使用它会使你的服务面临饥饿（starvation）的风险，除非该 unconstrained future 自己会让出。',
    ),
    (
        'Turn off cooperative scheduling for a future. The future will never be forced to yield by\nTokio. Using this exposes your service to starvation if the unconstrained future never yields\notherwise.',
        '关闭某个 future 的协作式调度。该 future 永远不会被 Tokio 强制让出。使用它会使你的服务面临饥饿（starvation）的风险，除非该 unconstrained future 自己会让出。',
    ),

    # === tokio/task/futures/index.html ===
    (
        'A future that sets a value <code>T</code> of a task local for the future <code>F</code> during\r\nits execution.',
        '一个 future，会在 <code>F</code> 执行期间为该 task 局部变量设置一个值 <code>T</code>。',
    ),
    (
        'A future that sets a value <code>T</code> of a task local for the future <code>F</code> during\nits execution.',
        '一个 future，会在 <code>F</code> 执行期间为该 task 局部变量设置一个值 <code>T</code>。',
    ),

    # === tokio/time/index.html ===
    (
        'A measurement of a monotonically nondecreasing clock.\r\nOpaque and useful only with <code>Duration</code>.',
        '单调递增时钟的一个度量值。不透明，仅与 <code>Duration</code> 一起使用时有意义。',
    ),
    (
        'A measurement of a monotonically nondecreasing clock.\nOpaque and useful only with <code>Duration</code>.',
        '单调递增时钟的一个度量值。不透明，仅与 <code>Duration</code> 一起使用时有意义。',
    ),
    (
        'Interval returned by <a href="fn.interval.html" title="fn tokio::time::interval"><code>interval</code></a> and <a href="fn.interval_at.html" title="fn tokio::time::interval_at"><code>interval_at</code></a>.',
        '由 <a href="fn.interval.html" title="fn tokio::time::interval"><code>interval</code></a> 和 <a href="fn.interval_at.html" title="fn tokio::time::interval_at"><code>interval_at</code></a> 返回的 Interval。',
    ),
    (
        'Future returned by <a href="fn.sleep.html" title="fn tokio::time::sleep"><code>sleep</code></a> and <a href="fn.sleep_until.html" title="fn tokio::time::sleep_until"><code>sleep_until</code></a>.',
        '由 <a href="fn.sleep.html" title="fn tokio::time::sleep"><code>sleep</code></a> 和 <a href="fn.sleep_until.html" title="fn tokio::time::sleep_until"><code>sleep_until</code></a> 返回的 future。',
    ),
    (
        'Future returned by <a href="fn.timeout.html" title="fn tokio::time::timeout"><code>timeout</code></a> and <a href="fn.timeout_at.html" title="fn tokio::time::timeout_at"><code>timeout_at</code></a>.',
        '由 <a href="fn.timeout.html" title="fn tokio::time::timeout"><code>timeout</code></a> 和 <a href="fn.timeout_at.html" title="fn tokio::time::timeout_at"><code>timeout_at</code></a> 返回的 future。',
    ),
    (
        'Defines the behavior of an <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a> when it misses a tick.',
        '当 <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a> 错过一个 tick 时定义其行为。',
    ),
    (
        'Creates new <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a> that yields with interval of <code>period</code>. The first\r\ntick completes immediately. The default <a href="enum.MissedTickBehavior.html" title="enum tokio::time::MissedTickBehavior"><code>MissedTickBehavior</code></a> is <code>Burst</code>, but it can be changed using <code>set_missed_tick_behavior</code>.',
        '创建一个新的 <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a>，以 <code>period</code> 为间隔周期产生 tick。第一次 tick 立即完成。默认的 <a href="enum.MissedTickBehavior.html" title="enum tokio::time::MissedTickBehavior"><code>MissedTickBehavior</code></a> 为 <code>Burst</code>，但可以使用 <code>set_missed_tick_behavior</code> 更改。',
    ),
    (
        'Creates new <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a> that yields with interval of <code>period</code>. The first\ntick completes immediately. The default <a href="enum.MissedTickBehavior.html" title="enum tokio::time::MissedTickBehavior"><code>MissedTickBehavior</code></a> is <code>Burst</code>, but it can be changed using <code>set_missed_tick_behavior</code>.',
        '创建一个新的 <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a>，以 <code>period</code> 为间隔周期产生 tick。第一次 tick 立即完成。默认的 <a href="enum.MissedTickBehavior.html" title="enum tokio::time::MissedTickBehavior"><code>MissedTickBehavior</code></a> 为 <code>Burst</code>，但可以使用 <code>set_missed_tick_behavior</code> 更改。',
    ),
    (
        'Creates new <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a> that yields with interval of <code>period</code> with the\r\nfirst tick completing at <code>start</code>. The default <a href="enum.MissedTickBehavior.html" title="enum tokio::time::MissedTickBehavior"><code>MissedTickBehavior</code></a> is <code>Burst</code>, but it can be changed using <code>set_missed_tick_behavior</code>.',
        '创建一个新的 <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a>，以 <code>period</code> 为间隔周期产生 tick，第一次 tick 在 <code>start</code> 时完成。默认的 <a href="enum.MissedTickBehavior.html" title="enum tokio::time::MissedTickBehavior"><code>MissedTickBehavior</code></a> 为 <code>Burst</code>，但可以使用 <code>set_missed_tick_behavior</code> 更改。',
    ),
    (
        'Creates new <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a> that yields with interval of <code>period</code> with the\nfirst tick completing at <code>start</code>. The default <a href="enum.MissedTickBehavior.html" title="enum tokio::time::MissedTickBehavior"><code>MissedTickBehavior</code></a> is <code>Burst</code>, but it can be changed using <code>set_missed_tick_behavior</code>.',
        '创建一个新的 <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a>，以 <code>period</code> 为间隔周期产生 tick，第一次 tick 在 <code>start</code> 时完成。默认的 <a href="enum.MissedTickBehavior.html" title="enum tokio::time::MissedTickBehavior"><code>MissedTickBehavior</code></a> 为 <code>Burst</code>，但可以使用 <code>set_missed_tick_behavior</code> 更改。',
    ),
    # interval/interval_at with separate <a> for Burst and set_missed_tick_behavior
    (
        'Creates new <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a> that yields with interval of <code>period</code>. The first\r\ntick completes immediately. The default <a href="enum.MissedTickBehavior.html" title="enum tokio::time::MissedTickBehavior"><code>MissedTickBehavior</code></a> is\r\n<a href="enum.MissedTickBehavior.html#variant.Burst" title="variant tokio::time::MissedTickBehavior::Burst"><code>Burst</code></a>, but this can be configured\r\nby calling <a href="struct.Interval.html#method.set_missed_tick_behavior" title="method tokio::time::Interval::set_missed_tick_behavior"><code>set_missed_tick_behavior</code></a>.',
        '创建一个新的 <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a>，以 <code>period</code> 为间隔周期产生 tick。第一次 tick 立即完成。默认的 <a href="enum.MissedTickBehavior.html" title="enum tokio::time::MissedTickBehavior"><code>MissedTickBehavior</code></a> 为 <a href="enum.MissedTickBehavior.html#variant.Burst" title="variant tokio::time::MissedTickBehavior::Burst"><code>Burst</code></a>，但可以调用 <a href="struct.Interval.html#method.set_missed_tick_behavior" title="method tokio::time::Interval::set_missed_tick_behavior"><code>set_missed_tick_behavior</code></a> 进行配置。',
    ),
    (
        'Creates new <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a> that yields with interval of <code>period</code> with the\r\nfirst tick completing at <code>start</code>. The default <a href="enum.MissedTickBehavior.html" title="enum tokio::time::MissedTickBehavior"><code>MissedTickBehavior</code></a> is\r\n<a href="enum.MissedTickBehavior.html#variant.Burst" title="variant tokio::time::MissedTickBehavior::Burst"><code>Burst</code></a>, but this can be configured\r\nby calling <a href="struct.Interval.html#method.set_missed_tick_behavior" title="method tokio::time::Interval::set_missed_tick_behavior"><code>set_missed_tick_behavior</code></a>.',
        '创建一个新的 <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a>，以 <code>period</code> 为间隔周期产生 tick，第一次 tick 在 <code>start</code> 时完成。默认的 <a href="enum.MissedTickBehavior.html" title="enum tokio::time::MissedTickBehavior"><code>MissedTickBehavior</code></a> 为 <a href="enum.MissedTickBehavior.html#variant.Burst" title="variant tokio::time::MissedTickBehavior::Burst"><code>Burst</code></a>，但可以调用 <a href="struct.Interval.html#method.set_missed_tick_behavior" title="method tokio::time::Interval::set_missed_tick_behavior"><code>set_missed_tick_behavior</code></a> 进行配置。',
    ),
    (
        'Waits until <code>duration</code> has elapsed.',
        '等待直到 <code>duration</code> 时长过去。',
    ),
    (
        'Waits until <code>deadline</code> is reached.',
        '等待直到 <code>deadline</code> 截止时刻到达。',
    ),
    (
        'Requires a <code>Future</code> to complete before the specified duration has elapsed.',
        '要求一个 <code>Future</code> 在指定时长过去之前完成。',
    ),
    (
        'Requires a <code>Future</code> to complete before the specified instant in time.',
        '要求一个 <code>Future</code> 在指定时刻之前完成。',
    ),

    # === tokio/time/error/index.html ===
    (
        'Errors returned by <code>Timeout</code>.',
        '由 <code>Timeout</code> 返回的错误。',
    ),

    # ====== quinn 漏译 ======
    (
        'Authentication data for (rustls) TLS session',
        '（rustls）TLS 会话的身份认证数据',
    ),
    (
        'The initial cipher suite (AES-128-GCM-SHA256) is not available',
        '初始密码套件（AES-128-GCM-SHA256）不可用',
    ),
    (
        'A QUIC-compatible TLS client configuration',
        '一个与 QUIC 兼容的 TLS 客户端配置',
    ),
    (
        'A QUIC-compatible TLS server configuration',
        '一个与 QUIC 兼容的 TLS 服务端配置',
    ),
    (
        'A rustls TLS session',
        '一个 rustls TLS 会话',
    ),
    (
        'rustls reports protocol errors using this type.',
        'rustls 使用此类型报告协议错误。',
    ),

    # ====== bytes 漏译 ======
    (
        'Utilities for working with buffers.',
        '用于处理缓冲区的工具。',
    ),
    (
        'A cheaply cloneable and sliceable chunk of contiguous memory.',
        '一个可廉价 clone 和切片的连续内存块。',
    ),
    (
        'A unique reference to a contiguous slice of memory.',
        '对一段连续内存切片的唯一引用。',
    ),
    (
        'Error type for the try_get_ methods of Buf. Indicates that there were not enough remaining bytes in the buffer while attempting to get a value from a Buf with one of the try_get_ methods.',
        'Buf 的 try_get_ 方法的错误类型。表示在使用 Buf 的某个 try_get_ 方法尝试取值时，缓冲区中没有足够的剩余字节。',
    ),
    (
        'A Chain sequences two buffers.',
        'Chain 将两个 buffer 串接起来。',
    ),
    (
        'Iterator over the bytes contained by the buffer.',
        '对 buffer 中包含的字节进行迭代的迭代器。',
    ),
    (
        'A BufMut adapter which limits the amount of bytes that can be written to an underlying buffer.',
        '一个 BufMut 适配器，用于限制可以写入底层 buffer 的字节数。',
    ),
    (
        'A Buf adapter which implements io::Read for the inner value.',
        '一个 Buf 适配器，为内部值实现 io::Read。',
    ),
    (
        'A Buf adapter which limits the bytes read from an underlying buffer.',
        '一个 Buf 适配器，用于限制从底层 buffer 读取的字节数。',
    ),
    (
        'Uninitialized byte slice.',
        '未初始化的字节切片。',
    ),
    (
        'A BufMut adapter which implements io::Write for the inner value.',
        '一个 BufMut 适配器，为内部值实现 io::Write。',
    ),
    (
        'Read bytes from a buffer.',
        '从一个 buffer 读取字节。',
    ),
    (
        'A trait for values that provide sequential write access to bytes.',
        '一个用于为字节提供顺序写访问的值的 trait。',
    ),
    # === bytes with <code> tags ===
    (
        'A <code>Chain</code> sequences two buffers.',
        '一个 <code>Chain</code>，用于将两个 buffer 串接起来。',
    ),
    (
        'A <code>BufMut</code> adapter which limits the amount of bytes that can be written\r\nto an underlying buffer.',
        '一个 <code>BufMut</code> 适配器，用于限制可以写入底层 buffer 的字节数。',
    ),
    (
        'A <code>BufMut</code> adapter which limits the amount of bytes that can be written\nto an underlying buffer.',
        '一个 <code>BufMut</code> 适配器，用于限制可以写入底层 buffer 的字节数。',
    ),
    (
        'A <code>Buf</code> adapter which implements <code>io::Read</code> for the inner value.',
        '一个 <code>Buf</code> 适配器，为内部值实现 <code>io::Read</code>。',
    ),
    (
        'A <code>Buf</code> adapter which limits the bytes read from an underlying buffer.',
        '一个 <code>Buf</code> 适配器，用于限制从底层 buffer 读取的字节数。',
    ),
    (
        'A <code>BufMut</code> adapter which implements <code>io::Write</code> for the inner value.',
        '一个 <code>BufMut</code> 适配器，为内部值实现 <code>io::Write</code>。',
    ),
    # === bytes with line wraps (LF versions) ===
    (
        'Error type for the try_get_ methods of Buf. Indicates that there were not enough remaining\nbytes in the buffer while attempting to get a value from a Buf with one of the try_get_\nmethods.',
        'Buf 的 try_get_ 方法的错误类型。表示在使用 Buf 的某个 try_get_ 方法尝试取值时，缓冲区中没有足够的剩余字节。',
    ),
    (
        'Error type for the <code>try_get_</code> methods of <a href="buf/trait.Buf.html" title="trait bytes::buf::Buf"><code>Buf</code></a>.\r\nIndicates that there were not enough remaining\r\nbytes in the buffer while attempting\r\nto get a value from a <a href="buf/trait.Buf.html" title="trait bytes::buf::Buf"><code>Buf</code></a> with one\r\nof the <code>try_get_</code> methods.',
        '<a href="buf/trait.Buf.html" title="trait bytes::buf::Buf"><code>Buf</code></a> 的 <code>try_get_</code> 方法的错误类型。表示在使用 <a href="buf/trait.Buf.html" title="trait bytes::buf::Buf"><code>Buf</code></a> 的某个 <code>try_get_</code> 方法尝试取值时，缓冲区中没有足够的剩余字节。',
    ),
    # === bytes buf/index.html "Traits" h2 chrome label variant ===
    (
        '<h2 id="traits" class="section-header">Trait<a href="#traits" class="anchor">§</a></h2>',
        '<h2 id="traits" class="section-header">特性<a href="#traits" class="anchor">§</a></h2>',
    ),
]


def main():
    """Apply these pairs as byte replacements across all .html files in the given crate."""
    import sys
    crate_dir = sys.argv[1] if len(sys.argv) > 1 else 'tokio'
    apply = '--apply' in sys.argv
    report = '--report' in sys.argv
    dry_run = not (apply or report)

    SKIP = {'static.files', 'search.index', 'src', '_common_tools', '.git'}

    total_hits = 0
    files_modified = 0
    pair_hits = {}

    for top, dirs, fs in os.walk(crate_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in SKIP and not d.endswith('_old')]
        for fn in fs:
            if not fn.endswith('.html'):
                continue
            path = os.path.join(top, fn)
            with open(path, 'rb') as f:
                content = f.read()
            new_content = content
            file_hits = 0
            for i, (en, zh) in enumerate(PAIRS):
                en_b = en.encode('utf-8')
                zh_b = zh.encode('utf-8')
                if en_b in new_content:
                    count = new_content.count(en_b)
                    new_content = new_content.replace(en_b, zh_b)
                    file_hits += count
                    pair_hits[i] = pair_hits.get(i, 0) + count
            if file_hits > 0:
                if not dry_run:
                    with open(path, 'wb') as f:
                        f.write(new_content)
                files_modified += 1
                total_hits += file_hits
                print(f'  {path}: {file_hits} replacements')

    print(f'\n=== Summary ===')
    print(f'Total replacements: {total_hits}')
    print(f'Files modified: {files_modified}')
    print(f'\nMissing pairs (in dict but not found in files):')
    for i, (en, zh) in enumerate(PAIRS):
        if i not in pair_hits:
            print(f'  [{i}] {en[:80]!r}')


if __name__ == '__main__':
    main()
