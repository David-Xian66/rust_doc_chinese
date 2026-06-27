#!/usr/bin/env python3
"""使用 bs4 解析 rustdoc HTML，把 <dd> 内的 inline HTML 标签临时替换为占位符，
然后做 str.replace，再恢复标签。

策略：
- 找到 <dl class="item-table"> ... <dd>...</dd> 块
- 在 dd 内，把所有 inline HTML 标签（<code>、<a>、<em>、<wbr/> 等）替换为 \x01N\x02 占位符
- 在 dd 的可见文本上做 str.replace
- 把占位符还原成原标签

这样既能匹配带 inline 标签的英文，又不会破坏 HTML 结构。

用法：
    python _common_tools/_translate_with_bs4.py <crate_dir> [--apply]
"""
import os
import re
import sys

from bs4 import BeautifulSoup, NavigableString, Tag


# ====== 词典：纯文本 → 中文 ======
TRANSLATION_PAIRS = [
    # === tokio 漏译 ===
    ('A wrapper around a byte buffer that is incrementally filled and initialized.',
     '一个字节缓冲区的封装，会被增量填充和初始化。'),
    ('Describes the readiness state of an I/O resources.',
     '描述 I/O 资源的就绪状态。'),
    ('Reads bytes asynchronously.', '异步地读取字节。'),
    ('Reads bytes from a source.', '从一个数据源异步地读取字节。'),
    ('Seek bytes asynchronously.', '异步地定位字节。'),
    ('Writes bytes asynchronously.', '异步地写入字节。'),
    ('Readiness event interest.', '就绪事件兴趣位。'),
    ('A TCP socket server, listening for connections.',
     '一个 TCP socket 服务端，用于监听连接。'),
    ('A TCP stream between a local and a remote socket.',
     '本地与远端 socket 之间的 TCP 流。'),
    ('A UDP socket.', '一个 UDP socket。'),
    ('Performs a DNS resolution.', '执行 DNS 解析。'),
    ('Converts or resolves without blocking to one or more SocketAddr values.',
     '非阻塞地转换或解析出一个或多个 SocketAddr 值。'),
    ('A TCP socket that has not yet been converted to a TcpStream or\nTcpListener.',
     '一个尚未转换为 TcpStream 或 TcpListener 的 TCP socket。'),
    ('A TCP socket that has not yet been converted to a TcpStream or TcpListener.',
     '一个尚未转换为 TcpStream 或 TcpListener 的 TCP socket。'),
    ('Owned read half of a TcpStream, created by into_split.',
     'TcpStream 的 owned 读半部，由 into_split 创建。'),
    ('Owned write half of a TcpStream, created by into_split.',
     'TcpStream 的 owned 写半部，由 into_split 创建。'),
    ('Borrowed read half of a TcpStream, created by split.',
     'TcpStream 的借用读半部，由 split 创建。'),
    ('Borrowed write half of a TcpStream, created by split.',
     'TcpStream 的借用写半部，由 split 创建。'),
    ('Error indicating that two halves were not from the same socket, and thus could\nnot be reunited.',
     '指示两半部分不是来自同一个 socket、因此无法重新合并的错误。'),
    ('Error indicating that two halves were not from the same socket, and thus could not be reunited.',
     '指示两半部分不是来自同一个 socket、因此无法重新合并的错误。'),
    ('Tokio support for Windows named pipes.', 'Tokio 对 Windows 命名管道的支持。'),
    ('A builder suitable for building and interacting with named pipes from the\nclient side.',
     '一个构建器，用于从客户端构建命名管道并与之交互。'),
    ('A builder suitable for building and interacting with named pipes from the client side.',
     '一个构建器，用于从客户端构建命名管道并与之交互。'),
    ('A Windows named pipe client.', '一个 Windows 命名管道客户端。'),
    ('A Windows named pipe server.', '一个 Windows 命名管道服务端。'),
    ('Information about a named pipe.', '命名管道的相关信息。'),
    ('Indicates the end of a named pipe.', '指示命名管道的端点。'),
    ('The pipe mode of a named pipe.', '命名管道的管道模式。'),
    ('A builder structure for construct a named pipe with named pipe-specific\noptions. This is required to use for named pipe servers who wants to modify\npipe-related options.',
     '一个构建器结构，用于构造带有命名管道特定选项的命名管道。需要修改管道相关选项的命名管道服务端必须使用它。'),
    # runtime
    ('Builds Tokio Runtime with custom configuration values.',
     '使用自定义配置值构建 Tokio Runtime。'),
    ('Runtime context guard.', 'Runtime 上下文守护。'),
    ('Handle to the runtime.', 'runtime 的句柄。'),
    ('An opaque ID that uniquely identifies a runtime relative to all other currently\nrunning runtimes.',
     '一个不透明的 ID，相对于所有其他当前正在运行的 runtimes 唯一标识一个 runtime。'),
    ('An opaque ID that uniquely identifies a runtime relative to all other currently running runtimes.',
     '一个不透明的 ID，相对于所有其他当前正在运行的 runtimes 唯一标识一个 runtime。'),
    ('LocalRuntime-only config options', 'LocalRuntime 专用配置选项'),
    ('A local Tokio runtime.', '一个本地 Tokio runtime。'),
    ('The Tokio runtime.', '即 Tokio runtime。'),
    ('Handle to the runtime’s metrics.', 'runtime 的指标句柄。'),
    ('Handle to the runtime’s metrics.', 'runtime 的指标句柄。'),
    ('Error returned by try_current when no Runtime has been started',
     '当尚未启动任何 Runtime 时由 try_current 返回的错误'),
    ('The flavor of a Runtime.', 'Runtime 的风格（flavor）。'),
    ('Checks whether the given error was emitted by Tokio when shutting down its runtime.',
     '检查给定的错误是否由 Tokio 在关闭其 runtime 时发出。'),
    # sync/mpsc
    ('Creates a bounded mpsc channel for communicating between asynchronous tasks with backpressure.',
     '创建一个有界 mpsc channel，用于在异步任务之间通过背压（backpressure）进行通信。'),
    ('Creates a bounded mpsc channel for communicating between asynchronous tasks\nwith backpressure.',
     '创建一个有界 mpsc channel，用于在异步任务之间通过背压（backpressure）进行通信。'),
    ('Creates an unbounded mpsc channel for communicating between asynchronous tasks without backpressure.',
     '创建一个无界 mpsc channel，用于在异步任务之间通信（不提供背压）。'),
    ('Creates an unbounded mpsc channel for communicating between asynchronous\ntasks without backpressure.',
     '创建一个无界 mpsc channel，用于在异步任务之间通信（不提供背压）。'),
    ('Owned permit to send one value into the channel.',
     'owned 类型的 permit，用于向 channel 发送一个值。'),
    ('Permits to send one value into the channel.',
     '用于向 channel 发送一个值的 permit。'),
    ('The implementation details described in this section may change in future Tokio releases.',
     '本节所述的实现细节在未来的 Tokio 版本中可能发生变化。'),
    ('A multi-producer, multi-consumer broadcast queue. Each sent value is seen by\nall consumers.',
     '一个多生产者、多消费者的广播队列。每个发送的值都会被所有消费者看到。'),
    ('A multi-producer, multi-consumer broadcast queue. Each sent value is seen by all consumers.',
     '一个多生产者、多消费者的广播队列。每个发送的值都会被所有消费者看到。'),
    ('A bounded channel for sending values between asynchronous tasks.',
     '用于在异步任务之间发送值的有界 channel。'),
    ('A channel for sending values between asynchronous tasks.',
     '用于在异步任务之间发送值的 channel。'),
    ('Named future types.', '命名的 future 类型。'),
    ('A multi-producer, single-consumer queue for sending values between\nasynchronous tasks.',
     '一个多生产者、单消费者的队列，用于在异步任务之间发送值。'),
    ('A multi-producer, single-consumer queue for sending values between asynchronous tasks.',
     '一个多生产者、单消费者的队列，用于在异步任务之间发送值。'),
    ('A one-shot channel is used for sending a single message between\nasynchronous tasks. The channel function is used to create a\nSender and Receiver handle pair that form the channel.',
     '一次性 channel 用于在异步任务之间发送单个消息。channel 函数用于创建一对构成 channel 的 Sender 与 Receiver 句柄。'),
    ('A one-shot channel is used for sending a single message between asynchronous tasks. The channel function is used to create a Sender and Receiver handle pair that form the channel.',
     '一次性 channel 用于在异步任务之间发送单个消息。channel 函数用于创建一对构成 channel 的 Sender 与 Receiver 句柄。'),
    ('A multi-producer, multi-consumer channel that only retains the last sent\nvalue.',
     '一个多生产者、多消费者的 channel，只保留最后发送的值。'),
    ('A multi-producer, multi-consumer channel that only retains the last sent value.',
     '一个多生产者、多消费者的 channel，只保留最后发送的值。'),
    ('Error returned from the Semaphore::acquire function.',
     '由 Semaphore::acquire 函数返回的错误。'),
    ('A barrier enables multiple tasks to synchronize the beginning of some computation.',
     'barrier 用于让多个 task 同步某些计算的起点。'),
    ('A BarrierWaitResult is returned by wait when all tasks in the Barrier have rendezvoused.',
     '当 Barrier 中所有 task 完成汇合时，wait 返回 BarrierWaitResult。'),
    ('A handle to a held Mutex that has had a function applied to it via MutexGuard::map.',
     '对持有的 Mutex 通过 MutexGuard::map 应用了某个函数后得到的句柄。'),
    ('An asynchronous Mutex-like type.', '一个异步 Mutex 类似的类型。'),
    ('A handle to a held Mutex. The guard can be held across any .await point\nas it is Send.',
     '持有的 Mutex 的句柄。guard 可以跨任何 .await 点持有，因为它实现了 Send。'),
    ('A handle to a held Mutex. The guard can be held across any .await point as it is Send.',
     '持有的 Mutex 的句柄。guard 可以跨任何 .await 点持有，因为它实现了 Send。'),
    ('Notifies a single task to wake up.', '通知单个 task 唤醒。'),
    ('A thread-safe cell that can be written to only once.',
     '一个线程安全的 cell，只能写入一次。'),
    ('A owned handle to a held Mutex that has had a function applied to it via\nOwnedMutexGuard::map.',
     '对持有的 Mutex 通过 OwnedMutexGuard::map 应用了某个函数后得到的 owned 句柄。'),
    ('A owned handle to a held Mutex that has had a function applied to it via OwnedMutexGuard::map.',
     '对持有的 Mutex 通过 OwnedMutexGuard::map 应用了某个函数后得到的 owned 句柄。'),
    ('An owned handle to a held Mutex.', '持有的 Mutex 的 owned 句柄。'),
    ('Owned RAII structure used to release the exclusive write access of a lock when\ndropped.',
     'owned 的 RAII 结构，在 drop 时释放锁的独占写访问权限。'),
    ('Owned RAII structure used to release the exclusive write access of a lock when dropped.',
     'owned 的 RAII 结构，在 drop 时释放锁的独占写访问权限。'),
    ('Owned RAII structure used to release the shared read access of a lock when\ndropped.',
     'owned 的 RAII 结构，在 drop 时释放锁的共享读访问权限。'),
    ('Owned RAII structure used to release the shared read access of a lock when dropped.',
     'owned 的 RAII 结构，在 drop 时释放锁的共享读访问权限。'),
    ('An owned permit from the semaphore.', '信号量的 owned permit。'),
    ('An asynchronous reader-writer lock.', '异步读写锁。'),
    ('RAII structure used to release the exclusive write access of a lock when\ndropped.',
     'RAII 结构，在 drop 时释放锁的独占写访问权限。'),
    ('RAII structure used to release the exclusive write access of a lock when dropped.',
     'RAII 结构，在 drop 时释放锁的独占写访问权限。'),
    ('RAII structure used to release the shared read access of a lock when\ndropped.',
     'RAII 结构，在 drop 时释放锁的共享读访问权限。'),
    ('RAII structure used to release the shared read access of a lock when dropped.',
     'RAII 结构，在 drop 时释放锁的共享读访问权限。'),
    ('Counting semaphore performing asynchronous permit acquisition.',
     '执行异步 permit 获取的计数信号量。'),
    ('A permit from the semaphore.', '信号量的 permit。'),
    ('Error that can be returned from SetOnce::set.',
     '可由 SetOnce::set 返回的错误。'),
    ('Error returned from the Mutex::try_lock, RwLock::try_read and\nRwLock::try_write functions.',
     '由 Mutex::try_lock、RwLock::try_read 与 RwLock::try_write 函数返回的错误。'),
    ('Error returned from the Mutex::try_lock, RwLock::try_read and RwLock::try_write functions.',
     '由 Mutex::try_lock、RwLock::try_read 与 RwLock::try_write 函数返回的错误。'),
    ('Errors that can be returned from OnceCell::set.',
     '可由 OnceCell::set 返回的错误。'),
    ('Error returned from the Semaphore::try_acquire function.',
     '由 Semaphore::try_acquire 函数返回的错误。'),
    # sync/broadcast
    ('Broadcast error types', '广播错误类型'),
    ('Receiving-half of the broadcast channel.', '广播 channel 的接收半部。'),
    ('Sending-half of the broadcast channel.', '广播 channel 的发送半部。'),
    ('An error returned from the recv function on a Receiver.',
     '从 Receiver 上的 recv 函数返回的错误。'),
    ('An error returned from the try_recv function on a Receiver.',
     '从 Receiver 上的 try_recv 函数返回的错误。'),
    ('A sender that does not prevent the channel from being closed.',
     '不阻止 channel 被关闭的发送端。'),
    ('An unbounded sender that does not prevent the channel from being closed.',
     '不阻止 channel 被关闭的无界发送端。'),
    ('An Iterator of Permit that can be used to hold n slots in the channel.',
     '一个 Permit 的迭代器，可用于在 channel 中保留 n 个槽位。'),
    ('Error returned by the send function on a Sender.',
     '由 Sender 上的 send 函数返回的错误。'),
    # sync/oneshot
    ('Creates a new one-shot channel for sending single values across asynchronous\ntasks.',
     '创建一个新的一次性 channel，用于跨异步任务发送单个值。'),
    ('Creates a new one-shot channel for sending single values across asynchronous tasks.',
     '创建一个新的一次性 channel，用于跨异步任务发送单个值。'),
    ('Error returned by a Sender::send when the receiving half was dropped.',
     '当接收半部被丢弃时由 Sender::send 返回的错误。'),
    ('The sending-half of Rust’s asynchronous channel type.',
     'Rust 异步 channel 类型的发送半部。'),
    ('The sending-half of Rust’s asynchronous channel type.',
     'Rust 异步 channel 类型的发送半部。'),
    ('The receiving half of a channel to send single values across asynchronous tasks.',
     '用于跨异步任务发送单个值的 channel 的接收半部。'),
    ('Error returned by the Future implementation for Receiver.',
     '由 Receiver 的 Future 实现返回的错误。'),
    ('Error returned by the try_recv function on Receiver.',
     '由 Receiver 上的 try_recv 函数返回的错误。'),
    ('Oneshot error types.', 'oneshot 错误类型。'),
    ('Receives a value from the associated Sender.',
     '从关联的 Sender 接收一个值。'),
    ('Sends a value to the associated Receiver.',
     '向关联的 Receiver 发送一个值。'),
    # sync/mpsc more
    ('Channel error types.', 'channel 错误类型。'),
    ('Receives values from the associated Sender.',
     '从关联的 Sender 接收值。'),
    ('Sends values to the associated Receiver.',
     '向关联的 Receiver 发送值。'),
    ('Receive values from the associated UnboundedSender.',
     '从关联的 UnboundedSender 接收值。'),
    ('Send values to the associated UnboundedReceiver.',
     '向关联的 UnboundedReceiver 发送值。'),
    ('Error returned by Sender::send.', '由 Sender::send 返回的错误。'),
    ('Error returned by Sender::send_timeout.', '由 Sender::send_timeout 返回的错误。'),
    ('Error returned by Receiver::try_recv.', '由 Receiver::try_recv 返回的错误。'),
    ('Error returned by Sender::try_send.', '由 Sender::try_send 返回的错误。'),
    ('Create a bounded, multi-producer, multi-consumer channel where each sent\nvalue is broadcasted to all active receivers.',
     '创建一个有界的多生产者、多消费者的 channel，每个发送的值都会广播给所有活跃的接收者。'),
    ('Create a bounded, multi-producer, multi-consumer channel where each sent value is broadcasted to all active receivers.',
     '创建一个有界的多生产者、多消费者的 channel，每个发送的值都会广播给所有活跃的接收者。'),
    # sync/watch
    ('Creates a new watch channel, returning the “send” and “receive” handles.',
     '创建一个新的 watch channel，返回"发送"与"接收"句柄。'),
    ('Creates a new watch channel, returning the “send” and “receive” handles.',
     '创建一个新的 watch channel，返回"发送"与"接收"句柄。'),
    ('Watch error types.', 'watch 错误类型。'),
    ('Error produced when receiving a change notification.',
     '接收变更通知时产生的错误。'),
    ('Error produced when sending a value fails.',
     '发送值失败时产生的错误。'),
    ('Returns a reference to the inner value.', '返回内部值的引用。'),
    # task
    ('A collection of tasks spawned on a Tokio runtime.',
     '在 Tokio runtime 上生成的 task 集合。'),
    ('A future that sets a value T of a task local for the future F during\nits execution.',
     '一个 future，在 future F 执行期间设置 task local 的一个值 T。'),
    ('A future that sets a value T of a task local for the future F during its execution.',
     '一个 future，在 future F 执行期间设置 task local 的一个值 T。'),
    ('A key for task-local data.', 'task-local 数据的 key。'),
    ('An opaque ID that uniquely identifies a task relative to all other currently\nrunning tasks.',
     '一个不透明的 ID，相对于所有其他当前正在运行的 task 唯一标识一个 task。'),
    ('An opaque ID that uniquely identifies a task relative to all other currently running tasks.',
     '一个不透明的 ID，相对于所有其他当前正在运行的 task 唯一标识一个 task。'),
    ('An owned permission to abort a spawned task, without awaiting its completion.',
     '用于中止已生成 task 的 owned 权限，无需等待其完成。'),
    ('An owned permission to join on a task (await its termination).',
     '用于 join（等待终止）一个 task 的 owned 权限。'),
    ('A set of tasks which are executed on the same thread.',
     '在同一线程上执行的 task 集合。'),
    ('Utilities for improved cooperative scheduling.',
     '用于改进协作调度的工具。'),
    ('Task-related futures.', '与 task 相关的 future。'),
    ('Task failed to execute to completion.',
     'task 未能执行完毕。'),
    ('Context guard for LocalSet', 'LocalSet 的上下文守护'),
    ('Returns the Id of the currently running task.',
     '返回当前正在运行的 task 的 Id。'),
    ('Returns the Id of the currently running task, or None if called outside\nof a task.',
     '返回当前正在运行的 task 的 Id，如果在 task 之外调用则返回 None。'),
    ('Returns the Id of the currently running task, or None if called outside of a task.',
     '返回当前正在运行的 task 的 Id，如果在 task 之外调用则返回 None。'),
    ('Spawns a new asynchronous task, returning a\nJoinHandle for it.',
     '生成一个新的异步 task，并返回它的 JoinHandle。'),
    ('Spawns a new asynchronous task, returning a JoinHandle for it.',
     '生成一个新的异步 task，并返回它的 JoinHandle。'),
    ('Runs the provided closure on a thread where blocking is acceptable.',
     '在允许阻塞的线程上运行提供的闭包。'),
    ('Spawns a !Send future on the current LocalSet or LocalRuntime.',
     '在当前 LocalSet 或 LocalRuntime 上生成一个 !Send 的 future。'),
    ('Yields execution back to the Tokio runtime.',
     '将执行权交还给 Tokio runtime。'),
    # task/coop
    ('Consumes a unit of budget and returns the execution back to the Tokio\nruntime if the task’s coop budget was exhausted.',
     '消耗一个单位的预算，如果 task 的协作预算已用完则将执行权归还给 Tokio runtime。'),
    ('Consumes a unit of budget and returns the execution back to the Tokio runtime if the task’s coop budget was exhausted.',
     '消耗一个单位的预算，如果 task 的协作预算已用完则将执行权归还给 Tokio runtime。'),
    ('Decrements the task budget and returns Poll::Pending if the budget is depleted.\nThis indicates that the task should yield to the scheduler. Otherwise, returns\nRestoreOnPending which can be used to commit the budget consumption.',
     '如果 task 预算已耗尽则递减 task 预算并返回 Poll::Pending。这表示 task 应该让出执行权给调度器；否则返回 RestoreOnPending，可用于提交预算消耗。'),
    ('Decrements the task budget and returns Poll::Pending if the budget is depleted. This indicates that the task should yield to the scheduler. Otherwise, returns RestoreOnPending which can be used to commit the budget consumption.',
     '如果 task 预算已耗尽则递减 task 预算并返回 Poll::Pending。这表示 task 应该让出执行权给调度器；否则返回 RestoreOnPending，可用于提交预算消耗。'),
    ('Creates a wrapper future that makes the inner future cooperate with the Tokio scheduler.',
     '创建一个包装 future，使内部 future 与 Tokio 调度器协作。'),
    ('Future wrapper to ensure cooperative scheduling created by cooperative.',
     '由 cooperative 创建的、用于确保协作调度的 future 包装。'),
    ('Value returned by the poll_proceed method.',
     '由 poll_proceed 方法返回的值。'),
    ('Future for the unconstrained method.',
     '用于 unconstrained 方法的 future。'),
    ('Returns true if there is still budget left on the task.',
     '如果 task 上还有剩余预算则返回 true。'),
    ('Turn off cooperative scheduling for a future. The future will never be forced to yield by\nTokio. Using this exposes your',
     '为某个 future 关闭协作调度。该 future 永远不会被 Tokio 强制让出执行权。使用它会暴露你的'),
    ('Turn off cooperative scheduling for a future. The future will never be forced to yield by Tokio. Using this exposes your',
     '为某个 future 关闭协作调度。该 future 永远不会被 Tokio 强制让出执行权。使用它会暴露你的'),
    # task/futures
    ('Future returned from Notify::notified().', '由 Notify::notified() 返回的 future。'),
    ('Future returned from Notify::notified_owned().', '由 Notify::notified_owned() 返回的 future。'),
    # time
    ('A measurement of a monotonically nondecreasing clock.\nOpaque and useful only with Duration.',
     '一个单调递增时钟的度量。不透明，仅与 Duration 配合使用。'),
    ('A measurement of a monotonically nondecreasing clock. Opaque and useful only with Duration.',
     '一个单调递增时钟的度量。不透明，仅与 Duration 配合使用。'),
    ('Creates new Interval that yields with interval of period. The first\ntick completes immediately. The default MissedTickBehavior is\nBurst, but this can be configured\nby calling set_missed_tick_behavior.',
     '创建一个新的 Interval，按 period 间隔产生 yield。第一次 tick 立即完成。默认的 MissedTickBehavior 是 Burst，但可通过调用 set_missed_tick_behavior 来配置。'),
    ('Creates new Interval that yields with interval of period. The first tick completes immediately. The default MissedTickBehavior is Burst, but this can be configured by calling set_missed_tick_behavior.',
     '创建一个新的 Interval，按 period 间隔产生 yield。第一次 tick 立即完成。默认的 MissedTickBehavior 是 Burst，但可通过调用 set_missed_tick_behavior 来配置。'),
    ('Creates new Interval that yields with interval of period with the\nfirst tick completing at start. The default MissedTickBehavior is\nBurst, but this can be configured\nby calling set_missed_tick_behavior.',
     '创建一个新的 Interval，按 period 间隔产生 yield，第一次 tick 在 start 时立即完成。默认的 MissedTickBehavior 是 Burst，但可通过调用 set_missed_tick_behavior 来配置。'),
    ('Creates new Interval that yields with interval of period with the first tick completing at start. The default MissedTickBehavior is Burst, but this can be configured by calling set_missed_tick_behavior.',
     '创建一个新的 Interval，按 period 间隔产生 yield，第一次 tick 在 start 时立即完成。默认的 MissedTickBehavior 是 Burst，但可通过调用 set_missed_tick_behavior 来配置。'),
    ('Interval returned by interval and interval_at.',
     '由 interval 和 interval_at 返回的 Interval。'),
    ('Future returned by sleep and sleep_until.', '由 sleep 和 sleep_until 返回的 future。'),
    ('Future returned by timeout and timeout_at.', '由 timeout 和 timeout_at 返回的 future。'),
    ('Defines the behavior of an Interval when it misses a tick.',
     '定义 Interval 在错过一次 tick 时的行为。'),
    ('Waits until duration has elapsed.', '等待直到指定的 duration 已过去。'),
    ('Waits until deadline is reached.', '等待直到到达指定的 deadline。'),
    ('Requires a Future to complete before the specified duration has elapsed.',
     '要求某个 Future 在指定的 duration 内完成。'),
    ('Requires a Future to complete before the specified instant in time.',
     '要求某个 Future 在指定的时刻之前完成。'),
    ('Time error types.', '时间错误类型。'),
    ('Errors returned by Timeout.', '由 Timeout 返回的错误。'),
    ('Errors encountered by the timer implementation.', '定时器实现所遇到的错误。'),
    # net util
    ('Tokio runtime’s metrics.', 'Tokio runtime 的指标。'),
    # io Interest specifics
    ('Converts or resolves without blocking to one or more SocketAddr values.',
     '非阻塞地转换或解析出一个或多个 SocketAddr 值。'),
    # 缺失的小条目
    ('Requires a `Runtime` or `LocalRuntime` to be set to be able to run futures.',
     '需要一个 `Runtime` 或 `LocalRuntime` 才能运行 future。'),

    # ----- quinn 漏译 -----
    ('Connection errors', '连接错误'),
    ('Cryptographic session identity.', '加密会话身份。'),
    ('Statelessly produce unique outbound streams',
     '无状态地产生唯一的出站流'),
    ('Long-lived futures on top of Quinn connections',
     '基于 Quinn 连接的长生命周期 future'),

    # ----- bytes 漏译 -----
    ('Utilities for the `Bytes` type.', '`Bytes` 类型的工具方法。'),
    ('A unique identifier for blocking operations',
     '阻塞操作的唯一标识符'),
    ('Traits for working with buffers.', '用于处理缓冲区的 trait。'),

    # ----- rustls_pki_types 漏译 -----
    ('The PKIX AlgorithmIdentifier type, and common values.',
     'PKIX AlgorithmIdentifier 类型及其常用取值。'),
    ('Low-level PEM decoding APIs.', '底层 PEM 解码 API。'),
    ('Failure to parse an IP address', '解析 IP 地址失败'),
    ('A DER-encoded X.509 certificate; as specified in RFC 5280',
     'DER 编码的 X.509 证书；按 RFC 5280 规定'),
    ('DER-encoded data, either owned or borrowed', 'DER 编码的数据，可以是 owned 或 borrowed'),
    ('A type which encapsulates a string (borrowed or owned) that is a syntactically valid DNS name.',
     '一个封装字符串（借用或拥有）的类型，其内容在语法上是合法的 DNS 名。'),
    ('A TLS-encoded Encrypted Client Hello (ECH) configuration list (ECHConfigList); as specified in RFC 9849 §4',
     'TLS 编码的 Encrypted Client Hello (ECH) 配置列表（ECHConfigList）；按 RFC 9849 §4 规定'),
    ('A TLS-encoded Encrypted Client Hello (ECH) configuration list (ECHConfigList); as specified in\nRFC 9849 §4',
     'TLS 编码的 Encrypted Client Hello (ECH) 配置列表（ECHConfigList）；按 RFC 9849 §4 规定'),
    ('The provided input could not be parsed because it is not a syntactically-valid DNS Name.',
     '提供的输入无法解析，因为它不是语法上合法的 DNS 名。'),
    ('The provided input could not be parsed because\nit is not a syntactically-valid DNS Name.',
     '提供的输入无法解析，因为它不是语法上合法的 DNS 名。'),
    ('A detail-less error when a signature is not valid.',
     '签名无效时返回的、无详细信息的错误。'),
    ('no_std implementation of std::net::Ipv4Addr.',
     'no_std 实现的 std::net::Ipv4Addr。'),
    ('no_std implementation of std::net::Ipv6Addr.',
     'no_std 实现的 std::net::Ipv6Addr。'),
    ('A DER-encoded plaintext RSA private key; as specified in PKCS#1/RFC 3447',
     'DER 编码的明文 RSA 私钥；按 PKCS#1/RFC 3447 规定'),
    ('A DER-encoded plaintext private key; as specified in PKCS#8/RFC 5958',
     'DER 编码的明文私钥；按 PKCS#8/RFC 5958 规定'),
    ('A DER-encoded SubjectPublicKeyInfo (SPKI), as specified in RFC 5280.',
     'DER 编码的 SubjectPublicKeyInfo (SPKI)，按 RFC 5280 规定。'),
    ('A trust anchor (a.k.a. root CA)', '一个信任锚（即根 CA）'),
    ('A timestamp, tracking the number of non-leap seconds since the Unix epoch.',
     '一个时间戳，记录自 Unix 纪元以来的非闰秒数。'),
    ('FIPS validation status of an algorithm or implementation.',
     '算法或实现的 FIPS 验证状态。'),
    ('no_std implementation of std::net::IpAddr.',
     'no_std 实现的 std::net::IpAddr。'),
    ('A DER-encoded X.509 private key, in one of several formats',
     'DER 编码的 X.509 私钥，格式为其中之一'),
    ('Encodes ways a client can know the expected name of the server.',
     '编码客户端可以知道服务端预期名称的方式。'),
    ('An abstract signature verification algorithm.',
     '一个抽象的签名验证算法。'),
    # alg_id
    ('A DER encoding of the PKIX AlgorithmIdentifier type:',
     'PKIX AlgorithmIdentifier 类型的 DER 编码：'),
    ('AlgorithmIdentifier for id-ecPublicKey with named curve secp256r1.',
     '使用 secp256r1 命名曲线的 id-ecPublicKey 的 AlgorithmIdentifier。'),
    ('AlgorithmIdentifier for id-ecPublicKey with named curve secp384r1.',
     '使用 secp384r1 命名曲线的 id-ecPublicKey 的 AlgorithmIdentifier。'),
    ('AlgorithmIdentifier for id-ecPublicKey with named curve secp521r1.',
     '使用 secp521r1 命名曲线的 id-ecPublicKey 的 AlgorithmIdentifier。'),
    ('AlgorithmIdentifier for id-ecPublicKey with named curve secp256k1.',
     '使用 secp256k1 命名曲线的 id-ecPublicKey 的 AlgorithmIdentifier。'),
    ('AlgorithmIdentifier for ecdsa-with-SHA256.', 'ecdsa-with-SHA256 的 AlgorithmIdentifier。'),
    ('AlgorithmIdentifier for ecdsa-with-SHA384.', 'ecdsa-with-SHA384 的 AlgorithmIdentifier。'),
    ('AlgorithmIdentifier for ecdsa-with-SHA512.', 'ecdsa-with-SHA512 的 AlgorithmIdentifier。'),
    ('AlgorithmIdentifier for ED448.', 'ED448 的 AlgorithmIdentifier。'),
    ('AlgorithmIdentifier for ED25519.', 'ED25519 的 AlgorithmIdentifier。'),
    ('AlgorithmIdentifier for id-ml-dsa-44.', 'id-ml-dsa-44 的 AlgorithmIdentifier。'),
    ('AlgorithmIdentifier for id-ml-dsa-65.', 'id-ml-dsa-65 的 AlgorithmIdentifier。'),
    ('AlgorithmIdentifier for id-ml-dsa-87.', 'id-ml-dsa-87 的 AlgorithmIdentifier。'),
    ('AlgorithmIdentifier for rsaEncryption.', 'rsaEncryption 的 AlgorithmIdentifier。'),
    ('AlgorithmIdentifier for sha256WithRSAEncryption.', 'sha256WithRSAEncryption 的 AlgorithmIdentifier。'),
    ('AlgorithmIdentifier for sha384WithRSAEncryption.', 'sha384WithRSAEncryption 的 AlgorithmIdentifier。'),
    ('AlgorithmIdentifier for sha512WithRSAEncryption.', 'sha512WithRSAEncryption 的 AlgorithmIdentifier。'),
    ('AlgorithmIdentifier for rsassaPss with:', 'rsassaPss 的 AlgorithmIdentifier，参数为：'),
    # pem
    ('Extract and return all PEM sections by reading rd.', '通过读取 rd 提取并返回所有 PEM section。'),
    ('Iterator over all PEM sections in a &[u8] slice.', '对 &[u8] 切片中所有 PEM section 进行迭代的迭代器。'),
    ('Iterator over all PEM sections in a &amp;[u8] slice.', '对 &amp;[u8] 切片中所有 PEM section 进行迭代的迭代器。'),
    ('Errors that may arise when parsing the contents of a PEM file',
     '解析 PEM 文件内容时可能产生的错误'),
    ('A single recognised section in a PEM file.', 'PEM 文件中一个被识别的 section。'),
    ('Items that can be decoded from PEM data.', '可以从 PEM 数据解码出的条目。'),
    ('Extract and decode the next supported PEM section from rd.',
     '从 rd 中提取并解码下一个支持的 PEM section。'),

    # ----- 章节标题（h3-heading） -----
    ('WASM support', 'WASM 支持'),
    ('Unstable WASM support', '不稳定 WASM 支持'),
    ('Buffered Readers and Writers', '带缓冲的 Readers 与 Writers'),
    ('Implementing AsyncRead and AsyncWrite', '实现 AsyncRead 与 AsyncWrite'),
    ('Conversion to and from Stream/Sink', 'Stream/Sink 之间的相互转换'),
    ('Bridging with sync code', '与同步代码桥接'),
    ('NUMA awareness', 'NUMA 感知'),
    ('Runtime Configurations', 'Runtime 配置'),
    ('Driving the runtime', '驱动 runtime'),
    ('Lifetime of spawned threads', '生成线程的生命周期'),
    ('IO and timers', 'IO 与定时器'),
    ('Current thread runtime (behavior at the time of writing)',
     '当前线程 runtime（撰写本文时的行为）'),
    ('Multi threaded runtime (behavior at the time of writing)',
     '多线程 runtime（撰写本文时的行为）'),
    ('File descriptor table pre-warming', '文件描述符表的预热'),
    ('Limit the number of simultaneously opened files in your program',
     '限制程序中同时打开的文件数'),
    ('Limit the number of outgoing requests being sent at the same time',
     '限制同时发送的出站请求数'),
    ('Limit the number of incoming requests being handled at the same time',
     '限制同时处理的入站请求数'),
    ('Prevent tests from running in parallel', '防止测试并行运行'),
    ('Rate limiting using a token bucket', '使用令牌桶进行限流'),
    ('Lagging', '延迟（lagging）'),
    ('Closing', '关闭（closing）'),
    ('Change notifications', '变更通知'),
    ('changed versus has_changed', 'changed 与 has_changed 的对比'),
    ('borrow_and_update versus borrow', 'borrow_and_update 与 borrow 的对比'),
    ('Non-guarantees', '非保证'),
    ('What are Tasks?', '什么是 Task？'),
    ('Working with Tasks', '使用 Task'),
    ('Awaiting a LocalSet', '等待 LocalSet'),
    ('Use inside tokio::spawn', '在 tokio::spawn 内部使用'),

    # ----- chrome 标签（h2-section-header） -----
    ('>Tuple Fields<', '>元组字段<'),
    ('>Variants (Non-exhaustive)<', '>变体（非穷尽）<'),
    ('>Fields (Non-exhaustive)<', '>字段（非穷尽）<'),
    # 标签后跟 anchor（不带 > 边界）：
    ('Tuple Fields', '元组字段'),
    ('Variants (Non-exhaustive)', '变体（非穷尽）'),
    ('Fields (Non-exhaustive)', '字段（非穷尽）'),
    # 修复 chrome 翻译 bug：把 "Traits" 误翻成 "trait"
    ('>trait<', '>特性<'),
    # quinn crypto descriptions
    ('Authentication data for (rustls) TLS session',
     '（rustls）TLS 会话的身份认证数据。'),
    ('The initial cipher suite (AES-128-GCM-SHA256) is not available',
     '初始 cipher suite（AES-128-GCM-SHA256）不可用'),
    ('A QUIC-compatible TLS client configuration',
     '一个兼容 QUIC 的 TLS 客户端配置。'),
    ('A QUIC-compatible TLS server configuration',
     '一个兼容 QUIC 的 TLS 服务端配置。'),
    ('A rustls TLS session', '一个 rustls TLS 会话。'),
    ('rustls reports protocol errors using this type.',
     'rustls 通过此类型上报协议错误。'),
    ('QUIC Token', 'QUIC Token'),

    # ----- 补充 dd 条目 -----
    ('TCP utility types.', 'TCP 工具类型。'),
    ('Windows specific network types.', 'Windows 专用网络类型。'),
    # ----- 补充 h3-heading 条目 -----
    ('DER and PEM', 'DER 与 PEM'),
    ('Creating new certificates and keys', '创建新的证书与密钥'),
    ('Cloning private keys', '克隆私钥'),
    ('or, alternatively…', '或者，也可以这样…'),
    ('or, alternatively...', '或者，也可以这样…'),
]


