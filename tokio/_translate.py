"""Translate tokio's cargo doc index.html to Chinese.

Workflow per rust-doc-translation-pattern:
- Use Python open() directly (no Read tool).
- Apply (old, new) replacements in long-string-first order.
- Preserve HTML structure, URLs, Rust identifiers, <wbr>, code blocks.
"""

import os
import re

TOKIO_ROOT = 'D:/Administrator/Documents/Code/rust_doc_all/tokio'


def verify(content, label):
    """Verify a translated HTML file: tag balance, line-number pollution, CJK density."""
    line_artifacts = re.findall(r'^\d+\t', content, flags=re.MULTILINE)
    if line_artifacts:
        print(f'  [WARN] {label}: {len(line_artifacts)} lines with cat-n style line numbers')

    cjk = re.findall(r'[一-鿿]', content)
    print(f'  [INFO] {label}: {len(cjk)} CJK characters')

    tag_pairs = ['html', 'head', 'body', 'main', 'section', 'div', 'p',
                 'a', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'ul', 'li',
                 'code', 'pre', 'details', 'summary', 'dl', 'dt', 'dd']
    bad = []
    for t in tag_pairs:
        opens = len(re.findall(rf'<{t}[\s>]', content))
        closes = len(re.findall(rf'</{t}>', content))
        if opens != closes:
            bad.append((t, opens, closes))
    if bad:
        for t, o, c in bad:
            print(f'  [WARN] {label}: <{t}> open={o} close={c} diff={o-c}')


# ============================================================================
# Common UI replacements (sidebar, nav, buttons, section headers)
# ============================================================================
COMMON_UI = [
    # Sidebar / nav headers
    ('>Sections<', '>章节<'),
    ('>Crate Items<', '>crate 项<'),
    ('>All Items<', '>所有项<'),
    # Buttons
    ('>Copy item path<', '>复制项目路径<'),
    ('>Source<', '>源代码<'),
    ('>Expand description<', '>展开描述<'),
    # Skip link
    ('>Skip to main content<', '>跳到主要内容<'),
    # IE warning
    ('This old browser is unsupported and will most likely display funky things.',
     '此旧版浏览器不受支持，很可能会显示异常内容。'),
    # Section headers in sidebar Crate Items list
    ('title="Re-exports"', 'title="重新导出"'),
    ('title="Modules"', 'title="模块"'),
    ('title="Macros"', 'title="宏"'),
    # Doc anchor section titles
    ('title="A Tour of Tokio"', 'title="Tokio 概览"'),
    ('title="Authoring applications"', 'title="编写应用程序"'),
    ('title="Authoring libraries"', 'title="编写库"'),
    ('title="Working With Tasks"', 'title="使用任务"'),
    ('title="CPU-bound tasks and blocking code"', 'title="CPU 密集型任务与阻塞代码"'),
    ('title="Asynchronous IO"', 'title="异步 I/O"'),
    ('title="Examples"', 'title="示例"'),
    ('title="Feature flags"', 'title="特性标志"'),
    ('title="Unstable features"', 'title="不稳定特性"'),
    ('title="Supported platforms"', 'title="支持的平台"'),
    ('title="`WASM` support"', 'title="`WASM` 支持"'),
    ('title="Unstable `WASM` support"', 'title="不稳定的 `WASM` 支持"'),
    # Misc title attrs
    ('title="Copy item path to clipboard"', 'title="复制项目路径到剪贴板"'),
    ('title="Drag to resize sidebar"', 'title="拖动以调整侧边栏宽度"'),
]


