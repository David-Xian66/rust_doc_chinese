#!/usr/bin/env python3
"""tokio 第九阶段：补译剩余含 <a> 链接与复杂 URL 的内容。"""
import os

BASE = r'D:/Administrator/Documents/Code/rust_doc_all/tokio'

PAIRS = [
    # === tokio::select! link wrapper ===
    ('<a href="../macros/select.html" title="macro tokio::select"><code>tokio::select!</code></a> statement and some other branch\ncompletes first, then some data may be lost.',
     '<a href="../macros/select.html" title="macro tokio::select"><code>tokio::select!</code></a> 语句中的事件，并且其他某个分支先完成，则可能丢失一些数据。'),
    ('<a href="../macros/select.html" title="macro tokio::select"><code>tokio::select!</code></a> statement and some other branch\ncompletes first, then some data may already have been\nread into <code>buf</code>.',
     '<a href="../macros/select.html" title="macro tokio::select"><code>tokio::select!</code></a> 语句中的事件，并且其他某个分支先完成，则可能已读取了一些数据到 <code>buf</code> 中。'),
    ('<a href="../macros/select.html" title="macro tokio::select"><code>tokio::select!</code></a> statement and some\nother branch completes first, then it is guaranteed that no data was read.',
     '<a href="../macros/select.html" title="macro tokio::select"><code>tokio::select!</code></a> 语句中的事件，并且其他某个分支先完成，则保证尚未读取任何数据。'),
    ('<a href="../macros/select.html" title="macro tokio::select"><code>tokio::select!</code></a> statement and some other branch\ncompletes first, then it is guaranteed that no data were read.',
     '<a href="../macros/select.html" title="macro tokio::select"><code>tokio::select!</code></a> 语句中的事件，并且其他某个分支先完成，则保证尚未读取任何数据。'),

    # === ErrorKind::UnexpectedEof link ===
    ('If the operation encounters an “end of file” before completely\nfilling the buffer, it returns an error of the kind\n<a href="https://doc.rust-lang.org/1.95.0/std/io/error/enum.ErrorKind.html#variant.UnexpectedEof" title="variant std::io::error::ErrorKind::UnexpectedEof"><code>ErrorKind::UnexpectedEof</code></a>. The contents of <code>buf</code> are unspecified\nin this case.',
     '若操作在完全填满缓冲之前遇到“文件结束”，则返回 <a href="https://doc.rust-lang.org/1.95.0/std/io/error/enum.ErrorKind.html#variant.UnexpectedEof" title="variant std::io::error::ErrorKind::UnexpectedEof"><code>ErrorKind::UnexpectedEof</code></a> 类型的错误。这种情况下 <code>buf</code> 的内容是未指定的。'),

    # === Files implement pattern with full URL ===
    ('<a href="../fs/struct.File.html" title="struct tokio::fs::File"><code>File</code></a>s implement <code>Read</code>:',
     '<a href="../fs/struct.File.html" title="struct tokio::fs::File"><code>File</code></a> 实现 <code>Read</code>：'),
    ('<a href="../fs/struct.File.html" title="struct tokio::fs::File"><code>File</code></a>s implement <code>AsyncRead</code>:',
     '<a href="../fs/struct.File.html" title="struct tokio::fs::File"><code>File</code></a> 实现 <code>AsyncRead</code>：'),
    ('<a href="../fs/struct.File.html" title="struct tokio::fs::File"><code>File</code></a>s implement <code>AsyncWrite</code>:',
     '<a href="../fs/struct.File.html" title="struct tokio::fs::File"><code>File</code></a> 实现 <code>AsyncWrite</code>：'),
    ('<a href="../fs/struct.File.html" title="struct tokio::fs::File"><code>File</code></a> implements <code>Read</code> and <a href="../../bytes/bytes_mut/struct.BytesMut.html" title="struct bytes::bytes_mut::BytesMut"><code>BytesMut</code></a> implements <code>BufMut</code>:',
     '<a href="../fs/struct.File.html" title="struct tokio::fs::File"><code>File</code></a> 实现 <code>Read</code>，<a href="../../bytes/bytes_mut/struct.BytesMut.html" title="struct bytes::bytes_mut::BytesMut"><code>BytesMut</code></a> 实现 <code>BufMut</code>：'),

    # === process/struct.Command.html methods ===
    ('Constructs a new <code>Command</code> for launching <code>program</code>.\nThe full path to the program can be specified.',
     '构造一个用于启动 <code>program</code> 的新 <code>Command</code>。\n可指定程序的完整路径。'),
    ('Constructs a new Command for launching the program at\npath program, with the following default configuration:',
     '构造一个用于启动 path 路径程序的新 Command，并采用以下默认配置：'),
    ('Constructs a new Command for launching the program at', '构造一个用于启动程序的新 Command，'),
    ('The full path to the program can be specified.', '可指定程序的完整路径。'),
    ('If program is not an absolute path, the PATH will be searched in\nan OS-defined way.',
     '若 program 不是绝对路径，将以操作系统定义的方式搜索 PATH。'),
    ('If program is not an absolute path, the PATH will be searched in the OS-defined way.',
     '若 program 不是绝对路径，将以操作系统定义的方式搜索 PATH。'),
    ('The search path to be used may be controlled by setting the\nPATH environment variable on the Command,\nbut this has some implementation limitations on Windows\n(see issue rust-lang/rust#37519).',
     '可通过在 Command 上设置 PATH 环境变量来控制要使用的搜索路径，\n但在 Windows 上有一些实现限制（参见 rust-lang/rust#37519）。'),
    ('The search path to be used may be controlled by setting the\nPATH environment variable on the Command,',
     '可通过在 Command 上设置 PATH 环境变量来控制要使用的搜索路径，'),
    ('but this has some implementation limitations on Windows\n(see issue rust-lang/rust#37519).',
     '但在 Windows 上有一些实现限制（参见 rust-lang/rust#37519）。'),
    ('Note that Tokio specific options will be lost. Currently, this only\napplies to <code>kill_on_drop</code>.',
     '请注意，tokio 特有的选项将丢失。目前，这仅影响 <code>kill_on_drop</code>。'),
    ('Note that Tokio specific options will be lost. Currently, this only applies to kill_on_drop.',
     '请注意，tokio 特有的选项将丢失。目前，这仅影响 kill_on_drop。'),
    ('Note that environment variable names are case-insensitive (but case-preserving) on Windows,\nand case-sensitive on all other platforms.',
     '请注意，在 Windows 上环境变量名称不区分大小写（但保留大小写），\n而在所有其他平台上区分大小写。'),
    ('Note that environment variable names are case-insensitive (but case-preserving) on Windows,',
     '请注意，在 Windows 上环境变量名称不区分大小写（但保留大小写），'),
    ('and case-sensitive on all other platforms.', '而在所有其他平台上区分大小写。'),
    ('Adds or updates multiple environment variable mappings.', '添加或更新多个环境变量映射。'),
    ('Clears the entire environment map for the child process.', '清除子进程的整个环境映射。'),
    ('Sets the child process to be killed when the <code>Command</code> is dropped.',
     '设置当 <code>Command</code> 被丢弃时，子进程将被杀死。'),
    ('This is checked in tokio’s runtime, so it does not need to be called from within a task.',
     '此检查在 tokio 的运行时中进行，因此不需要在任务中调用。'),
    ('Set the stdin handle to the child process.', '设置子进程的 stdin handle。'),
    ('Set the stdout handle to the child process.', '设置子进程的 stdout handle。'),
    ('Set the stderr handle to the child process.', '设置子进程的 stderr handle。'),
    ('Sets the child process to be spawned into a new session.', '设置子进程派生到新会话中。'),
    ('Sets the child process group.', '设置子进程组。'),
    ('On Unix, this will set the uid and euid of the child process.', '在 Unix 上，这会设置子进程的 uid 与 euid。'),
    ('On Unix, this will set the gid and egid of the child process.', '在 Unix 上，这会设置子进程的 gid 与 egid。'),
    ('On Unix, this sets the current working directory of the child process.',
     '在 Unix 上，这会设置子进程的当前工作目录。'),
    ('On Windows, this will set the create_no_window flag.', '在 Windows 上，这会设置 create_no_window 标志。'),
    ('On Windows, this sets the current working directory of the child process.',
     '在 Windows 上，这会设置子进程的当前工作目录。'),
    ('On Unix, this argument is required, and has no effect on Windows.',
     '在 Unix 上，此参数是必需的，在 Windows 上无效。'),
    ('Sets the <code>Stdio</code> to <code>Stdio::null()</code>.', '将 <code>Stdio</code> 设置为 <code>Stdio::null()</code>。'),
    ('Sets the <code>Stdio</code> to <code>Stdio::piped()</code>.', '将 <code>Stdio</code> 设置为 <code>Stdio::piped()</code>。'),
    ('Sets the <code>Stdio</code> to <code>Stdio::inherit()</code>.', '将 <code>Stdio</code> 设置为 <code>Stdio::inherit()</code>。'),
    ('Sets the <code>Stdio</code> to the given handle.', '将 <code>Stdio</code> 设置为给定的 handle。'),
    ('Set the <a href="struct.Command.html#method.uid" title="method tokio::process::Command::uid"><code>uid</code></a> for the child process.',
     '为子进程设置 <a href="struct.Command.html#method.uid" title="method tokio::process::Command::uid"><code>uid</code></a>。'),
    ('Set the <a href="struct.Command.html#method.gid" title="method tokio::process::Command::gid"><code>gid</code></a> for the child process.',
     '为子进程设置 <a href="struct.Command.html#method.gid" title="method tokio::process::Command::gid"><code>gid</code></a>。'),
    ('Set the current working directory of the child process.', '设置子进程的当前工作目录。'),
    ('Set the <a href="struct.Command.html#method.arg0" title="method tokio::process::Command::arg0"><code>arg0</code></a> of the child process.',
     '设置子进程的 <a href="struct.Command.html#method.arg0" title="method tokio::process::Command::arg0"><code>arg0</code></a>。'),
    ('For a brief description of the difference between this and <code>arg</code>, see <a href="struct.Command.html#method.arg" title="method tokio::process::Command::arg"><code>arg</code></a>.',
     '关于此与 <code>arg</code> 区别的简要描述，请参阅 <a href="struct.Command.html#method.arg" title="method tokio::process::Command::arg"><code>arg</code></a>。'),
    ('For a brief description of the difference between this and arg, see arg.',
     '关于此与 arg 区别的简要描述，请参阅 arg。'),

    # === fs/struct.OpenOptions.html long patterns ===
    ('All options are initially set to <code>false</code>.', '所有选项最初均设置为 <code>false</code>。'),
    ('All options are initially set to false.', '所有选项最初均设置为 false。'),
    ('This option, when true, will indicate that the file should be read-able if opened.',
     '当此选项为 true 时，表示如果打开，文件应可读。'),
    ('This option, when true, will indicate that the file should be write-able if opened.',
     '当此选项为 true 时，表示如果打开，文件应可写。'),
    ('This option, when true, means that writes will append to a file instead\nof overwriting previous contents.  Note that setting <code>.write(true).append(true)</code> has the same effect as setting only <code>.append(true)</code>.',
     '当此选项为 true 时，表示写入将追加到文件末尾，而不是覆盖先前的内容。注意，设置 <code>.write(true).append(true)</code> 的效果与仅设置 <code>.append(true)</code> 相同。'),
    ('This option is useful because there is a common situation, when running\nconfiguration scripts, where you want to create a file or do nothing if\nit already exists, but avoid the race condition of:\n\n1. Checking whether the file exists\n2. If it doesn’t, creating it\n\nbecause between the check and the create, another process may have\ncreated it.',
     '此选项很有用，因为在运行配置脚本时存在一种常见情况：希望创建文件，或在文件已存在时什么也不做，但要避免以下竞争条件：\n\n1. 检查文件是否存在\n2. 若不存在，则创建它\n\n因为在检查与创建之间，另一个进程可能已经创建了它。'),
    ('This option, when true, means that writes will append to a file instead\nof overwriting previous contents.  Note that setting .write(true).append(true) has the same effect as setting only .append(true).',
     '当此选项为 true 时，表示写入将追加到文件末尾，而不是覆盖先前的内容。注意，设置 .write(true).append(true) 的效果与仅设置 .append(true) 相同。'),
    ('Sets the option for read access.', '设置读访问选项。'),
    ('Sets the option for write access.', '设置写访问选项。'),
    ('Sets the option for the append mode.', '设置追加模式选项。'),
    ('Sets the option for truncating an existing file to zero length.', '设置将现有文件截断为零长度的选项。'),
    ('Sets the option for the read-write mode.', '设置读写模式选项。'),
    ('Sets the option for creating a new file.', '设置创建新文件的选项。'),
    ('Sets the option for creating a new file if it does not already exist.',
     '设置当文件不存在时创建新文件的选项。'),
    ('Sets the option for creating a new file or failing if the file already exists.',
     '设置创建新文件或若文件已存在则失败的选项。'),
    ('Sets the option for creating a new file or returning an error if the file already exists.',
     '设置创建新文件或若文件已存在则返回错误的选项。'),
    ('Sets the option for the custom flag.', '设置自定义标志选项。'),
    ('Sets the option for following symbolic links.', '设置跟随符号链接选项。'),

    # === fs/struct.File.html long descriptions ===
    ('See <a href="struct.OpenOptions.html"><code>OpenOptions</code></a> for more details.',
     '详见 <a href="struct.OpenOptions.html"><code>OpenOptions</code></a>。'),
    ('See <code>OpenOptions</code> for more details.', '详见 <code>OpenOptions</code>。'),
    ('See OpenOptions for more details.', '详见 OpenOptions。'),
    ('This function will return an error if called from outside of the Tokio runtime or if path does not already exist. Other errors may also be returned according to OpenOptions::open.',
     '若在 tokio 运行时外调用此函数，或若 path 不存在，此函数将返回错误。也可能根据 OpenOptions::open 返回其他错误。'),
    ('The <a href="trait.AsyncReadExt.html" title="trait tokio::io::AsyncReadExt"><code>read_to_end</code></a> method is defined on the <a href="trait.AsyncReadExt.html" title="trait tokio::io::AsyncReadExt"><code>AsyncReadExt</code></a> trait.',
     '<a href="trait.AsyncReadExt.html" title="trait tokio::io::AsyncReadExt"><code>read_to_end</code></a> 方法定义在 <a href="trait.AsyncReadExt.html" title="trait tokio::io::AsyncReadExt"><code>AsyncReadExt</code></a> 特性上。'),
    ('The <a href="trait.AsyncWriteExt.html" title="trait tokio::io::AsyncWriteExt"><code>write_all</code></a> method is defined on the <a href="trait.AsyncWriteExt.html" title="trait tokio::io::AsyncWriteExt"><code>AsyncWriteExt</code></a> trait.',
     '<a href="trait.AsyncWriteExt.html" title="trait tokio::io::AsyncWriteExt"><code>write_all</code></a> 方法定义在 <a href="trait.AsyncWriteExt.html" title="trait tokio::io::AsyncWriteExt"><code>AsyncWriteExt</code></a> 特性上。'),
    ('The read_to_end method is defined on the AsyncReadExt trait.', 'read_to_end 方法定义在 AsyncReadExt 特性上。'),
    ('The write_all method is defined on the AsyncWriteExt trait.', 'write_all 方法定义在 AsyncWriteExt 特性上。'),
    ('Attempts to open a file in read-only mode.', '尝试以只读模式打开文件。'),
    ('Opens a file in write-only mode.', '以只写模式打开文件。'),
    ('Opens a file in read-write mode.', '以读写模式打开文件。'),
    ('Truncates or creates a file in read-write mode.', '以读写模式截断或创建文件。'),
    ('Creates a file in read-write mode.', '以读写模式创建文件。'),
    ('Creates a new file in read-write mode, failing if the file already exists.',
     '以读写模式创建新文件；若文件已存在则失败。'),
    ('This function will create a file if it does not exist, and will truncate it if it does.',
     '若文件不存在，此函数将创建它；若已存在，则将其截断。'),
    ('This function will create a file if it does not exist, and will fail if it does.',
     '若文件不存在，此函数将创建它；若已存在，则失败。'),
    ('Results in an error if called from outside of the Tokio runtime or if the underlying create call results in an error.',
     '若在 tokio 运行时外调用，或底层 create 调用出错，则返回错误。'),
    ('This can also be written using <code>File::options().read(true).write(true).create_new(true).open(...)</code>.',
     '这也可以用 <code>File::options().read(true).write(true).create_new(true).open(...)</code> 来表达。'),

    # === io/struct.BufReader/BufWriter/BufStream ===
    ('The <code>BufReader</code> struct adds buffering to any reader.',
     '<code>BufReader</code> 结构体为任何读取器添加缓冲。'),
    ('The <code>BufWriter</code> struct adds buffering to any writer.',
     '<code>BufWriter</code> 结构体为任何写入器添加缓冲。'),
    ('The <code>BufStream</code> struct allows you to read and write from a bidirectional stream.',
     '<code>BufStream</code> 结构体允许你从一个双向流中读写。'),

    # === AsyncBufReadExt more ===
    ('Reads all bytes into <code>buf</code> until the delimiter byte or EOF is\nreached.', '读取所有字节到 <code>buf</code>，直到遇到分隔字节或 EOF。'),
    ('Reads all bytes into <code>buf</code> until the delimiter byte or EOF is reached.',
     '读取所有字节到 <code>buf</code>，直到遇到分隔字节或 EOF。'),
    ('Reads all bytes into buf until the delimiter byte or EOF is\nreached.',
     '读取所有字节到 buf，直到遇到分隔字节或 EOF。'),
    ('Reads all bytes into buf until the delimiter byte or EOF is reached.',
     '读取所有字节到 buf，直到遇到分隔字节或 EOF。'),
    ('Reads all bytes until a newline (the 0xA byte) is reached, and append\nthem to the provided <code>String</code> buffer.',
     '读取所有字节直到遇到换行符（0xA 字节），并将它们追加到提供的 <code>String</code> 缓冲。'),
    ('Reads all bytes until a newline (the 0xA byte) is reached, and append them to the provided <code>String</code> buffer.',
     '读取所有字节直到遇到换行符（0xA 字节），并将它们追加到提供的 <code>String</code> 缓冲。'),
    ('This function will read bytes from the underlying stream until the\ndelimiter or EOF is found. Once found, all bytes up to, and including,\nthe delimiter (if found) will be appended to <code>buf</code>.',
     '此函数将从底层流读取字节，直到找到分隔字节或 EOF。找到后，到此为止的所有字节（包括分隔字节本身，若找到的话）将被追加到 <code>buf</code>。'),
    ('This function will read bytes from the underlying stream until the delimiter or EOF is found. Once found, all bytes up to, and including, the delimiter (if found) will be appended to buf.',
     '此函数将从底层流读取字节，直到找到分隔字节或 EOF。找到后，到此为止的所有字节（包括分隔字节本身，若找到的话）将被追加到 buf。'),
    ('If successful, this function will return the total number of bytes read.',
     '若成功，此函数将返回读取的总字节数。'),

    # === AsyncSeekExt.seek ===
    ('Creates a future which will seek an IO object, and then yield the\nnew position in the object and the object itself.',
     '创建一个将定位 IO 对象，然后产出对象中的新位置以及对象本身的 Future。'),
    ('Creates a future which will return the current seek position from the\nunderlying object.',
     '创建一个 Future，返回底层对象的当前定位位置。'),
    ('Creates a future which will rewind to the beginning of the stream.',
     '创建一个将倒回到流开头的 Future。'),
    ('In the case of an error the buffer and the object will be discarded, with\nthe error yielded.',
     '若发生错误，缓冲与对象将被丢弃，并产出错误。'),
    ('In the case of an error the buffer and the object will be discarded, with the error yielded.',
     '若发生错误，缓冲与对象将被丢弃，并产出错误。'),

    # === io/struct.ReadHalf.html ===
    ('Checks if this <code>ReadHalf</code> and some <code>WriteHalf</code> were split from the same stream.',
     '检查此 <code>ReadHalf</code> 与某个 <code>WriteHalf</code> 是否是从同一个流拆分而来。'),
    ('Reunites with a previously split <code>WriteHalf</code>.', '与之前拆分的 <code>WriteHalf</code> 重新合并。'),
    ('If this <code>ReadHalf</code> and the given <code>WriteHalf</code> do not originate from the\nsame split operation this method will panic.',
     '若此 <code>ReadHalf</code> 与给定的 <code>WriteHalf</code> 不是来自同一次拆分操作，此方法将 panic。'),
    ('If this <code>ReadHalf</code> and the given <code>WriteHalf</code> do not originate from the same split operation this method will panic.',
     '若此 <code>ReadHalf</code> 与给定的 <code>WriteHalf</code> 不是来自同一次拆分操作，此方法将 panic。'),

    # === fs/struct.DirBuilder.html ===
    ('This is an async version of std::fs::DirBuilder::new.', '这是 std::fs::DirBuilder::new 的异步版本。'),
    ('This is an async version of std::fs::DirBuilder::recursive.', '这是 std::fs::DirBuilder::recursive 的异步版本。'),
    ('This is an async version of std::fs::DirBuilder::create.', '这是 std::fs::DirBuilder::create 的异步版本。'),
    ('Creates a new set of options with default mode/security settings for all\nplatforms and also non-recursive.',
     '创建一组对所有平台使用默认模式/安全设置，且非递归的新选项。'),
    ('Creates a new set of options with default mode/security settings for all platforms and also non-recursive.',
     '创建一组对所有平台使用默认模式/安全设置，且非递归的新选项。'),
    ('Indicates whether to create directories recursively (including all parent directories).\nParents that do not exist are created with the same security and permissions settings.',
     '指示是否递归创建目录（包括所有父目录）。不存在的父目录将使用相同的安全与权限设置创建。'),
    ('Indicates whether to create directories recursively (including all parent directories). Parents that do not exist are created with the same security and permissions settings.',
     '指示是否递归创建目录（包括所有父目录）。不存在的父目录将使用相同的安全与权限设置创建。'),

    # === fs/struct.ReadDir.html ===
    ('The <a href="struct.ReadDir.html"><code>ReadDir</code></a> struct is returned by <code>read_dir</code> and allows you to iterate\nover the entries in a directory.',
     '<a href="struct.ReadDir.html"><code>ReadDir</code></a> 结构体由 <code>read_dir</code> 返回，允许你迭代目录中的条目。'),
    ('The <code>ReadDir</code> struct is returned by <code>read_dir</code> and allows you to iterate over the entries in a directory.',
     '<code>ReadDir</code> 结构体由 <code>read_dir</code> 返回，允许你迭代目录中的条目。'),
    ('The ReadDir struct is returned by read_dir and allows you to iterate\nover the entries in a directory.',
     'ReadDir 结构体由 read_dir 返回，允许你迭代目录中的条目。'),
    ('Note that on multiple calls to <code>poll_next_entry</code>, only the <code>Waker</code> from\nthe <code>Context</code> passed to the most recent call is scheduled to receive a wakeup.',
     '请注意，在多次调用 <code>poll_next_entry</code> 时，只有最近一次调用传入的 <code>Context</code> 中的 <code>Waker</code> 会被调度以接收唤醒。'),
    ('When the method returns <code>Poll::Pending</code>, the <code>Waker</code> in the provided\n<code>Context</code> is scheduled to receive a wakeup when more bytes become available.',
     '当此方法返回 <code>Poll::Pending</code> 时，传入的 <code>Context</code> 中的 <code>Waker</code> 被调度以在更多字节可用时接收唤醒。'),
    ('When the method returns Poll::Pending, the Waker in the provided\nContext is scheduled to receive a wakeup when more bytes become',
     '当此方法返回 Poll::Pending 时，传入的 Context 中的 Waker 被调度以在更多字节可用时接收唤醒。'),
    ('When the method returns Poll::Pending, the Waker in the provided\nContext is scheduled to receive a wakeup when more bytes become available.',
     '当此方法返回 Poll::Pending 时，传入的 Context 中的 Waker 被调度以在更多字节可用时接收唤醒。'),
    ('Note that on multiple calls to poll_next_entry, only the Waker from\nthe Context passed to the most recent call is scheduled to receive a wakeup.',
     '请注意，在多次调用 poll_next_entry 时，只有最近一次调用传入的 Context 中的 Waker 会被调度以接收唤醒。'),
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

    # === process/struct.Child.html long ===
    ('Returns the OS-assigned process identifier associated with this child.',
     '返回与此子进程关联的、由操作系统分配的进程标识符。'),
    ('Returns the OS-assigned process identifier associated with this child\nwhile it is still running.',
     '返回与此子进程关联的、由操作系统分配的进程标识符（在子进程仍在运行时）。'),
    ('Returns the process identifier of the inner process.',
     '返回内部进程的进程标识符。'),
    ('If the child has already been waited on, this will return <code>None</code>.',
     '若子进程已经被等待过，则此方法返回 <code>None</code>。'),
    ('If the child has already been waited on, then this returns <code>None</code>.',
     '若子进程已经被等待过，则此方法返回 <code>None</code>。'),
    ('Once the child has been polled to completion this will return <code>None</code>.',
     '一旦子进程被轮询到完成，此方法将返回 <code>None</code>。'),
    ('If the child has already exited, then this returns <code>None</code>.',
     '若子进程已退出，则此方法返回 <code>None</code>。'),
    ('Returns the status of the child process, if it has already been polled to completion.',
     '返回子进程的状态（若它已被轮询到完成）。'),
    ('This function is cancel safe.', '此函数是取消安全的。'),
    ('This function will continue to have the same return value after it has been called at least once.',
     '此函数至少被调用一次后，将继续返回相同的返回值。'),
    ('In particular, calling wait() more than once will not block the second time if the child has already finished.',
     '特别是，若子进程已结束，多次调用 wait() 不会阻塞第二次调用。'),

    # === signal/windows/CtrlBreak/CtrlC/etc ===
    ('Although this returns <code>Option&lt;()&gt;</code>, it will never actually return <code>None</code>.\nThis was accidentally exposed and would be a breaking change to be removed.',
     '尽管此函数返回 <code>Option&lt;()&gt;</code>，但实际上永远不会返回 <code>None</code>。\n这是意外暴露的，要删除将是一个破坏性变更。'),
    ('Although this returns Option&lt;()&gt;, it will never actually return None.\nThis was accidentally exposed and would be a breaking change to be removed.',
     '尽管此函数返回 Option&lt;()&gt;，但实际上永远不会返回 None。\n这是意外暴露的，要删除将是一个破坏性变更。'),
    ('Polling from a manually implemented future', '从手动实现的 Future 轮询'),
    ('Polls to receive the next signal notification event, outside of an\nasync context.', '在异步上下文之外轮询以接收下一个信号通知事件。'),
    ('Polls to receive the next signal notification event, outside of an async context.',
     '在异步上下文之外轮询以接收下一个信号通知事件。'),

    # === AsyncWriteExt descriptions ===
    ('This function will attempt to write the entire contents of buf, but\nwill return an error if the underlying AsyncWrite instance reaches EOF\nbefore completing.',
     '此函数将尝试写入 buf 的全部内容，但如果底层 AsyncWrite 实例在完成前到达 EOF，则返回错误。'),
    ('This function will not write all of the data to the underlying writer, however it will write as much as possible without triggering a <code>Poll::Pending</code> from the underlying writer.',
     '此函数不会将所有数据写入底层写入器，但是它会在不触发底层写入器的 <code>Poll::Pending</code> 的前提下写入尽可能多的数据。'),
    ('Writes a buffer into this writer, returning how many bytes were\nwritten.', '将一个缓冲写入此写入器，返回写入的字节数。'),
    ('Writes a buffer into this writer, returning how many bytes were written.',
     '将一个缓冲写入此写入器，返回写入的字节数。'),
    ('Writes a buffer into this writer, advancing the buffer’s internal\ncursor.', '将一个缓冲写入此写入器，前进缓冲的内部游标。'),
    ('Writes a buffer into this writer, advancing the buffer’s internal cursor.',
     '将一个缓冲写入此写入器，前进缓冲的内部游标。'),
    ('Writes a buffer into this writer, advancing the buffer’s internal cursor.',
     '将一个缓冲写入此写入器，前进缓冲的内部游标。'),
    ('Attempts to write an entire buffer into this writer.', '尝试将整个缓冲写入此写入器。'),
    ('Writes an entire buffer into this writer.', '将整个缓冲写入此写入器。'),

    # === AsyncReadExt.description ===
    ('Reads bytes from a source.\nImplemented as an extension trait, adding utility methods to all\n<code>AsyncRead</code> types. Callers will tend to import this trait instead of\n<code>AsyncRead</code>',
     '从源读取字节。\n作为扩展特性实现，向所有 <code>AsyncRead</code> 类型添加工具方法。调用者通常会导入本特性而非 <code>AsyncRead</code>'),
    ('Writes bytes to a sink.\nImplemented as an extension trait, adding utility methods to all\n<code>AsyncWrite</code> types. Callers will tend to import this trait instead of\n<code>AsyncWrite</code>',
     '将字节写入汇。\n作为扩展特性实现，向所有 <code>AsyncWrite</code> 类型添加工具方法。调用者通常会导入本特性而非 <code>AsyncWrite</code>'),
    ('Asynchronously reads bytes from a source. Implemented as an extension trait, adding utility methods to all\n<code>AsyncBufRead</code> types.',
     '从源异步读取字节。作为扩展特性实现，向所有 <code>AsyncBufRead</code> 类型添加工具方法。'),
    ('Asynchronously seeks to a position in a stream. Implemented as an extension trait, adding utility methods to all\n<code>AsyncSeek</code> types.',
     '在流中异步定位到指定位置。作为扩展特性实现，向所有 <code>AsyncSeek</code> 类型添加工具方法。'),

    # === chain / take method first line ===
    ('Creates a new <code>AsyncRead</code> instance that chains this stream with\n<code>next</code>.',
     '创建一个新的 <code>AsyncRead</code> 实例，将此流与 <code>next</code> 链接起来。'),
    ('Creates a new AsyncRead instance that chains this stream with\nnext.',
     '创建一个新的 AsyncRead 实例，将此流与 next 链接起来。'),

    # === read_to_end full ===
    ('Reads all bytes until EOF in this source, placing them into <code>buf</code>.',
     '从此源读取所有字节直到 EOF，将它们放入 <code>buf</code>。'),
    ('Reads all bytes until EOF in this source, appending them to <code>buf</code>.',
     '从此源读取所有字节直到 EOF，将它们追加到 <code>buf</code>。'),
    ('All bytes read from this source will be appended to the specified\nbuffer <code>buf</code>. This function will continuously call <code>read()</code> to\nappend more data to <code>buf</code> until <code>read()</code> returns <code>Ok(0)</code>.',
     '从此源读取的所有字节都将追加到指定的缓冲 <code>buf</code> 中。此函数会持续调用 <code>read()</code> 将更多数据追加到 <code>buf</code>，直到 <code>read()</code> 返回 <code>Ok(0)</code>。'),
    ('If a read error is encountered then the <code>read_to_end</code> operation\nimmediately completes. Any bytes which have already been read will\nbe appended to <code>buf</code>.',
     '若遇到读取错误，<code>read_to_end</code> 操作将立即完成。已读取的所有字节将追加到 <code>buf</code>。'),

    # === read_to_string full ===
    ('If successful, the number of bytes which were read and appended to\n<code>buf</code> is returned.',
     '若成功，返回已读取并追加到 <code>buf</code> 的字节数。'),
    ('If the data in this stream is <em>not</em> valid UTF-8 then an error is\nreturned and <code>buf</code> is unchanged.',
     '若此流中的数据不是有效的 UTF-8，则返回错误且 <code>buf</code> 保持不变。'),
    ('See <code>read_to_end</code> for other error semantics.', '其他错误语义请参阅 <code>read_to_end</code>。'),
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

    print(f'Phase 9: {files_changed}/{total_files} files, {total_replacements} replacements')


if __name__ == '__main__':
    main()