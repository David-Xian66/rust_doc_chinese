#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""补译 tokio 14 个文件中的英文 docblock（<p> 单独含 CJK）。"""
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))


def read_bytes(rel):
    with open(os.path.join(ROOT, rel), 'rb') as f:
        return f.read()


def write_bytes(rel, data):
    with open(os.path.join(ROOT, rel), 'wb') as f:
        f.write(data)


def E(s):
    """Encode UTF-8 string to bytes."""
    return s.encode('utf-8')


def add(rel, pairs):
    PLAN.append((rel, pairs))


PLAN = []


# ============================================================
# io/struct.BufStream.html
# ============================================================
add('io/struct.BufStream.html', [
    (b'<div class="docblock"><p>Wraps a type in both <a href="struct.BufWriter.html" title="struct tokio::io::BufWriter"><code>BufWriter</code></a> and <a href="struct.BufReader.html" title="struct tokio::io::BufReader"><code>BufReader</code></a>.</p>\r\n<p>See the documentation for those types and <a href="struct.BufStream.html" title="struct tokio::io::BufStream"><code>BufStream</code></a> for details.</p>\r\n</div>',
     E('<div class="docblock"><p>使用 <a href="struct.BufWriter.html" title="struct tokio::io::BufWriter"><code>BufWriter</code></a> 和 <a href="struct.BufReader.html" title="struct tokio::io::BufReader"><code>BufReader</code></a> 共同封装一个类型。</p>\r\n<p>有关细节，请参阅这些类型以及 <a href="struct.BufStream.html" title="struct tokio::io::BufStream"><code>BufStream</code></a> 的文档。</p>\r\n</div>')),
    (b'<div class="docblock"><p>Creates a <code>BufStream</code> with the specified <a href="struct.BufReader.html" title="struct tokio::io::BufReader"><code>BufReader</code></a> capacity and <a href="struct.BufWriter.html" title="struct tokio::io::BufWriter"><code>BufWriter</code></a>\r\ncapacity.</p>\r\n<p>See the documentation for those types and <a href="struct.BufStream.html" title="struct tokio::io::BufStream"><code>BufStream</code></a> for details.</p>\r\n</div>',
     E('<div class="docblock"><p>使用指定的 <a href="struct.BufReader.html" title="struct tokio::io::BufReader"><code>BufReader</code></a> 容量和 <a href="struct.BufWriter.html" title="struct tokio::io::BufWriter"><code>BufWriter</code></a> 容量创建一个 <code>BufStream</code>。</p>\r\n<p>有关细节，请参阅这些类型以及 <a href="struct.BufStream.html" title="struct tokio::io::BufStream"><code>BufStream</code></a> 的文档。</p>\r\n</div>')),
])


# ============================================================
# io/struct.SimplexStream.html
# ============================================================
add('io/struct.SimplexStream.html', [
    (b'<p>A unidirectional pipe to read and write bytes in memory.</p>',
     E('<p>一个单向管道，用于在内存中读写字节。</p>')),
    (b'<p>It can be constructed by <a href="fn.simplex.html" title="fn tokio::io::simplex"><code>simplex</code></a> function which will create a pair of\r\nreader and writer or by calling <a href="struct.SimplexStream.html#method.new_unsplit" title="associated function tokio::io::SimplexStream::new_unsplit"><code>SimplexStream::new_unsplit</code></a> that will\r\ncreate a handle for both reading and writing.</p>',
     E('<p>它可以通过 <a href="fn.simplex.html" title="fn tokio::io::simplex"><code>simplex</code></a> 函数构造（该函数会创建一对读端和写端），\r\n也可以通过调用 <a href="struct.SimplexStream.html#method.new_unsplit" title="associated function tokio::io::SimplexStream::new_unsplit"><code>SimplexStream::new_unsplit</code></a> 来构造，\r\n后者会同时创建用于读和写的句柄。</p>')),
    (b'<p>The <code>max_buf_size</code> argument is the maximum amount of bytes that can be\r\nwritten to a buffer before the it returns <code>Poll::Pending</code>.</p>',
     E('<p><code>max_buf_size</code> 参数指定在返回 <code>Poll::Pending</code> 之前可写入缓冲区的最大字节数。</p>')),
])


# ============================================================
# io/trait.AsyncBufReadExt.html
# ============================================================
add('io/trait.AsyncBufReadExt.html', [
    (b'<p>An extension trait which adds utility methods to <a href="trait.AsyncBufRead.html" title="trait tokio::io::AsyncBufRead"><code>AsyncBufRead</code></a> types.</p>',
     E('<p>一个扩展 trait，为 <a href="trait.AsyncBufRead.html" title="trait tokio::io::AsyncBufRead"><code>AsyncBufRead</code></a> 类型添加实用方法。</p>')),
    (b'<p>If this function returns <code>Ok(0)</code>, the stream has reached EOF.</p>',
     E('<p>如果此函数返回 <code>Ok(0)</code>，则流已达到 EOF。</p>')),
    (b'<p>This function will ignore all instances of <a href="https://doc.rust-lang.org/1.95.0/std/io/error/enum.ErrorKind.html#variant.Interrupted" title="variant std::io::error::ErrorKind::Interrupted"><code>ErrorKind::Interrupted</code></a> and\r\nwill otherwise return any errors returned by <a href="trait.AsyncBufRead.html#tymethod.poll_fill_buf" title="method tokio::io::AsyncBufRead::poll_fill_buf"><code>fill_buf</code></a>.</p>',
     E('<p>此函数会忽略所有 <a href="https://doc.rust-lang.org/1.95.0/std/io/error/enum.ErrorKind.html#variant.Interrupted" title="variant std::io::error::ErrorKind::Interrupted"><code>ErrorKind::Interrupted</code></a> 错误，\r\n并返回 <a href="trait.AsyncBufRead.html#tymethod.poll_fill_buf" title="method tokio::io::AsyncBufRead::poll_fill_buf"><code>fill_buf</code></a> 所返回的其他任何错误。</p>')),
    (b'<p>If an I/O error is encountered then all bytes read so far will be\r\npresent in <code>buf</code> and its length will have been adjusted appropriately.</p>',
     E('<p>如果遇到 I/O 错误，则到目前为止已读取的所有字节都将保留在 <code>buf</code> 中，\r\n并且其长度会相应调整。</p>')),
    (b'<p>If the method is used as the event in a\r\n<a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> statement and some other branch\r\ncompletes first, then some data may have been partially read. Any\r\npartially read bytes are appended to <code>buf</code>, and the method can be\r\ncalled again to continue reading until <code>byte</code>.</p>',
     E('<p>如果该方法在 <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a>\r\n语句中作为事件使用，且另一个分支先完成，则部分数据可能已被读取。\r\n已部分读取的字节会附加到 <code>buf</code>，可以再次调用该方法以继续读取，\r\n直到遇到 <code>byte</code>。</p>')),
    (b'<p>This method returns the total number of bytes read. If you cancel\r\nthe call to <code>read_until</code> and then call it again to continue reading,\r\nthe counter is reset.</p>',
     E('<p>此方法返回已读取的总字节数。如果取消对 <code>read_until</code> 的调用，\r\n然后再次调用以继续读取，则计数器会重置。</p>')),
    (b'<p><a href="https://doc.rust-lang.org/1.95.0/std/io/cursor/struct.Cursor.html" title="struct std::io::cursor::Cursor"><code>std::io::Cursor</code></a> is a type that implements <code>BufRead</code>. In\r\nthis example, we use <a href="https://doc.rust-lang.org/1.95.0/std/io/cursor/struct.Cursor.html" title="struct std::io::cursor::Cursor"><code>Cursor</code></a> to read all the bytes in a byte slice\r\nin hyphen delimited segments:</p>',
     E('<p><a href="https://doc.rust-lang.org/1.95.0/std/io/cursor/struct.Cursor.html" title="struct std::io::cursor::Cursor"><code>std::io::Cursor</code></a> 是实现 <code>BufRead</code> 的类型。\r\n在此示例中，我们使用 <a href="https://doc.rust-lang.org/1.95.0/std/io/cursor/struct.Cursor.html" title="struct std::io::cursor::Cursor"><code>Cursor</code></a> 按连字符分隔的方式读取字节切片中的所有字节：</p>')),
    (b'<p>This function will read bytes from the underlying stream until the\r\nnewline delimiter (the 0xA byte) or EOF is found. Once found, all bytes\r\nup to, and including, the delimiter (if found) will be appended to\r\n<code>buf</code>.</p>',
     E('<p>此函数会从底层流读取字节，直到找到换行分隔符（0xA 字节）或 EOF。\r\n找到后，所有字节（如果找到分隔符，则包括分隔符）将附加到 <code>buf</code>。</p>')),
    (b'<p>This function has the same error semantics as <a href="trait.AsyncBufReadExt.html#method.read_until" title="method tokio::io::AsyncBufReadExt::read_until"><code>read_until</code></a> and will\r\nalso return an error if the read bytes are not valid UTF-8. If an I/O\r\nerror is encountered then <code>buf</code> may contain some bytes already read in\r\nthe event that all data read so far was valid UTF-8.</p>',
     E('<p>此函数的错误语义与 <a href="trait.AsyncBufReadExt.html#method.read_until" title="method tokio::io::AsyncBufReadExt::read_until"><code>read_until</code></a> 相同，\r\n并且如果读取的字节不是有效的 UTF-8，也会返回错误。\r\n如果遇到 I/O 错误，则在所有已读取数据均为有效 UTF-8 的情况下，\r\n<code>buf</code> 中可能已包含部分已读取的字节。</p>')),
    (b'<p>This method is not cancellation safe. If the method is used as the\r\nevent in a <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> statement and some\r\nother branch completes first, then some data may have been partially\r\nread, and this data is lost. There are no guarantees regarding the\r\ncontents of <code>buf</code> when the call is cancelled. The current\r\nimplementation replaces <code>buf</code> with the empty string, but this may\r\nchange in the future.</p>',
     E('<p>此方法不是可取消安全的。如果该方法在 <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a>\r\n语句中作为事件使用，且另一个分支先完成，则部分数据可能已被读取，\r\n并且该部分数据会丢失。取消调用时，<code>buf</code> 的内容不提供任何保证。\r\n当前实现会将 <code>buf</code> 替换为空字符串，但未来可能会有所变化。</p>')),
    (b'<p>This function does not behave like <a href="trait.AsyncBufReadExt.html#method.read_until" title="method tokio::io::AsyncBufReadExt::read_until"><code>read_until</code></a> because of the\r\nrequirement that a string contains only valid utf-8. If you need a\r\ncancellation safe <code>read_line</code>, there are three options:</p>',
     E('<p>由于字符串只能包含有效 UTF-8 的要求，此函数的行为与 <a href="trait.AsyncBufReadExt.html#method.read_until" title="method tokio::io::AsyncBufReadExt::read_until"><code>read_until</code></a> 不相同。\r\n如果你需要一个可取消安全的 <code>read_line</code>，有三种选择：</p>')),
    (b'<p><a href="https://doc.rust-lang.org/1.95.0/std/io/cursor/struct.Cursor.html" title="struct std::io::cursor::Cursor"><code>std::io::Cursor</code></a> is a type that implements\r\n<code>AsyncBufRead</code>. In this example, we use <a href="https://doc.rust-lang.org/1.95.0/std/io/cursor/struct.Cursor.html" title="struct std::io::cursor::Cursor"><code>Cursor</code></a> to read all the\r\nlines in a byte slice:</p>',
     E('<p><a href="https://doc.rust-lang.org/1.95.0/std/io/cursor/struct.Cursor.html" title="struct std::io::cursor::Cursor"><code>std::io::Cursor</code></a> 是实现 <code>AsyncBufRead</code> 的类型。\r\n在此示例中，我们使用 <a href="https://doc.rust-lang.org/1.95.0/std/io/cursor/struct.Cursor.html" title="struct std::io::cursor::Cursor"><code>Cursor</code></a> 读取字节切片中的所有行：</p>')),
    (b'<p>Returns a stream of the contents of this reader split on the byte\r\n<code>byte</code>.</p>',
     E('<p>返回一个流，其内容按字节 <code>byte</code> 切分。</p>')),
    (b'<p>This method is the asynchronous equivalent to\r\n<a href="https://doc.rust-lang.org/1.95.0/std/io/trait.BufRead.html#method.split" title="method std::io::BufRead::split"><code>BufRead::split</code></a>.</p>',
     E('<p>此方法是 <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.BufRead.html#method.split" title="method std::io::BufRead::split"><code>BufRead::split</code></a> 的异步等价方法。</p>')),
    (b'<p>The stream returned from this function will yield instances of\r\n<a href="https://doc.rust-lang.org/1.95.0/std/io/error/type.Result.html" title="type std::io::error::Result"><code>io::Result</code></a><code>&lt;</code><a href="https://doc.rust-lang.org/1.95.0/core/option/enum.Option.html" title="enum core::option::Option"><code>Option</code></a><code>&lt;</code><a href="https://doc.rust-lang.org/1.95.0/alloc/vec/struct.Vec.html" title="struct alloc::vec::Vec"><code>Vec&lt;u8&gt;</code></a><code>&gt;&gt;</code>. Each vector returned will <em>not</em> have\r\nthe delimiter byte at the end.</p>',
     E('<p>此函数返回的流将产生 <a href="https://doc.rust-lang.org/1.95.0/std/io/error/type.Result.html" title="type std::io::error::Result"><code>io::Result</code></a><code>&lt;</code><a href="https://doc.rust-lang.org/1.95.0/core/option/enum.Option.html" title="enum core::option::Option"><code>Option</code></a><code>&lt;</code><a href="https://doc.rust-lang.org/1.95.0/alloc/vec/struct.Vec.html" title="struct alloc::vec::Vec"><code>Vec&lt;u8&gt;</code></a><code>&gt;&gt;</code> 的实例。\r\n每个返回的向量<em>不</em>包含末尾的分隔符字节。</p>')),
    (b'<p>Each item of the stream has the same error semantics as\r\n<a href="trait.AsyncBufReadExt.html#method.read_until" title="method tokio::io::AsyncBufReadExt::read_until"><code>AsyncBufReadExt::read_until</code></a>.</p>',
     E('<p>流中每个项的错误语义与 <a href="trait.AsyncBufReadExt.html#method.read_until" title="method tokio::io::AsyncBufReadExt::read_until"><code>AsyncBufReadExt::read_until</code></a> 相同。</p>')),
    (b'<p>This function will return an I/O error if the underlying reader was\r\nread, but returned an error.</p>',
     E('<p>如果底层读取器被读取但返回了错误，此函数将返回 I/O 错误。</p>')),
    (b'<p>Tells this buffer that <code>amt</code> bytes have been consumed from the\r\nbuffer, so they should no longer be returned in calls to <a href="trait.AsyncReadExt.html#method.read" title="method tokio::io::AsyncReadExt::read"><code>read</code></a>.</p>',
     E('<p>通知此缓冲区已有 <code>amt</code> 个字节被消费，\r\n因此在调用 <a href="trait.AsyncReadExt.html#method.read" title="method tokio::io::AsyncReadExt::read"><code>read</code></a> 时不应再返回这些字节。</p>')),
    (b'<p>The <code>amt</code> must be less than the number of bytes in the buffer\r\nreturned by <a href="trait.AsyncBufReadExt.html#method.fill_buf" title="method tokio::io::AsyncBufReadExt::fill_buf"><code>fill_buf</code></a>.</p>',
     E('<p><code>amt</code> 必须小于 <a href="trait.AsyncBufReadExt.html#method.fill_buf" title="method tokio::io::AsyncBufReadExt::fill_buf"><code>fill_buf</code></a> 返回的缓冲区中的字节数。</p>')),
    (b'<p>The stream returned from this function will yield instances of\r\n<a href="https://doc.rust-lang.org/1.95.0/std/io/error/type.Result.html" title="type std::io::error::Result"><code>io::Result</code></a><code>&lt;</code><a href="https://doc.rust-lang.org/1.95.0/core/option/enum.Option.html" title="enum core::option::Option"><code>Option</code></a><code>&lt;</code><a href="https://doc.rust-lang.org/1.95.0/alloc/string/struct.String.html" title="struct alloc::string::String"><code>String</code></a><code>&gt;&gt;</code>. Each string returned will <em>not</em> have a newline\r\nbyte (the 0xA byte) or <code>CRLF</code> (0xD, 0xA bytes) at the end.</p>',
     E('<p>此函数返回的流将产生 <a href="https://doc.rust-lang.org/1.95.0/std/io/error/type.Result.html" title="type std::io::error::Result"><code>io::Result</code></a><code>&lt;</code><a href="https://doc.rust-lang.org/1.95.0/core/option/enum.Option.html" title="enum core::option::Option"><code>Option</code></a><code>&lt;</code><a href="https://doc.rust-lang.org/1.95.0/alloc/string/struct.String.html" title="struct alloc::string::String"><code>String</code></a><code>&gt;&gt;</code> 的实例。\r\n每个返回的字符串<em>不</em>包含末尾的换行字节（0xA 字节）或 <code>CRLF</code>（0xD, 0xA 字节）。</p>')),
    (b'<p>Each line of the stream has the same error semantics as <a href="trait.AsyncBufReadExt.html#method.read_line" title="method tokio::io::AsyncBufReadExt::read_line"><code>AsyncBufReadExt::read_line</code></a>.</p>',
     E('<p>流中每行的错误语义与 <a href="trait.AsyncBufReadExt.html#method.read_line" title="method tokio::io::AsyncBufReadExt::read_line"><code>AsyncBufReadExt::read_line</code></a> 相同。</p>')),
    (b'<p><a href="https://doc.rust-lang.org/1.95.0/std/io/cursor/struct.Cursor.html" title="struct std::io::cursor::Cursor"><code>std::io::Cursor</code></a> is a type that implements <code>BufRead</code>. In\r\nthis example, we use <a href="https://doc.rust-lang.org/1.95.0/std/io/cursor/struct.Cursor.html" title="struct std::io::cursor::Cursor"><code>Cursor</code></a> to iterate over all the lines in a byte\r\nslice.</p>',
     E('<p><a href="https://doc.rust-lang.org/1.95.0/std/io/cursor/struct.Cursor.html" title="struct std::io::cursor::Cursor"><code>std::io::Cursor</code></a> 是实现 <code>BufRead</code> 的类型。\r\n在此示例中，我们使用 <a href="https://doc.rust-lang.org/1.95.0/std/io/cursor/struct.Cursor.html" title="struct std::io::cursor::Cursor"><code>Cursor</code></a> 遍历字节切片中的所有行。</p>')),
    (b'<p>This trait is <b>not</b> <a href="https://doc.rust-lang.org/1.95.0/reference/items/traits.html#dyn-compatibility">dyn compatible</a>.</p>',
     E('<p>此 trait <b>不</b>是<a href="https://doc.rust-lang.org/1.95.0/reference/items/traits.html#dyn-compatibility">dyn 兼容</a>的。</p>')),
    (b'<p><i>In older versions of Rust, dyn compatibility was called "object safety", so this trait is not object safe.</i></p>',
     E('<p><i>在较早版本的 Rust 中，dyn 兼容性被称为"对象安全"，因此此 trait 不是对象安全的。</i></p>')),
])


# ============================================================
# io/trait.AsyncWriteExt.html
# ============================================================
add('io/trait.AsyncWriteExt.html', [
    (b'<p>Implemented as an extension trait, adding utility methods to all\r\n<a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> types. Callers will tend to import this trait instead of\r\n<a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a>.</p>',
     E('<p>作为扩展 trait 实现，向所有 <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> 类型添加实用方法。\r\n调用者通常会导入此 trait 而不是 <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a>。</p>')),
    (b'<p>See <a href="index.html" title="mod tokio::io">module</a> documentation for more details.</p>',
     E('<p>有关更多详细信息，请参阅 <a href="index.html" title="mod tokio::io">模块</a> 文档。</p>')),
    (b'<p>This function will attempt to write the entire contents of <code>buf</code>, but\r\nthe entire write may not succeed, or the write may also generate an\r\nerror. A call to <code>write</code> represents <em>at most one</em> attempt to write to\r\nany wrapped object.</p>',
     E('<p>此函数将尝试写入 <code>buf</code> 的全部内容，但整个写入可能无法完成，\r\n或者可能产生错误。对 <code>write</code> 的调用表示<em>至多一次</em>对\r\n任何包装对象的写入尝试。</p>')),
    (b'<p>If the return value is <code>Ok(n)</code> then it must be guaranteed that <code>n &lt;= buf.len()</code>. A return value of <code>0</code> typically means that the\r\nunderlying object is no longer able to accept bytes and will likely\r\nnot be able to in the future as well, or that the buffer provided is\r\nempty.</p>',
     E('<p>如果返回值为 <code>Ok(n)</code>，则必须保证 <code>n &lt;= buf.len()</code>。\r\n返回值为 <code>0</code> 通常表示底层对象已无法再接受字节，\r\n将来也不太可能接受，或者所提供的缓冲区为空。</p>')),
    (b'<p>It is <strong>not</strong> considered an error if the entire buffer could not be\r\nwritten to this writer.</p>',
     E('<p>如果无法将整个缓冲区写入此 writer，<strong>不</strong>视为错误。</p>')),
    (b'<p>This method is cancellation safe in the sense that if it is used as\r\nthe event in a <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> statement and some\r\nother branch completes first, then it is guaranteed that no data was\r\nwritten to this <code>AsyncWrite</code>.</p>',
     E('<p>此方法是可取消安全的：如果在 <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a>\r\n语句中作为事件使用且另一个分支先完成，则可以保证没有\r\n数据被写入此 <code>AsyncWrite</code>。</p>')),
    (b'<p>Like <a href="trait.AsyncWriteExt.html#method.write" title="method tokio::io::AsyncWriteExt::write"><code>write</code></a>, except that it writes from a slice of buffers.</p>',
     E('<p>与 <a href="trait.AsyncWriteExt.html#method.write" title="method tokio::io::AsyncWriteExt::write"><code>write</code></a> 类似，但从缓冲区切片中写入数据。</p>')),
    (b'<p>See <a href="trait.AsyncWrite.html#method.poll_write_vectored" title="method tokio::io::AsyncWrite::poll_write_vectored"><code>AsyncWrite::poll_write_vectored</code></a> for more details.</p>',
     E('<p>有关更多详细信息，请参阅 <a href="trait.AsyncWrite.html#method.poll_write_vectored" title="method tokio::io::AsyncWrite::poll_write_vectored"><code>AsyncWrite::poll_write_vectored</code></a>。</p>')),
    (b'<p>This function will attempt to write the entire contents of <code>buf</code>, but\r\nthe entire write may not succeed, or the write may also generate an\r\nerror. After the operation completes, the buffer\xe2\x80\x99s\r\ninternal cursor is advanced by the number of bytes written. A\r\nsubsequent call to <code>write_buf</code> using the <strong>same</strong> <code>buf</code> value will\r\nresume from the point that the first call to <code>write_buf</code> completed.\r\nA call to <code>write_buf</code> represents <em>at most one</em> attempt to write to any\r\nwrapped object.</p>',
     E('<p>此函数将尝试写入 <code>buf</code> 的全部内容，但整个写入可能无法完成，\r\n或者可能产生错误。操作完成后，缓冲区的\r\n内部游标将前进已写入的字节数。后续使用<strong>相同</strong> <code>buf</code> 值调用 <code>write_buf</code> 时，\r\n将从第一次调用 <code>write_buf</code> 完成的位置继续。\r\n对 <code>write_buf</code> 的调用表示<em>至多一次</em>对任何包装对象的写入尝试。</p>')),
    (b'<p><a href="../fs/struct.File.html" title="struct tokio::fs::File"><code>File</code></a> implements <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> and <a href="https://doc.rust-lang.org/1.95.0/std/io/cursor/struct.Cursor.html" title="struct std::io::cursor::Cursor"><code>Cursor</code></a><code>&lt;&amp;[u8]&gt;</code> implements <a href="../../bytes/buf/buf_impl/trait.Buf.html" title="trait bytes::buf::buf_impl::Buf"><code>Buf</code></a>:</p>',
     E('<p><a href="../fs/struct.File.html" title="struct tokio::fs::File"><code>File</code></a> 实现了 <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a>，<a href="https://doc.rust-lang.org/1.95.0/std/io/cursor/struct.Cursor.html" title="struct std::io::cursor::Cursor"><code>Cursor</code></a><code>&lt;&amp;[u8]&gt;</code> 实现了 <a href="../../bytes/buf/buf_impl/trait.Buf.html" title="trait bytes::buf::buf_impl::Buf"><code>Buf</code></a>：</p>')),
    (b'<p>This method will continuously call <a href="trait.AsyncWriteExt.html#method.write" title="method tokio::io::AsyncWriteExt::write"><code>write</code></a> until\r\n<a href="../../bytes/buf/buf_impl/trait.Buf.html#method.has_remaining" title="method bytes::buf::buf_impl::Buf::has_remaining"><code>buf.has_remaining()</code></a> returns false. This method will not\r\nreturn until the entire buffer has been successfully written or an error occurs. The\r\nfirst error generated will be returned.</p>',
     E('<p>此方法会持续调用 <a href="trait.AsyncWriteExt.html#method.write" title="method tokio::io::AsyncWriteExt::write"><code>write</code></a>，\r\n直到 <a href="../../bytes/buf/buf_impl/trait.Buf.html#method.has_remaining" title="method bytes::buf::buf_impl::Buf::has_remaining"><code>buf.has_remaining()</code></a> 返回 false。\r\n此方法在成功写入整个缓冲区或发生错误之前不会返回。\r\n将返回生成的第一个错误。</p>')),
    (b'<p>The buffer is advanced after each chunk is successfully written. After failure,\r\n<code>src.chunk()</code> will return the chunk that failed to write.</p>',
     E('<p>每个块成功写入后，游标会前进。失败后，<code>src.chunk()</code> 将返回未能写入的块。</p>')),
    (b'<p>If <code>write_all_buf</code> is used as the event in a\r\n<a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> statement and some other branch\r\ncompletes first, then the data in the provided buffer may have been\r\npartially written. However, it is guaranteed that the provided\r\nbuffer has been <a href="../../bytes/buf/buf_impl/trait.Buf.html#tymethod.advance" title="method bytes::buf::buf_impl::Buf::advance">advanced</a> by the amount of bytes that have been\r\npartially written.</p>',
     E('<p>如果在 <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> 语句中将 <code>write_all_buf</code>\r\n作为事件使用，且另一个分支先完成，则提供的缓冲区中的数据可能已被\r\n部分写入。但是，可以保证提供的缓冲区已按\r\n已部分写入的字节数<a href="../../bytes/buf/buf_impl/trait.Buf.html#tymethod.advance" title="method bytes::buf::buf_impl::Buf::advance">前进</a>。</p>')),
    (b'<p>This method will continuously call <a href="trait.AsyncWriteExt.html#method.write" title="method tokio::io::AsyncWriteExt::write"><code>write</code></a> until there is no more data\r\nto be written. This method will not return until the entire buffer\r\nhas been successfully written or such an error occurs. The first\r\nerror generated from this method will be returned.</p>',
     E('<p>此方法会持续调用 <a href="trait.AsyncWriteExt.html#method.write" title="method tokio::io::AsyncWriteExt::write"><code>write</code></a>，\r\n直到没有更多数据可写。此方法在成功写入整个缓冲区或发生此类错误之前不会返回。\r\n将返回由此方法生成的第一个错误。</p>')),
    (b'<p>This method is not cancellation safe. If it is used as the event\r\nin a <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> statement and some other\r\nbranch completes first, then the provided buffer may have been\r\npartially written, but future calls to <code>write_all</code> will start over\r\nfrom the beginning of the buffer.</p>',
     E('<p>此方法不是可取消安全的。如果在 <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a>\r\n语句中将其作为事件使用，且另一个分支先完成，\r\n则提供的缓冲区可能已被部分写入，但后续对 <code>write_all</code> 的调用\r\n将从头开始重新写入缓冲区。</p>')),
    (b'<p>This function will return the first error that <a href="trait.AsyncWriteExt.html#method.write" title="method tokio::io::AsyncWriteExt::write"><code>write</code></a> returns.</p>',
     E('<p>此函数将返回 <a href="trait.AsyncWriteExt.html#method.write" title="method tokio::io::AsyncWriteExt::write"><code>write</code></a> 返回的第一个错误。</p>')),
    (b'<p>It is recommended to use a buffered writer to avoid excessive\r\nsyscalls.</p>',
     E('<p>建议使用缓冲写入器以避免过多的系统调用。</p>')),
    (b'<p>This method returns the same errors as <a href="trait.AsyncWriteExt.html#method.write_all" title="method tokio::io::AsyncWriteExt::write_all"><code>AsyncWriteExt::write_all</code></a>.</p>',
     E('<p>此方法返回与 <a href="trait.AsyncWriteExt.html#method.write_all" title="method tokio::io::AsyncWriteExt::write_all"><code>AsyncWriteExt::write_all</code></a> 相同的错误。</p>')),
    (b'<p>Write unsigned 8 bit integers to a <code>AsyncWrite</code>:</p>',
     E('<p>将无符号 8 位整数写入 <code>AsyncWrite</code>：</p>')),
    (b'<p>Write signed 8 bit integers to a <code>AsyncWrite</code>:</p>',
     E('<p>将有符号 8 位整数写入 <code>AsyncWrite</code>：</p>')),
    (b'<p>Write unsigned 16-bit integers to a <code>AsyncWrite</code>:</p>',
     E('<p>将无符号 16 位整数写入 <code>AsyncWrite</code>：</p>')),
    (b'<p>Write signed 16-bit integers to a <code>AsyncWrite</code>:</p>',
     E('<p>将有符号 16 位整数写入 <code>AsyncWrite</code>：</p>')),
    (b'<p>Write unsigned 32-bit integers to a <code>AsyncWrite</code>:</p>',
     E('<p>将无符号 32 位整数写入 <code>AsyncWrite</code>：</p>')),
    (b'<p>Write signed 32-bit integers to a <code>AsyncWrite</code>:</p>',
     E('<p>将有符号 32 位整数写入 <code>AsyncWrite</code>：</p>')),
    (b'<p>Write unsigned 64-bit integers to a <code>AsyncWrite</code>:</p>',
     E('<p>将无符号 64 位整数写入 <code>AsyncWrite</code>：</p>')),
    (b'<p>Writes an signed 64-bit integer in big-endian order to the\r\nunderlying writer.</p>',
     E('<p>以大端字节序将有符号 64 位整数写入底层 writer。</p>')),
    (b'<p>Write signed 64-bit integers to a <code>AsyncWrite</code>:</p>',
     E('<p>将有符号 64 位整数写入 <code>AsyncWrite</code>：</p>')),
    (b'<p>Write unsigned 128-bit integers to a <code>AsyncWrite</code>:</p>',
     E('<p>将无符号 128 位整数写入 <code>AsyncWrite</code>：</p>')),
    (b'<p>Write signed 128-bit integers to a <code>AsyncWrite</code>:</p>',
     E('<p>将有符号 128 位整数写入 <code>AsyncWrite</code>：</p>')),
    (b'<p>Write 32-bit floating point type to a <code>AsyncWrite</code>:</p>',
     E('<p>将 32 位浮点类型写入 <code>AsyncWrite</code>：</p>')),
    (b'<p>Write 64-bit floating point type to a <code>AsyncWrite</code>:</p>',
     E('<p>将 64 位浮点类型写入 <code>AsyncWrite</code>：</p>')),
    (b'<p>This method is cancel safe.</p>',
     E('<p>此方法是可取消安全的。</p>')),
    (b'<p>If <code>flush</code> is used as the event in a <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a>\r\nstatement and some other branch completes first, then the data in the\r\nbuffered data in this <code>AsyncWrite</code> may have been partially flushed.\r\nHowever, it is guaranteed that the buffer is advanced by the amount of\r\nbytes that have been partially flushed.</p>',
     E('<p>如果在 <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> 语句中将 <code>flush</code>\r\n作为事件使用，且另一个分支先完成，则此 <code>AsyncWrite</code> 中缓冲的数据可能\r\n已被部分刷新。但是，可以保证缓冲区按已部分刷新的\r\n字节数前进。</p>')),
    (b'<p>Similar to <a href="trait.AsyncWriteExt.html#method.flush" title="method tokio::io::AsyncWriteExt::flush"><code>flush</code></a>, all intermediately buffered content is written to\r\nthe underlying stream. Once the operation completes, the caller should\r\nno longer attempt to write to the stream. For example, the\r\n<code>TcpStream</code> implementation will issue a <code>shutdown(Write)</code> sys call.</p>',
     E('<p>与 <a href="trait.AsyncWriteExt.html#method.flush" title="method tokio::io::AsyncWriteExt::flush"><code>flush</code></a> 类似，所有中间缓冲的内容都会写入到底层流。\r\n操作完成后，调用方不应再尝试写入该流。例如，<code>TcpStream</code> 的实现会发出\r\n<code>shutdown(Write)</code> 系统调用。</p>')),
    (b'<p>This trait is <b>not</b> <a href="https://doc.rust-lang.org/1.95.0/reference/items/traits.html#dyn-compatibility">dyn compatible</a>.</p>',
     E('<p>此 trait <b>不</b>是<a href="https://doc.rust-lang.org/1.95.0/reference/items/traits.html#dyn-compatibility">dyn 兼容</a>的。</p>')),
    (b'<p><i>In older versions of Rust, dyn compatibility was called "object safety", so this trait is not object safe.</i></p>',
     E('<p><i>在较早版本的 Rust 中，dyn 兼容性被称为"对象安全"，因此此 trait 不是对象安全的。</i></p>')),
])


