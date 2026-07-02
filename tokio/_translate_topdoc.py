# -*- coding: utf-8 -*-
"""Translate tokio top-doc <p> blocks (443 issues).

Bytes mode (rb/wb) to preserve UTF-8 + CRLF.
Long patterns first.
"""

import os
import json
import sys

# Load extracted top-doc issues
with open('/tmp/topdoc_issues.json', encoding='utf-8') as f:
    ISSUES = json.load(f)


def b(s):
    """Encode string as UTF-8 bytes, preserve CRLF."""
    return s.replace('\r\n', '\n').encode('utf-8')


# PAIRS: (en_bytes, zh_bytes) - long first
# These translations are written with explicit byte sequences for \r\n and Chinese chars

# Helper: make a (en, zh) pair from python strings
# IMPORTANT: tokio HTML files use CRLF. We keep \r\n in en/zh strings
# so the encoded bytes match the file. When the pair is written, the
# file gets the replacement (with CRLF preserved).
def pair(en_str, zh_str):
    # Convert any LF in input to CRLF so the search bytes match the file
    en_b = en_str.replace('\r\n', '\n').replace('\n', '\r\n').encode('utf-8')
    zh_b = zh_str.replace('\r\n', '\n').replace('\n', '\r\n').encode('utf-8')
    return (en_b, zh_b)


