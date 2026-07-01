#!/usr/bin/env python3
"""tokio 第二阶段翻译（bytes 模式）：翻译所有新增文件漏译的 docblock。

策略：
- 全部字符串以 bytes 模式处理
- 自动处理 CRLF：源文件用 \r\n 时，模式串会自动扩展 \n -> \r\n
"""
import os

BASE = r'D:/Administrator/Documents/Code/rust_doc_all/tokio'

# (en_text, zh_text)  - 文本片段以 \n 表示行尾（bytes 模式会处理 CRLF）
TRAIT_PAIRS = [
    # ===== Trait method docblocks =====
    ('Returns a duplicate of the value.', '返回值的副本。'),
    ('Formats the value using the given formatter.', '使用给定的格式化器格式化此值。'),
    ('Returns the "default value" for a type.', '返回一个类型的"默认值"。'),
    ('Returns the default value of a type.', '返回一个类型的默认值。'),
    ('Executes the destructor for this type.', '执行此类型的析构函数。'),
    ('Attempts to resolve the future to a final value, registering the current task for wakeup if the value is not yet available.',
     '尝试将 Future 解析为最终值，若值尚不可用则注册当前任务以备唤醒。'),
    ('Attempts to resolve the future to a final value.', '尝试将此 Future 解析为最终值。'),
    ('Tests for self and other values to be equal, and is used by == .', '测试 self 与 other 值是否相等，供 == 运算符使用。'),
    ('Tests for <code>self</code> and <code>other</code> values to be equal, and is used by <code>==</code>.', '测试 <code>self</code> 与 <code>other</code> 值是否相等，供 <code>==</code> 运算符使用。'),
    ('Tests for self and other values to be not equal, and is used by != .', '测试 self 与 other 值是否不相等，供 != 运算符使用。'),
    ('Tests for <code>self</code> and <code>other</code> values to be not equal, and is used by <code>!=</code>.', '测试 <code>self</code> 与 <code>other</code> 值是否不相等，供 <code>!=</code> 运算符使用。'),
    ('This method returns an ordering between self and other values if one exists.', '若存在，此方法返回 self 与 other 值之间的排序关系。'),
    ('Tests less than (for self and other) and is used by the < operator.', '测试小于（针对 self 与 other），供 < 运算符使用。'),
    ('Tests less than or equal to (for self and other) and is used by the <= operator.', '测试小于等于（针对 self 与 other），供 <= 运算符使用。'),
    ('Tests greater than (for self and other) and is used by the > operator.', '测试大于（针对 self 与 other），供 > 运算符使用。'),
    ('Tests greater than or equal to (for self and other) and is used by the >= operator.', '测试大于等于（针对 self 与 other），供 >= 运算符使用。'),
    ('This method returns an Ordering between self and other .', '此方法返回 self 与 other 之间的 Ordering。'),
    ('Feeds this value into the given Hasher .', '将此值送入给定的 Hasher。'),
    ('Converts to this type from the input type.', '从输入类型转换为此类型。'),
    ('Performs the conversion.', '执行转换。'),
    ('Returns the lower-level source of this error, if any.', '返回此错误的更底层来源（若有）。'),
    ('>Read more</a>', '>更多信息</a>'),
    ('Dyn Compatibility', '动态兼容性'),

    # ===== Title/description chrome =====
    ('<title>List of all items in this crate</title>', '<title>本 crate 所有条目列表</title>'),
    ('List of all items in this crate', '本 crate 所有条目列表'),
    ('In crate tokio', '在 crate tokio 中'),
    ('This variant is marked as non-exhaustive', '此变体被标记为 non-exhaustive'),

    # ===== attr.main.html =====
    ('Marks async function to be executed by the selected runtime. This macro\nhelps set up a Runtime without requiring the user to use\nRuntime or\nBuilder directly.\n\n# Examples\n\n```\n#[tokio::main]\nasync fn main() {\n    println!("hello");\n}\n```\n\n',
     '标记将由所选运行时执行的 async 函数。本宏帮助设置 Runtime，无需用户直接使用\nRuntime 或\nBuilder。\n\n# 示例\n\n```\n#[tokio::main]\nasync fn main() {\n    println!("hello");\n}\n```\n\n'),
    ('Note: This macro is designed to be simplistic and targets applications that\ndo not require a complex setup. If the provided functionality is not\nsufficient, you may be interested in using\nBuilder, which offers a much more powerful configuration.',
     '注意：本宏设计为简单易用，面向不需要复杂配置的应用。若所提供的功能不够用，可考虑使用 Builder，它提供更强大的配置。'),
    ('Note: This macro is designed to be simplistic and targets applications that\ndo not require a complex setup. If the provided functionality is not\nsufficient, you may be interested in using',
     '注意：本宏设计为简单易用，面向不需要复杂配置的应用。若所提供的功能不够用，可考虑使用'),
    ('Note: This macro can be used on any function and not just the main\nfunction. Using it on a non-main function makes the function behave as if it\nwas sync, but returns a future that can be awaited.',
     '注意：本宏可用于任何函数，不限于 main 函数。在非 main 函数上使用时，会让该函数表现得像同步函数，但实际返回一个可被 await 的 Future。'),
    ('Note that the async function marked with this macro does not run as a\nworker. The expectation is that other tasks are spawned by the function here.\nAwaiting on other futures from the function here is allowed.',
     '请注意，被本宏标记的 async 函数不会作为 worker 运行。预期此函数会在内部派生其他任务。在此处 await 其他 Future 是允许的。'),
    ('The macro can be configured with <code>flavor</code> and <code>worker_threads</code> parameters, where <code>flavor</code> selects different runtime configurations and <code>worker_threads</code> configures the number of worker threads.',
     '可通过 <code>flavor</code> 与 <code>worker_threads</code> 参数配置本宏：<code>flavor</code> 选择不同的运行时配置，<code>worker_threads</code> 配置 worker 线程数。'),
    ('To use the multi-threaded runtime, the macro can be configured using:\n\n```\n#[tokio::main(flavor = "multi_thread", worker_threads = 10)]\n```\n',
     '使用多线程运行时，可按如下方式配置本宏：\n\n```\n#[tokio::main(flavor = "multi_thread", worker_threads = 10)]\n```\n'),

    # ===== attr.test.html =====
    ('Marks async function to be executed by runtime, suitable to test environment.\nThis macro helps set up a Runtime without requiring the user to use\nRuntime or\nBuilder directly.\n\n# Examples\n\n```\n#[tokio::test]\nasync fn test() {\n    assert!(true);\n}\n```\n\n',
     '标记将由运行时（适用于测试环境）执行的 async 函数。本宏帮助设置 Runtime，无需用户直接使用\nRuntime 或\nBuilder。\n\n# 示例\n\n```\n#[tokio::test]\nasync fn test() {\n    assert!(true);\n}\n```\n\n'),

    # ===== macro.join.html =====
    ('Waits on multiple concurrent branches, returning when all branches\ncomplete.', '等待多个并发分支，当所有分支完成时返回。'),
    ('The join! macro must be used inside of async functions, closures, and\nblocks.', 'join! 宏必须在 async 函数、闭包与代码块内使用。'),
    ('The join! macro takes a list of async expressions and evaluates them\nconcurrently on the same task. Each async expression evaluates to a future\nand the futures from each expression are multiplexed on the current task.',
     'join! 宏接收一组 async 表达式，并在同一任务上并发求值。每个 async 表达式求值为一个 Future，各表达式产生的 Future 会在当前任务上进行多路复用。'),
    ('When working with async expressions returning <code>Result</code>, <code>join!</code> will wait\nfor all branches complete regardless if any complete with <code>Err</code>. Use\n<code>try_join!</code> to return early when an error is encountered.',
     '当 async 表达式返回 <code>Result</code> 时，<code>join!</code> 会等待所有分支完成，无论是否有分支返回 <code>Err</code>。遇到错误需要提前返回时，请使用 <code>try_join!</code>。'),
    ('The supplied futures are stored inline and do not require allocating a\n<code>Vec</code>.', '所提供的 Future 内联存储，无需分配 <code>Vec</code>。'),
    ('The supplied futures are stored inline and do not require allocating a\nVec.', '所提供的 Future 内联存储，无需分配 Vec。'),
    ('By running all async expressions on the current task, the expressions are\nable to run concurrently but not in parallel. This means all\nexpressions are run on the same thread and if one branch blocks the thread,\nall other expressions will be unable to continue. If parallelism is\nrequired, spawn each async expression using\n<code>tokio::spawn</code>.',
     '由于所有 async 表达式都在当前任务上运行，这些表达式可以并发运行，但不能并行执行。这意味着所有表达式都在同一线程上运行，如果某个分支阻塞线程，所有其他表达式都无法继续。如果需要并行，请使用 <code>tokio::spawn</code> 派生每个 async 表达式。'),
    ('By default, <code>join!</code>\'s generated future rotates which contained\nfuture is polled first whenever it is woken.',
     '默认情况下，<code>join!</code> 生成的 Future 在每次被唤醒时轮换最先轮询的内部 Future。'),
    ('By default, join!\'s generated future rotates which contained\nfuture is polled first whenever it is woken.',
     '默认情况下，join! 生成的 Future 在每次被唤醒时轮换最先轮询的内部 Future。'),
    ('This behavior can be overridden by adding <code>biased;</code> to the beginning of the\nmacro usage. See the examples for details. This will cause join to poll the\nfutures in the order they appear from top to bottom.',
     '可通过在宏调用的开头添加 <code>biased;</code> 来覆盖此行为。详见示例。这会让 join 按从上到下出现的顺序轮询 Future。'),
    ('This behavior can be overridden by adding <code>biased;</code> to the beginning of the\nmacro usage. See the examples for details. This will cause join to poll the\nfutures in the order they appear from top to bottom.\n\nYou may want this if your futures may interact in a way where known polling order is significant.',
     '可通过在宏调用的开头添加 <code>biased;</code> 来覆盖此行为。详见示例。这会让 join 按从上到下出现的顺序轮询 Future。\n\n当你的 Future 之间可能存在交互且已知的轮询顺序很重要时，可能需要此选项。'),
    ('You may want this if your futures may interact in a way where known polling order is significant.', '当你的 Future 之间可能存在交互且已知的轮询顺序很重要时，可能需要此选项。'),
    ('But there is an important caveat to this mode. It becomes your responsibility\nto ensure that the polling order of your futures is fair. If for example\nyou are joining a stream and a shutdown future, and the stream has a\nhuge volume of messages that takes a long time to finish processing per poll, yo',
     '但此模式有一个重要注意事项：保证 Future 轮询顺序的公平性是你的责任。例如，若你将一个流与关闭 Future 进行 join，且该流每次轮询都需要处理大量消息、要花很长时间才能完成一次轮询，'),

    # ===== macro.try_join.html =====
    ('Waits on multiple concurrent branches, returning when all branches\ncomplete with <code>Ok(_)</code> or on the first <code>Err(_)</code>.',
     '等待多个并发分支，当所有分支以 <code>Ok(_)</code> 完成或遇到第一个 <code>Err(_)</code> 时返回。'),
    ('The try_join! macro must be used inside of async functions, closures, and\nblocks.', 'try_join! 宏必须在 async 函数、闭包与代码块内使用。'),
    ('Similar to join!, the try_join! macro takes a list of async\nexpressions and evaluates them concurrently on the same task. Each async\nexpression evaluates to a future and the futures from each expression are\nmultiplexed on the current task.',
     '与 join! 类似，try_join! 宏接收一组 async 表达式，并在同一任务上并发求值。每个 async 表达式求值为一个 Future，各表达式产生的 Future 会在当前任务上进行多路复用。'),
    ('By default, <code>try_join!</code>\'s generated future rotates which\ncontained future is polled first whenever it is woken.',
     '默认情况下，<code>try_join!</code> 生成的 Future 在每次被唤醒时轮换最先轮询的内部 Future。'),
    ('By default, try_join!\'s generated future rotates which\ncontained future is polled first whenever it is woken.',
     '默认情况下，try_join! 生成的 Future 在每次被唤醒时轮换最先轮询的内部 Future。'),

    # ===== macro.select.html =====
    ('Waits on multiple concurrent branches, returning when the first branch\ncompletes, cancelling the remaining branches.',
     '等待多个并发分支，当第一个分支完成时返回，并取消其余分支。'),
    ('The select! macro must be used inside of async functions, closures, and\nblocks.', 'select! 宏必须在 async 函数、闭包与代码块内使用。'),
    ('The select! macro accepts one or more branches with the following pattern:\n\n```\n<prelude>;<pattern> = <async expression> (, if <precondition>)? => <handler>,\n```\n\n',
     'select! 宏接受一个或多个具有如下形式的分支：\n\n```\n<prelude>;<pattern> = <async 表达式> (, if <前置条件>)? => <处理逻辑>,\n```\n\n'),

    # ===== io/trait.AsyncReadExt.html =====
    ('Reads bytes from a source.\nImplemented as an extension trait, adding utility methods to all\n<a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> types. Callers will tend to import this trait instead of\n<a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a>',
     '从源读取字节。\n作为扩展特性实现，向所有\n<a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> 类型添加工具方法。调用者通常会导入本特性而非\n<a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a>'),

    # ===== io/struct.BufReader.html =====
    ('The <a href="struct.BufReader.html"><code>BufReader</code></a> struct adds buffering to any reader.\nIt can be excessively inefficient to work directly with a <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> instance.',
     '<a href="struct.BufReader.html"><code>BufReader</code></a> 结构体为任何读取器添加缓冲。\n直接使用 <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> 实例可能非常低效。'),
    ('Creating a <code>BufReader</code> with a default buffer capacity.', '使用默认缓冲容量创建 <code>BufReader</code>。'),
    ('Creating a <code>BufReader</code> with the specified buffer capacity.', '使用指定的缓冲容量创建 <code>BufReader</code>。'),
    ('Creating a <code>BufReader</code> with the specified buffer capacity.\n\nIt is an error to pass a <code>capacity</code> of zero.',
     '使用指定的缓冲容量创建 <code>BufReader</code>。\n\n传入 <code>capacity</code> 为零是错误的。'),
    ('Getting a reference to the underlying reader.', '获取底层读取器的引用。'),
    ('Getting a mutable reference to the underlying reader.', '获取底层读取器的可变引用。'),
    ('It is inadvisable to directly read from the underlying reader.', '不建议直接读取底层读取器。'),
    ('Getting a pinned mutable reference to the underlying reader.', '获取底层读取器的 pinned 可变引用。'),
    ('Consuming this <code>BufReader</code>, returning the underlying reader.', '消费此 <code>BufReader</code>，返回底层读取器。'),
    ('Note that any leftover data in the internal buffer is lost.', '请注意，内部缓冲中的所有剩余数据都将丢失。'),
    ('Returning a reference to the internally buffered data.', '返回内部缓冲数据的引用。'),
    ('Unlike <code>fill_buf</code>, this will not attempt to fill the buffer if it is empty.', '与 <code>fill_buf</code> 不同，若缓冲为空，此方法不会尝试填充缓冲。'),

    # ===== io/struct.BufWriter.html =====
    ('The <a href="struct.BufWriter.html"><code>BufWriter</code></a> struct adds buffering to any writer.\nIt can be excessively inefficient to work directly with a <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> instance.',
     '<a href="struct.BufWriter.html"><code>BufWriter</code></a> 结构体为任何写入器添加缓冲。\n直接使用 <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> 实例可能非常低效。'),
    ('Creating a <code>BufWriter</code> with a default buffer capacity.', '使用默认缓冲容量创建 <code>BufWriter</code>。'),
    ('Creating a <code>BufWriter</code> with the specified buffer capacity.', '使用指定的缓冲容量创建 <code>BufWriter</code>。'),
    ('Getting a reference to the underlying writer.', '获取底层写入器的引用。'),
    ('Getting a mutable reference to the underlying writer.', '获取底层写入器的可变引用。'),
    ('It is inadvisable to directly write to the underlying writer.', '不建议直接写入底层写入器。'),
    ('Getting a pinned mutable reference to the underlying writer.', '获取底层写入器的 pinned 可变引用。'),
    ('Consuming this <code>BufWriter</code>, returning the underlying writer.', '消费此 <code>BufWriter</code>，返回底层写入器。'),
    ('Returning a reference to the internally buffered data.\n\nUnlike <code>flush</code>, this will not attempt to write the buffer to the underlying writer.',
     '返回内部缓冲数据的引用。\n\n与 <code>flush</code> 不同，此方法不会尝试将缓冲写入底层写入器。'),

    # ===== io/struct.BufStream.html =====
    ('Wraps a type in both <a href="struct.BufReader.html" title="struct tokio::io::BufReader"><code>BufReader</code></a> and <a href="struct.BufWriter.html" title="struct tokio::io::BufWriter"><code>BufWriter</code></a>.\nSee the documentation for those types and <a href="struct.BufStream.html"><code>BufStream</code></a> for details.',
     '将一个类型同时包装为 <a href="struct.BufReader.html" title="struct tokio::io::BufReader"><code>BufReader</code></a> 与 <a href="struct.BufWriter.html" title="struct tokio::io::BufWriter"><code>BufWriter</code></a>。\n详见相关类型与 <a href="struct.BufStream.html"><code>BufStream</code></a> 的文档。'),
    ('Creating a <code>BufStream</code> with the default buffer capacities for the\nwrapped <a href="struct.BufReader.html" title="struct tokio::io::BufReader"><code>BufReader</code></a> and <a href="struct.BufWriter.html" title="struct tokio::io::BufWriter"><code>BufWriter</code></a>.',
     '使用 <a href="struct.BufReader.html" title="struct tokio::io::BufReader"><code>BufReader</code></a> 与 <a href="struct.BufWriter.html" title="struct tokio::io::BufWriter"><code>BufWriter</code></a> 的默认缓冲容量创建 <code>BufStream</code>。'),
    ('Creating a <code>BufStream</code> with the specified <a href="struct.BufReader.html" title="struct tokio::io::BufReader"><code>BufReader</code></a> capacity and <a href="struct.BufWriter.html" title="struct tokio::io::BufWriter"><code>BufWriter</code></a> capacity. See the documentation for those types and <a href="struct.BufStream.html"><code>BufStream</code></a> for details.',
     '使用指定的 <a href="struct.BufReader.html" title="struct tokio::io::BufReader"><code>BufReader</code></a> 与 <a href="struct.BufWriter.html" title="struct tokio::io::BufWriter"><code>BufWriter</code></a> 容量创建 <code>BufStream</code>。详见相关类型与 <a href="struct.BufStream.html"><code>BufStream</code></a> 的文档。'),
    ('Getting a reference to the underlying I/O object.', '获取底层 I/O 对象的引用。'),
    ('It is inadvisable to directly read from the underlying I/O object.', '不建议直接读取底层 I/O 对象。'),
    ('Getting a mutable reference to the underlying I/O object.', '获取底层 I/O 对象的可变引用。'),
    ('Getting a pinned mutable reference to the underlying I/O object.', '获取底层 I/O 对象的 pinned 可变引用。'),
    ('Consuming this <code>BufStream</code>, returning the underlying I/O object.', '消费此 <code>BufStream</code>，返回底层 I/O 对象。'),

    # ===== io/struct.Chain.html =====
    ('The <a href="struct.Chain.html"><code>Chain</code></a> struct allows you to chain two readers together.', '<a href="struct.Chain.html"><code>Chain</code></a> 结构体允许将两个读取器链在一起。'),
    ('Getting references to the underlying readers in this <code>Chain</code>.', '获取此 <code>Chain</code> 中底层读取器的引用。'),
    ('Getting mutable references to the underlying readers in this <code>Chain</code>.', '获取此 <code>Chain</code> 中底层读取器的可变引用。'),
    ('Getting pinned mutable references to the underlying readers in this <code>Chain</code>.', '获取此 <code>Chain</code> 中底层读取器的 pinned 可变引用。'),
    ('Care should be taken to avoid modifying the internal I/O state of the\nunderlying readers as doing so may corrupt the internal state of this\n<code>Chain</code>.',
     '请注意避免修改底层读取器的内部 I/O 状态，否则可能损坏此 <code>Chain</code> 的内部状态。'),
    ('Consuming the <code>Chain</code>, returning the wrapped readers.', '消费此 <code>Chain</code>，返回被包装的读取器。'),

    # ===== io/struct.Join.html =====
    ('The <a href="struct.Join.html"><code>Join</code></a> struct allows you to combine two streams into one.', '<a href="struct.Join.html"><code>Join</code></a> 结构体允许将两个流合并为一个。'),
    ('Splits this <code>Join</code> back into its <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> and <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> components.',
     '将此 <code>Join</code> 拆回 <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> 与 <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> 两个组件。'),
    ('Returning a reference to the inner reader.', '返回内部读取器的引用。'),
    ('Returning a reference to the inner writer.', '返回内部写入器的引用。'),

    # ===== io/struct.Lines.html =====
    ('The <a href="struct.Lines.html"><code>Lines</code></a> struct allows you to read a stream of lines.', '<a href="struct.Lines.html"><code>Lines</code></a> 结构体允许你按行读取流。'),
    ('Returns the inner reader.', '返回内部读取器。'),
    ('Returns a mutable reference to the inner reader.', '返回内部读取器的可变引用。'),
    ('Returns a pinned mutable reference to the inner reader.', '返回内部读取器的 pinned 可变引用。'),
    ('Returns the next line in the stream.', '返回流中的下一行。'),

    # ===== io/struct.Take.html =====
    ('The <a href="struct.Take.html"><code>Take</code></a> struct allows you to read a fixed number of bytes from a stream.', '<a href="struct.Take.Take.html"><code>Take</code></a> 结构体允许你从一个流中读取固定数量的字节。'.replace('Take.Take.html', 'Take.html')),
    ('Returns the maximum number of bytes that can be read.', '返回可读取的最大字节数。'),
    ('Returns the remaining number of bytes that can be read before this\ninstance will return EOF.', '返回此实例返回 EOF 之前还可以读取的剩余字节数。'),
    ('Note: This instance may reach EOF after reading fewer bytes than indicated\nby this method if the underlying reader does not provide enough data.',
     '注意：如果底层读取器没有提供足够的数据，此实例可能在读取的字节少于本方法指示的数量时到达 EOF。'),
    ('This instance may reach EOF after reading fewer bytes than indicated by\nthis method if the underlying reader does not provide enough data.',
     '如果底层读取器没有提供足够的数据，此实例可能在读取的字节少于本方法指示的数量时到达 EOF。'),
    ('Sets the number of bytes that can be read before this instance will\nreturn EOF. This is the same as constructing a new <code>Take</code> instance, so\nthe amount of bytes read and the previous limit value don\'t matter.',
     '设置此实例返回 EOF 之前可读取的字节数。这与构造一个新的 <code>Take</code> 实例等价，因此之前已读取的字节数与先前的限制值无关。'),
    ('Getting a reference to the underlying reader.', '获取底层读取器的引用。'),
    ('Getting a mutable reference to the underlying reader. Care should be\ntaken to avoid modifying the internal I/O state of the underlying reader as\ndoing so may corrupt the internal limit of this <code>Take</code>.',
     '获取底层读取器的可变引用。请注意避免修改底层读取器的内部 I/O 状态，否则可能损坏此 <code>Take</code> 的内部限制。'),
    ('Getting a pinned mutable reference to the underlying reader. Care\nshould be taken to avoid modifying the internal I/O state of the underlying\nreader as doing so may corrupt the internal limit of this <code>Take</code>.',
     '获取底层读取器的 pinned 可变引用。请注意避免修改底层读取器的内部 I/O 状态，否则可能损坏此 <code>Take</code> 的内部限制。'),
    ('Consuming the <code>Take</code>, returning the wrapped reader.', '消费此 <code>Take</code>，返回被包装的读取器。'),

    # ===== io/struct.DuplexStream.html =====
    ('The <a href="struct.DuplexStream.html"><code>DuplexStream</code></a> struct allows you to read and write from a bidirectional stream.',
     '<a href="struct.DuplexStream.html"><code>DuplexStream</code></a> 结构体允许你从一个双向流中读写。'),

    # ===== io/struct.Empty.html =====
    ('The <a href="struct.Empty.html"><code>Empty</code></a> struct allows you to create an empty reader.',
     '<a href="struct.Empty.html"><code>Empty</code></a> 结构体允许你创建一个空读取器。'),

    # ===== io/struct.Repeat.html =====
    ('The <a href="struct.Repeat.html"><code>Repeat</code></a> struct allows you to create a reader that repeats a single byte value infinitely.',
     '<a href="struct.Repeat.html"><code>Repeat</code></a> 结构体允许你创建一个无限重复单个字节值的读取器。'),

    # ===== io/struct.SimplexStream.html =====
    ('Creates unidirectional buffer that acts like in memory pipe. To create\nsplit version with separate reader and writer you can use simplex\nfunction. The <code>max_buf_size</code> argument is the maximum amount of bytes\nthat can be stored in the buffer.',
     '创建一个像内存管道一样的单向缓冲。若要创建读写分离的拆分版本，可使用 simplex 函数。<code>max_buf_size</code> 参数是缓冲能存储的最大字节数。'),
    ('Creates unidirectional buffer that acts like in memory pipe. To create\nsplit version with separate reader and writer you can use simplex\nfunction. The max_buf_size argument is the maximum amount of bytes\nthat can be stored in the buffer.',
     '创建一个像内存管道一样的单向缓冲。若要创建读写分离的拆分版本，可使用 simplex 函数。max_buf_size 参数是缓冲能存储的最大字节数。'),

    # ===== io/struct.Sink.html =====
    ('The <a href="struct.Sink.html"><code>Sink</code></a> struct allows you to write a stream of values.', '<a href="struct.Sink.html"><code>Sink</code></a> 结构体允许你写一个值流。'),

    # ===== io/struct.Split.html =====
    ('The <a href="struct.Split.html"><code>Split</code></a> struct allows you to split a bidirectional stream into separate read and write halves.',
     '<a href="struct.Split.html"><code>Split</code></a> 结构体允许你将一个双向流拆分为独立的读、写两半。'),

    # ===== io/struct.Stdin.html =====
    ('This handle is best used for non-interactive uses, such as when a file\nis piped into the application. For technical reasons, <code>stdin</code> is\nimplemented by using an ordinary blocking read on a separate thread, so\nit can be used in combination with any other runtime features.',
     '此 handle 最适合非交互场景，例如将文件通过管道输入应用。出于技术原因，<code>stdin</code> 通过一个单独的线程上的普通阻塞读取实现，因此可以与任何其他运行时特性结合使用。'),
    ('This handle is best used for non-interactive uses, such as when a file\nis piped into the application. For technical reasons, <code>stdin</code> is\nimplemented by using an asynchronous background thread to read from the\nstandard input, allowing it to yield to other tasks while waiting for\ninput, but this may behave subtly different from blocking I/O.',
     '此 handle 最适合非交互场景，例如将文件通过管道输入应用。出于技术原因，<code>stdin</code> 通过一个异步后台线程从标准输入读取，允许在等待输入时让出给其他任务，但其行为可能与阻塞 I/O 有细微差异。'),
    ('For interactive uses, it is recommended to spawn a thread dedicated to\nuser input and use blocking IO directly in that thread.',
     '对于交互场景，建议派生一个专用于用户输入的线程，并在该线程中直接使用阻塞 IO。'),
    ('Reads a line from standard input.', '从标准输入读取一行。'),
    ('The line does not include the trailing newline character.', '读取的行不包含末尾的换行符。'),

    # ===== io/struct.Stdout.html / Stderr.html =====
    ('Concurrent writes to stdout must be executed with care: Only individual\nwrites to this <code>AsyncWrite</code> are guaranteed to be intact. In particular\nyou should be aware that writes using <code>write_all</code> are not guaranteed\nto be atomic. Concurrent writes using <code>write</code> might result in\npartial writes.',
     '对 stdout 的并发写入必须谨慎执行：只有向此 <code>AsyncWrite</code> 的单个写入才保证是完整的。特别要注意，使用 <code>write_all</code> 的写入不保证原子性；并发使用 <code>write</code> 写入可能导致部分写入。'),
    ('Concurrent writes to stderr must be executed with care: Only individual\nwrites to this <code>AsyncWrite</code> are guaranteed to be intact. In particular\nyou should be aware that writes using <code>write_all</code> are not guaranteed\nto be atomic. Concurrent writes using <code>write</code> might result in\npartial writes.',
     '对 stderr 的并发写入必须谨慎执行：只有向此 <code>AsyncWrite</code> 的单个写入才保证是完整的。特别要注意，使用 <code>write_all</code> 的写入不保证原子性；并发使用 <code>write</code> 写入可能导致部分写入。'),
    ('Concurrent writes to stdout must be executed with care: Only individual\nwrites to this <code>AsyncWrite</code> are guaranteed to be intact. In particular\nyou should be aware that a concurrent write may observe only part of a\nbuffer if it is not written atomically.',
     '对 stdout 的并发写入必须谨慎执行：只有向此 <code>AsyncWrite</code> 的单个写入才保证是完整的。特别要注意，如果写入不是原子的，并发写入可能只能看到缓冲区的一部分。'),

    # ===== io/struct.ReadHalf.html / WriteHalf.html =====
    ('Checks if this <code>ReadHalf</code> and some <code>WriteHalf</code> were split from the same stream.',
     '检查此 <code>ReadHalf</code> 与某个 <code>WriteHalf</code> 是否是从同一个流拆分而来。'),
    ('Checks if this <code>WriteHalf</code> and some <code>ReadHalf</code> were split from the same stream.',
     '检查此 <code>WriteHalf</code> 与某个 <code>ReadHalf</code> 是否是从同一个流拆分而来。'),
    ('Reunites with a previously split <code>WriteHalf</code>.',
     '与之前拆分的 <code>WriteHalf</code> 重新合并。'),
    ('If this <code>ReadHalf</code> and the given <code>WriteHalf</code> do not originate from the same split operation this method will panic. This can be checked ahead of time with the <code>peer_addr</code> method.',
     '若此 <code>ReadHalf</code> 与给定的 <code>WriteHalf</code> 不是来自同一次拆分操作，此方法将 panic。可通过 <code>peer_addr</code> 方法预先检查。'),

    # ===== io/trait.AsyncBufReadExt.html / AsyncSeekExt.html =====
    ('Asynchronously reads bytes from a source.', '从源异步读取字节。'),
    ('Implemented as an extension trait, adding utility methods to all\n<a href="trait.AsyncBufRead.html" title="trait tokio::io::AsyncBufRead"><code>AsyncBufRead</code></a> types.',
     '作为扩展特性实现，向所有 <a href="trait.AsyncBufRead.html" title="trait tokio::io::AsyncBufRead"><code>AsyncBufRead</code></a> 类型添加工具方法。'),
    ('Asynchronously seeks to a position in a stream.', '在流中异步定位到指定位置。'),
    ('Implemented as an extension trait, adding utility methods to all\n<a href="trait.AsyncSeek.html" title="trait tokio::io::AsyncSeek"><code>AsyncSeek</code></a> types.',
     '作为扩展特性实现，向所有 <a href="trait.AsyncSeek.html" title="trait tokio::io::AsyncSeek"><code>AsyncSeek</code></a> 类型添加工具方法。'),

    # ===== io/fn.copy.html / copy_bidirectional.html / copy_buf.html =====
    ('Asynchronously copies the entire contents of a reader into a writer.', '异步将一个读取器的全部内容复制到写入器。'),
    ('This function returns a future that will continuously read data from\n<code>reader</code> and then write it into <code>writer</code> in a streaming fashion until\n<code>reader</code> returns EOF.',
     '此函数返回一个 Future，它会持续从 <code>reader</code> 读取数据，然后以流式方式写入 <code>writer</code>，直到 <code>reader</code> 返回 EOF。'),
    ('This function returns a future that will continuously read data from\nreader and then write it into writer in a streaming fashion until\nreader returns EOF or fails.',
     '此函数返回一个 Future，它会持续从 reader 读取数据，然后以流式方式写入 writer，直到 reader 返回 EOF 或出错。'),
    ('On success, the total number of bytes that were copied from <code>reader</code> to\n<code>writer</code> is returned.',
     '成功时返回从 <code>reader</code> 复制到 <code>writer</code> 的总字节数。'),
    ('On success, the total number of bytes that were copied from reader to\nwriter is returned.',
     '成功时返回从 reader 复制到 writer 的总字节数。'),
    ('A copy of bytes is currently buffered inside the function. To improve\nperformance, this buffer may be larger than the amount of data needed to\nfill <code>writer</code>\'s capacity. So if <code>writer</code> writes slowly, the buffer may grow\nunbounded.',
     '字节副本当前在函数内部缓冲。为提升性能，该缓冲可能大于填满 <code>writer</code> 容量所需的数据量。因此，若 <code>writer</code> 写入较慢，缓冲可能无界增长。'),
    ('This is an asynchronous version of <a href="https://doc.rust-lang.org/1.95.0/std/io/fn.copy.html" title="fn std::io::copy"><code>std::io::copy</code></a>.',
     '这是 <a href="https://doc.rust-lang.org/1.95.0/std/io/fn.copy.html" title="fn std::io::copy"><code>std::io::copy</code></a> 的异步版本。'),
    ('The <code>reader</code> and <code>writer</code> are copied until EOF is reached on <code>reader</code>, or an\nerror occurs.',
     '持续复制 <code>reader</code> 与 <code>writer</code>，直到 <code>reader</code> 到达 EOF 或发生错误。'),

    # ===== io/fn.empty.html / repeat.html / simplex.html / sink.html =====
    ('This is an asynchronous version of <a href="https://doc.rust-lang.org/1.95.0/std/io/struct.Empty.html" title="struct std::io::Empty"><code>std::io::Empty</code></a>.',
     '这是 <a href="https://doc.rust-lang.org/1.95.0/std/io/struct.Empty.html" title="struct std::io::Empty"><code>std::io::Empty</code></a> 的异步版本。'),
    ('This is an asynchronous version of <a href="https://doc.rust-lang.org/1.95.0/std/io/struct.Repeat.html" title="struct std::io::Repeat"><code>std::io::Repeat</code></a>.',
     '这是 <a href="https://doc.rust-lang.org/1.95.0/std/io/struct.Repeat.html" title="struct std::io::Repeat"><code>std::io::Repeat</code></a> 的异步版本。'),
    ('Creates a bidirectional in-memory pipe backed by a buffer of size\n<code>max_buf_size</code>. Reads/writes from the returned <code>ReadHalf</code>/<code>WriteHalf</code>\nwill be buffered.',
     '创建一个由大小为 <code>max_buf_size</code> 的缓冲支持的双向内存管道。从返回的 <code>ReadHalf</code>/<code>WriteHalf</code> 进行的读写都会被缓冲。'),
    ('Creating a unidirectional buffer that acts like an in-memory pipe. To\ncreate a split version with separate reader and writer you can use\nsimplex function.',
     '创建一个像内存管道一样的单向缓冲。要创建读写分离的拆分版本，请使用 simplex 函数。'),

    # ===== io/fn.stderr.html / stdout.html / stdin.html =====
    ('The <a href="https://doc.rust-lang.org/1.95.0/std/io/struct.Stderr.html" title="struct std::io::Stderr"><code>std::io::Stderr</code></a> type as an <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a>.',
     '<a href="https://doc.rust-lang.org/1.95.0/std/io/struct.Stderr.html" title="struct std::io::Stderr"><code>std::io::Stderr</code></a> 类型作为 <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a>。'),
    ('The <a href="https://doc.rust-lang.org/1.95.0/std/io/struct.Stdout.html" title="struct std::io::Stdout"><code>std::io::Stdout</code></a> type as an <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a>.',
     '<a href="https://doc.rust-lang.org/1.95.0/std/io/struct.Stdout.html" title="struct std::io::Stdout"><code>std::io::Stdout</code></a> 类型作为 <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a>。'),
    ('The <a href="https://doc.rust-lang.org/1.95.0/std/io/struct.Stdin.html" title="struct std::io::Stdin"><code>std::io::Stdin</code></a> type as an <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a>.',
     '<a href="https://doc.rust-lang.org/1.95.0/std/io/struct.Stdin.html" title="struct std::io::Stdin"><code>std::io::Stdin</code></a> 类型作为 <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a>。'),
    ('Reads a line from stdin.', '从 stdin 读取一行。'),

    # ===== fs/ =====
    ('Returns the canonical, absolute form of a path with all intermediate\ncomponents normalized and symbolic links resolved.',
     '返回路径的规范化绝对形式，所有中间组件均被规范化，且符号链接被解析。'),
    ('This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.canonicalize.html" title="fn std::fs::canonicalize"><code>std::fs::canonicalize</code></a>.',
     '这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.canonicalize.html" title="fn std::fs::canonicalize"><code>std::fs::canonicalize</code></a> 的异步版本。'),
    ('This function currently corresponds to the <code>realpath</code> function on Unix\nand the <code>CreateFile</code> and <code>GetFinalPathNameByHandle</code> functions on Windows.\nNote that, this may change in the future.',
     '此函数目前对应于 Unix 上的 <code>realpath</code> 与 Windows 上的 <code>CreateFile</code> 和 <code>GetFinalPathNameByHandle</code>。未来可能发生变化。'),
    ('On Windows, this converts the path to use extended length path syntax,\nwhich allows your program to use longer path names, but means you can only\njoin Windows paths to other Windows paths, and you cannot use extended\nlength path names with relative paths.',
     '在 Windows 上，这会将路径转换为扩展长度路径语法，允许程序使用更长的路径名，但意味着你只能将 Windows 路径与其他 Windows 路径拼接，且不能在相对路径中使用扩展长度路径名。'),
    ('Copies the contents of one file to another. This function will also\ncopy the permission bits of the original file to the destination file.',
     '将一个文件的内容复制到另一个文件。此函数还会将原始文件的权限位复制到目标文件。'),
    ('This function will also copy the permission bits of the original file\nto the destination file.',
     '此函数还会将原始文件的权限位复制到目标文件。'),
    ('This is the async equivalent of <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.copy.html" title="fn std::fs::copy"><code>std::fs::copy</code></a>.',
     '这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.copy.html" title="fn std::fs::copy"><code>std::fs::copy</code></a> 的异步等效版本。'),
    ('On success, the total number of bytes copied is returned and it is\nequal to the length of the <code>to</code> file.',
     '成功时返回复制的总字节数，等于 <code>to</code> 文件的长度。'),
    ('Creates a new, empty directory at the provided path.', '在指定路径创建一个新的空目录。'),
    ('This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.create_dir.html" title="fn std::fs::create_dir"><code>std::fs::create_dir</code></a>.',
     '这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.create_dir.html" title="fn std::fs::create_dir"><code>std::fs::create_dir</code></a> 的异步版本。'),
    ('This function currently corresponds to the <code>mkdir</code> function on Unix\nand the <code>CreateDirectory</code> function on Windows.\nNote that, this may change in the future.',
     '此函数目前对应于 Unix 上的 <code>mkdir</code> 与 Windows 上的 <code>CreateDirectory</code>。未来可能发生变化。'),
    ('This function currently corresponds to the mkdir function on Unix\nand the CreateDirectory function on Windows.\nNote that, this may change in the future.',
     '此函数目前对应于 Unix 上的 mkdir 与 Windows 上的 CreateDirectory。未来可能发生变化。'),
    ('Recursively create a directory and all of its parent components if they\nare missing.', '递归创建目录及其所有缺失的父组件。'),
    ('This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.create_dir_all.html" title="fn std::fs::create_dir_all"><code>std::fs::create_dir_all</code></a>.',
     '这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.create_dir_all.html" title="fn std::fs::create_dir_all"><code>std::fs::create_dir_all</code></a> 的异步版本。'),
    ('Creates a new hard link on the filesystem.', '在文件系统上创建一个新的硬链接。'),
    ('The <code>dst</code> path will be a link pointing to the <code>original</code> path.',
     '<code>dst</code> 路径将成为指向 <code>original</code> 路径的链接。'),
    ('This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.hard_link.html" title="fn std::fs::hard_link"><code>std::fs::hard_link</code></a>.',
     '这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.hard_link.html" title="fn std::fs::hard_link"><code>std::fs::hard_link</code></a> 的异步版本。'),
    ('Returns the metadata for a file or directory.', '返回文件或目录的元数据。'),
    ('This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.metadata.html" title="fn std::fs::metadata"><code>std::fs::metadata</code></a>.',
     '这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.metadata.html" title="fn std::fs::metadata"><code>std::fs::metadata</code></a> 的异步版本。'),
    ('Asynchronously read the entire contents of a file into a bytes vector.', '异步将文件的全部内容读入字节向量。'),
    ('This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.read.html" title="fn std::fs::read"><code>std::fs::read</code></a>.',
     '这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.read.html" title="fn std::fs::read"><code>std::fs::read</code></a> 的异步版本。'),
    ('Returns a future of <a href="https://doc.rust-lang.org/1.95.0/std/io/error/type.Result.html" title="type std::io::error::Result"><code>Result</code></a>. On success, contains the file contents as a bytes vector. This\nfunction is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.read.html" title="fn std::fs::read"><code>std::fs::read</code></a>.',
     '返回 <a href="https://doc.rust-lang.org/1.95.0/std/io/error/type.Result.html" title="type std::io::error::Result"><code>Result</code></a> 的 Future。成功时包含以字节向量表示的文件内容。此函数是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.read.html" title="fn std::fs::read"><code>std::fs::read</code></a> 的异步版本。'),
    ('Returns a future of <a href="https://doc.rust-lang.org/1.95.0/std/io/error/type.Result.html" title="type std::io::error::Result"><code>Result</code></a>. On success, contains the file contents as a string. This\nfunction is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.read_to_string.html" title="fn std::fs::read_to_string"><code>std::fs::read_to_string</code></a>.',
     '返回 <a href="https://doc.rust-lang.org/1.95.0/std/io/error/type.Result.html" title="type std::io::error::Result"><code>Result</code></a> 的 Future。成功时包含以字符串表示的文件内容。此函数是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.read_to_string.html" title="fn std::fs::read_to_string"><code>std::fs::read_to_string</code></a> 的异步版本。'),
    ('Returns a future of <code>Option</code>. <code>Some</code> when the path exists, <code>None</code> when it does not.', '返回 <code>Option</code> 的 Future。路径存在时为 <code>Some</code>，不存在时为 <code>None</code>。'),
    ('This function currently corresponds to the <code>remove</code> function on Unix\nand the <code>DeleteFile</code> and <code>RemoveDirectory</code> functions on Windows.\nNote that, this may change in the future.',
     '此函数目前对应于 Unix 上的 <code>remove</code> 与 Windows 上的 <code>DeleteFile</code> 和 <code>RemoveDirectory</code>。未来可能发生变化。'),
    ('Removes a file from the filesystem.', '从文件系统删除一个文件。'),
    ('Removes a directory at the provided path.', '删除指定路径的目录。'),
    ('Removes a directory at this path, after removing all its contents.', '递归删除该路径的目录及其全部内容。'),
    ('Renames a file or directory to a new name, replacing the original file\nif <code>to</code> already exists.',
     '将文件或目录重命名为新名称；若 <code>to</code> 已存在则覆盖。'),
    ('This will not work if the new name is on a different mount point.', '若新名称在不同的挂载点上，此操作将失败。'),
    ('Changes the permissions of a file or directory.', '修改文件或目录的权限。'),
    ('Creates a new symbolic link on the filesystem.', '在文件系统上创建一个新的符号链接。'),
    ('The <code>dst</code> path will be a symbolic link pointing to the <code>original</code> path.',
     '<code>dst</code> 路径将成为指向 <code>original</code> 路径的符号链接。'),
    ('Asynchronously write the entire contents of a buffer to a file.', '异步将缓冲的全部内容写入文件。'),
    ('This function will create a file if it does not exist, and will entirely\nreplace its contents if it does.',
     '若文件不存在，此函数将创建该文件；若已存在，则完全替换其内容。'),
    ('Asynchronously reads the directory at the given path and yields\n<a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.DirEntry.html" title="struct std::fs::DirEntry"><code>DirEntry</code></a> values.',
     '异步读取指定路径的目录并产出 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.DirEntry.html" title="struct std::fs::DirEntry"><code>DirEntry</code></a> 值。'),
    ('Reads a symbolic link, returning the file that the link points to.', '读取符号链接，返回链接指向的文件。'),
    ('Returns a future of <code>Option</code>. On success, <code>Some</code> with the directory\nentries iterator. <code>None</code> if the directory does not exist.',
     '返回 <code>Option</code> 的 Future。成功时为 <code>Some</code>，包含目录条目迭代器；若目录不存在则为 <code>None</code>。'),
    ('This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.read_dir.html" title="fn std::fs::read_dir"><code>std::fs::read_dir</code></a>.',
     '这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.read_dir.html" title="fn std::fs::read_dir"><code>std::fs::read_dir</code></a> 的异步版本。'),
    ('This function is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.read_link.html" title="fn std::fs::read_link"><code>std::fs::read_link</code></a>.',
     '此函数是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.read_link.html" title="fn std::fs::read_link"><code>std::fs::read_link</code></a> 的异步版本。'),

    # ===== fs/struct.File.html =====
    ('Reference to the inner file.', '内部文件的引用。'),
    ('Mutable reference to the inner file.', '内部文件的可变引用。'),
    ('Pinned mutable reference to the inner file.', '内部文件的 pinned 可变引用。'),
    ('Attempts to sync all OS-internal metadata to disk.', '尝试将所有操作系统内部元数据同步到磁盘。'),
    ('This function will attempt to ensure that all in-memory data reaches the\nfilesystem before returning.',
     '此函数将尝试确保所有内存数据在返回前已到达文件系统。'),
    ('This function currently corresponds to the <code>fsync</code> function on Unix\nand the <code>FlushFileBuffers</code> function on Windows.',
     '此函数目前对应于 Unix 上的 <code>fsync</code> 与 Windows 上的 <code>FlushFileBuffers</code>。'),
    ('Get the maximum buffer size for the underlying <code>AsyncRead</code>/<code>AsyncWrite</code> operation.',
     '获取底层 <code>AsyncRead</code>/<code>AsyncWrite</code> 操作的最大缓冲大小。'),

    # ===== fs/struct.OpenOptions.html =====
    ('Options and flags which can be used to configure how a file is opened.', '用于配置文件打开方式的可选项与标志。'),
    ('Creates a blank new set of options ready for configuration.', '创建一组待配置的空白选项。'),
    ('Sets the option for read-access.', '设置读访问选项。'),
    ('Sets the option for write-access.', '设置写访问选项。'),
    ('Sets the option for the append mode.', '设置追加模式选项。'),
    ('Sets the option for truncating an existing file to zero length.', '设置将现有文件截断为零长度的选项。'),

    # ===== fs/struct.ReadDir.html =====
    ('The <a href="struct.ReadDir.html"><code>ReadDir</code></a> struct is returned by <code>read_dir</code> and allows you to iterate\nover the entries in a directory.',
     '<a href="struct.ReadDir.html"><code>ReadDir</code></a> 结构体由 <code>read_dir</code> 返回，允许你迭代目录中的条目。'),
    ('Returns the next entry in the directory stream.', '返回目录流中的下一个条目。'),
    ('Cancel safety: This method is cancellation safe.', '取消安全性：此方法是取消安全的。'),
    ('Polls for the next directory entry in the stream.', '轮询流中的下一个目录条目。'),
    ('This method returns:', '此方法返回：'),
    ('* <code>Poll::Pending</code> if the next directory entry is not yet available.', '* 若下一个目录条目尚未就绪，返回 <code>Poll::Pending</code>。'),
    ('* <code>Poll::Ready(Ok(Some(entry)))</code> if the next directory entry is available.', '* 若下一个目录条目可用，返回 <code>Poll::Ready(Ok(Some(entry)))</code>。'),
    ('* <code>Poll::Ready(Ok(None))</code> if there are no more directory entries in this\nstream.', '* 若此流中再无更多目录条目，返回 <code>Poll::Ready(Ok(None))</code>。'),
    ('* <code>Poll::Ready(Err(error))</code> if an error occurred while reading the next\ndirectory entry.', '* 若读取下一个目录条目时发生错误，返回 <code>Poll::Ready(Err(error))</code>。'),

    # ===== fs/struct.DirEntry.html =====
    ('Entries returned by the <code>read_dir</code> function.', '由 <code>read_dir</code> 函数返回的条目。'),
    ('Returns the full path to the file that this entry represents.', '返回此条目所代表的文件的完整路径。'),

    # ===== fs/struct.DirBuilder.html =====
    ('Options and flags which can be used to configure how a directory is\ncreated.', '用于配置目录创建方式的可选项与标志。'),
    ('Creates a new set of options from an existing value.', '基于现有值创建一组新的选项。'),

    # ===== fs/index.html =====
    ('Asynchronous filesystem operations.', '异步文件系统操作。'),
    ('If you want to use the synchronous version of these functions, use the\n<code>std::fs</code> module.', '若要使用这些函数的同步版本，请使用 <code>std::fs</code> 模块。'),
    ('This module is only available when the <code>fs</code> feature is enabled.', '此模块仅在启用 <code>fs</code> 特性时可用。'),
    ('Some of the functions in this module are <code>async</code> versions of the\nfunctions in <code>std::fs</code>.',
     '此模块中部分函数是 <code>std::fs</code> 中函数的 <code>async</code> 版本。'),

    # ===== process/struct.Child.html =====
    ('The <a href="struct.Child.html"><code>Child</code></a> struct allows you to interact with a child process.',
     '<a href="struct.Child.html"><code>Child</code></a> 结构体允许你与子进程交互。'),
    ('Returns the OS-assigned process identifier associated with this child.', '返回与此子进程关联的、由操作系统分配的进程标识符。'),
    ('A detailed listing of all functions in this trait can be found in the\n<a href="https://doc.rust-lang.org/1.95.0/std/process/struct.Child.html" title="struct std::process::Child">standard library documentation</a>.',
     '本特性所有函数的详细列表可在 <a href="https://doc.rust-lang.org/1.95.0/std/process/struct.Child.html" title="struct std::process::Child">标准库文档</a> 中找到。'),
    ('For this method to be useful, the <code>Child</code> needs to be configured with\n<code>Command::stdout</code>(<code>Stdio::piped</code>()).',
     '要使此方法有用，<code>Child</code> 需要使用 <code>Command::stdout</code>(<code>Stdio::piped</code>()) 进行配置。'),
    ('For this method to be useful, the <code>Child</code> needs to be configured with\n<code>Command::stderr</code>(<code>Stdio::piped</code>()).',
     '要使此方法有用，<code>Child</code> 需要使用 <code>Command::stderr</code>(<code>Stdio::piped</code>()) 进行配置。'),
    ('For this method to be useful, the <code>Child</code> needs to be configured with\n<code>Command::stdin</code>(<code>Stdio::piped</code>()).',
     '要使此方法有用，<code>Child</code> 需要使用 <code>Command::stdin</code>(<code>Stdio::piped</code>()) 进行配置。'),
    ('A handle to the process\'s standard input.', '进程标准输入的 handle。'),
    ('A handle to the process\'s standard error output.', '进程标准错误输出的 handle。'),
    ('A handle to the process\'s standard output.', '进程标准输出的 handle。'),

    # ===== process/struct.ChildStderr/Stdout/Stdin.html =====
    ('The standard input stream of a child process.', '子进程的标准输入流。'),
    ('The standard output stream of a child process.', '子进程的标准输出流。'),
    ('The standard error stream of a child process.', '子进程的标准错误流。'),

    # ===== process/struct.Command.html =====
    ('This structure mimics the API of <code>std::process::Command</code> found in the standard library, but replaces functions that create a process with\nasynchronous equivalents.',
     '此结构体模仿标准库中的 <code>std::process::Command</code> 的 API，但将创建进程的函数替换为其异步等价物。'),
    ('Cheaply convert to a <code>&amp;std::process::Command</code> for places where the type\nfrom the standard library is expected.',
     '在期望标准库类型的位置，可廉价地转换为 <code>&amp;std::process::Command</code>。'),
    ('Cheaply convert to a <code>&amp;mut std::process::Command</code> for places where the\ntype from the standard library is expected.',
     '在期望标准库类型的位置，可廉价地转换为 <code>&amp;mut std::process::Command</code>。'),
    ('Creates a new <code>Command</code> from <code>std::process::Command</code>.',
     '从 <code>std::process::Command</code> 创建一个新的 <code>Command</code>。'),
    ('Creates a new <code>Command</code> from <code>std::process::Command</code>. Other fields are\ninitialized to their default values.',
     '从 <code>std::process::Command</code> 创建一个新的 <code>Command</code>。其他字段初始化为其默认值。'),
    ('Sets the program to be executed when this <code>Command</code> is run.', '设置当此 <code>Command</code> 运行时要执行的程序。'),
    ('Adds an argument to pass to the program.', '添加传递给程序的参数。'),
    ('Adds multiple arguments to pass to the program.', '添加多个传递给程序的参数。'),
    ('Inserts or updates an explicit environment variable mapping.', '插入或更新一个显式的环境变量映射。'),
    ('Removes an explicit environment variable mapping.', '删除一个显式的环境变量映射。'),

    # ===== process/index.html =====
    ('Asynchronous process management.', '异步进程管理。'),
    ('This module is only available when the <code>process</code> feature is enabled.', '此模块仅在启用 <code>process</code> 特性时可用。'),
    ('This crate provides a <a href="struct.Command.html"><code>Command</code></a> type which is a wrapper around <a href="https://doc.rust-lang.org/1.95.0/std/process/struct.Command.html" title="struct std::process::Command"><code>std::process::Command</code></a>.',
     '本 crate 提供 <a href="struct.Command.html"><code>Command</code></a> 类型，是对 <a href="https://doc.rust-lang.org/1.95.0/std/process/struct.Command.html" title="struct std::process::Command"><code>std::process::Command</code></a> 的包装。'),

    # ===== signal/ =====
    ('Asynchronous signal handling.', '异步信号处理。'),
    ('This module is only available when the <code>signal</code> feature is enabled.', '此模块仅在启用 <code>signal</code> 特性时可用。'),
    ('This crate provides async wrappers around <a href="https://doc.rust-lang.org/1.95.0/std/sync/struct.Once.html" title="struct std::sync::Once"><code>std::sync::Once</code></a>, a way to\nrun global initialization code exactly once across all threads in a\nprogram.',
     '本 crate 提供 <a href="https://doc.rust-lang.org/1.95.0/std/sync/struct.Once.html" title="struct std::sync::Once"><code>std::sync::Once</code></a> 的异步包装，用于在整个程序的多个线程中仅执行一次全局初始化代码。'),
    ('A notification to this process notifies all listeners listening for\nthis event. Moreover, the notifications are coalesced if they aren\'t\nprocessed quickly enough. This means that if two notifications are received\nbefore the first one is processed, the second one will be ignored.',
     '通知此进程将通知所有正在监听此事件的监听器。此外，若通知未能及时处理，通知会被合并。这意味着若在第一个通知处理完之前收到第二个通知，第二个通知将被忽略。'),
    ('A notification to this process notifies all receivers for\nthis event. Moreover, the notifications are coalesced if they aren\'t\nprocessed quickly enough. This means that if two notifications are received\nbefore the first one is processed, the second one will be ignored.',
     '通知此进程将通知此事件的所有接收者。此外，若通知未能快速处理，通知会被合并。这意味着若在第一个通知处理完之前收到第二个通知，第二个通知将被忽略。'),
    ('Completes when a "ctrl-c" notification has been received.', '当收到 "ctrl-c" 通知时完成。'),
    ('Creates a future that completes when a "ctrl-c" notification is received.',
     '创建一个在收到 "ctrl-c" 通知时完成的 Future。'),
    ('Use this function to listen for ctrl-c notifications sent to the\nprocess.', '使用此函数监听发送给进程的 ctrl-c 通知。'),
    ('Representing a listener which receives "ctrl-c" notifications sent to the\nprocess via <code>SetConsoleCtrlHandler</code>. The notifications are\ncoalesced if they are not processed quickly enough.',
     '表示一个监听器，它接收通过 <code>SetConsoleCtrlHandler</code> 发送给进程的 "ctrl-c" 通知。若通知未能快速处理，通知会被合并。'),
    ('The notifications are coalesced if they are not processed quickly\nenough.', '若通知未能快速处理，通知会被合并。'),

    # ===== signal/windows/ =====
    ('Windows-specific signal handling.', 'Windows 特有的信号处理。'),
    ('A listener which receives "ctrl-break" notifications sent to the\nprocess via <code>SetConsoleCtrlHandler</code>.',
     '一个监听器，接收通过 <code>SetConsoleCtrlHandler</code> 发送给进程的 "ctrl-break" 通知。'),
    ('A listener which receives "ctrl-c" notifications sent to the\nprocess via <code>SetConsoleCtrlHandler</code>.',
     '一个监听器，接收通过 <code>SetConsoleCtrlHandler</code> 发送给进程的 "ctrl-c" 通知。'),
    ('A listener which receives "ctrl-close" notifications sent to the\nprocess via <code>SetConsoleCtrlHandler</code>.',
     '一个监听器，接收通过 <code>SetConsoleCtrlHandler</code> 发送给进程的 "ctrl-close" 通知。'),
    ('A listener which receives "ctrl-logoff" notifications sent to the\nprocess via <code>SetConsoleCtrlHandler</code>.',
     '一个监听器，接收通过 <code>SetConsoleCtrlHandler</code> 发送给进程的 "ctrl-logoff" 通知。'),
    ('A listener which receives "ctrl-shutdown" notifications sent to the\nprocess via <code>SetConsoleCtrlHandler</code>.',
     '一个监听器，接收通过 <code>SetConsoleCtrlHandler</code> 发送给进程的 "ctrl-shutdown" 通知。'),
    ('Completes when a "ctrl-break" notification has been received.', '当收到 "ctrl-break" 通知时完成。'),
    ('Completes when a "ctrl-c" notification has been received.', '当收到 "ctrl-c" 通知时完成。'),
    ('Completes when a "ctrl-close" notification has been received.', '当收到 "ctrl-close" 通知时完成。'),
    ('Completes when a "ctrl-logoff" notification has been received.', '当收到 "ctrl-logoff" 通知时完成。'),
    ('Completes when a "ctrl-shutdown" notification has been received.', '当收到 "ctrl-shutdown" 通知时完成。'),

    # ===== task/blocking/fn.block_in_place.html =====
    ('This operation is implemented by running the equivalent blocking\noperation on a separate thread pool using <a href="../fn.spawn_blocking.html" title="fn tokio::spawn_blocking"><code>spawn_blocking</code></a>.',
     '此操作通过使用 <a href="../fn.spawn_blocking.html" title="fn tokio::spawn_blocking"><code>spawn_blocking</code></a> 在单独的线程池上运行等效的阻塞操作来实现。'),
    ('This operation is implemented by running the equivalent blocking operation\non a separate thread pool using <a href="../fn.spawn_blocking.html" title="fn tokio::spawn_blocking"><code>spawn_blocking</code></a>.',
     '此操作通过使用 <a href="../fn.spawn_blocking.html" title="fn tokio::spawn_blocking"><code>spawn_blocking</code></a> 在单独的线程池上运行等效的阻塞操作来实现。'),
    ('In general, using this method should be avoided.', '通常应避免使用此方法。'),
    ('It is important to keep in mind that this function is not guaranteed to\nbehave the same way as the underlying blocking operation.',
     '请务必注意，此函数的行为不一定与底层阻塞操作完全一致。'),
    ('For example, calling this function on a thread pool thread will not\nsaturate it, as the blocking operation would.',
     '例如，在线程池线程上调用此函数不会像阻塞操作那样饱和线程池。'),

    # ===== io/fn.split.html / io/fn.join.html =====
    ('Splits a stream into separate read and write halves.', '将一个流拆分为独立的读、写两半。'),
    ('Joins two streams into one, returning a duplex stream.', '将两个流合并为一个，返回一个双工流。'),

    # ===== io/fn.copy_bidirectional.html / copy_bidirectional_with_sizes.html =====
    ('Copies data in both directions between <code>a</code> and <code>b</code>.', '在 <code>a</code> 与 <code>b</code> 之间双向复制数据。'),
    ('Asynchronously copies data between two streams, in both directions.', '在两个流之间双向异步复制数据。'),
    ('Returns a future that resolves when copying in either direction\nfinishes.', '返回一个 Future，当任一方向的复制完成时解析。'),
    ('If an error occurs during the copy in either direction, the future\nresolves to that error.', '若任一方向的复制过程中出错，Future 解析为该错误。'),

    # ===== io/fn.copy_buf.html =====
    ('Copies data from <code>reader</code> into <code>buf</code> until <code>reader</code> reaches EOF.', '将数据从 <code>reader</code> 复制到 <code>buf</code>，直到 <code>reader</code> 到达 EOF。'),
    ('On success, the number of bytes copied is returned.', '成功时返回已复制的字节数。'),

    # ===== task/fn.block_in_place.html =====
    ('Informs the executor that the current task is about to block the\ncurrent thread, allowing the executor to schedule another task on the\ncurrent thread.',
     '通知执行器当前任务即将阻塞当前线程，允许执行器在当前线程上调度另一个任务。'),
    ('When a future in the current task blocks the current thread using a\nsynchronous I/O function or other blocking operation, the executor\nschedules another task to continue running on the current thread.',
     '当当前任务中的 Future 使用同步 I/O 函数或其他阻塞操作阻塞当前线程时，执行器会调度另一个任务以继续在当前线程上运行。'),
    ('In other words, the executor can multiplex tasks on the current thread\nwhen one task blocks.',
     '换言之，当某个任务阻塞时，执行器可以在当前线程上多路复用任务。'),
    ('The <code>block_in_place</code> function is used to indicate that the current\ntask is about to block the current thread.',
     '<code>block_in_place</code> 函数用于指示当前任务即将阻塞当前线程。'),

    # ===== Other method descriptions =====
    ('Obtains a reference to the underlying reader.', '获取底层读取器的引用。'),
    ('Obtains a mutable reference to the underlying reader.', '获取底层读取器的可变引用。'),
]


