"""Translate tokio::runtime::Builder struct HTML to Chinese.

Workflow per rust-doc-translation-pattern:
- Use Python open() directly (no Read tool).
- Apply (old, new) replacements in long-string-first order.
- Preserve HTML structure, URLs, Rust identifiers, <wbr>, code blocks.
"""

import os
import re

RUNTIME_ROOT = 'D:/Administrator/Documents/Code/rust_doc_all/tokio/runtime'


def verify(content, label):
    """Verify a translated HTML file: tag balance, line-number pollution, CJK density."""
    line_artifacts = re.findall(r'^\d+\t', content, flags=re.MULTILINE)
    if line_artifacts:
        print(f'  [WARN] {label}: {len(line_artifacts)} lines with cat-n style line numbers')

    cjk = re.findall(r'[一-鿿]', content)
    print(f'  [INFO] {label}: {len(cjk)} CJK characters')

    tag_pairs = ['html', 'head', 'body', 'main', 'section', 'div', 'p',
                 'a', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                 'ul', 'li', 'code', 'pre', 'details', 'summary',
                 'dl', 'dt', 'dd']
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
    # Buttons
    ('>Copy item path<', '>复制项目路径<'),
    ('>Source<', '>源代码<'),
    ('>Expand description<', '>展开描述<'),
    # Skip link
    ('>Skip to main content<', '>跳到主要内容<'),
    # IE warning
    ('This old browser is unsupported and will most likely display funky things.',
     '此旧版浏览器不受支持，很可能会显示异常内容。'),
    # Doc anchor section titles (sidebar)
    ('title="Examples"', 'title="示例"'),
    ('title="Methods"', 'title="方法"'),
    ('title="Trait Implementations"', 'title="trait 实现"'),
    # Sidebar / topbar titles (none of these are in this struct file; topbar is just "Builder")
    # H1 heading: keep the span Builder
    ('>Struct <span class="struct">Builder</span>',
     '>结构体 <span class="struct">Builder</span>'),
    # Misc title attrs
    ('title="Copy item path to clipboard"', 'title="复制项目路径到剪贴板"'),
    ('title="Drag to resize sidebar"', 'title="拖动以调整侧边栏宽度"'),
    # Section H2 visible headings
    ('<h2 id="implementations" class="section-header">Implementations',
     '<h2 id="implementations" class="section-header">实现'),
    ('<h2 id="synthetic-implementations" class="section-header">Auto Trait Implementations',
     '<h2 id="synthetic-implementations" class="section-header">自动 trait 实现'),
    ('<h2 id="blanket-implementations" class="section-header">Blanket Implementations',
     '<h2 id="blanket-implementations" class="section-header">blanket 实现'),
    # Inner section header H3s (sidebar anchors)
    ('>Auto Trait Implementations<', '>自动 trait 实现<'),
    ('>Blanket Implementations<', '>blanket 实现<'),
    ('>Implementations<', '>实现<'),
    ('>Methods<', '>方法<'),
    ('>Trait Implementations<', '>trait 实现<'),
    # Inside-doc h5 / h6 sub-headers
    ('>Default<', '>默认值<'),
    ('>Examples<', '>示例<'),
    ('>Panics<', '>恐慌<'),
    ('>Queue Behavior<', '>队列行为<'),
    ('>Upgrading from 0.x<', '>从 0.x 升级<'),
    ('>Example<', '>示例<'),
    # Sidebar Crate Items section title
    ('title="Re-exports"', 'title="重新导出"'),
    ('title="Modules"', 'title="模块"'),
    ('title="Macros"', 'title="宏"'),
    ('title="Structs"', 'title="结构体"'),
    ('title="Enums"', 'title="枚举"'),
    ('title="Constants"', 'title="常量"'),
    ('title="Traits"', 'title="trait"'),
    ('title="Functions"', 'title="函数"'),
    ('title="Type Aliases"', 'title="类型别名"'),
    # Method title attrs (sidebar)
    ('title="struct tokio::runtime::Builder"', 'title="结构体 tokio::runtime::Builder"'),
]