# ============================================================================
# Docblock content pairs (the main crate description)
# ============================================================================
# Long descriptive pairs that span multiple lines / include links.
DOCBLOCK_PAIRS = [
    # ----- Main intro (top of docblock) -----
    # The first <p> is also the meta description; we handle it in the meta block.
    # "Tokio is an event-driven, non-blocking I/O platform..."
    ('<p>Tokio is an event-driven, non-blocking I/O platform for writing asynchronous\napplications with the Rust programming language. At a high level, it\nprovides a few major components:</p>',
     '<p>Tokio 是一个事件驱动、非阻塞的 I/O 平台，用于使用 Rust 编程语言编写异步应用程序。从高层次上讲，它提供了几个主要组件：</p>'),
    # First list item
    ('<li>Tools for <a href="#working-with-tasks">working with asynchronous tasks</a>, including\n<a href="sync/index.html" title="mod tokio::sync">synchronization primitives and channels</a> and <a href="time/index.html" title="mod tokio::time">timeouts, sleeps, and\nintervals</a>.</li>',
     '<li>用于<a href="#working-with-tasks">使用异步任务</a>的工具，包括<a href="sync/index.html" title="mod tokio::sync">同步原语和通道</a>以及<a href="time/index.html" title="mod tokio::time">超时、休眠和\n定时器</a>。</li>'),
    # Second list item
    ('<li>APIs for <a href="#asynchronous-io">performing asynchronous I/O</a>, including <a href="net/index.html" title="mod tokio::net">TCP and UDP</a> sockets,\n<a href="crate::fs">filesystem</a> operations, and <a href="crate::process">process</a> and <a href="crate::signal">signal</a> management.</li>',
     '<li>用于<a href="#asynchronous-io">执行异步 I/O</a>的 API，包括 <a href="net/index.html" title="mod tokio::net">TCP 和 UDP</a> 套接字、\n<a href="crate::fs">文件系统</a>操作，以及 <a href="crate::process">进程</a>和 <a href="crate::signal">信号</a>管理。</li>'),
    # Third list item (note: `etc…)` uses U+2026 horizontal ellipsis)
    ('<li>A <a href="runtime/index.html" title="mod tokio::runtime">runtime</a> for executing asynchronous code, including a task scheduler,\nan I/O driver backed by the operating system’s event queue (<code>epoll</code>, <code>kqueue</code>,\n<code>IOCP</code>, etc…), and a high performance timer.</li>',
     '<li>用于执行异步代码的<a href="runtime/index.html" title="mod tokio::runtime">运行时</a>，包括任务调度器、由操作系统事件队列（<code>epoll</code>、<code>kqueue</code>、\n<code>IOCP</code> 等）支持的 I/O 驱动，以及一个高性能定时器。</li>'),
    # Guide pointer
    ('<p>Guide level documentation is found on the <a href="https://tokio.rs/tokio/tutorial">website</a>.</p>',
     '<p>指南级文档可在<a href="https://tokio.rs/tokio/tutorial">官网</a>上找到。</p>'),

    # ----- A Tour of Tokio -----
    ('<p>Tokio consists of a number of modules that provide a range of functionality\nessential for implementing asynchronous applications in Rust. In this\nsection, we will take a brief tour of Tokio, summarizing the major APIs and\ntheir uses.</p>',
     '<p>Tokio 由许多模块组成，这些模块提供了在 Rust 中实现异步应用程序所需的各种功能。在本节中，我们将简要地浏览 Tokio，概括其主要 API 及其用途。</p>'),
    ('<p>The easiest way to get started is to enable all features. Do this by\nenabling the <code>full</code> feature flag:</p>',
     '<p>最简单的上手方式是启用所有特性。请通过启用 <code>full</code> 特性标志来实现：</p>'),

    # ----- Authoring applications -----
    ('<p>Tokio is great for writing applications and most users in this case shouldn’t\nworry too much about what features they should pick. If you’re unsure, we suggest\ngoing with <code>full</code> to ensure that you don’t run into any road blocks while you’re\nbuilding your application.</p>',
     '<p>Tokio 非常适合编写应用程序，对于大多数用户来说，不需要过于担心应该选择哪些特性。如果你不确定，我们建议使用 <code>full</code>，以确保在构建应用程序时不会遇到任何阻碍。</p>'),
    ('<p>This example shows the quickest way to get started with Tokio.</p>',
     '<p>本示例展示使用 Tokio 最快速的上手方法。</p>'),

    # ----- Authoring libraries -----
    ('<p>As a library author your goal should be to provide the lightest weight crate\nthat is based on Tokio. To achieve this you should ensure that you only enable\nthe features you need. This allows users to pick up your crate without having\nto enable unnecessary features.</p>',
     '<p>作为库的作者，你的目标应该是提供基于 Tokio 的最轻量级 crate。为此，你应该确保只启用你需要的特性。这样用户就可以使用你的 crate，而无需启用不必要的特性。</p>'),
    ('<p>This example shows how you may want to import features for a library that just\nneeds to <code>tokio::spawn</code> and use a <code>TcpStream</code>.</p>',
     '<p>本示例展示对于一个只需要 <code>tokio::spawn</code> 并使用 <code>TcpStream</code> 的库，应当如何引入特性。</p>'),

    # ----- Working With Tasks -----
    ('<p>Asynchronous programs in Rust are based around lightweight, non-blocking\nunits of execution called <a href="#working-with-tasks"><em>tasks</em></a>. The <a href="task/index.html" title="mod tokio::task"><code>tokio::task</code></a> module provides\nimportant tools for working with tasks:</p>',
     '<p>Rust 中的异步程序围绕轻量级、非阻塞的执行单元（即<a href="#working-with-tasks"><em>任务</em></a>）构建。<a href="task/index.html" title="mod tokio::task"><code>tokio::task</code></a> 模块提供了处理任务的重要工具：</p>'),
    ('<li>The <a href="task/fn.spawn.html" title="fn tokio::task::spawn"><code>spawn</code></a> function and <a href="task/struct.JoinHandle.html" title="struct tokio::task::JoinHandle"><code>JoinHandle</code></a> type, for scheduling a new task\non the Tokio runtime and awaiting the output of a spawned task, respectively,</li>',
     '<li><a href="task/fn.spawn.html" title="fn tokio::task::spawn"><code>spawn</code></a> 函数和 <a href="task/struct.JoinHandle.html" title="struct tokio::task::JoinHandle"><code>JoinHandle</code></a> 类型，分别用于在 Tokio 运行时上调度一个新任务\n以及等待已生成任务的输出，</li>'),
    ('<li>Functions for <a href="task/index.html#blocking-and-yielding">running blocking operations</a> in an asynchronous\ntask context.</li>',
     '<li>用于在异步任务上下文中<a href="task/index.html#blocking-and-yielding">运行阻塞操作</a>的函数。</li>'),
    ('<p>The <a href="task/index.html" title="mod tokio::task"><code>tokio::task</code></a> module is present only when the “rt” feature flag\nis enabled.</p>',
     '<p><a href="task/index.html" title="mod tokio::task"><code>tokio::task</code></a> 模块仅在启用了 “rt” 特性标志时可用。</p>'),
    ('<p>The <a href="sync/index.html" title="mod tokio::sync"><code>tokio::sync</code></a> module contains synchronization primitives to use when\nneeding to communicate or share data. These include:</p>',
     '<p><a href="sync/index.html" title="mod tokio::sync"><code>tokio::sync</code></a> 模块包含在需要通信或共享数据时使用的同步原语。其中包括：</p>'),
    ('<li>channels (<a href="sync/oneshot/index.html" title="mod tokio::sync::oneshot"><code>oneshot</code></a>, <a href="sync/mpsc/index.html" title="mod tokio::sync::mpsc"><code>mpsc</code></a>, <a href="sync/watch/index.html" title="mod tokio::sync::watch"><code>watch</code></a>, and <a href="sync/broadcast/index.html" title="mod tokio::sync::broadcast"><code>broadcast</code></a>), for sending values\nbetween tasks,</li>',
     '<li>通道（<a href="sync/oneshot/index.html" title="mod tokio::sync::oneshot"><code>oneshot</code></a>、<a href="sync/mpsc/index.html" title="mod tokio::sync::mpsc"><code>mpsc</code></a>、<a href="sync/watch/index.html" title="mod tokio::sync::watch"><code>watch</code></a> 和 <a href="sync/broadcast/index.html" title="mod tokio::sync::broadcast"><code>broadcast</code></a>），用于在任务之间\n发送值，</li>'),
    ('<li>a non-blocking <a href="sync/struct.Mutex.html" title="struct tokio::sync::Mutex"><code>Mutex</code></a>, for controlling access to a shared, mutable\nvalue,</li>',
     '<li>一个非阻塞的 <a href="sync/struct.Mutex.html" title="struct tokio::sync::Mutex"><code>Mutex</code></a>，用于控制对共享可变值的访问，</li>'),
    ('<li>an asynchronous <a href="sync/struct.Barrier.html" title="struct tokio::sync::Barrier"><code>Barrier</code></a> type, for multiple tasks to synchronize before\nbeginning a computation.</li>',
     '<li>一个异步的 <a href="sync/struct.Barrier.html" title="struct tokio::sync::Barrier"><code>Barrier</code></a> 类型，用于在开始计算前让多个任务同步。</li>'),
    ('<p>The <code>tokio::sync</code> module is present only when the “sync” feature flag is\nenabled.</p>',
     '<p><code>tokio::sync</code> 模块仅在启用了 “sync” 特性标志时可用。</p>'),
    ('<p>The <a href="time/index.html" title="mod tokio::time"><code>tokio::time</code></a> module provides utilities for tracking time and\nscheduling work. This includes functions for setting <a href="time/fn.timeout.html" title="fn tokio::time::timeout">timeouts</a> for\ntasks, <a href="time/fn.sleep.html" title="fn tokio::time::sleep">sleeping</a> work to run in the future, or <a href="time/fn.interval.html" title="fn tokio::time::interval">repeating an operation at an\ninterval</a>.</p>',
     '<p><a href="time/index.html" title="mod tokio::time"><code>tokio::time</code></a> 模块提供了跟踪时间和调度工作的工具。这包括为任务设置<a href="time/fn.timeout.html" title="fn tokio::time::timeout">超时</a>、\n将工作<a href="time/fn.sleep.html" title="fn tokio::time::sleep">休眠</a>到将来某个时间再运行，或<a href="time/fn.interval.html" title="fn tokio::time::interval">以固定间隔重复执行某个操作</a>的函数。</p>'),
    ('<p>In order to use <code>tokio::time</code>, the “time” feature flag must be enabled.</p>',
     '<p>要使用 <code>tokio::time</code>，必须启用 “time” 特性标志。</p>'),
    ('<p>Finally, Tokio provides a <em>runtime</em> for executing asynchronous tasks. Most\napplications can use the <a href="attr.main.html"><code>#[tokio::main]</code></a> macro to run their code on the\nTokio runtime. However, this macro provides only basic configuration options. As\nan alternative, the <a href="runtime/index.html" title="mod tokio::runtime"><code>tokio::runtime</code></a> module provides more powerful APIs for configuring\nand managing runtimes. You should use that module if the <code>#[tokio::main]</code> macro doesn’t\nprovide the functionality you need.</p>',
     '<p>最后，Tokio 提供了一个用于执行异步任务的<em>运行时</em>。大多数应用程序可以使用 <a href="attr.main.html"><code>#[tokio::main]</code></a> 宏来在 Tokio 运行时上运行它们的代码。但是，该宏只提供基本的配置选项。作为替代方案，<a href="runtime/index.html" title="mod tokio::runtime"><code>tokio::runtime</code></a> 模块提供了更强大的 API 来配置和管理运行时。如果 <code>#[tokio::main]</code> 宏不能满足你的需求，应当使用该模块。</p>'),
    ('<p>Using the runtime requires the “rt” or “rt-multi-thread” feature flags, to\nenable the current-thread <a href="runtime/index.html#current-thread-scheduler">single-threaded scheduler</a> and the <a href="runtime/index.html#multi-thread-scheduler">multi-thread\nscheduler</a>, respectively. See the <a href="runtime/index.html#runtime-scheduler"><code>runtime</code> module\ndocumentation</a> for details. In addition, the “macros” feature\nflag enables the <code>#[tokio::main]</code> and <code>#[tokio::test]</code> attributes.</p>',
     '<p>使用运行时需要 “rt” 或 “rt-multi-thread” 特性标志，分别用于启用当前线程的<a href="runtime/index.html#current-thread-scheduler">单线程调度器</a>和<a href="runtime/index.html#multi-thread-scheduler">多线程\n调度器</a>。详情请参阅<a href="runtime/index.html#runtime-scheduler"><code>runtime</code> 模块文档</a>。此外，“macros” 特性\n标志会启用 <code>#[tokio::main]</code> 和 <code>#[tokio::test]</code> 属性。</p>'),

    # ----- CPU-bound tasks and blocking code -----
    ('<p>Tokio is able to concurrently run many tasks on a few threads by repeatedly\nswapping the currently running task on each thread. However, this kind of\nswapping can only happen at <code>.await</code> points, so code that spends a long time\nwithout reaching an <code>.await</code> will prevent other tasks from running. To\ncombat this, Tokio provides two kinds of threads: Core threads and blocking threads.</p>',
     '<p>Tokio 能够通过在线程上反复切换当前正在运行的任务，在少量线程上并发运行大量任务。但是，这种切换只能发生在 <code>.await</code> 处，因此长时间无法到达 <code>.await</code> 的代码会阻止其他任务运行。为了解决这一问题，Tokio 提供了两种线程：核心线程和阻塞线程。</p>'),
    ('<p>The core threads are where all asynchronous code runs, and Tokio will by default\nspawn one for each CPU core. You can use the environment variable <code>TOKIO_WORKER_THREADS</code>\nto override the default value.</p>',
     '<p>核心线程是所有异步代码运行的地方，Tokio 默认会为每个 CPU 核心派生一个核心线程。你可以使用环境变量 <code>TOKIO_WORKER_THREADS</code> 来覆盖默认值。</p>'),
    ('<p>The blocking threads are spawned on demand, can be used to run blocking code\nthat would otherwise block other tasks from running and are kept alive when\nnot used for a certain amount of time which can be configured with <a href="runtime/struct.Builder.html#method.thread_keep_alive" title="method tokio::runtime::Builder::thread_keep_alive"><code>thread_keep_alive</code></a>.\nSince it is not possible for Tokio to swap out blocking tasks, like it\ncan do with asynchronous code, the upper limit on the number of blocking\nthreads is very large. These limits can be configured on the <a href="runtime/struct.Builder.html" title="struct tokio::runtime::Builder"><code>Builder</code></a>.</p>',
     '<p>阻塞线程按需派生，可用于运行那些否则会阻塞其他任务运行的\n阻塞代码。它们在一段时间内未被使用时会被保留，该时间可以通过 <a href="runtime/struct.Builder.html#method.thread_keep_alive" title="method tokio::runtime::Builder::thread_keep_alive"><code>thread_keep_alive</code></a>\n进行配置。由于 Tokio 不可能像对异步代码那样换出阻塞任务，阻塞线程数量的上限非常大。这些限制可以在 <a href="runtime/struct.Builder.html" title="struct tokio::runtime::Builder"><code>Builder</code></a> 上配置。</p>'),
    ('<p>To spawn a blocking task, you should use the <a href="task/fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a> function.</p>',
     '<p>要派生一个阻塞任务，应当使用 <a href="task/fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a> 函数。</p>'),
    # Code comments inside the example
    ('<span class="comment">// This is running on a core thread.\n\n    </span>',
     '<span class="comment">// 这段代码运行在核心线程上。\n\n    </span>'),
    ('<span class="comment">// This is running on a blocking thread.\n        // Blocking here is ok.\n    </span>',
     '<span class="comment">// 这段代码运行在阻塞线程上。\n        // 在这里阻塞是允许的。\n    </span>'),
    ('<span class="comment">// We can wait for the blocking task like this:\n    // If the blocking task panics, the unwrap below will propagate the\n    // panic.\n    </span>',
     '<span class="comment">// 我们可以像这样等待阻塞任务完成：\n    // 如果阻塞任务 panic，下面的 unwrap 将传播该 panic。\n    </span>'),
    ('<p>If your code is CPU-bound and you wish to limit the number of threads used\nto run it, you should use a separate thread pool dedicated to CPU bound tasks.\nFor example, you could consider using the <a href="https://docs.rs/rayon">rayon</a> library for CPU-bound\ntasks. It is also possible to create an extra Tokio runtime dedicated to\nCPU-bound tasks, but if you do this, you should be careful that the extra\nruntime runs <em>only</em> CPU-bound tasks, as IO-bound tasks on that runtime\nwill behave poorly.</p>',
     '<p>如果你的代码是 CPU 密集型的，并且希望限制用于运行它的线程数量，则应使用专用于 CPU 密集型任务的单独线程池。例如，可以考虑使用 <a href="https://docs.rs/rayon">rayon</a> 库来处理 CPU 密集型任务。也可以创建一个专用于 CPU 密集型任务的额外 Tokio 运行时，但如果这样做，需要小心，让该额外运行时<em>仅</em>运行 CPU 密集型任务，因为在该运行时上运行 I/O 密集型任务时表现会很差。</p>'),
    ('<p>Hint: If using rayon, you can use a <a href="sync/oneshot/index.html" title="mod tokio::sync::oneshot"><code>oneshot</code></a> channel to send the result back\nto Tokio when the rayon task finishes.</p>',
     '<p>提示：如果使用 rayon，可以在 rayon 任务完成时使用 <a href="sync/oneshot/index.html" title="mod tokio::sync::oneshot"><code>oneshot</code></a> 通道将结果发送回 Tokio。</p>'),

    # ----- Asynchronous IO -----
    ('<p>As well as scheduling and running tasks, Tokio provides everything you need\nto perform input and output asynchronously.</p>',
     '<p>除了调度和运行任务外，Tokio 还提供了异步执行输入和输出所需的一切功能。</p>'),
    ('<p>The <a href="io/index.html" title="mod tokio::io"><code>tokio::io</code></a> module provides Tokio’s asynchronous core I/O primitives,\nthe <a href="io/trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a>, <a href="io/trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a>, and <a href="io/trait.AsyncBufRead.html" title="trait tokio::io::AsyncBufRead"><code>AsyncBufRead</code></a> traits. In addition,\nwhen the “io-util” feature flag is enabled, it also provides combinators and\nfunctions for working with these traits, forming as an asynchronous\ncounterpart to <a href="https://doc.rust-lang.org/1.95.0/std/io/index.html" title="mod std::io"><code>std::io</code></a>.</p>',
     '<p><a href="io/index.html" title="mod tokio::io"><code>tokio::io</code></a> 模块提供了 Tokio 的异步核心 I/O 原语，即 <a href="io/trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a>、<a href="io/trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> 和 <a href="io/trait.AsyncBufRead.html" title="trait tokio::io::AsyncBufRead"><code>AsyncBufRead</code></a> 这些 trait。此外，当启用了 “io-util” 特性标志时，它还提供了用于处理这些 trait 的组合子和函数，作为 <a href="https://doc.rust-lang.org/1.95.0/std/io/index.html" title="mod std::io"><code>std::io</code></a> 的异步对应物。</p>'),
    ('<p>Tokio also includes APIs for performing various kinds of I/O and interacting\nwith the operating system asynchronously. These include:</p>',
     '<p>Tokio 还包含用于执行各种 I/O 以及与操作系统异步交互的 API。其中包括：</p>'),
    ('<li><a href="net/index.html" title="mod tokio::net"><code>tokio::net</code></a>, which contains non-blocking versions of <a href="net/tcp/index.html" title="mod tokio::net::tcp">TCP</a>, <a href="net/struct.UdpSocket.html" title="struct tokio::net::UdpSocket">UDP</a>, and\n<a href="crate::net::unix">Unix Domain Sockets</a> (enabled by the “net” feature flag),</li>',
     '<li><a href="net/index.html" title="mod tokio::net"><code>tokio::net</code></a>，包含 <a href="net/tcp/index.html" title="mod tokio::net::tcp">TCP</a>、<a href="net/struct.UdpSocket.html" title="struct tokio::net::UdpSocket">UDP</a> 和\n<a href="crate::net::unix">Unix 域套接字</a>的非阻塞版本（通过 “net” 特性标志启用），</li>'),
    ('<li><a href="crate::fs"><code>tokio::fs</code></a>, similar to <a href="https://doc.rust-lang.org/1.95.0/std/fs/index.html" title="mod std::fs"><code>std::fs</code></a> but for performing filesystem I/O\nasynchronously (enabled by the “fs” feature flag),</li>',
     '<li><a href="crate::fs"><code>tokio::fs</code></a>，类似于 <a href="https://doc.rust-lang.org/1.95.0/std/fs/index.html" title="mod std::fs"><code>std::fs</code></a>，但用于异步执行文件系统 I/O\n（通过 “fs” 特性标志启用），</li>'),
    ('<li><a href="crate::signal"><code>tokio::signal</code></a>, for asynchronously handling Unix and Windows OS signals\n(enabled by the “signal” feature flag),</li>',
     '<li><a href="crate::signal"><code>tokio::signal</code></a>，用于异步处理 Unix 和 Windows 操作系统的信号\n（通过 “signal” 特性标志启用），</li>'),
    ('<li><a href="crate::process"><code>tokio::process</code></a>, for spawning and managing child processes (enabled by\nthe “process” feature flag).</li>',
     '<li><a href="crate::process"><code>tokio::process</code></a>，用于派生和管理子进程（通过\n“process” 特性标志启用）。</li>'),

    # ----- Examples -----
    ('<p>A simple TCP echo server:</p>', '<p>一个简单的 TCP 回显服务器：</p>'),
    ('<span class="comment">// In a loop, read data from the socket and write the data back.\n            </span>',
     '<span class="comment">// 在循环中，从套接字读取数据并将其写回。\n            </span>'),
    ('<span class="comment">// socket closed\n                    </span>',
     '<span class="comment">// 套接字已关闭\n                    </span>'),
    ('<span class="comment">// Write the data back\n                </span>',
     '<span class="comment">// 将数据写回\n                </span>'),

    # ----- Feature flags -----
    ('<p>Tokio uses a set of <a href="https://doc.rust-lang.org/cargo/reference/manifest.html#the-features-section">feature flags</a> to reduce the amount of compiled code. It\nis possible to just enable certain features over others. By default, Tokio\ndoes not enable any features but allows one to enable a subset for their use\ncase. Below is a list of the available feature flags. You may also notice\nabove each function, struct and trait there is listed one or more feature flags\nthat are required for that item to be used. If you are new to Tokio it is\nrecommended that you use the <code>full</code> feature flag which will enable all public APIs.\nBeware though that this will pull in many extra dependencies that you may not\nneed.</p>',
     '<p>Tokio 使用一组<a href="https://doc.rust-lang.org/cargo/reference/manifest.html#the-features-section">特性标志</a>来减少编译代码量。可以只启用其中某些特性而不启用其他特性。默认情况下，Tokio 不会启用任何特性，但允许你为用例启用一个子集。下面是可用特性标志的列表。你可能还会注意到在每个函数、结构体和 trait 上方会列出使用该项所需的一个或多个特性标志。如果你是 Tokio 的新手，建议使用 <code>full</code> 特性标志，它会启用所有公开 API。但请注意，这会引入许多你可能不需要的额外依赖。</p>'),
    ('<li><code>full</code>: Enables all features listed below except <code>test-util</code> and unstable features.</li>',
     '<li><code>full</code>：启用下面列出的所有特性，<code>test-util</code> 和不稳定特性除外。</li>'),
    ('<li><code>rt</code>: Enables <code>tokio::spawn</code>, the current-thread scheduler,\nand non-scheduler utilities.</li>',
     '<li><code>rt</code>：启用 <code>tokio::spawn</code>、当前线程调度器\n以及非调度器相关的工具。</li>'),
    ('<li><code>rt-multi-thread</code>: Enables the heavier, multi-threaded, work-stealing scheduler.</li>',
     '<li><code>rt-multi-thread</code>：启用较重的、多线程的工作窃取调度器。</li>'),
    ('<li><code>io-util</code>: Enables the IO based <code>Ext</code> traits.</li>',
     '<li><code>io-util</code>：启用基于 I/O 的 <code>Ext</code> trait。</li>'),
    ('<li><code>io-std</code>: Enable <code>Stdout</code>, <code>Stdin</code> and <code>Stderr</code> types.</li>',
     '<li><code>io-std</code>：启用 <code>Stdout</code>、<code>Stdin</code> 和 <code>Stderr</code> 类型。</li>'),
    ('<li><code>net</code>: Enables <code>tokio::net</code> types such as <code>TcpStream</code>, <code>UnixStream</code> and\n<code>UdpSocket</code>, as well as (on Unix-like systems) <code>AsyncFd</code> and (on\nFreeBSD) <code>PollAio</code>.</li>',
     '<li><code>net</code>：启用 <code>tokio::net</code> 中的类型，如 <code>TcpStream</code>、<code>UnixStream</code> 和\n<code>UdpSocket</code>，以及（类 Unix 系统上的）<code>AsyncFd</code> 和（FreeBSD 上的）<code>PollAio</code>。</li>'),
    ('<li><code>time</code>: Enables <code>tokio::time</code> types and allows the schedulers to enable\nthe built-in timer.</li>',
     '<li><code>time</code>：启用 <code>tokio::time</code> 中的类型，并允许调度器启用\n内置定时器。</li>'),
    ('<li><code>process</code>: Enables <code>tokio::process</code> types.</li>',
     '<li><code>process</code>：启用 <code>tokio::process</code> 中的类型。</li>'),
    ('<li><code>macros</code>: Enables <code>#[tokio::main]</code> and <code>#[tokio::test]</code> macros.</li>',
     '<li><code>macros</code>：启用 <code>#[tokio::main]</code> 和 <code>#[tokio::test]</code> 宏。</li>'),
    ('<li><code>sync</code>: Enables all <code>tokio::sync</code> types.</li>',
     '<li><code>sync</code>：启用所有 <code>tokio::sync</code> 类型。</li>'),
    ('<li><code>signal</code>: Enables all <code>tokio::signal</code> types.</li>',
     '<li><code>signal</code>：启用所有 <code>tokio::signal</code> 类型。</li>'),
    ('<li><code>fs</code>: Enables <code>tokio::fs</code> types.</li>',
     '<li><code>fs</code>：启用 <code>tokio::fs</code> 类型。</li>'),
    ('<li><code>test-util</code>: Enables testing based infrastructure for the Tokio runtime.</li>',
     '<li><code>test-util</code>：启用 Tokio 运行时的测试相关基础设施。</li>'),
    ('<li><code>parking_lot</code>: As a potential optimization, use the [<code>parking_lot</code>] crate’s\nsynchronization primitives internally. Also, this\ndependency is necessary to construct some of our primitives\nin a <code>const</code> context. <code>MSRV</code> may increase according to the\n[<code>parking_lot</code>] release in use.</li>',
     '<li><code>parking_lot</code>：作为一种潜在优化，内部使用 [<code>parking_lot</code>] crate 的\n同步原语。此外，该依赖也是在 <code>const</code> 上下文中构造\n我们某些原语所必需的。<code>MSRV</code> 可能会根据所使用\n的 [<code>parking_lot</code>] 版本而提高。</li>'),
    ('<p><em>Note: <code>AsyncRead</code> and <code>AsyncWrite</code> traits do not require any features and are\nalways available.</em></p>',
     '<p><em>注意：<code>AsyncRead</code> 和 <code>AsyncWrite</code> trait 不需要任何特性，始终可用。</em></p>'),

    # ----- Unstable features -----
    ('<p>Some feature flags are only available when specifying the <code>tokio_unstable</code> flag:</p>',
     '<p>某些特性标志仅在指定了 <code>tokio_unstable</code> 标志时才可用：</p>'),
    ('<li><code>tracing</code>: Enables tracing events.</li>',
     '<li><code>tracing</code>：启用 tracing 事件。</li>'),
    ('<li><code>io-uring</code>: Enables <code>io-uring</code> (Linux only).</li>',
     '<li><code>io-uring</code>：启用 <code>io-uring</code>（仅限 Linux）。</li>'),
    ('<li><code>taskdump</code>: Enables <code>taskdump</code> (Linux only).</li>',
     '<li><code>taskdump</code>：启用 <code>taskdump</code>（仅限 Linux）。</li>'),
    ('<p>Likewise, this flag enables access to unstable APIs.</p>',
     '<p>同样，此标志可以访问不稳定的 API。</p>'),
    ('<p>This flag enables <strong>unstable</strong> features. The public API of these features\nmay break in 1.x releases. To enable these features, the <code>--cfg tokio_unstable</code> argument must be passed to <code>rustc</code> when compiling. This\nserves to explicitly opt-in to features which may break semver conventions,\nsince Cargo <a href="https://internals.rust-lang.org/t/feature-request-unstable-opt-in-non-transitive-crate-features/16193#why-not-a-crate-feature-2">does not yet directly support such opt-ins</a>.</p>',
     '<p>此标志启用<strong>不稳定</strong>特性。这些特性的公开 API 可能会在 1.x 版本中发生破坏性变更。要启用这些特性，在编译时必须向 <code>rustc</code> 传递 <code>--cfg tokio_unstable</code> 参数。这样做是为了显式选择加入可能违反 semver 约定的特性，因为 Cargo <a href="https://internals.rust-lang.org/t/feature-request-unstable-opt-in-non-transitive-crate-features/16193#why-not-a-crate-feature-2">尚不直接支持此类选择加入</a>。</p>'),
    ('<p>You can specify it in your project’s <code>.cargo/config.toml</code> file:</p>',
     '<p>可以在项目的 <code>.cargo/config.toml</code> 文件中指定它：</p>'),
    ('<div class="warning">\nThe <code>[build]</code> section does <strong>not</strong> go in a\n<code>Cargo.toml</code> file. Instead it must be placed in the Cargo config\nfile <code>.cargo/config.toml</code>.\n</div>',
     '<div class="warning">\n<code>[build]</code> 节<strong>不是</strong>放在 <code>Cargo.toml</code> 文件中，\n而必须放在 Cargo 配置文件 <code>.cargo/config.toml</code> 中。\n</div>'),
    ('<p>Alternatively, you can specify it with an environment variable:</p>',
     '<p>或者，可以通过环境变量来指定它：</p>'),

    # ----- Supported platforms -----
    ('<p>Tokio currently guarantees support for the following platforms:</p>',
     '<p>Tokio 目前保证支持以下平台：</p>'),
    ('<li>Linux</li>', '<li>Linux</li>'),
    ('<li>Windows</li>', '<li>Windows</li>'),
    ('<li>Android (API level 21)</li>', '<li>Android（API 级别 21）</li>'),
    ('<li>macOS</li>', '<li>macOS</li>'),
    ('<li>iOS</li>', '<li>iOS</li>'),
    ('<li>FreeBSD</li>', '<li>FreeBSD</li>'),
    ('<p>Tokio will continue to support these platforms in the future. However,\nfuture releases may change requirements such as the minimum required libc\nversion on Linux, the API level on Android, or the supported FreeBSD\nrelease.</p>',
     '<p>Tokio 将在未来继续支持这些平台。但是，未来的版本可能会更改一些要求，例如 Linux 上所需的最低 libc 版本、Android 上的 API 级别，或受支持的 FreeBSD 版本。</p>'),
    ('<p>Beyond the above platforms, Tokio is intended to work on all platforms\nsupported by the mio crate. You can find a longer list <a href="https://crates.io/crates/mio#platforms">in mio’s\ndocumentation</a>. However, these additional platforms may\nbecome unsupported in the future.</p>',
     '<p>除上述平台外，Tokio 旨在能在 mio crate 支持的所有平台上运行。可以在 <a href="https://crates.io/crates/mio#platforms">mio 的文档中</a>找到更长的平台列表。但是，这些额外的平台在未来可能会变得不再受支持。</p>'),
    ('<p>Note that Wine is considered to be a different platform from Windows. See\nmio’s documentation for more information on Wine support.</p>',
     '<p>请注意，Wine 被视为与 Windows 不同的平台。有关 Wine 支持的更多信息，请参阅 mio 的文档。</p>'),

    # ----- WASM support -----
    ('<p>Tokio has some limited support for the <code>WASM</code> platform. Without the\n<code>tokio_unstable</code> flag, the following features are supported:</p>',
     '<p>Tokio 对 <code>WASM</code> 平台有一些有限的支持。在不使用 <code>tokio_unstable</code> 标志的情况下，支持以下特性：</p>'),
    ('<li><code>sync</code></li>', '<li><code>sync</code></li>'),
    ('<li><code>macros</code></li>', '<li><code>macros</code></li>'),
    ('<li><code>io-util</code></li>', '<li><code>io-util</code></li>'),
    ('<li><code>rt</code></li>', '<li><code>rt</code></li>'),
    ('<li><code>time</code></li>', '<li><code>time</code></li>'),
    ('<p>Enabling any other feature (including <code>full</code>) will cause a compilation\nfailure.</p>',
     '<p>启用任何其他特性（包括 <code>full</code>）都会导致编译失败。</p>'),
    ('<p>The <code>time</code> module will only work on <code>WASM</code> platforms that have support for\ntimers (e.g. wasm32-wasi). The timing functions will panic if used on a <code>WASM</code>\nplatform that does not support timers.</p>',
     '<p><code>time</code> 模块仅在支持定时器的 <code>WASM</code> 平台（例如 wasm32-wasi）上可用。在不支持定时器的 <code>WASM</code> 平台上使用时，相关的时间函数会 panic。</p>'),
    ('<p>Note also that if the runtime becomes indefinitely idle, it will panic\nimmediately instead of blocking forever. On platforms that don’t support\ntime, this means that the runtime can never be idle in any way.</p>',
     '<p>还需注意，如果运行时无限期地空闲，它会立即 panic，而不是永远阻塞。在不支持时间的平台上，这意味着运行时永远不能以任何方式处于空闲状态。</p>'),

    # ----- Unstable WASM support -----
    ('<p>Tokio also has unstable support for some additional <code>WASM</code> features. This\nrequires the use of the <code>tokio_unstable</code> flag.</p>',
     '<p>Tokio 还不稳定地支持一些额外的 <code>WASM</code> 特性。这需要使用 <code>tokio_unstable</code> 标志。</p>'),
    ('<p>Using this flag enables the use of <code>tokio::net</code> on the wasm32-wasi target.\nHowever, not all methods are available on the networking types as <code>WASI</code>\ncurrently does not support the creation of new sockets from within <code>WASM</code>.\nBecause of this, sockets must currently be created via the <code>FromRawFd</code>\ntrait.</p>',
     '<p>使用此标志可以在 wasm32-wasi 目标上使用 <code>tokio::net</code>。但是，并非所有方法都可在网络类型上使用，因为 <code>WASI</code> 目前不支持从 <code>WASM</code> 内部创建新套接字。因此，目前必须通过 <code>FromRawFd</code> trait 来创建套接字。</p>'),

    # ----- Item descriptions in module/macro tables -----
    # Re-exports (none have description text, just the line)
    # Modules
    ('<dd>Traits, helpers, and type definitions for asynchronous I/O functionality.</dd>',
     '<dd>异步 I/O 功能的 trait、辅助类型和类型定义。</dd>'),
    ('<dd>TCP/UDP/Unix bindings for <code>tokio</code>.</dd>',
     '<dd><code>tokio</code> 的 TCP/UDP/Unix 绑定。</dd>'),
    ('<dd>The Tokio runtime.</dd>', '<dd>Tokio 运行时。</dd>'),
    ('<dd>Due to the <code>Stream</code> trait’s inclusion in <code>std</code> landing later than Tokio’s 1.0\nrelease, most of the Tokio stream utilities have been moved into the <a href="https://docs.rs/tokio-stream"><code>tokio-stream</code></a>\ncrate.</dd>',
     '<dd>由于 <code>Stream</code> trait 进入 <code>std</code> 的时间晚于 Tokio 1.0 发布，\nTokio 的大多数流相关工具已迁移到 <a href="https://docs.rs/tokio-stream"><code>tokio-stream</code></a>\ncrate 中。</dd>'),
    ('<dd>Synchronization primitives for use in asynchronous contexts.</dd>',
     '<dd>用于异步上下文的同步原语。</dd>'),
    ('<dd>Asynchronous green-threads.</dd>', '<dd>异步的绿色线程。</dd>'),
    ('<dd>Utilities for tracking time.</dd>', '<dd>用于跟踪时间的工具。</dd>'),
    # Macros
    ('<dd>Pins a value on the stack.</dd>', '<dd>在栈上固定一个值。</dd>'),
    ('<dd>Declares a new task-local key of type <a href="task/struct.LocalKey.html" title="struct tokio::task::LocalKey"><code>tokio::task::LocalKey</code></a>.</dd>',
     '<dd>声明一个类型为 <a href="task/struct.LocalKey.html" title="struct tokio::task::LocalKey"><code>tokio::task::LocalKey</code></a> 的新任务局部键。</dd>'),
]


