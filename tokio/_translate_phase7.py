#!/usr/bin/env python3
"""tokio 第七阶段：补译剩余未翻译内容（含 <em> 标签、<code>...</code> 嵌套等）。"""
import os

BASE = r'D:/Administrator/Documents/Code/rust_doc_all/tokio'

PAIRS = [
    # === With <em> tags ===
    ('No guarantees are provided about the contents of <code>buf</code> when this\nfunction is called, implementations cannot rely on any property of the\ncontents of <code>buf</code> being true. It is recommended that <em>implementations</em>\nonly write data to <code>buf</code> instead of reading its contents.',
     '调用此函数时，不保证 <code>buf</code> 的内容，实现不能依赖 <code>buf</code> 内容的任何属性。建议<em>实现</em>仅向 <code>buf</code> 写入数据，而不是读取其内容。'),
    ('Correspondingly, however, <em>callers</em> of this method may not assume\nany guarantees about how the implementation uses <code>buf</code>. It is\npossible that the code that’s supposed to write to the buffer might\nalso read from it.',
     '相应地，但是，此方法的<em>调用者</em>不能假设实现使用 <code>buf</code> 的方式的任何保证。打算写入缓冲的代码也可能从其中读取。'),
    ('Correspondingly, however, callers of this method may not assume\nany guarantees about how the implementation uses buf. It is\npossible that the code that’s supposed to write to the buffer might\nalso read from it.',
     '相应地，但是，此方法的调用者不能假设实现使用 buf 的方式的任何保证。打算写入缓冲的代码也可能从其中读取。'),
    ('Correspondingly, however, callers of this method may not assume\nany guarantees about how the implementation uses buf. It is\npossible that the code that��s supposed to write to the buffer might\nalso read from it.',
     '相应地，但是，此方法的调用者不能假设实现使用 buf 的方式的任何保证。打算写入缓冲的代码也可能从其中读取。'),

    # === read_exact full details ===
    ('If the operation encounters an "end of file" before completely\nfilling the buffer, it returns an error of the kind\n<code>ErrorKind::UnexpectedEof</code>. The contents of <code>buf</code> are unspecified\nin this case.',
     '若操作在完全填满缓冲之前遇到“文件结束”，则返回 <code>ErrorKind::UnexpectedEof</code> 类型的错误。这种情况下 <code>buf</code> 的内容是未指定的。'),
    ('If the operation encounters an "end of file" before completely\nfilling the buffer, it returns an error of the kind\nErrorKind::UnexpectedEof. The contents of buf are unspecified\nin this case.',
     '若操作在完全填满缓冲之前遇到“文件结束”，则返回 ErrorKind::UnexpectedEof 类型的错误。这种情况下 buf 的内容是未指定的。'),
    ('This method is not cancellation safe. If the method is used as the\nevent in a <code>tokio::select!</code> statement and some\nother branch completes first, then some data may already have been\nread into <code>buf</code>.',
     '此方法不是取消安全的。如果将此方法用作 <code>tokio::select!</code> 语句中的事件，并且其他某个分支先完成，则可能已读取了一些数据到 <code>buf</code> 中。'),
    ('This method is not cancellation safe. If the method is used as the event in a <code>tokio::select!</code> statement and some other branch completes first, then some data may already have been read into <code>buf</code>.',
     '此方法不是取消安全的。如果将此方法用作 <code>tokio::select!</code> 语句中的事件，并且其他某个分支先完成，则可能已读取了一些数据到 <code>buf</code> 中。'),
    ('This method is not cancellation safe. If the method is used as the\nevent in a tokio::select! statement and some\nother branch completes first, then some data may already have been\nread into buf.',
     '此方法不是取消安全的。如果将此方法用作 tokio::select! 语句中的事件，并且其他某个分支先完成，则可能已读取了一些数据到 buf 中。'),

    # === read_uN cancel-safety pattern ===
    ('This method is not cancellation safe. If the method is used as the\nevent in a <code>tokio::select!</code> statement and some\nother branch completes first, then some data may be lost.',
     '此方法不是取消安全的。如果将此方法用作 <code>tokio::select!</code> 语句中的事件，并且其他某个分支先完成，则可能丢失一些数据。'),
    ('This method is not cancellation safe. If the method is used as the event in a <code>tokio::select!</code> statement and some other branch completes first, then some data may be lost.',
     '此方法不是取消安全的。如果将此方法用作 <code>tokio::select!</code> 语句中的事件，并且其他某个分支先完成，则可能丢失一些数据。'),

    # === code labels ===
    ('Read unsigned 8 bit integers from an <code>AsyncRead</code>:',
     '从 <code>AsyncRead</code> 读取无符号 8 位整数：'),
    ('Read unsigned 8 bit integers from an AsyncRead:',
     '从 AsyncRead 读取无符号 8 位整数：'),
    ('Read unsigned 16 bit big-endian integers from a <code>AsyncRead</code>:',
     '从 <code>AsyncRead</code> 读取无符号 16 位大端整数：'),
    ('Read unsigned 16 bit big-endian integers from a AsyncRead:',
     '从 AsyncRead 读取无符号 16 位大端整数：'),
    ('Read signed 16 bit big-endian integers from a <code>AsyncRead</code>:',
     '从 <code>AsyncRead</code> 读取有符号 16 位大端整数：'),
    ('Read signed 16 bit big-endian integers from a AsyncRead:',
     '从 AsyncRead 读取有符号 16 位大端整数：'),
    ('Read unsigned 32-bit big-endian integers from a <code>AsyncRead</code>:',
     '从 <code>AsyncRead</code> 读取无符号 32 位大端整数：'),
    ('Read unsigned 32-bit big-endian integers from a AsyncRead:',
     '从 AsyncRead 读取无符号 32 位大端整数：'),
    ('Read signed 32-bit big-endian integers from a <code>AsyncRead</code>:',
     '从 <code>AsyncRead</code> 读取有符号 32 位大端整数：'),
    ('Read signed 32-bit big-endian integers from a AsyncRead:',
     '从 AsyncRead 读取有符号 32 位大端整数：'),
    ('Read unsigned 64-bit big-endian integers from a <code>AsyncRead</code>:',
     '从 <code>AsyncRead</code> 读取无符号 64 位大端整数：'),
    ('Read unsigned 64-bit big-endian integers from a AsyncRead:',
     '从 AsyncRead 读取无符号 64 位大端整数：'),
    ('Read signed 64-bit big-endian integers from a <code>AsyncRead</code>:',
     '从 <code>AsyncRead</code> 读取有符号 64 位大端整数：'),
    ('Read signed 64-bit big-endian integers from a AsyncRead:',
     '从 AsyncRead 读取有符号 64 位大端整数：'),
    ('Read unsigned 128-bit big-endian integers from a <code>AsyncRead</code>:',
     '从 <code>AsyncRead</code> 读取无符号 128 位大端整数：'),
    ('Read unsigned 128-bit big-endian integers from a AsyncRead:',
     '从 AsyncRead 读取无符号 128 位大端整数：'),
    ('Read signed 128-bit big-endian integers from a <code>AsyncRead</code>:',
     '从 <code>AsyncRead</code> 读取有符号 128 位大端整数：'),
    ('Read signed 128-bit big-endian integers from a AsyncRead:',
     '从 AsyncRead 读取有符号 128 位大端整数：'),
    ('Read 32-bit floating point type from a <code>AsyncRead</code>:',
     '从 <code>AsyncRead</code> 读取 32 位浮点类型：'),
    ('Read 32-bit floating point type from a AsyncRead:',
     '从 AsyncRead 读取 32 位浮点类型：'),
    ('Read 64-bit floating point type from a <code>AsyncRead</code>:',
     '从 <code>AsyncRead</code> 读取 64 位浮点类型：'),
    ('Read 64-bit floating point type from a AsyncRead:',
     '从 AsyncRead 读取 64 位浮点类型：'),
    ('Read unsigned 16 bit little-endian integers from a <code>AsyncRead</code>:',
     '从 <code>AsyncRead</code> 读取无符号 16 位小端整数：'),
    ('Read unsigned 16 bit little-endian integers from a AsyncRead:',
     '从 AsyncRead 读取无符号 16 位小端整数：'),
    ('Read signed 16 bit little-endian integers from a <code>AsyncRead</code>:',
     '从 <code>AsyncRead</code> 读取有符号 16 位小端整数：'),
    ('Read signed 16 bit little-endian integers from a AsyncRead:',
     '从 AsyncRead 读取有符号 16 位小端整数：'),
    ('Read unsigned 32-bit little-endian integers from a <code>AsyncRead</code>:',
     '从 <code>AsyncRead</code> 读取无符号 32 位小端整数：'),
    ('Read unsigned 32-bit little-endian integers from a AsyncRead:',
     '从 AsyncRead 读取无符号 32 位小端整数：'),
    ('Read signed 32-bit little-endian integers from a <code>AsyncRead</code>:',
     '从 <code>AsyncRead</code> 读取有符号 32 位小端整数：'),
    ('Read signed 32-bit little-endian integers from a AsyncRead:',
     '从 AsyncRead 读取有符号 32 位小端整数：'),
    ('Read unsigned 64-bit little-endian integers from a <code>AsyncRead</code>:',
     '从 <code>AsyncRead</code> 读取无符号 64 位小端整数：'),
    ('Read unsigned 64-bit little-endian integers from a AsyncRead:',
     '从 AsyncRead 读取无符号 64 位小端整数：'),
    ('Read signed 64-bit little-endian integers from a <code>AsyncRead</code>:',
     '从 <code>AsyncRead</code> 读取有符号 64 位小端整数：'),
    ('Read signed 64-bit little-endian integers from a AsyncRead:',
     '从 AsyncRead 读取有符号 64 位小端整数：'),
    ('Read unsigned 128-bit little-endian integers from a <code>AsyncRead</code>:',
     '从 <code>AsyncRead</code> 读取无符号 128 位小端整数：'),
    ('Read unsigned 128-bit little-endian integers from a AsyncRead:',
     '从 AsyncRead 读取无符号 128 位小端整数：'),
    ('Read signed 128-bit little-endian integers from a <code>AsyncRead</code>:',
     '从 <code>AsyncRead</code> 读取有符号 128 位小端整数：'),
    ('Read signed 128-bit little-endian integers from a AsyncRead:',
     '从 AsyncRead 读取有符号 128 位小端整数：'),

    # === AsyncReadExt.read return value scenarios ===
    ('If the return value of this method is <code>Ok(n)</code>, then it must be\nguaranteed that <code>0 &lt;= n &lt;= buf.len()</code>. A nonzero <code>n</code> value indicates\nthat the buffer <code>buf</code> has been filled in with <code>n</code> bytes of data from\nthis source. If <code>n</code> is <code>0</code>, then it can indicate one of two\nscenarios:',
     '若此方法的返回值为 <code>Ok(n)</code>，则必须保证 <code>0 &lt;= n &lt;= buf.len()</code>。非零的 <code>n</code> 值表示缓冲 <code>buf</code> 已从该源填充了 <code>n</code> 个字节的数据。若 <code>n</code> 为 <code>0</code>，则可能表示以下两种情况之一：'),

    # === Lines for read_uN/iN (varied) ===
    ('Files implement <code>AsyncRead</code>:', 'File 实现 <code>AsyncRead</code>：'),
    ('Files implement AsyncRead:', 'File 实现 AsyncRead：'),
    ('Files implement <code>Read</code>:', 'File 实现 <code>Read</code>：'),
    ('Files implement Read:', 'File 实现 Read：'),
    ('File implements <code>Read</code> and <code>BytesMut</code> implements <code>BufMut</code>:',
     'File 实现 <code>Read</code>，<code>BytesMut</code> 实现 <code>BufMut</code>：'),
    ('File implements Read and BytesMut implements BufMut:',
     'File 实现 Read，BytesMut 实现 BufMut：'),

    # === process/struct.Child.html details ===
    ('Returns the process identifier of the inner process.',
     '返回内部进程的进程标识符。'),
    ('Returns the OS-assigned process identifier associated with this child.',
     '返回与此子进程关联的、由操作系统分配的进程标识符。'),
    ('Returns the OS-assigned process identifier associated with this child\nwhile it is still running.',
     '返回与此子进程关联的、由操作系统分配的进程标识符（在子进程仍在运行时）。'),
    ('If the child has already been waited on, this will return <code>None</code>.',
     '若子进程已经被等待过，则此方法返回 <code>None</code>。'),
    ('If the child has already been waited on, then this returns <code>None</code>.',
     '若子进程已经被等待过，则此方法返回 <code>None</code>。'),
    ('Once the child has been polled to completion this will return <code>None</code>.',
     '一旦子进程被轮询到完成，此方法将返回 <code>None</code>。'),
    ('If the child has already exited, then this returns <code>None</code>.',
     '若子进程已退出，则此方法返回 <code>None</code>。'),

    # === process/struct.Command.html details ===
    ('Inserts or updates an explicit environment variable mapping. This method allows you add an environment variable mapping to an\nenvironment for the child process, replacing any previous value for the\ncorresponding key. To control the environment of the child process\nwithout affecting the parent process, see <code>env_clear</code>.',
     '插入或更新一个显式的环境变量映射。此方法允许向子进程的环境添加一个环境变量映射，替换对应键的先前值。若要在不影响父进程的情况下控制子进程的环境，请参阅 <code>env_clear</code>。'),
    ('Removes an explicit environment variable mapping. To remove a\nmapping for a key which has not been previously set, this method has\nno effect.',
     '删除一个显式的环境变量映射。对于之前未设置的键，调用此方法无效。'),
    ('Append literal text to the command line without any quoting or escaping.',
     '向命令行追加字面文本，不进行任何引号或转义。'),
    ('This is useful for passing arguments to <code>cmd.exe /c</code>, which doesn’t follow\n<code>CommandLineToArgvW</code> escaping rules.',
     '这对于将参数传递给 <code>cmd.exe /c</code> 很有用，因为它不遵循 <code>CommandLineToArgvW</code> 的转义规则。'),
    ('Only one argument can be passed per use. So instead of:',
     '每次调用只能传递一个参数。因此，请勿这样：'),

    # === io/struct.BufReader/BufWriter/BufStream ===
    ('The <code>BufReader</code> struct adds buffering to any reader.',
     '<code>BufReader</code> 结构体为任何读取器添加缓冲。'),
    ('The <code>BufWriter</code> struct adds buffering to any writer.',
     '<code>BufWriter</code> 结构体为任何写入器添加缓冲。'),
    ('The <code>BufStream</code> struct allows you to read and write from a bidirectional stream.',
     '<code>BufStream</code> 结构体允许你从一个双向流中读写。'),

    # === AsyncReadExt.read return ===
    ('Pulls some bytes from this source into the specified buffer,\nreturning how many bytes were read.',
     '从此源拉取一些字节到指定的缓冲中，返回读取的字节数。'),
    ('Pulls some bytes from this source into the specified buffer, returning how many bytes were read.',
     '从此源拉取一些字节到指定的缓冲中，返回读取的字节数。'),
    ('Pulls some bytes from this source into the specified buffer,\nadvancing the buffer’s internal cursor.',
     '从此源拉取一些字节到指定的缓冲中，前进缓冲的内部游标。'),
    ('Pulls some bytes from this source into the specified buffer, advancing the buffer’s internal cursor.',
     '从此源拉取一些字节到指定的缓冲中，前进缓冲的内部游标。'),
    ('Pulls some bytes from this source into the specified buffer, advancing the buffer’s internal cursor.',
     '从此源拉取一些字节到指定的缓冲中，前进缓冲的内部游标。'),

    # === AsyncReadExt.read_to_end ===
    ('Reads all bytes until EOF in this source, placing them into <code>buf</code>.',
     '从此源读取所有字节直到 EOF，将它们放入 <code>buf</code>。'),
    ('Reads all bytes until EOF in this source, appending them to <code>buf</code>.',
     '从此源读取所有字节直到 EOF，将它们追加到 <code>buf</code>。'),

    # === AsyncWriteExt top docblock ===
    ('Writes bytes to a sink. Implemented as an extension trait, adding utility methods to all AsyncWrite types. Callers will tend to import this trait instead of AsyncWrite',
     '将字节写入汇。作为扩展特性实现，向所有 AsyncWrite 类型添加工具方法。调用者通常会导入本特性而非 AsyncWrite'),

    # === AsyncWriteExt.write (extended) ===
    ('This function will not write all of the data to the underlying writer, however it will write as much as possible without triggering a <code>Poll::Pending</code> from the underlying writer.',
     '此函数不会将所有数据写入底层写入器，但是它会在不触发底层写入器的 <code>Poll::Pending</code> 的前提下写入尽可能多的数据。'),
    ('This function will not write all of the data to the underlying writer, however it will write as much as possible without triggering a Poll::Pending from the underlying writer.',
     '此函数不会将所有数据写入底层写入器，但是它会在不触发底层写入器的 Poll::Pending 的前提下写入尽可能多的数据。'),
    ('If your code is required to be fully forward compatible with futures that may be <code>Pending</code>, calling this method will suffice.',
     '如果你的代码需要与可能处于 <code>Pending</code> 状态的 Future 完全向前兼容，则调用此方法即可。'),
    ('If you want to be fully compatible with <code>Pending</code> state, you should call <code>write</code> in a loop.',
     '如果你希望与 <code>Pending</code> 状态完全兼容，应在循环中调用 <code>write</code>。'),

    # === AsyncWriteExt.write_buf ===
    ('Writes a buffer into this writer, advancing the buffer’s internal cursor.',
     '将一个缓冲写入此写入器，前进缓冲的内部游标。'),

    # === AsyncWriteExt.write_all_buf ===
    ('Attempts to write an entire buffer into this writer.',
     '尝试将整个缓冲写入此写入器。'),
    ('This will repeatedly call <code>write_buf</code> until the buffer is empty or an error occurs.',
     '此方法会重复调用 <code>write_buf</code>，直到缓冲为空或发生错误。'),
    ('If the underlying writer supports vectored writes, this method will use those to write all the data.',
     '如果底层写入器支持向量化写入，此方法将使用它们来写入所有数据。'),

    # === io/struct.SimplexStream.html ===
    ('Creates unidirectional buffer that acts like in memory pipe. To create split',
     '创建一个像内存管道一样的单向缓冲。要创建读写分离的拆分版本，'),
    ('version with separate reader and writer you can use simplex function.',
     '请使用 simplex 函数。'),
    ('Creating a unidirectional buffer that acts like an in-memory pipe.',
     '创建一个像内存管道一样的单向缓冲。'),

    # === AsyncBufReadExt more details ===
    ('Reads all bytes into <code>buf</code> until the delimiter byte or EOF is\nreached.',
     '读取所有字节到 <code>buf</code>，直到遇到分隔字节或 EOF。'),
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

    # === fs/struct.File.html methods - long docs ===
    ('Opens a file in read-write mode.', '以读写模式打开文件。'),
    ('This function will create a file if it does not exist, and will fail if\nit does.',
     '若文件不存在，此函数将创建它；若已存在，则失败。'),

    # === fs/struct.OpenOptions.html extras ===
    ('This option, when true, means that writes will append to a file instead\nof overwriting previous contents.  Note that setting <code>.write(true).append(true)</code> has the same effect as setting only <code>.append(true)</code>.',
     '当此选项为 true 时，表示写入将追加到文件末尾，而不是覆盖先前的内容。注意，设置 <code>.write(true).append(true)</code> 的效果与仅设置 <code>.append(true)</code> 相同。'),
    ('This option, when true, means that writes will append to a file instead\nof overwriting previous contents.  Note that setting .write(true).append(true) has the same effect as setting only .append(true).',
     '当此选项为 true 时，表示写入将追加到文件末尾，而不是覆盖先前的内容。注意，设置 .write(true).append(true) 的效果与仅设置 .append(true) 相同。'),
    ('This option is useful because there is a common situation, when running\nconfiguration scripts, where you want to create a file or do nothing if\nit already exists, but avoid the race condition of:\n\n1. Checking whether the file exists\n2. If it doesn\'t, creating it\n\nbecause between the check and the create, another process may have\ncreated it.',
     '此选项很有用，因为在运行配置脚本时存在一种常见情况：希望创建文件，或在文件已存在时什么也不做，但要避免以下竞争条件：\n\n1. 检查文件是否存在\n2. 若不存在，则创建它\n\n因为在检查与创建之间，另一个进程可能已经创建了它。'),
    ('This option is useful because there is a common situation, when running\nconfiguration scripts, where you want to create a file or do nothing if\nit already exists, but avoid the race condition of:\n\n1. Checking whether the file exists\n2. If it doesn’t, creating it\n\nbecause between the check and the create, another process may have\ncreated it.',
     '此选项很有用，因为在运行配置脚本时存在一种常见情况：希望创建文件，或在文件已存在时什么也不做，但要避免以下竞争条件：\n\n1. 检查文件是否存在\n2. 若不存在，则创建它\n\n因为在检查与创建之间，另一个进程可能已经创建了它。'),

    # === BufStream take/consume examples ===
    ('Examples', '示例'),
    ('Errors', '错误'),
    ('The position used for <code>seeking</code> with <code>SeekFrom::Current(_)</code> is the\nposition the underlying stream would be at if the <code>BufStream</code> had no\ninternal buffer.',
     '使用 <code>SeekFrom::Current(_)</code> 定位时，所用的位置是底层流在 <code>BufStream</code> 没有内部缓冲的情况下所处的位置。'),
    ('The position used for seeking with SeekFrom::Current(_) is the\nposition the underlying stream would be at if the BufStream had no\ninternal buffer.',
     '使用 SeekFrom::Current(_) 定位时，所用的位置是底层流在 BufStream 没有内部缓冲的情况下所处的位置。'),
    ('The position used for seeking with SeekFrom::Current(_) is the\nposition the underlying stream would be at if the BufStream had no\ninternal buffer.\n\nThe position used for seeking with SeekFrom::Current(_) is the\nposition the underlying reader would be at if the BufReader had no',
     '使用 SeekFrom::Current(_) 定位时，所用的位置是底层流在 BufStream 没有内部缓冲的情况下所处的位置。\n\n使用 SeekFrom::Current(_) 定位时，所用的位置是底层读取器在 BufReader 没有内部缓冲的情况下所处的位置。'),

    # === AsyncSeekExt details ===
    ('Creates a future which will seek an IO object, and then yield the\nnew position in the object and the object itself.',
     '创建一个将定位 IO 对象，然后产出对象中的新位置以及对象本身的 Future。'),
    ('See <a href="trait.AsyncSeek.html"><code>AsyncSeek</code></a> for more details.',
     '详见 <a href="trait.AsyncSeek.html"><code>AsyncSeek</code></a>。'),
    ('See <code>AsyncSeek</code> for more details.', '详见 <code>AsyncSeek</code>。'),
    ('See AsyncSeek for more details.', '详见 AsyncSeek。'),
    ('Seeking always discards the internal buffer, even if the seek position\nfalls within it.',
     '定位总是会丢弃内部缓冲，即使定位位置落在缓冲范围内。'),
    ('Seeking always discards the internal buffer, even if the seek position falls within it.',
     '定位总是会丢弃内部缓冲，即使定位位置落在缓冲范围内。'),
    ('This is done to avoid confusion on platforms like Unix where the OS\ncan return the new position of an empty internal buffer.',
     '这是为了避免在像 Unix 这样的平台上产生混淆，其中操作系统可能返回空内部缓冲的新位置。'),
    ('This is done to avoid confusion on platforms like Unix where the OS can return the new position of an empty internal buffer.',
     '这是为了避免在像 Unix 这样的平台上产生混淆，其中操作系统可能返回空内部缓冲的新位置。'),
    ('This is convenience method, equivalent to <code>self.seek(SeekFrom::Start(0))</code>.',
     '这是便捷方法，等价于 <code>self.seek(SeekFrom::Start(0))</code>。'),
    ('This is equivalent to <code>self.seek(SeekFrom::Current(0))</code>.',
     '这等价于 <code>self.seek(SeekFrom::Current(0))</code>。'),
    ('Creates a future which will return the current seek position from the\nunderlying object.',
     '创建一个 Future，返回底层对象的当前定位位置。'),
    ('Creates a future which will return the current seek position from the\nstart of the stream.',
     '创建一个 Future，返回从流开头计算的当前定位位置。'),
    ('Creates a future which will rewind to the beginning of the stream.',
     '创建一个将倒回到流开头的 Future。'),
    ('In the case of an error the buffer and the object will be discarded, with\nthe error yielded.',
     '若发生错误，缓冲与对象将被丢弃，并产出错误。'),
    ('This is the asynchronous equivalent to <code>SeekExt::stream_position</code>.',
     '这是 <code>SeekExt::stream_position</code> 的异步等价物。'),

    # === fs/struct.ReadDir.html cancel-safety patterns ===
    ('This method is cancel safe. If you use it as the event in a\n<code>tokio::select!</code> statement and some\nother branch completes first, then it is guaranteed that no data was read.',
     '此方法是取消安全的。如果将此方法用作 <code>tokio::select!</code> 语句中的事件，并且其他某个分支先完成，则保证尚未读取任何数据。'),
    ('This method is cancel safe. If you use it as the event in a tokio::select! statement and some\nother branch completes first, then it is guaranteed that no data was read.',
     '此方法是取消安全的。如果将此方法用作 tokio::select! 语句中的事件，并且其他某个分支先完成，则保证尚未读取任何数据。'),

    # === io/struct.ReadHalf.html peer_addr ===
    ('Checks if this <code>ReadHalf</code> and some <code>WriteHalf</code> were split from the same stream.',
     '检查此 <code>ReadHalf</code> 与某个 <code>WriteHalf</code> 是否是从同一个流拆分而来。'),
    ('Reunites with a previously split <code>WriteHalf</code>.', '与之前拆分的 <code>WriteHalf</code> 重新合并。'),

    # === process/struct.Child.html Cancel safety section ===
    ('This function is cancel safe.', '此函数是取消安全的。'),
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

    print(f'Phase 7: {files_changed}/{total_files} files, {total_replacements} replacements')


if __name__ == '__main__':
    main()