# ============================================================================
# Docblock content pairs
# ============================================================================
DOCBLOCK_PAIRS = [
    # ----- Main struct docblock -----
    ('<p>Builds Tokio Runtime with custom configuration values.</p>',
     '<p>使用自定义配置值构建 Tokio 运行时。</p>'),
    ('<p>Methods can be chained in order to set the configuration values. The\nRuntime is constructed by calling <a href="struct.Builder.html#method.build" title="method tokio::runtime::Builder::build"><code>build</code></a>.</p>',
     '<p>可以按链式调用各方法来设置配置值。运行时通过调用 <a href="struct.Builder.html#method.build" title="method tokio::runtime::Builder::build"><code>build</code></a> 来构造。</p>'),
    ('<p>New instances of <code>Builder</code> are obtained via <a href="method@Self::new_multi_thread"><code>Builder::new_multi_thread</code></a>\nor <a href="struct.Builder.html#method.new_current_thread" title="associated function tokio::runtime::Builder::new_current_thread"><code>Builder::new_current_thread</code></a>.</p>',
     '<p>通过 <a href="method@Self::new_multi_thread"><code>Builder::new_multi_thread</code></a>\n或 <a href="struct.Builder.html#method.new_current_thread" title="associated function tokio::runtime::Builder::new_current_thread"><code>Builder::new_current_thread</code></a> 获取 <code>Builder</code> 的新实例。</p>'),
    ('<p>See function level documentation for details on the various configuration\nsettings.</p>',
     '<p>有关各种配置选项的详细信息，请参阅函数级文档。</p>'),
    # main example
    ('<span class="comment">// build runtime\n    </span>',
     '<span class="comment">// 构建运行时\n    </span>'),
    ('<span class="comment">// use runtime ...\n</span>',
     '<span class="comment">// 使用运行时 ...\n</span>'),

    # ----- new_current_thread -----
    ('<p>Returns a new builder with the current thread scheduler selected.</p>',
     '<p>返回一个选择了当前线程调度器的新构建器。</p>'),
    ('<p>Configuration methods can be chained on the return value.</p>',
     '<p>可以在返回值上链式调用各配置方法。</p>'),
    ('<p>To spawn non-<code>Send</code> tasks on the resulting runtime, combine it with a\n<a href="../task/struct.LocalSet.html" title="struct tokio::task::LocalSet"><code>LocalSet</code></a>, or call <a href="struct.Builder.html#method.build_local" title="method tokio::runtime::Builder::build_local"><code>build_local</code></a> to create a <a href="struct.LocalRuntime.html" title="struct tokio::runtime::LocalRuntime"><code>LocalRuntime</code></a>.</p>',
     '<p>要在所得到的运行时上派生非 <code>Send</code> 任务，需要将其与 <a href="../task/struct.LocalSet.html" title="struct tokio::task::LocalSet"><code>LocalSet</code></a> 组合使用，或者调用 <a href="struct.Builder.html#method.build_local" title="method tokio::runtime::Builder::build_local"><code>build_local</code></a> 来创建 <a href="struct.LocalRuntime.html" title="struct tokio::runtime::LocalRuntime"><code>LocalRuntime</code></a>。</p>'),

    # ----- enable_all -----
    ('<p>Enables both I/O and time drivers.</p>',
     '<p>同时启用 I/O 和时间驱动。</p>'),
    ('<p>Doing this is a shorthand for calling <code>enable_io</code> and <code>enable_time</code>\nindividually. If additional components are added to Tokio in the future,\n<code>enable_all</code> will include these future components.</p>',
     '<p>这是单独调用 <code>enable_io</code> 和 <code>enable_time</code> 的简写。如果未来 Tokio 中添加了其他组件，\n<code>enable_all</code> 也会包括这些未来的组件。</p>'),

    # ----- worker_threads -----
    ('<p>Sets the number of worker threads the <code>Runtime</code> will use.</p>',
     '<p>设置 <code>Runtime</code> 将使用的工作线程数。</p>'),
    ('<p>This can be any number above 0 though it is advised to keep this value\non the smaller side.</p>',
     '<p>该值可以是大于 0 的任何数字，不过建议保持一个较小的值。</p>'),
    ('<p>This will override the value read from environment variable <code>TOKIO_WORKER_THREADS</code>.</p>',
     '<p>这会覆盖从环境变量 <code>TOKIO_WORKER_THREADS</code> 读取的值。</p>'),
    ('<p>The default value is the number of cores available to the system.</p>',
     '<p>默认值是系统可用的 CPU 核心数。</p>'),
    ('<p>When using the <code>current_thread</code> runtime this method has no effect.</p>',
     '<p>使用 <code>current_thread</code> 运行时，此方法无效。</p>'),
    # H6 sub-headings
    ('>Multi threaded runtime with 4 threads<', '>具有 4 个线程的多线程运行时<'),
    ('>Current thread runtime (will only run on the current thread via <code>Runtime::block_on</code>)<',
     '>当前线程运行时（仅通过 <code>Runtime::block_on</code> 在当前线程上运行）<'),
    # worker_threads example comments
    ('<span class="comment">// This will spawn a work-stealing runtime with 4 worker threads.\n</span>',
     '<span class="comment">// 这将派生一个具有 4 个工作线程的工作窃取型运行时。\n</span>'),
    ('<span class="comment">// Create a runtime that _must_ be driven from a call\n// to `Runtime::block_on`.\n</span>',
     '<span class="comment">// 创建一个必须通过调用\n// `Runtime::block_on` 来驱动的运行时。\n</span>'),
    ('<span class="comment">// This will run the runtime and future on the current thread\n</span>',
     '<span class="comment">// 这将在当前线程上运行运行时和 future\n</span>'),
    ('<p>This will panic if <code>val</code> is not larger than <code>0</code>.</p>',
     '<p>如果 <code>val</code> 不大于 <code>0</code>，则会发生 panic。</p>'),

    # ----- max_blocking_threads -----
    ('<p>Specifies the limit for additional threads spawned by the Runtime.</p>',
     '<p>指定运行时派生的额外线程的上限。</p>'),
    ('<p>These threads are used for blocking operations like tasks spawned\nthrough <a href="../task/fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a>, this includes but is not limited to:</p>',
     '<p>这些线程用于阻塞操作，例如通过 <a href="../task/fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a> 派生的任务，包括但不限于：</p>'),
    ('<li><a href="mod@crate::fs"><code>fs</code></a> operations</li>',
     '<li><a href="mod@crate::fs"><code>fs</code></a> 操作</li>'),
    ('<li>dns resolution through <a href="../net/trait.ToSocketAddrs.html" title="trait tokio::net::ToSocketAddrs"><code>ToSocketAddrs</code></a></li>',
     '<li>通过 <a href="../net/trait.ToSocketAddrs.html" title="trait tokio::net::ToSocketAddrs"><code>ToSocketAddrs</code></a> 进行 DNS 解析</li>'),
    ('<li>writing to <a href="struct@crate::io::Stdout"><code>Stdout</code></a> or <a href="struct@crate::io::Stderr"><code>Stderr</code></a></li>',
     '<li>写入 <a href="struct@crate::io::Stdout"><code>Stdout</code></a> 或 <a href="struct@crate::io::Stderr"><code>Stderr</code></a></li>'),
    ('<li>reading from <a href="struct@crate::io::Stdin"><code>Stdin</code></a></li>',
     '<li>从 <a href="struct@crate::io::Stdin"><code>Stdin</code></a> 读取</li>'),
    ('<p>Unlike the <a href="struct.Builder.html#method.worker_threads" title="method tokio::runtime::Builder::worker_threads"><code>worker_threads</code></a>, they are not always active and will exit\nif left idle for too long. You can change this timeout duration with <a href="struct.Builder.html#method.thread_keep_alive" title="method tokio::runtime::Builder::thread_keep_alive"><code>thread_keep_alive</code></a>.</p>',
     '<p>与 <a href="struct.Builder.html#method.worker_threads" title="method tokio::runtime::Builder::worker_threads"><code>worker_threads</code></a> 不同，这些线程并非始终处于活动状态，\n如果空闲时间过长会退出。可以使用 <a href="struct.Builder.html#method.thread_keep_alive" title="method tokio::runtime::Builder::thread_keep_alive"><code>thread_keep_alive</code></a> 更改该超时时长。</p>'),
    ('<p>It’s recommended to not set this limit too low in order to avoid hanging on operations\nrequiring <a href="../task/fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a>.</p>',
     '<p>建议不要将该上限设置得过低，以避免在需要 <a href="../task/fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a> 的操作上发生挂起。</p>'),
    ('<p>The default value is 512.</p>',
     '<p>默认值是 512。</p>'),
    ('<p>When a blocking task is submitted, it will be inserted into a queue. If available, one of\nthe idle threads will be notified to run the task. Otherwise, if the threshold set by this\nmethod has not been reached, a new thread will be spawned. If no idle thread is available\nand no more threads are allowed to be spawned, the task will remain in the queue until one\nof the busy threads pick it up. Note that since the queue does not apply any backpressure,\nit could potentially grow unbounded.</p>',
     '<p>当提交一个阻塞任务时，它会被插入一个队列中。如果有空闲线程，则会通知其中一个线程来运行该任务。否则，\n如果尚未达到本方法设置的阈值，则会派生一个新的线程。如果没有可用的空闲线程，并且也不再允许派生新线程，\n那么该任务将一直留在队列中，直到某个繁忙的线程将其取出。需要注意的是，由于队列不施加任何背压，\n因此它可能会无限增长。</p>'),
    ('<p>In old versions <code>max_threads</code> limited both blocking and worker threads, but the\ncurrent <code>max_blocking_threads</code> does not include async worker threads in the count.</p>',
     '<p>在旧版本中，<code>max_threads</code> 同时限制阻塞线程和工作线程的数量，\n但当前的 <code>max_blocking_threads</code> 不再将异步工作线程计入该数量中。</p>'),

    # ----- thread_name -----
    ('<p>Sets name of threads spawned by the <code>Runtime</code>’s thread pool.</p>',
     '<p>设置 <code>Runtime</code> 线程池所派生线程的名称。</p>'),
    ('<p>The default name is “tokio-rt-worker”.</p>',
     '<p>默认名称为 “tokio-rt-worker”。</p>'),

    # ----- name -----
    ('<p>Sets the name of the runtime.</p>',
     '<p>设置运行时的名称。</p>'),
    ('<p>This function will panic if an empty value is passed as an argument.</p>',
     '<p>如果将空值作为参数传入，此函数将发生 panic。</p>'),

    # ----- thread_name_fn -----
    ('<p>Sets a function used to generate the name of threads spawned by the <code>Runtime</code>’s thread pool.</p>',
     '<p>设置一个用于生成 <code>Runtime</code> 线程池所派生线程名称的函数。</p>'),
    ('<p>The default name fn is <code>|| "tokio-rt-worker".into()</code>.</p>',
     '<p>默认的名称函数是 <code>|| "tokio-rt-worker".into()</code>。</p>'),

    # ----- thread_stack_size -----
    ('<p>Sets the stack size (in bytes) for worker threads.</p>',
     '<p>设置工作线程的栈大小（以字节为单位）。</p>'),
    ('<p>The actual stack size may be greater than this value if the platform\nspecifies minimal stack size.</p>',
     '<p>如果平台指定了最小栈大小，实际的栈大小可能大于此值。</p>'),
    ('<p>The default stack size for spawned threads is 2 MiB, though this\nparticular stack size is subject to change in the future.</p>',
     '<p>所派生线程的默认栈大小为 2 MiB，但此特定的栈大小将来可能会发生变化。</p>'),

    # ----- on_thread_start -----
    ('<p>Executes function <code>f</code> after each thread is started but before it starts\ndoing work.</p>',
     '<p>在每个线程启动之后、开始工作之前执行函数 <code>f</code>。</p>'),
    ('<p>This is intended for bookkeeping and monitoring use cases.</p>',
     '<p>此回调用于簿记和监控场景。</p>'),
    ('<span class="macro">println!</span>(<span class="string">"thread started"</span>);',
     '<span class="macro">println!</span>(<span class="string">"thread started"</span>);'),  # keep code string in examples, only the comment would be translated

    # ----- on_thread_stop -----
    ('<p>Executes function <code>f</code> before each thread stops.</p>',
     '<p>在每个线程停止之前执行函数 <code>f</code>。</p>'),
    ('<span class="macro">println!</span>(<span class="string">"thread stopping"</span>);',
     '<span class="macro">println!</span>(<span class="string">"thread stopping"</span>);'),  # code string preserved

    # ----- on_thread_park -----
    ('<p>Executes function <code>f</code> just before a thread is parked (goes idle).\n<code>f</code> is called within the Tokio context, so functions like <a href="../task/fn.spawn.html" title="fn tokio::task::spawn"><code>tokio::spawn</code></a>\ncan be called, and may result in this thread being unparked immediately.</p>',
     '<p>在线程即将被 park（变为空闲）之前执行函数 <code>f</code>。\n<code>f</code> 在 Tokio 上下文中被调用，因此可以调用 <a href="../task/fn.spawn.html" title="fn tokio::task::spawn"><code>tokio::spawn</code></a>\n等函数，这可能会导致该线程被立即 unpark。</p>'),
    ('<p>This can be used to start work only when the executor is idle, or for bookkeeping\nand monitoring purposes.</p>',
     '<p>可以用于仅在执行器空闲时启动工作，或用于簿记和监控目的。</p>'),
    ('<p>Note: There can only be one park callback for a runtime; calling this function\nmore than once replaces the last callback defined, rather than adding to it.</p>',
     '<p>注意：每个运行时只能有一个 park 回调；多次调用此函数将替换最后定义的回调，\n而不是叠加。</p>'),
    ('>Multithreaded executor<', '>多线程执行器<'),
    ('>Current thread executor<', '>当前线程执行器<'),

    # ----- on_thread_unpark -----
    ('<p>Executes function <code>f</code> just after a thread unparks (starts executing tasks).</p>',
     '<p>在线程 unpark（开始执行任务）之后立即执行函数 <code>f</code>。</p>'),
    ('<p>This is intended for bookkeeping and monitoring use cases; note that work\nin this callback will increase latencies when the application has allowed one or\nmore runtime threads to go idle.</p>',
     '<p>此回调用于簿记和监控场景；需要注意的是，当应用程序允许一个或多个运行时线程\n进入空闲状态时，此回调中的工作会增加延迟。</p>'),
    ('<p>Note: There can only be one unpark callback for a runtime; calling this function\nmore than once replaces the last callback defined, rather than adding to it.</p>',
     '<p>注意：每个运行时只能有一个 unpark 回调；多次调用此函数将替换最后定义的回调，\n而不是叠加。</p>'),
    ('<span class="macro">println!</span>(<span class="string">"thread unparking"</span>);',
     '<span class="macro">println!</span>(<span class="string">"thread unparking"</span>);'),  # code string preserved
    ('<span class="macro">println!</span>(<span class="string">"Hello from Tokio!"</span>);',
     '<span class="macro">println!</span>(<span class="string">"Hello from Tokio!"</span>);'),  # code string preserved

    # ----- build -----
    ('<p>Creates the configured <code>Runtime</code>.</p>',
     '<p>根据配置创建 <code>Runtime</code>。</p>'),
    ('<p>The returned <code>Runtime</code> instance is ready to spawn tasks.</p>',
     '<p>返回的 <code>Runtime</code> 实例已准备好派生任务。</p>'),
    ('<span class="macro">println!</span>(<span class="string">"Hello from the Tokio runtime"</span>);',
     '<span class="macro">println!</span>(<span class="string">"Hello from the Tokio runtime"</span>);'),  # code string preserved

    # ----- build_local -----
    ('<p>Creates the configured <a href="struct.LocalRuntime.html" title="struct tokio::runtime::LocalRuntime"><code>LocalRuntime</code></a>.</p>',
     '<p>根据配置创建 <a href="struct.LocalRuntime.html" title="struct tokio::runtime::LocalRuntime"><code>LocalRuntime</code></a>。</p>'),
    ('<p>The returned <a href="struct.LocalRuntime.html" title="struct tokio::runtime::LocalRuntime"><code>LocalRuntime</code></a> instance is ready to spawn tasks.</p>',
     '<p>返回的 <a href="struct.LocalRuntime.html" title="struct tokio::runtime::LocalRuntime"><code>LocalRuntime</code></a> 实例已准备好派生任务。</p>'),
    ('<p>This will panic if the runtime is configured with <a href="Builder::new_multi_thread"><code>new_multi_thread()</code></a>.</p>',
     '<p>如果运行时是使用 <a href="Builder::new_multi_thread"><code>new_multi_thread()</code></a> 配置的，则会发生 panic。</p>'),

    # ----- thread_keep_alive -----
    ('<p>Sets a custom timeout for a thread in the blocking pool.</p>',
     '<p>设置阻塞池中线程的自定义超时时间。</p>'),
    ('<p>By default, the timeout for a thread is set to 10 seconds. This can\nbe overridden using <code>.thread_keep_alive()</code>.</p>',
     '<p>默认情况下，线程的超时时间被设置为 10 秒。可以使用 <code>.thread_keep_alive()</code> 覆盖此设置。</p>'),

    # ----- global_queue_interval -----
    ('<p>Sets the number of scheduler ticks after which the scheduler will poll the global\ntask queue.</p>',
     '<p>设置调度器在多少个调度 tick 之后轮询全局任务队列。</p>'),
    ('<p>A scheduler “tick” roughly corresponds to one <code>poll</code> invocation on a task.</p>',
     '<p>一个调度“tick”大致对应于对任务的 <code>poll</code> 调用一次。</p>'),
    ('<p>By default the global queue interval is 31 for the current-thread scheduler. Please see\n<a href="index.html#multi-threaded-runtime-behavior-at-the-time-of-writing" title="mod tokio::runtime">the module documentation</a> for the default behavior of the multi-thread scheduler.</p>',
     '<p>对于当前线程调度器，默认的全局队列间隔为 31。有关多线程调度器的默认行为，请参阅\n<a href="index.html#multi-threaded-runtime-behavior-at-the-time-of-writing" title="mod tokio::runtime">模块文档</a>。</p>'),
    ('<p>Schedulers have a local queue of already-claimed tasks, and a global queue of incoming\ntasks. Setting the interval to a smaller value increases the fairness of the scheduler,\nat the cost of more synchronization overhead. That can be beneficial for prioritizing\ngetting started on new work, especially if tasks frequently yield rather than complete\nor await on further I/O. Setting the interval to <code>1</code> will prioritize the global queue and\ntasks from the local queue will be executed only if the global queue is empty.\nConversely, a higher value prioritizes existing work, and is a good choice when most\ntasks quickly complete polling.</p>',
     '<p>调度器有一个本地队列用于存放已认领的任务，还有一个全局队列用于存放新进入的任务。\n将间隔设置得更小可以提高调度器的公平性，但代价是会增加同步开销。这有利于优先开始新工作，\n特别是当任务经常让出执行权而不是完成或等待更多 I/O 时。将间隔设置为 <code>1</code> 将优先处理全局队列，\n只有当全局队列为空时才会执行本地队列中的任务。相反，较大的值则会优先处理现有工作，\n当大多数任务能很快完成轮询时，这是一个不错的选择。</p>'),
    ('<p>This function will panic if 0 is passed as an argument.</p>',
     '<p>如果将 0 作为参数传入，此函数将发生 panic。</p>'),

    # ----- event_interval -----
    ('<p>Sets the number of scheduler ticks after which the scheduler will poll for\nexternal events (timers, I/O, and so on).</p>',
     '<p>设置调度器在多少个调度 tick 之后轮询外部事件（定时器、I/O 等）。</p>'),
    ('<p>By default, the event interval is <code>61</code> for all scheduler types.</p>',
     '<p>默认情况下，所有调度器类型的事件间隔为 <code>61</code>。</p>'),
    ('<p>Setting the event interval determines the effective “priority” of delivering\nthese external events (which may wake up additional tasks), compared to\nexecuting tasks that are currently ready to run. A smaller value is useful\nwhen tasks frequently spend a long time in polling, or infrequently yield,\nwhich can result in overly long delays picking up I/O events. Conversely,\npicking up new events requires extra synchronization and syscall overhead,\nso if tasks generally complete their polling quickly, a higher event interval\nwill minimize that overhead while still keeping the scheduler responsive to\nevents.</p>',
     '<p>设置事件间隔决定了传递这些外部事件（它们可能会唤醒其他任务）的有效“优先级”，\n相对于执行当前已就绪的任务。当任务经常在轮询中花费较长时间或不经常让出执行权时，\n较小的值很有用，否则可能会导致在处理 I/O 事件时出现过长的延迟。\n相反，拾取新事件需要额外的同步和系统调用开销，所以如果任务通常能很快完成轮询，\n那么使用较大的事件间隔可以将这种开销降至最低，同时仍能保持调度器对事件的响应能力。</p>'),

    # ----- enable_io -----
    ('<p>Enables the I/O driver.</p>',
     '<p>启用 I/O 驱动。</p>'),
    ('<p>Doing this enables using net, process, signal, and some I/O types on\nthe runtime.</p>',
     '<p>启用后即可在运行时上使用 net、process、signal 以及某些 I/O 类型。</p>'),

    # ----- max_io_events_per_tick -----
    ('<p>Enables the I/O driver and configures the max number of events to be\nprocessed per tick.</p>',
     '<p>启用 I/O 驱动，并配置每个 tick 处理的最大事件数。</p>'),

    # ----- enable_time -----
    ('<p>Enables the time driver.</p>',
     '<p>启用时间驱动。</p>'),
    ('<p>Doing this enables using <code>tokio::time</code> on the runtime.</p>',
     '<p>启用后即可在运行时上使用 <code>tokio::time</code>。</p>'),

    # ----- Blanket impl notes -----
    ('<p>Returns the argument unchanged.</p>',
     '<p>原样返回参数。</p>'),
    ('<p>Calls <code>U::from(self)</code>.</p>',
     '<p>调用 <code>U::from(self)</code>。</p>'),
    # IMPORTANT: this single <p> spans multiple lines and contains an embedded <code>
    # block in the middle. Must replace as a single unit to preserve HTML structure.
    ('<p>That is, this conversion is whatever the implementation of\n<code><a href="https://doc.rust-lang.org/1.95.0/core/convert/trait.From.html" title="trait core::convert::From">From</a>&lt;T&gt; for U</code> chooses to do.</p>',
     '<p>也就是说，此转换是 <code><a href="https://doc.rust-lang.org/1.95.0/core/convert/trait.From.html" title="trait core::convert::From">From</a>&lt;T&gt; for U</code> 实现选择执行的操作。</p>'),
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


def translate_builder(content):
    # Meta description
    old_meta = '<meta name="description" content="Builds Tokio Runtime with custom configuration values.">'
    new_meta = '<meta name="description" content="使用自定义配置值构建 Tokio 运行时。">'
    if old_meta not in content:
        print('  [MISS] meta description')
    content = content.replace(old_meta, new_meta)

    # Title (keep "Builder" identifier)
    content = content.replace('<html lang="en">', '<html lang="zh-CN">')
    # The title contains "Builder in tokio::runtime - Rust" — keep the title as Rust convention

    # Common UI
    content = apply_pairs(content, COMMON_UI, 'common UI')
    # Docblock content
    content = apply_pairs(content, DOCBLOCK_PAIRS, 'docblock')
    return content


def main():
    path = os.path.join(RUNTIME_ROOT, 'struct.Builder.html')
    print(f'--- {path} ---')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = translate_builder(content)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    verify(new_content, 'runtime/struct.Builder.html')
    print()


if __name__ == '__main__':
    main()
