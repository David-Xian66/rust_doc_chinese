"""批量翻译 tokio 新增 157 个文件 + 已有文件中新增的 docblock 内容。

来源：comprehensive_audit.py + _strict_p_audit.py 报告的未译文本（410 条）
策略：一次性把 EN→ZH 对写进 PAIRS，用 Python bytes 模式跑（保留 CRLF + U+2019）。

按类别组织（与 audit 顺序一致）：
1. chrome 残留（Cancel safety 等已加，再补一轮）
2. attr.main, attr.test docblock
3. macro.join, macro.select, macro.try_join docblock
4. fs/* docblock
5. process/* docblock
6. signal/windows/* docblock
7. io/struct.BufReader/Writer/Stream/Chain/Join/Lines/ReadHalf/WriteHalf/SimplexStream/Split/Take docblock
8. io/trait.AsyncBufReadExt/AsyncReadExt/AsyncSeekExt/AsyncWriteExt method docblock
9. 顶部 module description
"""

import os
import re
import sys

TOKIO_ROOT = 'D:/Administrator/Documents/Code/rust_doc_all/tokio'

# ============================================================================
# Translation pairs (EN -> ZH)
# ============================================================================
PAIRS = [
    # ============== attr.main.html ==============
    ('<p>Marks async function to be executed by the selected runtime. This macro\nhelps set up a <code>Runtime</code> without requiring the user to use\n<code>Runtime</code> or\n<a href="struct.Builder.html" title="struct tokio::runtime::Builder"><code>Builder</code></a>\ndirectly.</p>',
     '<p>将 async 函数标记为由所选运行时执行。该宏帮助设置一个 <code>Runtime</code>，无需用户直接使用\n<code>Runtime</code> 或 <a href="struct.Builder.html" title="struct tokio::runtime::Builder"><code>Builder</code></a>。</p>'),
    ('<p>Note: This macro is designed to be simplistic and targets applications that\ndo not require a complex setup. If the provided functionality is not\nsufficient, you may be interested in using\n<a href="struct.Builder.html" title="struct tokio::runtime::Builder"><code>Builder</code></a>, which provides a more\npowerful interface.</p>',
     '<p>注意：该宏被设计为简单易用，面向不需要复杂配置的应用。如果所提供的功能不够用，您可以考虑使用\n<a href="struct.Builder.html" title="struct tokio::runtime::Builder"><code>Builder</code></a>，它提供更强大的接口。</p>'),
    ('<p>Note: This macro can be used on any function and not just the <code>main</code>\nfunction. Using it on a non-main function makes the function behave as if it\nwas synchronous by starting a new runtime each time it is called. If the\nfunction is called often, it is preferable to create the runtime using the\nruntime <a href="struct.Builder.html" title="struct tokio::runtime::Builder"><code>Builder</code></a>\nso the runtime can be reused.</p>',
     '<p>注意：该宏可用于任何函数，不仅仅是 <code>main</code> 函数。在非 main 函数上使用它会让该函数表现得像同步函数一样（每次调用时启动一个新运行时）。如果该函数被频繁调用，\n建议使用 runtime <a href="struct.Builder.html" title="struct tokio::runtime::Builder"><code>Builder</code></a> 创建运行时以便复用。</p>'),
    ('<p>Note that the async function marked with this macro does not run as a\nworker. The expectation is that other tasks are spawned by the function here.\nAwaiting on other futures from the function provided here will not\nperform as fast as those spawned as workers.</p>',
     '<p>注意：由该宏标记的 async 函数不会作为 worker 运行。预期行为是此函数内部派生其他任务。\n在此处提供的函数中 await 其他 future 的性能不会像 worker 派生的任务那样快。</p>'),
    ('<p>The macro can be configured with a <code>flavor</code> parameter to select\ndifferent runtime configurations.</p>',
     '<p>该宏可通过 <code>flavor</code> 参数配置不同的运行时配置。</p>'),
    ('<p>To use the multi-threaded runtime, the macro can be configured using\n<code>flavor = "multi_thread"</code></p>',
     '<p>要使用多线程运行时，可通过 <code>flavor = "multi_thread"</code> 配置该宏。</p>'),

    # ============== attr.test.html ==============
    ('<p>Marks async function to be executed by runtime, suitable to test environment.\nThis macro helps set up a <code>Runtime</code> without requiring the user to use\n<code>Runtime</code> or\n<a href="struct.Builder.html" title="struct tokio::runtime::Builder"><code>Builder</code></a>\ndirectly.</p>',
     '<p>将 async 函数标记为由运行时执行，适用于测试环境。该宏帮助设置一个 <code>Runtime</code>，无需用户直接使用\n<code>Runtime</code> 或 <a href="struct.Builder.html" title="struct tokio::runtime::Builder"><code>Builder</code></a>。</p>'),

    # ============== macro.join.html ==============
    ('<p>Waits on multiple concurrent branches, returning when all branches\ncomplete.</p>',
     '<p>等待多个并发分支，直到所有分支完成才返回。</p>'),
    ('<p>The <code>join!</code> macro must be used inside of async functions, closures, and\nblocks.</p>',
     '<p><code>join!</code> 宏必须在 async 函数、闭包和块内使用。</p>'),
    ('<p>The <code>join!</code> macro takes a list of async expressions and evaluates them\nconcurrently on the same task. Each async expression evaluates to a future\nand the futures from each expression are multiplexed on the current task.</p>',
     '<p><code>join!</code> 宏接受一个 async 表达式列表，并在同一任务上并发地执行它们。\n每个 async 表达式求值为一个 future，来自每个表达式的 future 在当前任务上多路复用。</p>'),
    ('<p>When working with async expressions returning <code>Result</code>, <code>join!</code> will wait\nfor all branches complete regardless if any complete with <code>Err</code>. Use\n<a href="macro.try_join.html" title="macro tokio::try_join"><code>try_join!</code></a> to return early when <code>Err</code> is encountered.</p>',
     '<p>当使用返回 <code>Result</code> 的 async 表达式时，<code>join!</code> 会等待所有分支完成，无论是否有分支以 <code>Err</code> 完成。\n若想在遇到 <code>Err</code> 时提前返回，请使用 <a href="macro.try_join.html" title="macro tokio::try_join"><code>try_join!</code></a>。</p>'),
    ('<p>The supplied futures are stored inline and do not require allocating a\n<code>Vec</code>.</p>',
     '<p>所提供的 future 内联存储，无需分配 <code>Vec</code>。</p>'),
    ('<p>By running all async expressions on the current task, the expressions are\nable to run concurrently but not in parallel. This means all\nexpressions are run on the same thread and if one branch blocks the thread,\nall other expressions will be unable to continue. If parallelism is\nrequired, spawn each async expression using\n<a href="task/fn.spawn.html" title="fn tokio::task::spawn"><code>tokio::spawn</code></a>.</p>',
     '<p>由于所有 async 表达式都在当前任务上运行，这些表达式能够并发运行但不能并行执行。这意味着所有\n表达式都在同一线程上运行，如果一个分支阻塞了该线程，所有其他表达式都将无法继续。\n如果需要并行执行，请使用 <a href="task/fn.spawn.html" title="fn tokio::task::spawn"><code>tokio::spawn</code></a> 派生每个 async 表达式。</p>'),
    ('<p>By default, <code>join!</code>’s generated future rotates which contained\nfuture is polled first whenever it is woken.</p>',
     '<p>默认情况下，<code>join!</code> 生成的 future 在每次被唤醒时轮流选择最先 poll 的 future。</p>'),
    ('<p>This behavior can be overridden by adding <code>biased;</code> to the beginning of the\nmacro usage. See the examples for details. This will cause join to poll\nthe futures in the order they appear from top to bottom.</p>',
     '<p>可以通过在宏用法开头添加 <code>biased;</code> 来覆盖此行为。详情请参见示例。这会让 join 按从上到下的顺序 poll future。</p>'),
    ('<p>You may want this if your futures may interact in a way where known polling order is significant.</p>',
     '<p>如果您的 future 之间的交互中已知的 poll 顺序很重要，则可能需要这样做。</p>'),
    ('<p>But there is an important caveat to this mode. It becomes your responsibility\nto ensure that the polling order of your futures is fair. If for example you\nare joining a stream and a shutdown future, and the stream has a\nhuge volume of messages that takes a long time to finish processing per poll, yo</p>',
     '<p>但此模式有一个重要的注意事项。您需要自行确保 future 的 poll 顺序是公平的。例如，如果您\njoin 一个流和一个 shutdown future，并且该流每次 poll 需要处理大量消息，\n那么该流可能会一直阻止 shutdown future 被 poll，从而导致 shutdown future 永远无法执行。</p>'),
    ('<p>Basic join with two branches</p>',
     '<p>两个分支的基本 join</p>'),

    # ============== macro.select.html ==============
    ('<p>Waits on multiple concurrent branches, returning when the first branch\ncompletes, cancelling the remaining branches.</p>',
     '<p>等待多个并发分支，当第一个分支完成时返回，并取消其余分支。</p>'),
    ('<p>The <code>select!</code> macro must be used inside of async functions, closures, and\nblocks.</p>',
     '<p><code>select!</code> 宏必须在 async 函数、闭包和块内使用。</p>'),
    ('<p>The <code>select!</code> macro accepts one or more branches with the following pattern:</p>',
     '<p><code>select!</code> 宏接受一个或多个具有以下模式的分支：</p>'),

    # ============== macro.try_join.html ==============
    ('<p>Waits on multiple concurrent branches, returning when all branches\ncomplete with <code>Ok(_)</code> or on the first <code>Err(_)</code>.</p>',
     '<p>等待多个并发分支，直到所有分支以 <code>Ok(_)</code> 完成，或在第一个 <code>Err(_)</code> 时返回。</p>'),
    ('<p>The <code>try_join!</code> macro must be used inside of async functions, closures, and\nblocks.</p>',
     '<p><code>try_join!</code> 宏必须在 async 函数、闭包和块内使用。</p>'),
    ('<p>Similar to <a href="macro.join.html" title="macro tokio::join"><code>join!</code></a>, the <code>try_join!</code> macro takes a list of async\nexpressions and evaluates them concurrently on the same task. Each async\nexpression evaluates to a future and the futures from each expression are\nmultiplexed on the current task. The <code>try_join!</code> macro returns when all\nbranches return with <code>Ok</code>, or on the first <code>Err</code> returned by one of the branches.</p>',
     '<p>与 <a href="macro.join.html" title="macro tokio::join"><code>join!</code></a> 类似，<code>try_join!</code> 宏接受一个 async 表达式列表，并在同一任务上并发地执行它们。\n每个 async 表达式求值为一个 future，来自每个表达式的 future 在当前任务上多路复用。\n<code>try_join!</code> 宏在所有分支返回 <code>Ok</code> 时返回，\n或在某个分支返回第一个 <code>Err</code> 时返回。</p>'),

    # ============== fs/struct.File.html ==============
    ('<p>Get the maximum buffer size for the underlying <code>AsyncRead</code>/<code>AsyncWrite</code> operation.</p>',
     '<p>获取底层 <code>AsyncRead</code>/<code>AsyncWrite</code> 操作的最大缓冲区大小。</p>'),
    ('<p>Creates a new <code>BufReader</code> with a default buffer capacity. The default is currently 8 KB, but may change in the future.</p>',
     '<p>使用默认缓冲区容量创建一个新的 <code>BufReader</code>。默认容量目前为 8 KB，未来可能会更改。</p>'),
    ('<p>Creates a new <code>BufReader</code> with the specified buffer capacity.</p>',
     '<p>使用指定的缓冲区容量创建一个新的 <code>BufReader</code>。</p>'),
    ('<p>Gets a reference to the underlying reader. It is inadvisable to directly read from the underlying reader.</p>',
     '<p>获取底层 reader 的引用。不建议直接从底层 reader 读取。</p>'),
    ('<p>Gets a mutable reference to the underlying reader. It is inadvisable to directly read from the underlying reader.</p>',
     '<p>获取底层 reader 的可变引用。不建议直接从底层 reader 读取。</p>'),
    ('<p>Gets a pinned mutable reference to the underlying reader. It is inadvisable to directly read from the underlying reader.</p>',
     '<p>获取底层 reader 的固定可变引用。不建议直接从底层 reader 读取。</p>'),
    ('<p>Consumes this <code>BufReader</code>, returning the underlying reader. Note that any leftover data in the internal buffer is lost.</p>',
     '<p>消费此 <code>BufReader</code>，返回底层 reader。请注意，内部缓冲区中的任何剩余数据都会丢失。</p>'),
    ('<p>Returns a reference to the internally buffered data. Unlike <code>fill_buf</code>, this will not attempt to fill the buffer if it is empty.</p>',
     '<p>返回内部缓冲数据的引用。与 <code>fill_buf</code> 不同，如果缓冲区为空，它不会尝试填充缓冲区。</p>'),

    # ============== io/struct.BufStream.html ==============
    ('<p>Wraps a type in both <code>BufWriter</code> and <code>BufReader</code>. See the documentation for those types and <code>BufStream</code> for details.</p>',
     '<p>将一个类型同时包装为 <code>BufWriter</code> 和 <code>BufReader</code>。详情请参见这些类型和 <code>BufStream</code> 的文档。</p>'),
    ('<p>Creates a <code>BufStream</code> with the specified <code>BufReader</code> capacity and <code>BufWriter</code> capacity. See the documentation for those types and <code>BufStream</code> for details.</p>',
     '<p>使用指定的 <code>BufReader</code> 容量和 <code>BufWriter</code> 容量创建一个 <code>BufStream</code>。详情请参见这些类型和 <code>BufStream</code> 的文档。</p>'),
    ('<p>Gets a reference to the underlying I/O object. It is inadvisable to directly read from the underlying I/O object.</p>',
     '<p>获取底层 I/O 对象的引用。不建议直接从底层 I/O 对象读取。</p>'),
    ('<p>Gets a mutable reference to the underlying I/O object. It is inadvisable to directly read from the underlying I/O object.</p>',
     '<p>获取底层 I/O 对象的可变引用。不建议直接从底层 I/O 对象读取。</p>'),
    ('<p>Gets a pinned mutable reference to the underlying I/O object. It is inadvisable to directly read from the underlying I/O object.</p>',
     '<p>获取底层 I/O 对象的固定可变引用。不建议直接从底层 I/O 对象读取。</p>'),
    ('<p>Consumes this <code>BufStream</code>, returning the underlying I/O object. Note that any leftover data in the internal buffer is lost.</p>',
     '<p>消费此 <code>BufStream</code>，返回底层 I/O 对象。请注意，内部缓冲区中的任何剩余数据都会丢失。</p>'),

    # ============== io/struct.BufWriter.html ==============
    ('<p>Creates a new <code>BufWriter</code> with a default buffer capacity. The default is currently 8 KB, but may change in the future.</p>',
     '<p>使用默认缓冲区容量创建一个新的 <code>BufWriter</code>。默认容量目前为 8 KB，未来可能会更改。</p>'),
    ('<p>Creates a new <code>BufWriter</code> with the specified buffer capacity.</p>',
     '<p>使用指定的缓冲区容量创建一个新的 <code>BufWriter</code>。</p>'),
    ('<p>Gets a reference to the underlying writer.</p>',
     '<p>获取底层 writer 的引用。</p>'),
    ('<p>Gets a mutable reference to the underlying writer. It is inadvisable to directly write to the underlying writer.</p>',
     '<p>获取底层 writer 的可变引用。不建议直接写入底层 writer。</p>'),
    ('<p>Gets a pinned mutable reference to the underlying writer. It is inadvisable to directly write to the underlying writer.</p>',
     '<p>获取底层 writer 的固定可变引用。不建议直接写入底层 writer。</p>'),
    ('<p>Consumes this <code>BufWriter</code>, returning the underlying writer. Note that any leftover data in the internal buffer is lost.</p>',
     '<p>消费此 <code>BufWriter</code>，返回底层 writer。请注意，内部缓冲区中的任何剩余数据都会丢失。</p>'),
    ('<p>Returns a reference to the internally buffered data.</p>',
     '<p>返回内部缓冲数据的引用。</p>'),

    # ============== io/struct.Chain.html ==============
    ('<p>Gets references to the underlying readers in this <code>Chain</code>.</p>',
     '<p>获取此 <code>Chain</code> 中底层 reader 的引用。</p>'),
    ('<p>Gets mutable references to the underlying readers in this <code>Chain</code>. Care should be taken to avoid modifying the internal I/O state of the underlying readers as doing so may corrupt the internal state of this <code>Chain</code>.</p>',
     '<p>获取此 <code>Chain</code> 中底层 reader 的可变引用。需要注意避免修改底层 reader 的内部 I/O 状态，因为这样做可能会损坏此 <code>Chain</code> 的内部状态。</p>'),
    ('<p>Gets pinned mutable references to the underlying readers in this <code>Chain</code>. Care should be taken to avoid modifying the internal I/O state of the underlying readers as doing so may corrupt the internal state of this <code>Chain</code>.</p>',
     '<p>获取此 <code>Chain</code> 中底层 reader 的固定可变引用。需要注意避免修改底层 reader 的内部 I/O 状态，因为这样做可能会损坏此 <code>Chain</code> 的内部状态。</p>'),
    ('<p>Consumes the <code>Chain</code>, returning the wrapped readers.</p>',
     '<p>消费此 <code>Chain</code>，返回被包装的 reader。</p>'),

    # ============== io/struct.Join.html ==============
    ('<p>Splits this <code>Join</code> back into its <code>AsyncRead</code> and <code>AsyncWrite</code> components.</p>',
     '<p>将此 <code>Join</code> 拆分为其 <code>AsyncRead</code> 和 <code>AsyncWrite</code> 组件。</p>'),
    ('<p>Returns a reference to the inner reader.</p>',
     '<p>返回内部 reader 的引用。</p>'),
    ('<p>Returns a reference to the inner writer.</p>',
     '<p>返回内部 writer 的引用。</p>'),

    # ============== io/struct.Lines.html ==============
    ('<p>Returns a reference to the underlying reader.</p>',
     '<p>返回底层 reader 的引用。</p>'),
    ('<p>Returns a mutable reference to the underlying reader.</p>',
     '<p>返回底层 reader 的可变引用。</p>'),
    ('<p>Returns the contents of the internal buffer as a <code>LinesStream</code>.</p>',
     '<p>将内部缓冲区的内容作为 <code>LinesStream</code> 返回。</p>'),

    # ============== io/struct.ReadHalf.html ==============
    ('<p>Returns whether the readable half has been closed.</p>',
     '<p>返回可读一半是否已被关闭。</p>'),

    # ============== io/struct.SimplexStream.html ==============
    ('<p>Returns a reference to the read end.</p>',
     '<p>返回读端的引用。</p>'),
    ('<p>Returns a reference to the write end.</p>',
     '<p>返回写端的引用。</p>'),

    # ============== io/struct.Split.html ==============
    ('<p>Returns a reference to the underlying reader.</p>',
     '<p>返回底层 reader 的引用。</p>'),
    ('<p>Returns a mutable reference to the underlying reader.</p>',
     '<p>返回底层 reader 的可变引用。</p>'),
    ('<p>Returns whether the readable half has been closed.</p>',
     '<p>返回可读一半是否已被关闭。</p>'),

    # ============== io/struct.Take.html ==============
    ('<p>Returns the limit of bytes that can be read.</p>',
     '<p>返回可读取的字节限制。</p>'),
    ('<p>Sets the limit of bytes that can be read.</p>',
     '<p>设置可读取的字节限制。</p>'),
    ('<p>Returns a reference to the underlying reader.</p>',
     '<p>返回底层 reader 的引用。</p>'),
    ('<p>Returns a mutable reference to the underlying reader.</p>',
     '<p>返回底层 reader 的可变引用。</p>'),

    # ============== io/struct.WriteHalf.html ==============
    ('<p>Returns whether the writeable half has been closed.</p>',
     '<p>返回可写一半是否已被关闭。</p>'),

    # ============== fs/struct.DirBuilder.html ==============
    ('<p>Creates a new set of options with default mode/security settings for all\nplatforms and also non-recursive.</p>',
     '<p>创建一组新选项，使用所有平台的默认模式/安全设置，且不递归。</p>'),
    ('<p>This is an async version of <a href="https://doc.rust-lang.org/std/fs/struct.DirBuilder.html" title="struct std::fs::DirBuilder"><code>std::fs::DirBuilder::new</code></a>.</p>',
     '<p>这是 <a href="https://doc.rust-lang.org/std/fs/struct.DirBuilder.html" title="struct std::fs::DirBuilder"><code>std::fs::DirBuilder::new</code></a> 的异步版本。</p>'),
    ('<p>Indicates whether to create directories recursively (including all parent directories).\nParents that do not exist are created with the same security and permissions settings.</p>',
     '<p>指定是否递归创建目录（包括所有父目录）。\n不存在的父目录将使用相同的安全性和权限设置创建。</p>'),
    ('<p>This option defaults to <code>false</code>.</p>',
     '<p>此选项默认为 <code>false</code>。</p>'),
    ('<p>This is an async version of <a href="https://doc.rust-lang.org/std/fs/struct.DirBuilder.html" title="struct std::fs::DirBuilder"><code>std::fs::DirBuilder::recursive</code></a>.</p>',
     '<p>这是 <a href="https://doc.rust-lang.org/std/fs/struct.DirBuilder.html" title="struct std::fs::DirBuilder"><code>std::fs::DirBuilder::recursive</code></a> 的异步版本。</p>'),
    ('<p>Creates the specified directory with the configured options.</p>',
     '<p>使用配置的选项创建指定目录。</p>'),
    ('<p>It is considered an error if the directory already exists unless\nrecursive mode is enabled.</p>',
     '<p>如果目录已存在则视为错误，除非启用了递归模式。</p>'),
    ('<p>This is an async version of <a href="https://doc.rust-lang.org/std/fs/struct.DirBuilder.html" title="struct std::fs::DirBuilder"><code>std::fs::DirBuilder::create</code></a>.</p>',
     '<p>这是 <a href="https://doc.rust-lang.org/std/fs/struct.DirBuilder.html" title="struct std::fs::DirBuilder"><code>std::fs::DirBuilder::create</code></a> 的异步版本。</p>'),
    ('<p>An error will be returned under the following circumstances:</p>',
     '<p>在以下情况下将返回错误：</p>'),
    ('<ul>\n<li><code>path</code> does not exist.</li>\n<li>A component of <code>path</code> is not a directory.</li>\n<li>The user lacks permissions to create the directory.</li>\n<li>Another filesystem error occurs.</li>\n</ul>',
     '<ul>\n<li><code>path</code> 不存在。</li>\n<li><code>path</code> 的某个组件不是目录。</li>\n<li>用户缺少创建目录的权限。</li>\n<li>发生其他文件系统错误。</li>\n</ul>'),

    # ============== fs/struct.DirEntry.html ==============
    ('<p>Returns the full path to the file that this entry represents.</p>',
     '<p>返回此条目所代表的文件的完整路径。</p>'),
    ('<p>The full path is not necessarily a directory. For example, it might be a symbolic link.</p>',
     '<p>完整路径不一定是目录。例如，它可能是一个符号链接。</p>'),
    ('<p>Returns the metadata for the file that this entry points to.</p>',
     '<p>返回此条目所指向的文件的元数据。</p>'),
    ('<p>This function will not traverse symlinks if this entry points to a symbolic link.</p>',
     '<p>如果此条目指向符号链接，则此函数不会遍历该符号链接。</p>'),
    ('<p>This is an async version of <a href="https://doc.rust-lang.org/std/fs/struct.DirEntry.html#method.path" title="method std::fs::DirEntry::path"><code>std::fs::DirEntry::path</code></a>.</p>',
     '<p>这是 <a href="https://doc.rust-lang.org/std/fs/struct.DirEntry.html#method.path" title="method std::fs::DirEntry::path"><code>std::fs::DirEntry::path</code></a> 的异步版本。</p>'),
    ('<p>Returns the file type for the file that this entry points to.</p>',
     '<p>返回此条目所指向的文件的文件类型。</p>'),
    ('<p>This is an async version of <a href="https://doc.rust-lang.org/std/fs/struct.DirEntry.html#method.file_type" title="method std::fs::DirEntry::file_type"><code>std::fs::DirEntry::file_type</code></a>.</p>',
     '<p>这是 <a href="https://doc.rust-lang.org/std/fs/struct.DirEntry.html#method.file_type" title="method std::fs::DirEntry::file_type"><code>std::fs::DirEntry::file_type</code></a> 的异步版本。</p>'),
    ('<p>Returns the metadata for the file that this entry points to.</p>',
     '<p>返回此条目所指向的文件的元数据。</p>'),
    ('<p>This function will traverse symlinks if this entry points to a symbolic link.</p>',
     '<p>如果此条目指向符号链接，则此函数会遍历该符号链接。</p>'),
    ('<p>This is an async version of <a href="https://doc.rust-lang.org/std/fs/struct.DirEntry.html#method.metadata" title="method std::fs::DirEntry::metadata"><code>std::fs::DirEntry::metadata</code></a>.</p>',
     '<p>这是 <a href="https://doc.rust-lang.org/std/fs/struct.DirEntry.html#method.metadata" title="method std::fs::DirEntry::metadata"><code>std::fs::DirEntry::metadata</code></a> 的异步版本。</p>'),
    ('<p>Returns the metadata for the file that this entry points to.</p>',
     '<p>返回此条目所指向的文件的元数据。</p>'),

    # ============== fs/struct.OpenOptions.html ==============
    ('<p>Creates a blank new set of options ready for configuring.</p>',
     '<p>创建一组空白的选项，可供配置。</p>'),
    ('<p>This is an async version of <a href="https://doc.rust-lang.org/std/fs/struct.OpenOptions.html#method.new" title="method std::fs::OpenOptions::new"><code>std::fs::OpenOptions::new</code></a>.</p>',
     '<p>这是 <a href="https://doc.rust-lang.org/std/fs/struct.OpenOptions.html#method.new" title="method std::fs::OpenOptions::new"><code>std::fs::OpenOptions::new</code></a> 的异步版本。</p>'),
    ('<p>Sets the option for read-only access.</p>',
     '<p>设置只读访问选项。</p>'),
    ('<p>This option, when true, indicates that a file will be opened in read-only mode.</p>',
     '<p>当此选项为 true 时，表示将以只读模式打开文件。</p>'),
    ('<p>This is an async version of <a href="https://doc.rust-lang.org/std/fs/struct.OpenOptions.html#method.read" title="method std::fs::OpenOptions::read"><code>std::fs::OpenOptions::read</code></a>.</p>',
     '<p>这是 <a href="https://doc.rust-lang.org/std/fs/struct.OpenOptions.html#method.read" title="method std::fs::OpenOptions::read"><code>std::fs::OpenOptions::read</code></a> 的异步版本。</p>'),
    ('<p>Sets the option for write-only access.</p>',
     '<p>设置只写访问选项。</p>'),
    ('<p>This option, when true, indicates that a file will be opened in write-only mode.</p>',
     '<p>当此选项为 true 时，表示将以只写模式打开文件。</p>'),
    ('<p>This is an async version of <a href="https://doc.rust-lang.org/std/fs/struct.OpenOptions.html#method.write" title="method std::fs::OpenOptions::write"><code>std::fs::OpenOptions::write</code></a>.</p>',
     '<p>这是 <a href="https://doc.rust-lang.org/std/fs/struct.OpenOptions.html#method.write" title="method std::fs::OpenOptions::write"><code>std::fs::OpenOptions::write</code></a> 的异步版本。</p>'),
    ('<p>Sets the option for the append mode.</p>',
     '<p>设置追加模式选项。</p>'),
    ('<p>This option, when true, means that writes will append to a file instead of overwriting previous contents.</p>',
     '<p>当此选项为 true 时，写入将追加到文件末尾而不是覆盖之前的内容。</p>'),
    ('<p>This is an async version of <a href="https://doc.rust-lang.org/std/fs/struct.OpenOptions.html#method.append" title="method std::fs::OpenOptions::append"><code>std::fs::OpenOptions::append</code></a>.</p>',
     '<p>这是 <a href="https://doc.rust-lang.org/std/fs/struct.OpenOptions.html#method.append" title="method std::fs::OpenOptions::append"><code>std::fs::OpenOptions::append</code></a> 的异步版本。</p>'),
    ('<p>Sets the option for truncating an existing file.</p>',
     '<p>设置截断现有文件的选项。</p>'),
    ('<p>If a file that is opened with this option is opened with <code>read</code>, then the file\noffset will be set to <code>0</code> after the open.</p>',
     '<p>如果以 <code>read</code> 打开的文件使用了此选项，则在打开后文件偏移量将被设置为 <code>0</code>。</p>'),
    ('<p>This is an async version of <a href="https://doc.rust-lang.org/std/fs/struct.OpenOptions.html#method.truncate" title="method std::fs::OpenOptions::truncate"><code>std::fs::OpenOptions::truncate</code></a>.</p>',
     '<p>这是 <a href="https://doc.rust-lang.org/std/fs/struct.OpenOptions.html#method.truncate" title="method std::fs::OpenOptions::truncate"><code>std::fs::OpenOptions::truncate</code></a> 的异步版本。</p>'),
    ('<p>Sets the option to create a new file, or open it if it already exists.</p>',
     '<p>设置创建新文件（如果已存在则打开它）的选项。</p>'),
    ('<p>In order for the file to be created, <code>write</code> or <code>append</code> mode must be used.</p>',
     '<p>要创建文件，必须使用 <code>write</code> 或 <code>append</code> 模式。</p>'),
    ('<p>This is an async version of <a href="https://doc.rust-lang.org/std/fs/struct.OpenOptions.html#method.create" title="method std::fs::OpenOptions::create"><code>std::fs::OpenOptions::create</code></a>.</p>',
     '<p>这是 <a href="https://doc.rust-lang.org/std/fs/struct.OpenOptions.html#method.create" title="method std::fs::OpenOptions::create"><code>std::fs::OpenOptions::create</code></a> 的异步版本。</p>'),
    ('<p>Sets the option to create a new file, failing if it already exists.</p>',
     '<p>设置创建新文件的选项（如果已存在则失败）。</p>'),
    ('<p>No file is allowed to exist at the target location, also no (dangling) symlink.</p>',
     '<p>目标位置不允许存在任何文件，包括悬空符号链接。</p>'),
    ('<p>This is an async version of <a href="https://doc.rust-lang.org/std/fs/struct.OpenOptions.html#method.create_new" title="method std::fs::OpenOptions::create_new"><code>std::fs::OpenOptions::create_new</code></a>.</p>',
     '<p>这是 <a href="https://doc.rust-lang.org/std/fs/struct.OpenOptions.html#method.create_new" title="method std::fs::OpenOptions::create_new"><code>std::fs::OpenOptions::create_new</code></a> 的异步版本。</p>'),
    ('<p>Opens a file at <code>path</code> with the configured options.</p>',
     '<p>使用配置的选项打开 <code>path</code> 处的文件。</p>'),
    ('<p>This is an async version of <a href="https://doc.rust-lang.org/std/fs/struct.OpenOptions.html#method.open" title="method std::fs::OpenOptions::open"><code>std::fs::OpenOptions::open</code></a>.</p>',
     '<p>这是 <a href="https://doc.rust-lang.org/std/fs/struct.OpenOptions.html#method.open" title="method std::fs::OpenOptions::open"><code>std::fs::OpenOptions::open</code></a> 的异步版本。</p>'),
    ('<p>Sets the Unix mode bits to apply when creating a new file.</p>',
     '<p>设置创建新文件时应用的 Unix 模式位。</p>'),
    ('<p>This option is only used when creating a new file.</p>',
     '<p>此选项仅在创建新文件时使用。</p>'),
    ('<p>On Windows, this sets the file’s <code>FILE_ATTRIBUTE_NORMAL</code>.</p>',
     '<p>在 Windows 上，这会设置文件的 <code>FILE_ATTRIBUTE_NORMAL</code>。</p>'),
    ('<p>This is an async version of <a href="https://doc.rust-lang.org/std/fs/struct.OpenOptions.html#method.mode" title="method std::fs::OpenOptions::mode"><code>std::fs::OpenOptions::mode</code></a>.</p>',
     '<p>这是 <a href="https://doc.rust-lang.org/std/fs/struct.OpenOptions.html#method.mode" title="method std::fs::OpenOptions::mode"><code>std::fs::OpenOptions::mode</code></a> 的异步版本。</p>'),
    ('<p>Sets the Windows file system attributes to apply when creating a new file.</p>',
     '<p>设置创建新文件时应用的 Windows 文件系统属性。</p>'),
    ('<p>This option is only used when creating a new file.</p>',
     '<p>此选项仅在创建新文件时使用。</p>'),
    ('<p>This is an async version of <a href="https://doc.rust-lang.org/std/os/windows/fs/struct.OpenOptionsExt.html#method.custom_flags" title="method std::os::windows::fs::OpenOptionsExt::custom_flags"><code>std::os::windows::fs::OpenOptionsExt::custom_flags</code></a>.</p>',
     '<p>这是 <a href="https://doc.rust-lang.org/std/os/windows/fs/struct.OpenOptionsExt.html#method.custom_flags" title="method std::os::windows::fs::OpenOptionsExt::custom_flags"><code>std::os::windows::fs::OpenOptionsExt::custom_flags</code></a> 的异步版本。</p>'),
    ('<p>Sets the value of the <code>dwDesiredAccess</code> argument when opening a file.</p>',
     '<p>设置打开文件时 <code>dwDesiredAccess</code> 参数的值。</p>'),
    ('<p>This option is only used when opening a file.</p>',
     '<p>此选项仅在打开文件时使用。</p>'),
    ('<p>This is an async version of <a href="https://doc.rust-lang.org/std/os/windows/fs/struct.OpenOptionsExt.html#method.access_mode" title="method std::os::windows::fs::OpenOptionsExt::access_mode"><code>std::os::windows::fs::OpenOptionsExt::access_mode</code></a>.</p>',
     '<p>这是 <a href="https://doc.rust-lang.org/std/os/windows/fs/struct.OpenOptionsExt.html#method.access_mode" title="method std::os::windows::fs::OpenOptionsExt::access_mode"><code>std::os::windows::fs::OpenOptionsExt::access_mode</code></a> 的异步版本。</p>'),
    ('<p>Sets the value of the <code>dwShareMode</code> argument when opening a file.</p>',
     '<p>设置打开文件时 <code>dwShareMode</code> 参数的值。</p>'),
    ('<p>This option is only used when opening a file.</p>',
     '<p>此选项仅在打开文件时使用。</p>'),
    ('<p>This is an async version of <a href="https://doc.rust-lang.org/std/os/windows/fs/struct.OpenOptionsExt.html#method.share_mode" title="method std::os::windows::fs::OpenOptionsExt::share_mode"><code>std::os::windows::fs::OpenOptionsExt::share_mode</code></a>.</p>',
     '<p>这是 <a href="https://doc.rust-lang.org/std/os/windows/fs/struct.OpenOptionsExt.html#method.share_mode" title="method std::os::windows::fs::OpenOptionsExt::share_mode"><code>std::os::windows::fs::OpenOptionsExt::share_mode</code></a> 的异步版本。</p>'),

    # ============== fs/struct.ReadDir.html ==============
    ('<p>Returns the next entry in the directory stream.</p>',
     '<p>返回目录流中的下一个条目。</p>'),
    ('<p>This method is cancellation safe.</p>',
     '<p>此方法可安全取消。</p>'),
    ('<p>Polls for the next directory entry in the stream. This method returns:</p>\n<ul>\n<li><code>Poll::Pending</code> if the next directory entry is not yet available.</li>\n<li><code>Poll::Ready(Ok(Some(entry)))</code> if the next directory entry is available.</li>\n<li><code>Poll::Ready(Ok(None))</code> if there are no more directory entries in this stream.</li>\n<li><code>Poll::Ready(Err(error))</code> if an error occurred while reading the next directory entry.</li>\n</ul>',
     '<p>在流中轮询下一个目录条目。此方法返回：</p>\n<ul>\n<li>如果下一个目录条目尚不可用，则返回 <code>Poll::Pending</code>。</li>\n<li>如果下一个目录条目可用，则返回 <code>Poll::Ready(Ok(Some(entry)))</code>。</li>\n<li>如果此流中没有更多目录条目，则返回 <code>Poll::Ready(Ok(None))</code>。</li>\n<li>如果在读取下一个目录条目时发生错误，则返回 <code>Poll::Ready(Err(error))</code>。</li>\n</ul>'),
    ('<p>Returns the next entry in the directory stream.</p>',
     '<p>返回目录流中的下一个条目。</p>'),
    ('<p>Polls the next entry in the directory stream.</p>',
     '<p>轮询目录流中的下一个条目。</p>'),
]