def main():
    total = 0
    files_touched = 0
    for rel, pairs in PLAN:
        raw = read_bytes(rel)
        file_hits = 0
        for old, new in pairs:
            if old in raw:
                count = raw.count(old)
                raw = raw.replace(old, new)
                file_hits += count
                print(f'  [{rel}] {count} hit(s)')
            else:
                print(f'  [{rel}] MISS: {old[:60]!r}...')
        if file_hits > 0:
            write_bytes(rel, raw)
            files_touched += 1
            total += file_hits
    print(f'\nTotal: {total} replacements across {files_touched} files')


# ============================================================
# process/struct.Child.html
# ============================================================
add('process/struct.Child.html', [
    (b'<p>Representation of a child process spawned onto an event loop.</p>',
     E('<p>表示已生成到事件循环上的子进程。</p>')),
    (b'<p>Similar to the behavior to the standard library, and unlike the futures\r\nparadigm of dropping-implies-cancellation, a spawned process will, by\r\ndefault, continue to execute even after the <code>Child</code> handle has been dropped.</p>',
     E('<p>与标准库的行为类似，且与 futures 范式中"丢弃即取消"不同，\r\n默认情况下，已生成的进程即使在 <code>Child</code> 句柄被丢弃后仍将继续执行。</p>')),
    (b'<p>The <code>Command::kill_on_drop</code> method can be used to modify this behavior\r\nand kill the child process if the <code>Child</code> wrapper is dropped before it\r\nhas exited.</p>',
     E('<p><code>Command::kill_on_drop</code> 方法可用于修改此行为，\r\n在 <code>Child</code> 包装器在子进程退出前被丢弃时杀死子进程。</p>')),
    (b'<p>to avoid partially moving the <code>child</code> and thus blocking yourself from calling\r\nfunctions on <code>child</code> while using <code>stdout</code>.</p>',
     E('<p>这可以避免部分移动 <code>child</code>，从而在使用 <code>stdout</code> 时不会阻碍对 <code>child</code> 函数的调用。</p>')),
    (b'<p>to avoid partially moving the <code>child</code> and thus blocking yourself from calling\r\nfunctions on <code>child</code> while using <code>stderr</code>.</p>',
     E('<p>这可以避免部分移动 <code>child</code>，从而在使用 <code>stderr</code> 时不会阻碍对 <code>child</code> 函数的调用。</p>')),
    (b'<p>Extracts the raw handle of the process associated with this child while\r\nit is still running. Returns <code>None</code> if the child has exited.</p>',
     E('<p>在子进程仍在运行时，提取与此子进程关联的原始句柄。\r\n如果子进程已退出，则返回 <code>None</code>。</p>')),
    (b'<p>Attempts to force the child to exit, but does not wait for the request\r\nto take effect.</p>',
     E('<p>尝试强制子进程退出，但不等待请求生效。</p>')),
    (b'<p>Forces the child to exit.</p>',
     E('<p>强制子进程退出。</p>')),
    (b'<p>This is equivalent to sending a <code>SIGKILL</code> on unix platforms\r\nfollowed by <a href="struct.Child.html#method.wait" title="method tokio::process::Child::wait"><code>wait</code></a>.</p>',
     E('<p>这相当于在 unix 平台上发送 <code>SIGKILL</code>，\r\n然后调用 <a href="struct.Child.html#method.wait" title="method tokio::process::Child::wait"><code>wait</code></a>。</p>')),
    (b'<p>Note: std version of <a href="https://doc.rust-lang.org/1.95.0/std/process/struct.Child.html#method.kill" title="method std::process::Child::kill"><code>Child::kill</code></a> does not <code>wait</code>.\r\nFor an equivalent of <code>Child::kill</code> in the standard library,\r\nuse <a href="struct.Child.html#method.start_kill" title="method tokio::process::Child::start_kill"><code>start_kill</code></a>.</p>',
     E('<p>注意：标准库版本的 <a href="https://doc.rust-lang.org/1.95.0/std/process/struct.Child.html#method.kill" title="method std::process::Child::kill"><code>Child::kill</code></a> 不会 <code>wait</code>。\r\n在标准库中，如需等价于 <code>Child::kill</code> 的功能，\r\n请使用 <a href="struct.Child.html#method.start_kill" title="method tokio::process::Child::start_kill"><code>start_kill</code></a>。</p>')),
    (b'<p>If the child has to be killed remotely, it is possible to do it using\r\na combination of the select! macro and a <code>oneshot</code> channel. In the following\r\nexample, the child will run until completion unless a message is sent on\r\nthe <code>oneshot</code> channel. If that happens, the child is killed immediately\r\nusing the <code>.kill()</code> method.</p>',
     E('<p>如果需要远程杀死子进程，可以使用 select! 宏\r\n结合 <code>oneshot</code> 信道来实现。在以下示例中，子进程将运行到完成，\r\n除非在 <code>oneshot</code> 信道上发送消息。\r\n如果发送了消息，则会立即使用 <code>.kill()</code> 方法杀死子进程。</p>')),
    (b'<p>You can also interact with the child\xe2\x80\x99s standard I/O. For example, you can\r\nread its stdout while waiting for it to exit.</p>',
     E('<p>你还可以与子进程的标准 I/O 交互。例如，\r\n可以在等待子进程退出的同时读取其 stdout。</p>')),
    (b'<p>The stdin handle to the child process, if any, will be closed\r\nbefore waiting. This helps avoid deadlock: it ensures that the\r\nchild does not block waiting for input from the parent, while\r\nthe parent waits for the child to exit.</p>',
     E('<p>子进程的 stdin 句柄（如果有）在等待之前会被关闭。\r\n这有助于避免死锁：它确保子进程不会因等待父进程的输入而阻塞，\r\n而父进程则在等待子进程退出。</p>')),
    (b'<p>This function will not block the calling thread and will only\r\ncheck to see if the child process has exited or not. If the child has\r\nexited then on Unix the process ID is reaped. This function is\r\nguaranteed to repeatedly return a successful exit status so long as the\r\nchild has already exited.</p>',
     E('<p>此函数不会阻塞调用线程，只会检查子进程是否已退出。\r\n如果子进程已退出，则在 Unix 上会回收其进程 ID。\r\n只要子进程已经退出，此函数保证可以重复返回成功的退出状态。</p>')),
    # method.id second p (partially translated)
    (E('<p>一旦子进程被轮询到完成，此方法将返回 <code>None</code>。\r\nThis is done to avoid confusion on platforms like Unix where the OS\r\nidentifier could be reused once the process has completed.</p>'),
     E('<p>一旦子进程被轮询到完成，此方法将返回 <code>None</code>。\r\n这样做是为了避免在 Unix 等操作系统上引起混淆——这些平台上\r\n进程完成后，操作系统标识符可能会被回收复用。</p>')),
])


# ============================================================
# process/struct.ChildStderr.html
# ============================================================
add('process/struct.ChildStderr.html', [
    (b'<p>The standard error stream for spawned children.</p>',
     E('<p>已生成子进程的标准错误流。</p>')),
    (b'<p>This type implements the <code>AsyncRead</code> trait to read data from the stderr\r\nhandle of a child process asynchronously.</p>',
     E('<p>此类型实现 <code>AsyncRead</code> trait，可用于从子进程的 stderr\r\n句柄异步读取数据。</p>')),
    (b'<p>Convert into <a href="https://doc.rust-lang.org/1.95.0/std/os/windows/io/handle/struct.OwnedHandle.html" title="struct std::os::windows::io::handle::OwnedHandle"><code>OwnedHandle</code></a>.</p>',
     E('<p>转换为 <a href="https://doc.rust-lang.org/1.95.0/std/os/windows/io/handle/struct.OwnedHandle.html" title="struct std::os::windows::io::handle::OwnedHandle"><code>OwnedHandle</code></a>。</p>')),
])


# ============================================================
# process/struct.ChildStdin.html
# ============================================================
add('process/struct.ChildStdin.html', [
    (b'<p>The standard input stream for spawned children.</p>',
     E('<p>已生成子进程的标准输入流。</p>')),
    (b'<p>This type implements the <code>AsyncWrite</code> trait to pass data to the stdin\r\nhandle of a child process asynchronously.</p>',
     E('<p>此类型实现 <code>AsyncWrite</code> trait，可用于向子进程的 stdin\r\n句柄异步传递数据。</p>')),
    (b'<p>Convert into <a href="https://doc.rust-lang.org/1.95.0/std/os/windows/io/handle/struct.OwnedHandle.html" title="struct std::os::windows::io::handle::OwnedHandle"><code>OwnedHandle</code></a>.</p>',
     E('<p>转换为 <a href="https://doc.rust-lang.org/1.95.0/std/os/windows/io/handle/struct.OwnedHandle.html" title="struct std::os::windows::io::handle::OwnedHandle"><code>OwnedHandle</code></a>。</p>')),
])


# ============================================================
# process/struct.ChildStdout.html
# ============================================================
add('process/struct.ChildStdout.html', [
    (b'<p>The standard output stream for spawned children.</p>',
     E('<p>已生成子进程的标准输出流。</p>')),
    (b'<p>This type implements the <code>AsyncRead</code> trait to read data from the stdout\r\nhandle of a child process asynchronously.</p>',
     E('<p>此类型实现 <code>AsyncRead</code> trait，可用于从子进程的 stdout\r\n句柄异步读取数据。</p>')),
    (b'<p>Convert into <a href="https://doc.rust-lang.org/1.95.0/std/os/windows/io/handle/struct.OwnedHandle.html" title="struct std::os::windows::io::handle::OwnedHandle"><code>OwnedHandle</code></a>.</p>',
     E('<p>转换为 <a href="https://doc.rust-lang.org/1.95.0/std/os/windows/io/handle/struct.OwnedHandle.html" title="struct std::os::windows::io::handle::OwnedHandle"><code>OwnedHandle</code></a>。</p>')),
])


# ============================================================
# process/struct.Command.html
# ============================================================
add('process/struct.Command.html', [
    (b'<p>Cheaply convert to a <code>&amp;std::process::Command</code> for places where the type from the standard\r\nlibrary is expected.</p>',
     E('<p>廉价地转换为 <code>&amp;std::process::Command</code>，用于期望使用标准库类型的位置。</p>')),
    (b'<p>Cheaply convert to a <code>&amp;mut std::process::Command</code> for places where the type from the\r\nstandard library is expected.</p>',
     E('<p>廉价地转换为 <code>&amp;mut std::process::Command</code>，用于期望使用标准库类型的位置。</p>')),
    (b'<p>Controls whether a <code>kill</code> operation should be invoked on a spawned child\r\nprocess when its corresponding <code>Child</code> handle is dropped.</p>\r\n<p>By default, this value is assumed to be <code>false</code>, meaning the next spawned\r\nprocess will not be killed on drop, similar to the behavior of the standard\r\nlibrary.</p>',
     E('<p>控制在丢弃对应的 <code>Child</code> 句柄时，是否应对已生成的子进程调用 <code>kill</code> 操作。</p>\r\n<p>默认情况下，此值假定为 <code>false</code>，即下一个生成的进程在丢弃时不会被杀死，\r\n与标准库的行为类似。</p>')),
    (b'<p>On Unix platforms processes must be \xe2\x80\x9creaped\xe2\x80\x9d by their parent process after\r\nthey have exited in order to release all OS resources. A child process which\r\nhas exited, but has not yet been reaped by its parent is considered a \xe2\x80\x9czombie\xe2\x80\x9d\r\nprocess. Such processes continue to count against limits imposed by the system,\r\nand having too many zombie processes present can prevent additional processes\r\nfrom being spawned.</p>',
     E('<p>在 Unix 平台上，进程退出后必须由其父进程\xe2\x80\x9c回收\xe2\x80\x9d，\r\n以释放所有操作系统资源。已退出但尚未被父进程回收的子进程被视为\xe2\x80\x9c僵尸\xe2\x80\x9d进程。\r\n此类进程仍会计入系统施加的限制，\r\n并且存在过多僵尸进程可能会阻止新进程的生成。</p>')),
    (b'<p>Although issuing a <code>kill</code> signal to the child process is a synchronous\r\noperation, the resulting zombie process cannot be <code>.await</code>ed inside of the\r\ndestructor to avoid blocking other tasks. The tokio runtime will, on a\r\nbest-effort basis, attempt to reap and clean up such processes in the\r\nbackground, but no additional guarantees are made with regard to\r\nhow quickly or how often this procedure will take place.</p>',
     E('<p>虽然向子进程发出 <code>kill</code> 信号是同步操作，\r\n但生成的僵尸进程无法在析构函数中 <code>.await</code>，\r\n以避免阻塞其他任务。Tokio 运行时将尽最大努力\r\n在后台尝试回收和清理此类进程，\r\n但对于此过程的发生频率和速度不提供额外保证。</p>')),
    (b'<p>If stronger guarantees are required, it is recommended to avoid dropping\r\na <a href="struct.Child.html" title="struct tokio::process::Child"><code>Child</code></a> handle where possible, and instead utilize <code>child.wait().await</code>\r\nor <code>child.kill().await</code> where possible.</p>',
     E('<p>如果需要更强的保证，建议尽可能避免丢弃\r\n<a href="struct.Child.html" title="struct tokio::process::Child"><code>Child</code></a> 句柄，\r\n而应尽可能使用 <code>child.wait().await</code>\r\n或 <code>child.kill().await</code>。</p>')),
    (b'<p>Sets the <a href="https://msdn.microsoft.com/en-us/library/windows/desktop/ms684863(v=vs.85).aspx">process creation flags</a> to be passed to <code>CreateProcess</code>.</p>\r\n<p>These will always be ORed with <code>CREATE_UNICODE_ENVIRONMENT</code>.</p>',
     E('<p>设置传递给 <code>CreateProcess</code> 的<a href="https://msdn.microsoft.com/en-us/library/windows/desktop/ms684863(v=vs.85).aspx">进程创建标志</a>。</p>\r\n<p>这些标志始终会与 <code>CREATE_UNICODE_ENVIRONMENT</code> 进行 OR 运算。</p>')),
])


# ============================================================
# macro.join.html
# ============================================================
add('macro.join.html', [
    (b'<p>Waits on multiple concurrent branches, returning when <strong>all</strong> branches\r\ncomplete.</p>',
     E('<p>等待多个并发分支，当<strong>所有</strong>分支完成时返回。</p>')),
    (b'<p>When working with async expressions returning <code>Result</code>, <code>join!</code> will wait\r\nfor <strong>all</strong> branches complete regardless if any complete with <code>Err</code>. Use\r\n<a href="macro.try_join.html" title="macro tokio::try_join"><code>try_join!</code></a> to return early when <code>Err</code> is encountered.</p>',
     E('<p>对于返回 <code>Result</code> 的异步表达式，<code>join!</code> 将等待\r\n<strong>所有</strong>分支完成，无论是否有任何分支以 <code>Err</code> 完成。\r\n使用 <a href="macro.try_join.html" title="macro tokio::try_join"><code>try_join!</code></a> 在遇到 <code>Err</code> 时提早返回。</p>')),
    (b'<p>By running all async expressions on the current task, the expressions are\r\nable to run <strong>concurrently</strong> but not in <strong>parallel</strong>. This means all\r\nexpressions are run on the same thread and if one branch blocks the thread,\r\nall other expressions will be unable to continue. If parallelism is\r\nrequired, spawn each async expression using <a href="task/fn.spawn.html" title="fn tokio::task::spawn"><code>tokio::spawn</code></a> and pass the\r\njoin handle to <code>join!</code>.</p>',
     E('<p>由于所有异步表达式都在当前任务上运行，这些表达式\r\n能够<strong>并发</strong>运行，但不能<strong>并行</strong>运行。这意味着所有\r\n表达式都在同一线程上运行，如果某个分支阻塞了线程，\r\n所有其他表达式都将无法继续。如果需要并行执行，\r\n请使用 <a href="task/fn.spawn.html" title="fn tokio::task::spawn"><code>tokio::spawn</code></a> 生成每个异步表达式，\r\n然后将其 join handle 传递给 <code>join!</code>。</p>')),
    (b'<p>By default, <code>join!</code>\xe2\x80\x99s generated future rotates which contained\r\nfuture is polled first whenever it is woken.</p>',
     E('<p>默认情况下，每次唤醒时，<code>join!</code> 生成的 future 会轮换首先\r\n轮询哪个包含的 future。</p>')),
    (b'<p>This behavior can be overridden by adding <code>biased;</code> to the beginning of the\r\nmacro usage. See the examples for details. This will cause <code>join</code> to poll\r\nthe futures in the order they appear from top to bottom.</p>',
     E('<p>可以通过在宏使用的开头添加 <code>biased;</code> 来覆盖此行为。\r\n有关详细信息，请参阅示例。这将使 <code>join</code> 按 future\r\n出现的顺序（从上到下）进行轮询。</p>')),
    (b'<p>Using the <code>biased;</code> mode to control polling order.</p>',
     E('<p>使用 <code>biased;</code> 模式控制轮询顺序。</p>')),
])


# ============================================================
# macro.try_join.html
# ============================================================
add('macro.try_join.html', [
    (b'<p>Waits on multiple concurrent branches, returning when <strong>all</strong> branches\r\ncomplete with <code>Ok(_)</code> or on the first <code>Err(_)</code>.</p>',
     E('<p>等待多个并发分支，当<strong>所有</strong>分支以 <code>Ok(_)</code> 完成时返回，\r\n或在第一个 <code>Err(_)</code> 时返回。</p>')),
    (b'<p>Similar to <a href="macro.join.html" title="macro tokio::join"><code>join!</code></a>, the <code>try_join!</code> macro takes a list of async\r\nexpressions and evaluates them concurrently on the same task. Each async\r\nexpression evaluates to a future and the futures from each expression are\r\nmultiplexed on the current task. The <code>try_join!</code> macro returns when <strong>all</strong>\r\nbranches return with <code>Ok</code> or when the <strong>first</strong> branch returns with <code>Err</code>.</p>',
     E('<p>与 <a href="macro.join.html" title="macro tokio::join"><code>join!</code></a> 类似，<code>try_join!</code> 宏接受一组\r\n异步表达式，并在同一任务上并发求值它们。每个异步\r\n表达式求值为一个 future，来自每个表达式的 future\r\n在当前任务上多路复用。<code>try_join!</code> 宏在<strong>所有</strong>分支\r\n返回 <code>Ok</code> 时或<strong>第一个</strong>分支返回 <code>Err</code> 时返回。</p>')),
    (b'<p>By running all async expressions on the current task, the expressions are\r\nable to run <strong>concurrently</strong> but not in <strong>parallel</strong>. This means all\r\nexpressions are run on the same thread and if one branch blocks the thread,\r\nall other expressions will be unable to continue. If parallelism is\r\nrequired, spawn each async expression using <a href="task/fn.spawn.html" title="fn tokio::task::spawn"><code>tokio::spawn</code></a> and pass the\r\njoin handle to <code>try_join!</code>.</p>',
     E('<p>由于所有异步表达式都在当前任务上运行，这些表达式\r\n能够<strong>并发</strong>运行，但不能<strong>并行</strong>运行。这意味着所有\r\n表达式都在同一线程上运行，如果某个分支阻塞了线程，\r\n所有其他表达式都将无法继续。如果需要并行执行，\r\n请使用 <a href="task/fn.spawn.html" title="fn tokio::task::spawn"><code>tokio::spawn</code></a> 生成每个异步表达式，\r\n然后将其 join handle 传递给 <code>try_join!</code>。</p>')),
    (b'<p>By default, <code>try_join!</code>\xe2\x80\x99s generated future rotates which\r\ncontained future is polled first whenever it is woken.</p>',
     E('<p>默认情况下，每次唤醒时，<code>try_join!</code> 生成的 future 会轮换首先\r\n轮询哪个包含的 future。</p>')),
    (b'<p>This behavior can be overridden by adding <code>biased;</code> to the beginning of the\r\nmacro usage. See the examples for details. This will cause <code>try_join</code> to poll\r\nthe futures in the order they appear from top to bottom.</p>',
     E('<p>可以通过在宏使用的开头添加 <code>biased;</code> 来覆盖此行为。\r\n有关详细信息，请参阅示例。这将使 <code>try_join</code> 按 future\r\n出现的顺序（从上到下）进行轮询。</p>')),
    (b'<p>Basic <code>try_join</code> with two branches.</p>',
     E('<p>具有两个分支的基础 <code>try_join</code>。</p>')),
    (b'<p>Using <code>try_join!</code> with spawned tasks.</p>',
     E('<p>将 <code>try_join!</code> 与生成的任务一起使用。</p>')),
    (b'<p>Using the <code>biased;</code> mode to control polling order.</p>',
     E('<p>使用 <code>biased;</code> 模式控制轮询顺序。</p>')),
])