def replace_inline_tags_with_placeholders(html_str):
    """把 inline HTML 标签（包括 <code>...</code>、<a>...</a>、<em>、<wbr/> 等）
    替换为占位符 \x01N\x02，使得相邻的纯文本可以拼成连续的字符串。"""
    # 记录每个占位符对应的原始 HTML
    placeholders = []
    out = []
    i = 0
    n = 0
    while i < len(html_str):
        if html_str[i] == '<':
            # 找匹配的 >，但跳过引号内的 >（如 attribute values 里的）
            j = i + 1
            in_attr = False
            quote_char = None
            while j < len(html_str):
                ch = html_str[j]
                if quote_char:
                    if ch == quote_char:
                        quote_char = None
                else:
                    if ch in ('"', "'"):
                        quote_char = ch
                    elif ch == '>':
                        break
                j += 1
            if j < len(html_str):
                tag = html_str[i:j+1]
                ph = f'\x01{n}\x02'
                placeholders.append(tag)
                out.append(ph)
                n += 1
                i = j + 1
            else:
                out.append(html_str[i])
                i += 1
        else:
            out.append(html_str[i])
            i += 1
    return ''.join(out), placeholders


def restore_placeholders(text, placeholders):
    """把占位符替换回原来的 HTML 标签。"""
    result = []
    i = 0
    while i < len(text):
        if text[i] == '\x01':
            j = text.find('\x02', i)
            if j < 0:
                result.append(text[i])
                i += 1
                continue
            try:
                idx = int(text[i+1:j])
                result.append(placeholders[idx])
            except (ValueError, IndexError):
                result.append(text[i:j+1])
            i = j + 1
        else:
            result.append(text[i])
            i += 1
    return ''.join(result)