PAIRS = [
    # ============= attr.main.html =============
    pair(
        '<p>Marks async function to be executed by the selected runtime. This macro\nhelps set up a <code>Runtime</code> without requiring the user to use\n<a href="../tokio/runtime/struct.Runtime.html">Runtime</a> or\n<a href="../tokio/runtime/struct.Builder.html">Builder</a> directly.</p>',
        '<p>将异步函数标记为由选定的 runtime 执行。该宏有助于设置 <code>Runtime</code>，\n而无需用户直接使用 <a href="../tokio/runtime/struct.Runtime.html">Runtime</a> 或\n<a href="../tokio/runtime/struct.Builder.html">Builder</a>。</p>'
    ),
    pair(
        '<p>Note: This macro can be used on any function and not just the <code>main</code>\nfunction. Using it on a non-main function makes the function behave as if it\nwas synchronous by starting a new runtime each time it is called. If the\nfunction is called often, it is preferable to create the runtime using the\nruntime builder so the runtime can be reused across calls.</p>',
        '<p>注意：该宏可以用于任何函数，而不仅仅是 <code>main</code>\n函数。在非 main 函数上使用它会使该函数表现得像同步函数一样，\n因为每次调用时都会启动一个新的 runtime。如果该函数被频繁调用，\n建议使用 runtime builder 来创建 runtime，以便在多次调用之间复用。</p>'
    ),
    pair(
        '<p>The macro can be configured with a <code>flavor</code> parameter to select\ndifferent runtime configurations.</p>',
        '<p>该宏可以通过 <code>flavor</code> 参数来配置，以选择不同的 runtime 配置。</p>'
    ),
    pair(
        '<p>To use the multi-threaded runtime, the macro can be configured using</p>',
        '<p>要使用多线程 runtime，可以通过如下方式配置该宏</p>'
    ),

    # ============= attr.test.html =============
    pair(
        '<p>Marks async function to be executed by runtime, suitable to test environment.\nThis macro helps set up a <code>Runtime</code> without requiring the user to use\n<a href="../tokio/runtime/struct.Runtime.html">Runtime</a> or\n<a href="../tokio/runtime/struct.Builder.html">Builder</a> directly.</p>',
        '<p>将异步函数标记为由 runtime 执行，适用于测试环境。\n该宏有助于设置 <code>Runtime</code>，而无需用户直接使用\n<a href="../tokio/runtime/struct.Runtime.html">Runtime</a> 或\n<a href="../tokio/runtime/struct.Builder.html">Builder</a>。</p>'
    ),

    # ============= macro.join.html =============
    pair(
        '<p>Waits on multiple concurrent branches, returning when all branches\ncomplete.</p>',
        '<p>等待多个并发分支完成，当所有分支都完成时返回。</p>'
    ),
    pair(
        '<p>The <code>join!</code> macro must be used inside of async functions, closures, and\nblocks.</p>',
        '<p><code>join!</code> 宏必须在 async 函数、闭包和代码块内部使用。</p>'
    ),
    pair(
        '<p>The <code>join!</code> macro takes a list of async expressions and evaluates them\nconcurrently on the same task. Each async expression evaluates to a future\nand the futures from each expression are multiplexed on the current task.</p>',
        '<p><code>join!</code> 宏接受一组异步表达式，并在同一个任务上并发地对它们求值。\n每个异步表达式都会求值成一个 future，这些 future 在当前任务上进行多路复用。</p>'
    ),
    pair(
        '<p>When working with async expressions returning <code>Result</code>, <code>join!</code> will wait\nfor all branches complete regardless if any complete with <code>Err</code>. Use\n<a href="macro.try_join.html" title="macro tokio::try_join"><code>try_join!</code></a> to return early when <code>Err</code> is encountered.</p>',
        '<p>在处理返回 <code>Result</code> 的异步表达式时，<code>join!</code> 会等待所有分支完成，\n无论其中是否有分支以 <code>Err</code> 完成。若要在遇到 <code>Err</code> 时提前返回，\n请使用 <a href="macro.try_join.html" title="macro tokio::try_join"><code>try_join!</code></a>。</p>'
    ),
    pair(
        '<p>The supplied futures are stored inline and do not require allocating a\n<code>Vec</code>.</p>',
        '<p>所提供的 future 是内联存储的，无需分配 <code>Vec</code>。</p>'
    ),
    pair(
        '<p>By running all async expressions on the current task, the expressions are\nable to run concurrently but not in parallel. This means all\nexpressions are run on the same thread and if one branch blocks the thread,\nall other expressions will be unable to continue. If parallelism is\nrequired, then each branch must be spawned as a separate task using\n<code>tokio::spawn</code>.</p>',
        '<p>通过在当前任务上运行所有异步表达式，这些表达式可以并发执行但不能并行执行。\n这意味着所有表达式都在同一个线程上运行，如果某个分支阻塞了线程，\n则所有其他表达式都将无法继续。如果需要并行执行，\n则必须使用 <code>tokio::spawn</code> 将每个分支作为单独的任务派生。</p>'
    ),
    pair(
        '<p>By default, <code>join!</code>’s generated future rotates which contained\nfuture is polled first whenever it is woken.</p>',
        '<p>默认情况下，<code>join!</code> 生成的 future 在每次被唤醒时，\n都会轮换决定首先轮询哪个所包含的 future。</p>'
    ),
    pair(
        '<p>This behavior can be overridden by adding <code>biased;</code> to the beginning of the\nmacro usage. See the examples for details. This will cause join to poll\nthe futures in the order they appear from top to bottom.</p>',
        '<p>可以通过在宏的开头添加 <code>biased;</code> 来覆盖此行为。详细信息请参见示例。\n这将使 join 按照 future 从上到下出现的顺序进行轮询。</p>'
    ),
    pair(
        '<p>But there is an important caveat to this mode. It becomes your responsibility\nto ensure that the polling order of your futures is fair. If for example you\nare joining a stream and a shutdown future, and the stream has a\nhuge volume of messages that takes a long time to finish processing per poll, you\nshould place it at the end of the macro arguments or use a different\nconcurrency primitive.</p>',
        '<p>但此模式有一个重要的注意事项。确保你的 future 的轮询顺序是公平的变成你的责任。\n例如，如果你在 join 一个流和一个关闭 future，并且该流每次轮询都要花很长时间\n才能完成处理大量消息，那么应将其放在宏参数的最后，\n或使用其他的并发原语。</p>'
    ),
    pair(
        '<p>Basic join with two branches</p>',
        '<p>两个分支的基本 join</p>'
    ),

    # ============= macro.pin.html =============
    pair(
        '<p>Calls to <code>async fn</code> return anonymous <code>Future</code> values that are <code>!Unpin</code>.\nThese values must be pinned before they can be polled. Calling <code>.await</code> will\nhandle this, but consumes the future. If it is required to call <code>.await</code> on\na <code>&amp;mut _</code> reference, the caller is responsible for pinning the future.</p>',
        '<p>对 <code>async fn</code> 的调用会返回未命名的 <code>!Unpin</code> 的 <code>Future</code> 值。\n这些值在被轮询之前必须被 pin 住。调用 <code>.await</code> 会处理这一点，\n但会消费该 future。如果需要对 <code>&amp;mut _</code> 引用调用 <code>.await</code>，\n则调用者需要负责 pin 该 future。</p>'
    ),
    pair(
        '<p>Pinning may be done by allocating with <code>Box::pin</code> or by using the stack\nwith the <code>pin!</code> macro.</p>',
        '<p>Pin 操作可以通过 <code>Box::pin</code> 分配，或使用 <code>pin!</code> 宏在栈上进行。</p>'
    ),
    pair(
        '<p>The following will fail to compile:</p>',
        '<p>下面的代码将无法编译：</p>'
    ),

    # ============= macro.select.html =============
    pair(
        '<p>Waits on multiple concurrent branches, returning when the first branch\ncompletes, cancelling the remaining branches.</p>',
        '<p>等待多个并发分支，当第一个分支完成时返回，取消剩余的分支。</p>'
    ),
    pair(
        '<p>The <code>select!</code> macro must be used inside of async functions, closures, and\nblocks.</p>',
        '<p><code>select!</code> 宏必须在 async 函数、闭包和代码块内部使用。</p>'
    ),
    pair(
        '<p>The <code>select!</code> macro takes a list of async expressions and evaluates them\nconcurrently on the same task. Each async expression evaluates to a future\nand the futures from each expression are multiplexed on the current task. Once\nthe first future completes, all other futures are cancelled and the result of\nthe completed future is returned.</p>',
        '<p><code>select!</code> 宏接受一组异步表达式，并在同一个任务上并发地对它们求值。\n每个异步表达式都会求值成一个 future，这些 future 在当前任务上进行多路复用。\n一旦第一个 future 完成，所有其他 future 都将被取消，并返回已完成的 future 的结果。</p>'
    ),
    pair(
        '<p>Use <code>biased;</code> to run the branches in a specific order, even when future\ncompletion order may be random.</p>',
        '<p>使用 <code>biased;</code> 可按特定顺序运行分支，即使 future 完成的顺序可能是随机的。</p>'
    ),
    pair(
        '<p>Each <code>&lt;async expression&gt;</code> in the <code>select!</code> macro must have the same\nresult type. To use <code>select!</code> with futures of different result types, see\n<code>tokio::pin! + FutureExt::await</code>.</p>',
        '<p><code>select!</code> 宏中的每个 <code>&lt;异步表达式&gt;</code> 必须具有相同的结果类型。\n要在不同结果类型的 future 上使用 <code>select!</code>，\n请参见 <code>tokio::pin! + FutureExt::await</code>。</p>'
    ),

    # ============= macro.try_join.html =============
    pair(
        '<p>Waits on multiple concurrent branches, returning when all branches\ncomplete with <code>Ok(_)</code> or on the first <code>Err(_)</code>.</p>',
        '<p>等待多个并发分支，当所有分支都以 <code>Ok(_)</code> 完成时返回，\n或在第一个 <code>Err(_)</code> 时返回。</p>'
    ),
    pair(
        '<p>The <code>try_join!</code> macro must be used inside of async functions, closures, and\nblocks.</p>',
        '<p><code>try_join!</code> 宏必须在 async 函数、闭包和代码块内部使用。</p>'
    ),
    pair(
        '<p>The <code>try_join!</code> macro takes a list of async expressions and evaluates them\nconcurrently on the same task. Each async expression evaluates to a future\nand the futures from each expression are multiplexed on the current task.\nWhen all futures have completed, <code>try_join!</code> sums the result of each future\ninto a <a href="https://doc.rust-lang.org/1.95.0/core/result/enum.Result.html" title="enum core::result::Result"><code>Result</code></a> containing a tuple of the individual\nresults. If any future returns an <code>Err</code>, then <code>try_join!</code> short-circuits and\nreturns the error.</p>',
        '<p><code>try_join!</code> 宏接受一组异步表达式，并在同一个任务上并发地对它们求值。\n每个异步表达式都会求值成一个 future，这些 future 在当前任务上进行多路复用。\n当所有 future 都完成后，<code>try_join!</code> 会将每个 future 的结果\n合并到一个包含各个结果的元组的 <a href="https://doc.rust-lang.org/1.95.0/core/result/enum.Result.html" title="enum core::result::Result"><code>Result</code></a> 中。\n如果任何 future 返回 <code>Err</code>，则 <code>try_join!</code> 会短路并返回该错误。</p>'
    ),
    pair(
        '<p>When working with async expressions returning <a href="https://doc.rust-lang.org/1.95.0/core/result/enum.Result.html" title="enum core::result::Result"><code>Result</code></a>, <code>try_join!</code> will\nshort-circuit on the first <code>Err</code>. Use\n<a href="macro.join.html" title="macro tokio::join"><code>join!</code></a> to wait for all branches to complete\nregardless of result.</p>',
        '<p>在处理返回 <a href="https://doc.rust-lang.org/1.95.0/core/result/enum.Result.html" title="enum core::result::Result"><code>Result</code></a> 的异步表达式时，<code>try_join!</code> 会在第一个 <code>Err</code> 处短路。\n要等待所有分支完成（无论结果如何），请使用\n<a href="macro.join.html" title="macro tokio::join"><code>join!</code></a>。</p>'
    ),
    pair(
        '<p>The supplied futures are stored inline and do not require allocating a\n<a href="https://doc.rust-lang.org/1.95.0/alloc/vec/struct.Vec.html" title="struct alloc::vec::Vec"><code>Vec</code></a>.</p>',
        '<p>所提供的 future 是内联存储的，无需分配\n<a href="https://doc.rust-lang.org/1.95.0/alloc/vec/struct.Vec.html" title="struct alloc::vec::Vec"><code>Vec</code></a>。</p>'
    ),
    pair(
        '<p>By running all async expressions on the current task, the expressions are\nable to run concurrently but not in parallel. This means all\nexpressions are run on the same thread and if one branch blocks the thread,\nall other expressions will be unable to continue. If parallelism is\nrequired, then each branch must be spawned as a separate task using\n<a href="fn.spawn.html" title="fn tokio::spawn"><code>tokio::spawn</code></a>.</p>',
        '<p>通过在当前任务上运行所有异步表达式，这些表达式可以并发执行但不能并行执行。\n这意味着所有表达式都在同一个线程上运行，如果某个分支阻塞了线程，\n则所有其他表达式都将无法继续。如果需要并行执行，\n则必须使用 <a href="fn.spawn.html" title="fn tokio::spawn"><code>tokio::spawn</code></a> 将每个分支作为单独的任务派生。</p>'
    ),
    pair(
        '<p>It is sometimes useful to call <a href="https://doc.rust-lang.org/1.95.0/core/future/future/trait.Future.html#method.fuse" title="method core::future::future::Future::fuse"><code>Future::fuse</code></a> on futures\npassed to <code>try_join!</code> to require the future to be polled to completion before\ncompleting <code>try_join!</code>, even if it is cancelled before that point.</p>',
        '<p>有时对传递给 <code>try_join!</code> 的 future 调用\n<a href="https://doc.rust-lang.org/1.95.0/core/future/future/trait.Future.html#method.fuse" title="method core::future::future::Future::fuse"><code>Future::fuse</code></a> 是很有用的，\n这样可以要求 future 在 <code>try_join!</code> 完成之前一直轮询到完成，\n即使它在该点之前被取消。</p>'
    ),
    pair(
        '<p>Basic try_join with two branches</p>',
        '<p>两个分支的基本 try_join</p>'
    ),
    pair(
        '<p>Two <code>try_join!</code> calls can be combined to await multiple values concurrently</p>',
        '<p>可以组合两次 <code>try_join!</code> 调用以并发地等待多个值</p>'
    ),

    # ============= runtime/struct.Runtime.html =============
    pair(
        '<p>Runtime is the heart of the Tokio runtime. It is a multi-threaded, work-stealing\nscheduler that allows tasks to be executed concurrently across multiple\nthreads. The runtime is also responsible for managing I/O resources,\nincluding sockets, files, and timers.</p>',
        '<p>Runtime 是 Tokio 运行时的核心。它是一个多线程、工作窃取调度器，\n允许任务在多个线程上并发执行。Runtime 还负责管理 I/O 资源，\n包括 socket、文件和定时器。</p>'
    ),
    pair(
        '<p>The Tokio runtime also includes a scheduler that executes tasks cooperatively,\nallowing tasks to yield control when they are waiting for I/O or other\noperations to complete. This enables efficient use of system resources and\nprevents any single task from blocking the entire runtime.</p>',
        '<p>Tokio runtime 还包含一个调度器，它以协作方式执行任务，\n允许任务在等待 I/O 或其他操作完成时让出控制权。\n这可以高效利用系统资源，并防止任何单个任务阻塞整个 runtime。</p>'
    ),
    pair(
        '<p>For example, the runtime will automatically reschedule tasks when\nthey are blocked on I/O, allowing other tasks to run in the meantime.</p>',
        '<p>例如，当任务在 I/O 上阻塞时，runtime 会自动重新调度这些任务，\n从而允许其他任务在此期间运行。</p>'
    ),
    pair(
        '<p>For example, you can spawn a future as a task using\n<a href="struct.Runtime.html#method.spawn" title="method tokio::runtime::Runtime::spawn"><code>spawn</code></a> and await the result\nusing the returned <a href="../task/struct.JoinHandle.html" title="struct tokio::task::JoinHandle"><code>JoinHandle</code></a>.</p>',
        '<p>例如，你可以使用\n<a href="struct.Runtime.html#method.spawn" title="method tokio::runtime::Runtime::spawn"><code>spawn</code></a> 将一个 future 派生为任务，\n并使用返回的\n<a href="../task/struct.JoinHandle.html" title="struct tokio::task::JoinHandle"><code>JoinHandle</code></a> 来等待结果。</p>'
    ),
    pair(
        '<p>To use the runtime, you first need to create an instance of\n<a href="struct.Runtime.html" title="struct tokio::runtime::Runtime"><code>Runtime</code></a> or\n<a href="struct.Builder.html" title="struct tokio::runtime::Builder"><code>Builder</code></a> and then spawn tasks or run\n<a href="fn.block_on.html" title="fn tokio::runtime::block_on"><code>block_on</code></a> a future to completion.</p>',
        '<p>要使用 runtime，首先需要创建\n<a href="struct.Runtime.html" title="struct tokio::runtime::Runtime"><code>Runtime</code></a> 或\n<a href="struct.Builder.html" title="struct tokio::runtime::Builder"><code>Builder</code></a> 的实例，\n然后派生任务或使用 <a href="fn.block_on.html" title="fn tokio::runtime::block_on"><code>block_on</code></a> 阻塞运行一个 future 直到完成。</p>'
    ),
    pair(
        '<p>The runtime is designed to be easy to use and provides a simple, ergonomic API for\nmanaging concurrent tasks. It is also designed to be highly efficient,\nwith low overhead and minimal resource usage.</p>',
        '<p>该 runtime 旨在易于使用，并为管理并发任务提供简单、人体工程学的 API。\n它还旨在非常高效，开销低、资源占用少。</p>'
    ),
    pair(
        '<p>The Tokio runtime is a powerful tool for building high-performance network\napplications. It provides a simple, ergonomic API for managing concurrent\ntasks and I/O resources, making it a popular choice for building network\nservices in Rust.</p>',
        '<p>Tokio runtime 是构建高性能网络应用程序的强大工具。\n它为管理并发任务和 I/O 资源提供了简单、人体工程学的 API，\n使其成为在 Rust 中构建网络服务的热门选择。</p>'
    ),

    # ============= sync/mpsc/index.html =============
    pair(
        '<p>This channel is also suitable for the single-producer single-consumer\nuse-case. (Unless you only need to send one message, in which case the\n<code>oneshot</code> channel is a better choice.)</p>',
        '<p>该 channel 也适用于单生产者单消费者场景。\n（除非你只需要发送一条消息，这种情况下 <code>oneshot</code> channel 是更好的选择。）</p>'
    ),
    pair(
        '<p>When you want to communicate between synchronous and asynchronous code, there\nare two situations to consider:</p>',
        '<p>当你想在同步代码和异步代码之间通信时，需要考虑两种情况：</p>'
    ),
    pair(
        '<p>When used in a Tokio runtime, it participates in\ncooperative scheduling to avoid\nstarvation. This feature does not apply\nto a channel that is being used outside the Tokio runtime.</p>',
        '<p>在 Tokio runtime 中使用时，它会参与协作式调度，\n以避免任务饥饿。\n该特性不适用于在 Tokio runtime 之外使用的 channel。</p>'
    ),
    pair(
        '<p>The mpsc channel stores elements in blocks. Blocks are organized in a linked list. Sending\npushes new elements onto the back of the linked list. Receiving pops elements\nfrom the front of the list.</p>',
        '<p>mpsc channel 将元素存储在 block 中。这些 block 组织在一个链表中。\n发送操作将新元素压入链表的尾部，接收操作从链表的头部弹出元素。</p>'
    ),
    pair(
        '<p>When all values in a block have been received, it becomes empty. It will then be freed, unless\nthe channel’s first block has not yet been freed.</p>',
        '<p>当一个 block 中的所有值都被接收后，它会变为空。\n然后该 block 会被释放，除非 channel 的第一个 block 尚未被释放。</p>'
    ),

    # ============= sync/broadcast/index.html =============
    pair(
        '<p>This channel is also suitable for the single-producer multi-consumer\nuse-case, where a single sender broadcasts values to multiple receivers.</p>',
        '<p>该 channel 也适用于单生产者多消费者场景，\n其中单个 sender 向多个 receiver 广播值。</p>'
    ),
    pair(
        '<p>This behavior enables a receiver to detect when it has lagged so far behind\nthat data has been dropped. The caller may decide to re-sync by reading\nthe latest value, or take other action.</p>',
        '<p>该行为使得 receiver 能够检测到它已经落后很多，\n以至于数据被丢弃。调用方可以决定通过读取最新值来重新同步，\n或采取其他措施。</p>'
    ),

    # ============= sync/oneshot/... =============
    pair(
        '<p>Each handle can be used on separate tasks.</p>',
        '<p>每个 handle 可以在不同的任务上使用。</p>'
    ),
    pair(
        '<p>This error is returned by the receiver when the sender is dropped without sending.</p>',
        '<p>当 sender 在没有发送的情况下被丢弃时，receiver 会返回此错误。</p>'
    ),

    # ============= sync/watch/index.html =============
    pair(
        '<p>This channel is useful for watching for changes to a value from multiple\npoints in the code base, for example, configuration changes, shutdown signals,\nor monitoring state changes.</p>',
        '<p>该 channel 对于从代码库中的多个位置观察值的更改非常有用，\n例如配置更改、关闭信号或监控状态变化。</p>'
    ),
    pair(
        '<p>For more information on when to use these methods, see\n<a href="https://docs.rs/tokio/latest/tokio/sync/watch/index.html#which-method">here</a>.</p>',
        '<p>有关何时使用这些方法的更多信息，请参见\n<a href="https://docs.rs/tokio/latest/tokio/sync/watch/index.html#which-method">此处</a>。</p>'
    ),
    pair(
        '<p>Note there are two behavioral differences on when these two methods return\nan error.</p>',
        '<p>请注意，这两种方法在返回错误时存在两个行为差异。</p>'
    ),
    pair(
        '<p>See the example below that shows how these methods have different fallibility.</p>',
        '<p>请参见下面的示例，该示例展示了这些方法具有不同的可失败性。</p>'
    ),
    pair(
        '<p>The value in the channel will not be dropped until all senders and all\nreceivers have been dropped.</p>',
        '<p>在所有 sender 和 receiver 都被丢弃之前，channel 中的值不会被释放。</p>'
    ),

    # ============= sync/index.html =============
    pair(
        '<p>Tasks are scheduled to run on the runtime. When a task is waiting for\nsomething, such as an I/O or synchronization event, the task is suspended\nand the runtime schedules another task to run.</p>',
        '<p>任务被调度到 runtime 上运行。当任务正在等待某些事件（例如 I/O 或同步事件）时，\n该任务会被挂起，runtime 会调度另一个任务来运行。</p>'
    ),
    pair(
        '<p>The synchronization primitives in this module are designed to be used\nwithin the Tokio runtime. Using these primitives outside of the Tokio\nruntime is undefined behavior.</p>',
        '<p>此模块中的同步原语被设计为在 Tokio runtime 中使用。\n在 Tokio runtime 之外使用这些原语是未定义行为。</p>'
    ),

    # ============= sync/struct.Mutex.html =============
    pair(
        '<p>Tokio’s <code>Mutex</code> operates on a guaranteed FIFO basis. This means that the\norder in which tasks call the <code>lock</code> method is the exact order in which they\nwill acquire the lock.</p>',
        '<p>Tokio 的 <code>Mutex</code> 基于保证的 FIFO 原则运作。\n这意味着任务调用 <code>lock</code> 方法的顺序，就是它们获取锁的确切顺序。</p>'
    ),
    pair(
        '<p>Contrary to popular belief, it is ok and often preferred to use the ordinary\n<a href="https://doc.rust-lang.org/1.95.0/std/sync/struct.Mutex.html" title="struct std::sync::Mutex"><code>Mutex</code></a> from the standard library in asynchronous code.</p>',
        '<p>与普遍的看法相反，在异步代码中使用标准库中的普通\n<a href="https://doc.rust-lang.org/1.95.0/std/sync/struct.Mutex.html" title="struct std::sync::Mutex"><code>Mutex</code></a> 是没问题的，\n而且通常是首选。</p>'
    ),
    pair(
        '<p>The feature that the async mutex offers over the blocking mutex is the\nability to keep it locked across an <code>.await</code> point. This makes the async\nmutex more expensive than the blocking mutex, so the blocking mutex should\nbe preferred in the cases where it can be used. The primary use case for the\nasync mutex is to provide shared mutable access to I/O resources such as a\nconnection pool or a shared channel that must be locked across await points.</p>',
        '<p>异步 mutex 相对于阻塞 mutex 所提供的特性是能够在 <code>.await</code> 跨度上保持锁定。\n这使得异步 mutex 比阻塞 mutex 更昂贵，因此在可以使用阻塞 mutex 的情况下，\n应优先选择阻塞 mutex。\n异步 mutex 的主要用例是为 I/O 资源（如连接池或必须在 await 跨度上锁定的共享 channel）\n提供共享可变访问。</p>'
    ),

    # ============= sync/struct.Notify.html =============
    pair(
        '<p>Each <code>Notify</code> value holds a single permit. If <code>notify_one</code> is called and no\npermits are available, the permit is stored and the next call to\n<code>notified().await</code> will complete immediately.</p>',
        '<p>每个 <code>Notify</code> 值持有一个 permit。如果在无可用 permit 时调用 <code>notify_one</code>，\n该 permit 会被存储，下一次调用 <code>notified().await</code> 将立即完成。</p>'
    ),

    # ============= task/fn.block_in_place.html =============
    pair(
        '<p>Runs the provided blocking function on the current thread without\nblocking the executor.</p>',
        '<p>在当前线程上运行所提供的阻塞函数，而不会阻塞 executor。</p>'
    ),
    pair(
        '<p>In general, issuing a blocking call or performing a lot of compute in a\nfuture without yielding is problematic, as it may prevent the executor from\ndriving other tasks forward. To combat this, this function runs the blocking\nfunction in the runtime’s dedicated blocking thread pool.</p>',
        '<p>通常，在 future 中发起阻塞调用或执行大量计算而不让出控制权是有问题的，\n因为这可能会阻止 executor 推进其他任务。\n为了解决这个问题，此函数在 runtime 专用的阻塞线程池中运行该阻塞函数。</p>'
    ),

    # ============= task/fn.spawn.html =============
    pair(
        '<p>It is guaranteed that <a href="fn.spawn.html" title="fn tokio::spawn"><code>spawn</code></a> will not synchronously poll the task being spawned.\nThis means that calling <a href="fn.spawn.html" title="fn tokio::spawn"><code>spawn</code></a> while holding a lock or doing other\nnon-async-suitable things is safe.</p>',
        '<p>可以保证 <a href="fn.spawn.html" title="fn tokio::spawn"><code>spawn</code></a> 不会同步轮询被派生的任务。\n这意味着在持有锁或做其他不适合异步操作的事情时调用\n<a href="fn.spawn.html" title="fn tokio::spawn"><code>spawn</code></a> 是安全的。</p>'
    ),
    pair(
        '<p>There is no guarantee that a spawned task will execute to completion.\nWhen a runtime is shutdown, all outstanding tasks are dropped, regardless\nof whether they have completed or not.</p>',
        '<p>不能保证派生的任务会执行到完成。当 runtime 关闭时，\n所有未完成的任务都会被丢弃，无论它们是否已经完成。</p>'
    ),
    pair(
        '<p>For example, this will work:</p>',
        '<p>例如，下面的代码可以工作：</p>'
    ),

    # ============= task/fn.spawn_blocking.html =============
    pair(
        '<p>In general, issuing a blocking call or performing a lot of compute in a\nfuture without yielding is problematic, as it may prevent the executor from\ndriving other tasks forward. To combat this, this function moves the blocking\nfunction to a dedicated thread pool, leaving the executor free to continue\nto drive other tasks.</p>',
        '<p>通常，在 future 中发起阻塞调用或执行大量计算而不让出控制权是有问题的，\n因为这可能会阻止 executor 推进其他任务。\n为了解决这个问题，此函数将阻塞函数移至专用线程池，\n从而使 executor 可以继续推进其他任务。</p>'
    ),
    pair(
        '<p>As a rule of thumb:</p>',
        '<p>经验法则：</p>'
    ),
    pair(
        '<p>Note that if you are using the single threaded runtime, this function will\nstill spawn additional threads for blocking operations.</p>',
        '<p>请注意，如果你使用的是单线程 runtime，\n此函数仍会为阻塞操作派生额外的线程。</p>'
    ),
    pair(
        '<p>In simple cases, it is sufficient to have the closure accept input\nparameters at creation time and return a single value.</p>',
        '<p>在简单的情况下，让闭包在创建时接受输入参数并返回单个值就够了。</p>'
    ),
    pair(
        '<p>Pass an input value and receive result of computation:</p>',
        '<p>传递一个输入值并接收计算结果：</p>'
    ),

    # ============= task/fn.yield_now.html =============
    pair(
        '<p>See also the usage example in the <a href="../task/index.html" title="mod tokio::task">task module</a>.</p>',
        '<p>另请参见 <a href="../task/index.html" title="mod tokio::task">task 模块</a> 中的使用示例。</p>'
    ),
    pair(
        '<p>In general, changes to the order in which the runtime polls tasks is not\nconsidered a breaking change, and your program should not rely on any\nspecific ordering. If you need to guarantee that a task runs before some\nother operation, use a synchronization primitive such as a oneshot channel\nto coordinate them.</p>',
        '<p>通常，对 runtime 轮询任务顺序的更改不被视为破坏性更改，\n你的程序不应依赖于任何特定的排序。\n如果需要保证任务在某些其他操作之前运行，\n请使用诸如 oneshot channel 之类的同步原语来协调它们。</p>'
    ),

    # ============= task/struct.Id.html =============
    pair(
        '<p>A task’s ID may be re-used for another task only once both of the\nfollowing happen:</p>',
        '<p>一个任务的 ID 只能在以下两个条件都满足后才能被另一个任务重用：</p>'
    ),

    # ============= task/coop/fn.consume_budget.html =============
    pair(
        '<p>The task will only yield if its entire coop budget has been exhausted.\nThis function can be used in order to insert explicit yield points in\nfunctions that are not async but want to participate in cooperative\nscheduling.</p>',
        '<p>只有当任务整个协作预算耗尽时，任务才会让出控制权。\n该函数可以用于在非 async 但希望参与协作式调度的函数中插入显式的让出点。</p>'
    ),
    pair(
        '<p>Make sure that a function which returns a sum of (potentially lots of)\niterated values is cooperative.</p>',
        '<p>确保返回（可能大量）迭代值之和的函数是协作式的。</p>'
    ),

    # ============= task/coop/fn.unconstrained.html =============
    pair(
        '<p>See also the usage example in the <a href="../index.html" title="mod tokio::task">task module</a>.</p>',
        '<p>另请参见 <a href="../index.html" title="mod tokio::task">task 模块</a> 中的使用示例。</p>'
    ),

    # ============= task/coop/index.html =============
    pair(
        '<p>Consider a future like this one:</p>',
        '<p>考虑这样一个 future：</p>'
    ),
    pair(
        '<p>To account for this, Tokio has explicit yield points in a number of library\nfunctions, which force tasks to return to the runtime so that other tasks\ncan be polled.</p>',
        '<p>为了解决此问题，Tokio 在许多库函数中都有显式的让出点，\n强制任务返回到 runtime，以便其他任务可以被轮询。</p>'
    ),

    # ============= time/fn.sleep.html =============
    pair(
        '<p>Canceling a sleep instance is done by dropping the returned future. No additional\ncleanup work is required.</p>',
        '<p>取消 sleep 实例的方法是丢弃返回的 future。不需要额外的清理工作。</p>'
    ),
    pair(
        '<p>Wait 100ms and print “100 ms have elapsed”.</p>',
        '<p>等待 100 毫秒并打印 "100 毫秒已过"。</p>'
    ),
    pair(
        '<p>This function panics if there is no current timer set.</p>',
        '<p>如果未设置当前定时器，则此函数会 panic。</p>'
    ),

    # ============= time/fn.sleep_until.html =============
    pair(
        '<p>Wait 100ms and print “100 ms have elapsed”.</p>',
        '<p>等待 100 毫秒并打印 "100 毫秒已过"。</p>'
    ),

    # ============= time/fn.timeout.html =============
    pair(
        '<p>If the future completes before the duration has elapsed, then the completed\nvalue is returned. Otherwise, an error is returned.</p>',
        '<p>如果 future 在指定时长之前完成，则返回已完成的 value。\n否则返回错误。</p>'
    ),
    pair(
        '<p>Note that the timeout is checked before polling the future, so if the future\ndoes not yield during execution then it is possible for the timeout to\nexpire without the future making any progress.</p>',
        '<p>请注意，超时是在轮询 future 之前检查的，\n因此如果 future 在执行期间不让出，\n则可能会出现超时已过但 future 尚未取得任何进展的情况。</p>'
    ),
    pair(
        '<p>Cancelling a timeout is done by dropping the future. No additional cleanup\nor other work is required.</p>',
        '<p>取消 timeout 的方法是丢弃该 future。不需要额外的清理或其他工作。</p>'
    ),

    # ============= time/fn.timeout_at.html =============
    pair(
        '<p>If the future completes before the instant is reached, then the completed\nvalue is returned. Otherwise, an error is returned.</p>',
        '<p>如果 future 在指定时刻之前完成，则返回已完成的 value。\n否则返回错误。</p>'
    ),

    # ============= time/error/struct.Elapsed.html =============
    pair(
        '<p>This error is returned when a timeout expires before the function was able\nto finish.</p>',
        '<p>当超时在函数能够完成之前到期时，返回此错误。</p>'
    ),
]


def main():
    total = 0
    affected_files = set()
    for fp, items in ISSUES.items():
        if not os.path.exists(fp):
            continue
        with open(fp, 'rb') as f:
            data = f.read()
        orig = data
        count = 0
        # Filter PAIRS that are in this file
        for en, zh in PAIRS:
            if en in data:
                n = data.count(en)
                data = data.replace(en, zh)
                count += n
        if data != orig:
            with open(fp, 'wb') as f:
                f.write(data)
            print(f'{fp}: {count} replacements')
            total += count
            affected_files.add(fp)
    print(f'\nTotal: {total} replacements across {len(affected_files)} files')


if __name__ == '__main__':
    main()