#!/usr/bin/env python3
"""tokio 第五阶段：补译 trait extension 中复杂多段描述。"""
import os

BASE = r'D:/Administrator/Documents/Code/rust_doc_all/tokio'

# 多行 / 复杂描述 - 长字符串优先
PAIRS = [
    # ===== AsyncBufReadExt =====
    # read_until (full description)
    ('Reads all bytes into <code>buf</code> until the delimiter <code>byte</code> or EOF is\nreached.',
     '读取所有字节到 <code>buf</code>，直到遇到分隔字节 <code>byte</code> 或 EOF。'),
    ('Reads all bytes into <code>buf</code> until the delimiter <code>byte</code> or EOF is reached.',
     '读取所有字节到 <code>buf</code>，直到遇到分隔字节 <code>byte</code> 或 EOF。'),
    ('This function will read bytes from the underlying stream until the\ndelimiter or EOF is found. Once found, all bytes up to, and including,\nthe delimiter (if found) will be appended to <code>buf</code>.',
     '此函数将从底层流读取字节，直到找到分隔字节或 EOF。找到后，到此为止的所有字节（包括分隔字节本身，若找到的话）将被追加到 <code>buf</code>。'),
    ('This function will read bytes from the underlying stream until the delimiter or EOF is found. Once found, all bytes up to, and including, the delimiter (if found) will be appended to <code>buf</code>.',
     '此函数将从底层流读取字节，直到找到分隔字节或 EOF。找到后，到此为止的所有字节（包括分隔字节本身，若找到的话）将被追加到 <code>buf</code>。'),
    ('If successful, this function will return the total number of bytes read.',
     '若成功，此函数将返回读取的总字节数。'),
    ('If an I/O error is encountered then all bytes read so far will be\ndiscarded.', '若遇到 I/O 错误，到目前为止读取的所有字节都将被丢弃。'),
    ('If an I/O error is encountered then all bytes read so far will be discarded.',
     '若遇到 I/O 错误，到目前为止读取的所有字节都将被丢弃。'),

    # read_line
    ('Reads all bytes until a newline (the 0xA byte) is reached, and append\nthem to the provided <code>String</code> buffer.',
     '读取所有字节直到遇到换行符（0xA 字节），并将它们追加到提供的 <code>String</code> 缓冲。'),
    ('Reads all bytes until a newline (the 0xA byte) is reached, and append them to the provided buffer.',
     '读取所有字节直到遇到换行符（0xA 字节），并将它们追加到提供的缓冲。'),

    # split (full)
    ('Returns a stream of the contents of this reader split on the byte\n<code>byte</code>.\nThis method is the asynchronous equivalent to\n<code>BufRead::split</code>.\nThe stream returned from this function will yield instances of\n<code>io::Result&lt;Option&lt;Vec&lt;u8&gt;&gt;&gt;</code>. Each vector returned will <em>not</em> have\nthe delimiter byte at the end.',
     '返回此读取器内容的流，按字节 <code>byte</code> 拆分。\n此方法是 <code>BufRead::split</code> 的异步等价物。\n此函数返回的流将产出 <code>io::Result&lt;Option&lt;Vec&lt;u8&gt;&gt;&gt;</code> 实例。每个返回的向量末尾将 <em>不会</em> 包含分隔字节。'),
    ('Returns a stream of the contents of this reader split on the byte byte.',
     '返回此读取器内容的流，按字节分隔。'),
    ('This method is the asynchronous equivalent to <code>BufRead::split</code>.', '此方法是 <code>BufRead::split</code> 的异步等价物。'),
    ('The stream returned from this function will yield instances of <code>io::Result&lt;Option&lt;Vec&lt;u8&gt;&gt;&gt;</code>. Each vector returned will <em>not</em> have the delimiter byte at the end.',
     '此函数返回的流将产出 <code>io::Result&lt;Option&lt;Vec&lt;u8&gt;&gt;&gt;</code> 实例。每个返回的向量末尾将 <em>不会</em> 包含分隔字节。'),
    ('Each item of the stream has the same error semantics as <code>AsyncBufReadExt::read_until</code>.',
     '流的每个项具有与 <code>AsyncBufReadExt::read_until</code> 相同的错误语义。'),

    # fill_buf (full)
    ('This function is a lower-level call. It needs to be paired with the\n<code>consume</code> method to function properly. When calling this method,\nnone of the contents will be “read” in the sense that later calling\n<code>read</code> may return the same contents. As such, <code>consume</code> must be\ncalled with the number of bytes that are consumed from this buffer\nto ensure that the bytes are never returned twice.',
     '此函数是较低级别的调用。它需要与 <code>consume</code> 方法配合使用才能正常工作。调用此方法时，任何内容都不会被“读取”，即后续调用 <code>read</code> 仍可能返回相同的内容。因此，必须使用从此缓冲消费的字节数调用 <code>consume</code>，以确保字节不会被返回两次。'),
    ('This function is a lower-level call. It needs to be paired with the consume method to function properly. When calling this method, none of the contents will be “read” in the sense that later calling read may return the same contents. As such, consume must be called with the number of bytes that are consumed from this buffer to ensure that the bytes are never returned twice.',
     '此函数是较低级别的调用。它需要与 consume 方法配合使用才能正常工作。调用此方法时，任何内容都不会被“读取”，即后续调用 read 仍可能返回相同的内容。因此，必须使用从此缓冲消费的字节数调用 consume，以确保字节不会被返回两次。'),
    ('An empty buffer returned indicates that the stream has reached EOF.', '返回空缓冲表示流已到达 EOF。'),

    # consume (full)
    ('Tells this buffer that <code>amt</code> bytes have been consumed from the\nbuffer, so they should no longer be returned in calls to <code>read</code>.\nThis function is a lower-level call. It needs to be paired with the\n<code>fill_buf</code> method to function properly. This function does not\nperform any I/O, it simply informs this object that some amount of\nits buffer, returned from <code>fill_buf</code>, has been consumed and should\nno longer be returned. As such, this function may do odd things if\n<code>fill_buf</code> isn’t called before calling it.\nThe <code>amt</code> must be less than the number of bytes in the buffer\nreturned by <code>fill_buf</code>.',
     '通知此缓冲已有 <code>amt</code> 个字节被消费，因此这些字节不应再在 <code>read</code> 调用中返回。\n此函数是较低级别的调用。它需要与 <code>fill_buf</code> 方法配合使用才能正常工作。此函数不执行任何 I/O，只是通知此对象其缓冲（由 <code>fill_buf</code> 返回）已有一定数量被消费，不应再返回。因此，若在调用此函数之前未调用 <code>fill_buf</code>，此函数可能会产生奇怪的行为。\n<code>amt</code> 必须小于 <code>fill_buf</code> 返回的缓冲中的字节数。'),
    ('This function is a lower-level call. It needs to be paired with the fill_buf method to function properly. This function does not perform any I/O, it simply informs this object that some amount of its buffer, returned from fill_buf, has been consumed and should no longer be returned. As such, this function may do odd things if fill_buf isn’t called before calling it.',
     '此函数是较低级别的调用。它需要与 fill_buf 方法配合使用才能正常工作。此函数不执行任何 I/O，只是通知此对象其缓冲（由 fill_buf 返回）已有一定数量被消费，不应再返回。因此，若在调用此函数之前未调用 fill_buf，此函数可能会产生奇怪的行为。'),
    ('The amt must be less than the number of bytes in the buffer\nreturned by fill_buf.', 'amt 必须小于 fill_buf 返回的缓冲中的字节数。'),

    # lines
    ('Returns a stream over the lines of this reader.\nThis method is the async equivalent to <code>BufRead::lines</code>.\nThe stream returned from this function will yield instances of\n<code>io::Result&lt;Option&lt;String&gt;&gt;</code>. Each string returned will <em>not</em> have a newline\nbyte (the 0xA byte) or <code>CRLF</code> (0xD, 0xA bytes) at the end.\n# Errors\nEach line of the stream has the same error semantics as <code>AsyncBufReadExt::read_line</code>.',
     '返回此读取器各行的流。\n此方法是 <code>BufRead::lines</code> 的异步等价物。\n此函数返回的流将产出 <code>io::Result&lt;Option&lt;String&gt;&gt;</code> 实例。每个返回的字符串末尾将 <em>不会</em> 包含换行字节（0xA 字节）或 <code>CRLF</code>（0xD、0xA 字节）。\n# 错误\n流的每一行具有与 <code>AsyncBufReadExt::read_line</code> 相同的错误语义。'),
    ('Returns a stream over the lines of this reader.\nThis method is the async equivalent to <code>BufRead::lines</code>.',
     '返回此读取器各行的流。\n此方法是 <code>BufRead::lines</code> 的异步等价物。'),
    ('Returns a stream over the lines of this reader.', '返回此读取器各行的流。'),
    ('The stream returned from this function will yield instances of <code>io::Result&lt;Option&lt;String&gt;&gt;</code>. Each string returned will <em>not</em> have a newline byte (the 0xA byte) or <code>CRLF</code> (0xD, 0xA bytes) at the end.',
     '此函数返回的流将产出 <code>io::Result&lt;Option&lt;String&gt;&gt;</code> 实例。每个返回的字符串末尾将 <em>不会</em> 包含换行字节（0xA 字节）或 <code>CRLF</code>（0xD、0xA 字节）。'),
    ('Each line of the stream has the same error semantics as <code>AsyncBufReadExt::read_line</code>.',
     '流的每一行具有与 <code>AsyncBufReadExt::read_line</code> 相同的错误语义。'),

    # ===== AsyncWriteExt =====
    # flush (full)
    ('Flushes this output stream, ensuring that all intermediately buffered\ncontents reach their destination.',
     '刷新此输出流，确保所有中间缓冲的内容到达目的地。'),
    ('Shuts down the output stream, ensuring that the value can be dropped\ncleanly.', '关闭输出流，确保此值能被干净地丢弃。'),
    ('Like <code>write</code>, except that it writes from a slice of buffers.',
     '与 <code>write</code> 类似，但从缓冲切片中写入。'),
    ('Data may be buffered if there is not enough space in the buffers, in\nwhich case the output stream may not be flushed.',
     '如果缓冲中没有足够的空间，数据可能会被缓冲，在这种情况下输出流可能不会被刷新。'),

    # ===== AsyncSeekExt =====
    ('Creates a future which will seek an IO object, and then yield the\nnew position in the object and the object itself.',
     '创建一个将定位 IO 对象，然后产出对象中的新位置以及对象本身的 Future。'),
    ('Creates a future which will return the current seek position from the\nunderlying object.',
     '创建一个 Future，返回底层对象的当前定位位置。'),
    ('Creates a future which will rewind to the beginning of the stream.',
     '创建一个将倒回到流开头的 Future。'),
    ('This is convenience method, equivalent to <code>self.seek(SeekFrom::Start(0))</code>.',
     '这是便捷方法，等价于 <code>self.seek(SeekFrom::Start(0))</code>。'),
    ('This is equivalent to <code>self.seek(SeekFrom::Current(0))</code>.',
     '这等价于 <code>self.seek(SeekFrom::Current(0))</code>。'),

    # ===== io/struct.BufReader.html =====
    ('Consuming this BufReader, returning the underlying reader.', '消费此 BufReader，返回底层读取器。'),
    ('Consuming this BufWriter, returning the underlying writer.', '消费此 BufWriter，返回底层写入器。'),
    ('Consuming this BufStream, returning the underlying I/O object.', '消费此 BufStream，返回底层 I/O 对象。'),
    ('Note that any leftover data in the internal buffer is lost.', '请注意，内部缓冲中的所有剩余数据都将丢失。'),
    ('Returning a reference to the internally buffered data.', '返回内部缓冲数据的引用。'),
    ('Unlike <code>fill_buf</code>, this will not attempt to fill the buffer if it is empty.',
     '与 <code>fill_buf</code> 不同，若缓冲为空，此方法不会尝试填充缓冲。'),

    # ===== fs/struct.DirBuilder.html =====
    ('This is an async version of std::fs::DirBuilder::new.', '这是 std::fs::DirBuilder::new 的异步版本。'),
    ('This is an async version of std::fs::DirBuilder::recursive.', '这是 std::fs::DirBuilder::recursive 的异步版本。'),
    ('This is an async version of std::fs::DirBuilder::create.', '这是 std::fs::DirBuilder::create 的异步版本。'),
    ('This is an async version of std::fs::OpenOptions::new', '这是 std::fs::OpenOptions::new 的异步版本。'),
    ('This is an async version of std::fs::OpenOptions::read', '这是 std::fs::OpenOptions::read 的异步版本。'),
    ('This is an async version of std::fs::OpenOptions::write', '这是 std::fs::OpenOptions::write 的异步版本。'),
    ('This option, when true, will indicate that the file should be read-able if opened.',
     '当此选项为 true 时，表示如果打开，文件应可读。'),
    ('This option, when true, will indicate that the file should be write-able if opened.',
     '当此选项为 true 时，表示如果打开，文件应可写。'),
    ('This option, when true, means that writes will append to a file instead of overwriting previous contents.',
     '当此选项为 true 时，表示写入将追加到文件末尾，而不是覆盖先前的内容。'),
    ('This option, when true, means that writes will append to a file instead of overwriting previous contents. Note that setting',
     '当此选项为 true 时，表示写入将追加到文件末尾，而不是覆盖先前的内容。注意，设置'),
    ('This can also be written using <code>File::options().read(true).write(true).create_new(true).open(...)</code>.',
     '这也可以用 <code>File::options().read(true).write(true).create_new(true).open(...)</code> 来表达。'),
    ('This can also be written using File::options().read(true).write(true).create_new(true).open(...).',
     '这也可以用 File::options().read(true).write(true).create_new(true).open(...) 来表达。'),

    # ===== fs/struct.File.html - long descriptions =====
    ('See <a href="struct.OpenOptions.html"><code>OpenOptions</code></a> for more details.',
     '详见 <a href="struct.OpenOptions.html"><code>OpenOptions</code></a>。'),
    ('See <code>OpenOptions</code> for more details.', '详见 <code>OpenOptions</code>。'),
    ('See OpenOptions for more details.', '详见 OpenOptions。'),
    ('This function will return an error if called from outside of the Tokio\nruntime or if <code>path</code> does not already exist. Other errors may also be\nreturned according to <a href="struct.OpenOptions.html"><code>OpenOptions::open</code></a>.',
     '若在 tokio 运行时外调用此函数，或若 <code>path</code> 不存在，此函数将返回错误。也可能根据 <a href="struct.OpenOptions.html"><code>OpenOptions::open</code></a> 返回其他错误。'),
    ('This function will return an error if called from outside of the Tokio runtime or if path does not already exist. Other errors may also be returned according to OpenOptions::open.',
     '若在 tokio 运行时外调用此函数，或若 path 不存在，此函数将返回错误。也可能根据 OpenOptions::open 返回其他错误。'),
    ('The read_to_end method is defined on the AsyncReadExt trait.', 'read_to_end 方法定义在 AsyncReadExt 特性上。'),
    ('The write_all method is defined on the AsyncWriteExt trait.', 'write_all 方法定义在 AsyncWriteExt 特性上。'),
    ('This function will create a file if it does not exist, and will truncate it if it does.',
     '若文件不存在，此函数将创建它；若已存在，则将其截断。'),
    ('Results in an error if called from outside of the Tokio runtime or if the underlying create call results in an error.',
     '若在 tokio 运行时外调用，或底层 create 调用出错，则返回错误。'),
    ('This function will create a file if it does not exist, and will fail if it does.',
     '若文件不存在，此函数将创建它；若已存在，则失败。'),
    ('Results in an error if called from outside of the Tokio runtime or if\nthe underlying create call results in an error.',
     '若在 tokio 运行时外调用，或底层 create 调用出错，则返回错误。'),
    ('This function will create a file if it does not exist, or return an error if the underlying create call fails.',
     '若文件不存在，此函数将创建它；若底层 create 调用失败，则返回错误。'),
    ('This function will create a file if it does not exist, or return an error',
     '若文件不存在，此函数将创建它，否则返回错误'),
    ('if it does.', '若文件已存在。'),
    ('This function will create a file if it does not exist, and will return an error',
     '若文件不存在，此函数将创建它，否则返回错误'),
    ('See the documentation for those types and <a href="struct.BufStream.html"><code>BufStream</code></a> for details.',
     '详见相关类型与 <a href="struct.BufStream.html"><code>BufStream</code></a> 的文档。'),
    ('See the documentation for those types and BufStream for details.', '详见相关类型与 BufStream 的文档。'),
    ('If an I/O error is encountered then all bytes read so far will be\ndiscarded.', '若遇到 I/O 错误，到目前为止读取的所有字节都将被丢弃。'),
    ('This function will ignore all instances of <code>ErrorKind::Interrupted</code> and\nhandle them as if the underlying call returned no bytes.',
     '此函数将忽略所有 <code>ErrorKind::Interrupted</code> 实例，并将它们当作底层调用未返回字节来处理。'),

    # ===== process/struct.Child.html =====
    ('The handle for writing to the child’s standard input (stdin), if it has\nbeen captured. To avoid partially moving the <code>child</code> and thus blocking\nyourself from calling functions on <code>child</code> while using <code>stdin</code>, you might\nfind it helpful to do',
     '子进程标准输入 (stdin) 的写入 handle（若已捕获）。为避免部分移动 <code>child</code> 导致在使用 <code>stdin</code> 时无法对 <code>child</code> 调用其他函数，你可能需要这样做'),
    ('The handle for reading from the child’s standard output (stdout), if it has\nbeen captured. To avoid partially moving the <code>child</code> and thus blocking\nyourself from calling functions on <code>child</code> while using <code>stdout</code>, you might\nfind it helpful to do',
     '子进程标准输出 (stdout) 的读取 handle（若已捕获）。为避免部分移动 <code>child</code> 导致在使用 <code>stdout</code> 时无法对 <code>child</code> 调用其他函数，你可能需要这样做'),
    ('The handle for reading from the child’s standard error (stderr), if it has\nbeen captured. To avoid partially moving the <code>child</code> and thus blocking\nyourself from calling functions on <code>child</code> while using <code>stderr</code>, you might\nfind it helpful to do',
     '子进程标准错误 (stderr) 的读取 handle（若已捕获）。为避免部分移动 <code>child</code> 导致在使用 <code>stderr</code> 时无法对 <code>child</code> 调用其他函数，你可能需要这样做'),
    ('let stdin = child.stdin.take().unwrap();', 'let stdin = child.stdin.take().unwrap();'),
    ('let stdout = child.stdout.take().unwrap();', 'let stdout = child.stdout.take().unwrap();'),
    ('let stderr = child.stderr.take().unwrap();', 'let stderr = child.stderr.take().unwrap();'),
    ('This will close any stdin/stdout/stderr handles that were opened via <code>Stdio::piped</code> when the <code>OwnedHandle</code> is dropped.',
     '当 <code>OwnedHandle</code> 被丢弃时，将关闭通过 <code>Stdio::piped</code> 打开的所有 stdin/stdout/stderr handle。'),
    ('On Unix systems, this will close any stdin/stdout/stderr handles that were opened via <code>Stdio::piped</code> when the <code>OwnedHandle</code> is dropped.',
     '在 Unix 系统上，当 <code>OwnedHandle</code> 被丢弃时，这将关闭通过 <code>Stdio::piped</code> 打开的所有 stdin/stdout/stderr handle。'),
    ('This method may be used to drop the raw handle without affecting any of the piped stdin/stdout/stderr handles.',
     '此方法可用于丢弃原始 handle 而不影响任何通过管道接出的 stdin/stdout/stderr handle。'),
    ('Important: calling this function is required to prevent a deadlock\nin the case that the child process has captured stdin/stdout/stderr pipes.',
     '重要：在子进程已捕获 stdin/stdout/stderr 管道的场景中，调用此函数对于避免死锁是必需的。'),
    ('Waits for the child to exit completely, returning the status that it\nexited with. This function will continue to have the same return value\nafter it has been called at least once.',
     '等待子进程完全退出，返回它退出的状态。此函数至少被调用一次后，将继续返回相同的返回值。'),
    ('If the caller wishes to explicitly control when the child’s stdin\nhandle is closed, they may <code>.take()</code> it before calling <code>.wait()</code>:',
     '若调用者希望显式控制子进程的 stdin handle 何时关闭，可在调用 <code>.wait()</code> 之前先 <code>.take()</code>：'),
    ('This function is cancel safe.', '此函数是取消安全的。'),
    ('Attempts to collect the exit status of the child if it has already\nexited.', '若子进程已退出，尝试收集其退出状态。'),
    ('If the child has exited, then <code>Ok(Some(status))</code> is returned. If the\nexit status is not available at this time then <code>Ok(None)</code> is returned.\nIf an error occurs, then that error is returned.',
     '若子进程已退出，返回 <code>Ok(Some(status))</code>。若退出状态此时不可用，返回 <code>Ok(None)</code>。若发生错误，返回该错误。'),
    ('Note that unlike <code>wait</code>, this function will not attempt to drop stdin,\nnor will it wake the current task if the child exits.',
     '请注意，与 <code>wait</code> 不同，此函数不会尝试关闭 stdin，也不会在子进程退出时唤醒当前任务。'),
    ('Returns a future that will resolve to an <code>Output</code>, containing the exit\nstatus, stdout, and stderr of the child process.',
     '返回一个 Future，它将解析为 <code>Output</code>，包含子进程的退出状态、stdout 与 stderr。'),
    ('The returned future will simultaneously waits for the child to exit and\ncollect all remaining output on the stdout/stderr handles, returning an\n<code>Output</code> instance.',
     '返回的 Future 将同时等待子进程退出并收集 stdout/stderr handle 上所有剩余输出，返回一个 <code>Output</code> 实例。'),
    ('The stdin handle to the child process, if any, will be closed before\nwaiting. This helps avoid deadlock: it ensures that the child does not\nblock waiting for input from the parent, while the parent waits for the\nchild to exit.',
     '子进程的 stdin handle（若有）在等待前将被关闭。这有助于避免死锁：它确保子进程不会因等待父进程输入而阻塞，同时父进程正在等待子进程退出。'),
    ('By default, stdin, stdout and stderr are inherited from the parent. In\norder to capture the output into this <code>Output</code> it is necessary to create\nnew pipes between parent and child. Use <code>stdout(Stdio::piped())</code> and\n<code>stderr(Stdio::piped())</code> to capture the output into this <code>Output</code>.',
     '默认情况下，stdin、stdout 与 stderr 继承自父进程。要将输出捕获到此 <code>Output</code>，需要在父进程与子进程之间创建新管道。请使用 <code>stdout(Stdio::piped())</code> 与 <code>stderr(Stdio::piped())</code> 将输出捕获到此 <code>Output</code>。'),
    ('The stdin handle, if any, will be closed after waiting. This helps avoid\ndeadlock: it ensures that the child does not block waiting for input\nfrom the parent, while the parent waits for the child to exit.',
     'stdin handle（若有）将在等待后被关闭。这有助于避免死锁：它确保子进程不会因等待父进程输入而阻塞，同时父进程正在等待子进程退出。'),
    ('By default, stdin, stdout and stderr are inherited from the parent. In\norder to capture the output into this <code>Output</code> it is necessary to create\nnew pipes between parent and child.',
     '默认情况下，stdin、stdout 与 stderr 继承自父进程。要将输出捕获到此 <code>Output</code>，需要在父进程与子进程之间创建新管道。'),
    ('Use <code>stdout(Stdio::piped())</code> and <code>stderr(Stdio::piped())</code> to capture the output into this <code>Output</code>.',
     '请使用 <code>stdout(Stdio::piped())</code> 与 <code>stderr(Stdio::piped())</code> 将输出捕获到此 <code>Output</code>。'),
    ('Returns the process identifier of the inner process.', '返回内部进程的进程标识符。'),
    ('Receives the next signal notification event.', '接收下一个信号通知事件。'),
    ('Polls to receive the next signal notification event, outside of an\nasync context.', '在异步上下文之外轮询以接收下一个信号通知事件。'),
    ('This method returns the total number of bytes read. If you cancel\nthe future, it may read some bytes but they will be lost. The future\nwill return an error in this case.',
     '此方法返回读取的总字节数。如果取消 Future，它可能读取一些字节但这些字节会丢失。这种情况下 Future 将返回错误。'),
    ('If you want to read the bytes even after cancellation, you should call\n<code>read_buf</code> and then <code>read</code> in a loop.',
     '如果希望在取消后仍能读取字节，应在循环中调用 <code>read_buf</code> 然后调用 <code>read</code>。'),

    # ===== process/struct.Command.html =====
    ('Builder methods are provided to change these defaults and\nconfigure other aspects on the <code>Command</code>.',
     '提供了 Builder 方法来修改这些默认值，并配置 <code>Command</code> 的其他方面。'),
    ('Builder methods are provided to change these defaults and configure other aspects on the Command.',
     '提供了 Builder 方法来修改这些默认值，并配置 Command 的其他方面。'),
    ('Append literal text to the command line without any quoting or escaping.',
     '向命令行追加字面文本，不进行任何引号或转义。'),
    ('This is useful for passing arguments to <code>cmd.exe /c</code>, which doesn’t follow\n<code>CommandLineToArgvW</code> escaping rules.',
     '这对于将参数传递给 <code>cmd.exe /c</code> 很有用，因为它不遵循 <code>CommandLineToArgvW</code> 的转义规则。'),
    ('This is useful for passing arguments to cmd.exe /c, which doesn’t follow CommandLineToArgvW escaping rules.',
     '这对于将参数传递给 cmd.exe /c 很有用，因为它不遵循 CommandLineToArgvW 的转义规则。'),
    ('If program is not an absolute path, the PATH will be searched in\nthe OS-defined way.', '若 program 不是绝对路径，将以操作系统定义的方式搜索 PATH。'),
    ('If program is not an absolute path, the PATH will be searched in the OS-defined way.',
     '若 program 不是绝对路径，将以操作系统定义的方式搜索 PATH。'),
    ('The search path to be used may be controlled by setting the\nPATH environment variable appropriately.',
     '可通过适当设置 PATH 环境变量来控制要使用的搜索路径。'),
    ('The search path to be used may be controlled by setting the PATH environment variable appropriately.',
     '可通过适当设置 PATH 环境变量来控制要使用的搜索路径。'),
    ('Only one argument can be passed per use. So instead of:', '每次调用只能传递一个参数。因此，请勿这样：'),
    ('To pass a single argument see <code>arg</code>.', '若要传递单个参数，请参阅 <code>arg</code>。'),
    ('To pass a single argument see arg.', '若要传递单个参数，请参阅 arg。'),
    ('Cheaply convert to a <code>&amp;std::process::Command</code> for places where the type from the standard library is expected.',
     '在期望标准库类型的位置，可廉价地转换为 <code>&amp;std::process::Command</code>。'),
    ('Cheaply convert to a <code>&amp;mut std::process::Command</code> for places where the type from the standard library is expected.',
     '在期望标准库类型的位置，可廉价地转换为 <code>&amp;mut std::process::Command</code>。'),

    # ===== fs/struct.DirEntry.html long descriptions =====
    ('This prints output like:', '此代码输出类似：'),
    ('The exact text, of course, depends on what files you have in ..',
     '确切的文本当然取决于你在 .. 中有哪些文件。'),
    ('On Windows and most Unix platforms this function is free (no extra\nsystem calls needed), but some Unix platforms may require the equivalent\ncall to <code>symlink_metadata</code> to learn about the target file type.',
     '在 Windows 与大多数 Unix 平台上，此函数是免费的（无需额外的系统调用），但部分 Unix 平台可能需要等效调用 <code>symlink_metadata</code> 来了解目标文件的类型。'),
    ('On Windows and most Unix platforms this function is free (no extra system calls needed), but some Unix platforms may require the equivalent call to symlink_metadata to learn about the target file type.',
     '在 Windows 与大多数 Unix 平台上，此函数是免费的（无需额外的系统调用），但部分 Unix 平台可能需要等效调用 symlink_metadata 来了解目标文件的类型。'),

    # ===== fs/struct.ReadDir.html long =====
    ('Note that on multiple calls to <code>poll_next_entry</code>, only the <code>Waker</code> from\nthe <code>Context</code> passed to the most recent call is scheduled to receive a wakeup.',
     '请注意，在多次调用 <code>poll_next_entry</code> 时，只有最近一次调用传入的 <code>Context</code> 中的 <code>Waker</code> 会被调度以接收唤醒。'),
    ('Note that on multiple calls to poll_next_entry, only the Waker from\nthe Context passed to the most recent call is scheduled to receive a wakeup.',
     '请注意，在多次调用 poll_next_entry 时，只有最近一次调用传入的 Context 中的 Waker 会被调度以接收唤醒。'),
    ('When the method returns <code>Poll::Pending</code>, the <code>Waker</code> in the provided\n<code>Context</code> is scheduled to receive a wakeup when more bytes become available.',
     '当此方法返回 <code>Poll::Pending</code> 时，传入的 <code>Context</code> 中的 <code>Waker</code> 被调度以在更多字节可用时接收唤醒。'),
    ('When the method returns Poll::Pending, the Waker in the provided\nContext is scheduled to receive a wakeup when more bytes become',
     '当此方法返回 Poll::Pending 时，传入的 Context 中的 Waker 被调度以在更多字节可用时接收唤醒。'),
    ('* <code>Poll::Pending</code> if the next directory entry is not yet available.', '* 若下一个目录条目尚未就绪，返回 <code>Poll::Pending</code>。'),
    ('* <code>Poll::Ready(Ok(Some(entry)))</code> if the next directory entry is available.', '* 若下一个目录条目可用，返回 <code>Poll::Ready(Ok(Some(entry)))</code>。'),
    ('* <code>Poll::Ready(Ok(None))</code> if there are no more directory entries in this\nstream.', '* 若此流中再无更多目录条目，返回 <code>Poll::Ready(Ok(None))</code>。'),
    ('* <code>Poll::Ready(Ok(None))</code> if there are no more directory entries in this stream.',
     '* 若此流中再无更多目录条目，返回 <code>Poll::Ready(Ok(None))</code>。'),
    ('* <code>Poll::Ready(Err(error))</code> if an error occurred while reading the next\ndirectory entry.', '* 若读取下一个目录条目时发生错误，返回 <code>Poll::Ready(Err(error))</code>。'),
    ('* <code>Poll::Ready(Err(error))</code> if an error occurred while reading the next directory entry.',
     '* 若读取下一个目录条目时发生错误，返回 <code>Poll::Ready(Err(error))</code>。'),

    # ===== signal/windows/struct.Ctrl*.html poll_recv =====
    ('Although this returns <code>Option&lt;()&gt;</code>, it will never actually return <code>None</code>.\nThis was accidentally exposed and would be a breaking change to be removed.',
     '尽管此函数返回 <code>Option&lt;()&gt;</code>，但实际上永远不会返回 <code>None</code>。\n这是意外暴露的，要删除将是一个破坏性变更。'),
    ('Polling from a manually implemented future', '从手动实现的 Future 轮询'),

    # ===== io/struct.SimplexStream.html =====
    ('Creates unidirectional buffer that acts like in memory pipe. To create split',
     '创建一个像内存管道一样的单向缓冲。要创建读写分离的拆分版本，'),
    ('version with separate reader and writer you can use simplex function.', '请使用 simplex 函数。'),
    ('Creating a unidirectional buffer that acts like an in-memory pipe.',
     '创建一个像内存管道一样的单向缓冲。'),

    # ===== io/struct.Split.html =====
    ('Splits a stream into separate read and write halves.', '将一个流拆分为独立的读、写两半。'),
    ('The <code>Split</code> struct allows you to split a bidirectional stream into separate read and write halves.',
     '<code>Split</code> 结构体允许你将一个双向流拆分为独立的读、写两半。'),

    # ===== io/struct.Lines.html =====
    ('Returns the inner reader.', '返回内部读取器。'),
    ('Returns a mutable reference to the inner reader.', '返回内部读取器的可变引用。'),
    ('Returns a pinned mutable reference to the inner reader.', '返回内部读取器的 pinned 可变引用。'),
    ('Returns the next line in the stream.', '返回流中的下一行。'),

    # ===== io/struct.ReadHalf.html peer_addr =====
    ('Checks if this <code>ReadHalf</code> and some <code>WriteHalf</code> were split from the same stream.',
     '检查此 <code>ReadHalf</code> 与某个 <code>WriteHalf</code> 是否是从同一个流拆分而来。'),
    ('Reunites with a previously split <code>WriteHalf</code>.', '与之前拆分的 <code>WriteHalf</code> 重新合并。'),
    ('If this <code>ReadHalf</code> and the given <code>WriteHalf</code> do not originate from the same split operation this method will panic.',
     '若此 <code>ReadHalf</code> 与给定的 <code>WriteHalf</code> 不是来自同一次拆分操作，此方法将 panic。'),
    ('This can be checked ahead of time by calling <code>is_pair_of()</code>.', '可通过调用 <code>is_pair_of()</code> 提前检查。'),
    ('If this ReadHalf and the given WriteHalf do not originate from the\nsame split operation this method will panic.',
     '若此 ReadHalf 与给定的 WriteHalf 不是来自同一次拆分操作，此方法将 panic。'),

    # ===== io/struct.Take.html =====
    ('Getting a reference to the underlying reader.', '获取底层读取器的引用。'),
    ('Getting a mutable reference to the underlying reader. Care should be\ntaken to avoid modifying the internal I/O state of the underlying reader as\ndoing so may corrupt the internal limit of this <code>Take</code>.',
     '获取底层读取器的可变引用。请注意避免修改底层读取器的内部 I/O 状态，否则可能损坏此 <code>Take</code> 的内部限制。'),
    ('Getting a mutable reference to the underlying reader. Care should be taken to avoid modifying the internal I/O state of the underlying reader as',
     '获取底层读取器的可变引用。请注意避免修改底层读取器的内部 I/O 状态，'),
    ('Getting a pinned mutable reference to the underlying reader. Care\nshould be taken to avoid modifying the internal I/O state of the underlying\nreader as doing so may corrupt the internal limit of this <code>Take</code>.',
     '获取底层读取器的 pinned 可变引用。请注意避免修改底层读取器的内部 I/O 状态，否则可能损坏此 <code>Take</code> 的内部限制。'),
    ('Getting a pinned mutable reference to the underlying reader. Care should be taken to avoid modifying the internal I/O state of the underlying reader as',
     '获取底层读取器的 pinned 可变引用。请注意避免修改底层读取器的内部 I/O 状态，'),
    ('Consuming the <code>Take</code>, returning the wrapped reader.', '消费此 <code>Take</code>，返回被包装的读取器。'),
    ('Consuming the Take, returning the wrapped reader.', '消费此 Take，返回被包装的读取器。'),

    # ===== io/struct.BufStream.html (long descriptions) =====
    ('See the documentation for those types and <a href="struct.BufStream.html"><code>BufStream</code></a> for details.',
     '详见相关类型与 <a href="struct.BufStream.html"><code>BufStream</code></a> 的文档。'),
    ('See the documentation for those types and <code>BufStream</code> for details.', '详见相关类型与 <code>BufStream</code> 的文档。'),
    ('Wraps a type in both <a href="struct.BufReader.html" title="struct tokio::io::BufReader"><code>BufReader</code></a> and <a href="struct.BufWriter.html" title="struct tokio::io::BufWriter"><code>BufWriter</code></a>.\nSee the documentation for those types and <a href="struct.BufStream.html"><code>BufStream</code></a> for details.',
     '将一个类型同时包装为 <a href="struct.BufReader.html" title="struct tokio::io::BufReader"><code>BufReader</code></a> 与 <a href="struct.BufWriter.html" title="struct tokio::io::BufWriter"><code>BufWriter</code></a>。\n详见相关类型与 <a href="struct.BufStream.html"><code>BufStream</code></a> 的文档。'),
    ('Wraps a type in both BufReader and BufWriter.', '将一个类型同时包装为 BufReader 与 BufWriter。'),
    ('Consuming this BufStream, returning the underlying I/O object.', '消费此 BufStream，返回底层 I/O 对象。'),

    # ===== common sentence pieces =====
    ('Context is scheduled to receive a wakeup when more bytes become\navailable.', '当更多字节可用时，上下文被调度以接收唤醒。'),
    ('Context is scheduled to receive a wakeup when more bytes become', '当更多字节可用时，上下文被调度以接收唤醒。'),
    ('Context is scheduled to receive a wakeup when the next directory entry becomes available.',
     '当下一个目录条目可用时，上下文被调度以接收唤醒。'),
    ('Context is scheduled to receive a wakeup when the next directory entry', '当下一个目录条目可用时，上下文被调度以接收唤醒。'),

    # ===== fs/struct.File.html remaining =====
    ('Creates a new file in read-write mode, failing if the file already exists.',
     '以读写模式创建新文件；若文件已存在则失败。'),
    ('Creates a file in read-write mode.', '以读写模式创建文件。'),
    ('Truncates or creates a file in read-write mode.', '以读写模式截断或创建文件。'),

    # ===== simpler fragmented pieces (longer wins) =====
    ('Note that Tokio specific options will be lost. Currently, this only\napplies to <code>kill_on_drop</code>.',
     '请注意，tokio 特有的选项将丢失。目前，这仅影响 <code>kill_on_drop</code>。'),
    ('Cheaply convert into a <code>std::process::Command</code>.', '廉价地转换为 <code>std::process::Command</code>。'),
    ('Convert into <code>OwnedHandle</code>.', '转换为 <code>OwnedHandle</code>。'),
    ('Correspondingly, however, callers of this method may not assume\nthat on Unix platforms it is possible for a zombie process to remain\nafter a kill is sent; to avoid this, the caller should ensure that\n<code>Child::wait</code> or <code>Child::try_wait</code> is invoked.',
     '相应地，但是，调用此方法不能假设在 Unix 平台上发送 kill 信号后子进程可能不会成为僵尸进程；为避免这种情况，调用者应确保调用 <code>Child::wait</code> 或 <code>Child::try_wait</code>。'),
    ('Correspondingly, however, callers of this method may not assume', '相应地，但是，调用此方法不能假设'),
    ('that on Unix platforms it is possible for a zombie process to remain\nafter a kill is sent; to avoid this, the caller should ensure that',
     '在 Unix 平台上发送 kill 信号后子进程可能成为僵尸进程；为避免这种情况，调用者应确保'),
    ('The process identifier returned by this function is the\nidentifier that the kernel uses, and may be reused once the child has\nexited.',
     '此函数返回的进程标识符是内核使用的标识符，在子进程退出后可能被复用。'),
    ('The process identifier returned by this function is the identifier that the kernel uses, and may be reused once the child has exited.',
     '此函数返回的进程标识符是内核使用的标识符，在子进程退出后可能被复用。'),
    ('Extracts the raw handle of the process associated with this child while\nensuring it is closed if the returned <code>OwnedHandle</code> is dropped.',
     '提取与此子进程关联的原始 handle，同时确保在返回的 <code>OwnedHandle</code> 被丢弃时将其关闭。'),
    ('Extracts the raw handle of the process associated with this child while ensuring it is closed if the returned OwnedHandle is dropped.',
     '提取与此子进程关联的原始 handle，同时确保在返回的 OwnedHandle 被丢弃时将其关闭。'),
    ('This method may fail if an error is encountered when setting the pipe to\nnon-blocking mode, or when registering the pipe with the runtime’s IO\ndriver.',
     '此方法可能在将管道设置为非阻塞模式，或在向运行时的 IO 驱动注册管道时遇到错误而失败。'),
    ('This method may fail if an error is encountered when setting the pipe to non-blocking mode, or when registering the pipe with the runtime’s IO driver.',
     '此方法可能在将管道设置为非阻塞模式，或在向运行时的 IO 驱动注册管道时遇到错误而失败。'),
    ('Once the child has been polled to completion this will return <code>None</code>.',
     '一旦子进程被轮询到完成，此方法将返回 <code>None</code>。'),
    ('Once the child has been polled to completion this will return None.',
     '一旦子进程被轮询到完成，此方法将返回 None。'),
    ('If the child has already been waited on, then this returns <code>None</code>.',
     '若子进程已经被等待过，则此方法返回 <code>None</code>。'),
    ('Returns the status of the child process, if it has already been polled to completion.',
     '返回子进程的状态（若它已被轮询到完成）。'),

    # ===== io/struct.ReadHalf.html docblock (from page) =====
    ('The read half of a TCP connection.', 'TCP 连接的读半。'),
    ('This is the half created by <a href="fn.split.html" title="fn tokio::net::split"><code>split</code></a>.', '这是由 <a href="fn.split.html" title="fn tokio::net::split"><code>split</code></a> 创建的半。'),
    ('Allows the use of <code>AsyncRead</code> functionality on the read half.', '允许在读半上使用 <code>AsyncRead</code> 功能。'),
    ('The write half of a TCP connection.', 'TCP 连接的写半。'),
    ('Allows the use of <code>AsyncWrite</code> functionality on the write half.', '允许在写半上使用 <code>AsyncWrite</code> 功能。'),

    # ===== io/struct.BufReader.html full docblock =====
    ('It is inadvisable to directly read from the underlying reader.',
     '不建议直接读取底层读取器。'),
    ('The <code>BufReader</code> struct adds buffering to any reader.\nIt can be excessively inefficient to work directly with a <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a>\ninstance. A <code>BufReader</code> performs large, infrequent reads on the underlying\n<a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> and maintains an in-memory buffer of the results.',
     '<code>BufReader</code> 结构体为任何读取器添加缓冲。\n直接使用 <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> 实例可能非常低效。<code>BufReader</code> 对底层 <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> 执行大而少的读取，并在内存中维护结果的缓冲。'),
    ('<code>BufReader</code> can improve the speed of programs that make *small* and\n*repeated* read calls to the same file or network socket. This happens\nbecause <code>BufReader</code> maintains an in-memory buffer of read data, allowing\nfewer actual calls to the underlying reader.',
     '<code>BufReader</code> 可提升对同一文件或网络套接字进行*小*且*重复*读取调用的程序的速度。其原理是 <code>BufReader</code> 在内存中维护读取数据的缓冲，从而减少对底层读取器的实际调用次数。'),
    ('The handle for reading from the child\'s standard error (stderr), if it\nhas been captured.', '子进程标准错误 (stderr) 的读取 handle（若已捕获）。'),
    ('The handle for reading from the child\'s standard output (stdout), if it\nhas been captured.', '子进程标准输出 (stdout) 的读取 handle（若已捕获）。'),
    ('The handle for writing to the child\'s standard input (stdin), if it has\nbeen captured.', '子进程标准输入 (stdin) 的写入 handle（若已捕获）。'),
    ('To avoid partially moving the child and thus blocking yourself from calling functions on child while using stdout, you should call .into_inner() immediately after reading all data.',
     '为避免部分移动子进程导致在使用 stdout 时无法对子进程调用其他函数，应在读取所有数据后立即调用 .into_inner()。'),
    ('To avoid partially moving the child and thus blocking yourself from calling functions on child while using stderr, you should call .into_inner() immediately after reading all data.',
     '为避免部分移动子进程导致在使用 stderr 时无法对子进程调用其他函数，应在读取所有数据后立即调用 .into_inner()。'),
    ('To avoid partially moving the child and thus blocking yourself from calling functions on child while using stdin, you should call .into_inner() immediately after writing all data.',
     '为避免部分移动子进程导致在使用 stdin 时无法对子进程调用其他函数，应在写入所有数据后立即调用 .into_inner()。'),

    # ===== AsyncReadExt description at top =====
    ('Reads bytes from a source. Implemented as an extension trait, adding utility methods to all <code>AsyncRead</code> types. Callers will tend to import this trait instead of <code>AsyncRead</code>',
     '从源读取字节。作为扩展特性实现，向所有 <code>AsyncRead</code> 类型添加工具方法。调用者通常会导入本特性而非 <code>AsyncRead</code>'),
    ('Writes bytes to a sink. Implemented as an extension trait, adding utility methods to all <code>AsyncWrite</code> types. Callers will tend to import this trait instead of <code>AsyncWrite</code>',
     '将字节写入汇。作为扩展特性实现，向所有 <code>AsyncWrite</code> 类型添加工具方法。调用者通常会导入本特性而非 <code>AsyncWrite</code>'),
    ('Reads bytes from a source.', '从源读取字节。'),
    ('Writes bytes to a sink.', '将字节写入汇。'),
    ('Implemented as an extension trait, adding utility methods to all AsyncRead types.', '作为扩展特性实现，向所有 AsyncRead 类型添加工具方法。'),
    ('Implemented as an extension trait, adding utility methods to all AsyncWrite types.', '作为扩展特性实现，向所有 AsyncWrite 类型添加工具方法。'),
    ('Implemented as an extension trait, adding utility methods to all AsyncBufRead types.', '作为扩展特性实现，向所有 AsyncBufRead 类型添加工具方法。'),
    ('Implemented as an extension trait, adding utility methods to all AsyncSeek types.', '作为扩展特性实现，向所有 AsyncSeek 类型添加工具方法。'),
    ('Callers will tend to import this trait instead of <code>AsyncRead</code>', '调用者通常会导入本特性而非 <code>AsyncRead</code>'),
    ('Callers will tend to import this trait instead of <code>AsyncWrite</code>', '调用者通常会导入本特性而非 <code>AsyncWrite</code>'),

    # ===== AsyncReadExt chain detail =====
    ('Creates a new <code>AsyncRead</code> instance that chains this stream with another.\nThe returned <code>AsyncRead</code> instance will first read all bytes from this object\nuntil EOF is encountered. Afterwards the output is equivalent to the\noutput of <code>next</code>.',
     '创建一个新的 <code>AsyncRead</code> 实例，将此流与另一个流链接起来。\n返回的 <code>AsyncRead</code> 实例将首先从此对象读取所有字节直到 EOF。之后的输出等同于 <code>next</code> 的输出。'),
    ('Creates a new <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> instance that chains this stream with another.',
     '创建一个新的 <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> 实例，将此流与另一个流链接起来。'),
    ('The returned <code>AsyncRead</code> instance will first read all bytes from this object\nuntil EOF is encountered. Afterwards the output is equivalent to the\noutput of <code>next</code>.',
     '返回的 <code>AsyncRead</code> 实例将首先从此对象读取所有字节直到 EOF。之后的输出等同于 <code>next</code> 的输出。'),
    ('The returned <code>AsyncRead</code> instance will first read all bytes from this object until EOF is encountered. Afterwards the output is equivalent to the output of <code>next</code>.',
     '返回的 <code>AsyncRead</code> 实例将首先从此对象读取所有字节直到 EOF。之后的输出等同于 <code>next</code> 的输出。'),

    # ===== AsyncReadExt take detail =====
    ('Creates an adaptor which reads at most <code>limit</code> bytes from it.\nThis function returns a new instance of <code>AsyncRead</code> which will read\nat most <code>limit</code> bytes, after which it will always return EOF\n(<code>Ok(0)</code>). Any read errors will not count towards the number of\nbytes read and future calls to <code>read()</code> may succeed.',
     '创建一个适配器，从其中最多读取 <code>limit</code> 个字节。\n此函数返回 <code>AsyncRead</code> 的一个新实例，最多读取 <code>limit</code> 个字节，之后将始终返回 EOF（<code>Ok(0)</code>）。任何读取错误将不计入已读取字节数，且对 <code>read()</code> 的后续调用仍可能成功。'),
    ('Creates an adaptor which reads at most <code>limit</code> bytes from it.',
     '创建一个适配器，从其中最多读取 <code>limit</code> 个字节。'),
    ('This function returns a new instance of <code>AsyncRead</code> which will read\nat most <code>limit</code> bytes, after which it will always return EOF\n(<code>Ok(0)</code>). Any read errors will not count towards the number of\nbytes read and future calls to <code>read()</code> may succeed.',
     '此函数返回 <code>AsyncRead</code> 的一个新实例，最多读取 <code>limit</code> 个字节，之后将始终返回 EOF（<code>Ok(0)</code>）。任何读取错误将不计入已读取字节数，且对 <code>read()</code> 的后续调用仍可能成功。'),

    # ===== AsyncSeekExt.seek full description =====
    ('See <a href="trait.AsyncSeek.html"><code>AsyncSeek</code></a> for more details.', '详见 <a href="trait.AsyncSeek.html"><code>AsyncSeek</code></a>。'),
    ('See <code>AsyncSeek</code> for more details.', '详见 <code>AsyncSeek</code>。'),
    ('See AsyncSeek for more details.', '详见 AsyncSeek。'),
    ('Seeking always discards the internal buffer, even if the seek position\nfalls within it.', '定位总是会丢弃内部缓冲，即使定位位置落在缓冲范围内。'),
    ('Seeking always discards the internal buffer, even if the seek position falls within it.',
     '定位总是会丢弃内部缓冲，即使定位位置落在缓冲范围内。'),
    ('This is done to avoid confusion on platforms like Unix where the OS\ncan return the new position of an empty internal buffer.',
     '这是为了避免在像 Unix 这样的平台上产生混淆，其中操作系统可能返回空内部缓冲的新位置。'),
    ('This is done to avoid confusion on platforms like Unix where the OS can return the new position of an empty internal buffer.',
     '这是为了避免在像 Unix 这样的平台上产生混淆，其中操作系统可能返回空内部缓冲的新位置。'),
    ('Seeking always writes out the internal buffer before seeking.', '定位前总是会先写出内部缓冲。'),

    # ===== AsyncSeekExt rewind / stream_position =====
    ('This is convenience method, equivalent to <code>self.seek(SeekFrom::Start(0))</code>.',
     '这是便捷方法，等价于 <code>self.seek(SeekFrom::Start(0))</code>。'),
    ('This is equivalent to <code>self.seek(SeekFrom::Current(0))</code>.', '这等价于 <code>self.seek(SeekFrom::Current(0))</code>。'),

    # ===== AsyncWriteExt.write all =====
    ('Writes an entire buffer into this writer.', '将整个缓冲写入此写入器。'),
    ('Attempts to write an entire buffer into this writer.', '尝试将整个缓冲写入此写入器。'),
    ('If the return value is <code>Ok(n)</code> then it must be guaranteed that\n<code>n &lt;= buf.len()</code>. A return value of <code>0</code> typically means that the\nunderlying object is no longer able to accept bytes and will likely\nnot be able to in the future as well, or that the internal buffer is\nfull.',
     '若返回值为 <code>Ok(n)</code>，则必须保证 <code>n &lt;= buf.len()</code>。返回 <code>0</code> 通常意味着底层对象已无法接收字节，并且很可能将来也无法接收，或内部缓冲已满。'),
    ('Each call to <code>write</code> may generate an I/O error indicating that the\noperation could not be completed. If an error is returned then no bytes\nin the buffer were written to this writer.',
     '每次调用 <code>write</code> 都可能生成一个 I/O 错误，表明操作未能完成。若返回错误，则缓冲中的所有字节均未写入此写入器。'),
    ('Each call to write may generate an I/O error indicating that the\noperation could not be completed. If an error is returned then no bytes',
     '每次调用 write 都可能生成一个 I/O 错误，表明操作未能完成。若返回错误，则缓冲中的所有字节'),
    ('in the buffer were written to this writer.', '均未写入此写入器。'),
    ('A nonzero n value indicates that the buffer was filled in with n bytes of data from this writer.',
     '非零的 n 值表示此写入器向缓冲填充了 n 个字节的数据。'),
    ('This is an error where bytes have already been written but the writer has returned an error.',
     '这是一种错误：字节已经被写入，但写入器返回了错误。'),

    # ===== AsyncWriteExt.write_vectored full description =====
    ('Like <code>write</code>, except that it writes from a slice of buffers.',
     '与 <code>write</code> 类似，但从缓冲切片中写入。'),
    ('Data may be buffered if there is not enough space in the buffers, in\nwhich case the output stream may not be flushed.',
     '如果缓冲中没有足够的空间，数据可能会被缓冲，在这种情况下输出流可能不会被刷新。'),

    # ===== AsyncWriteExt.shutdown =====
    ('On Unix, this will close the write side of the socket. On Windows, this\nwill close the underlying TCP socket.',
     '在 Unix 上，这会关闭套接字的写端。在 Windows 上，这会关闭底层 TCP 套接字。'),
    ('If this method returns <code>Ok(())</code>, it is guaranteed that the value can be\ndropped safely.',
     '若此方法返回 <code>Ok(())</code>，则保证此值可以安全地丢弃。'),

    # ===== AsyncWriteExt.flush =====
    ('It is considered an error if not all bytes could be written due to\nI/O errors or EOF being reached.',
     '如果由于 I/O 错误或到达 EOF 而无法写入所有字节，则视为错误。'),

    # ===== AsyncBufReadExt.fill_buf on top doc =====
    ('This function is a lower-level call.', '此函数是较低级别的调用。'),
    ('It needs to be paired with the <code>consume</code> method to function properly.',
     '它需要与 <code>consume</code> 方法配合使用才能正常工作。'),
    ('When calling this method, none of the contents will be "read" in the sense that later calling <code>read</code> may return the same contents.',
     '调用此方法时，任何内容都不会被"读取"，即后续调用 <code>read</code> 仍可能返回相同的内容。'),
    ('As such, <code>consume</code> must be called with the number of bytes that are consumed from this buffer to ensure that the bytes are never returned twice.',
     '因此，必须使用从此缓冲消费的字节数调用 <code>consume</code>，以确保字节不会被返回两次。'),

    # ===== AsyncReadExt.read (full) =====
    ('Pulls some bytes from this source into the specified buffer,\nreturning how many bytes were read.',
     '从此源拉取一些字节到指定的缓冲中，返回读取的字节数。'),
    ('Pulls some bytes from this source into the specified buffer, returning how many bytes were read.',
     '从此源拉取一些字节到指定的缓冲中，返回读取的字节数。'),

    # ===== common process pieces =====
    ('Returns the OS-assigned process identifier associated with this child.', '返回与此子进程关联的、由操作系统分配的进程标识符。'),
    ('Returns the OS-assigned process identifier associated with this child\nwhile it is still running.',
     '返回与此子进程关联的、由操作系统分配的进程标识符（在子进程仍在运行时）。'),
    ('If the child has already been waited on, this will return <code>None</code>.',
     '若子进程已经被等待过，则此方法返回 <code>None</code>。'),

    # ===== process - more fragments =====
    ('Writes bytes into a sink.', '将字节写入汇。'),

    # ===== io/struct.BufReader long description =====
    ('It can be excessively inefficient to work directly with a <code>AsyncRead</code>\ninstance. A <code>BufReader</code> performs large, infrequent reads on the underlying\n<code>AsyncRead</code> and maintains an in-memory buffer of the results.',
     '直接使用 <code>AsyncRead</code> 实例可能非常低效。<code>BufReader</code> 对底层 <code>AsyncRead</code> 执行大而少的读取，并在内存中维护结果的缓冲。'),
    ('It can be excessively inefficient to work directly with a AsyncRead instance.', '直接使用 AsyncRead 实例可能非常低效。'),
    ('A <code>BufReader</code> performs large, infrequent reads on the underlying\n<code>AsyncRead</code> and maintains an in-memory buffer of the results.',
     '<code>BufReader</code> 对底层 <code>AsyncRead</code> 执行大而少的读取，并在内存中维护结果的缓冲。'),
    ('BufReader can improve the speed of programs that make *small* and\n*repeated* read calls to the same file or network socket. This happens\nbecause BufReader maintains an in-memory buffer of read data, allowing\nfewer actual calls to the underlying reader.',
     'BufReader 可提升对同一文件或网络套接字进行*小*且*重复*读取调用的程序的速度。其原理是 BufReader 在内存中维护读取数据的缓冲，从而减少对底层读取器的实际调用次数。'),
    ('<code>BufReader</code> can improve the speed of programs that make *small* and\n*repeated* read calls to the same file or network socket. This happens\nbecause <code>BufReader</code> maintains an in-memory buffer of read data, allowing\nfewer actual calls to the underlying reader.',
     '<code>BufReader</code> 可提升对同一文件或网络套接字进行*小*且*重复*读取调用的程序的速度。其原理是 <code>BufReader</code> 在内存中维护读取数据的缓冲，从而减少对底层读取器的实际调用次数。'),

    # ===== io/struct.BufWriter =====
    ('It can be excessively inefficient to work directly with a <code>AsyncWrite</code>\ninstance. A <code>BufWriter</code> performs large, infrequent writes on the underlying\n<code>AsyncWrite</code> and maintains an in-memory buffer of the results.',
     '直接使用 <code>AsyncWrite</code> 实例可能非常低效。<code>BufWriter</code> 对底层 <code>AsyncWrite</code> 执行大而少的写入，并在内存中维护结果的缓冲。'),
    ('It can be excessively inefficient to work directly with a AsyncWrite instance.', '直接使用 AsyncWrite 实例可能非常低效。'),

    # ===== AsyncBufReadExt.read_until description =====
    ('Reads all bytes into <code>buf</code> until the delimiter byte or EOF is reached.',
     '读取所有字节到 <code>buf</code>，直到遇到分隔字节或 EOF。'),
    ('Reads all bytes into <code>buf</code> until the delimiter byte or EOF is\nreached.', '读取所有字节到 <code>buf</code>，直到遇到分隔字节或 EOF。'),
    ('Reads all bytes into buf until the delimiter byte or EOF is reached.', '读取所有字节到 buf，直到遇到分隔字节或 EOF。'),
    ('Reads all bytes into buf until the delimiter byte or EOF is\nreached.', '读取所有字节到 buf，直到遇到分隔字节或 EOF。'),
    ('Reads all bytes until a newline (the 0xA byte) is reached, and append\nthem to the provided <code>String</code> buffer.',
     '读取所有字节直到遇到换行符（0xA 字节），并将它们追加到提供的 <code>String</code> 缓冲。'),
    ('Reads all bytes until a newline (the 0xA byte) is reached, and append them to the provided <code>String</code> buffer.',
     '读取所有字节直到遇到换行符（0xA 字节），并将它们追加到提供的 <code>String</code> 缓冲。'),
    ('Reads all bytes until a newline (the 0xA byte) is reached, and append\nthem to the provided buffer.',
     '读取所有字节直到遇到换行符（0xA 字节），并将它们追加到提供的缓冲。'),
    ('Reads all bytes until a newline (the 0xA byte) is reached, and append them to the provided buffer.',
     '读取所有字节直到遇到换行符（0xA 字节），并将它们追加到提供的缓冲。'),

    # ===== common fragments =====
    ('A wait is considered to have been performed if the future returned by\n<code>wait</code> was polled to completion.',
     '如果由 <code>wait</code> 返回的 Future 被轮询到完成，则认为已执行了一次等待。'),
    ('This function will continue to have the same return value after it has been called at least once.',
     '此函数至少被调用一次后，将继续返回相同的返回值。'),
    ('In particular, calling wait() more than once will not block the second\ntime if the child has already finished.',
     '特别是，若子进程已结束，多次调用 wait() 不会阻塞第二次调用。'),
    ('This function will also close any stdin handle to the child process.',
     '此函数还将关闭到子进程的 stdin handle。'),
    ('The std::process::Child type, defined in the standard library, has\nadditional methods that may be useful for getting information about the\nchild process, including its exit status.',
     '标准库中定义的 std::process::Child 类型还有其他方法可用于获取子进程信息，包括其退出状态。'),

    # ===== common docblock fragments =====
    ('Files implement <code>AsyncRead</code>:', 'File 实现 <code>AsyncRead</code>：'),
    ('Files implement <code>Read</code>:', 'File 实现 <code>Read</code>：'),
    ('Files implement AsyncRead:', 'File 实现 AsyncRead：'),
    ('Files implement Read:', 'File 实现 Read：'),

    # ===== AsyncWriteExt.flush details =====
    ('It is considered an error if not all bytes could be written due to\nI/O errors or EOF being reached.',
     '如果由于 I/O 错误或到达 EOF 而无法写入所有字节，则视为错误。'),

    # ===== AsyncWriteExt.shutdown details =====
    ('On Unix, this will close the write side of the socket.', '在 Unix 上，这会关闭套接字的写端。'),
    ('On Windows, this will close the underlying TCP socket.', '在 Windows 上，这会关闭底层 TCP 套接字。'),
    ('If this method returns Ok(()), it is guaranteed that the value can be\ndropped safely.', '若此方法返回 Ok(()), 则保证此值可以安全地丢弃。'),
    ('If this method returns <code>Ok(())</code>, it is guaranteed that the value can be dropped safely.',
     '若此方法返回 <code>Ok(())</code>，则保证此值可以安全地丢弃。'),

    # ===== io/AsyncReadExt.read_buf details =====
    ('Pulls some bytes from this source into the specified buffer,\nadvancing the buffer’s internal cursor.',
     '从此源拉取一些字节到指定的缓冲中，前进缓冲的内部游标。'),
    ('Pulls some bytes from this source into the specified buffer, advancing the buffer’s internal cursor.',
     '从此源拉取一些字节到指定的缓冲中，前进缓冲的内部游标。'),
    ('Pulls some bytes from this source into the specified buffer, advancing the buffer’s internal cursor.',
     '从此源拉取一些字节到指定的缓冲中，前进缓冲的内部游标。'),

    # ===== more fragments =====
    ('The handle for reading from the child’s standard error (stderr), if it\nhas been captured.',
     '子进程标准错误 (stderr) 的读取 handle（若已捕获）。'),
    ('The handle for reading from the child’s standard output (stdout), if it\nhas been captured.',
     '子进程标准输出 (stdout) 的读取 handle（若已捕获）。'),
    ('The handle for writing to the child’s standard input (stdin), if it has\nbeen captured.',
     '子进程标准输入 (stdin) 的写入 handle（若已捕获）。'),

    # ===== AsyncWriteExt details =====
    ('Writes a buffer into this writer, advancing the buffer’s internal\ncursor.', '将一个缓冲写入此写入器，前进缓冲的内部游标。'),
    ('Writes a buffer into this writer, advancing the buffer’s internal\ncursor.', '将一个缓冲写入此写入器，前进缓冲的内部游标。'),

    # ===== BufStream long description =====
    ('It can be excessively inefficient to work directly with a <code>AsyncRead</code> or\n<code>AsyncWrite</code>. A <code>BufStream</code> performs large, infrequent reads and writes on the\nunderlying stream and maintains an in-memory buffer of the results.',
     '直接使用 <code>AsyncRead</code> 或 <code>AsyncWrite</code> 可能非常低效。<code>BufStream</code> 对底层流执行大而少的读写，并在内存中维护结果的缓冲。'),
    ('It can be excessively inefficient to work directly with a AsyncRead or AsyncWrite. A BufStream performs large, infrequent reads and writes on the underlying stream and maintains an in-memory buffer of the results.',
     '直接使用 AsyncRead 或 AsyncWrite 可能非常低效。BufStream 对底层流执行大而少的读写，并在内存中维护结果的缓冲。'),
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

    print(f'Phase 5: {files_changed}/{total_files} files, {total_replacements} replacements')


if __name__ == '__main__':
    main()