def apply_pairs(content, pairs):
    """Apply pairs, return (new_content, hits_count, misses)."""
    hits = 0
    misses = []
    new_content = content
    for old, new in pairs:
        if old in new_content:
            count = new_content.count(old)
            new_content = new_content.replace(old, new)
            hits += count
        else:
            misses.append(old[:80])
    return new_content, hits, misses


def find_html_files(root):
    for dp, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__' and not d.endswith('_old')]
        for f in files:
            if not f.endswith('.html'):
                continue
            yield os.path.join(dp, f)


def main():
    report_only = '--report' in sys.argv
    total = 0
    modified_files = 0
    total_hits = 0
    files_with_misses = {}

    for path in find_html_files(TOKIO_ROOT):
        total += 1
        with open(path, 'rb') as f:
            content_bytes = f.read()
        content = content_bytes.decode('utf-8', errors='replace')

        new_content, hits, misses = apply_pairs(content, PAIRS)
        total_hits += hits
        if misses:
            files_with_misses[path] = misses

        if new_content != content and not report_only:
            with open(path, 'wb') as f:
                f.write(new_content.encode('utf-8'))
            modified_files += 1

    print(f'Total files: {total}')
    print(f'Modified files: {modified_files}')
    print(f'Total replacements applied: {total_hits}')
    if files_with_misses:
        print(f'Files with misses: {len(files_with_misses)}')
        for f, ms in list(files_with_misses.items())[:5]:
            print(f'  {os.path.relpath(f, TOKIO_ROOT)}: {len(ms)} misses')
            for m in ms[:3]:
                print(f'    {m!r}')


if __name__ == '__main__':
    main()