def translate_inner_html(inner_html, pairs, stats):
    """翻译一段 dd 内 HTML，做占位符替换再恢复。

    策略：
    1. 把 inline 标签替换为占位符 \x01N\x02
    2. 构建一个组合 regex（含所有 pairs，每个字符间允许任意占位符）
    3. 一次 subn 替换
    """
    placeholdered, tags = replace_inline_tags_with_placeholders(inner_html)
    PH_ANY = r'\x01\d+\x02*'

    if not pairs:
        return inner_html

    local_changes = [0]

    def build_pattern(en):
        escaped = re.escape(en)
        parts = []
        i = 0
        while i < len(escaped):
            if escaped[i] == '\\':
                parts.append(escaped[i:i+2])
                i += 2
            else:
                parts.append(escaped[i])
                i += 1
        return ''.join(p + PH_ANY for p in parts)

    # 按 en 长度分桶：先匹配长的（避免短字符串部分匹配长字符串）
    len_buckets = {}
    for en, zh in pairs:
        len_buckets.setdefault(len(en), []).append((en, zh))

    new_placeholdered = placeholdered
    # 按长度从大到小处理
    for length, bucket in sorted(len_buckets.items(), key=lambda x: -x[0]):
        # 按长度桶构建一个 regex（按 en 长度再次排序）
        sorted_bucket = sorted(bucket, key=lambda x: -len(x[0]))
        pattern_parts = []
        en_to_zh = {}
        for idx, (en, zh) in enumerate(sorted_bucket):
            pattern_parts.append(f'(?P<E{idx}>{build_pattern(en)})')
            en_to_zh[f'E{idx}'] = (en, zh)
        big_pattern = '|'.join(pattern_parts)
        try:
            compiled = re.compile(big_pattern)
        except re.error:
            continue

        def make_replacer(bucket_dict):
            def replace_match(m):
                for name, (en, zh) in bucket_dict.items():
                    if m.group(name):
                        stats[(en, zh)] = stats.get((en, zh), 0) + 1
                        local_changes[0] += 1
                        return zh
                return m.group(0)
            return replace_match

        replacer = make_replacer(en_to_zh)
        # 反复替换直到没有变化
        prev = None
        while prev != new_placeholdered:
            prev = new_placeholdered
            new_placeholdered = compiled.sub(replacer, new_placeholdered)

    if local_changes[0] > 0:
        return restore_placeholders(new_placeholdered, tags)
    return inner_html