# ============================================================
# macro.select.html
# ============================================================
add('macro.select.html', [
    (b'<p>Waits on multiple concurrent branches, returning when the <strong>first</strong> branch\r\ncompletes, cancelling the remaining branches.</p>',
     E('<p>等待多个并发分支，当<strong>第一个</strong>分支完成时返回，\r\n并取消其余分支。</p>')),
    (b'<p>Additionally, the <code>select!</code> macro may include a single, optional <code>else</code>\r\nbranch, which evaluates if none of the other branches match their patterns:</p>',
     E('<p>此外，<code>select!</code> 宏可以包含一个可选的 <code>else</code> 分支，\r\n在没有其他分支匹配其模式时进行求值：</p>')),
    (b'<p>The macro aggregates all <code>&lt;async expression&gt;</code> expressions and runs them\r\nconcurrently on the <strong>current</strong> task. Once the <strong>first</strong> expression\r\ncompletes with a value that matches its <code>&lt;pattern&gt;</code>, the <code>select!</code> macro\r\nreturns the result of evaluating the completed branch\xe2\x80\x99s <code>&lt;handler&gt;</code>\r\nexpression.</p>',
     E('<p>宏会聚合所有 <code>&lt;async expression&gt;</code> 表达式，\r\n并在<strong>当前</strong>任务上并发运行它们。一旦<strong>第一个</strong>表达式\r\n以匹配其 <code>&lt;pattern&gt;</code> 的值完成，<code>select!</code> 宏\r\n就会返回已完成分支的 <code>&lt;handler&gt;</code> 表达式的求值结果。</p>')),
    (b'<p>Additionally, each branch may include an optional <code>if</code> precondition. If the\r\nprecondition returns <code>false</code>, then the branch is disabled. The provided\r\n<code>&lt;async expression&gt;</code> is still evaluated but the resulting future is never\r\npolled. This capability is useful when using <code>select!</code> within a loop.</p>',
     E('<p>此外，每个分支可以包含一个可选的 <code>if</code> 前置条件。如果\r\n前置条件返回 <code>false</code>，则该分支被禁用。提供的\r\n<code>&lt;async expression&gt;</code> 仍会被求值，但生成的 future 永远不会被\r\n轮询。此功能在循环中使用 <code>select!</code> 时非常有用。</p>')),
    (b'<p>The complete lifecycle of a <code>select!</code> expression is as follows:</p>',
     E('<p><code>select!</code> 表达式的完整生命周期如下：</p>')),
    (b'<p>By running all async expressions on the current task, the expressions are\r\nable to run <strong>concurrently</strong> but not in <strong>parallel</strong>. This means all\r\nexpressions are run on the same thread and if one branch blocks the thread,\r\nall other expressions will be unable to continue. If parallelism is\r\nrequired, spawn each async expression using <a href="task/fn.spawn.html" title="fn tokio::task::spawn"><code>tokio::spawn</code></a> and pass the\r\njoin handle to <code>select!</code>.</p>',
     E('<p>由于所有异步表达式都在当前任务上运行，这些表达式\r\n能够<strong>并发</strong>运行，但不能<strong>并行</strong>运行。这意味着所有\r\n表达式都在同一线程上运行，如果某个分支阻塞了线程，\r\n所有其他表达式都将无法继续。如果需要并行执行，\r\n请使用 <a href="task/fn.spawn.html" title="fn tokio::task::spawn"><code>tokio::spawn</code></a> 生成每个异步表达式，\r\n然后将其 join handle 传递给 <code>select!</code>。</p>')),
    (b'<p>By default, <code>select!</code> randomly picks a branch to check first. This provides\r\nsome level of fairness when calling <code>select!</code> in a loop with branches that\r\nare always ready.</p>',
     E('<p>默认情况下，<code>select!</code> 会随机选择一个分支优先检查。\r\n当在循环中调用 <code>select!</code> 且分支始终就绪时，\r\n这提供了一定程度的公平性。</p>')),
    (b'<p>This behavior can be overridden by adding <code>biased;</code> to the beginning of the\r\nmacro usage. See the examples for details. This will cause <code>select</code> to poll\r\nthe futures in the order they appear from top to bottom. There are a few\r\nreasons you may want this:</p>',
     E('<p>可以通过在宏使用的开头添加 <code>biased;</code> 来覆盖此行为。\r\n有关详细信息，请参阅示例。这将使 <code>select</code> 按 future\r\n出现的顺序（从上到下）进行轮询。出于以下几种原因，你可能希望这样做：</p>')),
    (b'<p>But there is an important caveat to this mode. It becomes your responsibility\r\nto ensure that the polling order of your futures is fair. If for example you\r\nare selecting between a stream and a shutdown future, and the stream has a\r\nhuge volume of messages and zero or nearly zero time between them, you should\r\nplace the shutdown future earlier in the <code>select!</code> list to ensure that it is\r\nalways polled, and will not be ignored due to the stream being constantly\r\nready.</p>',
     E('<p>但此模式有一个重要的注意事项。确保你的 future 的轮询顺序是公平的\r\n成为了你的责任。例如，如果你在流和关闭 future 之间进行选择，\r\n而流有大量消息且消息之间的时间间隔为零或几乎为零，\r\n则应将关闭 future 放在 <code>select!</code> 列表的更靠前位置，\r\n以确保它始终被轮询，并且不会因为流始终就绪而被忽略。</p>')),
    (b'<p>The <code>select!</code> macro panics if all branches are disabled <strong>and</strong> there is no\r\nprovided <code>else</code> branch. A branch is disabled when the provided <code>if</code>\r\nprecondition returns <code>false</code> <strong>or</strong> when the pattern does not match the\r\nresult of <code>&lt;async expression&gt;</code>.</p>',
     E('<p>如果所有分支都被禁用<strong>且</strong>没有提供 <code>else</code> 分支，\r\n则 <code>select!</code> 宏会 panic。当提供的 <code>if</code>\r\n前置条件返回 <code>false</code> <strong>或</strong>模式与\r\n<code>&lt;async expression&gt;</code> 的结果不匹配时，分支被禁用。</p>')),
    (b'<p>When using <code>select!</code> in a loop to receive messages from multiple sources,\r\nyou should make sure that the receive call is cancellation safe to avoid\r\nlosing messages. This section goes through various common methods and\r\ndescribes whether they are cancel safe.  The lists in this section are not\r\nexhaustive.</p>',
     E('<p>在循环中使用 <code>select!</code> 从多个来源接收消息时，\r\n应确保接收调用是可取消安全的，以避免\r\n丢失消息。本节介绍各种常见方法并\r\n说明它们是否是可取消安全的。本节中的列表并不\r\n详尽。</p>')),
    (b'<p>The following methods are cancellation safe:</p>',
     E('<p>以下方法是可取消安全的：</p>')),
    (b'<p>The following methods are not cancellation safe and can lead to loss of data:</p>',
     E('<p>以下方法不是可取消安全的，可能导致数据丢失：</p>')),
    (b'<p>The following methods are not cancellation safe because they use a queue for\r\nfairness and cancellation makes you lose your place in the queue:</p>',
     E('<p>以下方法不是可取消安全的，因为它们使用队列以保证公平性，\r\n而取消会使你在队列中失去位置：</p>')),
    (b'<p>To determine whether your own methods are cancellation safe, look for the\r\nlocation of uses of <code>.await</code>. This is because when an asynchronous method is\r\ncancelled, that always happens at an <code>.await</code>. If your function behaves\r\ncorrectly even if it is restarted while waiting at an <code>.await</code>, then it is\r\ncancellation safe.</p>',
     E('<p>要判断你自己的方法是否可取消安全，请查找\r\n<code>.await</code> 的使用位置。这是因为当异步方法被\r\n取消时，这总是发生在 <code>.await</code> 处。如果你的函数\r\n即使在 <code>.await</code> 处等待时被重启也能正确运行，\r\n那么它就是可取消安全的。</p>')),
    (b'<p>Cancellation safety can be defined in the following way: If you have a\r\nfuture that has not yet completed, then it must be a no-op to drop that\r\nfuture and recreate it. This definition is motivated by the situation where\r\na <code>select!</code> is used in a loop. Without this guarantee, you would lose your\r\nprogress when another branch completes and you restart the <code>select!</code> by\r\ngoing around the loop.</p>',
     E('<p>可以按以下方式定义可取消安全：如果你有一个\r\n尚未完成的 future，那么丢弃该 future\r\n并重新创建它必须是无操作（no-op）。此定义源自于\r\n在循环中使用 <code>select!</code> 的场景。如果没有此保证，\r\n当另一个分支完成时，你将失去进度，\r\n并通过循环重新启动 <code>select!</code>。</p>')),
    (b'<p>Be aware that cancelling something that is not cancellation safe is not\r\nnecessarily wrong. For example, if you are cancelling a task because the\r\napplication is shutting down, then you probably don\xe2\x80\x99t care that partially\r\nread data is lost.</p>',
     E('<p>请注意，取消不可取消安全的操作\r\n并不一定是错误的。例如，如果你因为\r\n应用程序关闭而取消任务，那么你可能不\r\n关心部分读取的数据丢失。</p>')),
    (b'<p>Basic select with two branches.</p>',
     E('<p>具有两个分支的基础 select。</p>')),
    (b'<p>Basic stream selecting.</p>',
     E('<p>基础流选择。</p>')),
    (b'<p>Collect the contents of two streams. In this example, we rely on pattern\r\nmatching and the fact that <code>stream::iter</code> is \xe2\x80\x9cfused\xe2\x80\x9d, i.e. once the stream\r\nis complete, all calls to <code>next()</code> return <code>None</code>.</p>',
     E('<p>收集两个流的内容。在本例中，我们依赖模式\r\n匹配以及 <code>stream::iter</code> 是\xe2\x80\x9c融合（fused）\xe2\x80\x9d的这一事实，\r\n即一旦流完成，对 <code>next()</code> 的所有调用都返回 <code>None</code>。</p>')),
    (b'<p>Using the same future in multiple <code>select!</code> expressions can be done by passing\r\na reference to the future. Doing so requires the future to be <a href="https://doc.rust-lang.org/1.95.0/core/marker/trait.Unpin.html" title="trait core::marker::Unpin"><code>Unpin</code></a>. A\r\nfuture can be made <a href="https://doc.rust-lang.org/1.95.0/core/marker/trait.Unpin.html" title="trait core::marker::Unpin"><code>Unpin</code></a> by either using <a href="https://doc.rust-lang.org/1.95.0/alloc/boxed/struct.Box.html#method.pin" title="associated function alloc::boxed::Box::pin"><code>Box::pin</code></a> or stack pinning.</p>',
     E('<p>在多个 <code>select!</code> 表达式中使用同一个 future 可以通过传递\r\n该 future 的引用来实现。这要求该 future 必须是 <a href="https://doc.rust-lang.org/1.95.0/core/marker/trait.Unpin.html" title="trait core::marker::Unpin"><code>Unpin</code></a> 的。\r\n可以通过使用 <a href="https://doc.rust-lang.org/1.95.0/alloc/boxed/struct.Box.html#method.pin" title="associated function alloc::boxed::Box::pin"><code>Box::pin</code></a> 或栈固定（stack pinning）\r\n将 future 变为 <a href="https://doc.rust-lang.org/1.95.0/core/marker/trait.Unpin.html" title="trait core::marker::Unpin"><code>Unpin</code></a>。</p>')),
    (b'<p>Here, a stream is consumed for at most 1 second.</p>',
     E('<p>在此示例中，一个流最多被消耗 1 秒。</p>')),
    (b'<p>Joining two values using <code>select!</code>.</p>',
     E('<p>使用 <code>select!</code> 连接两个值。</p>')),
    (b'<p>Using the <code>biased;</code> mode to control polling order.</p>',
     E('<p>使用 <code>biased;</code> 模式控制轮询顺序。</p>')),
    (b'<p>Given that <code>if</code> preconditions are used to disable <code>select!</code> branches, some\r\ncaution must be used to avoid missing values.</p>',
     E('<p>由于 <code>if</code> 前置条件用于禁用 <code>select!</code> 分支，\r\n因此必须谨慎使用以避免遗漏值。</p>')),
    (b'<p>For example, here is <strong>incorrect</strong> usage of <code>sleep</code> with <code>if</code>. The objective\r\nis to repeatedly run an asynchronous task for up to 50 milliseconds.\r\nHowever, there is a potential for the <code>sleep</code> completion to be missed.</p>',
     E('<p>例如，下面是 <code>sleep</code> 与 <code>if</code> 的<strong>错误</strong>用法。目标是\r\n重复运行异步任务最多 50 毫秒。\r\n但是，<code>sleep</code> 的完成有被遗漏的可能。</p>')),
    (b'<p>In the above example, <code>sleep.is_elapsed()</code> may return <code>true</code> even if\r\n<code>sleep.poll()</code> never returned <code>Ready</code>. This opens up a potential race\r\ncondition where <code>sleep</code> expires between the <code>while !sleep.is_elapsed()</code>\r\ncheck and the call to <code>select!</code> resulting in the <code>some_async_work()</code> call to\r\nrun uninterrupted despite the sleep having elapsed.</p>',
     E('<p>在上面的示例中，即使 <code>sleep.poll()</code> 始终未返回 <code>Ready</code>，\r\n<code>sleep.is_elapsed()</code> 也可能返回 <code>true</code>。这会造成潜在的竞态条件——\r\n<code>sleep</code> 在 <code>while !sleep.is_elapsed()</code> 检查与\r\n对 <code>select!</code> 的调用之间到期，导致 <code>some_async_work()</code> 调用\r\n在 sleep 已到期的情况下仍不间断地运行。</p>')),
    (b'<p>One way to write the above example without the race would be:</p>',
     E('<p>在不存在竞态条件的情况下编写上述示例的一种方法是：</p>')),
    (b'<p>The <code>select!</code> macro is a powerful tool for managing multiple asynchronous\r\nbranches, enabling tasks to run concurrently within the same thread. However,\r\nits use can introduce challenges, particularly around cancellation safety, which\r\ncan lead to subtle and hard-to-debug errors. For many use cases, ecosystem\r\nalternatives may be preferable as they mitigate these concerns by offering\r\nclearer syntax, more predictable control flow, and reducing the need to manually\r\nhandle issues like fuse semantics or cancellation safety.</p>',
     E('<p><code>select!</code> 宏是管理多个异步分支的强大工具，\r\n使得任务能够在同一线程内并发运行。然而，\r\n其使用也可能带来挑战，特别是关于可取消安全，\r\n这可能导致微妙且难以调试的错误。对于许多用例，\r\n生态系统的替代方案可能更可取，因为它们通过提供\r\n更清晰的语法、更可预测的控制流来缓解这些问题，\r\n并减少手动处理熔断语义或可取消安全等问题的需要。</p>')),
    (b'<p>For cases where <code>loop { select! { ... } }</code> is used to poll multiple tasks,\r\nstream merging offers a concise alternative, inherently handle cancellation-safe\r\nprocessing, removing the risk of data loss. Libraries such as <a href="https://docs.rs/tokio-stream/latest/tokio_stream/"><code>tokio_stream</code></a>,\r\n<a href="https://docs.rs/futures/latest/futures/stream/"><code>futures::stream</code></a> and <a href="https://docs.rs/futures-concurrency/latest/futures_concurrency/"><code>futures_concurrency</code></a> provide tools for merging\r\nstreams and handling their outputs sequentially.</p>',
     E('<p>对于使用 <code>loop { select! { ... } }</code> 来轮询多个任务的情况，\r\n流合并提供了一种简洁的替代方案，天生支持可取消安全的\r\n处理，消除了数据丢失的风险。诸如 <a href="https://docs.rs/tokio-stream/latest/tokio_stream/"><code>tokio_stream</code></a>、\r\n<a href="https://docs.rs/futures/latest/futures/stream/"><code>futures::stream</code></a> 和 <a href="https://docs.rs/futures-concurrency/latest/futures_concurrency/"><code>futures_concurrency</code></a> 等库提供了用于合并\r\n流并按顺序处理其输出的工具。</p>')),
    (b'<p>By using merge, you can unify multiple asynchronous tasks into a single stream,\r\neliminating the need to manage tasks manually and reducing the risk of\r\nunintended behavior like data loss.</p>',
     E('<p>通过使用 merge，可以将多个异步任务统一到单个流中，\r\n无需手动管理任务，并降低意外行为（如数据丢失）的风险。</p>')),
    (b'<p>If you need to wait for the first completion among several asynchronous tasks,\r\necosystem utilities such as\r\n<a href="https://docs.rs/futures/latest/futures/"><code>futures</code></a>,\r\n<a href="https://docs.rs/futures-lite/latest/futures_lite/"><code>futures-lite</code></a> or\r\n<a href="https://docs.rs/futures-concurrency/latest/futures_concurrency/"><code>futures-concurrency</code></a>\r\nprovide streamlined syntax for racing futures:</p>',
     E('<p>如果你需要等待几个异步任务中的第一个完成，\r\n可以使用以下生态系统实用工具：\r\n<a href="https://docs.rs/futures/latest/futures/"><code>futures</code></a>、\r\n<a href="https://docs.rs/futures-lite/latest/futures_lite/"><code>futures-lite</code></a> 或\r\n<a href="https://docs.rs/futures-concurrency/latest/futures_concurrency/"><code>futures-concurrency</code></a>，\r\n它们提供了用于 race future 的简洁语法：</p>')),
])


# ============================================================
# attr.main.html
# ============================================================
add('attr.main.html', [
    (b'<p>The <code>worker_threads</code> option configures the number of worker threads, and\r\ndefaults to the number of cpus on the system. This is the default flavor.</p>',
     E('<p><code>worker_threads</code> 选项配置工作线程的数量，\r\n默认为系统上的 CPU 数量。这是默认的 flavor。</p>')),
    (b'<p>To use the <a href="../tokio/runtime/struct.LocalRuntime.html">local runtime</a>, the macro can be configured using</p>',
     E('<p>要使用 <a href="../tokio/runtime/struct.LocalRuntime.html">local runtime</a>，可以按以下方式配置宏</p>')),
    (b'<p>Arguments are allowed for any functions, aside from <code>main</code> which is special.</p>',
     E('<p>除 <code>main</code> 是特殊的之外，任何函数都允许使用参数。</p>')),
    (b'<p>Equivalent code not using <code>#[tokio::main]</code></p>',
     E('<p>不使用 <code>#[tokio::main]</code> 的等价代码</p>')),
    (b'<p>The basic scheduler is single-threaded.</p>',
     E('<p>基础调度器是单线程的。</p>')),
    (b'<p>The <a href="../tokio/runtime/struct.LocalRuntime.html">local runtime</a> is similar to the current-thread runtime but\r\nsupports <a href="../tokio/task/fn.spawn_local.html"><code>task::spawn_local</code></a>.</p>',
     E('<p><a href="../tokio/runtime/struct.LocalRuntime.html">local runtime</a> 与 current-thread runtime 类似，但\r\n支持 <a href="../tokio/task/fn.spawn_local.html"><code>task::spawn_local</code></a>。</p>')),
    (b'<p>Note that <code>start_paused</code> requires the <code>test-util</code> feature to be enabled.</p>',
     E('<p>请注意，<code>start_paused</code> 需要启用 <code>test-util</code> feature。</p>')),
    (b'<p>Available options are <code>shutdown_runtime</code> and <code>ignore</code>. For more details, see\r\n<a href="../tokio/runtime/struct.Builder.html#method.unhandled_panic"><code>Builder::unhandled_panic</code></a>.</p>',
     E('<p>可用选项为 <code>shutdown_runtime</code> 和 <code>ignore</code>。有关更多详细信息，请参阅\r\n<a href="../tokio/runtime/struct.Builder.html#method.unhandled_panic"><code>Builder::unhandled_panic</code></a>。</p>')),
    (b'<p><strong>Note</strong>: This option depends on Tokio\xe2\x80\x99s <a href="../tokio/index.html#unstable-features">unstable API</a>. See <a href="../tokio/index.html#unstable-features">the\r\ndocumentation on unstable features</a> for details on how to enable\r\nTokio\xe2\x80\x99s unstable features.</p>',
     E('<p><strong>注意</strong>：此选项依赖于 Tokio 的<a href="../tokio/index.html#unstable-features">不稳定 API</a>。有关如何启用\r\nTokio 不稳定 feature 的详细信息，请参阅<a href="../tokio/index.html#unstable-features">关于不稳定 feature 的文档</a>。</p>')),
])


# ============================================================
# attr.test.html
# ============================================================
add('attr.test.html', [
    (b'<p>The <code>worker_threads</code> option configures the number of worker threads, and\r\ndefaults to the number of cpus on the system.</p>',
     E('<p><code>worker_threads</code> 选项配置工作线程的数量，\r\n默认为系统上的 CPU 数量。</p>')),
    (b'<p>The default test runtime is single-threaded. Each test gets a\r\nseparate current-thread runtime.</p>',
     E('<p>默认的测试运行时是单线程的。每个测试\r\n都获得单独的 current-thread runtime。</p>')),
    (b'<p>Equivalent code not using <code>#[tokio::test]</code></p>',
     E('<p>不使用 <code>#[tokio::test]</code> 的等价代码</p>')),
    (b'<p>Note that <code>start_paused</code> requires the <code>test-util</code> feature to be enabled.</p>',
     E('<p>请注意，<code>start_paused</code> 需要启用 <code>test-util</code> feature。</p>')),
    (b'<p>Available options are <code>shutdown_runtime</code> and <code>ignore</code>. For more details, see\r\n<a href="../tokio/runtime/struct.Builder.html#method.unhandled_panic"><code>Builder::unhandled_panic</code></a>.</p>',
     E('<p>可用选项为 <code>shutdown_runtime</code> 和 <code>ignore</code>。有关更多详细信息，请参阅\r\n<a href="../tokio/runtime/struct.Builder.html#method.unhandled_panic"><code>Builder::unhandled_panic</code></a>。</p>')),
    (b'<p><strong>Note</strong>: This option depends on Tokio\xe2\x80\x99s <a href="../tokio/index.html#unstable-features">unstable API</a>. See <a href="../tokio/index.html#unstable-features">the\r\ndocumentation on unstable features</a> for details on how to enable\r\nTokio\xe2\x80\x99s unstable features.</p>',
     E('<p><strong>注意</strong>：此选项依赖于 Tokio 的<a href="../tokio/index.html#unstable-features">不稳定 API</a>。有关如何启用\r\nTokio 不稳定 feature 的详细信息，请参阅<a href="../tokio/index.html#unstable-features">关于不稳定 feature 的文档</a>。</p>')),
])


# ============================================================
# fs/fn.canonicalize.html
# ============================================================
add('fs/fn.canonicalize.html', [
    (b'<p>This function currently corresponds to the <code>realpath</code> function on Unix\r\nand the <code>CreateFile</code> and <code>GetFinalPathNameByHandle</code> functions on Windows.\r\nNote that, this <a href="https://doc.rust-lang.org/std/io/index.html#platform-specific-behavior">may change in the future</a>.</p>',
     E('<p>此函数当前对应于 Unix 上的 <code>realpath</code> 函数，\r\n以及 Windows 上的 <code>CreateFile</code> 和 <code>GetFinalPathNameByHandle</code> 函数。\r\n请注意，<a href="https://doc.rust-lang.org/std/io/index.html#platform-specific-behavior">未来可能会发生变化</a>。</p>')),
    (b'<p>On Windows, this converts the path to use <a href="https://msdn.microsoft.com/en-us/library/windows/desktop/aa365247(v=vs.85).aspx#maxpath">extended length path</a>\r\nsyntax, which allows your program to use longer path names, but means you\r\ncan only join backslash-delimited paths to it, and it may be incompatible\r\nwith other applications (if passed to the application on the command-line,\r\nor written to a file another application may read).</p>',
     E('<p>在 Windows 上，这会将路径转换为使用<a href="https://msdn.microsoft.com/en-us/library/windows/desktop/aa365247(v=vs.85).aspx#maxpath">扩展长度路径</a>\r\n语法，这允许你的程序使用更长的路径名，但这意味着你\r\n只能将反斜杠分隔的路径连接到它，并且它可能与\r\n其他应用程序不兼容（如果通过命令行传递给应用程序，\r\n或者写入其他应用程序可能读取的文件中）。</p>')),
    (b'<p>This function will return an error in the following situations, but is not\r\nlimited to just these cases:</p>',
     E('<p>此函数将在以下情况下返回错误，但不限于\r\n这些情况：</p>')),
])


# ============================================================
# fs/fn.copy.html
# ============================================================
add('fs/fn.copy.html', [
    (b'<p>Copies the contents of one file to another. This function will also copy the permission bits\r\nof the original file to the destination file.\r\nThis function will overwrite the contents of to.</p>',
     E('<p>将一个文件的内容复制到另一个文件。此函数还会将原始文件的权限位\r\n复制到目标文件。\r\n此函数将覆盖 to 的内容。</p>')),
])


# ============================================================
# fs/fn.create_dir.html
# ============================================================
add('fs/fn.create_dir.html', [
    (b'<p>This function currently corresponds to the <code>mkdir</code> function on Unix\r\nand the <code>CreateDirectory</code> function on Windows.\r\nNote that, this <a href="https://doc.rust-lang.org/std/io/index.html#platform-specific-behavior">may change in the future</a>.</p>',
     E('<p>此函数当前对应于 Unix 上的 <code>mkdir</code> 函数，\r\n以及 Windows 上的 <code>CreateDirectory</code> 函数。\r\n请注意，<a href="https://doc.rust-lang.org/std/io/index.html#platform-specific-behavior">未来可能会发生变化</a>。</p>')),
    (b'<p><strong>NOTE</strong>: If a parent of the given path doesn\xe2\x80\x99t exist, this function will\r\nreturn an error. To create a directory and all its missing parents at the\r\nsame time, use the <a href="fn.create_dir_all.html" title="fn tokio::fs::create_dir_all"><code>create_dir_all</code></a> function.</p>',
     E('<p><strong>注意</strong>：如果给定路径的父目录不存在，此函数将\r\n返回错误。要同时创建目录及其所有缺失的父目录，\r\n请使用 <a href="fn.create_dir_all.html" title="fn tokio::fs::create_dir_all"><code>create_dir_all</code></a> 函数。</p>')),
    (b'<p>This function will return an error in the following situations, but is not\r\nlimited to just these cases:</p>',
     E('<p>此函数将在以下情况下返回错误，但不限于\r\n这些情况：</p>')),
])


# ============================================================
# fs/fn.create_dir_all.html
# ============================================================
add('fs/fn.create_dir_all.html', [
    (b'<p>Recursively creates a directory and all of its parent components if they\r\nare missing.</p>',
     E('<p>递归地创建一个目录及其所有父组件（如果它们\r\n缺失）。</p>')),
    (b'<p>This function currently corresponds to the <code>mkdir</code> function on Unix\r\nand the <code>CreateDirectory</code> function on Windows.\r\nNote that, this <a href="https://doc.rust-lang.org/std/io/index.html#platform-specific-behavior">may change in the future</a>.</p>',
     E('<p>此函数当前对应于 Unix 上的 <code>mkdir</code> 函数，\r\n以及 Windows 上的 <code>CreateDirectory</code> 函数。\r\n请注意，<a href="https://doc.rust-lang.org/std/io/index.html#platform-specific-behavior">未来可能会发生变化</a>。</p>')),
    (b'<p>This function will return an error in the following situations, but is not\r\nlimited to just these cases:</p>',
     E('<p>此函数将在以下情况下返回错误，但不限于\r\n这些情况：</p>')),
    (b'<p>Notable exception is made for situations where any of the directories\r\nspecified in the <code>path</code> could not be created as it was being created concurrently.\r\nSuch cases are considered to be successful. That is, calling <code>create_dir_all</code>\r\nconcurrently from multiple threads or processes is guaranteed not to fail\r\ndue to a race condition with itself.</p>',
     E('<p>对于 <code>path</code> 中指定的任何目录因同时创建而无法创建的情况，\r\n会做出值得注意的例外处理。\r\n此类情况被视为成功。也就是说，从多个线程或进程\r\n并发调用 <code>create_dir_all</code> 保证不会因自身的竞态条件\r\n而失败。</p>')),
])


# ============================================================
# fs/fn.read.html
# ============================================================
add('fs/fn.read.html', [
    (b'<p>Reads the entire contents of a file into a bytes vector.</p>',
     E('<p>将文件的全部内容读取到字节向量中。</p>')),
    (b'<p>This is a convenience function for using <a href="struct.File.html#method.open" title="associated function tokio::fs::File::open"><code>File::open</code></a> and <a href="../io/trait.AsyncReadExt.html#method.read_to_end" title="method tokio::io::AsyncReadExt::read_to_end"><code>read_to_end</code></a>\r\nwith fewer imports and without an intermediate variable. It pre-allocates a\r\nbuffer based on the file size when available, so it is generally faster than\r\nreading into a vector created with <code>Vec::new()</code>.</p>',
     E('<p>这是一个便捷函数，用于结合使用 <a href="struct.File.html#method.open" title="associated function tokio::fs::File::open"><code>File::open</code></a> 和 <a href="../io/trait.AsyncReadExt.html#method.read_to_end" title="method tokio::io::AsyncReadExt::read_to_end"><code>read_to_end</code></a>，\r\n使用更少的导入且无需中间变量。如果可用，它会\r\n根据文件大小预分配缓冲区，因此通常比\r\n读取到使用 <code>Vec::new()</code> 创建的向量中更快。</p>')),
    (b'<p>This operation is implemented by running the equivalent blocking operation\r\non a separate thread pool using <a href="../task/fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a>.</p>',
     E('<p>此操作通过使用 <a href="../task/fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a> 在\r\n单独的线程池上运行等效的阻塞操作来实现。</p>')),
    (b'<p>This function will return an error if <code>path</code> does not already exist.\r\nOther errors may also be returned according to <a href="struct.OpenOptions.html#method.open" title="method tokio::fs::OpenOptions::open"><code>OpenOptions::open</code></a>.</p>',
     E('<p>如果 <code>path</code> 不存在，此函数将返回错误。\r\n根据 <a href="struct.OpenOptions.html#method.open" title="method tokio::fs::OpenOptions::open"><code>OpenOptions::open</code></a>，也可能会返回其他错误。</p>')),
    (b'<p>It will also return an error if it encounters while reading an error\r\nof a kind other than <a href="https://doc.rust-lang.org/1.95.0/std/io/error/enum.ErrorKind.html#variant.Interrupted" title="variant std::io::error::ErrorKind::Interrupted"><code>ErrorKind::Interrupted</code></a>.</p>',
     E('<p>如果在读取时遇到除 <a href="https://doc.rust-lang.org/1.95.0/std/io/error/enum.ErrorKind.html#variant.Interrupted" title="variant std::io::error::ErrorKind::Interrupted"><code>ErrorKind::Interrupted</code></a>\r\n以外的错误，它也会返回错误。</p>')),
    (b'<p>On Linux, you can also use io_uring for executing system calls. To enable\r\nio_uring, you need to specify the <code>--cfg tokio_unstable</code> flag at compile time,\r\nenable the io-uring cargo feature, and set the <code>Builder::enable_io_uring</code>\r\nruntime option.</p>',
     E('<p>在 Linux 上，你还可以使用 io_uring 来执行系统调用。要启用\r\nio_uring，需要在编译时指定 <code>--cfg tokio_unstable</code> 标志，\r\n启用 io-uring cargo feature，并设置 <code>Builder::enable_io_uring</code>\r\n运行时选项。</p>')),
    (b'<p>Support for io_uring is currently experimental, so its behavior may change\r\nor it may be removed in future versions.</p>',
     E('<p>目前对 io_uring 的支持是实验性的，因此其行为可能\r\n发生变化或在未来版本中被移除。</p>')),
])


# ============================================================
# fs/fn.metadata.html
# ============================================================
add('fs/fn.metadata.html', [
    (b'<p>Given a path, queries the file system to get information about a file,\r\ndirectory, etc.</p>',
     E('<p>给定路径，查询文件系统以获取有关文件、\r\n目录等的信息。</p>')),
    (b'<p>This function will traverse symbolic links to query information about the\r\ndestination file.</p>',
     E('<p>此函数会遍历符号链接以查询有关\r\n目标文件的信息。</p>')),
    (b'<p>This function currently corresponds to the <code>stat</code> function on Unix and the\r\n<code>GetFileAttributesEx</code> function on Windows.  Note that, this <a href="https://doc.rust-lang.org/std/io/index.html#platform-specific-behavior">may change in\r\nthe future</a>.</p>',
     E('<p>此函数当前对应于 Unix 上的 <code>stat</code> 函数以及\r\nWindows 上的 <code>GetFileAttributesEx</code> 函数。请注意，<a href="https://doc.rust-lang.org/std/io/index.html#platform-specific-behavior">未来\r\n可能会发生变化</a>。</p>')),
    (b'<p>This function will return an error in the following situations, but is not\r\nlimited to just these cases:</p>',
     E('<p>此函数将在以下情况下返回错误，但不限于\r\n这些情况：</p>')),
])


