#!/usr/bin/env python3
"""批量翻译 rustdoc HTML 中模块索引（<dl class="item-table"> <dd>）和
子章节标题（<h3> / <h2>）里的英文描述。

填补 _strict_p_audit.py 漏检的翻译盲区。
设计为所有已翻译 crate 共用一份词典，每条 entry 是 (en_text, zh_text) 二元组。

使用方法：
    python _common_tools/_translate_module_descriptions.py <crate_dir> [--report] [--apply]

--report   只列出命中的英文文本（不替换）
--apply    真正替换文件
默认是 dry-run（只统计命中次数）

约定：
- bytes 模式，避免 CRLF/LF 问题
- 长字符串优先匹配（避免前缀冲突）
- 替换前打印所有命中条目供审查
"""
import os
import re
import sys


# ====== 词典（English → 中文） ======
# 通用模块索引描述（item-table-dd）
TRANSLATION_PAIRS = [
    # ----- tokio 漏译 -----
    # === tokio/io ===
    ('A wrapper around a byte buffer that is incrementally filled and initialized.',
     '一个字节缓冲区的封装，会被增量填充和初始化。'),
    ('Describes the readiness state of an I/O resources.',
     '描述 I/O 资源的就绪状态。'),
    ('Reads bytes asynchronously.', '异步地读取字节。'),
    ('Reads bytes from a source.', '从一个数据源异步地读取字节。'),
    ('Seek bytes asynchronously.', '异步地定位字节。'),
    ('Writes bytes asynchronously.', '异步地写入字节。'),
    ('Readiness event interest.', '就绪事件兴趣位。'),

    # === tokio/net ===
    ('TCP utility types.', 'TCP 工具类型。'),
    ('Windows specific network types.', 'Windows 专用网络类型。'),
    ('A TCP socket server, listening for connections.',
     '一个 TCP socket 服务端，用于监听连接。'),
    ('A TCP socket that has not yet been converted to a TcpStream or\r\nTcpListener.',
     '一个尚未转换为 TcpStream 或 TcpListener 的 TCP socket。'),
    ('A TCP socket that has not yet been converted to a TcpStream or\nTcpListener.',
     '一个尚未转换为 TcpStream 或 TcpListener 的 TCP socket。'),
    ('A TCP stream between a local and a remote socket.',
     '本地与远端 socket 之间的 TCP 流。'),
    ('A UDP socket.', '一个 UDP socket。'),
    ('Converts or resolves without blocking to one or more SocketAddr values.',
     '非阻塞地转换或解析出一个或多个 SocketAddr 值。'),
    ('Performs a DNS resolution.', '执行 DNS 解析。'),

    # === tokio/net/tcp ===
    ('Owned read half of a TcpStream, created by into_split.',
     'TcpStream 的 owned 读半部，由 into_split 创建。'),
    ('Owned write half of a TcpStream, created by into_split.',
     'TcpStream 的 owned 写半部，由 into_split 创建。'),
    ('Borrowed read half of a TcpStream, created by split.',
     'TcpStream 的借用读半部，由 split 创建。'),
    ('Borrowed write half of a TcpStream, created by split.',
     'TcpStream 的借用写半部，由 split 创建。'),
    ('Error indicating that two halves were not from the same socket, and thus could\r\nnot be reunited.',
     '指示两半部分不是来自同一个 socket、因此无法重新合并的错误。'),
    ('Error indicating that two halves were not from the same socket, and thus could\nnot be reunited.',
     '指示两半部分不是来自同一个 socket、因此无法重新合并的错误。'),
    ('Error indicating that two halves were not from the same socket, and thus could not be reunited.',
     '指示两半部分不是来自同一个 socket、因此无法重新合并的错误。'),

    # === tokio/net/windows ===
    ('Tokio support for Windows named pipes.',
     'Tokio 对 Windows 命名管道的支持。'),

    # === tokio/net/windows/named_pipe ===
    ('A builder suitable for building and interacting with named pipes from the\r\nclient side.',
     '一个构建器，用于从客户端构建命名管道并与之交互。'),
    ('A builder suitable for building and interacting with named pipes from the\nclient side.',
     '一个构建器，用于从客户端构建命名管道并与之交互。'),
    ('A builder suitable for building and interacting with named pipes from the client side.',
     '一个构建器，用于从客户端构建命名管道并与之交互。'),
    ('A builder structure for construct a named pipe with named pipe-specific\r\noptions. This is required to use for named pipe servers who wants to modify\r\npipe-related options.',
     '一个构建器结构，用于构造带有命名管道特定选项的命名管道。需要修改管道相关选项的命名管道服务端必须使用它。'),
    ('A builder structure for construct a named pipe with named pipe-specific\noptions. This is required to use for named pipe servers who wants to modify\npipe-related options.',
     '一个构建器结构，用于构造带有命名管道特定选项的命名管道。需要修改管道相关选项的命名管道服务端必须使用它。'),
    ('A Windows named pipe client.', '一个 Windows 命名管道客户端。'),
    ('A Windows named pipe server.', '一个 Windows 命名管道服务端。'),
    ('Information about a named pipe.', '命名管道的相关信息。'),
    ('A builder structure for construct a named pipe with named pipe-specific\noptions. This is required to use for named pipe ',
     '一个构建器结构，用于构造带有命名管道特定选项的命名管道。使用命名管道 '),
    ('A builder structure for construct a named pipe with named pipe-specific options. This is required to use for named pipe ',
     '一个构建器结构，用于构造带有命名管道特定选项的命名管道。使用命名管道 '),
    ('Indicates the end of a named pipe.', '指示命名管道的端点。'),
    ('The pipe mode of a named pipe.', '命名管道的管道模式。'),

    # === tokio/runtime ===
    ('Builds Tokio Runtime with custom configuration values.',
     '使用自定义配置值构建 Tokio Runtime。'),
    ('Runtime context guard.', 'Runtime 上下文守护。'),
    ('Handle to the runtime.', 'runtime 的句柄。'),
    ('An opaque ID that uniquely identifies a runtime relative to all other currently\r\nrunning runtimes.',
     '一个不透明的 ID，相对于所有其他当前正在运行的 runtimes 唯一标识一个 runtime。'),
    ('An opaque ID that uniquely identifies a runtime relative to all other currently\nrunning runtimes.',
     '一个不透明的 ID，相对于所有其他当前正在运行的 runtimes 唯一标识一个 runtime。'),
    ('An opaque ID that uniquely identifies a runtime relative to all other currently running runtimes.',
     '一个不透明的 ID，相对于所有其他当前正在运行的 runtimes 唯一标识一个 runtime。'),
    ('LocalRuntime-only config options', 'LocalRuntime 专用配置选项'),
    ('A local Tokio runtime.', '一个本地 Tokio runtime。'),
    ('The Tokio runtime.', 'Tokio runtime。'),
    ('Handle to the runtime’s metrics.', 'runtime 的指标句柄。'),
    ("Handle to the runtime’s metrics.", 'runtime 的指标句柄。'),
    ('Error returned by try_current when no Runtime has been started',
     '当尚未启动任何 Runtime 时由 try_current 返回的错误'),
    ('The flavor of a Runtime.', 'Runtime 的风格（flavor）。'),
    ('Checks whether the given error was emitted by Tokio when shutting down its runtime.',
     '检查给定的错误是否由 Tokio 在关闭其 runtime 时发出。'),

    # === tokio/sync ===
    ('A multi-producer, multi-consumer broadcast queue. Each sent value is seen by\r\nall consumers.',
     '一个多生产者、多消费者的广播队列。每个发送的值都会被所有消费者看到。'),
    ('A multi-producer, multi-consumer broadcast queue. Each sent value is seen by\nall consumers.',
     '一个多生产者、多消费者的广播队列。每个发送的值都会被所有消费者看到。'),
    ('A multi-producer, multi-consumer broadcast queue. Each sent value is seen by all consumers.',
     '一个多生产者、多消费者的广播队列。每个发送的值都会被所有消费者看到。'),
    ('A bounded channel for sending values between asynchronous tasks.',
     '用于在异步任务之间发送值的有界 channel。'),
    ('A channel for sending values between asynchronous tasks.',
     '用于在异步任务之间发送值的 channel。'),

    # === tokio/sync/mpsc (用户报告的具体例子) ===
    ('Creates a bounded mpsc channel for communicating between asynchronous tasks with backpressure.',
     '创建一个有界 mpsc channel，用于在异步任务之间通过背压（backpressure）进行通信。'),
    ('Creates an unbounded mpsc channel for communicating between asynchronous tasks without backpressure.',
     '创建一个无界 mpsc channel，用于在异步任务之间通信（不提供背压）。'),
    ('Owned permit to send one value into the channel.',
     'owned 类型的 permit，用于向 channel 发送一个值。'),
    ('Permits to send one value into the channel.',
     '用于向 channel 发送一个值的 permit。'),
    ('The implementation details described in this section may change in future Tokio releases.',
     '本节所述的实现细节在未来的 Tokio 版本中可能发生变化。'),

    # === tokio/task ===
    ('A future that completes when the runtime shuts down.',
     '一个在 runtime 关闭时完成的 future。'),

    # === tokio/loom (如果存在) ===
    # === tokio/time ===
    ('A future that completes at a specified instant in time.',
     '一个在指定时刻完成的 future。'),
    ('A future that completes after a specified duration has elapsed.',
     '一个在指定时长过后完成的 future。'),
    ('Requires a `Runtime` or `LocalRuntime` to be set to be able to run futures.',
     '需要一个 `Runtime` 或 `LocalRuntime` 才能运行 future。'),

    # === tokio/net (extended) ===
    ('A TCP socket that has not yet been converted to a TcpStream or TcpListener.',
     '一个尚未转换为 TcpStream 或 TcpListener 的 TCP socket。'),
    ('A TCP socket that has not yet been converted to a TcpStream or\r\nTcpListener.',
     '一个尚未转换为 TcpStream 或 TcpListener 的 TCP socket。'),
    ('A TCP socket that has not yet been converted to a TcpStream or\nTcpListener.',
     '一个尚未转换为 TcpStream 或 TcpListener 的 TCP socket。'),
    ('Converts or resolves without blocking to one or more SocketAddr values.',
     '非阻塞地转换或解析出一个或多个 SocketAddr 值。'),

    # === tokio/net/tcp (extended) ===
    ('Owned read half of a TcpStream, created by into_split.',
     'TcpStream 的 owned 读半部，由 into_split 创建。'),
    ('Owned write half of a TcpStream, created by into_split.',
     'TcpStream 的 owned 写半部，由 into_split 创建。'),
    ('Borrowed read half of a TcpStream, created by split.',
     'TcpStream 的 borrowed 读半部，由 split 创建。'),
    ('Borrowed write half of a TcpStream, created by split.',
     'TcpStream 的 borrowed 写半部，由 split 创建。'),

    # === tokio/net/windows ===
    ('Tokio support for Windows named pipes.',
     'Tokio 对 Windows 命名管道的支持。'),

    # === tokio/net/windows/named_pipe ===
    ('A Windows named pipe client.', '一个 Windows 命名管道客户端。'),
    ('A Windows named pipe server.', '一个 Windows 命名管道服务端。'),

    # === tokio/runtime ===
    ('LocalRuntime-only config options', '仅 LocalRuntime 的配置选项'),
    ('Tokio runtime.', 'Tokio runtime。'),
    ('Error returned by try_current when no Runtime has been started',
     '当没有 Runtime 启动时，由 try_current 返回的错误'),
    ('The flavor of a Runtime.', 'Runtime 的运行模式（flavor）。'),

    # === tokio/sync (extended) ===
    ('Named future types.', '命名的 future 类型。'),
    ('A multi-producer, single-consumer queue for sending values between asynchronous tasks.',
     '用于在异步任务之间发送值的多生产者、单消费者队列。'),
    ('A one-shot channel is used for sending a single message between asynchronous tasks. The channel function is used to create a Sender and Receiver.',
     'oneshot channel 用于在异步任务之间发送单个消息。可使用 channel 函数创建 Sender 和 Receiver。'),
    ('A multi-producer, multi-consumer channel that only retains the last sent value.',
     '一个多生产者、多消费者的 channel，仅保留最近一次发送的值。'),
    ('Error returned from the Semaphore::acquire function.',
     '由 Semaphore::acquire 函数返回的错误。'),
    ('A barrier enables multiple tasks to synchronize the beginning of some computation.',
     'Barrier（屏障）使多个 task 能够同步开始某段计算。'),
    ('A BarrierWaitResult is returned by wait when all tasks in the Barrier have rendezvoused.',
     '当 Barrier 中所有 task 都在 wait 处汇合时，wait 返回一个 BarrierWaitResult。'),
    ('A handle to a held Mutex that has had a function applied to it via MutexGuard::map.',
     '对持有的 Mutex 通过 MutexGuard::map 应用函数后得到的句柄。'),
    ('An asynchronous Mutex-like type.', '一个异步的、类似 Mutex 的类型。'),
    ('A handle to a held Mutex. The guard can be held across any .await point as it is Send.',
     '持有的 Mutex 的句柄。由于实现了 Send，可以在任意 .await 点持有该 guard。'),
    ('Notifies a single task to wake up.', '通知单个 task 唤醒。'),
    ('A thread-safe cell that can be written to only once.',
     '一个线程安全的 cell，只能写入一次。'),
    ('A owned handle to a held Mutex that has had a function applied to it via OwnedMutexGuard::map.',
     '对持有的 Mutex 通过 OwnedMutexGuard::map 应用函数后得到的 owned 句柄。'),
    ('An owned handle to a held Mutex.', '持有的 Mutex 的 owned 句柄。'),
    ('Owned RAII structure used to release the exclusive write access of a lock when dropped.',
     'Owned RAII 结构，在 drop 时释放锁的独占写访问。'),
    ('Owned RAII structure used to release the shared read access of a lock when dropped.',
     'Owned RAII 结构，在 drop 时释放锁的共享读访问。'),
    ('An owned permit from the semaphore.', '来自 semaphore 的 owned permit。'),
    ('An asynchronous reader-writer lock.', '一个异步的读者-写者锁。'),
    ('RAII structure used to release the exclusive write access of a lock when dropped.',
     'RAII 结构，在 drop 时释放锁的独占写访问。'),
    ('RAII structure used to release the shared read access of a lock when dropped.',
     'RAII 结构，在 drop 时释放锁的共享读访问。'),
    ('Counting semaphore performing asynchronous permit acquisition.',
     '执行异步 permit 获取的计数信号量（counting semaphore）。'),
    ('A permit from the semaphore.', '来自 semaphore 的 permit。'),
    ('Error that can be returned from SetOnce::set.',
     '可由 SetOnce::set 返回的错误。'),
    ('Error returned from the Mutex::try_lock, RwLock::try_read and RwLock::try_write functions.',
     '由 Mutex::try_lock、RwLock::try_read 和 RwLock::try_write 函数返回的错误。'),
    ('Errors that can be returned from OnceCell::set.',
     '可由 OnceCell::set 返回的错误。'),
    ('Error returned from the Semaphore::try_acquire function.',
     '由 Semaphore::try_acquire 函数返回的错误。'),

    # === tokio/sync/broadcast ===
    ('Broadcast error types', '广播错误类型'),
    ('Receiving-half of the broadcast channel.', 'broadcast channel 的接收端。'),
    ('Sending-half of the broadcast channel.', 'broadcast channel 的发送端。'),
    ('A sender that does not prevent the channel from being closed.',
     '一个 sender，不会阻止 channel 被关闭。'),
    ('Create a bounded, multi-producer, multi-consumer channel where each sent value is broadcasted to all active receivers.',
     '创建一个有界的、多生产者、多消费者的 channel，每个发送的值都会广播给所有活跃的接收者。'),

    # === tokio/sync/broadcast/error ===
    ('Error returned by the send function on a Sender.',
     'Sender 上的 send 函数返回的错误。'),
    ('An error returned from the recv function on a Receiver.',
     'Receiver 上的 recv 函数返回的错误。'),
    ('An error returned from the try_recv function on a Receiver.',
     'Receiver 上的 try_recv 函数返回的错误。'),

    # === tokio/sync/futures ===
    ('Future returned from Notify::notified().',
     '由 Notify::notified() 返回的 future。'),
    ('Future returned from Notify::notified_owned().',
     '由 Notify::notified_owned() 返回的 future。'),

    # === tokio/sync/mpsc (extended, includes user-reported items) ===
    ('Channel error types.', 'Channel 错误类型。'),
    ('An Iterator of Permit that can be used to hold n slots in the channel.',
     '一个 Permit 迭代器，可用于在 channel 中持有 n 个槽位。'),
    ('Receives values from the associated Sender.',
     '从关联的 Sender 接收值。'),
    ('Sends values to the associated Receiver.',
     '向关联的 Receiver 发送值。'),
    ('Receive values from the associated UnboundedSender.',
     '从关联的 UnboundedSender 接收值。'),
    ('Send values to the associated UnboundedReceiver.',
     '向关联的 UnboundedReceiver 发送值。'),
    ('An unbounded sender that does not prevent the channel from being closed.',
     '一个无界 sender，不会阻止 channel 被关闭。'),

    # === tokio/sync/mpsc/error ===
    ('Error returned by Sender::send.', '由 Sender::send 返回的错误。'),
    ('Error returned by Sender::send_timeout.', '由 Sender::send_timeout 返回的错误。'),
    ('Error returned by Receiver::try_recv.', '由 Receiver::try_recv 返回的错误。'),
    ('Error returned by Sender::try_send.', '由 Sender::try_send 返回的错误。'),

    # === tokio/sync/oneshot ===
    ('Oneshot error types.', 'Oneshot 错误类型。'),
    ('Receives a value from the associated Sender.',
     '从关联的 Sender 接收一个值。'),
    ('Sends a value to the associated Receiver.',
     '向关联的 Receiver 发送一个值。'),
    ('Creates a new one-shot channel for sending single values across asynchronous tasks.',
     '创建一个新的 one-shot channel，用于在异步任务之间发送单个值。'),

    # === tokio/sync/oneshot/error ===
    ('Error returned by the Future implementation for Receiver.',
     '由 Receiver 的 Future 实现返回的错误。'),
    ('Error returned by the try_recv function on Receiver.',
     'Receiver 上的 try_recv 函数返回的错误。'),

    # === tokio/sync/watch ===
    ('Watch error types.', 'Watch 错误类型。'),
    ('Returns a reference to the inner value.',
     '返回内部值的引用。'),
    ('Creates a new watch channel, returning the “send” and “receive” handles.',
     '创建一个新的 watch channel，返回"发送"和"接收"句柄。'),

    # === tokio/sync/watch/error ===
    ('Error produced when receiving a change notification.',
     '接收变更通知时产生的错误。'),
    ('Error produced when sending a value fails.',
     '发送值失败时产生的错误。'),

    # === tokio/task ===
    ('Utilities for improved cooperative scheduling.',
     '用于改进协作式调度的工具。'),
    ('Task-related futures.', '与 task 相关的 future。'),
    ('An owned permission to abort a spawned task, without awaiting its completion.',
     '中止已生成 task 的 owned 权限，无须等待其完成。'),
    ('An opaque ID that uniquely identifies a task relative to all other currently running tasks.',
     '一个不透明的 ID，用于在所有当前运行的 task 中唯一标识某个 task。'),
    ('Task failed to execute to completion.', 'Task 未执行完毕即失败。'),
    ('An owned permission to join on a task (await its termination).',
     '用于 join 一个 task（等待其终止）的 owned 权限。'),
    ('A collection of tasks spawned on a Tokio runtime.',
     '在 Tokio runtime 上生成的一组 task。'),
    ('Context guard for LocalSet', 'LocalSet 的上下文守护'),
    ('A key for task-local data.', 'task 局部数据的键。'),
    ('A set of tasks which are executed on the same thread.',
     '在同一线程上执行的一组 task。'),
    ('Returns the Id of the currently running task.',
     '返回当前正在运行的 task 的 Id。'),
    ('Spawns a new asynchronous task, returning a JoinHandle for it.',
     '生成一个新的异步 task，返回一个 JoinHandle。'),
    ('Runs the provided closure on a thread where blocking is acceptable.',
     '在允许阻塞的线程上运行所提供的闭包。'),
    ('Spawns a !Send future on the current LocalSet or LocalRuntime.',
     '在当前 LocalSet 或 LocalRuntime 上生成一个 !Send future。'),
    ('Returns the Id of the currently running task, or None if called outside of a task.',
     '返回当前正在运行的 task 的 Id；若在 task 之外调用则返回 None。'),
    ('Yields execution back to the Tokio runtime.',
     '将执行权交回 Tokio runtime。'),

    # === tokio/task/coop ===
    ('Future wrapper to ensure cooperative scheduling created by cooperative.',
     '由 cooperative 创建的、用于保证协作式调度的 future 包装器。'),
    ('Value returned by the poll_proceed method.',
     '由 poll_proceed 方法返回的值。'),
    ('Future for the unconstrained method.',
     'unconstrained 方法对应的 future。'),
    ('Consumes a unit of budget and returns the execution back to the Tokio runtime if the task’s coop budget was exhausted.',
     '消耗一个单位的预算；若 task 的协作预算已耗尽，则将执行权交回 Tokio runtime。'),
    ('Creates a wrapper future that makes the inner future cooperate with the Tokio scheduler.',
     '创建一个包装 future，使内部 future 与 Tokio 调度器协作。'),
    ('Returns true if there is still budget left on the task.',
     '如果 task 上还有剩余预算，则返回 true。'),
    ('Decrements the task budget and returns Poll::Pending if the budget is depleted. This indicates that the task should yield to the scheduler.',
     '减少 task 预算；若预算已耗尽，则返回 Poll::Pending。这表示 task 应让出（yield）给调度器。'),
    ('Turn off cooperative scheduling for a future. The future will never be forced to yield by Tokio. Using this exposes your service to starvation.',
     '关闭某个 future 的协作式调度。该 future 永远不会被 Tokio 强制让出。使用它会使你的服务面临饥饿（starvation）的风险。'),

    # === tokio/task/futures ===
    ('A future that sets a value T of a task local for the future F during its execution.',
     '一个 future，会在 future F 执行期间为该 task 局部变量设置一个值 T。'),

    # === tokio/time ===
    ('Time error types.', '时间错误类型。'),
    ('A measurement of a monotonically nondecreasing clock. Opaque and useful only with Duration.',
     '单调递增时钟的一个度量值。不透明，仅与 Duration 一起使用时有意义。'),
    ('Interval returned by interval and interval_at.',
     '由 interval 和 interval_at 返回的 Interval。'),
    ('Future returned by sleep and sleep_until.',
     '由 sleep 和 sleep_until 返回的 future。'),
    ('Future returned by timeout and timeout_at.',
     '由 timeout 和 timeout_at 返回的 future。'),
    ('Defines the behavior of an Interval when it misses a tick.',
     '当 Interval 错过一个 tick 时定义其行为。'),
    ('Creates new Interval that yields with interval of period. The first tick completes immediately. The default MissedTickBehavior is Burst, but it can be changed using `set_missed_tick_behavior`.',
     '创建一个新的 Interval，以 period 为间隔周期产生 tick。第一次 tick 立即完成。默认的 MissedTickBehavior 为 Burst，但可以使用 `set_missed_tick_behavior` 更改。'),
    ('Creates new Interval that yields with interval of period with the first tick completing at start. The default MissedTickBehavior is Burst, but it can be changed using `set_missed_tick_behavior`.',
     '创建一个新的 Interval，以 period 为间隔周期产生 tick，第一次 tick 在 start 时完成。默认的 MissedTickBehavior 为 Burst，但可以使用 `set_missed_tick_behavior` 更改。'),
    ('Waits until duration has elapsed.', '等待直到指定时长过去。'),
    ('Waits until deadline is reached.', '等待直到截止时间到达。'),
    ('Requires a Future to complete before the specified duration has elapsed.',
     '要求一个 Future 在指定时长过去之前完成。'),
    ('Requires a Future to complete before the specified instant in time.',
     '要求一个 Future 在指定时刻之前完成。'),

    # === tokio/time/error ===
    ('Errors returned by Timeout.', '由 Timeout 返回的错误。'),
    ('Errors encountered by the timer implementation.',
     '定时器实现所遇到的错误。'),

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
    ('A TLS-encoded Encrypted Client Hello (ECH) configuration list (ECHConfigList); as specified in\r\nRFC 9849 §4',
     'TLS 编码的 Encrypted Client Hello (ECH) 配置列表（ECHConfigList）；按 RFC 9849 §4 规定'),
    ('A TLS-encoded Encrypted Client Hello (ECH) configuration list (ECHConfigList); as specified in\nRFC 9849 §4',
     'TLS 编码的 Encrypted Client Hello (ECH) 配置列表（ECHConfigList）；按 RFC 9849 §4 规定'),
    ('A TLS-encoded Encrypted Client Hello (ECH) configuration list (ECHConfigList); as specified in RFC 9849 §4',
     'TLS 编码的 Encrypted Client Hello (ECH) 配置列表（ECHConfigList）；按 RFC 9849 §4 规定'),
    ('The provided input could not be parsed because\r\nit is not a syntactically-valid DNS Name.',
     '提供的输入无法解析，因为它不是语法上合法的 DNS 名。'),
    ('The provided input could not be parsed because\nit is not a syntactically-valid DNS Name.',
     '提供的输入无法解析，因为它不是语法上合法的 DNS 名。'),
    ('The provided input could not be parsed because it is not a syntactically-valid DNS Name.',
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
    # rustls_pki_types/alg_id
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
    ('AlgorithmIdentifier for ecdsa-with-SHA256.',
     'ecdsa-with-SHA256 的 AlgorithmIdentifier。'),
    ('AlgorithmIdentifier for ecdsa-with-SHA384.',
     'ecdsa-with-SHA384 的 AlgorithmIdentifier。'),
    ('AlgorithmIdentifier for ecdsa-with-SHA512.',
     'ecdsa-with-SHA512 的 AlgorithmIdentifier。'),
    ('AlgorithmIdentifier for ED448.', 'ED448 的 AlgorithmIdentifier。'),
    ('AlgorithmIdentifier for ED25519.', 'ED25519 的 AlgorithmIdentifier。'),
    ('AlgorithmIdentifier for id-ml-dsa-44.',
     'id-ml-dsa-44 的 AlgorithmIdentifier。'),
    ('AlgorithmIdentifier for id-ml-dsa-65.',
     'id-ml-dsa-65 的 AlgorithmIdentifier。'),
    ('AlgorithmIdentifier for id-ml-dsa-87.',
     'id-ml-dsa-87 的 AlgorithmIdentifier。'),
    ('AlgorithmIdentifier for rsaEncryption.', 'rsaEncryption 的 AlgorithmIdentifier。'),
    ('AlgorithmIdentifier for sha256WithRSAEncryption.',
     'sha256WithRSAEncryption 的 AlgorithmIdentifier。'),
    ('AlgorithmIdentifier for sha384WithRSAEncryption.',
     'sha384WithRSAEncryption 的 AlgorithmIdentifier。'),
    ('AlgorithmIdentifier for sha512WithRSAEncryption.',
     'sha512WithRSAEncryption 的 AlgorithmIdentifier。'),
    ('AlgorithmIdentifier for rsassaPss with:',
     'rsassaPss 的 AlgorithmIdentifier，参数为：'),
    # rustls_pki_types/pem
    ('Extract and return all PEM sections by reading rd.',
     '通过读取 rd 提取并返回所有 PEM section。'),
    ('Iterator over all PEM sections in a &amp;[u8] slice.',
     '对 &amp;[u8] 切片中所有 PEM section 进行迭代的迭代器。'),
    ('Iterator over all PEM sections in a &[u8] slice.',
     '对 &[u8] 切片中所有 PEM section 进行迭代的迭代器。'),
    ('Errors that may arise when parsing the contents of a PEM file',
     '解析 PEM 文件内容时可能产生的错误'),
    ('A single recognised section in a PEM file.', 'PEM 文件中一个被识别的 section。'),
    ('Items that can be decoded from PEM data.', '可以从 PEM 数据解码出的条目。'),
    ('Extract and decode the next supported PEM section from rd.',
     '从 rd 中提取并解码下一个支持的 PEM section。'),

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
    ('oneshot channel', 'oneshot channel'),
    ('mpsc channel', 'mpsc channel'),
    ('broadcast channel', 'broadcast channel'),
    ('watch channel', 'watch channel'),
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

    # ----- chrome 标签（章节标题） -----
    ('>Tuple Fields<', '>元组字段<'),
    ('>Variants (Non-exhaustive)<', '>变体（非穷尽）<'),
    ('>Fields (Non-exhaustive)<', '>字段（非穷尽）<'),
    ('Implementing AsyncRead and AsyncWrite', '实现 AsyncRead 与 AsyncWrite'),
    ('Awaiting a LocalSet', '等待 LocalSet'),
    ('Use inside tokio::spawn', '在 tokio::spawn 内部使用'),
    ('changed versus has_changed', 'changed 与 has_changed 的对比'),
    ('borrow_and_update versus borrow', 'borrow_and_update 与 borrow 的对比'),
    # channel 名（oneshot/mpsc/broadcast/watch）是 Tokio 的术语，不强行翻译
    # 但在 h3 标题里它们与 'channel' 一起出现时可保留
    ('<h3>oneshot channel</h3>', '<h3>oneshot channel</h3>'),
    ('<h3>mpsc channel</h3>', '<h3>mpsc channel</h3>'),
    ('<h3>broadcast channel</h3>', '<h3>broadcast channel</h3>'),
    ('<h3>watch channel</h3>', '<h3>watch channel</h3>'),

    # ----- chrome 修正（之前误翻） -----
    ('<h2 id="traits" class="section-header">trait', '<h2 id="traits" class="section-header">特性'),
    ('>trait<', '>特性<'),  # 修复 chrome 翻译把 "Traits" 误翻成 "trait" 的 bug
]


def apply_translations(crate_dir, pairs, dry_run=True):
    """遍历 crate 内所有 .html，做 bytes 替换。返回总命中次数。"""
    total_hits = 0
    files_modified = 0
    hits_per_pair = {}  # pair index → count

    SKIP = {'static.files', 'search.index', 'src', '_common_tools', '.git'}

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
            for i, (en, zh) in enumerate(pairs):
                en_b = en.encode('utf-8')
                zh_b = zh.encode('utf-8')
                if en_b in new_content:
                    count = new_content.count(en_b)
                    new_content = new_content.replace(en_b, zh_b)
                    file_hits += count
                    hits_per_pair[i] = hits_per_pair.get(i, 0) + count
            if file_hits > 0:
                if not dry_run:
                    with open(path, 'wb') as f:
                        f.write(new_content)
                files_modified += 1
                total_hits += file_hits
                print(f'  {path}: {file_hits} replacements')

    return total_hits, files_modified, hits_per_pair


def main():
    if len(sys.argv) < 2:
        print('Usage: _translate_module_descriptions.py <crate_dir> [--report|--apply]')
        sys.exit(1)
    crate_dir = sys.argv[1]
    apply = '--apply' in sys.argv
    report = '--report' in sys.argv
    dry_run = not (apply or report)

    if dry_run:
        print('=== Dry-run (default). Use --apply to write, --report to list only. ===')

    pairs = TRANSLATION_PAIRS
    print(f'\nLoaded {len(pairs)} translation pairs.\n')

    total, files, hits_per_pair = apply_translations(crate_dir, pairs, dry_run=dry_run)

    print(f'\n=== Summary ===')
    print(f'Total replacements: {total}')
    print(f'Files modified: {files}')
    print(f'\nHits per pair:')
    for i, (en, zh) in enumerate(pairs):
        cnt = hits_per_pair.get(i, 0)
        if cnt > 0:
            print(f'  [{cnt:4d}x] {en[:60]!r}  →  {zh[:40]!r}')


if __name__ == '__main__':
    main()