def translate_dd_inner_html(dd_elem, pairs, stats):
    """翻译一个 dd 元素的 inner HTML。"""
    # 直接取 dd 的 inner HTML（不包含外层 <dd> 标签）
    inner = dd_elem.decode_contents()
    new_inner = translate_inner_html(inner, pairs, stats)
    if new_inner != inner:
        # 用 new_inner 替换 dd 的内部内容
        dd_elem.clear()
        # 重新解析 new_inner 为 soup 片段
        from bs4 import BeautifulSoup as BS
        fragment = BS(new_inner, 'html.parser')
        for child in fragment.contents:
            dd_elem.append(child.extract() if hasattr(child, 'extract') else child)
        return True
    return False


def main():
    if len(sys.argv) < 2:
        print('Usage: _translate_with_bs4.py <crate_dir> [--apply]')
        sys.exit(1)
    crate_dir = sys.argv[1]
    apply_mode = '--apply' in sys.argv
    dry_run = not apply_mode

    if dry_run:
        print('=== Dry-run (default). Use --apply to write. ===')

    pairs = TRANSLATION_PAIRS
    print(f'\nLoaded {len(pairs)} translation pairs.\n')

    total_replacements = 0
    files_modified = 0
    pair_stats = {}
    SKIP = {'static.files', 'search.index', 'src', '_common_tools', '.git'}

    for top, dirs, fs in os.walk(crate_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in SKIP and not d.endswith('_old')]
        for fn in fs:
            if not fn.endswith('.html'):
                continue
            path = os.path.join(top, fn)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            soup = BeautifulSoup(content, 'html.parser')
            file_changes = 0

            # 翻译 <dd>
            for dd in soup.find_all('dd'):
                if translate_dd_inner_html(dd, pairs, pair_stats):
                    file_changes += 1

            # 翻译 h2/h3（不含 code 标签的）
            for h in soup.find_all(['h2', 'h3']):
                if h.find('code'):
                    continue
                inner = h.decode_contents()
                new_inner = translate_inner_html(inner, pairs, pair_stats)
                if new_inner != inner:
                    h.clear()
                    fragment = BeautifulSoup(new_inner, 'html.parser')
                    for child in fragment.contents:
                        h.append(child.extract() if hasattr(child, 'extract') else child)
                    file_changes += 1

            # 翻译 <details class="toggle top-doc"> 内的 <p> 文本节点
            for details in soup.find_all('details', class_='toggle'):
                if 'top-doc' not in details.get('class', []):
                    continue
                for p in details.find_all('p'):
                    # 跳过纯代码：含 <code> 子节点的视为代码示例
                    if p.find('code'):
                        continue
                    # 跳过位于 <pre> 内的
                    parent_pre = p.find_parent('pre')
                    if parent_pre is not None:
                        continue
                    inner = p.decode_contents()
                    new_inner = translate_inner_html(inner, pairs, pair_stats)
                    if new_inner != inner:
                        p.clear()
                        fragment = BeautifulSoup(new_inner, 'html.parser')
                        for child in fragment.contents:
                            p.append(child.extract() if hasattr(child, 'extract') else child)
                        file_changes += 1

            if file_changes > 0:
                files_modified += 1
                total_replacements += file_changes
                if apply_mode:
                    new_content = str(soup)
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                print(f'  {path}: {file_changes} modifications')

    print(f'\n=== Summary ===')
    print(f'Total replacements: {total_replacements}')
    print(f'Files modified: {files_modified}')
    print(f'\nHits per pair:')
    for (en, zh), cnt in sorted(pair_stats.items(), key=lambda x: -x[1]):
        if cnt > 0:
            print(f'  [{cnt:4d}x] {en[:60]!r}  →  {zh[:40]!r}')


if __name__ == '__main__':
    main()