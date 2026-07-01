#!/usr/bin/env python3
"""tokio 第八阶段：补译 rustdoc examples 标签（含 File/impl 链接 + <code>X</code>）。"""
import os

BASE = r'D:/Administrator/Documents/Code/rust_doc_all/tokio'

PAIRS = [
    # === Examples labels with File link ===
    ('<a href="../fs/struct.File.html" title="struct tokio::fs::File"><code>File</code></a>s implement <code>AsyncRead</code>:',
     '<a href="../fs/struct.File.html" title="struct tokio::fs::File"><code>File</code></a> 实现 <code>AsyncRead</code>：'),
    ('<a href="../fs/struct.File.html" title="struct tokio::fs::File"><code>File</code></a>s implement <code>Read</code>:',
     '<a href="../fs/struct.File.html" title="struct tokio::fs::File"><code>File</code></a> 实现 <code>Read</code>：'),
    ('<a href="../fs/struct.File.html" title="struct tokio::fs::File"><code>File</code></a> implements <code>Read</code> and <a href="../../bytes/bytes_mut/struct.BytesMut.html" title="struct bytes::bytes_mut::BytesMut"><code>BytesMut</code></a> implements <code>BufMut</code>:',
     '<a href="../fs/struct.File.html" title="struct tokio::fs::File"><code>File</code></a> 实现 <code>Read</code>，<a href="../../bytes/bytes_mut/struct.BytesMut.html" title="struct bytes::bytes_mut::BytesMut"><code>BytesMut</code></a> 实现 <code>BufMut</code>：'),
    ('<a href="../fs/struct.File.html" title="struct tokio::fs::File"><code>File</code></a>s implement <code>AsyncWrite</code>:',
     '<a href="../fs/struct.File.html" title="struct tokio::fs::File"><code>File</code></a> 实现 <code>AsyncWrite</code>：'),

    # === read_exact full ===
    ('If the operation encounters an "end of file" before completely\nfilling the buffer, it returns an error of the kind\n<code>ErrorKind::UnexpectedEof</code>. The contents of <code>buf</code> are unspecified\nin this case.',
     '若操作在完全填满缓冲之前遇到“文件结束”，则返回 <code>ErrorKind::UnexpectedEof</code> 类型的错误。这种情况下 <code>buf</code> 的内容是未指定的。'),
    ('If the operation encounters an "end of file" before completely\nfilling the buffer, it returns an error of the kind\nErrorKind::UnexpectedEof. The contents of buf are unspecified\nin this case.',
     '若操作在完全填满缓冲之前遇到“文件结束”，则返回 ErrorKind::UnexpectedEof 类型的错误。这种情况下 buf 的内容是未指定的。'),
    ('This method is not cancellation safe. If the method is used as the\nevent in a <code>tokio::select!</code> statement and some\nother branch completes first, then some data may already have been\nread into <code>buf</code>.',
     '此方法不是取消安全的。如果将此方法用作 <code>tokio::select!</code> 语句中的事件，并且其他某个分支先完成，则可能已读取了一些数据到 <code>buf</code> 中。'),
    ('This method is not cancellation safe. If the method is used as the event in a <code>tokio::select!</code> statement and some other branch completes first, then some data may already have been read into <code>buf</code>.',
     '此方法不是取消安全的。如果将此方法用作 <code>tokio::select!</code> 语句中的事件，并且其他某个分支先完成，则可能已读取了一些数据到 <code>buf</code> 中。'),

    # === read_uN cancel ===
    ('This method is not cancellation safe. If the method is used as the\nevent in a <code>tokio::select!</code> statement and some\nother branch completes first, then some data may be lost.',
     '此方法不是取消安全的。如果将此方法用作 <code>tokio::select!</code> 语句中的事件，并且其他某个分支先完成，则可能丢失一些数据。'),
    ('This method is not cancellation safe. If the method is used as the event in a <code>tokio::select!</code> statement and some other branch completes first, then some data may be lost.',
     '此方法不是取消安全的。如果将此方法用作 <code>tokio::select!</code> 语句中的事件，并且其他某个分支先完成，则可能丢失一些数据。'),

    # === read_uN returns same errors as ===
    ('This method returns the same errors as <code>AsyncReadExt::read_exact</code>.',
     '此方法返回与 <code>AsyncReadExt::read_exact</code> 相同的错误。'),
    ('This method returns the same errors as AsyncReadExt::read_exact.',
     '此方法返回与 AsyncReadExt::read_exact 相同的错误。'),

    # === process/struct.Command.html full pieces ===
    ('Append literal text to the command line without any quoting or escaping.',
     '向命令行追加字面文本，不进行任何引号或转义。'),
    ('This is useful for passing arguments to <code>cmd.exe /c</code>, which doesn’t follow\n<code>CommandLineToArgvW</code> escaping rules.',
     '这对于将参数传递给 <code>cmd.exe /c</code> 很有用，因为它不遵循 <code>CommandLineToArgvW</code> 的转义规则。'),
    ('This is useful for passing arguments to cmd.exe /c, which doesn’t follow CommandLineToArgvW escaping rules.',
     '这对于将参数传递给 cmd.exe /c 很有用，因为它不遵循 CommandLineToArgvW 的转义规则。'),
    ('This is useful for passing arguments to cmd.exe /c, which doesn’t follow\nCommandLineToArgvW escaping rules.',
     '这对于将参数传递给 cmd.exe /c 很有用，因为它不遵循 CommandLineToArgvW 的转义规则。'),
    ('Inserts or updates an explicit environment variable mapping.\nThis method allows you add an environment variable mapping to an\nenvironment for the child process, replacing any previous value for the\ncorresponding key. To control the environment of the child process\nwithout affecting the parent process, see <code>env_clear</code>.',
     '插入或更新一个显式的环境变量映射。\n此方法允许向子进程的环境添加一个环境变量映射，替换对应键的先前值。若要在不影响父进程的情况下控制子进程的环境，请参阅 <code>env_clear</code>。'),
    ('Removes an explicit environment variable mapping. To remove a\nmapping for a key which has not been previously set, this method has\nno effect.',
     '删除一个显式的环境变量映射。对于之前未设置的键，调用此方法无效。'),
    ('Sets the program to be executed when this <code>Command</code> is run.',
     '设置当此 <code>Command</code> 运行时要执行的程序。'),
    ('Sets the program to be executed when this Command is run.',
     '设置当此 Command 运行时要执行的程序。'),
    ('Adds an argument to pass to the program.', '添加传递给程序的参数。'),
    ('Adds multiple arguments to pass to the program.', '添加多个传递给程序的参数。'),
    ('Inserts or updates an explicit environment variable mapping.',
     '插入或更新一个显式的环境变量映射。'),
    ('Removes an explicit environment variable mapping.', '删除一个显式的环境变量映射。'),
    ('Only one argument can be passed per use. So instead of:', '每次调用只能传递一个参数。因此，请勿这样：'),
    ('To pass a single argument see <code>arg</code>.', '若要传递单个参数，请参阅 <code>arg</code>。'),
    ('To pass a single argument see arg.', '若要传递单个参数，请参阅 arg。'),
    ('To pass multiple arguments see <a href="struct.Command.html#method.args" title="method tokio::process::Command::args"><code>args</code></a>.',
     '若要传递多个参数，请参阅 <a href="struct.Command.html#method.args" title="method tokio::process::Command::args"><code>args</code></a>。'),
    ('To pass multiple arguments see args.', '若要传递多个参数，请参阅 args。'),

    # === fs/struct.OpenOptions.html full ===
    ('This option, when true, means that writes will append to a file instead\nof overwriting previous contents.  Note that setting <code>.write(true).append(true)</code> has the same effect as setting only <code>.append(true)</code>.',
     '当此选项为 true 时，表示写入将追加到文件末尾，而不是覆盖先前的内容。注意，设置 <code>.write(true).append(true)</code> 的效果与仅设置 <code>.append(true)</code> 相同。'),
    ('This option, when true, means that writes will append to a file instead\nof overwriting previous contents.  Note that setting .write(true).append(true) has the same effect as setting only .append(true).',
     '当此选项为 true 时，表示写入将追加到文件末尾，而不是覆盖先前的内容。注意，设置 .write(true).append(true) 的效果与仅设置 .append(true) 相同。'),
    ('This option is useful because there is a common situation, when running\nconfiguration scripts, where you want to create a file or do nothing if\nit already exists, but avoid the race condition of:\n\n1. Checking whether the file exists\n2. If it doesn’t, creating it\n\nbecause between the check and the create, another process may have\ncreated it.',
     '此选项很有用，因为在运行配置脚本时存在一种常见情况：希望创建文件，或在文件已存在时什么也不做，但要避免以下竞争条件：\n\n1. 检查文件是否存在\n2. 若不存在，则创建它\n\n因为在检查与创建之间，另一个进程可能已经创建了它。'),
    ('This option is useful because there is a common situation, when running\nconfiguration scripts, where you want to create a file or do nothing if\nit already exists, but avoid the race condition of:\n\n1. Checking whether the file exists\n2. If it doesn\'t, creating it\n\nbecause between the check and the create, another process may have\ncreated it.',
     '此选项很有用，因为在运行配置脚本时存在一种常见情况：希望创建文件，或在文件已存在时什么也不做，但要避免以下竞争条件：\n\n1. 检查文件是否存在\n2. 若不存在，则创建它\n\n因为在检查与创建之间，另一个进程可能已经创建了它。'),

    # === process/struct.Child.html full ===
    ('If the child has already been waited on, this will return <code>None</code>.',
     '若子进程已经被等待过，则此方法返回 <code>None</code>。'),
    ('If the child has already been waited on, then this returns <code>None</code>.',
     '若子进程已经被等待过，则此方法返回 <code>None</code>。'),
    ('Once the child has been polled to completion this will return <code>None</code>.',
     '一旦子进程被轮询到完成，此方法将返回 <code>None</code>。'),
    ('If the child has already exited, then this returns <code>None</code>.',
     '若子进程已退出，则此方法返回 <code>None</code>。'),
    ('Returns the OS-assigned process identifier associated with this child.',
     '返回与此子进程关联的、由操作系统分配的进程标识符。'),
    ('Returns the OS-assigned process identifier associated with this child\nwhile it is still running.',
     '返回与此子进程关联的、由操作系统分配的进程标识符（在子进程仍在运行时）。'),
    ('Returns the process identifier of the inner process.',
     '返回内部进程的进程标识符。'),
    ('Returns the status of the child process, if it has already been polled to completion.',
     '返回子进程的状态（若它已被轮询到完成）。'),

    # === io/struct.BufReader.html ===
    ('The <code>BufReader</code> struct adds buffering to any reader.\nIt can be excessively inefficient to work directly with a <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a>\ninstance. A <code>BufReader</code> performs large, infrequent reads on the underlying\n<a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> and maintains an in-memory buffer of the results.',
     '<code>BufReader</code> 结构体为任何读取器添加缓冲。\n直接使用 <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> 实例可能非常低效。<code>BufReader</code> 对底层 <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> 执行大而少的读取，并在内存中维护结果的缓冲。'),

    # === io/struct.BufWriter.html ===
    ('The <code>BufWriter</code> struct adds buffering to any writer.\nIt can be excessively inefficient to work directly with a <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a>\ninstance. A <code>BufWriter</code> performs large, infrequent writes on the underlying\n<a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> and maintains an in-memory buffer of the results.',
     '<code>BufWriter</code> 结构体为任何写入器添加缓冲。\n直接使用 <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> 实例可能非常低效。<code>BufWriter</code> 对底层 <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> 执行大而少的写入，并在内存中维护结果的缓冲。'),

    # === io/struct.BufStream.html ===
    ('Wraps a type in both <a href="struct.BufReader.html" title="struct tokio::io::BufReader"><code>BufReader</code></a> and <a href="struct.BufWriter.html" title="struct tokio::io::BufWriter"><code>BufWriter</code></a>.\nSee the documentation for those types and <a href="struct.BufStream.html"><code>BufStream</code></a> for details.',
     '将一个类型同时包装为 <a href="struct.BufReader.html" title="struct tokio::io::BufReader"><code>BufReader</code></a> 与 <a href="struct.BufWriter.html" title="struct tokio::io::BufWriter"><code>BufWriter</code></a>。\n详见相关类型与 <a href="struct.BufStream.html"><code>BufStream</code></a> 的文档。'),
    ('Wraps a type in both BufReader and BufWriter.', '将一个类型同时包装为 BufReader 与 BufWriter。'),

    # === ReadHalf.html peer_addr ===
    ('Checks if this <code>ReadHalf</code> and some <code>WriteHalf</code> were split from the same stream.',
     '检查此 <code>ReadHalf</code> 与某个 <code>WriteHalf</code> 是否是从同一个流拆分而来。'),
    ('Reunites with a previously split <code>WriteHalf</code>.', '与之前拆分的 <code>WriteHalf</code> 重新合并。'),
    ('If this <code>ReadHalf</code> and the given <code>WriteHalf</code> do not originate from the same split operation this method will panic.',
     '若此 <code>ReadHalf</code> 与给定的 <code>WriteHalf</code> 不是来自同一次拆分操作，此方法将 panic。'),
    ('If this <code>ReadHalf</code> and the given <code>WriteHalf</code> do not originate from the\nsame split operation this method will panic.',
     '若此 <code>ReadHalf</code> 与给定的 <code>WriteHalf</code> 不是来自同一次拆分操作，此方法将 panic。'),

    # === fs/struct.File.html long open descriptions ===
    ('Opens a file in read-only mode.', '以只读模式打开文件。'),
    ('Opens a file in write-only mode.', '以只写模式打开文件。'),
    ('Opens a file in read-write mode.', '以读写模式打开文件。'),
    ('Truncates or creates a file in read-write mode.', '以读写模式截断或创建文件。'),
    ('Creates a file in read-write mode.', '以读写模式创建文件。'),
    ('Creates a new file in read-write mode, failing if the file already exists.',
     '以读写模式创建新文件；若文件已存在则失败。'),

    # === ReadDir.html ===
    ('Note that on multiple calls to <code>poll_next_entry</code>, only the <code>Waker</code> from\nthe <code>Context</code> passed to the most recent call is scheduled to receive a wakeup.',
     '请注意，在多次调用 <code>poll_next_entry</code> 时，只有最近一次调用传入的 <code>Context</code> 中的 <code>Waker</code> 会被调度以接收唤醒。'),
    ('When the method returns <code>Poll::Pending</code>, the <code>Waker</code> in the provided\n<code>Context</code> is scheduled to receive a wakeup when more bytes become available.',
     '当此方法返回 <code>Poll::Pending</code> 时，传入的 <code>Context</code> 中的 <code>Waker</code> 被调度以在更多字节可用时接收唤醒。'),
    ('* <code>Poll::Pending</code> if the next directory entry is not yet available.',
     '* 若下一个目录条目尚未就绪，返回 <code>Poll::Pending</code>。'),
    ('* <code>Poll::Ready(Ok(Some(entry)))</code> if the next directory entry is available.',
     '* 若下一个目录条目可用，返回 <code>Poll::Ready(Ok(Some(entry)))</code>。'),
    ('* <code>Poll::Ready(Ok(None))</code> if there are no more directory entries in this\nstream.',
     '* 若此流中再无更多目录条目，返回 <code>Poll::Ready(Ok(None))</code>。'),
    ('* <code>Poll::Ready(Ok(None))</code> if there are no more directory entries in this stream.',
     '* 若此流中再无更多目录条目，返回 <code>Poll::Ready(Ok(None))</code>。'),
    ('* <code>Poll::Ready(Err(error))</code> if an error occurred while reading the next\ndirectory entry.',
     '* 若读取下一个目录条目时发生错误，返回 <code>Poll::Ready(Err(error))</code>。'),
    ('* <code>Poll::Ready(Err(error))</code> if an error occurred while reading the next directory entry.',
     '* 若读取下一个目录条目时发生错误，返回 <code>Poll::Ready(Err(error))</code>。'),

    # === signal/windows/Ctrl* poll_recv ===
    ('Although this returns <code>Option&lt;()&gt;</code>, it will never actually return <code>None</code>.\nThis was accidentally exposed and would be a breaking change to be removed.',
     '尽管此函数返回 <code>Option&lt;()&gt;</code>，但实际上永远不会返回 <code>None</code>。\n这是意外暴露的，要删除将是一个破坏性变更。'),
    ('Polling from a manually implemented future', '从手动实现的 Future 轮询'),
    ('Polls to receive the next signal notification event, outside of an\nasync context.', '在异步上下文之外轮询以接收下一个信号通知事件。'),

    # === AsyncBufReadExt top docblock ===
    ('Asynchronously reads bytes from a source. Implemented as an extension trait, adding utility methods to all\n<code>AsyncBufRead</code> types.',
     '从源异步读取字节。作为扩展特性实现，向所有 <code>AsyncBufRead</code> 类型添加工具方法。'),
    ('Asynchronously reads bytes from a source. Implemented as an extension trait, adding utility methods to all <code>AsyncBufRead</code> types.',
     '从源异步读取字节。作为扩展特性实现，向所有 <code>AsyncBufRead</code> 类型添加工具方法。'),
    ('Asynchronously seeks to a position in a stream. Implemented as an extension trait, adding utility methods to all\n<code>AsyncSeek</code> types.',
     '在流中异步定位到指定位置。作为扩展特性实现，向所有 <code>AsyncSeek</code> 类型添加工具方法。'),
    ('Asynchronously seeks to a position in a stream. Implemented as an extension trait, adding utility methods to all <code>AsyncSeek</code> types.',
     '在流中异步定位到指定位置。作为扩展特性实现，向所有 <code>AsyncSeek</code> 类型添加工具方法。'),

    # === AsyncWriteExt more descriptions ===
    ('This function will attempt to write the entire contents of buf, but\nwill return an error if the underlying AsyncWrite instance reaches EOF\nbefore completing.',
     '此函数将尝试写入 buf 的全部内容，但如果底层 AsyncWrite 实例在完成前到达 EOF，则返回错误。'),
    ('This function will not write all of the data to the underlying writer, however it will write as much as possible without triggering a <code>Poll::Pending</code> from the underlying writer.',
     '此函数不会将所有数据写入底层写入器，但是它会在不触发底层写入器的 <code>Poll::Pending</code> 的前提下写入尽可能多的数据。'),

    # === AsyncWriteExt.write (long desc) ===
    ('Writes a buffer into this writer, returning how many bytes were\nwritten.', '将一个缓冲写入此写入器，返回写入的字节数。'),
    ('Writes a buffer into this writer, returning how many bytes were written.',
     '将一个缓冲写入此写入器，返回写入的字节数。'),
    ('Writes a buffer into this writer, advancing the buffer’s internal\ncursor.', '将一个缓冲写入此写入器，前进缓冲的内部游标。'),
    ('Writes a buffer into this writer, advancing the buffer’s internal\ncursor.', '将一个缓冲写入此写入器，前进缓冲的内部游标。'),
    ('Writes a buffer into this writer, advancing the buffer’s internal cursor.',
     '将一个缓冲写入此写入器，前进缓冲的内部游标。'),
    ('Attempts to write an entire buffer into this writer.', '尝试将整个缓冲写入此写入器。'),
    ('Writes an entire buffer into this writer.', '将整个缓冲写入此写入器。'),

    # === AsyncReadExt.read (full) ===
    ('Pulls some bytes from this source into the specified buffer,\nreturning how many bytes were read.',
     '从此源拉取一些字节到指定的缓冲中，返回读取的字节数。'),
    ('Pulls some bytes from this source into the specified buffer, returning how many bytes were read.',
     '从此源拉取一些字节到指定的缓冲中，返回读取的字节数。'),
    ('Pulls some bytes from this source into the specified buffer,\nadvancing the buffer’s internal cursor.',
     '从此源拉取一些字节到指定的缓冲中，前进缓冲的内部游标。'),
    ('Pulls some bytes from this source into the specified buffer, advancing the buffer’s internal cursor.',
     '从此源拉取一些字节到指定的缓冲中，前进缓冲的内部游标。'),

    # === AsyncReadExt.read_to_end / read_to_string ===
    ('Reads all bytes until EOF in this source, placing them into <code>buf</code>.',
     '从此源读取所有字节直到 EOF，将它们放入 <code>buf</code>。'),
    ('Reads all bytes until EOF in this source, appending them to <code>buf</code>.',
     '从此源读取所有字节直到 EOF，将它们追加到 <code>buf</code>。'),
    ('All bytes read from this source will be appended to the specified\nbuffer <code>buf</code>. This function will continuously call <code>read()</code> to\nappend more data to <code>buf</code> until <code>read()</code> returns <code>Ok(0)</code>.',
     '从此源读取的所有字节都将追加到指定的缓冲 <code>buf</code> 中。此函数会持续调用 <code>read()</code> 将更多数据追加到 <code>buf</code>，直到 <code>read()</code> 返回 <code>Ok(0)</code>。'),
    ('All bytes read from this source will be appended to the specified buffer buf. This function will continuously call read() to append more data to buf until read() returns Ok(0).',
     '从此源读取的所有字节都将追加到指定的缓冲 buf 中。此函数会持续调用 read() 将更多数据追加到 buf，直到 read() 返回 Ok(0)。'),
    ('If a read error is encountered then the <code>read_to_end</code> operation\nimmediately completes. Any bytes which have already been read will\nbe appended to <code>buf</code>.',
     '若遇到读取错误，<code>read_to_end</code> 操作将立即完成。已读取的所有字节将追加到 <code>buf</code>。'),
    ('If a read error is encountered then the read_to_end operation immediately completes. Any bytes which have already been read will be appended to buf.',
     '若遇到读取错误，read_to_end 操作将立即完成。已读取的所有字节将追加到 buf。'),
    ('If the data in this stream is <em>not</em> valid UTF-8 then an error is\nreturned and <code>buf</code> is unchanged.',
     '若此流中的数据不是有效的 UTF-8，则返回错误且 <code>buf</code> 保持不变。'),
    ('See <code>read_to_end</code> for other error semantics.', '其他错误语义请参阅 <code>read_to_end</code>。'),
    ('See read_to_end for other error semantics.', '其他错误语义请参阅 read_to_end。'),
    ('If successful, the number of bytes which were read and appended to\n<code>buf</code> is returned.',
     '若成功，返回已读取并追加到 <code>buf</code> 的字节数。'),
    ('If successful, the number of bytes which were read and appended to buf is returned.',
     '若成功，返回已读取并追加到 buf 的字节数。'),

    # === io/struct.SimplexStream.html ===
    ('Creates unidirectional buffer that acts like in memory pipe. To create split',
     '创建一个像内存管道一样的单向缓冲。要创建读写分离的拆分版本，'),
    ('version with separate reader and writer you can use simplex function.',
     '请使用 simplex 函数。'),

    # === io/struct.Lines.html / Take.html / BufWriter.html ===
    ('Returns the inner reader.', '返回内部读取器。'),
    ('Returns a mutable reference to the inner reader.', '返回内部读取器的可变引用。'),
    ('Returns a pinned mutable reference to the inner reader.', '返回内部读取器的 pinned 可变引用。'),
    ('Returns the next line in the stream.', '返回流中的下一行。'),
    ('Polls for the next line in the stream.', '轮询流中的下一行。'),
    ('Consuming this <code>Take</code>, returning the wrapped reader.', '消费此 <code>Take</code>，返回被包装的读取器。'),
    ('Consuming the Take, returning the wrapped reader.', '消费此 Take，返回被包装的读取器。'),
    ('Returns the maximum number of bytes that can be read.', '返回可读取的最大字节数。'),
    ('Returns the remaining number of bytes that can be read before this instance will return EOF.',
     '返回此实例返回 EOF 之前还可以读取的剩余字节数。'),

    # === io/struct.Split.html ===
    ('Splits a stream into separate read and write halves.', '将一个流拆分为独立的读、写两半。'),
    ('The <code>Split</code> struct allows you to split a bidirectional stream into separate read and write halves.',
     '<code>Split</code> 结构体允许你将一个双向流拆分为独立的读、写两半。'),

    # === AsyncSeekExt.seek detail ===
    ('Creates a future which will seek an IO object, and then yield the\nnew position in the object and the object itself.',
     '创建一个将定位 IO 对象，然后产出对象中的新位置以及对象本身的 Future。'),
    ('See <a href="trait.AsyncSeek.html"><code>AsyncSeek</code></a> for more details.',
     '详见 <a href="trait.AsyncSeek.html"><code>AsyncSeek</code></a>。'),
    ('See <code>AsyncSeek</code> for more details.', '详见 <code>AsyncSeek</code>。'),
    ('See AsyncSeek for more details.', '详见 AsyncSeek。'),
    ('In the case of an error the buffer and the object will be discarded, with\nthe error yielded.',
     '若发生错误，缓冲与对象将被丢弃，并产出错误。'),
    ('In the case of an error the buffer and the object will be discarded, with the error yielded.',
     '若发生错误，缓冲与对象将被丢弃，并产出错误。'),

    # === fs/struct.DirBuilder.html remaining ===
    ('This is an async version of std::fs::DirBuilder::new.', '这是 std::fs::DirBuilder::new 的异步版本。'),
    ('This is an async version of std::fs::DirBuilder::recursive.', '这是 std::fs::DirBuilder::recursive 的异步版本。'),
    ('This is an async version of std::fs::DirBuilder::create.', '这是 std::fs::DirBuilder::create 的异步版本。'),

    # === process/struct.ChildStderr/Stdin/Stdout ===
    ('The standard input stream of a child process.', '子进程的标准输入流。'),
    ('The standard output stream of a child process.', '子进程的标准输出流。'),
    ('The standard error stream of a child process.', '子进程的标准错误流。'),
    ('Creates an asynchronous <code>ChildStderr</code> from a synchronous one.', '从同步 <code>ChildStderr</code> 创建一个异步 <code>ChildStderr</code>。'),
    ('Creates an asynchronous <code>ChildStdout</code> from a synchronous one.', '从同步 <code>ChildStdout</code> 创建一个异步 <code>ChildStdout</code>。'),
    ('Creates an asynchronous <code>ChildStdin</code> from a synchronous one.', '从同步 <code>ChildStdin</code> 创建一个异步 <code>ChildStdin</code>。'),

    # === process/struct.Child.html cancel-safety ===
    ('This function is cancel safe.', '此函数是取消安全的。'),
    ('This function is cancel safe.\n\nIf the future is canceled, the child should be waited on using\n<code>wait</code> or <code>try_wait</code> to ensure the child process is properly\nreaped and any resources are cleaned up.',
     '此函数是取消安全的。\n\n如果 Future 被取消，应使用 <code>wait</code> 或 <code>try_wait</code> 等待子进程，以确保子进程被正确收割，并清理任何资源。'),
]


def main():
    pairs_b = []
    for en, zh in PAIRS:
        pairs_b.append((en.encode('utf-8'), zh.encode('utf-8')))

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
                if en_b in c:
                    occurrences = c.count(en_b)
                    c = c.replace(en_b, zh_b)
                    local += occurrences
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

    print(f'Phase 8: {files_changed}/{total_files} files, {total_replacements} replacements')


if __name__ == '__main__':
    main()