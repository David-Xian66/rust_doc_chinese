# -*- coding: utf-8 -*-
"""Translate tokio/runtime/ HTML docblocks (subagent).

Bytes mode (rb/wb) to preserve UTF-8 + CRLF. Replace English docblock text with Chinese.
Long-string-first ordering.
"""

import os
import sys

# Path of this script's directory
RUNTIME_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))


def b(s):
    """Encode s as UTF-8 bytes with LF line endings (these files use LF)."""
    return s.replace('\r\n', '\n').encode('utf-8')


# PAIRS list: (en_bytes, zh_bytes)
# Long patterns first to avoid sub-matching.
PAIRS = [
    # ========== index.html (module description) ==========
    (b('<p>The Tokio runtime.</p>\r\n<p>Unlike other Rust programs, asynchronous applications require runtime\r\nsupport. In particular, the following runtime services are necessary:</p>'),
     b('<p>Tokio 运行时。</p>\r\n<p>与其他 Rust 程序不同，异步应用需要运行时的支持。具体而言，需要以下运行时服务：</p>')),

    (b('<li>An <strong>I/O event loop</strong>, called the driver, which drives I/O resources and\r\ndispatches I/O events to tasks that depend on them.</li>'),
     b('<li>一个 <strong>I/O 事件循环</strong>（称为 driver），它驱动 I/O 资源，并把 I/O 事件分发给依赖这些资源的任务。</li>')),

    (b('<li>A <strong>scheduler</strong> to execute <a href="../task/index.html" title="mod tokio::task">tasks</a> that use these I/O resources.</li>'),
     b('<li>一个 <strong>调度器</strong>，用于执行使用这些 I/O 资源的<a href="../task/index.html" title="mod tokio::task">任务</a>。</li>')),

    (b('<li>A <strong>timer</strong> for scheduling work to run after a set period of time.</li>'),
     b('<li>一个 <strong>定时器</strong>，用于在一段时间后调度工作的运行。</li>')),

    (b('<p>Tokio’s <a href="struct.Runtime.html" title="struct tokio::runtime::Runtime"><code>Runtime</code></a> bundles all of these services as a single type, allowing\r\nthem to be started, shut down, and configured together. However, often it is\r\nnot required to configure a <a href="struct.Runtime.html" title="struct tokio::runtime::Runtime"><code>Runtime</code></a> manually, and a user may just use the\r\n<a href="../attr.main.html"><code>tokio::main</code></a> attribute macro, which creates a <a href="struct.Runtime.html" title="struct tokio::runtime::Runtime"><code>Runtime</code></a> under the hood.</p>'),
     b('<p>Tokio 的<a href="struct.Runtime.html" title="struct tokio::runtime::Runtime"><code>Runtime</code></a>将这些服务捆绑为单一类型，允许它们一起启动、关闭和配置。但通常不需要手动配置<a href="struct.Runtime.html" title="struct tokio::runtime::Runtime"><code>Runtime</code></a>，用户可以直接使用<a href="../attr.main.html"><code>tokio::main</code></a>属性宏，它会在底层创建一个<a href="struct.Runtime.html" title="struct tokio::runtime::Runtime"><code>Runtime</code></a>。</p>')),

    (b('<p>Here is the rules of thumb to choose the right runtime for your application.</p>'),
     b('<p>以下是为应用选择合适运行时的经验法则。</p>')),

    # ========== fn.is_rt_shutdown_err.html ==========
    (b('<p>Checks whether the given error was emitted by Tokio when shutting down its runtime.</p>'),
     b('<p>检查给定的错误是否由 Tokio 在关闭其运行时时发出。</p>')),

    # ========== enum.RuntimeFlavor.html ==========
    (b('<p>The flavor of a <code>Runtime</code>.</p>\r\n<p>This is the return type for <a href="struct.Handle.html#method.runtime_flavor" title="method tokio::runtime::Handle::runtime_flavor"><code>Handle::runtime_flavor</code></a>.</p>'),
     b('<p><code>Runtime</code> 的类型风格。</p>\r\n<p>这是 <a href="struct.Handle.html#method.runtime_flavor" title="method tokio::runtime::Handle::runtime_flavor"><code>Handle::runtime_flavor</code></a> 的返回类型。</p>')),

    (b('Non-exhaustive enums could have additional variants added in future. Therefore, when matching against variants of non-exhaustive enums, an extra wildcard arm must be added to account for any future variants.'),
     b('非穷尽枚举将来可能会添加额外的变体。因此，在对非穷尽枚举的变体进行匹配时，必须添加一个额外的通配符分支以涵盖未来的任何变体。')),

    (b('<p>The flavor that executes all tasks on the current thread.</p>'),
     b('<p>在当前线程上执行所有任务的类型风格。</p>')),

    (b('<p>The flavor that executes tasks across multiple threads.</p>'),
     b('<p>跨多个线程执行任务的类型风格。</p>')),

    # ========== struct.EnterGuard.html ==========
    (b('<p>Runtime context guard.</p>\r\n<p>Returned by <a href="struct.Runtime.html#method.enter" title="method tokio::runtime::Runtime::enter"><code>Runtime::enter</code></a> and <a href="struct.Handle.html#method.enter" title="method tokio::runtime::Handle::enter"><code>Handle::enter</code></a>, the context guard exits\r\nthe runtime context on drop.</p>'),
     b('<p>运行时上下文守卫。</p>\r\n<p>由 <a href="struct.Runtime.html#method.enter" title="method tokio::runtime::Runtime::enter"><code>Runtime::enter</code></a> 和 <a href="struct.Handle.html#method.enter" title="method tokio::runtime::Handle::enter"><code>Handle::enter</code></a> 返回，该上下文守卫在 drop 时退出运行时上下文。</p>')),

    # ========== struct.LocalOptions.html ==========
    (b('<p><a href="struct.LocalRuntime.html" title="struct tokio::runtime::LocalRuntime"><code>LocalRuntime</code></a>-only config options</p>'),
     b('<p><a href="struct.LocalRuntime.html" title="struct tokio::runtime::LocalRuntime"><code>LocalRuntime</code></a> 专属的配置选项</p>')),

    (b('<p>Currently, there are no such options, but in the future, things like <code>!Send + !Sync</code> hooks may\r\nbe added.</p>'),
     b('<p>目前尚无此类选项，但未来可能会添加类似 <code>!Send + !Sync</code> 钩子的选项。</p>')),

    (b('<p>Use <code>LocalOptions::default()</code> to create the default set of options. This type is used with\r\n<a href="struct.Builder.html#method.build_local" title="method tokio::runtime::Builder::build_local"><code>Builder::build_local</code>'),
     b('<p>使用 <code>LocalOptions::default()</code> 创建默认选项集。此类型与 <a href="struct.Builder.html#method.build_local" title="method tokio::runtime::Builder::build_local"><code>Builder::build_local</code>')),

    # ========== struct.Id.html ==========
    (b('<p>An opaque ID that uniquely identifies a runtime relative to all other currently\r\nrunning runtimes.</p>'),
     b('<p>一个不透明的 ID，相对于所有其他当前正在运行的运行时唯一标识一个运行时。</p>')),

    (b('<li>Runtime IDs are unique relative to other <em>currently running</em> runtimes.\r\nWhen a runtime completes, the same ID may be used for another runtime.</li>'),
     b('<li>Runtime ID 相对于其他<em>当前正在运行</em>的运行时是唯一的。当一个运行时结束后，同一 ID 可被另一个运行时复用。</li>')),

    (b('<li>Runtime IDs are <em>not</em> sequential, and do not indicate the order in which\r\nruntimes are started or any other data.</li>'),
     b('<li>Runtime ID <em>不是</em>连续的，也不表示运行时启动的顺序或任何其他数据。</li>')),

    # ========== struct.TryCurrentError.html ==========
    (b('<p>Error returned by <code>try_current</code> when no Runtime has been started</p>'),
     b('<p>在没有启动 Runtime 时由 <code>try_current</code> 返回的错误</p>')),

    (b('<p>Returns true if the call failed because there is currently no runtime in\r\nthe Tokio context.</p>'),
     b('<p>如果调用因当前 Tokio 上下文中没有运行时而失败，则返回 true。</p>')),

    (b('<p>Returns true if the call failed because the Tokio context thread-local\r\nhad been destroyed. This can usually only happen if in the destructor of\r\nother thread-locals.</p>'),
     b('<p>如果调用因 Tokio 上下文线程局部变量已被销毁而失败，则返回 true。这通常只会在其他线程局部变量的析构函数中发生。</p>')),

    # ========== struct.Handle.html ==========
    (b('<p>Handle to the runtime.</p>\r\n<p>The handle is internally reference-counted and can be freely cloned. A handle can be\r\nobtained using the <a href="struct.Runtime.html#method.handle" title="method tokio::runtime::Runtime::handle"><code>Runtime::handle</code></a> method.</p>'),
     b('<p>运行时的句柄。</p>\r\n<p>句柄内部使用引用计数，可以自由克隆。可以通过 <a href="struct.Runtime.html#method.handle" title="method tokio::runtime::Runtime::handle"><code>Runtime::handle</code></a> 方法获取句柄。</p>')),

    (b('<p>Enters the runtime context. This allows you to construct types that must\r\nhave an executor available on creation such as <a href="../time/struct.Sleep.html" title="struct tokio::time::Sleep"><code>Sleep</code></a> or\r\n<a href="../net/struct.TcpStream.html" title="struct tokio::net::TcpStream"><code>TcpStream</code></a>. It will also allow you to call methods such as\r\n<a href="../task/fn.spawn.html" title="fn tokio::task::spawn"><code>tokio::spawn</code></a> and <a href="struct.Handle.html#method.current" title="associated function tokio::runtime::Handle::current"><code>Handle::current</code></a> without panicking.</p>'),
     b('<p>进入运行时上下文。这允许你构造创建时必须有可用执行器的类型，例如 <a href="../time/struct.Sleep.html" title="struct tokio::time::Sleep"><code>Sleep</code></a> 或\r\n<a href="../net/struct.TcpStream.html" title="struct tokio::net::TcpStream"><code>TcpStream</code></a>。它还允许你调用 <a href="../task/fn.spawn.html" title="fn tokio::task::spawn"><code>tokio::spawn</code></a> 和 <a href="struct.Handle.html#method.current" title="associated function tokio::runtime::Handle::current"><code>Handle::current</code></a> 等方法而不会 panic。</p>')),

    (b('<p>When calling <code>Handle::enter</code> multiple times, the returned guards\r\n<strong>must</strong> be dropped in the reverse order that they were acquired.\r\nFailure to do so will result in a panic and possible memory leaks.</p>'),
     b('<p>多次调用 <code>Handle::enter</code> 时，返回的守卫<strong>必须</strong>按与获取相反的顺序 drop。\r\n否则会导致 panic 以及可能的内存泄漏。</p>')),

    (b('<p>Returns a <code>Handle</code> view over the currently running <code>Runtime</code>.</p>'),
     b('<p>返回当前正在运行的 <code>Runtime</code> 的 <code>Handle</code> 视图。</p>')),

    (b('<p>This will panic if called outside the context of a Tokio runtime. That means that you must\r\ncall this on one of the threads <strong>being run by the runtime</strong>, or from a thread with an active\r\n<code>EnterGuard</code>. Calling this from within a thread created by <code>std::thread::spawn</code> (for example)\r\nwill cause a panic unless that thread has an active <code>EnterGuard</code>.</p>'),
     b('<p>如果在 Tokio 运行时的上下文之外调用此方法会 panic。也就是说，你必须在<strong>由运行时运行的</strong>某个线程上调用此方法，或者在持有活跃 <code>EnterGuard</code> 的线程上调用。例如，在由 <code>std::thread::spawn</code> 创建的线程内调用此方法会导致 panic，除非该线程持有活跃的 <code>EnterGuard</code>。</p>')),

    (b('<p>This can be used to obtain the handle of the surrounding runtime from an async\r\nblock or function running on that runtime.</p>'),
     b('<p>此方法可用于从该运行时上运行的异步块或异步函数中获取其所属运行时的句柄。</p>')),

    (b('<p>Returns a Handle view over the currently running Runtime</p>'),
     b('<p>返回当前正在运行的 Runtime 的 Handle 视图</p>')),

    (b('<p>Returns an error if no Runtime has been started</p>'),
     b('<p>如果没有启动 Runtime，则返回错误</p>')),

    (b('<p>Contrary to <code>current</code>, this never panics</p>'),
     b('<p>与 <code>current</code> 不同，此方法永远不会 panic</p>')),

    (b('<p>Spawns a future onto the Tokio runtime.</p>'),
     b('<p>将 future 派生到 Tokio 运行时上。</p>')),

    (b('<p>This spawns the given future onto the runtime’s executor, usually a\r\nthread pool. The thread pool is then responsible for polling the future\r\nuntil it completes.</p>'),
     b('<p>此方法将给定的 future 派生到运行时的执行器（通常是线程池）上。然后由线程池负责 poll future 直到其完成。</p>')),

    (b('<p>The provided future will start running in the background immediately\r\nwhen <code>spawn</code> is called, even if you don’t await the returned\r\n<code>JoinHandle</code> (assuming that the runtime <a href="index.html#driving-the-runtime">is running</a>).</p>'),
     b('<p>给定的 future 在调用 <code>spawn</code> 后会立即开始在后台运行，即使你没有 await 返回的 <code>JoinHandle</code>（前提是运行时<a href="index.html#driving-the-runtime">正在运行</a>）。</p>')),

    (b('<p>See <a href="index.html">module level</a> documentation for more details.</p>'),
     b('<p>更多详细信息请参见<a href="index.html">模块级</a>文档。</p>')),

    (b('<p>Runs the provided function on an executor dedicated to blocking\r\noperations.</p>'),
     b('<p>在专用于阻塞操作的执行器上运行提供的函数。</p>')),

    (b('<p>Runs a future to completion on this <code>Handle</code>’s associated <code>Runtime</code>.</p>'),
     b('<p>在该 <code>Handle</code> 所关联的 <code>Runtime</code> 上运行一个 future 直到完成。</p>')),

    (b('<p>This runs the given future on the current thread, blocking until it is\r\ncomplete, and yielding its resolved result. Any tasks or timers which\r\nthe future spawns internally will be executed on the runtime.</p>'),
     b('<p>此方法在当前线程上运行给定的 future，阻塞直到其完成，并产出其解析后的结果。future 在内部派生的任何任务或定时器都将在运行时上执行。</p>')),

    (b('<p>When this is used on a <code>current_thread</code> runtime, only the\r\n<a href="struct.Runtime.html#method.block_on" title="method tokio::runtime::Runtime::block_on"><code>Runtime::block_on</code></a> method can drive the IO and timer drivers, but the\r\n<code>Handle::block_on</code> method cannot drive them. This means that, when using\r\nthis method on a <code>current_thread</code> runtime, anything that relies on IO or\r\ntimers will not work unless there is another thread currently calling\r\n<a href="struct.Runtime.html#method.block_on" title="method tokio::runtime::Runtime::block_on"><code>Runtime::block_on</code></a> on the same runtime.</p>'),
     b('<p>当在 <code>current_thread</code> 运行时上使用时，只有 <a href="struct.Runtime.html#method.block_on" title="method tokio::runtime::Runtime::block_on"><code>Runtime::block_on</code></a> 方法能够驱动 IO 和 timer driver，而 <code>Handle::block_on</code> 方法不能驱动它们。这意味着，在 <code>current_thread</code> 运行时上使用此方法时，任何依赖 IO 或 timer 的功能都无法工作，除非同一运行时上有另一个线程正在调用 <a href="struct.Runtime.html#method.block_on" title="method tokio::runtime::Runtime::block_on"><code>Runtime::block_on</code></a>。</p>')),

    (b('<p>Returns the flavor of the current <code>Runtime</code>.</p>'),
     b('<p>返回当前 <code>Runtime</code> 的类型风格。</p>')),

    (b('<p>Returns the <a href="struct.Id.html" title="struct tokio::runtime::Id"><code>Id</code></a> of the current <code>Runtime</code>.</p>'),
     b('<p>返回当前 <code>Runtime</code> 的 <a href="struct.Id.html" title="struct tokio::runtime::Id"><code>Id</code></a>。</p>')),

    (b('<p>Returns the name of the current <code>Runtime</code>.</p>'),
     b('<p>返回当前 <code>Runtime</code> 的名称。</p>')),

    (b('<p>Returns a view that lets you get information about how the runtime\r\nis performing.</p>'),
     b('<p>返回一个视图，可用于获取运行时运行状况的相关信息。</p>')),

    # ========== struct.Runtime.html ==========
    (b('<p>The Tokio runtime.</p>\r\n<p>The runtime provides an I/O driver, task scheduler, <a href="../time/index.html" title="mod tokio::time">timer</a>, and\r\nblocking pool, necessary for running asynchronous tasks.</p>'),
     b('<p>Tokio 运行时。</p>\r\n<p>运行时提供了 I/O driver、任务调度器、<a href="../time/index.html" title="mod tokio::time">定时器</a>和阻塞池，是运行异步任务所必需的。</p>')),

    (b('<p>Instances of <code>Runtime</code> can be created using <a href="struct.Runtime.html#method.new" title="associated function tokio::runtime::Runtime::new"><code>new</code></a>, or <a href="struct.Builder.html" title="struct tokio::runtime::Builder"><code>Builder</code></a>.\r\nHowever, most users will use the <a href="../attr.main.html" title="attr tokio::main"><code>#[tokio::main]</code></a> annotation on\r\ntheir entry point instead.</p>'),
     b('<p>可以使用 <a href="struct.Runtime.html#method.new" title="associated function tokio::runtime::Runtime::new"><code>new</code></a> 或 <a href="struct.Builder.html" title="struct tokio::runtime::Builder"><code>Builder</code></a> 创建 <code>Runtime</code> 实例。\r\n不过，大多数用户会在其入口点使用 <a href="../attr.main.html" title="attr tokio::main"><code>#[tokio::main]</code></a> 注解。</p>')),

    (b('<p>Shutting down the runtime is done by dropping the value, or calling\r\n<a href="struct.Runtime.html#method.shutdown_background" title="method tokio::runtime::Runtime::shutdown_background"><code>shutdown_background</code></a>\r\nimmediately. The former will block until the runtime has completed all\r\nits work, while the latter will shutdown asynchronously.</p>'),
     b('<p>可以通过 drop 该值来关闭运行时，或者立即调用 <a href="struct.Runtime.html#method.shutdown_background" title="method tokio::runtime::Runtime::shutdown_background"><code>shutdown_background</code></a>。前者会阻塞直到运行时完成所有工作，而后者会异步关闭。</p>')),

    (b('<p>Creates a new runtime instance with default configuration values.</p>'),
     b('<p>使用默认配置值创建一个新的运行时实例。</p>')),

    (b('<p>This results in the multi threaded scheduler, I/O driver, and time driver being\r\ninitialized.</p>'),
     b('<p>这将初始化多线程调度器、I/O driver 和 time driver。</p>')),

    (b('<p>Most applications will not need to call this function directly. Instead,\r\nthey will use the  <a href="../attr.main.html"><code>#[tokio::main]</code> attribute</a>. When a more complex\r\nconfiguration is necessary, the <a href="struct.Builder.html" title="struct tokio::runtime::Builder">runtime builder</a> may be used.</p>'),
     b('<p>大多数应用程序不需要直接调用此函数。它们将使用 <a href="../attr.main.html"><code>#[tokio::main]</code> 属性</a>。当需要更复杂的配置时，可以使用<a href="struct.Builder.html" title="struct tokio::runtime::Builder">运行时 builder</a>。</p>')),

    (b('<p>Creating a new <code>Runtime</code> with default configuration values.</p>'),
     b('<p>使用默认配置值创建一个新的 <code>Runtime</code>。</p>')),

    (b('<p>Returns a handle to the runtime’s spawner.</p>'),
     b('<p>返回运行时 spawner 的句柄。</p>')),

    (b('<p>The returned handle can be used to spawn tasks that run on this runtime, and can\r\nbe cloned to allow moving the <code>Handle</code> to other threads.</p>'),
     b('<p>返回的句柄可用于派生在此运行时上运行的任务，并且可以克隆，以便将 <code>Handle</code> 移动到其他线程。</p>')),

    (b('<p>Calling <a href="struct.Handle.html#method.block_on" title="method tokio::runtime::Handle::block_on"><code>Handle::block_on</code></a> on a handle to a <code>current_thread</code> runtime is error-prone.\r\nRefer to the documentation of <a href="struct.Handle.html#method.block_on" title="method tokio::runtime::Handle::block_on"><code>Handle::block_on</code></a> for more.</p>'),
     b('<p>在 <code>current_thread</code> 运行时的句柄上调用 <a href="struct.Handle.html#method.block_on" title="method tokio::runtime::Handle::block_on"><code>Handle::block_on</code></a> 是容易出错的。\r\n更多细节请参考 <a href="struct.Handle.html#method.block_on" title="method tokio::runtime::Handle::block_on"><code>Handle::block_on</code></a> 的文档。</p>')),

    (b('<p>Runs the provided function on an executor dedicated to blocking operations.</p>'),
     b('<p>在专用于阻塞操作的执行器上运行提供的函数。</p>')),

    (b('<p>Runs a future to completion on the Tokio runtime. This is the\r\nruntime’s entry point.</p>'),
     b('<p>在 Tokio 运行时上运行一个 future 直到完成。这是运行时的入口点。</p>')),

    (b('<p>This runs the given future on the current thread, blocking until it is\r\ncomplete, and yielding its resolved result. Any tasks or timers\r\nwhich the future spawns internally will be executed on the runtime.</p>'),
     b('<p>此方法在当前线程上运行给定的 future，阻塞直到其完成，并产出其解析后的结果。future 在内部派生的任何任务或定时器都将在运行时上执行。</p>')),

    (b('<p>Note that the future required by this function does not run as a\r\nworker. The expectation is that other tasks are spawned by the future here.\r\nAwaiting on other futures from the future provided here will not\r\nperform as fast as those spawned as workers.</p>'),
     b('<p>请注意，此函数所需的 future 不会作为 worker 运行。这里的预期是 future 内部会派生其他任务。在提供的 future 中 await 其他 future，其性能不会像作为 worker 派生的任务那样快。</p>')),

    (b('<p>When the multi thread scheduler is used this will allow futures\r\nto run within the io driver and timer context of the overall runtime.</p>'),
     b('<p>使用多线程调度器时，future 可以在整体运行时的 io driver 和 timer 上下文中运行。</p>')),

    (b('<p>Any spawned tasks will continue running after <code>block_on</code> returns'),
     b('<p>任何已派生的任务将在 <code>block_on</code> 返回后继续运行')),

    (b('<p>Enters the runtime context.</p>'),
     b('<p>进入运行时上下文。</p>')),

    (b('<p>This allows you to construct types that must have an executor\r\navailable on creation such as <a href="../time/struct.Sleep.html" title="struct tokio::time::Sleep"><code>Sleep</code></a> or <a href="../net/struct.TcpStream.html" title="struct tokio::net::TcpStream"><code>TcpStream</code></a>. It will\r\nalso allow you to call methods such as <a href="../task/fn.spawn.html" title="fn tokio::task::spawn"><code>tokio::spawn</code></a>.</p>'),
     b('<p>这允许你构造创建时必须有可用执行器的类型，例如 <a href="../time/struct.Sleep.html" title="struct tokio::time::Sleep"><code>Sleep</code></a> 或 <a href="../net/struct.TcpStream.html" title="struct tokio::net::TcpStream"><code>TcpStream</code></a>。它还允许你调用 <a href="../task/fn.spawn.html" title="fn tokio::task::spawn"><code>tokio::spawn</code></a> 等方法。</p>')),

    (b('<p>Shuts down the runtime, waiting for at most <code>duration</code> for all spawned\r\nwork to stop.</p>'),
     b('<p>关闭运行时，最多等待 <code>duration</code> 时间让所有已派生的工作停止。</p>')),

    (b('<p>Shuts down the runtime, without waiting for any spawned work to stop.</p>'),
     b('<p>关闭运行时，不等待任何已派生的工作停止。</p>')),

    (b('<p>This can be useful if you want to drop a runtime from within another runtime.\r\nNormally, dropping a runtime will block indefinitely for spawned blocking tasks\r\nto complete, which would normally not be permitted within an asynchronous context.\r\nBy calling <code>shutdown_background()</code>, you can drop the runtime from such a context.</p>'),
     b('<p>如果你希望从另一个运行时内部 drop 一个运行时，这非常有用。通常情况下，drop 一个运行时会无限期阻塞，直到已派生的阻塞任务完成，这在异步上下文中通常是不允许的。调用 <code>shutdown_background()</code> 可以从此类上下文中 drop 该运行时。</p>')),

    (b('<p>Note however, that because we do not wait for any blocking tasks to complete, this\r\nmay result in a resource leak (in that any blocking tasks are still running until they\r\nreturn.</p>'),
     b('<p>但请注意，由于我们不会等待任何阻塞任务完成，这可能导致资源泄漏（任何阻塞任务仍在运行，直到它们返回）。</p>')),

    (b('<p>This function is equivalent to calling <code>shutdown_timeout(Duration::from_nanos(0))</code>.</p>'),
     b('<p>此函数等效于调用 <code>shutdown_timeout(Duration::from_nanos(0))</code>。</p>')),

    # ========== struct.LocalRuntime.html ==========
    (b('<p>A local Tokio runtime.</p>'),
     b('<p>一个本地 Tokio 运行时。</p>')),

    (b('<p>This runtime is capable of driving tasks which are not <code>Send + Sync</code> without the use of a\r\n<code>LocalSet</code>, and thus supports <code>spawn_local</code> without the need for a <code>LocalSet</code> context.</p>'),
     b('<p>此运行时能够驱动那些不是 <code>Send + Sync</code> 的任务，无需使用 <code>LocalSet</code>，因此支持 <code>spawn_local</code> 而不需要 <code>LocalSet</code> 上下文。</p>')),

    (b('<p>This runtime cannot be moved between threads or driven from different threads.</p>'),
     b('<p>此运行时不能在不同的线程之间移动，也不能由不同的线程驱动。</p>')),

    (b('<p>This runtime is incompatible with <code>LocalSet</code>. You should not attempt to drive a <code>LocalSet</code> within a\r\n<code>LocalRuntime</code>.</p>'),
     b('<p>此运行时与 <code>LocalSet</code> 不兼容。你不应尝试在 <code>LocalRuntime</code> 内驱动 <code>LocalSet</code>。</p>')),

    (b('<p>Currently, this runtime supports one flavor, which is internally identical to <code>current_thread</code>,\r\nsave for the aforementioned differences related to <code>spawn_local</code>.</p>'),
     b('<p>目前，此运行时支持一种类型风格，其内部与 <code>current_thread</code> 相同，除了上述与 <code>spawn_local</code> 相关的差异。</p>')),

    (b('<p>For more general information on how to use runtimes, see the <a href="index.html" title="mod tokio::runtime">module</a> docs.</p>'),
     b('<p>有关如何使用运行时的更多常规信息，请参阅<a href="index.html" title="mod tokio::runtime">模块</a>文档。</p>')),

    (b('<p>Creates a new local runtime instance with default configuration values.</p>'),
     b('<p>使用默认配置值创建一个新的本地运行时实例。</p>')),

    (b('<p>This results in the scheduler, I/O driver, and time driver being\r\ninitialized.</p>'),
     b('<p>这将初始化调度器、I/O driver 和 time driver。</p>')),

    (b('<p>When a more complex configuration is necessary, the <a href="struct.Builder.html" title="struct tokio::runtime::Builder">runtime builder</a> may be used.</p>'),
     b('<p>当需要更复杂的配置时，可以使用<a href="struct.Builder.html" title="struct tokio::runtime::Builder">运行时 builder</a>。</p>')),

    (b('<p>See <a href="index.html" title="mod tokio::runtime">module level</a> documentation for more details.</p>'),
     b('<p>更多详细信息请参见<a href="index.html" title="mod tokio::runtime">模块级</a>文档。</p>')),

    (b('<p>Creating a new <code>LocalRuntime</code> with default configuration values.</p>'),
     b('<p>使用默认配置值创建一个新的 <code>LocalRuntime</code>。</p>')),

    (b('<p>As the handle can be sent to other threads, it can only be used to spawn tasks that are <code>Send</code>.</p>'),
     b('<p>由于句柄可以发送到其他线程，它只能用于派生 <code>Send</code> 的任务。</p>')),

    (b('<p>Calling <a href="struct.Handle.html#method.block_on" title="method tokio::runtime::Handle::block_on"><code>Handle::block_on</code></a> on a handle to a <code>LocalRuntime</code> is error-prone.\r\nRefer to the documentation of <a href="struct.Handle.html#method.block_on" title="method tokio::runtime::Handle::block_on"><code>Handle::block_on</code></a> for more.</p>'),
     b('<p>在 <code>LocalRuntime</code> 的句柄上调用 <a href="struct.Handle.html#method.block_on" title="method tokio::runtime::Handle::block_on"><code>Handle::block_on</code></a> 是容易出错的。\r\n更多细节请参考 <a href="struct.Handle.html#method.block_on" title="method tokio::runtime::Handle::block_on"><code>Handle::block_on</code></a> 的文档。</p>')),

    (b('<p>Spawns a task on the runtime.</p>'),
     b('<p>在运行时上派生一个任务。</p>')),

    (b('<p>This is analogous to the <a href="struct.Runtime.html#method.spawn" title="method tokio::runtime::Runtime::spawn"><code>spawn</code></a> method on the standard <a href="struct.Runtime.html" title="struct tokio::runtime::Runtime"><code>Runtime</code></a>, but works even if the task is not thread-safe.</p>'),
     b('<p>此方法类似于标准 <a href="struct.Runtime.html" title="struct tokio::runtime::Runtime"><code>Runtime</code></a> 上的 <a href="struct.Runtime.html#method.spawn" title="method tokio::runtime::Runtime::spawn"><code>spawn</code></a> 方法，但即使任务不是线程安全的也可以工作。</p>')),

    (b('<p>Runs the provided function on a thread from a dedicated blocking thread pool.</p>'),
     b('<p>在专用阻塞线程池中的某个线程上运行提供的函数。</p>')),

    (b('<p>This function <em>will</em> be run on another thread.</p>'),
     b('<p>此函数<em>将</em>在另一个线程上运行。</p>')),

    (b('<p>See the <a href="struct.Runtime.html#method.spawn_blocking" title="method tokio::runtime::Runtime::spawn_blocking">documentation in the non-local runtime</a> for more\r\ninformation.</p>'),
     b('<p>更多信息请参阅<a href="struct.Runtime.html#method.spawn_blocking" title="method tokio::runtime::Runtime::spawn_blocking">非本地运行时中的文档</a>。</p>')),

    (b('<p>See the documentation for <a href="struct.Runtime.html#method.block_on" title="method tokio::runtime::Runtime::block_on">the equivalent method on Runtime</a>\r\nfor more information.</p>'),
     b('<p>更多信息请参阅 <a href="struct.Runtime.html#method.block_on" title="method tokio::runtime::Runtime::block_on">Runtime 上的等价方法</a> 的文档。</p>')),

    (b('<p>If this is a handle to a <a href="struct.LocalRuntime.html" title="struct tokio::runtime::LocalRuntime"><code>LocalRuntime</code></a>, and this function is being invoked from the same\r\nthread that the runtime was created on, you will also be able to call\r\n<a href="../task/fn.spawn_local.html" title="fn tokio::task::spawn_local"><code>tokio::task::spawn_local</code></a>.</p>'),
     b('<p>如果这是 <a href="struct.LocalRuntime.html" title="struct tokio::runtime::LocalRuntime"><code>LocalRuntime</code></a> 的句柄，并且此函数是从创建该运行时的同一线程上调用的，你还可以调用 <a href="../task/fn.spawn_local.html" title="fn tokio::task::spawn_local"><code>tokio::task::spawn_local</code></a>。</p>')),

    (b('<p>Note that <code>spawn_blocking</code> tasks, and only <code>spawn_blocking</code> tasks, can get left behind if\r\nthe timeout expires.</p>'),
     b('<p>请注意，如果超时到期，则 <code>spawn_blocking</code> 任务（且只有 <code>spawn_blocking</code> 任务）可能会被遗留。</p>')),

    (b('<p>Normally, dropping a runtime will block indefinitely for spawned blocking tasks\r\nto complete, which would normally not be permitted within an asynchronous context.\r\nBy calling <code>shutdown_background()</code>, you can drop the runtime from such a context.</p>'),
     b('<p>通常情况下，drop 一个运行时会无限期阻塞，直到已派生的阻塞任务完成，这在异步上下文中通常是不允许的。调用 <code>shutdown_background()</code> 可以从此类上下文中 drop 该运行时。</p>')),

    (b('<p>Note however, that because we do not wait for any blocking tasks to complete, this\r\nmay result in a resource leak (in that any blocking tasks are still running until they\r\nreturn. No other tasks will leak.</p>'),
     b('<p>但请注意，由于我们不会等待任何阻塞任务完成，这可能导致资源泄漏（任何阻塞任务仍在运行，直到它们返回。不会有其他任务泄漏。</p>')),

    # ========== struct.RuntimeMetrics.html ==========
    (b('<p>Handle to the runtime’s metrics.</p>\r\n<p>This handle is internally reference-counted and can be freely cloned. A\r\n<code>RuntimeMetrics</code> handle is obtained using the <a href="struct.Runtime.html#method.metrics" title="method tokio::runtime::Runtime::metrics"><code>Runtime::metrics</code></a> method.</p>'),
     b('<p>运行时 metrics 的句柄。</p>\r\n<p>此句柄内部使用引用计数，可以自由克隆。可以使用 <a href="struct.Runtime.html#method.metrics" title="method tokio::runtime::Runtime::metrics"><code>Runtime::metrics</code></a> 方法获取 <code>RuntimeMetrics</code> 句柄。</p>')),

    (b('<p>Returns the number of worker threads used by the runtime.</p>'),
     b('<p>返回运行时使用的工作线程数。</p>')),

    (b('<p>The number of workers is set by configuring <code>worker_threads</code> on\r\n<code>runtime::Builder</code>. When using the <code>current_thread</code> runtime, the return\r\nvalue is always <code>1</code>.</p>'),
     b('<p>worker 数量通过在 <code>runtime::Builder</code> 上配置 <code>worker_threads</code> 来设置。使用 <code>current_thread</code> 运行时时，返回值始终为 <code>1</code>。</p>')),

    (b('<p>Returns the current number of alive tasks in the runtime.</p>'),
     b('<p>返回运行时中当前存活任务的数量。</p>')),

    (b('<p>This counter increases when a task is spawned and decreases when a\r\ntask exits.</p>'),
     b('<p>派生任务时此计数器会增加，任务退出时则会减少。</p>')),

    (b('<p>Note: When using the multi-threaded runtime this number may not\r\nnot have strong consistency i.e. no tasks may be running but the metric\r\nreports otherwise.</p>'),
     b('<p>注意：在使用多线程运行时时，此数字可能不具有强一致性，即可能没有任务在运行，但 metric 却报告有任务。</p>')),

    (b('<p>Returns the number of tasks currently scheduled in the runtime’s\r\nglobal queue.</p>'),
     b('<p>返回运行时全局队列中当前已调度的任务数。</p>')),

    (b('<p>Tasks that are spawned or notified from a non-runtime thread are\r\nscheduled using the runtime’s global queue. This metric returns the\r\n<strong>current</strong> number of tasks pending in the global queue. As such, the\r\nreturned value may increase or decrease as new tasks are scheduled and\r\nprocessed.</p>'),
     b('<p>从非运行时线程派生或通知的任务使用运行时的全局队列进行调度。此 metric 返回全局队列中待处理任务的<strong>当前</strong>数量。因此，随着新任务被调度和处理，返回值可能增加或减少。</p>')),

    (b('<p>Returns the amount of time the given worker thread has been busy.</p>'),
     b('<p>返回给定工作线程已忙的时间量。</p>')),

    (b('<p>The worker busy duration starts at zero when the runtime is created and\r\nincreases whenever the worker is spending time processing work. Using\r\nthis value can indicate the load of the given worker. If a lot of time\r\nis spent busy, then the worker is under load and will check for inbound\r\nevents less often.</p>'),
     b('<p>worker 忙时计时从运行时创建时的零开始，每当 worker 花费时间处理工作时就会增加。使用此值可以指示给定 worker 的负载。如果大部分时间都处于忙状态，则说明 worker 负载较重，将不那么频繁地检查入站事件。</p>')),

    (b('<p>The timer is monotonically increasing. It is never decremented or reset\r\nto zero.</p>'),
     b('<p>此计时器单调递增，永不递减或重置为零。</p>')),

    (b('<p><code>worker</code> is the index of the worker being queried. The given value must\r\nbe between 0 and <code>num_workers()</code>. The index uniquely identifies a single\r\nworker and will continue to identify the worker throughout the lifetime\r\nof the runtime instance.</p>'),
     b('<p><code>worker</code> 是被查询 worker 的索引。给定值必须介于 0 和 <code>num_workers()</code> 之间。该索引唯一标识一个 worker，并在运行时实例的整个生命周期内持续标识该 worker。</p>')),

    (b('<p>The method panics when <code>worker</code> represents an invalid worker, i.e. is\r\ngreater than or equal to'),
     b('<p>当 <code>worker</code> 表示无效 worker（即大于或等于')),

    (b('<p>Returns the total number of times the given worker thread has parked.</p>'),
     b('<p>返回给定工作线程 park 的总次数。</p>')),

    (b('<p>The worker park count starts at zero when the runtime is created and\r\nincreases by one each time the worker parks the thread waiting for new\r\ninbound events to process. This usually means the worker has processed\r\nall pending work and is currently idle.</p>'),
     b('<p>worker park 计数从运行时创建时的零开始，每当 worker park 线程等待新的入站事件处理时增加一。这通常意味着 worker 已处理完所有待处理工作，当前处于空闲状态。</p>')),

    (b('<p>The counter is monotonically increasing. It is never decremented or\r\nreset to zero.</p>'),
     b('<p>此计数器单调递增，永不递减或重置为零。</p>')),

    (b('<p>Returns the total number of times the given worker thread has parked\r\nand unparked.</p>'),
     b('<p>返回给定工作线程 park 和 unpark 的总次数。</p>')),

    (b('<p>The worker park/unpark count starts at zero when the runtime is created\r\nand increases by one each time the worker parks the thread waiting for\r\nnew inbound events to process. This usually means the worker has processed\r\nall pending work and is currently idle. When new work becomes available,\r\nthe worker is unparked and the park/unpark count is again increased by one.</p>'),
     b('<p>worker park/unpark 计数从运行时创建时的零开始，每当 worker park 线程等待新的入站事件处理时增加一。这通常意味着 worker 已处理完所有待处理工作，当前处于空闲状态。当新工作变得可用时，worker 会被 unpark，park/unpark 计数再次增加一。</p>')),

    (b('<p>An odd count means that the worker is currently parked.\r\nAn even count means that the worker is currently active.</p>'),
     b('<p>奇数表示 worker 当前处于 parked 状态。\r\n偶数表示 worker 当前处于 active 状态。</p>')),

    # ========== struct.Builder.html ==========
    (b('<p>Builds Tokio Runtime with custom configuration values.</p>\r\n<p>Methods can be chained in order to set the configuration values. The\r\nRuntime is constructed by calling <a href="struct.Builder.html#method.build" title="method tokio::runtime::Builder::build"><code>build</code></a>.</p>'),
     b('<p>使用自定义配置值构建 Tokio Runtime。</p>\r\n<p>方法可以链式调用以设置配置值。通过调用 <a href="struct.Builder.html#method.build" title="method tokio::runtime::Builder::build"><code>build</code></a> 来构造 Runtime。</p>')),

    (b('<p>New instances of <code>Builder</code> are obtained via <a href="struct.Builder.html#method.new_multi_thread" title="associated function tokio::runtime::Builder::new_multi_thread"><code>Builder::new_multi_thread</code></a>\r\nor <a href="struct.Builder.html#method.new_current_thread" title="associated function tokio::runtime::Builder::new_current_thread"><code>Builder::new_current_thread</code></a>.</p>'),
     b('<p>通过 <a href="struct.Builder.html#method.new_multi_thread" title="associated function tokio::runtime::Builder::new_multi_thread"><code>Builder::new_multi_thread</code></a> 或 <a href="struct.Builder.html#method.new_current_thread" title="associated function tokio::runtime::Builder::new_current_thread"><code>Builder::new_current_thread</code></a> 获取新的 <code>Builder</code> 实例。</p>')),

    (b('<p>See function level documentation for details on the various configuration\r\nsettings.</p>'),
     b('<p>有关各种配置设置的详细信息，请参阅函数级文档。</p>')),

    (b('<p>Returns a new builder with the current thread scheduler selected.</p>'),
     b('<p>返回一个选定了当前线程调度器的新 builder。</p>')),

    (b('<p>Configuration methods can be chained on the return value.</p>'),
     b('<p>配置方法可以在返回值上链式调用。</p>')),

    (b('<p>To spawn non-<code>Send</code> tasks on the resulting runtime, combine it with a\r\n<a href="../task/struct.LocalSet.html" title="struct tokio::task::LocalSet"><code>LocalSet</code></a>, or call <a href="struct.Builder.html#method.build_local" title="method tokio::runtime::Builder::build_local"><code>build_local</code></a> to create a <a href="struct.LocalRuntime.html" title="struct tokio::runtime::LocalRuntime"><code>LocalRuntime</code></a>.</p>'),
     b('<p>要在生成的运行时上派生非 <code>Send</code> 任务，请将其与 <a href="../task/struct.LocalSet.html" title="struct tokio::task::LocalSet"><code>LocalSet</code></a> 结合使用，或调用 <a href="struct.Builder.html#method.build_local" title="method tokio::runtime::Builder::build_local"><code>build_local</code></a> 创建 <a href="struct.LocalRuntime.html" title="struct tokio::runtime::LocalRuntime"><code>LocalRuntime</code></a>。</p>')),

    (b('<p>Returns a new builder with the multi thread scheduler selected.</p>'),
     b('<p>返回一个选定了多线程调度器的新 builder。</p>')),

    (b('<p>Enables both I/O and time drivers.</p>'),
     b('<p>同时启用 I/O 和 time driver。</p>')),

    (b('<p>Doing this is a shorthand for calling <code>enable_io</code> and <code>enable_time</code>\r\nindividually. If additional components are added to Tokio in the future,\r\n<code>enable_all</code> will include these future components.</p>'),
     b('<p>这是分别调用 <code>enable_io</code> 和 <code>enable_time</code> 的简写。如果将来向 Tokio 添加额外的组件，<code>enable_all</code> 将包含这些未来的组件。</p>')),

    (b('<p>Sets the number of worker threads the <code>Runtime</code> will use.</p>'),
     b('<p>设置 <code>Runtime</code> 将使用的工作线程数。</p>')),

    (b('<p>This can be any number above 0 though it is advised to keep this value\r\non the smaller side.</p>'),
     b('<p>这可以是大于 0 的任何数字，但建议将此值保持在较小的范围内。</p>')),

    (b('<p>This will override the value read from environment variable <code>TOKIO_WORKER_THREADS</code>.</p>'),
     b('<p>这将覆盖从环境变量 <code>TOKIO_WORKER_THREADS</code> 读取的值。</p>')),

    (b('<p>The default value is the number of cores available to the system.</p>'),
     b('<p>默认值是系统可用的核心数。</p>')),

    (b('<p>When using the <code>current_thread</code> runtime this method has no effect.</p>'),
     b('<p>当使用 <code>current_thread</code> 运行时，此方法无效。</p>')),

    (b('<p>Specifies the limit for additional threads spawned by the Runtime.</p>'),
     b('<p>指定 Runtime 派生的额外线程的上限。</p>')),

    (b('<p>These threads are used for blocking operations like tasks spawned\r\nthrough <a href="../task/fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a>, this includes but is not limited to:</p>'),
     b('<p>这些线程用于阻塞操作，例如通过 <a href="../task/fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a> 派生的任务，包括但不限于：</p>')),

    (b('<li><a href="../fs/index.html" title="mod tokio::fs"><code>fs</code></a> operations</li>'),
     b('<li><a href="../fs/index.html" title="mod tokio::fs"><code>fs</code></a> 操作</li>')),

    (b('<li>dns resolution through <a href="../net/trait.ToSocketAddrs.html" title="trait tokio::net::ToSocketAddrs"><code>ToSocketAddrs</code></a></li>'),
     b('<li>通过 <a href="../net/trait.ToSocketAddrs.html" title="trait tokio::net::ToSocketAddrs"><code>ToSocketAddrs</code></a> 进行 DNS 解析</li>')),

    (b('<li>writing to <a href="../io/struct.Stdout.html" title="struct tokio::io::Stdout"><code>Stdout</code></a> or <a href="../io/struct.Stderr.html" title="struct tokio::io::Stderr"><code>Stderr</code></a></li>'),
     b('<li>写入 <a href="../io/struct.Stdout.html" title="struct tokio::io::Stdout"><code>Stdout</code></a> 或 <a href="../io/struct.Stderr.html" title="struct tokio::io::Stderr"><code>Stderr</code></a></li>')),

    (b('<li>reading from <a href="../io/struct.Stdin.html" title="struct tokio::io::Stdin"><code>Stdin</code></a></li>'),
     b('<li>从 <a href="../io/struct.Stdin.html" title="struct tokio::io::Stdin"><code>Stdin</code></a> 读取</li>')),

    (b('<p>Unlike the <a href="struct.Builder.html#method.worker_threads" title="method tokio::runtime::Builder::worker_threads"><code>worker_threads</code></a>, they are not always active and will exit\r\nif left idle for too long. You can change this timeout duration with <a href="struct.Builder.html#method.thread_keep_alive" title="method tokio::runtime::Builder::thread_keep_alive"><code>thread_keep_alive</code></a>.</p>'),
     b('<p>与 <a href="struct.Builder.html#method.worker_threads" title="method tokio::runtime::Builder::worker_threads"><code>worker_threads</code></a> 不同，它们并不总是处于活动状态，如果空闲时间过长就会退出。你可以使用 <a href="struct.Builder.html#method.thread_keep_alive" title="method tokio::runtime::Builder::thread_keep_alive"><code>thread_keep_alive</code></a> 更改此超时时长。</p>')),

    (b('<p>It’s recommended to not set this limit too low in order to avoid hanging on operations\r\nrequiring <a href="../task/fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a>.</p>'),
     b('<p>建议不要将此上限设置得过低，以避免需要 <a href="../task/fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a> 的操作挂起。</p>')),

    (b('<p>The default value is 512.</p>'),
     b('<p>默认值为 512。</p>')),

    (b('<p>When a blocking task is submitted, it will be inserted into a queue. If available, one of\r\nthe idle threads will be notified to run the task. Otherwise, if the threshold set by this\r\nmethod has not been reached, a new thread will be spawned. If no idle thread is available\r\nand no more threads are allowed to be spawned, the task will remain in the queue until one\r\nof the busy threads pick it up. Note that since the queue does not apply any backpressure,\r\nit could potentially grow unbounded.</p>'),
     b('<p>当提交阻塞任务时，它将被插入到队列中。如果有可用的空闲线程，会通知其中一个线程运行该任务。否则，如果尚未达到此方法设置的阈值，则会派生一个新线程。如果没有可用的空闲线程且不允许再派生线程，则该任务将保留在队列中，直到某个繁忙的线程拾取它。请注意，由于队列不应用任何背压，它可能会无限增长。</p>')),

    (b('<p>This will panic if <code>val</code> is not larger than <code>0</code>.</p>'),
     b('<p>如果 <code>val</code> 不大于 <code>0</code>，则会发生 panic。</p>')),

    (b('<p>In old versions <code>max_threads</code> limited both blocking and worker threads, but the\r\ncurrent <code>max_blocking_threads</code> does not include async worker threads in the count.</p>'),
     b('<p>在旧版本中，<code>max_threads</code> 同时限制阻塞线程和 worker 线程，但当前的 <code>max_blocking_threads</code> 不在计数中包含异步 worker 线程。</p>')),

    (b('<p>Sets name of threads spawned by the <code>Runtime</code>’s thread pool.</p>'),
     b('<p>设置由 <code>Runtime</code> 线程池派生的线程的名称。</p>')),

    (b('<p>The default name is “tokio-rt-worker”.</p>'),
     b('<p>默认名称为 "tokio-rt-worker"。</p>')),

    (b('<p>Sets the name of the runtime.</p>'),
     b('<p>设置运行时的名称。</p>')),

    (b('<p>Sets a function used to generate the name of threads spawned by the <code>Runtime</code>’s thread pool.</p>'),
     b('<p>设置用于生成由 <code>Runtime</code> 线程池派生的线程名称的函数。</p>')),

    (b('<p>The default name fn is <code>|| "tokio-rt-worker".into()</code>.</p>'),
     b('<p>默认的名称函数为 <code>|| "tokio-rt-worker".into()</code>。</p>')),

    (b('<p>Sets the stack size (in bytes) for worker threads.</p>'),
     b('<p>设置工作线程的栈大小（以字节为单位）。</p>')),

    (b('<p>The actual stack size may be greater than this value if the platform\r\nspecifies minimal stack size.</p>'),
     b('<p>如果平台指定了最小栈大小，则实际栈大小可能大于此值。</p>')),

    (b('<p>The default stack size for spawned threads is 2 MiB, though this\r\nparticular stack size is subject to change in the future.</p>'),
     b('<p>派生线程的默认栈大小为 2 MiB，但该栈大小将来可能会更改。</p>')),

    (b('<p>Executes function <code>f</code> after each thread is started but before it starts\r\ndoing work.</p>'),
     b('<p>在每个线程启动之后、开始执行工作之前，执行函数 <code>f</code>。</p>')),

    (b('<p>This is intended for bookkeeping and monitoring use cases.</p>'),
     b('<p>此函数用于簿记和监控用途。</p>')),

    (b('<p>Executes function <code>f</code> before each thread stops.</p>'),
     b('<p>在每个线程停止之前执行函数 <code>f</code>。</p>')),

    (b('<p>Executes function <code>f</code> just before a thread is parked (goes idle).\r\n<code>f</code> is called within the Tokio context, so functions like <a href="../task/fn.spawn.html" title="fn tokio::task::spawn"><code>tokio::spawn</code></a>\r\ncan be called, and may result in this thread being unparked immediately.</p>'),
     b('<p>在线程即将 park（变为空闲）之前执行函数 <code>f</code>。<code>f</code> 在 Tokio 上下文内被调用，因此可以调用诸如 <a href="../task/fn.spawn.html" title="fn tokio::task::spawn"><code>tokio::spawn</code></a> 之类的函数，并可能导致此线程立即被 unpark。</p>')),

    (b('<p>This can be used to start work only when the executor is idle, or for bookkeeping\r\nand monitoring purposes.</p>'),
     b('<p>这可用于仅在执行器空闲时启动工作，或用于簿记和监控目的。</p>')),

    (b('<p>Note: There can only be one park callback for a runtime; calling this function\r\nmore than once replaces the last callback defined, rather than adding to it.</p>'),
     b('<p>注意：一个运行时只能有一个 park 回调；多次调用此函数将替换最后定义的回调，而不是添加到其中。</p>')),

    (b('<p>Executes function <code>f</code> just after a thread unparks (starts executing tasks).</p>'),
     b('<p>在线程 unpark（开始执行任务）之后立即执行函数 <code>f</code>。</p>')),

    (b('<p>This is intended for bookkeeping and monitoring use cases; note that work\r\nin this callback will increase latencies when the application has allowed one or\r\nmore runtime threads to go idle.</p>'),
     b('<p>这用于簿记和监控用途；请注意，当应用程序允许一个或多个运行时线程空闲时，此回调中的工作会增加延迟。</p>')),

    (b('<p>Note: There can only be one unpark callback for a runtime; calling this function\r\nmore than once replaces the last callback defined, rather than adding to it.</p>'),
     b('<p>注意：一个运行时只能有一个 unpark 回调；多次调用此函数将替换最后定义的回调，而不是添加到其中。</p>')),

    (b('<p>Creates the configured <code>Runtime</code>.</p>'),
     b('<p>创建已配置的 <code>Runtime</code>。</p>')),

    (b('<p>The returned <code>Runtime</code> instance is ready to spawn tasks.</p>'),
     b('<p>返回的 <code>Runtime</code> 实例已准备好派生任务。</p>')),

    (b('<p>Creates the configured <a href="struct.LocalRuntime.html" title="struct tokio::runtime::LocalRuntime"><code>LocalRuntime</code></a>.</p>'),
     b('<p>创建已配置的 <a href="struct.LocalRuntime.html" title="struct tokio::runtime::LocalRuntime"><code>LocalRuntime</code></a>。</p>')),

    (b('<p>The returned <a href="struct.LocalRuntime.html" title="struct tokio::runtime::LocalRuntime"><code>LocalRuntime</code></a> instance is ready to spawn tasks.</p>'),
     b('<p>返回的 <a href="struct.LocalRuntime.html" title="struct tokio::runtime::LocalRuntime"><code>LocalRuntime</code></a> 实例已准备好派生任务。</p>')),

    (b('<p>This will panic if the runtime is configured with <a href="struct.Builder.html#method.new_multi_thread" title="associated function tokio::runtime::Builder::new_multi_thread"><code>new_multi_thread()</code></a>.</p>'),
     b('<p>如果运行时是通过 <a href="struct.Builder.html#method.new_multi_thread" title="associated function tokio::runtime::Builder::new_multi_thread"><code>new_multi_thread()</code></a> 配置的，则会发生 panic。</p>')),

    (b('<p>Sets a custom timeout for a thread in the blocking pool.</p>'),
     b('<p>为阻塞池中的线程设置自定义超时时间。</p>')),

    (b('<p>By default, the timeout for a thread is set to 10 seconds. This can\r\nbe overridden using <code>.thread_keep_alive()</code>.</p>'),
     b('<p>默认情况下，线程的超时时间设置为 10 秒。可以使用 <code>.thread_keep_alive()</code> 进行覆盖。</p>')),

    (b('<p>Sets the number of scheduler ticks after which the scheduler will poll the global\r\ntask queue.</p>'),
     b('<p>设置调度器在 poll 全局任务队列之前的调度器 tick 数。</p>')),

    (b('<p>A scheduler “tick” roughly corresponds to one <code>poll</code> invocation on a task.</p>'),
     b('<p>一个调度器 "tick" 大致对应于对任务的一次 <code>poll</code> 调用。</p>')),

    (b('<p>By default the global queue interval is 31 for the current-thread scheduler. Please see\r\n<a href="index.html#multi-threaded-runtime-behavior-at-the-time-of-writing" title="mod tokio::runtime">the module documentation</a> for the default behavior of the multi-thread scheduler.</p>'),
     b('<p>对于 current-thread 调度器，默认的全局队列间隔为 31。有关多线程调度器的默认行为，请参阅<a href="index.html#multi-threaded-runtime-behavior-at-the-time-of-writing" title="mod tokio::runtime">模块文档</a>。</p>')),

    (b('<p>Schedulers have a local queue of already-claimed tasks, and a global queue of incoming\r\ntasks. Setting the interval to a smaller value increases the fairness of the scheduler,\r\nat the cost of more synchronization overhead. That can be beneficial for prioritizing\r\ngetting started on new work, especially if tasks frequently yield rather than complete\r\nor await on further I/O. Setting the interval to <code>1</code> will prioritize the global queue and\r\ntasks from the local queue will be executed only if the global queue is empty.\r\nConversely, a higher value prioritizes existing work, and is a good choice when most\r\ntasks quickly complete polling.</p>'),
     b('<p>调度器有一个本地队列用于存放已认领的任务，以及一个全局队列用于存放新到达的任务。将间隔设置为较小的值会提高调度器的公平性，但代价是更多的同步开销。这有利于优先开始新工作，特别是当任务频繁 yield 而不是完成或等待进一步的 I/O 时。将间隔设置为 <code>1</code> 将优先处理全局队列，并且仅在全局队列为空时才会执行本地队列中的任务。相反，较高的值优先处理现有工作，是大多数任务快速完成 poll 时的不错选择。</p>')),

    (b('<p>This function will panic if 0 is passed as an argument.</p>'),
     b('<p>如果传入 0 作为参数，此函数将发生 panic。</p>')),

    (b('<p>Sets the number of scheduler ticks after which the scheduler will poll for\r\nexternal events (timers, I/O, and so on).</p>'),
     b('<p>设置调度器在 poll 外部事件（timer、I/O 等）之前的调度器 tick 数。</p>')),

    (b('<p>By default, the event interval is <code>61</code> for all scheduler types.</p>'),
     b('<p>默认情况下，所有调度器类型的事件间隔为 <code>61</code>。</p>')),

    (b('<p>Setting the event interval determines the effective “priority” of delivering\r\nthese external events (which may wake up additional tasks), compared to\r\nexecuting tasks that are currently ready to run. A smaller value is useful\r\nwhen tasks frequently spend a long time in polling, or infrequently yield,\r\nwhich can result in overly long delays picking up I/O events. Conversely,\r\npicking up new events requires extra synchronization and syscall overhead,\r\nso if tasks generally complete their polling quickly, a higher event interval\r\nwill minimize that overhead while still keeping the scheduler responsive to\r\nevents.</p>'),
     b('<p>设置事件间隔决定了传递这些外部事件（可能会唤醒其他任务）的有效"优先级"，相对于执行当前已准备好运行的任务。当任务频繁长时间 poll 或不频繁 yield 时，较小的值很有用，因为这样可以避免在处理 I/O 事件时产生过长的延迟。相反，拾取新事件需要额外的同步和系统调用开销，因此如果任务通常很快完成 poll，较高的事件间隔可以最大限度地减少该开销，同时仍保持调度器对事件的响应能力。</p>')),

    (b('<p>Enables the I/O driver.</p>'),
     b('<p>启用 I/O driver。</p>')),

    (b('<p>Doing this enables using net, process, signal, and some I/O types on\r\nthe runtime.</p>'),
     b('<p>这将允许在运行时上使用 net、process、signal 以及某些 I/O 类型。</p>')),

    (b('<p>Enables the I/O driver and configures the max number of events to be\r\nprocessed per tick.</p>'),
     b('<p>启用 I/O driver 并配置每个 tick 处理的最大事件数。</p>')),

    (b('<p>Enables the time driver.</p>'),
     b('<p>启用 time driver。</p>')),

    (b('<p>Doing this enables using <code>tokio::time</code> on the runtime.</p>'),
     b('<p>这将允许在运行时上使用 <code>tokio::time</code>。</p>')),

    # ========== Chrome / section header items ==========
    (b('Runtime context guard.'),
     b('运行时上下文守卫。')),

    (b('Handle to the runtime.'),
     b('运行时的句柄。')),

    (b('An opaque ID that uniquely identifies a runtime relative to all other currently'),
     b('一个不透明的 ID，相对于所有其他当前')),

    (b('LocalRuntime-only config options'),
     b('LocalRuntime 专属的配置选项')),

    (b('A local Tokio runtime.'),
     b('一个本地 Tokio 运行时。')),

    (b('The Tokio runtime.'),
     b('Tokio 运行时。')),

    (b('Handle to the runtime’s metrics.'),
     b('运行时 metrics 的句柄。')),

    (b('Error returned by try_current when no Runtime has been started'),
     b('在没有启动 Runtime 时由 try_current 返回的错误')),

    (b('The flavor of a Runtime.'),
     b('Runtime 的类型风格。')),

    (b('Checks whether the given error was emitted by Tokio when shutting down its runtime.'),
     b('检查给定的错误是否由 Tokio 在关闭其运行时时发出。')),

    (b('Builds Tokio Runtime with custom configuration values.'),
     b('使用自定义配置值构建 Tokio Runtime。')),

    (b('Unlike other Rust programs, asynchronous applications require runtime'),
     b('与其他 Rust 程序不同，异步应用需要运行时')),

    (b('Here is the rules of thumb to choose the right runtime for your application.'),
     b('以下是为你的应用选择合适运行时的经验法则。')),

    (b('See https://tokio.rs/tokio/topics/bridging for details.'),
     b('有关详细信息，请参见 https://tokio.rs/tokio/topics/bridging。')),

    (b('The tokio runtime is not NUMA (Non-Uniform Memory Access) aware.'),
     b('tokio 运行时不是 NUMA（非一致性内存访问）感知的。')),

    (b('This section gives more details into how the Tokio runtime will schedule'),
     b('本节详细介绍了 Tokio 运行时将如何调度')),

    (b('However, the above is not sufficient to guarantee a well-behaved runtime.'),
     b('然而，上述并不足以保证运行时表现良好。')),

    (b('If the total number of tasks does not grow without bound, and no task is'),
     b('如果任务总数不会无限制增长，且没有任务')),

    (b('Under the following two assumptions:'),
     b('在以下两个假设下：')),

    (b('Beyond just scheduling tasks, the runtime must also manage IO resources and'),
     b('除了调度任务之外，运行时还必须管理 IO 资源和')),

    (b('These checks are performed periodically between scheduling tasks. Under the'),
     b('这些检查在调度任务之间定期执行。在以下条件下')),

    (b('This section describes how the current thread runtime behaves today. This'),
     b('本节描述了当前线程运行时如今的行为方式。本')),

    (b('When a task is woken from within a task running on the runtime, then the'),
     b('当从运行时上运行的任务内部唤醒一个任务时，则')),

    (b('This section describes how the multi thread runtime behaves today. This'),
     b('本节描述了多线程运行时如今的行为方式。本')),

    (b('A multi thread runtime has a fixed number of worker threads, which are all'),
     b('多线程运行时具有固定数量的工作线程，所有这些工作线程')),

    (b('If both the local queue and global queue is empty, then the worker thread'),
     b('如果本地队列和全局队列都为空，则工作线程')),

    (b('When a task is woken from a thread that is not a worker thread, then the'),
     b('当从不是工作线程的线程唤醒任务时，则')),

    # H2 section headers
    (b('>Bridging with sync code<'),
     b('>与同步代码桥接<')),

    (b('>NUMA awareness<'),
     b('>NUMA 感知<')),

    (b('>Runtime Configurations<'),
     b('>运行时配置<')),

    (b('>Driving the runtime<'),
     b('>驱动运行时<')),

    (b('>Lifetime of spawned threads<'),
     b('>派生线程的生命周期<')),

    (b('>IO and timers<'),
     b('>IO 和定时器<')),

    (b('>Current thread runtime (behavior at the time of writing)<'),
     b('>当前线程运行时（撰写时的行为）<')),

    (b('>Multi threaded runtime (behavior at the time of writing)<'),
     b('>多线程运行时（撰写时的行为）<')),

    (b('>File descriptor table pre-warming<'),
     b('>文件描述符表预热<')),

    # Variants non-exhaustive chrome
    (b('Variants (Non-exhaustive)§'),
     b('变体（非穷尽）§')),

    # Section labels (h3 / h4 etc)
    (b('>Methods<'),
     b('>方法<')),

    # See struct level documentation
    (b('<p>See the <a href="struct.Runtime.html#shutdown" title="struct tokio::runtime::Runtime">struct level documentation</a> for more details.</p>'),
     b('<p>更多详细信息请参见 <a href="struct.Runtime.html#shutdown" title="struct tokio::runtime::Runtime">结构体级文档</a>。</p>')),

    (b('<p>See the <a href="struct.LocalRuntime.html#shutdown" title="struct tokio::runtime::LocalRuntime">struct level documentation</a> for more details.</p>'),
     b('<p>更多详细信息请参见 <a href="struct.LocalRuntime.html#shutdown" title="struct tokio::runtime::LocalRuntime">结构体级文档</a>。</p>')),

    # ========== Remaining untranslated items ==========

    # struct.Builder.html method.name - panic
    (b('<p>This function will panic if an empty value is passed as an argument.</p>'),
     b('<p>如果传入空字符串作为参数，此函数将发生 panic。</p>')),

    # struct.Handle.html method.enter - Do not do the following
    (b('<p>Do <strong>not</strong> do the following, this shows a scenario that will result in a\npanic and possible memory leak.</p>'),
     b('<p><strong>不要</strong>执行以下操作，这展示了一种会导致 panic 和可能的内存泄漏的场景。</p>')),

    # struct.Handle.html method.block_on - If the runtime has been shut down
    (b('<p>If the <code>Handle</code>’s associated <code>Runtime</code> has been shut down (through\n<a href="struct.Runtime.html#method.shutdown_background" title="method tokio::runtime::Runtime::shutdown_background"><code>Runtime::shutdown_background</code></a>, <a href="struct.Runtime.html#method.shutdown_timeout" title="method tokio::runtime::Runtime::shutdown_timeout"><code>Runtime::shutdown_timeout</code></a>, or by\ndropping it) and <code>Handle::block_on</code> is used it might return an error or\npanic. Specifically IO resources will return an error and timers will\npanic. Runtime independent futures will run as normal.</p>'),
     b('<p>如果该 <code>Handle</code> 所关联的 <code>Runtime</code> 已经被关闭（通过 <a href="struct.Runtime.html#method.shutdown_background" title="method tokio::runtime::Runtime::shutdown_background"><code>Runtime::shutdown_background</code></a>、<a href="struct.Runtime.html#method.shutdown_timeout" title="method tokio::runtime::Runtime::shutdown_timeout"><code>Runtime::shutdown_timeout</code></a> 或 drop 它），并且使用了 <code>Handle::block_on</code>，它可能会返回错误或发生 panic。具体而言，IO 资源将返回错误，timer 将 panic。运行时无关的 future 将正常运行。</p>')),

    # struct.Handle.html method.block_on - This function will panic
    (b('<p>This function will panic if any of the following conditions are met:</p>'),
     b('<p>如果满足以下任何条件，此函数将发生 panic：</p>')),

    # struct.Handle.html method.block_on - Handle::block_on may be combined with task::block_in_place
    (b('<p><code>Handle::block_on</code> may be combined with <a href="../task/fn.block_in_place.html" title="fn tokio::task::block_in_place"><code>task::block_in_place</code></a> to\nre-enter the async context of a multi-thread scheduler runtime:</p>'),
     b('<p><code>Handle::block_on</code> 可以与 <a href="../task/fn.block_in_place.html" title="fn tokio::task::block_in_place"><code>task::block_in_place</code></a> 结合使用，以重新进入多线程调度器运行时的异步上下文：</p>')),

    # struct.Runtime.html method.block_on - When the current thread scheduler is enabled
    (b('<p>When the current thread scheduler is enabled <code>block_on</code>\ncan be called concurrently from multiple threads. The first call\nwill take ownership of the io and timer drivers. This means\nother threads which do not own the drivers will hook into that one.\nWhen the first <code>block_on</code> completes, other threads will be able to\n“steal” the driver to allow continued execution of their futures.</p>'),
     b('<p>启用 current thread scheduler 时，<code>block_on</code> 可以从多个线程并发调用。第一次调用将获得 io 和 timer driver 的所有权。这意味着不拥有 driver 的其他线程将挂接到该 driver 上。当第一次 <code>block_on</code> 完成时，其他线程将能够"窃取"该 driver 以允许它们的 future 继续执行。</p>')),

    # struct.Runtime.html method.block_on - Any spawned tasks will be suspended
    (b('<p>Any spawned tasks will be suspended after <code>block_on</code> returns. Calling\n<code>block_on</code> again will resume previously spawned tasks.</p>'),
     b('<p>任何已派生的任务将在 <code>block_on</code> 返回后挂起。再次调用 <code>block_on</code> 将恢复之前已派生的任务。</p>')),

    # struct.Runtime.html method.block_on - This function panics
    (b('<p>This function panics if the provided future panics, or if called within an\nasynchronous execution context.</p>'),
     b('<p>如果提供的 future 发生 panic，或在异步执行上下文中调用，则此函数将 panic。</p>')),

    # stdlib trait method docblocks (from From<T>/Into<T> impls)
    (b('<p>Returns the argument unchanged.</p>'),
     b('<p>原样返回参数。</p>')),

    (b('<p>Calls <code>U::from(self)</code>.</p>\n<p>That is, this conversion is whatever the implementation of\n<code><a href="https://doc.rust-lang.org/1.95.0/core/convert/trait.From.html" title="trait core::convert::From">From</a>&lt;T&gt; for U</code> chooses to do.</p>'),
     b('<p>调用 <code>U::from(self)</code>。</p>\n<p>也就是说，此转换由 <code><a href="https://doc.rust-lang.org/1.95.0/core/convert/trait.From.html" title="trait core::convert::From">From</a>&lt;T&gt; for U</code> 的实现来决定。</p>')),

    # struct.Handle.html method.block_on - Or using Handle::current
    (b('<p>Or using <code>Handle::current</code>:</p>'),
     b('<p>或者使用 <code>Handle::current</code>：</p>')),
]