def to_bytes(s):
    """Convert string to bytes, handling CRLF: replace \n with \r\n if needed."""
    b = s.encode('utf-8')
    return b


def main():
    # Convert all pairs to bytes
    pairs_b = []
    for en, zh in TRAIT_PAIRS:
        en_b = en.encode('utf-8')
        zh_b = zh.encode('utf-8')
        pairs_b.append((en_b, zh_b))

    total_files = 0
    total_replacements = 0
    files_changed = 0

    for root, dirs, files in os.walk(BASE):
        for f in files:
            if not f.endswith('.html'):
                continue
            p = os.path.join(root, f)
            with open(p, 'rb') as fh:
                c = fh.read()
            original = c
            local = 0

            for en_b, zh_b in pairs_b:
                # Try LF version
                if en_b in c:
                    occurrences = c.count(en_b)
                    c = c.replace(en_b, zh_b)
                    local += occurrences
                # Also try CRLF version
                en_crlf = en_b.replace(b'\n', b'\r\n')
                zh_crlf = zh_b.replace(b'\n', b'\r\n')
                if en_crlf != en_b and en_crlf in c:
                    occurrences = c.count(en_crlf)
                    c = c.replace(en_crlf, zh_crlf)
                    local += occurrences

            if c != original:
                with open(p, 'wb') as fh:
                    fh.write(c)
                files_changed += 1
                total_replacements += local
            total_files += 1

    print(f'Translated {files_changed}/{total_files} files, {total_replacements} replacements')


if __name__ == '__main__':
    main()