# ============================================================================
# Section header text inside <h2 id="..."> tags (visible in the docblock)
# ============================================================================
SECTION_HEADER_PAIRS = [
    # These are the H2/H3/H4/H5 visible headings (not the title attributes)
    ('>A Tour of Tokio<', '>Tokio 概览<'),
    ('>Working With Tasks<', '>使用任务<'),
    ('>CPU-bound tasks and blocking code<', '>CPU 密集型任务与阻塞代码<'),
    ('>Asynchronous IO<', '>异步 I/O<'),
    ('>Examples<', '>示例<'),
    ('>Feature flags<', '>特性标志<'),
    ('>Unstable features<', '>不稳定特性<'),
    ('>Supported platforms<', '>支持的平台<'),
    ('>Authoring applications<', '>编写应用程序<'),
    ('>Authoring libraries<', '>编写库<'),
    ('>Re-exports<', '>重新导出<'),
    ('>Modules<', '>模块<'),
    ('>Macros<', '>宏<'),
    # Topbar H1 (Crate) and H2 nav
    ('>Crate tokio<', '>crate tokio<'),
    ('>Crate <span>tokio</span>', '>crate <span>tokio</span>'),
]


def apply_pairs(content, pairs, label=''):
    """Apply a list of (old, new) replacements, tracking misses."""
    missed = []
    for old, new in pairs:
        if old not in content:
            missed.append(old)
        content = content.replace(old, new)
    if missed:
        for m in missed[:5]:
            print(f'  [MISS] {label}: {m[:80]!r}')
        if len(missed) > 5:
            print(f'  [MISS] {label}: ... and {len(missed)-5} more')
    return content


def translate_tokio_index(content):
    # Meta description (must match exactly; this is the only meta description line)
    old_meta = '<meta name="description" content="A runtime for writing reliable network applications without compromising speed.">'
    new_meta = '<meta name="description" content="一个用于编写可靠网络应用程序且不妥协性能的运行时。">'
    if old_meta not in content:
        print('  [MISS] meta description')
    content = content.replace(old_meta, new_meta)

    # Title (keep crate name in title; just ensure lang)
    content = content.replace('<title>tokio - Rust</title>', '<title>tokio - Rust</title>')
    content = content.replace('<html lang="en">', '<html lang="zh-CN">')

    # Common UI replacements
    content = apply_pairs(content, COMMON_UI, 'common UI')
    # Docblock content
    content = apply_pairs(content, DOCBLOCK_PAIRS, 'docblock')
    # Section header text
    content = apply_pairs(content, SECTION_HEADER_PAIRS, 'section headers')

    return content


def main():
    path = os.path.join(TOKIO_ROOT, 'index.html')
    print(f'--- {path} ---')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = translate_tokio_index(content)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    verify(new_content, 'tokio/index.html')
    print()


if __name__ == '__main__':
    main()