def main():
    target_files = [
        'tokio/runtime/index.html',
        'tokio/runtime/enum.RuntimeFlavor.html',
        'tokio/runtime/fn.is_rt_shutdown_err.html',
        'tokio/runtime/struct.Builder.html',
        'tokio/runtime/struct.Handle.html',
        'tokio/runtime/struct.Runtime.html',
        'tokio/runtime/struct.EnterGuard.html',
        'tokio/runtime/struct.Id.html',
        'tokio/runtime/struct.LocalOptions.html',
        'tokio/runtime/struct.LocalRuntime.html',
        'tokio/runtime/struct.RuntimeMetrics.html',
        'tokio/runtime/struct.TryCurrentError.html',
    ]

    grand_total = 0
    file_count = 0
    for fp in target_files:
        if not os.path.exists(fp):
            print(f'SKIP (missing): {fp}')
            continue
        with open(fp, 'rb') as f:
            content = f.read()
        original = content
        count = 0
        for en, zh in PAIRS:
            if en in content:
                n = content.count(en)
                content = content.replace(en, zh)
                count += n
        if content != original:
            with open(fp, 'wb') as f:
                f.write(content)
            print(f'{fp}: {count} replacements')
            grand_total += count
            file_count += 1
        else:
            print(f'{fp}: 0 replacements (no match)')
    print(f'\nTOTAL: {grand_total} replacements across {file_count} files')


if __name__ == '__main__':
    main()