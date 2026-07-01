#!/usr/bin/env python3
"""tokio 第六阶段：批量翻译 AsyncReadExt / AsyncWriteExt 等文件中重复出现的常见短语。"""
import os

BASE = r'D:/Administrator/Documents/Code/rust_doc_all/tokio'

# 通用短语 (en, zh)
PAIRS = [
    # 通用短语
    ('It is recommended to use a buffered reader to avoid excessive\nsyscalls.', '建议使用带缓冲的读取器，以避免过多的系统调用。'),
    ('It is recommended to use a buffered reader to avoid excessive syscalls.',
     '建议使用带缓冲的读取器，以避免过多的系统调用。'),
    ('This method returns the same errors as <code>AsyncReadExt::read_exact</code>.',
     '此方法返回与 <code>AsyncReadExt::read_exact</code> 相同的错误。'),
    ('This method returns the same errors as <code>AsyncWriteExt::write_all</code>.',
     '此方法返回与 <code>AsyncWriteExt::write_all</code> 相同的错误。'),
    ('This method is cancel safe.', '此方法是取消安全的。'),
    ('This method is cancel safe. If this method is used as an event in a\n<code>tokio::select!</code> statement and some other branch\ncompletes first, it is guaranteed that no data were read.',
     '此方法是取消安全的。如果将此方法用作 <code>tokio::select!</code> 语句中的事件，并且其他某个分支先完成，则保证尚未读取任何数据。'),
    ('This method is cancel safe. If this method is used as an event in a <code>tokio::select!</code> statement and some other branch completes first, it is guaranteed that no data were read.',
     '此方法是取消安全的。如果将此方法用作 <code>tokio::select!</code> 语句中的事件，并且其他某个分支先完成，则保证尚未读取任何数据。'),
    ('This method is not cancellation safe. If the method is used as the\nevent in a <code>tokio::select!</code> statement and some\nother branch completes first, then some data may be lost.',
     '此方法不是取消安全的。如果将此方法用作 <code>tokio::select!</code> 语句中的事件，并且其他某个分支先完成，则可能丢失一些数据。'),
    ('This method is not cancellation safe. If the method is used as the event in a <code>tokio::select!</code> statement and some other branch completes first, then some data may be lost.',
     '此方法不是取消安全的。如果将此方法用作 <code>tokio::select!</code> 语句中的事件，并且其他某个分支先完成，则可能丢失一些数据。'),
    ('This method is not cancellation safe. If the method is used as the\nevent in a <code>tokio::select!</code> statement and some\nother branch completes first, then some data may have been\nread into <code>buf</code>.',
     '此方法不是取消安全的。如果将此方法用作 <code>tokio::select!</code> 语句中的事件，并且其他某个分支先完成，则可能已读取了一些数据到 <code>buf</code> 中。'),
    ('This method is not cancellation safe. If the method is used as the event in a <code>tokio::select!</code> statement and some other branch completes first, then some data may have been read into <code>buf</code>.',
     '此方法不是取消安全的。如果将此方法用作 <code>tokio::select!</code> 语句中的事件，并且其他某个分支先完成，则可能已读取了一些数据到 <code>buf</code> 中。'),
    ('This method does not provide any guarantees about whether it\ncompletes immediately or asynchronously.',
     '此方法不保证是立即完成还是异步完成。'),
    ('This method does not provide any guarantees about whether it completes immediately or asynchronously.',
     '此方法不保证是立即完成还是异步完成。'),
    ('If the return value of this method is <code>Ok(n)</code>, then it must be\nguaranteed that <code>0 &lt;= n &lt;= buf.len()</code>. A nonzero <code>n</code> value indicates\nthat the buffer <code>buf</code> has been filled in with <code>n</code> bytes of data from\nthis source. If <code>n</code> is <code>0</code>, then it can indicate one of two\nscenarios:',
     '若此方法的返回值为 <code>Ok(n)</code>，则必须保证 <code>0 &lt;= n &lt;= buf.len()</code>。非零的 <code>n</code> 值表示缓冲 <code>buf</code> 已从该源填充了 <code>n</code> 个字节的数据。若 <code>n</code> 为 <code>0</code>，则可能表示以下两种情况之一：'),
    ('If the return value of this method is Ok(n), then it must be\nguaranteed that 0 &lt;= n &lt;= buf.len(). A nonzero n value indicates\nthat the buffer buf has been filled in with n bytes of data from\nthis source. If n is 0, then it can indicate one of two\nscenarios:',
     '若此方法的返回值为 Ok(n)，则必须保证 0 &lt;= n &lt;= buf.len()。非零的 n 值表示缓冲 buf 已从该源填充了 n 个字节的数据。若 n 为 0，则可能表示以下两种情况之一：'),
    ('If the return value of this method is Ok(n), then it must be\nguaranteed that 0 &lt;= n &lt;= buf.len(). A nonzero n value indicates\nthat the buffer buf has been filled in with n bytes of data from',
     '若此方法的返回值为 Ok(n)，则必须保证 0 &lt;= n &lt;= buf.len()。非零的 n 值表示缓冲 buf 已从该源填充了 n 个字节的数据，'),
    ('No guarantees are provided about the contents of <code>buf</code> when this\nfunction is called, implementations cannot rely on any property of the\ncontents of <code>buf</code> being true. It is recommended that implementations\nonly write data to <code>buf</code> instead of reading its contents.',
     '调用此函数时，不保证 <code>buf</code> 的内容，实现不能依赖 <code>buf</code> 内容的任何属性。建议实现仅向 <code>buf</code> 写入数据，而不是读取其内容。'),
    ('No guarantees are provided about the contents of buf when this\nfunction is called, implementations cannot rely on any property of the\ncontents of buf being true. It is recommended that implementations\nonly write data to buf instead of reading its contents.',
     '调用此函数时，不保证 buf 的内容，实现不能依赖 buf 内容的任何属性。建议实现仅向 buf 写入数据，而不是读取其内容。'),
    ('Correspondingly, however, callers of this method may not assume\nany guarantees about how the implementation uses <code>buf</code>. It is\npossible that the code that’s supposed to write to the buffer might\nalso read from it.',
     '相应地，但是，此方法的调用者不能假设实现使用 <code>buf</code> 的方式的任何保证。打算写入缓冲的代码也可能从其中读取。'),
    ('Correspondingly, however, callers of this method may not assume\nany guarantees about how the implementation uses buf. It is\npossible that the code that’s supposed to write to the buffer might\nalso read from it.',
     '相应地，但是，此方法的调用者不能假设实现使用 buf 的方式的任何保证。打算写入缓冲的代码也可能从其中读取。'),
    ('Correspondingly, however, callers of this method may not assume\nany guarantees about how the implementation uses buf. It is\npossible that the code that��s supposed to write to the buffer might\nalso read from it.',
     '相应地，但是，此方法的调用者不能假设实现使用 buf 的方式的任何保证。打算写入缓冲的代码也可能从其中读取。'),
    ('If this function encounters any form of I/O or other error, an error\nvariant will be returned. If an error is returned then it must be\nguaranteed that no bytes were read.',
     '若此函数遇到任何形式的 I/O 或其他错误，则返回错误变体。若返回错误，则必须保证尚未读取任何字节。'),
    ('If this function encounters any form of I/O or other error, an error variant will be returned. If an error is returned then it must be guaranteed that no bytes were read.',
     '若此函数遇到任何形式的 I/O 或其他错误，则返回错误变体。若返回错误，则必须保证尚未读取任何字节。'),
    ('<code>n &gt; 0</code> means that the stream has read some data and the buffer contains it.','<code>n &gt; 0</code> 表示流已读取了一些数据并且缓冲中包含这些数据。'),
    ('<code>n == 0</code> means that no data was read, either because the stream is at EOF or','<code>n == 0</code> 表示未读取任何数据，可能因为流到达 EOF，或者'),
    ('because the underlying reader returned <code>Poll::Pending</code> before any bytes could be read.','底层读取器在读取任何字节之前返回了 <code>Poll::Pending</code>。'),

    # read_buf details
    ('Usually, only a single <code>read</code> syscall is issued, even if there is\nmore space in the supplied buffer.',
     '通常，即使提供的缓冲还有更多空间，也只会发出单个 <code>read</code> 系统调用。'),
    ('Usually, only a single read syscall is issued, even if there is\nmore space in the supplied buffer.',
     '通常，即使提供的缓冲还有更多空间，也只会发出单个 read 系统调用。'),
    ('A nonzero <code>n</code> value indicates that the buffer <code>buf</code> has been filled\nin with <code>n</code> bytes of data from this source. If <code>n</code> is <code>0</code>, then it\ncan indicate one of two scenarios:',
     '非零的 <code>n</code> 值表示缓冲 <code>buf</code> 已从该源填充了 <code>n</code> 个字节的数据。若 <code>n</code> 为 <code>0</code>，则可能表示以下两种情况之一：'),
    ('A nonzero n value indicates that the buffer buf has been filled\nin with n bytes of data from this source. If n is 0, then it\ncan indicate one of two scenarios:',
     '非零的 n 值表示缓冲 buf 已从该源填充了 n 个字节的数据。若 n 为 0，则可能表示以下两种情况之一：'),

    # read_exact details
    ('This function reads as many bytes as necessary to completely fill\nthe specified buffer <code>buf</code>.',
     '此函数读取必要的字节数，以完全填充指定的缓冲 <code>buf</code>。'),
    ('This function reads as many bytes as necessary to completely fill the specified buffer buf.',
     '此函数读取必要的字节数，以完全填充指定的缓冲 buf。'),
    ('If any other read error is encountered then the operation\nimmediately returns. The contents of <code>buf</code> are unspecified in this\ncase.',
     '若遇到任何其他读取错误，操作将立即返回。这种情况下 <code>buf</code> 的内容是未指定的。'),
    ('If any other read error is encountered then the operation immediately returns. The contents of buf are unspecified in this case.',
     '若遇到任何其他读取错误，操作将立即返回。这种情况下 buf 的内容是未指定的。'),
    ('If this operation returns an error, it is unspecified how many bytes\nit has read, but it will never read more than would be necessary to\ncompletely fill the buffer.',
     '若此操作返回错误，则读取的字节数是未指定的，但绝不会读取超过完全填充缓冲所需的字节数。'),
    ('If this operation returns an error, it is unspecified how many bytes it has read, but it will never read more than would be necessary to completely fill the buffer.',
     '若此操作返回错误，则读取的字节数是未指定的，但绝不会读取超过完全填充缓冲所需的字节数。'),

    # read_to_end details
    ('All bytes read from this source will be appended to the specified\nbuffer <code>buf</code>. This function will continuously call <code>read()</code> to\nappend more data to <code>buf</code> until <code>read()</code> returns <code>Ok(0)</code>.',
     '从此源读取的所有字节都将追加到指定的缓冲 <code>buf</code> 中。此函数会持续调用 <code>read()</code> 将更多数据追加到 <code>buf</code>，直到 <code>read()</code> 返回 <code>Ok(0)</code>。'),
    ('All bytes read from this source will be appended to the specified buffer buf. This function will continuously call read() to append more data to buf until read() returns Ok(0).',
     '从此源读取的所有字节都将追加到指定的缓冲 buf 中。此函数会持续调用 read() 将更多数据追加到 buf，直到 read() 返回 Ok(0)。'),
    ('If a read error is encountered then the <code>read_to_end</code> operation\nimmediately completes. Any bytes which have already been read will\nbe appended to <code>buf</code>.',
     '若遇到读取错误，<code>read_to_end</code> 操作将立即完成。已读取的所有字节将追加到 <code>buf</code>。'),
    ('If a read error is encountered then the read_to_end operation immediately completes. Any bytes which have already been read will be appended to buf.',
     '若遇到读取错误，read_to_end 操作将立即完成。已读取的所有字节将追加到 buf。'),

    # read_to_string details
    ('If successful, the number of bytes which were read and appended to\n<code>buf</code> is returned.',
     '若成功，返回已读取并追加到 <code>buf</code> 的字节数。'),
    ('If successful, the number of bytes which were read and appended to buf is returned.',
     '若成功，返回已读取并追加到 buf 的字节数。'),
    ('If the data in this stream is <em>not</em> valid UTF-8 then an error is\nreturned and <code>buf</code> is unchanged.',
     '若此流中的数据不是有效的 UTF-8，则返回错误且 <code>buf</code> 保持不变。'),
    ('If the data in this stream is not valid UTF-8 then an error is\nreturned and buf is unchanged.',
     '若此流中的数据不是有效的 UTF-8，则返回错误且 buf 保持不变。'),
    ('See <code>read_to_end</code> for other error semantics.', '其他错误语义请参阅 <code>read_to_end</code>。'),
    ('See read_to_end for other error semantics.', '其他错误语义请参阅 read_to_end。'),

    # top docblock at start of AsyncReadExt / AsyncWriteExt / AsyncBufReadExt
    ('Reads bytes from a source.\nImplemented as an extension trait, adding utility methods to all\n<code>AsyncRead</code> types. Callers will tend to import this trait instead of\n<code>AsyncRead</code>',
     '从源读取字节。\n作为扩展特性实现，向所有 <code>AsyncRead</code> 类型添加工具方法。调用者通常会导入本特性而非 <code>AsyncRead</code>'),
    ('Reads bytes from a source.\nImplemented as an extension trait, adding utility methods to all <code>AsyncRead</code> types. Callers will tend to import this trait instead of <code>AsyncRead</code>',
     '从源读取字节。\n作为扩展特性实现，向所有 <code>AsyncRead</code> 类型添加工具方法。调用者通常会导入本特性而非 <code>AsyncRead</code>'),
    ('Writes bytes to a sink.\nImplemented as an extension trait, adding utility methods to all\n<code>AsyncWrite</code> types. Callers will tend to import this trait instead of\n<code>AsyncWrite</code>',
     '将字节写入汇。\n作为扩展特性实现，向所有 <code>AsyncWrite</code> 类型添加工具方法。调用者通常会导入本特性而非 <code>AsyncWrite</code>'),
    ('Writes bytes to a sink.\nImplemented as an extension trait, adding utility methods to all <code>AsyncWrite</code> types. Callers will tend to import this trait instead of <code>AsyncWrite</code>',
     '将字节写入汇。\n作为扩展特性实现，向所有 <code>AsyncWrite</code> 类型添加工具方法。调用者通常会导入本特性而非 <code>AsyncWrite</code>'),

    # chain method line (with `<code>next</code>` not "another")
    ('Creates a new <code>AsyncRead</code> instance that chains this stream with\n<code>next</code>.',
     '创建一个新的 <code>AsyncRead</code> 实例，将此流与 <code>next</code> 链接起来。'),
    ('Creates a new AsyncRead instance that chains this stream with\nnext.',
     '创建一个新的 AsyncRead 实例，将此流与 next 链接起来。'),

    # take method line
    ('Creates an adaptor which reads at most <code>limit</code> bytes from it.\nThis function returns a new instance of <code>AsyncRead</code> which will read\nat most <code>limit</code> bytes, after which it will always return EOF\n(<code>Ok(0)</code>). Any read errors will not count towards the number of\nbytes read and future calls to <code>read()</code> may succeed.',
     '创建一个适配器，从其中最多读取 <code>limit</code> 个字节。\n此函数返回 <code>AsyncRead</code> 的一个新实例，最多读取 <code>limit</code> 个字节，之后将始终返回 EOF（<code>Ok(0)</code>）。任何读取错误将不计入已读取字节数，且对 <code>read()</code> 的后续调用仍可能成功。'),
    ('Creates an adaptor which reads at most <code>limit</code> bytes from it.',
     '创建一个适配器，从其中最多读取 <code>limit</code> 个字节。'),
    ('Creates an adaptor which reads at most limit bytes from it.',
     '创建一个适配器，从其中最多读取 limit 个字节。'),
    ('This function returns a new instance of <code>AsyncRead</code> which will read\nat most <code>limit</code> bytes, after which it will always return EOF\n(<code>Ok(0)</code>). Any read errors will not count towards the number of\nbytes read and future calls to <code>read()</code> may succeed.',
     '此函数返回 <code>AsyncRead</code> 的一个新实例，最多读取 <code>limit</code> 个字节，之后将始终返回 EOF（<code>Ok(0)</code>）。任何读取错误将不计入已读取字节数，且对 <code>read()</code> 的后续调用仍可能成功。'),
    ('This function returns a new instance of AsyncRead which will read\nat most limit bytes, after which it will always return EOF\n(Ok(0)). Any read errors will not count towards the number of\nbytes read and future calls to read() may succeed.',
     '此函数返回 AsyncRead 的一个新实例，最多读取 limit 个字节，之后将始终返回 EOF（Ok(0)）。任何读取错误将不计入已读取字节数，且对 read() 的后续调用仍可能成功。'),
    ('This function returns a new instance of <code>AsyncRead</code> which will read\nat most <code>limit</code> bytes, after which it will always return EOF\n(<code>Ok(0)</code>).',
     '此函数返回 <code>AsyncRead</code> 的一个新实例，最多读取 <code>limit</code> 个字节，之后将始终返回 EOF（<code>Ok(0)</code>）。'),

    # write variants
    ('Writes a buffer into this writer, returning how many bytes were\nwritten.', '将一个缓冲写入此写入器，返回写入的字节数。'),
    ('Writes a buffer into this writer, returning how many bytes were written.',
     '将一个缓冲写入此写入器，返回写入的字节数。'),
    ('Writes a buffer into this writer, advancing the buffer’s internal\ncursor.', '将一个缓冲写入此写入器，前进缓冲的内部游标。'),
    ('Writes a buffer into this writer, advancing the buffer’s internal\ncursor.', '将一个缓冲写入此写入器，前进缓冲的内部游标。'),
    ('Writes a buffer into this writer, advancing the buffer’s internal cursor.',
     '将一个缓冲写入此写入器，前进缓冲的内部游标。'),
    ('Attempts to write an entire buffer into this writer.', '尝试将整个缓冲写入此写入器。'),
    ('Writes an entire buffer into this writer.', '将整个缓冲写入此写入器。'),
    ('Flushes this output stream, ensuring that all intermediately buffered\ncontents reach their destination.',
     '刷新此输出流，确保所有中间缓冲的内容到达目的地。'),
    ('Shuts down the output stream, ensuring that the value can be dropped\ncleanly.', '关闭输出流，确保此值能被干净地丢弃。'),

    # chain extension method detail (the long version)
    ('Creates a new <code>AsyncRead</code> instance that chains this stream with another.\nThe returned <code>AsyncRead</code> instance will first read all bytes from this object\nuntil EOF is encountered. Afterwards the output is equivalent to the\noutput of <code>next</code>.',
     '创建一个新的 <code>AsyncRead</code> 实例，将此流与另一个流链接起来。\n返回的 <code>AsyncRead</code> 实例将首先从此对象读取所有字节直到 EOF。之后的输出等同于 <code>next</code> 的输出。'),

    # AsyncWriteExt.write detail
    ('This function will attempt to write the entire contents of buf, but\nwill return an error if the underlying AsyncWrite instance reaches EOF\nbefore completing.',
     '此函数将尝试写入 buf 的全部内容，但如果底层 AsyncWrite 实例在完成前到达 EOF，则返回错误。'),
    ('This function will attempt to write the entire contents of buf, but will return an error if the underlying AsyncWrite instance reaches EOF before completing.',
     '此函数将尝试写入 buf 的全部内容，但如果底层 AsyncWrite 实例在完成前到达 EOF，则返回错误。'),

    # write_vectored detail
    ('Data may be buffered if there is not enough space in the buffers, in\nwhich case the output stream may not be flushed.',
     '如果缓冲中没有足够的空间，数据可能会被缓冲，在这种情况下输出流可能不会被刷新。'),

    # write_all detail
    ('It is considered an error if not all bytes could be written due to\nI/O errors or EOF being reached.',
     '如果由于 I/O 错误或到达 EOF 而无法写入所有字节，则视为错误。'),

    # AsyncWriteExt.flush details
    ('It is considered an error if not all bytes could be written due to I/O errors or EOF being reached.',
     '如果由于 I/O 错误或到达 EOF 而无法写入所有字节，则视为错误。'),

    # AsyncWriteExt.shutdown
    ('On Unix, this will close the write side of the socket. On Windows, this\nwill close the underlying TCP socket.',
     '在 Unix 上，这会关闭套接字的写端。在 Windows 上，这会关闭底层 TCP 套接字。'),
    ('If this method returns <code>Ok(())</code>, it is guaranteed that the value can be\ndropped safely.', '若此方法返回 <code>Ok(())</code>，则保证此值可以安全地丢弃。'),

    # AsyncBufReadExt top docblock
    ('Asynchronously reads bytes from a source. Implemented as an extension trait, adding utility methods to all\n<code>AsyncBufRead</code> types.',
     '从源异步读取字节。作为扩展特性实现，向所有 <code>AsyncBufRead</code> 类型添加工具方法。'),
    ('Asynchronously reads bytes from a source. Implemented as an extension trait, adding utility methods to all <code>AsyncBufRead</code> types.',
     '从源异步读取字节。作为扩展特性实现，向所有 <code>AsyncBufRead</code> 类型添加工具方法。'),
    ('Asynchronously seeks to a position in a stream. Implemented as an extension trait, adding utility methods to all\n<code>AsyncSeek</code> types.',
     '在流中异步定位到指定位置。作为扩展特性实现，向所有 <code>AsyncSeek</code> 类型添加工具方法。'),
    ('Asynchronously seeks to a position in a stream. Implemented as an extension trait, adding utility methods to all <code>AsyncSeek</code> types.',
     '在流中异步定位到指定位置。作为扩展特性实现，向所有 <code>AsyncSeek</code> 类型添加工具方法。'),

    # AsyncSeekExt.seek detail
    ('In the case of an error the buffer and the object will be discarded, with\nthe error yielded.',
     '若发生错误，缓冲与对象将被丢弃，并产出错误。'),
    ('Creates a future which will return the current seek position from the\nstart of the stream.',
     '创建一个 Future，返回从流开头计算的当前定位位置。'),

    # ===== process/struct.Command.html =====
    ('Constructs a new <code>Command</code> for launching <code>program</code>.',
     '构造一个用于启动 <code>program</code> 的新 <code>Command</code>。'),
    ('Constructs a new Command for launching the program at', '构造一个用于启动程序的新 Command，'),
    ('The full path to the program can be specified.', '可指定程序的完整路径。'),
    ('Inserts or updates an explicit environment variable mapping.\nThis method allows you add an environment variable mapping to an\nenvironment for the child process, replacing any previous value for the\ncorresponding key. To control the environment of the child process\nwithout affecting the parent process, see <code>env_clear</code>.',
     '插入或更新一个显式的环境变量映射。\n此方法允许向子进程的环境添加一个环境变量映射，替换对应键的先前值。若要在不影响父进程的情况下控制子进程的环境，请参阅 <code>env_clear</code>。'),
    ('Removes an explicit environment variable mapping. To remove a\nmapping for a key which has not been previously set, this method has\nno effect.',
     '删除一个显式的环境变量映射。对于之前未设置的键，调用此方法无效。'),

    # ===== process/struct.Child.html more =====
    ('To kill the child process, you should use <a href="struct.Child.html#method.kill" title="method tokio::process::Child::kill"><code>kill</code></a>, not <code>kill_on_drop</code>.',
     '要杀死子进程，应使用 <a href="struct.Child.html#method.kill" title="method tokio::process::Child::kill"><code>kill</code></a>，而不是 <code>kill_on_drop</code>。'),
    ('Returning how many bytes were written.', '返回写入的字节数。'),

    # ===== fs/struct.OpenOptions.html =====
    ('This is an async version of std::fs::OpenOptions::read', '这是 std::fs::OpenOptions::read 的异步版本。'),
    ('This is an async version of std::fs::OpenOptions::write', '这是 std::fs::OpenOptions::write 的异步版本。'),
    ('This is an async version of std::fs::OpenOptions::new', '这是 std::fs::OpenOptions::new 的异步版本。'),
    ('Sets the option for read access.', '设置读访问选项。'),
    ('Sets the option for write access.', '设置写访问选项。'),
    ('This option, when true, will indicate that the file should be read-able if opened.',
     '当此选项为 true 时，表示如果打开，文件应可读。'),
    ('This option, when true, will indicate that the file should be write-able if opened.',
     '当此选项为 true 时，表示如果打开，文件应可写。'),
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
    ('All options are initially set to false.', '所有选项最初均设置为 false。'),
    ('Options and flags which can be used to configure how a file is opened.', '用于配置文件打开方式的可选项与标志。'),
    ('Creates a blank new set of options ready for configuration.', '创建一组待配置的空白选项。'),
    ('This can also be written using <code>File::options().read(true).write(true).create_new(true).open(...)</code>.',
     '这也可以用 <code>File::options().read(true).write(true).create_new(true).open(...)</code> 来表达。'),
    ('This can also be written using File::options().read(true).write(true).create_new(true).open(...).',
     '这也可以用 File::options().read(true).write(true).create_new(true).open(...) 来表达。'),

    # ===== fs/struct.File.html long descs =====
    ('Creates a new file in read-write mode, failing if the file already exists.',
     '以读写模式创建新文件；若文件已存在则失败。'),
    ('This can also be written using <code>File::options().read(true).write(true).truncate(true).create(true).open(...)</code>.',
     '这也可以用 <code>File::options().read(true).write(true).truncate(true).create(true).open(...)</code> 来表达。'),
    ('This can also be written using File::options().read(true).write(true).truncate(true).create(true).open(...).',
     '这也可以用 File::options().read(true).write(true).truncate(true).create(true).open(...) 来表达。'),
    ('This can also be written using <code>File::options().read(true).write(true).create(true).truncate(true).open(...)</code>.',
     '这也可以用 <code>File::options().read(true).write(true).create(true).truncate(true).open(...)</code> 来表达。'),
    ('Truncates or creates a file in read-write mode.', '以读写模式截断或创建文件。'),
    ('Creates a file in read-write mode.', '以读写模式创建文件。'),
    ('See <a href="struct.OpenOptions.html"><code>OpenOptions</code></a> for more details.', '详见 <a href="struct.OpenOptions.html"><code>OpenOptions</code></a>。'),
    ('See <code>OpenOptions</code> for more details.', '详见 <code>OpenOptions</code>。'),
    ('See OpenOptions for more details.', '详见 OpenOptions。'),
    ('This function will return an error if called from outside of the Tokio runtime or if path does not already exist. Other errors may also be returned according to OpenOptions::open.',
     '若在 tokio 运行时外调用此函数，或若 path 不存在，此函数将返回错误。也可能根据 OpenOptions::open 返回其他错误。'),
    ('The read_to_end method is defined on the AsyncReadExt trait.', 'read_to_end 方法定义在 AsyncReadExt 特性上。'),
    ('The write_all method is defined on the AsyncWriteExt trait.', 'write_all 方法定义在 AsyncWriteExt 特性上。'),
    ('This function will create a file if it does not exist, and will truncate it if it does.',
     '若文件不存在，此函数将创建它；若已存在，则将其截断。'),
    ('This function will create a file if it does not exist, and will fail if it does.',
     '若文件不存在，此函数将创建它；若已存在，则失败。'),
    ('Results in an error if called from outside of the Tokio runtime or if the underlying create call results in an error.',
     '若在 tokio 运行时外调用，或底层 create 调用出错，则返回错误。'),

    # ===== io/struct.BufStream.html =====
    ('See the documentation for those types and <a href="struct.BufStream.html"><code>BufStream</code></a> for details.',
     '详见相关类型与 <a href="struct.BufStream.html"><code>BufStream</code></a> 的文档。'),
    ('See the documentation for those types and BufStream for details.', '详见相关类型与 BufStream 的文档。'),

    # ===== io/struct.BufReader.html =====
    ('It is inadvisable to directly read from the underlying reader.',
     '不建议直接读取底层读取器。'),
    ('Note that any leftover data in the internal buffer is lost.',
     '请注意，内部缓冲中的所有剩余数据都将丢失。'),
    ('Returning a reference to the internally buffered data.',
     '返回内部缓冲数据的引用。'),
    ('Unlike <code>fill_buf</code>, this will not attempt to fill the buffer if it is empty.',
     '与 <code>fill_buf</code> 不同，若缓冲为空，此方法不会尝试填充缓冲。'),

    # ===== io/struct.Split.html =====
    ('Splits a stream into separate read and write halves.', '将一个流拆分为独立的读、写两半。'),
    ('The Split struct allows you to split a bidirectional stream into separate read and write halves.',
     'Split 结构体允许你将一个双向流拆分为独立的读、写两半。'),

    # ===== fs/struct.ReadDir.html =====
    ('Note that on multiple calls to poll_next_entry, only the Waker from\nthe Context passed to the most recent call is scheduled to receive a wakeup.',
     '请注意，在多次调用 poll_next_entry 时，只有最近一次调用传入的 Context 中的 Waker 会被调度以接收唤醒。'),
    ('When the method returns Poll::Pending, the Waker in the provided\nContext is scheduled to receive a wakeup when more bytes become',
     '当此方法返回 Poll::Pending 时，传入的 Context 中的 Waker 被调度以在更多字节可用时接收唤醒。'),
    ('* Poll::Pending if the next directory entry is not yet available.',
     '* 若下一个目录条目尚未就绪，返回 Poll::Pending。'),
    ('* Poll::Ready(Ok(Some(entry))) if the next directory entry is available.',
     '* 若下一个目录条目可用，返回 Poll::Ready(Ok(Some(entry)))。'),
    ('* Poll::Ready(Ok(None)) if there are no more directory entries in this\nstream.', '* 若此流中再无更多目录条目，返回 Poll::Ready(Ok(None))。'),
    ('* Poll::Ready(Ok(None)) if there are no more directory entries in this stream.',
     '* 若此流中再无更多目录条目，返回 Poll::Ready(Ok(None))。'),
    ('* Poll::Ready(Err(error)) if an error occurred while reading the next\ndirectory entry.', '* 若读取下一个目录条目时发生错误，返回 Poll::Ready(Err(error))。'),
    ('* Poll::Ready(Err(error)) if an error occurred while reading the next directory entry.',
     '* 若读取下一个目录条目时发生错误，返回 Poll::Ready(Err(error))。'),

    # ===== signal/windows/CtrlBreak/CtrlC/etc =====
    ('Although this returns <code>Option&lt;()&gt;</code>, it will never actually return <code>None</code>.\nThis was accidentally exposed and would be a breaking change to be removed.',
     '尽管此函数返回 <code>Option&lt;()&gt;</code>，但实际上永远不会返回 <code>None</code>。\n这是意外暴露的，要删除将是一个破坏性变更。'),
    ('Although this returns Option&lt;()&gt;, it will never actually return None.\nThis was accidentally exposed and would be a breaking change to be removed.',
     '尽管此函数返回 Option&lt;()&gt;，但实际上永远不会返回 None。\n这是意外暴露的，要删除将是一个破坏性变更。'),
    ('Polling from a manually implemented future', '从手动实现的 Future 轮询'),
    ('Receives the next signal notification event.', '接收下一个信号通知事件。'),
    ('Polls to receive the next signal notification event, outside of an\nasync context.', '在异步上下文之外轮询以接收下一个信号通知事件。'),
    ('Polls to receive the next signal notification event, outside of an async context.',
     '在异步上下文之外轮询以接收下一个信号通知事件。'),

    # ===== io/struct.BufStream.html =====
    ('Gets a reference to the underlying I/O object.', '获取底层 I/O 对象的引用。'),
    ('Gets a mutable reference to the underlying I/O object.', '获取底层 I/O 对象的可变引用。'),
    ('It is inadvisable to directly read from the underlying I/O object.',
     '不建议直接读取底层 I/O 对象。'),
    ('Gets a pinned mutable reference to the underlying I/O object.',
     '获取底层 I/O 对象的 pinned 可变引用。'),
    ('Consumes this BufStream, returning the underlying I/O object.', '消费此 BufStream，返回底层 I/O 对象。'),

    # ===== io/struct.BufReader/BufWriter =====
    ('Consuming this BufReader, returning the underlying reader.', '消费此 BufReader，返回底层读取器。'),
    ('Consuming this BufWriter, returning the underlying writer.', '消费此 BufWriter，返回底层写入器。'),
    ('Getting a reference to the underlying reader.', '获取底层读取器的引用。'),
    ('Getting a reference to the underlying writer.', '获取底层写入器的引用。'),
    ('Getting a mutable reference to the underlying reader.', '获取底层读取器的可变引用。'),
    ('Getting a mutable reference to the underlying writer.', '获取底层写入器的可变引用。'),
    ('Getting a pinned mutable reference to the underlying reader.',
     '获取底层读取器的 pinned 可变引用。'),
    ('Getting a pinned mutable reference to the underlying writer.',
     '获取底层写入器的 pinned 可变引用。'),
    ('Note that any leftover data in the internal buffer is lost.',
     '请注意，内部缓冲中的所有剩余数据都将丢失。'),
    ('Returning a reference to the internally buffered data.', '返回内部缓冲数据的引用。'),
    ('Unlike fill_buf, this will not attempt to fill the buffer if it is empty.',
     '与 fill_buf 不同，若缓冲为空，此方法不会尝试填充缓冲。'),
    ('Unlike fill_buf, this will not attempt to fill the buffer if it is empty.\n', '与 fill_buf 不同，若缓冲为空，此方法不会尝试填充缓冲。'),
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

    print(f'Phase 6: {files_changed}/{total_files} files, {total_replacements} replacements')


if __name__ == '__main__':
    main()