# ============================================================
# fs/fn.read_to_string.html
# ============================================================
add('fs/fn.read_to_string.html', [
    (b'<p>Creates a future which will open a file for reading and read the entire\r\ncontents into a string and return said string.</p>',
     E('<p>创建一个 future，它将打开一个文件进行读取，\r\n并将全部内容读取到一个字符串中，然后返回该字符串。</p>')),
    (b'<p>This is the async equivalent of <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.read_to_string.html" title="fn std::fs::read_to_string"><code>std::fs::read_to_string</code></a>.</p>',
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.read_to_string.html" title="fn std::fs::read_to_string"><code>std::fs::read_to_string</code></a> 的异步等价方法。</p>')),
    (b'<p>This operation is implemented by running the equivalent blocking operation\r\non a separate thread pool using <a href="../task/fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a>.</p>',
     E('<p>此操作通过使用 <a href="../task/fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a> 在\r\n单独的线程池上运行等效的阻塞操作来实现。</p>')),
])


# ============================================================
# fs/fn.hard_link.html
# ============================================================
add('fs/fn.hard_link.html', [
    (b'<p>The <code>link</code> path will be a link pointing to the <code>original</code> path. Note that systems\r\noften require these two paths to both be located on the same filesystem.</p>',
     E('<p><code>link</code> 路径将是指向 <code>original</code> 路径的链接。\r\n请注意，系统通常要求这两个路径都位于同一文件系统上。</p>')),
    (b'<p>This function currently corresponds to the <code>link</code> function on Unix\r\nand the <code>CreateHardLink</code> function on Windows.\r\nNote that, this <a href="https://doc.rust-lang.org/std/io/index.html#platform-specific-behavior">may change in the future</a>.</p>',
     E('<p>此函数当前对应于 Unix 上的 <code>link</code> 函数，\r\n以及 Windows 上的 <code>CreateHardLink</code> 函数。\r\n请注意，<a href="https://doc.rust-lang.org/std/io/index.html#platform-specific-behavior">未来可能会发生变化</a>。</p>')),
    (b'<p>This function will return an error in the following situations, but is not\r\nlimited to just these cases:</p>',
     E('<p>此函数将在以下情况下返回错误，但不限于\r\n这些情况：</p>')),
])


# ============================================================
# fs/fn.read_dir.html
# ============================================================
add('fs/fn.read_dir.html', [
    (b'<p>Returns a stream over the entries within a directory.</p>',
     E('<p>返回一个目录中条目的流。</p>')),
    (b'<p>This operation is implemented by running the equivalent blocking\r\noperation on a separate thread pool using <a href="../task/fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a>.</p>',
     E('<p>此操作通过使用 <a href="../task/fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a> 在\r\n单独的线程池上运行等效的阻塞操作来实现。</p>')),
])


# ============================================================
# fs/fn.read_link.html
# ============================================================
add('fs/fn.read_link.html', [
    (b'<p>This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.read_link.html" title="fn std::fs::read_link"><code>std::fs::read_link</code></a>.</p>',
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.read_link.html" title="fn std::fs::read_link"><code>std::fs::read_link</code></a> 的异步版本。</p>')),
])


# ============================================================
# fs/fn.try_exists.html
# ============================================================
add('fs/fn.try_exists.html', [
    (b'<p>Returns <code>Ok(true)</code> if the path points at an existing entity.</p>',
     E('<p>如果路径指向已存在的实体，则返回 <code>Ok(true)</code>。</p>')),
    (b'<p>This function will traverse symbolic links to query information about the\r\ndestination file. In case of broken symbolic links this will return <code>Ok(false)</code>.</p>',
     E('<p>此函数会遍历符号链接以查询有关\r\n目标文件的信息。对于损坏的符号链接，将返回 <code>Ok(false)</code>。</p>')),
    (b'<p>This is the async equivalent of <a href="https://doc.rust-lang.org/1.95.0/std/path/struct.Path.html#method.try_exists" title="method std::path::Path::try_exists"><code>std::path::Path::try_exists</code></a>.</p>',
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/path/struct.Path.html#method.try_exists" title="method std::path::Path::try_exists"><code>std::path::Path::try_exists</code></a> 的异步等价方法。</p>')),
])


# ============================================================
# fs/fn.symlink_file.html
# ============================================================
add('fs/fn.symlink_file.html', [
    (b'<p>Creates a new file symbolic link on the filesystem.</p>',
     E('<p>在文件系统上创建一个新的文件符号链接。</p>')),
    (b'<p>The <code>link</code> path will be a file symbolic link pointing to the <code>original</code>\r\npath.</p>',
     E('<p><code>link</code> 路径将是指向 <code>original</code> 路径的\r\n文件符号链接。</p>')),
    (b'<p>This is an async version of <a href="https://doc.rust-lang.org/std/os/windows/fs/fn.symlink_file.html"><code>std::os::windows::fs::symlink_file</code></a>',
     E('<p>这是 <a href="https://doc.rust-lang.org/std/os/windows/fs/fn.symlink_file.html"><code>std::os::windows::fs::symlink_file</code></a> 的异步版本')),
])


# ============================================================
# fs/fn.symlink_dir.html
# ============================================================
add('fs/fn.symlink_dir.html', [
    (b'<p>Creates a new directory symlink on the filesystem.</p>',
     E('<p>在文件系统上创建一个新的目录符号链接。</p>')),
    (b'<p>The <code>link</code> path will be a directory symbolic link pointing to the <code>original</code>\r\npath.</p>',
     E('<p><code>link</code> 路径将是指向 <code>original</code> 路径的\r\n目录符号链接。</p>')),
    (b'<p>This is an async version of <a href="https://doc.rust-lang.org/std/os/windows/fs/fn.symlink_dir.html"><code>std::os::windows::fs::symlink_dir</code></a>',
     E('<p>这是 <a href="https://doc.rust-lang.org/std/os/windows/fs/fn.symlink_dir.html"><code>std::os::windows::fs::symlink_dir</code></a> 的异步版本')),
])


# ============================================================
# fs/fn.symlink_metadata.html
# ============================================================
add('fs/fn.symlink_metadata.html', [
    (b'<p>Queries the file system metadata for a path.</p>',
     E('<p>查询路径的文件系统元数据。</p>')),
    (b'<p>This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.symlink_metadata.html" title="fn std::fs::symlink_metadata"><code>std::fs::symlink_metadata</code></a>',
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.symlink_metadata.html" title="fn std::fs::symlink_metadata"><code>std::fs::symlink_metadata</code></a> 的异步版本')),
])


# ============================================================
# fs/fn.set_permissions.html
# ============================================================
add('fs/fn.set_permissions.html', [
    (b'<p>Changes the permissions found on a file or a directory.</p>',
     E('<p>更改文件或目录的权限。</p>')),
    (b'<p>This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.set_permissions.html" title="fn std::fs::set_permissions"><code>std::fs::set_permissions</code></a>',
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.set_permissions.html" title="fn std::fs::set_permissions"><code>std::fs::set_permissions</code></a> 的异步版本')),
])


# ============================================================
# fs/fn.rename.html
# ============================================================
add('fs/fn.rename.html', [
    (b'<p>Renames a file or directory to a new name, replacing the original file if\r\n<code>to</code> already exists.</p>',
     E('<p>将文件或目录重命名为新名称，如果\r\n<code>to</code> 已存在则替换原始文件。</p>')),
    (b'<p>This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.rename.html" title="fn std::fs::rename"><code>std::fs::rename</code></a>.</p>',
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.rename.html" title="fn std::fs::rename"><code>std::fs::rename</code></a> 的异步版本。</p>')),
])


# ============================================================
# fs/fn.remove_file.html
# ============================================================
add('fs/fn.remove_file.html', [
    (b'<p>Note that there is no guarantee that the file is immediately deleted (e.g.\r\ndepending on platform, other open file descriptors may prevent immediate\r\nremoval).</p>',
     E('<p>请注意，无法保证文件会被立即删除（例如，\r\n取决于平台，其他打开的文件描述符可能会阻止立即\r\n删除）。</p>')),
    (b'<p>This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.remove_file.html" title="fn std::fs::remove_file"><code>std::fs::remove_file</code></a>.</p>',
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.remove_file.html" title="fn std::fs::remove_file"><code>std::fs::remove_file</code></a> 的异步版本。</p>')),
])


# ============================================================
# fs/fn.remove_dir.html
# ============================================================
add('fs/fn.remove_dir.html', [
    (b'<p>Removes an existing, empty directory.</p>',
     E('<p>删除一个已存在的空目录。</p>')),
    (b'<p>This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.remove_dir.html" title="fn std::fs::remove_dir"><code>std::fs::remove_dir</code></a>.</p>',
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.remove_dir.html" title="fn std::fs::remove_dir"><code>std::fs::remove_dir</code></a> 的异步版本。</p>')),
])


# ============================================================
# fs/fn.remove_dir_all.html
# ============================================================
add('fs/fn.remove_dir_all.html', [
    (b'<p>This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.remove_dir_all.html" title="fn std::fs::remove_dir_all"><code>std::fs::remove_dir_all</code></a>',
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.remove_dir_all.html" title="fn std::fs::remove_dir_all"><code>std::fs::remove_dir_all</code></a> 的异步版本')),
])


# ============================================================
# fs/fn.write.html
# ============================================================
add('fs/fn.write.html', [
    (b'<p>Creates a future that will open a file for writing and write the entire\r\ncontents of <code>contents</code> to it.</p>',
     E('<p>创建一个 future，它将打开一个文件用于写入，并将\r\n<code>contents</code> 的全部内容写入其中。</p>')),
    (b'<p>This is the async equivalent of <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.write.html" title="fn std::fs::write"><code>std::fs::write</code></a>.</p>',
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/fn.write.html" title="fn std::fs::write"><code>std::fs::write</code></a> 的异步等价方法。</p>')),
    (b'<p>This operation is implemented by running the equivalent blocking operation\r\non a separate thread pool using <a href="../task/fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a>.</p>',
     E('<p>此操作通过使用 <a href="../task/fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a> 在\r\n单独的线程池上运行等效的阻塞操作来实现。</p>')),
])


# ============================================================
# fs/struct.DirBuilder.html
# ============================================================
add('fs/struct.DirBuilder.html', [
    (b'<p>A builder for creating directories in various manners.</p>',
     E('<p>用于以各种方式创建目录的构建器。</p>')),
    (b'<p>This is a specialized version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.DirBuilder.html" title="struct std::fs::DirBuilder"><code>std::fs::DirBuilder</code></a> for usage on\r\nthe Tokio runtime.</p>',
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.DirBuilder.html" title="struct std::fs::DirBuilder"><code>std::fs::DirBuilder</code></a> 的特化版本，用于\r\nTokio 运行时。</p>')),
    (b'<p>This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.DirBuilder.html#method.new" title="associated function std::fs::DirBuilder::new"><code>std::fs::DirBuilder::new</code></a>.</p>',
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.DirBuilder.html#method.new" title="associated function std::fs::DirBuilder::new"><code>std::fs::DirBuilder::new</code></a> 的异步版本。</p>')),
    (b'<p>This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.DirBuilder.html#method.recursive" title="method std::fs::DirBuilder::recursive"><code>std::fs::DirBuilder::recursive</code></a>.</p>',
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.DirBuilder.html#method.recursive" title="method std::fs::DirBuilder::recursive"><code>std::fs::DirBuilder::recursive</code></a> 的异步版本。</p>')),
    (b'<p>This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.DirBuilder.html#method.create" title="method std::fs::DirBuilder::create"><code>std::fs::DirBuilder::create</code></a>.</p>',
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.DirBuilder.html#method.create" title="method std::fs::DirBuilder::create"><code>std::fs::DirBuilder::create</code></a> 的异步版本。</p>')),
])


# ============================================================
# fs/struct.DirEntry.html
# ============================================================
add('fs/struct.DirEntry.html', [
    (b'<p>Entries returned by the <a href="struct.ReadDir.html" title="struct tokio::fs::ReadDir"><code>ReadDir</code></a> stream.</p>',
     E('<p>由 <a href="struct.ReadDir.html" title="struct tokio::fs::ReadDir"><code>ReadDir</code></a> 流返回的条目。</p>')),
    (b'<p>This is a specialized version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.DirEntry.html" title="struct std::fs::DirEntry"><code>std::fs::DirEntry</code></a> for usage from the\r\nTokio runtime.</p>',
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.DirEntry.html" title="struct std::fs::DirEntry"><code>std::fs::DirEntry</code></a> 的特化版本，用于\r\nTokio 运行时。</p>')),
    (b'<p>An instance of <code>DirEntry</code> represents an entry inside of a directory on the\r\nfilesystem. Each entry can be inspected via methods to learn about the full\r\npath or possibly other metadata through per-platform extension traits.</p>',
     E('<p><code>DirEntry</code> 的实例表示文件系统上某个目录中的条目。\r\n每个条目都可以通过方法检查，以了解完整\r\n路径或可能的其他元数据（通过各平台的扩展 trait）。</p>')),
    (b'<p>The exact text, of course, depends on what files you have in <code>.</code>.</p>',
     E('<p>当然，确切的文本取决于 <code>.</code> 中有哪些文件。</p>')),
])


# ============================================================
# fs/index.html
# ============================================================
add('fs/index.html', [
    (b'<p>Asynchronous file utilities.</p>',
     E('<p>异步文件实用工具。</p>')),
    (b'<p>This module contains utility methods for working with the file system\r\nasynchronously. This includes reading/writing to files, and working with\r\ndirectories.</p>',
     E('<p>此模块包含用于异步\r\n处理文件系统的实用方法。这包括对文件的读/写以及\r\n对目录的操作。</p>')),
    (b'<p>Be aware that most operating systems do not provide asynchronous file system\r\nAPIs. Because of that, Tokio will use ordinary blocking file operations\r\nbehind the scenes. This is done using the <a href="../task/fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a> threadpool to\r\nrun them in the background.</p>',
     E('<p>请注意，大多数操作系统不提供异步文件系统\r\nAPI。因此，Tokio 在后台将使用普通的阻塞文件操作。\r\n这是通过使用 <a href="../task/fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a> 线程池在\r\n后台运行它们来实现的。</p>')),
    (b'<p>The <code>tokio::fs</code> module should only be used for ordinary files. Trying to use\r\nit with e.g., a named pipe on Linux can result in surprising behavior,\r\nsuch as hangs during runtime shutdown. For special files, you should use a\r\ndedicated type such as <a href="crate::net::unix::pipe"><code>tokio::net::unix::pipe</code></a> or <a href="crate::io::unix::AsyncFd"><code>AsyncFd</code></a> instead.</p>',
     E('<p><code>tokio::fs</code> 模块只应用于普通文件。尝试将其用于\r\nLinux 上的命名管道等特殊文件可能会导致意外行为，\r\n例如在运行时关闭期间挂起。对于特殊文件，\r\n应使用专门的类型，例如 <a href="crate::net::unix::pipe"><code>tokio::net::unix::pipe</code></a> 或 <a href="crate::io::unix::AsyncFd"><code>AsyncFd</code></a>。</p>')),
    (b'<p>Currently, Tokio will always use <a href="../task/fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a> on all platforms, but it\r\nmay be changed to use asynchronous file system APIs such as io_uring in the\r\nfuture.</p>',
     E('<p>目前，Tokio 始终在所有平台上使用 <a href="../task/fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a>，\r\n但未来可能会更改以使用异步文件系统 API（如 io_uring）。</p>')),
    (b'<p>The easiest way to use this module is to use the utility functions that\r\noperate on entire files:</p>',
     E('<p>使用此模块的最简单方法是使用对整个文件进行操作的实用函数：</p>')),
    (b'<p>The two <code>read</code> functions reads the entire file and returns its contents.\r\nThe <code>write</code> function takes the contents of the file and writes those\r\ncontents to the file. It overwrites the existing file, if any.</p>',
     E('<p>两个 <code>read</code> 函数读取整个文件并返回其内容。\r\n<code>write</code> 函数接受文件内容并将这些\r\n内容写入文件。如果存在现有文件，则会覆盖它。</p>')),
    (b'<p>For example, to read the file:</p>',
     E('<p>例如，要读取文件：</p>')),
    (b'<p>To overwrite the file:</p>',
     E('<p>要覆盖文件：</p>')),
    (b'<p>The main type for interacting with files is <a href="struct.File.html" title="struct tokio::fs::File"><code>File</code></a>. It can be used to read\r\nfrom and write to a given file. This is done using the <a href="../io/trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> and\r\n<a href="../io/trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> traits. This type is generally used when you want to do\r\nsomething more complex than just reading or writing the entire contents in\r\none go.</p>',
     E('<p>与文件交互的主要类型是 <a href="struct.File.html" title="struct tokio::fs::File"><code>File</code></a>。它可用于对\r\n给定的文件进行读取和写入。这是通过 <a href="../io/trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a>\r\n和 <a href="../io/trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> trait 完成的。\r\n当你希望执行比一次性读取或写入整个内容更复杂的操作时，\r\n通常会使用此类型。</p>')),
    (b'<p><strong>Note:</strong> It is important to use <a href="../io/trait.AsyncWriteExt.html#method.flush" title="method tokio::io::AsyncWriteExt::flush"><code>flush</code></a> when writing to a Tokio\r\n<a href="struct.File.html" title="struct tokio::fs::File"><code>File</code></a>. This is because calls to <code>write</code> will return before the write has\r\nfinished, and <a href="../io/trait.AsyncWriteExt.html#method.flush" title="method tokio::io::AsyncWriteExt::flush"><code>flush</code></a> will wait for the write to finish. (The write will\r\nhappen even if you don\xe2\x80\x99t flush; it will just happen later.) This is\r\ndifferent from <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.File.html" title="struct std::fs::File"><code>std::fs::File</code></a>, and is due to the fact that <code>File</code> uses\r\n<code>spawn_blocking</code> behind the scenes.</p>',
     E('<p><strong>注意：</strong>在写入 Tokio\r\n<a href="struct.File.html" title="struct tokio::fs::File"><code>File</code></a> 时使用 <a href="../io/trait.AsyncWriteExt.html#method.flush" title="method tokio::io::AsyncWriteExt::flush"><code>flush</code></a> 很重要。\r\n这是因为对 <code>write</code> 的调用将在写入完成之前返回，\r\n而 <a href="../io/trait.AsyncWriteExt.html#method.flush" title="method tokio::io::AsyncWriteExt::flush"><code>flush</code></a> 将等待写入完成。\r\n（即使你不调用 flush，写入也会发生；只是稍后发生。）\r\n这与 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.File.html" title="struct std::fs::File"><code>std::fs::File</code></a> 不同，原因是 <code>File</code> 在\r\n后台使用了 <code>spawn_blocking</code>。</p>')),
    (b'<p>For example, to count the number of lines in a file without loading the\r\nentire file into memory:</p>',
     E('<p>例如，要计算文件中的行数而不将整个文件加载到内存中：</p>')),
    (b'<p>For example, to write a file line-by-line:</p>',
     E('<p>例如，要逐行写入文件：</p>')),
    (b'<p>Tokio\xe2\x80\x99s file uses <a href="../task/fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a> behind the scenes, and this has serious\r\nperformance consequences. To get good performance with file IO on Tokio, it\r\nis recommended to batch your operations into as few <code>spawn_blocking</code> calls\r\nas possible.</p>',
     E('<p>Tokio 的文件操作在后台使用 <a href="../task/fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a>，\r\n这会带来严重的性能影响。为了在 Tokio 上获得良好的文件 IO 性能，\r\n建议将你的操作批处理为尽可能少的 <code>spawn_blocking</code> 调用。</p>')),
    (b'<p>One example of this difference can be seen by comparing the two reading\r\nexamples above. The first example uses <a href="fn.read.html" title="fn tokio::fs::read"><code>tokio::fs::read</code></a>, which reads the\r\nentire file in a single <code>spawn_blocking</code> call, and then returns it. The\r\nsecond example will read the file in chunks using many <code>spawn_blocking</code>\r\ncalls. This means that the second example will most likely be more expensive\r\nfor large files. (Of course, using chunks may be necessary for very large\r\nfiles that don\xe2\x80\x99t fit in memory.)</p>',
     E('<p>通过比较上面的两个读取示例，可以看到这种差异的一个例子。\r\n第一个示例使用 <a href="fn.read.html" title="fn tokio::fs::read"><code>tokio::fs::read</code></a>，\r\n它在单个 <code>spawn_blocking</code> 调用中读取\r\n整个文件，然后返回它。第二个示例将使用许多 <code>spawn_blocking</code>\r\n调用以块的形式读取文件。这意味着对于大文件，\r\n第二个示例很可能更昂贵。\r\n（当然，对于无法放入内存的超大文件，使用分块读取可能是必要的。）</p>')),
    (b'<p>The following examples will show some strategies for this:</p>',
     E('<p>以下示例将展示一些相关策略：</p>')),
    (b'<p>When creating a file, write the data to a <code>String</code> or <code>Vec&lt;u8&gt;</code> and then\r\nwrite the entire file in a single <code>spawn_blocking</code> call with\r\n<code>tokio::fs::write</code>.</p>',
     E('<p>创建文件时，将数据写入 <code>String</code> 或 <code>Vec&lt;u8&gt;</code>，\r\n然后使用 <code>tokio::fs::write</code> 在\r\n单个 <code>spawn_blocking</code> 调用中写入整个文件。</p>')),
    (b'<p>Use <a href="../io/struct.BufReader.html" title="struct tokio::io::BufReader"><code>BufReader</code></a> and <a href="../io/struct.BufWriter.html" title="struct tokio::io::BufWriter"><code>BufWriter</code></a> to buffer many small reads or writes\r\ninto a few large ones. This example will most likely only perform one\r\n<code>spawn_blocking</code> call.</p>',
     E('<p>使用 <a href="../io/struct.BufReader.html" title="struct tokio::io::BufReader"><code>BufReader</code></a> 和 <a href="../io/struct.BufWriter.html" title="struct tokio::io::BufWriter"><code>BufWriter</code></a> 将许多小的读/写操作\r\n缓冲为少数大的读/写操作。\r\n此示例很可能只会执行一次 <code>spawn_blocking</code> 调用。</p>')),
    (b'<p>Manually use <a href="https://doc.rust-lang.org/1.95.0/std/fs/index.html" title="mod std::fs"><code>std::fs</code></a> inside <a href="../task/fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a>.</p>',
     E('<p>在 <a href="../task/fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a> 中手动使用 <a href="https://doc.rust-lang.org/1.95.0/std/fs/index.html" title="mod std::fs"><code>std::fs</code></a>。</p>')),
    (b'<p>It\xe2\x80\x99s also good to be aware of <a href="struct.File.html#method.set_max_buf_size" title="method tokio::fs::File::set_max_buf_size"><code>File::set_max_buf_size</code></a>, which controls the\r\nmaximum amount of bytes that Tokio\xe2\x80\x99s <a href="struct.File.html" title="struct tokio::fs::File"><code>File</code></a> will read or write in a single\r\n<a href="../task/fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a> call. The default is two megabytes, but this is subject\r\nto change.</p>',
     E('<p>还应注意 <a href="struct.File.html#method.set_max_buf_size" title="method tokio::fs::File::set_max_buf_size"><code>File::set_max_buf_size</code></a>，\r\n它控制 Tokio 的 <a href="struct.File.html" title="struct tokio::fs::File"><code>File</code></a> 在单个\r\n<a href="../task/fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a> 调用中\r\n将读取或写入的最大字节数。默认为 2 MB，但可能会更改。</p>')),
])


# ============================================================
# fs/struct.File.html (top-doc only)
# ============================================================
add('fs/struct.File.html', [
    (b'<p>A reference to an open file on the filesystem.</p>',
     E('<p>对文件系统上打开文件的引用。</p>')),
    (b'<p>This is a specialized version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.File.html" title="struct std::fs::File"><code>std::fs::File</code></a> for usage from the\r\nTokio runtime.</p>',
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.File.html" title="struct std::fs::File"><code>std::fs::File</code></a> 的特化版本，用于\r\nTokio 运行时。</p>')),
    (b'<p>An instance of a <code>File</code> can be read and/or written depending on what options\r\nit was opened with. Files also implement <a href="../io/trait.AsyncSeek.html" title="trait tokio::io::AsyncSeek"><code>AsyncSeek</code></a> to alter the logical\r\ncursor that the file contains internally.</p>',
     E('<p>可以根据打开时使用的选项对 <code>File</code> 实例进行读取\r\n和/或写入。文件还实现了 <a href="../io/trait.AsyncSeek.html" title="trait tokio::io::AsyncSeek"><code>AsyncSeek</code></a>，用于改变\r\n文件内部包含的逻辑游标。</p>')),
    (b'<p>A file will not be closed immediately when it goes out of scope if there\r\nare any IO operations that have not yet completed. To ensure that a file is\r\nclosed immediately when it is dropped, you should call <a href="../io/trait.AsyncWriteExt.html#method.flush" title="method tokio::io::AsyncWriteExt::flush"><code>flush</code></a> before\r\ndropping it. Note that this does not ensure that the file has been fully\r\nwritten to disk; the operating system might keep the changes around in an\r\nin-memory buffer. See the <a href="struct.File.html#method.sync_all" title="method tokio::fs::File::sync_all"><code>sync_all</code></a> method for telling the OS to write\r\nthe data to disk.</p>',
     E('<p>如果存在尚未完成的 IO 操作，文件在超出作用域时不会\r\n立即关闭。为确保文件在丢弃时立即关闭，\r\n应在丢弃之前调用 <a href="../io/trait.AsyncWriteExt.html#method.flush" title="method tokio::io::AsyncWriteExt::flush"><code>flush</code></a>。\r\n请注意，这不能确保文件已完全\r\n写入磁盘；操作系统可能会将更改保留在\r\n内存缓冲区中。有关告知操作系统将数据写入磁盘的信息，\r\n请参阅 <a href="struct.File.html#method.sync_all" title="method tokio::fs::File::sync_all"><code>sync_all</code></a> 方法。</p>')),
    (b'<p>Reading and writing to a <code>File</code> is usually done using the convenience\r\nmethods found on the <a href="../io/trait.AsyncReadExt.html" title="trait tokio::io::AsyncReadExt"><code>AsyncReadExt</code></a> and <a href="../io/trait.AsyncWriteExt.html" title="trait tokio::io::AsyncWriteExt"><code>AsyncWriteExt</code></a> traits.</p>',
     E('<p>对 <code>File</code> 的读写通常使用\r\n<a href="../io/trait.AsyncReadExt.html" title="trait tokio::io::AsyncReadExt"><code>AsyncReadExt</code></a> 和 <a href="../io/trait.AsyncWriteExt.html" title="trait tokio::io::AsyncWriteExt"><code>AsyncWriteExt</code></a> trait 中的\r\n便捷方法来完成。</p>')),
    (b'<p>Create a new file and asynchronously write bytes to it:</p>',
     E('<p>创建一个新文件并以异步方式向其写入字节：</p>')),
    (b'<p>Read the contents of a file into a buffer:</p>',
     E('<p>将文件的内容读入缓冲区：</p>')),
    (b'<p>See <a href="struct.OpenOptions.html" title="struct tokio::fs::OpenOptions"><code>OpenOptions</code></a> for more details.</p>',
     E('<p>有关更多详细信息，请参阅 <a href="struct.OpenOptions.html" title="struct tokio::fs::OpenOptions"><code>OpenOptions</code></a>。</p>')),
    (b'<p>This function will return an error if called from outside of the Tokio\r\nruntime or if path does not already exist. Other errors may also be\r\nreturned according to <code>OpenOptions::open</code>.</p>',
     E('<p>如果在 Tokio 运行时\r\n外部调用，或者路径不存在，此函数将返回错误。\r\n根据 <code>OpenOptions::open</code>，也可能会返回其他错误。</p>')),
    (b'<p>The <a href="../io/trait.AsyncReadExt.html#method.read_to_end" title="method tokio::io::AsyncReadExt::read_to_end"><code>read_to_end</code></a> method is defined on the <a href="../io/trait.AsyncReadExt.html" title="trait tokio::io::AsyncReadExt"><code>AsyncReadExt</code></a> trait.</p>',
     E('<p><a href="../io/trait.AsyncReadExt.html#method.read_to_end" title="method tokio::io::AsyncReadExt::read_to_end"><code>read_to_end</code></a> 方法定义在 <a href="../io/trait.AsyncReadExt.html" title="trait tokio::io::AsyncReadExt"><code>AsyncReadExt</code></a> trait 上。</p>')),
    (b'<p>Results in an error if called from outside of the Tokio runtime or if\r\nthe underlying <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.File.html#method.create" title="associated function std::fs::File::create"><code>create</code></a> call results in an error.</p>',
     E('<p>如果在 Tokio 运行时外部调用，或者\r\n底层的 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.File.html#method.create" title="associated function std::fs::File::create"><code>create</code></a> 调用导致错误，则会导致错误。</p>')),
    (b'<p>The <a href="../io/trait.AsyncWriteExt.html#method.write_all" title="method tokio::io::AsyncWriteExt::write_all"><code>write_all</code></a> method is defined on the <a href="../io/trait.AsyncWriteExt.html" title="trait tokio::io::AsyncWriteExt"><code>AsyncWriteExt</code></a> trait.</p>',
     E('<p><a href="../io/trait.AsyncWriteExt.html#method.write_all" title="method tokio::io::AsyncWriteExt::write_all"><code>write_all</code></a> 方法定义在 <a href="../io/trait.AsyncWriteExt.html" title="trait tokio::io::AsyncWriteExt"><code>AsyncWriteExt</code></a> trait 上。</p>')),
    (b'<p>This option is useful because it is atomic. Otherwise between checking\r\nwhether a file exists and creating a new one, the file may have been\r\ncreated by another process (a TOCTOU race condition / attack).</p>',
     E('<p>此选项很有用，因为它是原子操作。否则，\r\n在检查文件是否存在和创建新文件之间，\r\n文件可能已被其他进程创建（TOCTOU 竞态条件/攻击）。</p>')),
    (b'<p>Returns a new <a href="struct.OpenOptions.html" title="struct tokio::fs::OpenOptions"><code>OpenOptions</code></a> object.</p>',
     E('<p>返回一个新的 <a href="struct.OpenOptions.html" title="struct tokio::fs::OpenOptions"><code>OpenOptions</code></a> 对象。</p>')),
    (b'<p>This function returns a new <code>OpenOptions</code> object that you can use to\r\nopen or create a file with specific options if <code>open()</code> or <code>create()</code>\r\nare not appropriate.</p>',
     E('<p>此函数返回一个新的 <code>OpenOptions</code> 对象，如果 <code>open()</code> 或 <code>create()</code>\r\n不合适，你可以使用它来\r\n以特定选项打开或创建文件。</p>')),
    (b'<p>It is equivalent to <code>OpenOptions::new()</code>, but allows you to write more\r\nreadable code. Instead of\r\n<code>OpenOptions::new().append(true).open("example.log")</code>,\r\nyou can write <code>File::options().append(true).open("example.log")</code>. This\r\nalso avoids the need to import <code>OpenOptions</code>.</p>',
     E('<p>它等价于 <code>OpenOptions::new()</code>，但允许你编写更\r\n可读的代码。可以使用\r\n<code>File::options().append(true).open("example.log")</code>\r\n代替 <code>OpenOptions::new().append(true).open("example.log")</code>。\r\n这还避免了导入 <code>OpenOptions</code> 的需要。</p>')),
    (b'<p>See the <a href="struct.OpenOptions.html#method.new" title="associated function tokio::fs::OpenOptions::new"><code>OpenOptions::new</code></a> function for more details.</p>',
     E('<p>有关更多详细信息，请参阅 <a href="struct.OpenOptions.html#method.new" title="associated function tokio::fs::OpenOptions::new"><code>OpenOptions::new</code></a> 函数。</p>')),
    (b'<p>Converts a <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.File.html" title="struct std::fs::File"><code>std::fs::File</code></a> to a <a href="struct.File.html" title="struct tokio::fs::File"><code>tokio::fs::File</code></a>.</p>',
     E('<p>将 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.File.html" title="struct std::fs::File"><code>std::fs::File</code></a> 转换为 <a href="struct.File.html" title="struct tokio::fs::File"><code>tokio::fs::File</code></a>。</p>')),
    (b'<p>This function will attempt to ensure that all in-core data reaches the\r\nfilesystem before returning.</p>',
     E('<p>此函数将尝试确保所有内核中的数据在返回前已到达\r\n文件系统。</p>')),
    (b'<p>This function is similar to <code>sync_all</code>, except that it may not\r\nsynchronize file metadata to the filesystem.</p>',
     E('<p>此函数与 <code>sync_all</code> 类似，只是它\r\n不会将文件元数据同步到文件系统。</p>')),
    (b'<p>This is intended for use cases that must synchronize content, but don\xe2\x80\x99t\r\nneed the metadata on disk. The goal of this method is to reduce disk\r\noperations.</p>',
     E('<p>此方法用于必须同步内容但\r\n不需要磁盘上的元数据的用例。\r\n此方法的目标是减少磁盘操作。</p>')),
    (b'<p>Note that some platforms may simply implement this in terms of <code>sync_all</code>.</p>',
     E('<p>请注意，某些平台可能直接基于 <code>sync_all</code> 实现此方法。</p>')),
    (b'<p>Truncates or extends the underlying file, updating the size of this file to become size.</p>',
     E('<p>截断或扩展底层文件，将此文件的大小更新为 size。</p>')),
    (b'<p>If the size is less than the current file\xe2\x80\x99s size, then the file will be\r\nshrunk. If it is greater than the current file\xe2\x80\x99s size, then the file\r\nwill be extended to size and have all of the intermediate data filled in\r\nwith 0s.</p>',
     E('<p>如果 size 小于当前文件的大小，则文件将\r\n被缩小。如果大于当前文件的大小，\r\n则文件将扩展到 size，并且所有中间数据都将\r\n填充为 0。</p>')),
    (b'<p>This function will return an error if the file is not opened for\r\nwriting.</p>',
     E('<p>如果文件未以写入\r\n方式打开，此函数将返回错误。</p>')),
    (b'<p>Queries metadata about the underlying file.</p>',
     E('<p>查询有关底层文件的元数据。</p>')),
    (b'<p>Creates a new <code>File</code> instance that shares the same underlying file handle\r\nas the existing <code>File</code> instance. Reads, writes, and seeks will affect both\r\nFile instances simultaneously.</p>',
     E('<p>创建一个新的 <code>File</code> 实例，与现有 <code>File</code> 实例共享\r\n相同的底层文件句柄。读取、写入和 seek 操作将\r\n同时影响两个 File 实例。</p>')),
    (b'<p>Destructures <code>File</code> into a <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.File.html" title="struct std::fs::File"><code>std::fs::File</code></a>. This function is\r\nasync to allow any in-flight operations to complete.</p>',
     E('<p>将 <code>File</code> 解构为 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.File.html" title="struct std::fs::File"><code>std::fs::File</code></a>。此函数是\r\n异步的，以允许所有进行中的操作完成。</p>')),
    (b'<p>Use <code>File::try_into_std</code> to attempt conversion immediately.</p>',
     E('<p>使用 <code>File::try_into_std</code> 立即尝试转换。</p>')),
    (b'<p>Tries to immediately destructure <code>File</code> into a <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.File.html" title="struct std::fs::File"><code>std::fs::File</code></a>.</p>',
     E('<p>尝试将 <code>File</code> 立即解构为 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.File.html" title="struct std::fs::File"><code>std::fs::File</code></a>。</p>')),
    (b'<p>This function will return an error containing the file if some\r\noperation is in-flight.</p>',
     E('<p>如果某些\r\n操作正在进行中，此函数将返回包含该文件的错误。</p>')),
    (b'<p>Changes the permissions on the underlying file.</p>',
     E('<p>更改底层文件的权限。</p>')),
    (b'<p>This function currently corresponds to the <code>fchmod</code> function on Unix and\r\nthe <code>SetFileInformationByHandle</code> function on Windows. Note that, this\r\n<a href="https://doc.rust-lang.org/std/io/index.html#platform-specific-behavior">may change in the future</a>.</p>',
     E('<p>此函数当前对应于 Unix 上的 <code>fchmod</code> 函数和\r\nWindows 上的 <code>SetFileInformationByHandle</code> 函数。请注意，\r\n<a href="https://doc.rust-lang.org/std/io/index.html#platform-specific-behavior">未来可能会发生变化</a>。</p>')),
    (b'<p>This function will return an error if the user lacks permission change\r\nattributes on the underlying file. It may also return an error in other\r\nos-specific unspecified cases.</p>',
     E('<p>如果用户缺少对底层文件的\r\n权限更改属性，此函数将返回错误。\r\n在其他操作系统特定但未指明的情况下，它也可能返回错误。</p>')),
    (b'<p>Set the maximum buffer size for the underlying <a href="../io/trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> / <a href="../io/trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> operation.</p>',
     E('<p>为底层的 <a href="../io/trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> / <a href="../io/trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> 操作设置最大缓冲区大小。</p>')),
    (b'<p>Although Tokio uses a sensible default value for this buffer size, this function would be\r\nuseful for changing that default depending on the situation.</p>',
     E('<p>虽然 Tokio 为此缓冲区大小使用了一个合理的默认值，\r\n但此函数可用于根据具体情况更改该默认值。</p>')),
])


# ============================================================
# io/fn.copy.html
# ============================================================
add('io/fn.copy.html', [
    (b'<p>This function returns a future that will continuously read data from\r\n<code>reader</code> and then write it into <code>writer</code> in a streaming fashion until\r\n<code>reader</code> returns EOF or fails.</p>',
     E('<p>此函数返回一个 future，它将以流式方式持续从 <code>reader</code>\r\n读取数据，然后将其写入 <code>writer</code>，直到 <code>reader</code>\r\n返回 EOF 或失败。</p>')),
    (b'<p>This is an asynchronous version of <a href="https://doc.rust-lang.org/1.95.0/std/io/copy/fn.copy.html" title="fn std::io::copy::copy"><code>std::io::copy</code></a>.</p>',
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/io/copy/fn.copy.html" title="fn std::io::copy::copy"><code>std::io::copy</code></a> 的异步版本。</p>')),
    (b'<p>A heap-allocated copy buffer with 8 KB is created to take data from the\r\nreader to the writer, check <a href="fn.copy_buf.html" title="fn tokio::io::copy_buf"><code>copy_buf</code></a> if you want an alternative for\r\n<a href="trait.AsyncBufRead.html" title="trait tokio::io::AsyncBufRead"><code>AsyncBufRead</code></a>. You can use <code>copy_buf</code> with <a href="struct.BufReader.html" title="struct tokio::io::BufReader"><code>BufReader</code></a> to change the\r\nbuffer capacity.</p>',
     E('<p>会创建一个 8 KB 的堆分配复制缓冲区以将数据从读取器\r\n传送到写入器，如果想要 <a href="trait.AsyncBufRead.html" title="trait tokio::io::AsyncBufRead"><code>AsyncBufRead</code></a> 的替代方案，\r\n请查看 <a href="fn.copy_buf.html" title="fn tokio::io::copy_buf"><code>copy_buf</code></a>。你可以将 <code>copy_buf</code> 与\r\n<a href="struct.BufReader.html" title="struct tokio::io::BufReader"><code>BufReader</code></a> 一起使用以更改缓冲区容量。</p>')),
    (b'<p>If you are looking to use <a href="https://doc.rust-lang.org/1.95.0/std/io/copy/fn.copy.html" title="fn std::io::copy::copy"><code>std::io::copy</code></a> with a synchronous consumer\r\n(like a <code>hasher</code> or compressor), consider using async alternatives instead of\r\nwrapping the reader with <a href="https://docs.rs/tokio-util/latest/tokio_util/io/struct.SyncIoBridge.html"><code>SyncIoBridge</code></a>.\r\nSee the <a href="https://docs.rs/tokio-util/latest/tokio_util/io/struct.SyncIoBridge.html"><code>SyncIoBridge</code></a> documentation for detailed examples and guidance.</p>',
     E('<p>如果你希望将 <a href="https://doc.rust-lang.org/1.95.0/std/io/copy/fn.copy.html" title="fn std::io::copy::copy"><code>std::io::copy</code></a> 与同步消费者\r\n（如 <code>hasher</code> 或压缩器）一起使用，请考虑使用异步替代方案，\r\n而不是使用 <a href="https://docs.rs/tokio-util/latest/tokio_util/io/struct.SyncIoBridge.html"><code>SyncIoBridge</code></a> 包装读取器。\r\n有关详细示例和指南，请参阅 <a href="https://docs.rs/tokio-util/latest/tokio_util/io/struct.SyncIoBridge.html"><code>SyncIoBridge</code></a> 文档。</p>')),
    (b'<p>The returned future will return an error immediately if any call to\r\n<code>poll_read</code> or <code>poll_write</code> returns an error.</p>',
     E('<p>如果对 <code>poll_read</code> 或 <code>poll_write</code> 的任何调用返回错误，\r\n则返回的 future 将立即返回错误。</p>')),
])


# ============================================================
# io/fn.copy_bidirectional.html
# ============================================================
add('io/fn.copy_bidirectional.html', [
    (b'<p>This function returns a future that will read from both streams,\r\nwriting any data read to the opposing stream.\r\nThis happens in both directions concurrently.</p>',
     E('<p>此函数返回一个 future，它将从两个流读取数据，\r\n并将读取的任何数据写入对端流。\r\n这在两个方向上并发进行。</p>')),
    (b'<p>If an EOF is observed on one stream, <a href="trait.AsyncWriteExt.html#method.shutdown" title="method tokio::io::AsyncWriteExt::shutdown"><code>shutdown()</code></a> will be invoked on\r\nthe other, and reading from that stream will stop. Copying of data in\r\nthe other direction will continue.</p>',
     E('<p>如果在一个流上观察到 EOF，将\r\n在另一个流上调用 <a href="trait.AsyncWriteExt.html#method.shutdown" title="method tokio::io::AsyncWriteExt::shutdown"><code>shutdown()</code></a>，\r\n并停止从该流读取。另一个方向上的数据\r\n复制将继续。</p>')),
    (b'<p>The future will complete successfully once both directions of communication has been shut down.\r\nA direction is shut down when the reader reports EOF,\r\nat which point <a href="trait.AsyncWriteExt.html#method.shutdown" title="method tokio::io::AsyncWriteExt::shutdown"><code>shutdown()</code></a> is called on the corresponding writer. When finished,\r\nit will return a tuple of the number of bytes copied from a to b\r\nand the number of bytes copied from b to a, in that order.</p>',
     E('<p>当通信的两个方向都已关闭时，future 将\r\n成功完成。当读取器报告 EOF 时，\r\n该方向将被关闭，此时\r\n在相应的写入器上调用 <a href="trait.AsyncWriteExt.html#method.shutdown" title="method tokio::io::AsyncWriteExt::shutdown"><code>shutdown()</code></a>。完成后，\r\n它将按顺序返回一个元组，分别是从 a 复制到 b 的字节数和\r\n从 b 复制到 a 的字节数。</p>')),
    (b'<p>It uses two 8 KB buffers for transferring bytes between <code>a</code> and <code>b</code> by default.\r\nTo set your own buffers sizes use <a href="fn.copy_bidirectional_with_sizes.html" title="fn tokio::io::copy_bidirectional_with_sizes"><code>copy_bidirectional_with_sizes()</code></a>.</p>',
     E('<p>默认情况下，它使用两个 8 KB 缓冲区在 <code>a</code> 和 <code>b</code>\r\n之间传输字节。要设置自己的缓冲区大小，\r\n请使用 <a href="fn.copy_bidirectional_with_sizes.html" title="fn tokio::io::copy_bidirectional_with_sizes"><code>copy_bidirectional_with_sizes()</code></a>。</p>')),
    (b'<p>The future will immediately return an error if any IO operation on <code>a</code>\r\nor <code>b</code> returns an error. Some data read from either stream may be lost (not\r\nwritten to the other stream) in this case.</p>',
     E('<p>如果对 <code>a</code> 或 <code>b</code> 的任何 IO 操作返回错误，\r\nfuture 将立即返回错误。在这种情况下，\r\n从任一流读取的部分数据可能会丢失\r\n（未写入对端流）。</p>')),
    (b'<p>Returns a tuple of bytes copied <code>a</code> to <code>b</code> and bytes copied <code>b</code> to <code>a</code>.</p>',
     E('<p>返回一个元组，分别为从 <code>a</code> 复制到 <code>b</code> 的字节数和从 <code>b</code> 复制到 <code>a</code> 的字节数。</p>')),
])


# ============================================================
# fs/struct.ReadDir.html
# ============================================================
add('fs/struct.ReadDir.html', [
    (b'<p>Reads the entries in a directory.</p>',
     E('<p>读取目录中的条目。</p>')),
    (b'<p>This struct is returned from the <a href="fn.read_dir.html" title="fn tokio::fs::read_dir"><code>read_dir</code></a> function of this module and\r\nwill yield instances of <a href="struct.DirEntry.html" title="struct tokio::fs::DirEntry"><code>DirEntry</code></a>. Through a <a href="struct.DirEntry.html" title="struct tokio::fs::DirEntry"><code>DirEntry</code></a> information\r\nlike the entry\xe2\x80\x99s path and possibly other metadata can be learned.</p>',
     E('<p>此结构体由本模块的 <a href="fn.read_dir.html" title="fn tokio::fs::read_dir"><code>read_dir</code></a> 函数返回，\r\n并将产生 <a href="struct.DirEntry.html" title="struct tokio::fs::DirEntry"><code>DirEntry</code></a> 实例。\r\n通过 <a href="struct.DirEntry.html" title="struct tokio::fs::DirEntry"><code>DirEntry</code></a>，可以了解诸如\r\n条目路径以及可能的元数据等信息。</p>')),
    (b'<p>A <code>ReadDir</code> can be turned into a <code>Stream</code> with <a href="https://docs.rs/tokio-stream/0.1/tokio_stream/wrappers/struct.ReadDirStream.html"><code>ReadDirStream</code></a>.</p>',
     E('<p>可以使用 <a href="https://docs.rs/tokio-stream/0.1/tokio_stream/wrappers/struct.ReadDirStream.html"><code>ReadDirStream</code></a> 将 <code>ReadDir</code> 转换为 <code>Stream</code>。</p>')),
    (b'<p>This stream will return an <a href="https://doc.rust-lang.org/1.95.0/core/result/enum.Result.html#variant.Err" title="variant core::result::Result::Err"><code>Err</code></a> if there\xe2\x80\x99s some sort of intermittent\r\nIO error during iteration.</p>',
     E('<p>如果在迭代过程中出现某种间歇性 IO 错误，\r\n此流将返回 <a href="https://doc.rust-lang.org/1.95.0/core/result/enum.Result.html#variant.Err" title="variant core::result::Result::Err"><code>Err</code></a>。</p>')),
    (b'<p>When the method returns <code>Poll::Pending</code>, the <code>Waker</code> in the provided\r\n<code>Context</code> is scheduled to receive a wakeup when the next directory entry\r\nbecomes available on the underlying IO resource.</p>',
     E('<p>当该方法返回 <code>Poll::Pending</code> 时，提供的\r\n<code>Context</code> 中的 <code>Waker</code> 被安排为在下一个目录条目\r\n在底层 IO 资源上可用时接收唤醒。</p>')),
    (b'<p>Note that on multiple calls to <code>poll_next_entry</code>, only the <code>Waker</code> from\r\nthe <code>Context</code> passed to the most recent call is scheduled to receive a\r\nwakeup.</p>',
     E('<p>请注意，对于多次调用 <code>poll_next_entry</code>，\r\n只有传递给最近一次调用的 <code>Context</code> 中的 <code>Waker</code> 才会\r\n被安排接收唤醒。</p>')),
])


# ============================================================
# fs/struct.OpenOptions.html
# ============================================================
add('fs/struct.OpenOptions.html', [
    (b'<p>This builder exposes the ability to configure how a <a href="struct.File.html" title="struct tokio::fs::File"><code>File</code></a> is opened and\r\nwhat operations are permitted on the open file. The <a href="struct.File.html#method.open" title="associated function tokio::fs::File::open"><code>File::open</code></a> and\r\n<a href="struct.File.html#method.create" title="associated function tokio::fs::File::create"><code>File::create</code></a> methods are aliases for commonly used options using this\r\nbuilder.</p>',
     E('<p>此构建器提供配置 <a href="struct.File.html" title="struct tokio::fs::File"><code>File</code></a> 的打开方式以及\r\n允许在打开的文件上执行哪些操作的能力。\r\n<a href="struct.File.html#method.open" title="associated function tokio::fs::File::open"><code>File::open</code></a> 和 <a href="struct.File.html#method.create" title="associated function tokio::fs::File::create"><code>File::create</code></a>\r\n方法使用此构建器作为常用选项的别名。</p>')),
    (b'<p>Generally speaking, when using <code>OpenOptions</code>, you\xe2\x80\x99ll first call <a href="struct.OpenOptions.html#method.new" title="associated function tokio::fs::OpenOptions::new"><code>new</code></a>,\r\nthen chain calls to methods to set each option, then call <a href="struct.OpenOptions.html#method.open" title="method tokio::fs::OpenOptions::open"><code>open</code></a>, passing\r\nthe path of the file you\xe2\x80\x99re trying to open. This will give you a\r\n<a href="https://doc.rust-lang.org/1.95.0/std/io/error/type.Result.html" title="type std::io::error::Result"><code>io::Result</code></a> with a <a href="struct.File.html" title="struct tokio::fs::File"><code>File</code></a> inside that you can further operate\r\non.</p>',
     E('<p>一般来说，使用 <code>OpenOptions</code> 时，你将首先调用 <a href="struct.OpenOptions.html#method.new" title="associated function tokio::fs::OpenOptions::new"><code>new</code></a>，\r\n然后链接方法调用以设置每个选项，然后调用 <a href="struct.OpenOptions.html#method.open" title="method tokio::fs::OpenOptions::open"><code>open</code></a>，\r\n传入要打开的文件的路径。这将\r\n为你提供一个 <a href="https://doc.rust-lang.org/1.95.0/std/io/error/type.Result.html" title="type std::io::error::Result"><code>io::Result</code></a>，其中\r\n包含一个 <a href="struct.File.html" title="struct tokio::fs::File"><code>File</code></a>，你可以对其进行进一步\r\n操作。</p>')),
    (b'<p>This is a specialized version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.OpenOptions.html" title="struct std::fs::OpenOptions"><code>std::fs::OpenOptions</code></a> for usage from\r\nthe Tokio runtime.</p>',
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.OpenOptions.html" title="struct std::fs::OpenOptions"><code>std::fs::OpenOptions</code></a> 的特化版本，用于\r\nTokio 运行时。</p>')),
    (b'<p><code>From&lt;std::fs::OpenOptions&gt;</code> is implemented for more advanced configuration\r\nthan the methods provided here.</p>',
     E('<p>为比此处提供的方法更高级的配置\r\n实现了 <code>From&lt;std::fs::OpenOptions&gt;</code>。</p>')),
    (b'<p>Opening a file to read:</p>',
     E('<p>打开文件以进行读取：</p>')),
    (b'<p>Opening a file for both reading and writing, as well as creating it if it\r\ndoesn\xe2\x80\x99t exist:</p>',
     E('<p>打开一个文件以进行读写，并在文件\r\n不存在时创建它：</p>')),
    (b'<p>All options are initially set to <code>false</code>.</p>',
     E('<p>所有选项最初都设置为 <code>false</code>。</p>')),
    (b'<p>This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.OpenOptions.html#method.new" title="associated function std::fs::OpenOptions::new"><code>std::fs::OpenOptions::new</code></a>',
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.OpenOptions.html#method.new" title="associated function std::fs::OpenOptions::new"><code>std::fs::OpenOptions::new</code></a> 的异步版本')),
    (b'<p>This option, when true, will indicate that the file should be\r\n<code>read</code>-able if opened.</p>',
     E('<p>当此选项为 true 时，将\r\n指示文件在打开时应该是可\r\n<code>read</code>（读取）的。</p>')),
    (b'<p>This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.OpenOptions.html#method.read" title="method std::fs::OpenOptions::read"><code>std::fs::OpenOptions::read</code></a>',
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.OpenOptions.html#method.read" title="method std::fs::OpenOptions::read"><code>std::fs::OpenOptions::read</code></a> 的异步版本')),
    (b'<p>This option, when true, will indicate that the file should be\r\n<code>write</code>-able if opened.</p>',
     E('<p>当此选项为 true 时，将\r\n指示文件在打开时应该是可\r\n<code>write</code>（写入）的。</p>')),
    (b'<p>This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.OpenOptions.html#method.write" title="method std::fs::OpenOptions::write"><code>std::fs::OpenOptions::write</code></a>',
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.OpenOptions.html#method.write" title="method std::fs::OpenOptions::write"><code>std::fs::OpenOptions::write</code></a> 的异步版本')),
    (b'<p>This option, when true, means that writes will append to a file instead\r\nof overwriting previous contents.  Note that setting\r\n<code>.write(true).append(true)</code> has the same effect as setting only\r\n<code>.append(true)</code>.</p>',
     E('<p>当此选项为 true 时，表示写入将\r\n追加到文件末尾而不是覆盖\r\n之前的内容。请注意，设置\r\n<code>.write(true).append(true)</code> 与仅设置\r\n<code>.append(true)</code> 的效果相同。</p>')),
    (b'<p>For most filesystems, the operating system guarantees that all writes are\r\natomic: no writes get mangled because another process writes at the same\r\ntime.</p>',
     E('<p>对于大多数文件系统，操作系统保证所有\r\n写入都是原子的：不会因另一个进程同时\r\n写入而损坏写入。</p>')),
    (b'<p>One maybe obvious note when using append-mode: make sure that all data\r\nthat belongs together is written to the file in one operation. This\r\ncan be done by concatenating strings before passing them to <a href="../io/trait.AsyncWriteExt.html#method.write" title="method tokio::io::AsyncWriteExt::write"><code>write()</code></a>,\r\nor using a buffered writer (with a buffer of adequate size),\r\nand calling <a href="../io/trait.AsyncWriteExt.html#method.flush" title="method tokio::io::AsyncWriteExt::flush"><code>flush()</code></a> when the message is complete.</p>',
     E('<p>使用追加模式时，也许一个明显的注意事项是：\r\n确保所有属于一起的数据\r\n在一次操作中写入文件。这可以通过在\r\n将字符串传递给 <a href="../io/trait.AsyncWriteExt.html#method.write" title="method tokio::io::AsyncWriteExt::write"><code>write()</code></a> 之前连接字符串来实现，\r\n或者使用缓冲写入器（具有足够大小的缓冲区），\r\n并在消息完成时调用 <a href="../io/trait.AsyncWriteExt.html#method.flush" title="method tokio::io::AsyncWriteExt::flush"><code>flush()</code></a>。</p>')),
    (b'<p>If a file is opened with both read and append access, beware that after\r\nopening, and after every write, the position for reading may be set at the\r\nend of the file. So, before writing, save the current position (using\r\n<a href="../io/trait.AsyncSeekExt.html#method.seek" title="method tokio::io::AsyncSeekExt::seek"><code>seek</code></a><code>(</code><a href="https://doc.rust-lang.org/1.95.0/std/io/enum.SeekFrom.html" title="enum std::io::SeekFrom"><code>SeekFrom</code></a><code>::</code><a href="https://doc.rust-lang.org/1.95.0/std/io/enum.SeekFrom.html#variant.Current" title="variant std::io::SeekFrom::Current"><code>Current</code></a><code>(0))</code>), and restore it before the next read.</p>',
     E('<p>如果文件同时以读取和追加访问权限打开，请注意\r\n在打开之后以及每次写入之后，读取\r\n位置可能会被设置在\r\n文件末尾。因此，在写入之前，请保存当前位置\r\n（使用 <a href="../io/trait.AsyncSeekExt.html#method.seek" title="method tokio::io::AsyncSeekExt::seek"><code>seek</code></a><code>(</code><a href="https://doc.rust-lang.org/1.95.0/std/io/enum.SeekFrom.html" title="enum std::io::SeekFrom"><code>SeekFrom</code></a><code>::</code><a href="https://doc.rust-lang.org/1.95.0/std/io/enum.SeekFrom.html#variant.Current" title="variant std::io::SeekFrom::Current"><code>Current</code></a><code>(0))</code>），\r\n并在下次读取之前恢复它。</p>')),
    (b'<p>This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.OpenOptions.html#method.append" title="method std::fs::OpenOptions::append"><code>std::fs::OpenOptions::append</code></a>',
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.OpenOptions.html#method.append" title="method std::fs::OpenOptions::append"><code>std::fs::OpenOptions::append</code></a> 的异步版本')),
    (b'<p>This function doesn\xe2\x80\x99t create the file if it doesn\xe2\x80\x99t exist. Use the <a href="struct.OpenOptions.html#method.create" title="method tokio::fs::OpenOptions::create"><code>create</code></a>\r\nmethod to do so.</p>',
     E('<p>如果文件不存在，此函数不会创建该文件。\r\n请使用 <a href="struct.OpenOptions.html#method.create" title="method tokio::fs::OpenOptions::create"><code>create</code></a> 方法来\r\n创建文件。</p>')),
    (b'<p>Sets the option for truncating a previous file.</p>',
     E('<p>设置截断先前文件的选项。</p>')),
    (b'<p>If a file is successfully opened with this option set it will truncate\r\nthe file to 0 length if it already exists.</p>',
     E('<p>如果设置了此选项并成功打开文件，\r\n则如果文件已存在，将\r\n其截断为 0 长度。</p>')),
    (b'<p>The file must be opened with write access for truncate to work.</p>',
     E('<p>文件必须以写入访问权限打开才能进行截断。</p>')),
    (b'<p>This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.OpenOptions.html#method.truncate" title="method std::fs::OpenOptions::truncate"><code>std::fs::OpenOptions::truncate</code></a>',
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.OpenOptions.html#method.truncate" title="method std::fs::OpenOptions::truncate"><code>std::fs::OpenOptions::truncate</code></a> 的异步版本')),
    (b'<p>This option indicates whether a new file will be created if the file\r\ndoes not yet already exist.</p>',
     E('<p>此选项指示如果文件\r\n尚不存在，是否将创建新文件。</p>')),
    (b'<p>In order for the file to be created, <a href="struct.OpenOptions.html#method.write" title="method tokio::fs::OpenOptions::write"><code>write</code></a> or <a href="struct.OpenOptions.html#method.append" title="method tokio::fs::OpenOptions::append"><code>append</code></a> access must\r\nbe used.</p>',
     E('<p>为了创建文件，必须使用 <a href="struct.OpenOptions.html#method.write" title="method tokio::fs::OpenOptions::write"><code>write</code></a> 或\r\n<a href="struct.OpenOptions.html#method.append" title="method tokio::fs::OpenOptions::append"><code>append</code></a> 访问权限。</p>')),
    (b'<p>This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.OpenOptions.html#method.create" title="method std::fs::OpenOptions::create"><code>std::fs::OpenOptions::create</code></a>',
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.OpenOptions.html#method.create" title="method std::fs::OpenOptions::create"><code>std::fs::OpenOptions::create</code></a> 的异步版本')),
    (b'<p>Sets the option to always create a new file.</p>',
     E('<p>设置始终创建新文件的选项。</p>')),
    (b'<p>This option indicates whether a new file will be created.  No file is\r\nallowed to exist at the target location, also no (dangling) symlink.</p>',
     E('<p>此选项指示是否将创建新文件。目标位置\r\n不允许存在任何文件，也不允许存在（悬空的）符号链接。</p>')),
    (b'<p>This option is useful because it is atomic. Otherwise between checking\r\nwhether a file exists and creating a new one, the file may have been\r\ncreated by another process (a TOCTOU race condition / attack).</p>',
     E('<p>此选项很有用，因为它是原子操作。否则，在检查\r\n文件是否存在和创建新文件之间，文件可能\r\n已被其他进程创建（TOCTOU 竞态条件/攻击）。</p>')),
    (b'<p>If <code>.create_new(true)</code> is set, <a href="struct.OpenOptions.html#method.create" title="method tokio::fs::OpenOptions::create"><code>.create()</code></a> and <a href="struct.OpenOptions.html#method.truncate" title="method tokio::fs::OpenOptions::truncate"><code>.truncate()</code></a> are\r\nignored.</p>',
     E('<p>如果设置了 <code>.create_new(true)</code>，则\r\n<a href="struct.OpenOptions.html#method.create" title="method tokio::fs::OpenOptions::create"><code>.create()</code></a> 和 <a href="struct.OpenOptions.html#method.truncate" title="method tokio::fs::OpenOptions::truncate"><code>.truncate()</code></a>\r\n将被忽略。</p>')),
    (b'<p>The file must be opened with write or append access in order to create a\r\nnew file.</p>',
     E('<p>文件必须以写入或追加访问权限打开才能\r\n创建新文件。</p>')),
    (b'<p>This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.OpenOptions.html#method.create_new" title="method std::fs::OpenOptions::create_new"><code>std::fs::OpenOptions::create_new</code></a>',
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.OpenOptions.html#method.create_new" title="method std::fs::OpenOptions::create_new"><code>std::fs::OpenOptions::create_new</code></a> 的异步版本')),
    (b'<p>Opens a file at <code>path</code> with the options specified by <code>self</code>.</p>',
     E('<p>使用 <code>self</code> 指定的选项打开位于 <code>path</code> 的文件。</p>')),
    (b'<p>This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.OpenOptions.html#method.open" title="method std::fs::OpenOptions::open"><code>std::fs::OpenOptions::open</code></a>',
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.OpenOptions.html#method.open" title="method std::fs::OpenOptions::open"><code>std::fs::OpenOptions::open</code></a> 的异步版本')),
    (b'<p>This function will return an error under a number of different\r\ncircumstances. Some of these error conditions are listed here, together\r\nwith their <a href="https://doc.rust-lang.org/1.95.0/std/io/error/enum.ErrorKind.html" title="enum std::io::error::ErrorKind"><code>ErrorKind</code></a>. The mapping to <a href="https://doc.rust-lang.org/1.95.0/std/io/error/enum.ErrorKind.html" title="enum std::io::error::ErrorKind"><code>ErrorKind</code></a>s is not part of\r\nthe compatibility contract of the function, especially the <code>Other</code> kind\r\nmight change to more specific kinds in the future.</p>',
     E('<p>此函数在多种不同\r\n情况下会返回错误。此处列出了其中一些\r\n错误情况及其对应的 <a href="https://doc.rust-lang.org/1.95.0/std/io/error/enum.ErrorKind.html" title="enum std::io::error::ErrorKind"><code>ErrorKind</code></a>。\r\n到 <a href="https://doc.rust-lang.org/1.95.0/std/io/error/enum.ErrorKind.html" title="enum std::io::error::ErrorKind"><code>ErrorKind</code></a> 的映射不是函数\r\n兼容性约定的一部分，特别是 <code>Other</code> 种类\r\n将来可能会更改为更具体的种类。</p>')),
    (b'<p>On Linux, you can also use <code>io_uring</code> for executing system calls.\r\nTo enable <code>io_uring</code>, you need to specify the <code>--cfg tokio_unstable</code>\r\nflag at compile time, enable the <code>io-uring</code> cargo feature, and set the\r\n<code>Builder::enable_io_uring</code> runtime option.</p>',
     E('<p>在 Linux 上，你还可以使用 <code>io_uring</code> 来执行系统调用。\r\n要启用 <code>io_uring</code>，需要在编译时指定 <code>--cfg tokio_unstable</code>\r\n标志，启用 <code>io-uring</code> cargo feature，并设置\r\n<code>Builder::enable_io_uring</code> 运行时选项。</p>')),
    (b'<p>Support for <code>io_uring</code> is currently experimental, so its behavior may\r\nchange or it may be removed in future versions.</p>',
     E('<p>目前对 <code>io_uring</code> 的支持是实验性的，因此其行为\r\n可能会发生变化或在未来版本中被移除。</p>')),
    (b'<p>Overrides the <code>dwDesiredAccess</code> argument to the call to <a href="https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea"><code>CreateFile</code></a>\r\nwith the specified value.</p>',
     E('<p>使用指定值覆盖调用 <a href="https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea"><code>CreateFile</code></a> 时\r\n传递的 <code>dwDesiredAccess</code> 参数。</p>')),
    (b'<p>This will override the <code>read</code>, <code>write</code>, and <code>append</code> flags on the\r\n<code>OpenOptions</code> structure. This method provides fine-grained control over\r\nthe permissions to read, write and append data, attributes (like hidden\r\nand system), and extended attributes.</p>',
     E('<p>这将覆盖 <code>OpenOptions</code> 结构上的 <code>read</code>、\r\n<code>write</code> 和 <code>append</code> 标志。\r\n此方法提供对读取、写入和追加数据、属性（如隐藏\r\n和系统）以及扩展属性的精细控制。</p>')),
    (b'<p>Overrides the <code>dwShareMode</code> argument to the call to <a href="https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea"><code>CreateFile</code></a> with\r\nthe specified value.</p>',
     E('<p>使用指定值覆盖调用 <a href="https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea"><code>CreateFile</code></a> 时\r\n传递的 <code>dwShareMode</code> 参数。</p>')),
    (b'<p>By default <code>share_mode</code> is set to\r\n<code>FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE</code>. This allows\r\nother processes to read, write, and delete/rename the same file\r\nwhile it is open. Removing any of the flags will prevent other\r\nprocesses from performing the corresponding operation until the file\r\nhandle is closed.</p>',
     E('<p>默认情况下，<code>share_mode</code> 设置为\r\n<code>FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE</code>。\r\n这允许其他进程在\r\n文件打开时读取、写入和删除/重命名\r\n同一文件。删除任何标志都将阻止其他\r\n进程执行相应操作，直到\r\n文件句柄关闭。</p>')),
    (b'<p>Sets extra flags for the <code>dwFileFlags</code> argument to the call to\r\n<a href="https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfile2"><code>CreateFile2</code></a> to the specified value (or combines it with\r\n<code>attributes</code> and <code>security_qos_flags</code> to set the <code>dwFlagsAndAttributes</code>\r\nfor <a href="https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea"><code>CreateFile</code></a>).</p>',
     E('<p>为调用 <a href="https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfile2"><code>CreateFile2</code></a> 时\r\n传递的 <code>dwFileFlags</code> 参数设置额外的标志（或者将其与\r\n<code>attributes</code> 和 <code>security_qos_flags</code> 组合，\r\n以为 <a href="https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea"><code>CreateFile</code></a> 设置 <code>dwFlagsAndAttributes</code>）。</p>')),
    (b'<p>Custom flags can only set flags, not remove flags set by Rust\xe2\x80\x99s options.\r\nThis option overwrites any previously set custom flags.</p>',
     E('<p>自定义标志只能设置标志，不能\r\n移除 Rust 选项设置的标志。\r\n此选项将覆盖任何先前设置的自定义标志。</p>')),
    (b'<p>Sets the <code>dwFileAttributes</code> argument to the call to <a href="https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfile2"><code>CreateFile2</code></a> to\r\nthe specified value (or combines it with <code>custom_flags</code> and\r\n<code>security_qos_flags</code> to set the <code>dwFlagsAndAttributes</code> for\r\n<a href="https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea"><code>CreateFile</code></a>).</p>',
     E('<p>为调用 <a href="https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfile2"><code>CreateFile2</code></a> 时\r\n传递的 <code>dwFileAttributes</code> 参数设置指定的值（或者将其与\r\n<code>custom_flags</code> 和 <code>security_qos_flags</code> 组合，\r\n以为 <a href="https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea"><code>CreateFile</code></a> 设置 <code>dwFlagsAndAttributes</code>）。</p>')),
    (b'<p>If a <em>new</em> file is created because it does not yet exist and\r\n<code>.create(true)</code> or <code>.create_new(true)</code> are specified, the new file is\r\ngiven the attributes declared with <code>.attributes()</code>.</p>',
     E('<p>如果因为文件尚不存在而创建了<em>新</em>文件，\r\n并且指定了 <code>.create(true)</code> 或 <code>.create_new(true)</code>，\r\n则新文件将获得使用 <code>.attributes()</code> 声明的属性。</p>')),
    (b'<p>If an <em>existing</em> file is opened with <code>.create(true).truncate(true)</code>, its\r\nexisting attributes are preserved and combined with the ones declared\r\nwith <code>.attributes()</code>.</p>',
     E('<p>如果使用 <code>.create(true).truncate(true)</code> 打开<em>已存在</em>的文件，\r\n则其现有属性将被保留，并与使用 <code>.attributes()</code> 声明的属性\r\n组合。</p>')),
    (b'<p>In all other cases the attributes get ignored.</p>',
     E('<p>在所有其他情况下，属性将被忽略。</p>')),
    (b'<p>Sets the <code>dwSecurityQosFlags</code> argument to the call to <a href="https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfile2"><code>CreateFile2</code></a> to\r\nthe specified value (or combines it with <code>custom_flags</code> and <code>attributes</code>\r\nto set the <code>dwFlagsAndAttributes</code> for <a href="https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea"><code>CreateFile</code></a>).</p>',
     E('<p>为调用 <a href="https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfile2"><code>CreateFile2</code></a> 时\r\n传递的 <code>dwSecurityQosFlags</code> 参数设置指定的值（或者将其与\r\n<code>custom_flags</code> 和 <code>attributes</code> 组合，\r\n以为 <a href="https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea"><code>CreateFile</code></a> 设置 <code>dwFlagsAndAttributes</code>）。</p>')),
    (b'<p>By default <code>security_qos_flags</code> is not set. It should be specified when\r\nopening a named pipe, to control to which degree a server process can\r\nact on behalf of a client process (security impersonation level).</p>',
     E('<p>默认情况下，未设置 <code>security_qos_flags</code>。\r\n在打开命名管道时应指定它，以控制服务器进程\r\n可以代表客户端进程（安全模拟级别）执行操作的程度。</p>')),
    (b'<p>When <code>security_qos_flags</code> is not set, a malicious program can gain the\r\nelevated privileges of a privileged Rust process when it allows opening\r\nuser-specified paths, by tricking it into opening a named pipe. So\r\narguably <code>security_qos_flags</code> should also be set when opening arbitrary\r\npaths. However the bits can then conflict with other flags, specifically\r\n<code>FILE_FLAG_OPEN_NO_RECALL</code>.</p>',
     E('<p>当未设置 <code>security_qos_flags</code> 时，恶意程序可以\r\n在允许打开用户指定路径时，通过\r\n诱骗特权 Rust 进程打开命名管道来获取\r\n提升的权限。因此，可以说在打开任意路径时，\r\n也应该设置 <code>security_qos_flags</code>。\r\n但这些位可能与其他标志（特别是\r\n<code>FILE_FLAG_OPEN_NO_RECALL</code>）冲突。</p>')),
    (b'<p>For information about possible values, see <a href="https://docs.microsoft.com/en-us/windows/win32/api/winnt/ne-winnt-security_impersonation_level">Impersonation Levels</a> on the\r\nWindows Dev Center site. The <code>SECURITY_SQOS_PRESENT</code> flag is set\r\nautomatically when using this method.</p>',
     E('<p>有关可能值的信息，请参阅 Windows 开发人员中心上的<a href="https://docs.microsoft.com/en-us/windows/win32/api/winnt/ne-winnt-security_impersonation_level">模拟级别</a>。\r\n使用此方法时，将自动设置 <code>SECURITY_SQOS_PRESENT</code> 标志。</p>')),
])


# ============================================================
# io/fn.copy_bidirectional_with_sizes.html
# ============================================================
add('io/fn.copy_bidirectional_with_sizes.html', [
    (b'<p>Copies data in both directions between <code>a</code> and <code>b</code> using buffers of the specified size.</p>',
     E('<p>使用指定大小的缓冲区在 <code>a</code> 和 <code>b</code> 之间双向复制数据。</p>')),
    (b'<p>This method is the same as the <a href="fn.copy_bidirectional.html" title="fn tokio::io::copy_bidirectional"><code>copy_bidirectional()</code></a>, except that it allows you to set the\r\nsize of the internal buffers used when copying data.</p>',
     E('<p>此方法与 <a href="fn.copy_bidirectional.html" title="fn tokio::io::copy_bidirectional"><code>copy_bidirectional()</code></a> 相同，只是它允许你设置\r\n复制数据时使用的内部缓冲区的大小。</p>')),
])


# ============================================================
# io/fn.copy_buf.html
# ============================================================
add('io/fn.copy_buf.html', [
    (b'<p>This function returns a future that will continuously read data from\r\n<code>reader</code> and then write it into <code>writer</code> in a streaming fashion until\r\n<code>reader</code> returns EOF or fails.</p>',
     E('<p>此函数返回一个 future，它将以流式方式持续从 <code>reader</code>\r\n读取数据，然后将其写入 <code>writer</code>，直到 <code>reader</code>\r\n返回 EOF 或失败。</p>')),
    (b'<p>This is a <a href="fn.copy.html" title="fn tokio::io::copy"><code>tokio::io::copy</code></a> alternative for <a href="trait.AsyncBufRead.html" title="trait tokio::io::AsyncBufRead"><code>AsyncBufRead</code></a> readers\r\nwith no extra buffer allocation, since <a href="trait.AsyncBufRead.html" title="trait tokio::io::AsyncBufRead"><code>AsyncBufRead</code></a> allow access\r\nto the reader\xe2\x80\x99s inner buffer.</p>',
     E('<p>这是针对 <a href="trait.AsyncBufRead.html" title="trait tokio::io::AsyncBufRead"><code>AsyncBufRead</code></a> 读取器的\r\n<a href="fn.copy.html" title="fn tokio::io::copy"><code>tokio::io::copy</code></a> 替代方案，且无需额外的\r\n缓冲区分配，因为 <a href="trait.AsyncBufRead.html" title="trait tokio::io::AsyncBufRead"><code>AsyncBufRead</code></a> 允许\r\n访问读取器的内部缓冲区。</p>')),
    (b'<p>If you are looking to use <a href="https://doc.rust-lang.org/1.95.0/std/io/copy/fn.copy.html" title="fn std::io::copy::copy"><code>std::io::copy</code></a> with a synchronous consumer\r\n(like a <code>hasher</code> or compressor), consider using async alternatives instead of\r\nwrapping the reader with <a href="https://docs.rs/tokio-util/latest/tokio_util/io/struct.SyncIoBridge.html"><code>SyncIoBridge</code></a>. See the <a href="https://docs.rs/tokio-util/latest/tokio_util/io/struct.SyncIoBridge.html"><code>SyncIoBridge</code></a>\r\ndocumentation for detailed examples and guidance on hashing, compression,\r\nand data parsing.</p>',
     E('<p>如果你希望将 <a href="https://doc.rust-lang.org/1.95.0/std/io/copy/fn.copy.html" title="fn std::io::copy::copy"><code>std::io::copy</code></a> 与同步消费者\r\n（如 <code>hasher</code> 或压缩器）一起使用，请考虑使用异步替代方案，\r\n而不是使用 <a href="https://docs.rs/tokio-util/latest/tokio_util/io/struct.SyncIoBridge.html"><code>SyncIoBridge</code></a> 包装读取器。有关哈希、压缩\r\n和数据解析的详细示例和指南，请参阅\r\n<a href="https://docs.rs/tokio-util/latest/tokio_util/io/struct.SyncIoBridge.html"><code>SyncIoBridge</code></a> 文档。</p>')),
    (b'<p>The returned future will finish with an error will return an error\r\nimmediately if any call to <code>poll_fill_buf</code> or <code>poll_write</code> returns an\r\nerror.</p>',
     E('<p>如果对 <code>poll_fill_buf</code> 或 <code>poll_write</code> 的任何调用返回错误，\r\n则返回的 future 将立即返回错误。</p>')),
])


# ============================================================
# io/fn.duplex.html
# ============================================================
add('io/fn.duplex.html', [
    (b'<p>Create a new pair of <code>DuplexStream</code>s that act like a pair of connected sockets.</p>',
     E('<p>创建一个新的 <code>DuplexStream</code> 对，其行为类似于一对已连接的 socket。</p>')),
    (b'<p>The <code>max_buf_size</code> argument is the maximum amount of bytes that can be\r\nwritten to a side before the write returns <code>Poll::Pending</code>.</p>',
     E('<p><code>max_buf_size</code> 参数是写入返回 <code>Poll::Pending</code>\r\n之前可写入一端的最大字节数。</p>')),
])


# ============================================================
# io/fn.empty.html
# ============================================================
add('io/fn.empty.html', [
    (b'<p>Creates a value that is always at EOF for reads, and ignores all data written.</p>',
     E('<p>创建一个读取时始终处于 EOF、写入时忽略所有数据的值。</p>')),
    (b'<p>All writes on the returned instance will return <code>Poll::Ready(Ok(buf.len()))</code>\r\nand the contents of the buffer will not be inspected.</p>',
     E('<p>对返回实例的所有写入都将返回 <code>Poll::Ready(Ok(buf.len()))</code>，\r\n并且不会检查缓冲区的内容。</p>')),
    (b'<p>All reads from the returned instance will return <code>Poll::Ready(Ok(0))</code>.</p>',
     E('<p>从返回实例的所有读取都将返回 <code>Poll::Ready(Ok(0))</code>。</p>')),
    (b'<p>This is an asynchronous version of <a href="https://doc.rust-lang.org/1.95.0/std/io/util/fn.empty.html" title="fn std::io::util::empty"><code>std::io::empty</code></a>.</p>',
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/io/util/fn.empty.html" title="fn std::io::util::empty"><code>std::io::empty</code></a> 的异步版本。</p>')),
    (b'<p>A slightly sad example of not reading anything into a buffer:</p>',
     E('<p>一个不太实用的"不向缓冲区读取任何内容"的示例：</p>')),
    (b'<p>A convoluted way of getting the length of a buffer:</p>',
     E('<p>一种获取缓冲区长度的迂回方式：</p>')),
])


# ============================================================
# io/fn.join.html
# ============================================================
add('io/fn.join.html', [
    (b'<p>Join two values implementing <code>AsyncRead</code> and <code>AsyncWrite</code> into a\r\nsingle handle.</p>',
     E('<p>将实现 <code>AsyncRead</code> 和 <code>AsyncWrite</code> 的两个值合并为\r\n单个句柄。</p>')),
])


# ============================================================
# io/fn.repeat.html
# ============================================================
add('io/fn.repeat.html', [
    (b'<p>Creates an instance of an async reader that infinitely repeats one byte.</p>',
     E('<p>创建一个无限重复单个字节的异步读取器实例。</p>')),
    (b'<p>All reads from this reader will succeed by filling the specified buffer with\r\nthe given byte.</p>',
     E('<p>从此读取器的所有读取都将通过使用\r\n给定字节填充指定的缓冲区来成功。</p>')),
    (b'<p>This is an asynchronous version of <a href="https://doc.rust-lang.org/1.95.0/std/io/util/fn.repeat.html" title="fn std::io::util::repeat"><code>std::io::repeat</code></a>.</p>',
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/io/util/fn.repeat.html" title="fn std::io::util::repeat"><code>std::io::repeat</code></a> 的异步版本。</p>')),
])


# ============================================================
# io/fn.simplex.html
# ============================================================
add('io/fn.simplex.html', [
    (b'<p>Creates unidirectional buffer that acts like in memory pipe.</p>',
     E('<p>创建一个单向缓冲区，其行为类似于内存管道。</p>')),
    (b'<p>The <code>max_buf_size</code> argument is the maximum amount of bytes that can be\r\nwritten to a buffer before the it returns <code>Poll::Pending</code>.</p>',
     E('<p><code>max_buf_size</code> 参数是在返回 <code>Poll::Pending</code>\r\n之前可写入缓冲区的最大字节数。</p>')),
    (b'<p>The reader and writer half can be unified into a single structure\r\nof <code>SimplexStream</code> that supports both reading and writing or\r\nthe <code>SimplexStream</code> can be already created as unified structure\r\nusing <a href="struct.SimplexStream.html#method.new_unsplit" title="associated function tokio::io::SimplexStream::new_unsplit"><code>SimplexStream::new_unsplit()</code></a>.</p>',
     E('<p>读端和写端可以统一为支持\r\n同时读写的单个 <code>SimplexStream</code> 结构，\r\n或者可以使用\r\n<a href="struct.SimplexStream.html#method.new_unsplit" title="associated function tokio::io::SimplexStream::new_unsplit"><code>SimplexStream::new_unsplit()</code></a>\r\n将 <code>SimplexStream</code> 创建为统一的结构。</p>')),
])


# ============================================================
# io/fn.sink.html
# ============================================================
add('io/fn.sink.html', [
    (b'<p>Creates an instance of an async writer which will successfully consume all\r\ndata.</p>',
     E('<p>创建一个异步写入器实例，它将成功消费所有\r\n数据。</p>')),
    (b'<p>All calls to <a href="trait.AsyncWrite.html#tymethod.poll_write" title="method tokio::io::AsyncWrite::poll_write"><code>poll_write</code></a> on the returned instance will return\r\n<code>Poll::Ready(Ok(buf.len()))</code> and the contents of the buffer will not be\r\ninspected.</p>',
     E('<p>对返回实例的所有 <a href="trait.AsyncWrite.html#tymethod.poll_write" title="method tokio::io::AsyncWrite::poll_write"><code>poll_write</code></a> 调用都将返回\r\n<code>Poll::Ready(Ok(buf.len()))</code>，并且\r\n不会检查缓冲区的内容。</p>')),
    (b'<p>This is an asynchronous version of <a href="https://doc.rust-lang.org/1.95.0/std/io/util/fn.sink.html" title="fn std::io::util::sink"><code>std::io::sink</code></a>.</p>',
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/io/util/fn.sink.html" title="fn std::io::util::sink"><code>std::io::sink</code></a> 的异步版本。</p>')),
])


# ============================================================
# io/fn.split.html
# ============================================================
add('io/fn.split.html', [
    (b'<p>Splits a single value implementing <code>AsyncRead + AsyncWrite</code> into separate\r\n<code>AsyncRead</code> and <code>AsyncWrite</code> handles.</p>',
     E('<p>将实现 <code>AsyncRead + AsyncWrite</code> 的单个值拆分为\r\n独立的 <code>AsyncRead</code> 和 <code>AsyncWrite</code> 句柄。</p>')),
    (b'<p>To restore this read/write object from its <code>ReadHalf</code> and\r\n<code>WriteHalf</code> use <a href="struct.ReadHalf.html#method.unsplit" title="method tokio::io::ReadHalf::unsplit"><code>unsplit</code></a>.</p>',
     E('<p>要从其 <code>ReadHalf</code> 和\r\n<code>WriteHalf</code> 恢复此读/写对象，请使用\r\n<a href="struct.ReadHalf.html#method.unsplit" title="method tokio::io::ReadHalf::unsplit"><code>unsplit</code></a>。</p>')),
])


# ============================================================
# io/fn.stderr.html
# ============================================================
add('io/fn.stderr.html', [
    (b'<p>Constructs a new handle to the standard error of the current process.</p>',
     E('<p>构造一个到当前进程标准错误的新句柄。</p>')),
    (b'<p>The returned handle allows writing to standard error from the within the\r\nTokio runtime.</p>',
     E('<p>返回的句柄允许在 Tokio\r\n运行时内写入标准错误。</p>')),
    (b'<p>Concurrent writes to stderr must be executed with care: Only individual\r\nwrites to this <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> are guaranteed to be intact. In particular\r\nyou should be aware that writes using <a href="trait.AsyncWriteExt.html#method.write_all" title="method tokio::io::AsyncWriteExt::write_all"><code>write_all</code></a> are not guaranteed\r\nto occur as a single write, so multiple threads writing data with\r\n<a href="trait.AsyncWriteExt.html#method.write_all" title="method tokio::io::AsyncWriteExt::write_all"><code>write_all</code></a> may result in interleaved output.</p>',
     E('<p>对 stderr 的并发写入必须谨慎执行：只有对此 <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a>\r\n的单个写入才能保证完整。特别是请注意，使用\r\n<a href="trait.AsyncWriteExt.html#method.write_all" title="method tokio::io::AsyncWriteExt::write_all"><code>write_all</code></a> 进行\r\n写入时不能保证作为单次写入完成，因此多个线程使用\r\n<a href="trait.AsyncWriteExt.html#method.write_all" title="method tokio::io::AsyncWriteExt::write_all"><code>write_all</code></a> 写入数据\r\n可能会导致输出交错。</p>')),
    (b'<p>Note that unlike <a href="https://doc.rust-lang.org/1.95.0/std/io/stdio/fn.stderr.html" title="fn std::io::stdio::stderr"><code>std::io::stderr</code></a>, each call to this <code>stderr()</code>\r\nproduces a new writer, so for example, this program does <strong>not</strong> flush stderr:</p>',
     E('<p>请注意，与 <a href="https://doc.rust-lang.org/1.95.0/std/io/stdio/fn.stderr.html" title="fn std::io::stdio::stderr"><code>std::io::stderr</code></a> 不同，对 <code>stderr()</code>\r\n的每次调用都会产生一个新的 writer，例如，此程序<strong>不</strong>会\r\n刷新 stderr：</p>')),
])


# ============================================================
# io/fn.stdin.html
# ============================================================
add('io/fn.stdin.html', [
    (b'<p>Constructs a new handle to the standard input of the current process.</p>',
     E('<p>构造一个到当前进程标准输入的新句柄。</p>')),
    (b'<p>This handle is best used for non-interactive uses, such as when a file\r\nis piped into the application. For technical reasons, <code>stdin</code> is\r\nimplemented by using an ordinary blocking read on a separate thread, and\r\nit is impossible to cancel that read. This can make shutdown of the\r\nruntime hang until the user presses enter.</p>',
     E('<p>此句柄最适合用于非交互式用途，例如当文件\r\n通过管道传入应用程序时。出于技术原因，<code>stdin</code>\r\n通过在单独的线程上使用普通的阻塞读取实现，\r\n并且无法取消该读取。这可能导致运行时\r\n关闭挂起，直到用户按下回车键。</p>')),
])


# ============================================================
# io/fn.stdout.html
# ============================================================
add('io/fn.stdout.html', [
    (b'<p>Constructs a new handle to the standard output of the current process.</p>',
     E('<p>构造一个到当前进程标准输出的新句柄。</p>')),
    (b'<p>The returned handle allows writing to standard out from the within the\r\nTokio runtime.</p>',
     E('<p>返回的句柄允许在 Tokio\r\n运行时内写入标准输出。</p>')),
    (b'<p>Concurrent writes to stdout must be executed with care: Only individual\r\nwrites to this <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> are guaranteed to be intact. In particular\r\nyou should be aware that writes using <a href="trait.AsyncWriteExt.html#method.write_all" title="method tokio::io::AsyncWriteExt::write_all"><code>write_all</code></a> are not guaranteed\r\nto occur as a single write, so multiple threads writing data with\r\n<a href="trait.AsyncWriteExt.html#method.write_all" title="method tokio::io::AsyncWriteExt::write_all"><code>write_all</code></a> may result in interleaved output.</p>',
     E('<p>对 stdout 的并发写入必须谨慎执行：只有对此 <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a>\r\n的单个写入才能保证完整。特别是请注意，使用\r\n<a href="trait.AsyncWriteExt.html#method.write_all" title="method tokio::io::AsyncWriteExt::write_all"><code>write_all</code></a> 进行\r\n写入时不能保证作为单次写入完成，因此多个线程使用\r\n<a href="trait.AsyncWriteExt.html#method.write_all" title="method tokio::io::AsyncWriteExt::write_all"><code>write_all</code></a> 写入数据\r\n可能会导致输出交错。</p>')),
    (b'<p>Note that unlike <a href="https://doc.rust-lang.org/1.95.0/std/io/stdio/fn.stdout.html" title="fn std::io::stdio::stdout"><code>std::io::stdout</code></a>, each call to this <code>stdout()</code>\r\nproduces a new writer, so for example, this program does <strong>not</strong> flush stdout:</p>',
     E('<p>请注意，与 <a href="https://doc.rust-lang.org/1.95.0/std/io/stdio/fn.stdout.html" title="fn std::io::stdio::stdout"><code>std::io::stdout</code></a> 不同，对 <code>stdout()</code>\r\n的每次调用都会产生一个新的 writer，例如，此程序<strong>不</strong>会\r\n刷新 stdout：</p>')),
    (b'<p>The following is an example of using <code>stdio</code> with loop.</p>',
     E('<p>以下是使用循环使用 <code>stdio</code> 的示例。</p>')),
])


# ============================================================
# io/struct.BufReader.html
# ============================================================
add('io/struct.BufReader.html', [
    (b'<p>It can be excessively inefficient to work directly with a <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a>\r\ninstance. A <code>BufReader</code> performs large, infrequent reads on the underlying\r\n<a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> and maintains an in-memory buffer of the results.</p>',
     E('<p>直接使用 <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> 实例\r\n可能效率极低。<code>BufReader</code> 对底层\r\n<a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> 执行少量大块读取，\r\n并在内存中维护结果的缓冲区。</p>')),
    (b'<p><code>BufReader</code> can improve the speed of programs that make <em>small</em> and\r\n<em>repeated</em> read calls to the same file or network socket. It does not\r\nhelp when reading very large amounts at once, or reading just one or a few\r\ntimes. It also provides no advantage when reading from a source that is\r\nalready in memory, like a <code>Vec&lt;u8&gt;</code>.</p>',
     E('<p><code>BufReader</code> 可以提升对同一文件或网络 socket\r\n进行<em>小</em>型<em>重复</em>读取调用的程序的速度。\r\n它在一次读取大量数据时没有帮助，\r\n或者只读取一两次时也没有帮助。\r\n当从内存中已存在的数据源（如 <code>Vec&lt;u8&gt;</code>）\r\n读取时，它也没有优势。</p>')),
    (b'<p>When the <code>BufReader</code> is dropped, the contents of its buffer will be\r\ndiscarded. Creating multiple instances of a <code>BufReader</code> on the same\r\nstream can cause data loss.</p>',
     E('<p>当 <code>BufReader</code> 被丢弃时，其缓冲区的内容将被\r\n丢弃。在同一\r\n流上创建多个 <code>BufReader</code> 实例可能会导致数据丢失。</p>')),
    (b'<p>Consumes this <code>BufReader</code>, returning the underlying reader.</p>',
     E('<p>消费此 <code>BufReader</code>，返回底层读取器。</p>')),
    (b'<p>The position used for seeking with <code>SeekFrom::Current(_)</code> is the\r\nposition the underlying reader would be at if the <code>BufReader</code> had no\r\ninternal buffer.</p>',
     E('<p>使用 <code>SeekFrom::Current(_)</code> 进行 seek 所使用的位置\r\n是底层读取器在没有\r\n<code>BufReader</code> 内部缓冲区时所处的位置。</p>')),
    (b'<p>Seeking always discards the internal buffer, even if the seek position\r\nwould otherwise fall within it. This guarantees that calling\r\n<code>.into_inner()</code> immediately after a seek yields the underlying reader\r\nat the same position.</p>',
     E('<p>seek 始终会丢弃内部缓冲区，即使 seek 位置\r\n原本落在该缓冲区内。这保证了在 seek\r\n之后立即调用 <code>.into_inner()</code> 会返回处于\r\n相同位置的底层读取器。</p>')),
    (b'<p>See <a href="trait.AsyncSeek.html" title="trait tokio::io::AsyncSeek"><code>AsyncSeek</code></a> for more details.</p>',
     E('<p>有关更多详细信息，请参阅 <a href="trait.AsyncSeek.html" title="trait tokio::io::AsyncSeek"><code>AsyncSeek</code></a>。</p>')),
    (b'<p>Note: In the edge case where you\xe2\x80\x99re seeking with <code>SeekFrom::Current(n)</code>\r\nwhere <code>n</code> minus the internal buffer length overflows an <code>i64</code>, two\r\nseeks will be performed instead of one. If the second seek returns\r\n<code>Err</code>, the underlying reader will be left at the same position it would\r\nhave if you called <code>seek</code> with <code>SeekFrom::Current(0)</code>.</p>',
     E('<p>注意：在你使用 <code>SeekFrom::Current(n)</code>\r\n进行 seek 且 <code>n</code> 减去内部缓冲区长度会溢出 <code>i64</code> 的极端情况下，\r\n将执行两次 seek 而不是一次。如果第二次 seek 返回\r\n<code>Err</code>，则底层读取器将保持在\r\n你使用 <code>SeekFrom::Current(0)</code> 调用 <code>seek</code> 时所处的位置。</p>')),
])


# ============================================================
# io/struct.BufStream.html
# ============================================================
add('io/struct.BufStream.html', [
    (b'<p>Wraps a type that is <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> and <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a>, and buffers its input and output.</p>',
     E('<p>封装一个同时实现 <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> 和 <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> 的类型，\r\n并缓冲其输入和输出。</p>')),
    (b'<p>It can be excessively inefficient to work directly with something that implements <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a>\r\nand <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a>. For example, every <code>write</code>, however small, has to traverse the syscall\r\ninterface, and similarly, every read has to do the same. The <a href="struct.BufWriter.html" title="struct tokio::io::BufWriter"><code>BufWriter</code></a> and <a href="struct.BufReader.html" title="struct tokio::io::BufReader"><code>BufReader</code></a>\r\ntypes aid with these problems respectively, but do so in only one direction. <code>BufStream</code> wraps\r\none in the other so that both directions are buffered. See their documentation for details.</p>',
     E('<p>直接使用实现 <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a>\r\n和 <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> 的东西可能效率极低。\r\n例如，每次 <code>write</code>（无论多小）都必须穿越 syscall 接口，\r\n每次读取也是如此。<a href="struct.BufWriter.html" title="struct tokio::io::BufWriter"><code>BufWriter</code></a> 和\r\n<a href="struct.BufReader.html" title="struct tokio::io::BufReader"><code>BufReader</code></a>\r\n类型分别有助于解决这些问题，但只在单个方向上起作用。\r\n<code>BufStream</code> 将一个包装在另一个内，从而双向都得到缓冲。\r\n有关细节，请参阅其文档。</p>')),
    (b'<p>Consumes this <code>BufStream</code>, returning the underlying I/O object.</p>',
     E('<p>消费此 <code>BufStream</code>，返回底层的 I/O 对象。</p>')),
    (b'<p>The position used for seeking with <code>SeekFrom::Current(_)</code> is the\r\nposition the underlying stream would be at if the <code>BufStream</code> had no\r\ninternal buffer.</p>',
     E('<p>使用 <code>SeekFrom::Current(_)</code> 进行 seek 所使用的位置\r\n是底层流在没有\r\n<code>BufStream</code> 内部缓冲区时所处的位置。</p>')),
    (b'<p>Seeking always discards the internal buffer, even if the seek position\r\nwould otherwise fall within it. This guarantees that calling\r\n<code>.into_inner()</code> immediately after a seek yields the underlying reader\r\nat the same position.</p>',
     E('<p>seek 始终会丢弃内部缓冲区，即使 seek 位置\r\n原本落在该缓冲区内。这保证了在 seek\r\n之后立即调用 <code>.into_inner()</code> 会返回处于\r\n相同位置的底层读取器。</p>')),
    (b'<p>See <a href="trait.AsyncSeek.html" title="trait tokio::io::AsyncSeek"><code>AsyncSeek</code></a> for more details.</p>',
     E('<p>有关更多详细信息，请参阅 <a href="trait.AsyncSeek.html" title="trait tokio::io::AsyncSeek"><code>AsyncSeek</code></a>。</p>')),
    (b'<p>Note: In the edge case where you\xe2\x80\x99re seeking with <code>SeekFrom::Current(n)</code>\r\nwhere <code>n</code> minus the internal buffer length overflows an <code>i64</code>, two\r\nseeks will be performed instead of one. If the second seek returns\r\n<code>Err</code>, the underlying reader will be left at the same position it would\r\nhave if you called <code>seek</code> with <code>SeekFrom::Current(0)</code>.</p>',
     E('<p>注意：在你使用 <code>SeekFrom::Current(n)</code>\r\n进行 seek 且 <code>n</code> 减去内部缓冲区长度会溢出 <code>i64</code> 的极端情况下，\r\n将执行两次 seek 而不是一次。如果第二次 seek 返回\r\n<code>Err</code>，则底层读取器将保持在\r\n你使用 <code>SeekFrom::Current(0)</code> 调用 <code>seek</code> 时所处的位置。</p>')),
])


# ============================================================
# io/struct.BufWriter.html
# ============================================================
add('io/struct.BufWriter.html', [
    (b'<p>Wraps a writer and buffers its output.</p>',
     E('<p>包装一个 writer 并缓冲其输出。</p>')),
])


# ============================================================
# io/struct.BufWriter.html (more)
# ============================================================
add('io/struct.BufWriter.html', [
    (b'<p>It can be excessively inefficient to work directly with something that\r\nimplements <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a>. A <code>BufWriter</code> keeps an in-memory buffer of data and\r\nwrites it to an underlying writer in large, infrequent batches.</p>',
     E('<p>直接使用实现\r\n<a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> 的东西可能效率极低。<code>BufWriter</code> 在内存中维护数据缓冲区，\r\n并以少量大块的形式将数据写入底层 writer。</p>')),
    (b'<p><code>BufWriter</code> can improve the speed of programs that make <em>small</em> and\r\n<em>repeated</em> write calls to the same file or network socket. It does not\r\nhelp when writing very large amounts at once, or writing just one or a few\r\ntimes. It also provides no advantage when writing to a destination that is\r\nin memory, like a <code>Vec&lt;u8&gt;</code>.</p>',
     E('<p><code>BufWriter</code> 可以提升对同一文件或网络 socket\r\n进行<em>小</em>型<em>重复</em>写入调用的程序的速度。\r\n它在一次写入大量数据时没有帮助，\r\n或者只写入一两次时也没有帮助。\r\n当写入内存中的目标（如 <code>Vec&lt;u8&gt;</code>）\r\n时，它也没有优势。</p>')),
    (b'<p>When the <code>BufWriter</code> is dropped, the contents of its buffer will be\r\ndiscarded. Creating multiple instances of a <code>BufWriter</code> on the same\r\nstream can cause data loss. If you need to write out the contents of its\r\nbuffer, you must manually call flush before the writer is dropped.</p>',
     E('<p>当 <code>BufWriter</code> 被丢弃时，其缓冲区的内容将被\r\n丢弃。在同一\r\n流上创建多个 <code>BufWriter</code> 实例可能会导致数据丢失。\r\n如果需要写出其缓冲区的内容，必须在 writer 丢弃之前\r\n手动调用 flush。</p>')),
    (b'<p>Consumes this <code>BufWriter</code>, returning the underlying writer.</p>',
     E('<p>消费此 <code>BufWriter</code>，返回底层 writer。</p>')),
])


# ============================================================
# io/struct.Chain.html
# ============================================================
add('io/struct.Chain.html', [
    (b'<p>Stream for the <a href="trait.AsyncReadExt.html#method.chain" title="method tokio::io::AsyncReadExt::chain"><code>chain</code></a> method.</p>',
     E('<p>用于 <a href="trait.AsyncReadExt.html#method.chain" title="method tokio::io::AsyncReadExt::chain"><code>chain</code></a> 方法的流。</p>')),
])


# ============================================================
# io/struct.DuplexStream.html
# ============================================================
add('io/struct.DuplexStream.html', [
    (b'<p>A bidirectional pipe to read and write bytes in memory.</p>',
     E('<p>用于在内存中读写字节的双向管道。</p>')),
    (b'<p>A pair of <code>DuplexStream</code>s are created together, and they act as a \xe2\x80\x9cchannel\xe2\x80\x9d\r\nthat can be used as in-memory IO types. Writing to one of the pairs will\r\nallow that data to be read from the other, and vice versa.</p>',
     E('<p>一对 <code>DuplexStream</code> 同时创建，它们充当\xe2\x80\x9c信道\xe2\x80\x9d，\r\n可用作内存中的 IO 类型。写入对中的一端\r\n将允许从另一端读取该数据，反之亦然。</p>')),
    (b'<p>If one end of the <code>DuplexStream</code> channel is dropped, any pending reads on\r\nthe other side will continue to read data until the buffer is drained, then\r\nthey will signal EOF by returning 0 bytes. Any writes to the other side,\r\nincluding pending ones (that are waiting for free space in the buffer) will\r\nreturn <code>Err(BrokenPipe)</code> immediately.</p>',
     E('<p>如果 <code>DuplexStream</code> 信道的一端被丢弃，\r\n另一端的任何挂起读取将继续读取数据直到缓冲区被排空，\r\n然后它们将通过返回 0 字节来表示 EOF。\r\n对另一端的任何写入，包括\r\n挂起的写入（正在等待缓冲区中的空闲空间），\r\n将立即返回 <code>Err(BrokenPipe)</code>。</p>')),
])


# ============================================================
# io/struct.Empty.html
# ============================================================
add('io/struct.Empty.html', [
    (b'<p><code>Empty</code> ignores any data written via <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a>, and will always be empty\r\n(returning zero bytes) when read via <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a>.</p>',
     E('<p><code>Empty</code> 忽略通过 <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> 写入的任何数据，\r\n并且在通过 <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> 读取时始终为空\r\n（返回零字节）。</p>')),
    (b'<p>This struct is generally created by calling <a href="fn.empty.html" title="fn tokio::io::empty"><code>empty</code></a>. Please see\r\nthe documentation of <a href="fn.empty.html" title="fn tokio::io::empty"><code>empty()</code></a> for more details.</p>',
     E('<p>此结构体通常通过调用 <a href="fn.empty.html" title="fn tokio::io::empty"><code>empty</code></a> 创建。有关更多详细信息，\r\n请参阅 <a href="fn.empty.html" title="fn tokio::io::empty"><code>empty()</code></a> 的文档。</p>')),
    (b'<p>This is an asynchronous version of <a href="https://doc.rust-lang.org/1.95.0/std/io/util/fn.empty.html" title="fn std::io::util::empty"><code>std::io::empty</code></a>.</p>',
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/io/util/fn.empty.html" title="fn std::io::util::empty"><code>std::io::empty</code></a> 的异步版本。</p>')),
])


# ============================================================
# io/struct.Join.html
# ============================================================
add('io/struct.Join.html', [
    (b'<p>Joins two values implementing <code>AsyncRead</code> and <code>AsyncWrite</code> into a\r\nsingle handle.</p>',
     E('<p>将实现 <code>AsyncRead</code> 和 <code>AsyncWrite</code> 的两个值合并为\r\n单个句柄。</p>')),
])


# ============================================================
# io/struct.Lines.html
# ============================================================
add('io/struct.Lines.html', [
    (b'<p>Reads lines from an <a href="trait.AsyncBufRead.html" title="trait tokio::io::AsyncBufRead"><code>AsyncBufRead</code></a>.</p>',
     E('<p>从 <a href="trait.AsyncBufRead.html" title="trait tokio::io::AsyncBufRead"><code>AsyncBufRead</code></a> 读取行。</p>')),
    (b'<p>A <code>Lines</code> can be turned into a <code>Stream</code> with <a href="https://docs.rs/tokio-stream/0.1/tokio_stream/wrappers/struct.LinesStream.html"><code>LinesStream</code></a>.</p>',
     E('<p>可以使用 <a href="https://docs.rs/tokio-stream/0.1/tokio_stream/wrappers/struct.LinesStream.html"><code>LinesStream</code></a> 将 <code>Lines</code> 转换为 <code>Stream</code>。</p>')),
    (b'<p>This type is usually created using the <a href="trait.AsyncBufReadExt.html#method.lines" title="method tokio::io::AsyncBufReadExt::lines"><code>lines</code></a> method.</p>',
     E('<p>此类型通常使用 <a href="trait.AsyncBufReadExt.html#method.lines" title="method tokio::io::AsyncBufReadExt::lines"><code>lines</code></a> 方法创建。</p>')),
    (b'<p>When the method returns <code>Poll::Pending</code>, the <code>Waker</code> in the provided\r\n<code>Context</code> is scheduled to receive a wakeup when more bytes become\r\navailable on the underlying IO resource.  Note that on multiple calls to\r\n<code>poll_next_line</code>, only the <code>Waker</code> from the <code>Context</code> passed to the most\r\nrecent call is scheduled to receive a wakeup.</p>',
     E('<p>当该方法返回 <code>Poll::Pending</code> 时，提供的\r\n<code>Context</code> 中的 <code>Waker</code> 被安排为在底层 IO 资源上有更多\r\n字节可用时接收唤醒。请注意，对于多次调用\r\n<code>poll_next_line</code>，只有传递给最近一次调用的 <code>Context</code> 中的 <code>Waker</code> 才会\r\n被安排接收唤醒。</p>')),
])


# ============================================================
# io/struct.ReadHalf.html
# ============================================================
add('io/struct.ReadHalf.html', [
    (b'<p>The readable half of a value returned from <a href="fn.split.html" title="fn tokio::io::split"><code>split</code></a>.</p>',
     E('<p>由 <a href="fn.split.html" title="fn tokio::io::split"><code>split</code></a> 返回的值的可读半部分。</p>')),
    (b'<p>If this <code>ReadHalf</code> and the given <code>WriteHalf</code> do not originate from the same\r\n<code>split</code> operation this method will panic.\r\nThis can be checked ahead of time by calling <a href="struct.ReadHalf.html#method.is_pair_of" title="method tokio::io::ReadHalf::is_pair_of"><code>is_pair_of()</code></a>.</p>',
     E('<p>如果此 <code>ReadHalf</code> 和给定的 <code>WriteHalf</code> 不是源自\r\n同一个 <code>split</code> 操作，则此方法\r\n会 panic。可以\r\n通过调用 <a href="struct.ReadHalf.html#method.is_pair_of" title="method tokio::io::ReadHalf::is_pair_of"><code>is_pair_of()</code></a> 提前检查这一点。</p>')),
])


# ============================================================
# io/struct.Repeat.html
# ============================================================
add('io/struct.Repeat.html', [
    (b'<p>An async reader which yields one byte over and over and over and over and\r\nover and\xe2\x80\xa6</p>',
     E('<p>一个反复产生一个字节又又一个字节\r\n又又一个字节的异步读取器\xe2\x80\xa6</p>')),
    (b'<p>This struct is generally created by calling <a href="fn.repeat.html" title="fn tokio::io::repeat"><code>repeat</code></a>. Please\r\nsee the documentation of <code>repeat()</code> for more details.</p>',
     E('<p>此结构体通常通过调用 <a href="fn.repeat.html" title="fn tokio::io::repeat"><code>repeat</code></a> 创建。\r\n有关更多详细信息，请参阅 <code>repeat()</code> 的文档。</p>')),
    (b'<p>This is an asynchronous version of <a href="https://doc.rust-lang.org/1.95.0/std/io/util/struct.Repeat.html" title="struct std::io::util::Repeat"><code>std::io::Repeat</code></a>.</p>',
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/io/util/struct.Repeat.html" title="struct std::io::util::Repeat"><code>std::io::Repeat</code></a> 的异步版本。</p>')),
])


# ============================================================
# io/struct.Sink.html
# ============================================================
add('io/struct.Sink.html', [
    (b'<p>An async writer which will move data into the void.</p>',
     E('<p>一个将数据移入虚无的异步 writer。</p>')),
    (b'<p>This struct is generally created by calling <a href="fn.sink.html" title="fn tokio::io::sink"><code>sink</code></a>. Please\r\nsee the documentation of <code>sink()</code> for more details.</p>',
     E('<p>此结构体通常通过调用 <a href="fn.sink.html" title="fn tokio::io::sink"><code>sink</code></a> 创建。\r\n有关更多详细信息，请参阅 <code>sink()</code> 的文档。</p>')),
    (b'<p>This is an asynchronous version of <a href="https://doc.rust-lang.org/1.95.0/std/io/util/struct.Sink.html" title="struct std::io::util::Sink"><code>std::io::Sink</code></a>.</p>',
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/io/util/struct.Sink.html" title="struct std::io::util::Sink"><code>std::io::Sink</code></a> 的异步版本。</p>')),
])


# ============================================================
# io/struct.Split.html
# ============================================================
add('io/struct.Split.html', [
    (b'<p>Splitter for the <a href="trait.AsyncBufReadExt.html#method.split" title="method tokio::io::AsyncBufReadExt::split"><code>split</code></a> method.</p>',
     E('<p>用于 <a href="trait.AsyncBufReadExt.html#method.split" title="method tokio::io::AsyncBufReadExt::split"><code>split</code></a> 方法的分割器。</p>')),
    (b'<p>A <code>Split</code> can be turned into a <code>Stream</code> with <a href="https://docs.rs/tokio-stream/0.1/tokio_stream/wrappers/struct.SplitStream.html"><code>SplitStream</code></a>.</p>',
     E('<p>可以使用 <a href="https://docs.rs/tokio-stream/0.1/tokio_stream/wrappers/struct.SplitStream.html"><code>SplitStream</code></a> 将 <code>Split</code> 转换为 <code>Stream</code>。</p>')),
    (b'<p>When the method returns <code>Poll::Pending</code>, the <code>Waker</code> in the provided\r\n<code>Context</code> is scheduled to receive a wakeup when more bytes become\r\navailable on the underlying IO resource.</p>',
     E('<p>当该方法返回 <code>Poll::Pending</code> 时，提供的\r\n<code>Context</code> 中的 <code>Waker</code> 被安排为在底层 IO 资源上有更多字节可用时接收唤醒。</p>')),
    (b'<p>Note that on multiple calls to <code>poll_next_segment</code>, only the <code>Waker</code>\r\nfrom the <code>Context</code> passed to the most recent call is scheduled to\r\nreceive a wakeup.</p>',
     E('<p>请注意，对于多次调用 <code>poll_next_segment</code>，\r\n只有传递给最近一次调用的 <code>Context</code> 中的 <code>Waker</code> 才会\r\n被安排接收唤醒。</p>')),
])


# ============================================================
# io/struct.Stderr.html
# ============================================================
add('io/struct.Stderr.html', [
    (b'<p>A handle to the standard error stream of a process.</p>',
     E('<p>进程标准错误流的句柄。</p>')),
    (b'<p>Concurrent writes to stderr must be executed with care: Only individual\r\nwrites to this <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> are guaranteed to be intact. In particular\r\nyou should be aware that writes using <a href="trait.AsyncWriteExt.html#method.write_all" title="method tokio::io::AsyncWriteExt::write_all"><code>write_all</code></a> are not guaranteed\r\nto occur as a single write, so multiple threads writing data with\r\n<a href="trait.AsyncWriteExt.html#method.write_all" title="method tokio::io::AsyncWriteExt::write_all"><code>write_all</code></a> may result in interleaved output.</p>',
     E('<p>对 stderr 的并发写入必须谨慎执行：只有对此 <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a>\r\n的单个写入才能保证完整。特别是请注意，使用\r\n<a href="trait.AsyncWriteExt.html#method.write_all" title="method tokio::io::AsyncWriteExt::write_all"><code>write_all</code></a> 进行\r\n写入时不能保证作为单次写入完成，因此多个线程使用\r\n<a href="trait.AsyncWriteExt.html#method.write_all" title="method tokio::io::AsyncWriteExt::write_all"><code>write_all</code></a> 写入数据\r\n可能会导致输出交错。</p>')),
    (b'<p>Created by the <a href="fn.stderr.html" title="fn tokio::io::stderr"><code>stderr</code></a> function.</p>',
     E('<p>由 <a href="fn.stderr.html" title="fn tokio::io::stderr"><code>stderr</code></a> 函数创建。</p>')),
])


# ============================================================
# io/struct.Stdin.html
# ============================================================
add('io/struct.Stdin.html', [
    (b'<p>A handle to the standard input stream of a process.</p>',
     E('<p>进程标准输入流的句柄。</p>')),
    (b'<p>The handle implements the <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> trait, but beware that concurrent\r\nreads of <code>Stdin</code> must be executed with care.</p>',
     E('<p>该句柄实现 <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> trait，但请注意\r\n必须谨慎执行对 <code>Stdin</code> 的并发读取。</p>')),
    (b'<p>This handle is best used for non-interactive uses, such as when a file\r\nis piped into the application. For technical reasons, <code>stdin</code> is\r\nimplemented by using an ordinary blocking read on a separate thread, and\r\nit is impossible to cancel that read. This can make shutdown of the\r\nruntime hang until the user presses enter.</p>',
     E('<p>此句柄最适合用于非交互式用途，例如当文件\r\n通过管道传入应用程序时。出于技术原因，<code>stdin</code>\r\n通过在单独的线程上使用普通的阻塞读取实现，\r\n并且无法取消该读取。这可能导致运行时\r\n关闭挂起，直到用户按下回车键。</p>')),
    (b'<p>Created by the <a href="fn.stdin.html" title="fn tokio::io::stdin"><code>stdin</code></a> function.</p>',
     E('<p>由 <a href="fn.stdin.html" title="fn tokio::io::stdin"><code>stdin</code></a> 函数创建。</p>')),
])


# ============================================================
# io/struct.Stdout.html
# ============================================================
add('io/struct.Stdout.html', [
    (b'<p>A handle to the standard output stream of a process.</p>',
     E('<p>进程标准输出流的句柄。</p>')),
    (b'<p>Concurrent writes to stdout must be executed with care: Only individual\r\nwrites to this <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> are guaranteed to be intact. In particular\r\nyou should be aware that writes using <a href="trait.AsyncWriteExt.html#method.write_all" title="method tokio::io::AsyncWriteExt::write_all"><code>write_all</code></a> are not guaranteed\r\nto occur as a single write, so multiple threads writing data with\r\n<a href="trait.AsyncWriteExt.html#method.write_all" title="method tokio::io::AsyncWriteExt::write_all"><code>write_all</code></a> may result in interleaved output.</p>',
     E('<p>对 stdout 的并发写入必须谨慎执行：只有对此 <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a>\r\n的单个写入才能保证完整。特别是请注意，使用\r\n<a href="trait.AsyncWriteExt.html#method.write_all" title="method tokio::io::AsyncWriteExt::write_all"><code>write_all</code></a> 进行\r\n写入时不能保证作为单次写入完成，因此多个线程使用\r\n<a href="trait.AsyncWriteExt.html#method.write_all" title="method tokio::io::AsyncWriteExt::write_all"><code>write_all</code></a> 写入数据\r\n可能会导致输出交错。</p>')),
    (b'<p>Created by the <a href="fn.stdout.html" title="fn tokio::io::stdout"><code>stdout</code></a> function.</p>',
     E('<p>由 <a href="fn.stdout.html" title="fn tokio::io::stdout"><code>stdout</code></a> 函数创建。</p>')),
    (b'<p>The following is an example of using <code>stdio</code> with loop.</p>',
     E('<p>以下是使用循环使用 <code>stdio</code> 的示例。</p>')),
])


# ============================================================
# io/struct.Take.html
# ============================================================
add('io/struct.Take.html', [
    (b'<p>Stream for the <a href="trait.AsyncReadExt.html#method.take" title="method tokio::io::AsyncReadExt::take"><code>take</code></a> method.</p>',
     E('<p>用于 <a href="trait.AsyncReadExt.html#method.take" title="method tokio::io::AsyncReadExt::take"><code>take</code></a> 方法的流。</p>')),
    (b'<p>This instance may reach <code>EOF</code> after reading fewer bytes than indicated by\r\nthis method if the underlying <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> instance reaches EOF.</p>',
     E('<p>如果底层的 <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> 实例到达 EOF，则此实例可能在读取少于\r\n此方法指示的字节数之后到达 <code>EOF</code>。</p>')),
])


# ============================================================
# io/struct.WriteHalf.html
# ============================================================
add('io/struct.WriteHalf.html', [
    (b'<p>The writable half of a value returned from <a href="fn.split.html" title="fn tokio::io::split"><code>split</code></a>.</p>',
     E('<p>由 <a href="fn.split.html" title="fn tokio::io::split"><code>split</code></a> 返回的值的可写半部分。</p>')),
])


# ============================================================
# io/trait.AsyncReadExt.html
# ============================================================
add('io/trait.AsyncReadExt.html', [
    (b'<p>Implemented as an extension trait, adding utility methods to all\r\n<a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> types. Callers will tend to import this trait instead of\r\n<a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a>.</p>',
     E('<p>作为扩展 trait 实现，向所有 <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> 类型添加实用方法。\r\n调用者通常会导入此 trait 而不是 <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a>。</p>')),
    (b'<p>See <a href="index.html" title="mod tokio::io">module</a> documentation for more details.</p>',
     E('<p>有关更多详细信息，请参阅 <a href="index.html" title="mod tokio::io">模块</a> 文档。</p>')),
    (b'<p>Equivalent to:</p>',
     E('<p>等价于：</p>')),
    (b'<p><a href="../fs/struct.File.html" title="struct tokio::fs::File"><code>File</code></a> implements <code>Read</code> and <a href="../../bytes/bytes_mut/struct.BytesMut.html" title="struct bytes::bytes_mut::BytesMut"><code>BytesMut</code></a> implements <a href="../../bytes/buf/buf_mut/trait.BufMut.html" title="trait bytes::buf::buf_mut::BufMut"><code>BufMut</code></a>:</p>',
     E('<p><a href="../fs/struct.File.html" title="struct tokio::fs::File"><code>File</code></a> 实现了 <code>Read</code>，<a href="../../bytes/bytes_mut/struct.BytesMut.html" title="struct bytes::bytes_mut::BytesMut"><code>BytesMut</code></a> 实现了 <a href="../../bytes/buf/buf_mut/trait.BufMut.html" title="trait bytes::buf::buf_mut::BufMut"><code>BufMut</code></a>：</p>')),
    (b'<p>This method is not cancellation safe. If the method is used as the\r\nevent in a <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> statement and some\r\nother branch completes first, then some data may already have been\r\nread into <code>buf</code>.</p>',
     E('<p>此方法不是可取消安全的。如果在 <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a>\r\n语句中作为事件使用且另一个分支先完成，\r\n则某些数据可能已经\r\n被读入 <code>buf</code>。</p>')),
    (b'<p>This method returns the same errors as <a href="trait.AsyncReadExt.html#method.read_exact" title="method tokio::io::AsyncReadExt::read_exact"><code>AsyncReadExt::read_exact</code></a>.</p>',
     E('<p>此方法返回与 <a href="trait.AsyncReadExt.html#method.read_exact" title="method tokio::io::AsyncReadExt::read_exact"><code>AsyncReadExt::read_exact</code></a> 相同的错误。</p>')),
    (b'<p>All bytes read from this source will be appended to the specified\r\nbuffer <code>buf</code>. This function will continuously call <a href="trait.AsyncReadExt.html#method.read" title="method tokio::io::AsyncReadExt::read"><code>read()</code></a> to\r\nappend more data to <code>buf</code> until <a href="trait.AsyncReadExt.html#method.read" title="method tokio::io::AsyncReadExt::read"><code>read()</code></a> returns <code>Ok(0)</code>.</p>',
     E('<p>从此源读取的所有字节都将附加到指定的\r\n缓冲区 <code>buf</code>。此函数会持续调用 <a href="trait.AsyncReadExt.html#method.read" title="method tokio::io::AsyncReadExt::read"><code>read()</code></a> 来\r\n将更多数据附加到 <code>buf</code>，直到 <a href="trait.AsyncReadExt.html#method.read" title="method tokio::io::AsyncReadExt::read"><code>read()</code></a> 返回 <code>Ok(0)</code>。</p>')),
    (b'<p>If successful, the total number of bytes read is returned.</p>',
     E('<p>如果成功，则返回读取的总字节数。</p>')),
    (b'<p>(See also the <a href="../fs/fn.read.html" title="fn tokio::fs::read"><code>tokio::fs::read</code></a> convenience function for reading from a\r\nfile.)</p>',
     E('<p>（另请参阅用于从文件读取的便捷函数 <a href="../fs/fn.read.html" title="fn tokio::fs::read"><code>tokio::fs::read</code></a>。）</p>')),
    (b'<p>See <a href="trait.AsyncReadExt.html#method.read_to_end" title="method tokio::io::AsyncReadExt::read_to_end"><code>read_to_end</code></a> for other error semantics.</p>',
     E('<p>有关其他错误语义，请参阅 <a href="trait.AsyncReadExt.html#method.read_to_end" title="method tokio::io::AsyncReadExt::read_to_end"><code>read_to_end</code></a>。</p>')),
    (b'<p>(See also the <a href="../fs/fn.read_to_string.html" title="fn tokio::fs::read_to_string"><code>crate::fs::read_to_string</code></a> convenience function for\r\nreading from a file.)</p>',
     E('<p>（另请参阅用于从文件读取的便捷函数 <a href="../fs/fn.read_to_string.html" title="fn tokio::fs::read_to_string"><code>crate::fs::read_to_string</code></a>。）</p>')),
    (b'<p>This trait is <b>not</b> <a href="https://doc.rust-lang.org/1.95.0/reference/items/traits.html#dyn-compatibility">dyn compatible</a>.</p>',
     E('<p>此 trait <b>不</b>是<a href="https://doc.rust-lang.org/1.95.0/reference/items/traits.html#dyn-compatibility">dyn 兼容</a>的。</p>')),
    (b'<p><i>In older versions of Rust, dyn compatibility was called "object safety", so this trait is not object safe.</i></p>',
     E('<p><i>在较早版本的 Rust 中，dyn 兼容性被称为"对象安全"，因此此 trait 不是对象安全的。</i></p>')),
])


# ============================================================
# io/trait.AsyncSeekExt.html
# ============================================================
add('io/trait.AsyncSeekExt.html', [
    (b'<p>An extension trait that adds utility methods to <a href="trait.AsyncSeek.html" title="trait tokio::io::AsyncSeek"><code>AsyncSeek</code></a> types.</p>',
     E('<p>为 <a href="trait.AsyncSeek.html" title="trait tokio::io::AsyncSeek"><code>AsyncSeek</code></a> 类型添加实用方法的扩展 trait。</p>')),
    (b'<p>See <a href="index.html" title="mod tokio::io">module</a> documentation for more details.</p>',
     E('<p>有关更多详细信息，请参阅 <a href="index.html" title="mod tokio::io">模块</a> 文档。</p>')),
    (b'<p>Equivalent to:</p>',
     E('<p>等价于：</p>')),
    (b'<p>This trait is <b>not</b> <a href="https://doc.rust-lang.org/1.95.0/reference/items/traits.html#dyn-compatibility">dyn compatible</a>.</p>',
     E('<p>此 trait <b>不</b>是<a href="https://doc.rust-lang.org/1.95.0/reference/items/traits.html#dyn-compatibility">dyn 兼容</a>的。</p>')),
    (b'<p><i>In older versions of Rust, dyn compatibility was called "object safety", so this trait is not object safe.</i></p>',
     E('<p><i>在较早版本的 Rust 中，dyn 兼容性被称为"对象安全"，因此此 trait 不是对象安全的。</i></p>')),
])


# ============================================================
# process/index.html
# ============================================================
add('process/index.html', [
    (b'<p>An implementation of asynchronous process management for Tokio.</p>',
     E('<p>Tokio 的异步进程管理实现。</p>')),
    (b'<p>This module provides a <a href="struct.Command.html" title="struct tokio::process::Command"><code>Command</code></a> struct that imitates the interface of the\r\n<a href="https://doc.rust-lang.org/1.95.0/std/process/struct.Command.html" title="struct std::process::Command"><code>std::process::Command</code></a> type in the standard library, but provides asynchronous versions of\r\nfunctions that create processes. These functions (<code>spawn</code>, <code>status</code>, <code>output</code> and their\r\nvariants) return \xe2\x80\x9cfuture aware\xe2\x80\x9d types that interoperate with Tokio. The asynchronous process\r\nsupport is provided through signal handling on Unix and system APIs on Windows.</p>',
     E('<p>此模块提供一个 <a href="struct.Command.html" title="struct tokio::process::Command"><code>Command</code></a> 结构体，模仿标准库中的\r\n<a href="https://doc.rust-lang.org/1.95.0/std/process/struct.Command.html" title="struct std::process::Command"><code>std::process::Command</code></a> 类型接口，但提供用于创建进程的函数的\r\n异步版本。这些函数（<code>spawn</code>、<code>status</code>、<code>output</code> 及其\r\n变体）返回与 Tokio 互操作的\xe2\x80\x9cfuture 感知\xe2\x80\x9d类型。异步进程支持通过 Unix 上的信号处理\r\n和 Windows 上的系统 API 提供。</p>')),
    (b'<p>Here\xe2\x80\x99s an example program which will spawn <code>echo hello world</code> and then wait\r\nfor it complete.</p>',
     E('<p>下面是一个示例程序，将生成 <code>echo hello world</code> 然后等待\r\n其完成。</p>')),
    (b'<p>Next, let\xe2\x80\x99s take a look at an example where we not only spawn <code>echo hello world</code> but we also capture its output.</p>',
     E('<p>接下来，让我们看一个示例，不仅生成 <code>echo hello world</code>，还捕获其输出。</p>')),
    (b'<p>We can also read input line by line.</p>',
     E('<p>我们还可以逐行读取输入。</p>')),
    (b'<p>Here is another example using <code>sort</code> writing into the child process\r\nstandard input, capturing the output of the sorted text.</p>',
     E('<p>这是另一个示例，使用 <code>sort</code> 写入到子进程的标准输入，\r\n捕获排序后文本的输出。</p>')),
    (b'<p>With some coordination, we can also pipe the output of one command into\r\nanother.</p>',
     E('<p>通过一些协调，我们还可以将一个命令的输出通过管道\r\n传送到另一个命令。</p>')),
    (b'<p>Similar to the behavior to the standard library, and unlike the futures\r\nparadigm of dropping-implies-cancellation, a spawned process will, by\r\ndefault, continue to execute even after the <code>Child</code> handle has been dropped.</p>',
     E('<p>与标准库的行为类似，且与 futures 范式中"丢弃即取消"不同，\r\n默认情况下，已生成的进程即使在 <code>Child</code> 句柄被丢弃后仍将继续执行。</p>')),
    (b'<p>The <a href="struct.Command.html#method.kill_on_drop" title="method tokio::process::Command::kill_on_drop"><code>Command::kill_on_drop</code></a> method can be used to modify this behavior\r\nand kill the child process if the <code>Child</code> wrapper is dropped before it\r\nhas exited.</p>',
     E('<p><a href="struct.Command.html#method.kill_on_drop" title="method tokio::process::Command::kill_on_drop"><code>Command::kill_on_drop</code></a> 方法可用于修改此行为，\r\n在 <code>Child</code> 包装器在子进程退出前被丢弃时杀死子进程。</p>')),
    (b'<p>On Unix platforms processes must be \xe2\x80\x9creaped\xe2\x80\x9d by their parent process after\r\nthey have exited in order to release all OS resources. A child process which\r\nhas exited, but has not yet been reaped by its parent is considered a \xe2\x80\x9czombie\xe2\x80\x9d\r\nprocess. Such processes continue to count against limits imposed by the system,\r\nand having too many zombie processes present can prevent additional processes\r\nfrom being spawned.</p>',
     E('<p>在 Unix 平台上，进程退出后必须由其父进程\xe2\x80\x9c回收\xe2\x80\x9d，\r\n以释放所有操作系统资源。已退出但尚未被父进程回收的子进程被视为\xe2\x80\x9c僵尸\xe2\x80\x9d进程。\r\n此类进程仍会计入系统施加的限制，\r\n并且存在过多僵尸进程可能会阻止新进程的生成。</p>')),
    (b'<p>The tokio runtime will, on a best-effort basis, attempt to reap and clean up\r\nany process which it has spawned. No additional guarantees are made with regard to\r\nhow quickly or how often this procedure will take place.</p>',
     E('<p>Tokio 运行时将尽最大努力\r\n尝试回收和清理其已生成的任何进程。\r\n对于此过程的发生频率和速度不提供额外保证。</p>')),
    (b'<p>It is recommended to avoid dropping a <a href="struct.Child.html" title="struct tokio::process::Child"><code>Child</code></a> process handle before it has been\r\nfully <code>await</code>ed if stricter cleanup guarantees are required.</p>',
     E('<p>如果需要更严格的清理保证，建议避免在 <a href="struct.Child.html" title="struct tokio::process::Child"><code>Child</code></a>\r\n进程句柄完全\r\n被 <code>await</code> 之前丢弃它。</p>')),
])


# ============================================================
# process/struct.Command.html
# ============================================================
add('process/struct.Command.html', [
    (b'<p>This structure mimics the API of <a href="https://doc.rust-lang.org/1.95.0/std/process/struct.Command.html" title="struct std::process::Command"><code>std::process::Command</code></a> found in the standard library, but\r\nreplaces functions that create a process with an asynchronous variant. The main provided\r\nasynchronous functions are <a href="struct.Command.html#method.spawn" title="method tokio::process::Command::spawn">spawn</a>, <a href="struct.Command.html#method.status" title="method tokio::process::Command::status">status</a>, and\r\n<a href="struct.Command.html#method.output" title="method tokio::process::Command::output">output</a>.</p>',
     E('<p>此结构体模仿标准库中的\r\n<a href="https://doc.rust-lang.org/1.95.0/std/process/struct.Command.html" title="struct std::process::Command"><code>std::process::Command</code></a> API，但将用于创建进程的函数替换为\r\n异步变体。主要提供的\r\n异步函数为 <a href="struct.Command.html#method.spawn" title="method tokio::process::Command::spawn">spawn</a>、<a href="struct.Command.html#method.status" title="method tokio::process::Command::status">status</a> 和\r\n<a href="struct.Command.html#method.output" title="method tokio::process::Command::output">output</a>。</p>')),
    (b'<p><code>Command</code> uses asynchronous versions of some <code>std</code> types (for example <a href="struct.Child.html" title="struct tokio::process::Child"><code>Child</code></a>).</p>',
     E('<p><code>Command</code> 使用某些 <code>std</code> 类型的异步版本（例如 <a href="struct.Child.html" title="struct tokio::process::Child"><code>Child</code></a>）。</p>')),
    (b'<p>Constructs a new <code>Command</code> for launching the program at\r\npath <code>program</code>, with the following default configuration:</p>',
     E('<p>构造一个新的 <code>Command</code>，用于在\r\n路径 <code>program</code> 启动程序，使用以下默认配置：</p>')),
    (b'<p>If <code>program</code> is not an absolute path, the <code>PATH</code> will be searched in\r\nan OS-defined way.</p>',
     E('<p>如果 <code>program</code> 不是绝对路径，将以\r\n操作系统定义的方式搜索 <code>PATH</code>。</p>')),
    (b'<p>The search path to be used may be controlled by setting the\r\n<code>PATH</code> environment variable on the Command,\r\nbut this has some implementation limitations on Windows\r\n(see issue <a href="https://github.com/rust-lang/rust/issues/37519">rust-lang/rust#37519</a>).</p>',
     E('<p>要使用的搜索路径可以通过\r\n在 Command 上设置 <code>PATH</code>\r\n环境变量来控制，但这在 Windows 上有一些\r\n实现限制\r\n（参见 issue <a href="https://github.com/rust-lang/rust/issues/37519">rust-lang/rust#37519</a>）。</p>')),
    (b'<p>Basic usage:</p>',
     E('<p>基本用法：</p>')),
    (b'<p>Note that Tokio specific options will be lost. Currently, this only applies to <a href="struct.Command.html#method.kill_on_drop" title="method tokio::process::Command::kill_on_drop"><code>kill_on_drop</code></a>.</p>',
     E('<p>请注意，Tokio 特定选项将丢失。目前，这仅适用于 <a href="struct.Command.html#method.kill_on_drop" title="method tokio::process::Command::kill_on_drop"><code>kill_on_drop</code></a>。</p>')),
    (b'<p>usage would be:</p>',
     E('<p>用法如下：</p>')),
    (b'<p>To pass a single argument see <a href="struct.Command.html#method.arg" title="method tokio::process::Command::arg"><code>arg</code></a>.</p>',
     E('<p>要传递单个参数，请参阅 <a href="struct.Command.html#method.arg" title="method tokio::process::Command::arg"><code>arg</code></a>。</p>')),
    (b'<p>Inserts or updates an environment variable mapping.</p>',
     E('<p>插入或更新环境变量映射。</p>')),
    (b'<p>Removes an environment variable mapping.</p>',
     E('<p>删除环境变量映射。</p>')),
    (b'<p>Sets the working directory for the child process.</p>',
     E('<p>为子进程设置工作目录。</p>')),
    (b'<p>If the program path is relative (e.g., <code>"./script.sh"</code>), it\xe2\x80\x99s ambiguous\r\nwhether it should be interpreted relative to the parent\xe2\x80\x99s working\r\ndirectory or relative to <code>current_dir</code>. The behavior in this case is\r\nplatform specific and unstable, and it\xe2\x80\x99s recommended to use\r\n<a href="../fs/fn.canonicalize.html" title="fn tokio::fs::canonicalize"><code>canonicalize</code></a> to get an absolute program path instead.</p>',
     E('<p>如果程序路径是相对的（例如 <code>"./script.sh"</code>），\r\n那么是应该相对于\r\n父进程的工作目录解释，还是相对于 <code>current_dir</code> 解释，\r\n这一点不明确。这种情况下的行为\r\n是平台特定的且不稳定的，\r\n建议使用\r\n<a href="../fs/fn.canonicalize.html" title="fn tokio::fs::canonicalize"><code>canonicalize</code></a> 来获取绝对的程序路径。</p>')),
    (b'<p>Sets configuration for the child process\xe2\x80\x99s standard input (stdin) handle.</p>',
     E('<p>为子进程的标准输入 (stdin) 句柄\r\n设置配置。</p>')),
    (b'<p>Defaults to <a href="https://doc.rust-lang.org/1.95.0/std/process/struct.Stdio.html#method.inherit" title="associated function std::process::Stdio::inherit"><code>inherit</code></a>.</p>',
     E('<p>默认为 <a href="https://doc.rust-lang.org/1.95.0/std/process/struct.Stdio.html#method.inherit" title="associated function std::process::Stdio::inherit"><code>inherit</code></a>。</p>')),
    (b'<p>Sets configuration for the child process\xe2\x80\x99s standard output (stdout) handle.</p>',
     E('<p>为子进程的标准输出 (stdout) 句柄\r\n设置配置。</p>')),
    (b'<p>Defaults to <a href="https://doc.rust-lang.org/1.95.0/std/process/struct.Stdio.html#method.inherit" title="associated function std::process::Stdio::inherit"><code>inherit</code></a> when used with <code>spawn</code> or <code>status</code>, and\r\ndefaults to <a href="https://doc.rust-lang.org/1.95.0/std/process/struct.Stdio.html#method.piped" title="associated function std::process::Stdio::piped"><code>piped</code></a> when used with <code>output</code>.</p>',
     E('<p>与 <code>spawn</code> 或 <code>status</code> 一起使用时默认为\r\n<a href="https://doc.rust-lang.org/1.95.0/std/process/struct.Stdio.html#method.inherit" title="associated function std::process::Stdio::inherit"><code>inherit</code></a>，\r\n与 <code>output</code> 一起使用时默认为\r\n<a href="https://doc.rust-lang.org/1.95.0/std/process/struct.Stdio.html#method.piped" title="associated function std::process::Stdio::piped"><code>piped</code></a>。</p>')),
    (b'<p>Sets configuration for the child process\xe2\x80\x99s standard error (stderr) handle.</p>',
     E('<p>为子进程的标准错误 (stderr) 句柄\r\n设置配置。</p>')),
    (b'<p>Executes the command as a child process, returning a handle to it.</p>',
     E('<p>将命令作为子进程执行，并返回\r\n到该进程的句柄。</p>')),
    (b'<p>By default, stdin, stdout and stderr are inherited from the parent.</p>',
     E('<p>默认情况下，stdin、stdout 和 stderr 继承自父进程。</p>')),
    (b'<p>This method will spawn the child process synchronously and return a\r\nhandle to a future-aware child process. The <code>Child</code> returned implements\r\n<code>Future</code> itself to acquire the <code>ExitStatus</code> of the child, and otherwise\r\nthe <code>Child</code> has methods to acquire handles to the stdin, stdout, and\r\nstderr streams.</p>',
     E('<p>此方法会同步生成子进程并返回\r\n到 future 感知子进程的句柄。返回的 <code>Child</code>\r\n自身实现 <code>Future</code> 以获取子进程的 <code>ExitStatus</code>，\r\n此外 <code>Child</code> 还有\r\n获取 stdin、stdout 和 stderr 流句柄的方法。</p>')),
    (b'<p>All I/O this child does will be associated with the current default\r\nevent loop.</p>',
     E('<p>此子进程执行的所有 I/O 都将与\r\n当前默认事件循环关联。</p>')),
    (b'<p>The tokio runtime will, on a best-effort basis, attempt to reap and clean up\r\nany process which it has spawned. No additional guarantees are made with regard to\r\nhow quickly or how often this procedure will take place.</p>',
     E('<p>Tokio 运行时将尽最大努力\r\n尝试回收和清理其已生成的任何进程。\r\n对于此过程的发生频率和速度不提供额外保证。</p>')),
    (b'<p>On Unix platforms this method will fail with <code>std::io::ErrorKind::WouldBlock</code>\r\nif the system process limit is reached (which includes other applications\r\nrunning on the system).</p>',
     E('<p>在 Unix 平台上，如果达到系统进程限制（包括系统上运行的其他应用程序），\r\n此方法将失败并返回 <code>std::io::ErrorKind::WouldBlock</code>。</p>')),
    (b'<p>Executes the command as a child process, waiting for it to finish and\r\ncollecting its exit status.</p>',
     E('<p>将命令作为子进程执行，等待其完成\r\n并收集其退出状态。</p>')),
    (b'<p>The destructor of the future returned by this function will kill\r\nthe child if <a href="struct.Command.html#method.kill_on_drop" title="method tokio::process::Command::kill_on_drop"><code>kill_on_drop</code></a> is set to true.</p>',
     E('<p>如果 <a href="struct.Command.html#method.kill_on_drop" title="method tokio::process::Command::kill_on_drop"><code>kill_on_drop</code></a> 设置为 true，\r\n此函数返回的 future 的析构函数\r\n将杀死子进程。</p>')),
    (b'<p>This future will return an error if the child process cannot be spawned\r\nor if there is an error while awaiting its status.</p>',
     E('<p>如果无法生成子进程，或者\r\n在等待其状态时发生错误，则此 future\r\n将返回错误。</p>')),
    (b'<p><strong>Note</strong>: this method, unlike the standard library, will\r\nunconditionally configure the stdout/stderr handles to be pipes, even\r\nif they have been previously configured. If this is not desired then\r\nthe <code>spawn</code> method should be used in combination with the\r\n<code>wait_with_output</code> method on child.</p>',
     E('<p><strong>注意</strong>：与标准库不同，此方法会\r\n无条件地将 stdout/stderr 句柄配置为管道，\r\n即使它们之前已经配置过。如果不需要这种行为，\r\n则应将 <code>spawn</code> 方法与 child 上的\r\n<code>wait_with_output</code> 方法结合使用。</p>')),
    (b'<p>This method will return a future representing the collection of the\r\nchild process\xe2\x80\x99s stdout/stderr. It will resolve to\r\nthe <code>Output</code> type in the standard library, containing <code>stdout</code> and\r\n<code>stderr</code> as <code>Vec&lt;u8&gt;</code> along with an <code>ExitStatus</code> representing how the\r\nprocess exited.</p>',
     E('<p>此方法将返回一个 future，表示\r\n收集子进程的 stdout/stderr。它将解析\r\n为标准库中的 <code>Output</code> 类型，包含 <code>stdout</code> 和\r\n<code>stderr</code> 作为 <code>Vec&lt;u8&gt;</code>，以及表示进程退出方式的\r\n<code>ExitStatus</code>。</p>')),
    (b'<p>Returns the boolean value that was previously set by <a href="struct.Command.html#method.kill_on_drop" title="method tokio::process::Command::kill_on_drop"><code>Command::kill_on_drop</code></a>.</p>',
     E('<p>返回之前由 <a href="struct.Command.html#method.kill_on_drop" title="method tokio::process::Command::kill_on_drop"><code>Command::kill_on_drop</code></a> 设置的布尔值。</p>')),
    (b'<p>Note that if you have not previously called <a href="struct.Command.html#method.kill_on_drop" title="method tokio::process::Command::kill_on_drop"><code>Command::kill_on_drop</code></a>, the\r\ndefault value of <code>false</code> will be returned here.</p>',
     E('<p>请注意，如果你之前没有调用 <a href="struct.Command.html#method.kill_on_drop" title="method tokio::process::Command::kill_on_drop"><code>Command::kill_on_drop</code></a>，\r\n则此处将返回默认值 <code>false</code>。</p>')),
])


# ============================================================
# signal/fn.ctrl_c.html
# ============================================================
add('signal/fn.ctrl_c.html', [
    (b'<p>Completes when a \xe2\x80\x9cctrl-c\xe2\x80\x9d notification is sent to the process.</p>',
     E('<p>当向进程发送\xe2\x80\x9cctrl-c\xe2\x80\x9d通知时完成。</p>')),
    (b'<p>While signals are handled very differently between Unix and Windows, both\r\nplatforms support receiving a signal on \xe2\x80\x9cctrl-c\xe2\x80\x9d. This function provides a\r\nportable API for receiving this notification.</p>',
     E('<p>虽然 Unix 和 Windows 处理信号的方式差异很大，但\r\n两个平台都支持在\xe2\x80\x9cctrl-c\xe2\x80\x9d上接收信号。\r\n此函数提供用于接收此通知的\r\n可移植 API。</p>')),
    (b'<p>Once the returned future is polled, a listener is registered. The future\r\nwill complete on the first received <code>ctrl-c</code> <strong>after</strong> the initial call to\r\neither <code>Future::poll</code> or <code>.await</code>.</p>',
     E('<p>返回的 future 一旦被轮询，就会注册一个监听器。\r\n此 future 将在首次接收到 <code>ctrl-c</code> 时完成，\r\n该<strong>之后</strong>的初始调用为\r\n<code>Future::poll</code> 或 <code>.await</code>。</p>')),
    (b'<p>On Unix platforms, the first time that a <code>Signal</code> instance is registered for a\r\nparticular signal kind, an OS signal-handler is installed which replaces the\r\ndefault platform behavior when that signal is received, <strong>for the duration of\r\nthe entire process</strong>.</p>',
     E('<p>在 Unix 平台上，第一次为\r\n特定信号类型注册 <code>Signal</code> 实例时，\r\n会安装一个操作系统信号处理程序，\r\n该程序在接收到该信号时将替换\r\n默认的平台行为，<strong>持续\r\n整个进程期间</strong>。</p>')),
    (b'<p>For example, Unix systems will terminate a process by default when it\r\nreceives a signal generated by <code>"CTRL+C"</code> on the terminal. But, when a\r\n<code>ctrl_c</code> stream is created to listen for this signal, the time it arrives,\r\nit will be translated to a stream event, and the process will continue to\r\nexecute.  <strong>Even if this <code>Signal</code> instance is dropped, subsequent <code>SIGINT</code>\r\ndeliveries will end up captured by Tokio, and the default platform behavior\r\nwill NOT be reset</strong>.</p>',
     E('<p>例如，Unix 系统默认会在收到\r\n终端上 <code>"CTRL+C"</code> 生成的信号时终止进程。但是，当创建\r\n<code>ctrl_c</code> 流以监听此信号时，在其到达时，\r\n它将被转换为流事件，并且进程将继续\r\n执行。<strong>即使此 <code>Signal</code> 实例被丢弃，\r\n后续的 <code>SIGINT</code> 传递最终也会被 Tokio 捕获，并且默认平台行为\r\n将不会重置</strong>。</p>')),
    (b'<p>Thus, applications should take care to ensure the expected signal behavior\r\noccurs as expected after listening for specific signals.</p>',
     E('<p>因此，应用程序应小心以确保\r\n在监听特定信号后预期的信号行为\r\n按预期发生。</p>')),
    (b'<p>Listen in the background:</p>',
     E('<p>在后台监听：</p>')),
])


# ============================================================
# signal/index.html
# ============================================================
add('signal/index.html', [
    (b'<p>Asynchronous signal handling for Tokio.</p>',
     E('<p>Tokio 的异步信号处理。</p>')),
    (b'<p>Note that signal handling is in general a very tricky topic and should be\r\nused with great care. This crate attempts to implement \xe2\x80\x98best practice\xe2\x80\x99 for\r\nsignal handling, but it should be evaluated for your own applications\xe2\x80\x99 needs\r\nto see if it\xe2\x80\x99s suitable.</p>',
     E('<p>请注意，信号处理总体上是一个非常棘手的话题，\r\n应谨慎使用。本 crate 试图为\r\n信号处理实现\xe2\x80\x98最佳实践\xe2\x80\x99，\r\n但应根据你自己应用的需求评估其是否\r\n适合。</p>')),
    (b'<p>There are some fundamental limitations of this crate documented on the OS\r\nspecific structures, as well.</p>',
     E('<p>本 crate 在操作系统特定结构上也记录了一些基本限制。</p>')),
    (b'<p>Print on \xe2\x80\x9cctrl-c\xe2\x80\x9d notification.</p>',
     E('<p>在\xe2\x80\x9cctrl-c\xe2\x80\x9d通知时打印。</p>')),
    (b'<p>Wait for <code>SIGHUP</code> on Unix</p>',
     E('<p>在 Unix 上等待 <code>SIGHUP</code></p>')),
])


# ============================================================
# signal/windows/fn.ctrl_break.html
# ============================================================
add('signal/windows/fn.ctrl_break.html', [
    (b'<p>Creates a new listener which receives \xe2\x80\x9cctrl-break\xe2\x80\x9d notifications sent to the\r\nprocess.</p>',
     E('<p>创建一个新的监听器，用于接收发送到\r\n进程的\xe2\x80\x9cctrl-break\xe2\x80\x9d通知。</p>')),
])


# ============================================================
# signal/windows/fn.ctrl_c.html
# ============================================================
add('signal/windows/fn.ctrl_c.html', [
    (b'<p>Creates a new listener which receives \xe2\x80\x9cctrl-c\xe2\x80\x9d notifications sent to the\r\nprocess.</p>',
     E('<p>创建一个新的监听器，用于接收发送到\r\n进程的\xe2\x80\x9cctrl-c\xe2\x80\x9d通知。</p>')),
])


# ============================================================
# signal/windows/fn.ctrl_close.html
# ============================================================
add('signal/windows/fn.ctrl_close.html', [
    (b'<p>Creates a new listener which receives \xe2\x80\x9cctrl-close\xe2\x80\x9d notifications sent to the\r\nprocess.</p>',
     E('<p>创建一个新的监听器，用于接收发送到\r\n进程的\xe2\x80\x9cctrl-close\xe2\x80\x9d通知。</p>')),
])


# ============================================================
# signal/windows/fn.ctrl_logoff.html
# ============================================================
add('signal/windows/fn.ctrl_logoff.html', [
    (b'<p>Creates a new listener which receives \xe2\x80\x9cctrl-logoff\xe2\x80\x9d notifications sent to the\r\nprocess.</p>',
     E('<p>创建一个新的监听器，用于接收发送到\r\n进程的\xe2\x80\x9cctrl-logoff\xe2\x80\x9d通知。</p>')),
])


# ============================================================
# signal/windows/fn.ctrl_shutdown.html
# ============================================================
add('signal/windows/fn.ctrl_shutdown.html', [
    (b'<p>Creates a new listener which receives \xe2\x80\x9cctrl-shutdown\xe2\x80\x9d notifications sent to the\r\nprocess.</p>',
     E('<p>创建一个新的监听器，用于接收发送到\r\n进程的\xe2\x80\x9cctrl-shutdown\xe2\x80\x9d通知。</p>')),
])


# ============================================================
# signal/windows/index.html
# ============================================================
add('signal/windows/index.html', [
    (b'<p>Windows-specific types for signal handling.</p>',
     E('<p>用于信号处理的 Windows 特定类型。</p>')),
    (b'<p>This module is only defined on Windows and allows receiving \xe2\x80\x9cctrl-c\xe2\x80\x9d,\r\n\xe2\x80\x9cctrl-break\xe2\x80\x9d, \xe2\x80\x9cctrl-logoff\xe2\x80\x9d, \xe2\x80\x9cctrl-shutdown\xe2\x80\x9d, and \xe2\x80\x9cctrl-close\xe2\x80\x9d\r\nnotifications. These events are listened for via the <code>SetConsoleCtrlHandler</code>\r\nfunction which receives the corresponding <code>windows_sys</code> event type.</p>',
     E('<p>此模块仅在 Windows 上定义，允许接收\xe2\x80\x9cctrl-c\xe2\x80\x9d、\r\n\xe2\x80\x9cctrl-break\xe2\x80\x9d、\xe2\x80\x9cctrl-logoff\xe2\x80\x9d、\xe2\x80\x9cctrl-shutdown\xe2\x80\x9d和\xe2\x80\x9cctrl-close\xe2\x80\x9d\r\n通知。这些事件通过 <code>SetConsoleCtrlHandler</code>\r\n函数监听，该函数接收相应的 <code>windows_sys</code> 事件类型。</p>')),
])


# ============================================================
# signal/windows/struct.CtrlBreak.html
# ============================================================
add('signal/windows/struct.CtrlBreak.html', [
    (b'<p>Represents a listener which receives \xe2\x80\x9cctrl-break\xe2\x80\x9d notifications sent to the process\r\nvia <code>SetConsoleCtrlHandler</code>.</p>',
     E('<p>表示一个监听器，它接收通过 <code>SetConsoleCtrlHandler</code>\r\n发送到进程的\xe2\x80\x9cctrl-break\xe2\x80\x9d通知。</p>')),
    (b'<p>This listener can be turned into a <code>Stream</code> using <a href="https://docs.rs/tokio-stream/latest/tokio_stream/wrappers/struct.CtrlBreakStream.html"><code>CtrlBreakStream</code></a>.</p>',
     E('<p>可以使用 <a href="https://docs.rs/tokio-stream/latest/tokio_stream/wrappers/struct.CtrlBreakStream.html"><code>CtrlBreakStream</code></a> 将此监听器转换为 <code>Stream</code>。</p>')),
    (b'<p>A notification to this process notifies <em>all</em> receivers for\r\nthis event. Moreover, the notifications <strong>are coalesced</strong> if they aren\xe2\x80\x99t processed\r\nquickly enough. This means that if two notifications are received back-to-back,\r\nthen the listener may only receive one item about the two notifications.</p>',
     E('<p>对此进程的通知会通知此事件的<em>所有</em>接收者。\r\n此外，通知<strong>会合并</strong>，\r\n如果它们没有被\r\n足够快地处理。这意味着如果连续收到两个通知，\r\n则监听器可能仅收到关于这两个通知的一个条目。</p>')),
    (b'<p>Polls to receive the next signal notification event, outside of an\r\n<code>async</code> context.</p>',
     E('<p>在 <code>async</code> 上下文之外，轮询以接收下一个信号通知事件。</p>')),
])


# ============================================================
# signal/windows/struct.CtrlC.html
# ============================================================
add('signal/windows/struct.CtrlC.html', [
    (b'<p>Represents a listener which receives \xe2\x80\x9cctrl-c\xe2\x80\x9d notifications sent to the process\r\nvia <code>SetConsoleCtrlHandler</code>.</p>',
     E('<p>表示一个监听器，它接收通过 <code>SetConsoleCtrlHandler</code>\r\n发送到进程的\xe2\x80\x9cctrl-c\xe2\x80\x9d通知。</p>')),
    (b'<p>This event can be turned into a <code>Stream</code> using <a href="https://docs.rs/tokio-stream/latest/tokio_stream/wrappers/struct.CtrlCStream.html"><code>CtrlCStream</code></a>.</p>',
     E('<p>可以使用 <a href="https://docs.rs/tokio-stream/latest/tokio_stream/wrappers/struct.CtrlCStream.html"><code>CtrlCStream</code></a> 将此事件转换为 <code>Stream</code>。</p>')),
    (b'<p>A notification to this process notifies <em>all</em> receivers for\r\nthis event. Moreover, the notifications <strong>are coalesced</strong> if they aren\xe2\x80\x99t processed\r\nquickly enough. This means that if two notifications are received back-to-back,\r\nthen the listener may only receive one item about the two notifications.</p>',
     E('<p>对此进程的通知会通知此事件的<em>所有</em>接收者。\r\n此外，通知<strong>会合并</strong>，\r\n如果它们没有被\r\n足够快地处理。这意味着如果连续收到两个通知，\r\n则监听器可能仅收到关于这两个通知的一个条目。</p>')),
    (b'<p>Polls to receive the next signal notification event, outside of an\r\n<code>async</code> context.</p>',
     E('<p>在 <code>async</code> 上下文之外，轮询以接收下一个信号通知事件。</p>')),
])


# ============================================================
# signal/windows/struct.CtrlClose.html
# ============================================================
add('signal/windows/struct.CtrlClose.html', [
    (b'<p>Represents a listener which receives \xe2\x80\x9cctrl-close\xe2\x80\x9d notifications sent to the process\r\nvia <code>SetConsoleCtrlHandler</code>.</p>',
     E('<p>表示一个监听器，它接收通过 <code>SetConsoleCtrlHandler</code>\r\n发送到进程的\xe2\x80\x9cctrl-close\xe2\x80\x9d通知。</p>')),
    (b'<p>A notification to this process notifies <em>all</em> listeners listening for\r\nthis event. Moreover, the notifications <strong>are coalesced</strong> if they aren\xe2\x80\x99t processed\r\nquickly enough. This means that if two notifications are received back-to-back,\r\nthen the listener may only receive one item about the two notifications.</p>',
     E('<p>对此进程的通知会通知正在监听\r\n此事件的<em>所有</em>监听器。\r\n此外，通知<strong>会合并</strong>，\r\n如果它们没有被\r\n足够快地处理。这意味着如果连续收到两个通知，\r\n则监听器可能仅收到关于这两个通知的一个条目。</p>')),
    (b'<p>Polls to receive the next signal notification event, outside of an\r\n<code>async</code> context.</p>',
     E('<p>在 <code>async</code> 上下文之外，轮询以接收下一个信号通知事件。</p>')),
])


# ============================================================
# signal/windows/struct.CtrlLogoff.html
# ============================================================
add('signal/windows/struct.CtrlLogoff.html', [
    (b'<p>Represents a listener which receives \xe2\x80\x9cctrl-logoff\xe2\x80\x9d notifications sent to the process\r\nvia <code>SetConsoleCtrlHandler</code>.</p>',
     E('<p>表示一个监听器，它接收通过 <code>SetConsoleCtrlHandler</code>\r\n发送到进程的\xe2\x80\x9cctrl-logoff\xe2\x80\x9d通知。</p>')),
    (b'<p>A notification to this process notifies <em>all</em> listeners listening for\r\nthis event. Moreover, the notifications <strong>are coalesced</strong> if they aren\xe2\x80\x99t processed\r\nquickly enough. This means that if two notifications are received back-to-back,\r\nthen the listener may only receive one item about the two notifications.</p>',
     E('<p>对此进程的通知会通知正在监听\r\n此事件的<em>所有</em>监听器。\r\n此外，通知<strong>会合并</strong>，\r\n如果它们没有被\r\n足够快地处理。这意味着如果连续收到两个通知，\r\n则监听器可能仅收到关于这两个通知的一个条目。</p>')),
    (b'<p>Polls to receive the next signal notification event, outside of an\r\n<code>async</code> context.</p>',
     E('<p>在 <code>async</code> 上下文之外，轮询以接收下一个信号通知事件。</p>')),
])


# ============================================================
# signal/windows/struct.CtrlShutdown.html
# ============================================================
add('signal/windows/struct.CtrlShutdown.html', [
    (b'<p>Represents a listener which receives \xe2\x80\x9cctrl-shutdown\xe2\x80\x9d notifications sent to the process\r\nvia <code>SetConsoleCtrlHandler</code>.</p>',
     E('<p>表示一个监听器，它接收通过 <code>SetConsoleCtrlHandler</code>\r\n发送到进程的\xe2\x80\x9cctrl-shutdown\xe2\x80\x9d通知。</p>')),
    (b'<p>A notification to this process notifies <em>all</em> listeners listening for\r\nthis event. Moreover, the notifications <strong>are coalesced</strong> if they aren\xe2\x80\x99t processed\r\nquickly enough. This means that if two notifications are received back-to-back,\r\nthen the listener may only receive one item about the two notifications.</p>',
     E('<p>对此进程的通知会通知正在监听\r\n此事件的<em>所有</em>监听器。\r\n此外，通知<strong>会合并</strong>，\r\n如果它们没有被\r\n足够快地处理。这意味着如果连续收到两个通知，\r\n则监听器可能仅收到关于这两个通知的一个条目。</p>')),
    (b'<p>Polls to receive the next signal notification event, outside of an\r\n<code>async</code> context.</p>',
     E('<p>在 <code>async</code> 上下文之外，轮询以接收下一个信号通知事件。</p>')),
])


# ============================================================
# task/fn.block_in_place.html
# ============================================================
add('task/fn.block_in_place.html', [
    (b'<p>Runs the provided blocking function on the current thread without\r\nblocking the executor.</p>',
     E('<p>在当前线程上运行提供的阻塞函数，\r\n而不阻塞执行器。</p>')),
    (b'<p>In general, issuing a blocking call or performing a lot of compute in a\r\nfuture without yielding is problematic, as it may prevent the executor\r\nfrom driving other tasks forward. Calling this function informs the\r\nexecutor that the currently executing task is about to block the thread,\r\nso the executor is able to hand off any other tasks it has to a new\r\nworker thread before that happens. See the <a href="../index.html#cpu-bound-tasks-and-blocking-code">CPU-bound tasks and blocking\r\ncode</a> section for more information.</p>',
     E('<p>一般来说，发出阻塞调用或在\r\nfuture 中执行大量计算而不让出是有问题的，\r\n因为它可能会阻止执行器\r\n推进其他任务。调用此函数\r\n通知执行器当前正在执行的任务即将阻塞线程，\r\n以便执行器能够在此之前\r\n将其拥有的任何其他任务移交给\r\n新的工作线程。有关更多信息，\r\n请参阅<a href="../index.html#cpu-bound-tasks-and-blocking-code">CPU 密集型任务和阻塞代码</a>部分。</p>')),
    (b'<p>Be aware that although this function avoids starving other independently\r\nspawned tasks, any other code running concurrently in the same task will\r\nbe suspended during the call to <code>block_in_place</code>. This can happen e.g.\r\nwhen using the <a href="../macro.join.html" title="macro tokio::join"><code>join!</code></a> macro. To avoid this issue, use\r\n<a href="fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a> instead of <code>block_in_place</code>.</p>',
     E('<p>请注意，尽管此函数避免了饿死其他独立\r\n生成的任务，但在调用 <code>block_in_place</code> 期间，\r\n同一任务中并发运行的任何其他代码\r\n都将被挂起。例如在使用\r\n<a href="../macro.join.html" title="macro tokio::join"><code>join!</code></a> 宏时\r\n可能发生这种情况。为避免此问题，\r\n请使用 <a href="fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a> 代替 <code>block_in_place</code>。</p>')),
    (b'<p>Note that this function cannot be used within a <a href="../runtime/struct.Builder.html#method.new_current_thread" title="associated function tokio::runtime::Builder::new_current_thread"><code>current_thread</code></a> runtime\r\nbecause in this case there are no other worker threads to hand off tasks\r\nto. On the other hand, calling the function outside a runtime is\r\nallowed. In this case, <code>block_in_place</code> just calls the provided closure\r\nnormally.</p>',
     E('<p>请注意，此函数不能在\r\n<a href="../runtime/struct.Builder.html#method.new_current_thread" title="associated function tokio::runtime::Builder::new_current_thread"><code>current_thread</code></a> 运行\r\n时内使用，因为在这种情况下\r\n没有其他工作线程可以移交任务。\r\n另一方面，允许在运行时外部调用此函数。\r\n在这种情况下，<code>block_in_place</code> 只是正常地\r\n调用所提供的闭包。</p>')),
    (b'<p>Code running behind <code>block_in_place</code> cannot be cancelled. When you shut\r\ndown the executor, it will wait indefinitely for all blocking operations\r\nto finish. You can use <a href="../runtime/struct.Runtime.html#method.shutdown_timeout" title="method tokio::runtime::Runtime::shutdown_timeout"><code>shutdown_timeout</code></a> to stop waiting for them\r\nafter a certain timeout. Be aware that this will still not cancel the\r\ntasks \xe2\x80\x94 they are simply allowed to keep running after the method\r\nreturns.</p>',
     E('<p><code>block_in_place</code> 后运行的代码\r\n无法被取消。当你关闭\r\n执行器时，它将无限期等待所有阻塞操作完成。\r\n你可以使用\r\n<a href="../runtime/struct.Runtime.html#method.shutdown_timeout" title="method tokio::runtime::Runtime::shutdown_timeout"><code>shutdown_timeout</code></a> 在\r\n超时后停止等待它们。请注意，这\r\n仍然不会取消这些任务\xe2\x80\x94它们\r\n只是在方法返回后继续运行。</p>')),
    (b'<p>Code running inside <code>block_in_place</code> may use <code>block_on</code> to reenter the\r\nasync context.</p>',
     E('<p><code>block_in_place</code> 内运行的代码可以使用 <code>block_on</code> 重新进入\r\nasync 上下文。</p>')),
    (b'<p>This function panics if called from a <a href="../runtime/struct.Builder.html#method.new_current_thread" title="associated function tokio::runtime::Builder::new_current_thread"><code>current_thread</code></a> runtime.</p>',
     E('<p>如果从 <a href="../runtime/struct.Builder.html#method.new_current_thread" title="associated function tokio::runtime::Builder::new_current_thread"><code>current_thread</code></a> 运行时调用，此函数会 panic。</p>')),
])


if __name__ == '__main__':
    main()
