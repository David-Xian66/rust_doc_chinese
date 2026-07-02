#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Translate untranslated <p> blocks in tokio/io/ files to Chinese.

Strategy: bytes-mode replace, single-pass per file, target all 703 blocks.
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
PLAN = []


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


# ============================================================
# Common phrases shared across multiple files
# (Use larger unique patterns to avoid false matches)
# ============================================================
COMMON_PAIRS = [
    # Universal: "Returns the argument unchanged."
    (E('<p>Returns the argument unchanged.</p>'),
     E('<p>原样返回参数。</p>')),
    # Universal: "Calls <code>U::from(self)</code>."
    (E('<p>Calls <code>U::from(self)</code>.</p>'),
     E('<p>调用 <code>U::from(self)</code>。</p>')),
    # Universal: "That is, this conversion is whatever the implementation of...From<T> for U...chooses to do."
    (E('<p>That is, this conversion is whatever the implementation of\n<code><a href="https://doc.rust-lang.org/1.95.0/core/convert/trait.From.html" title="trait core::convert::From">From</a>&lt;T&gt; for U</code> chooses to do.</p>'),
     E('<p>也就是说，此转换就是 <code><a href="https://doc.rust-lang.org/1.95.0/core/convert/trait.From.html" title="trait core::convert::From">From</a>&lt;T&gt; for U</code> 的实现所选择的操作。</p>')),
    # Equivalent to:
    (E('<p>Equivalent to:</p>'),
     E('<p>等价于：</p>')),
    # This method is cancel safe.
    (E('<p>This method is cancel safe. If you use it as the event in a\n<a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> statement and some other branch\ncompletes first, then it is guaranteed that no data was read.</p>'),
     E('<p>此方法是可取消安全的。如果你在 <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> 语句中将其作为事件，\n而其他分支先完成，则保证不会读取任何数据。</p>')),
    # This method is cancellation safe.
    (E('<p>This method is cancellation safe.</p>'),
     E('<p>此方法是可取消安全的。</p>')),
    # This method is not cancellation safe.
    (E('<p>This method is not cancellation safe. If the method is used as the\nevent in a <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> statement and some\nother branch completes first, then some data may already have been\nread into <code>buf</code>.</p>'),
     E('<p>此方法不可取消安全。如果在 <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> 语句中将其作为事件，\n而其他分支先完成，则可能有部分数据已经被读入 <code>buf</code>。</p>')),
    (E('<p>This method is not cancellation safe. If the method is used as the\nevent in a <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> statement and some\nother branch completes first, then some data may be lost.</p>'),
     E('<p>此方法不可取消安全。如果在 <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> 语句中将其作为事件，\n而其他分支先完成，则可能会丢失部分数据。</p>')),
    (E('<p>This method is not cancellation safe. If the method is used as the\nevent in a <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> statement and some\nother branch completes first, then some data may have been partially\nread, and this data is lost. There are no guarantees regarding the\ncontents of <code>buf</code> when the call is cancelled. The current\nimplementation replaces <code>buf</code> with the empty string, but this may\nchange in the future.</p>'),
     E('<p>此方法不可取消安全。如果在 <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> 语句中将其作为事件，\n而其他分支先完成，则可能有部分数据被读取并且这些数据会丢失。\n当调用被取消时，不保证 <code>buf</code> 的内容。\n当前实现会将 <code>buf</code> 替换为空字符串，但未来可能会更改。</p>')),
    # dyn compatibility
    (E('<p>This trait is <b>not</b> <a href="https://doc.rust-lang.org/1.95.0/reference/items/traits.html#dyn-compatibility">dyn compatible</a>.</p>'),
     E('<p>此 trait <b>不</b>支持 <a href="https://doc.rust-lang.org/1.95.0/reference/items/traits.html#dyn-compatibility">dyn 兼容性</a>。</p>')),
    (E('<p><i>In older versions of Rust, dyn compatibility was called "object safety", so this trait is not object safe.</i></p>'),
     E('<p><i>在旧版 Rust 中，dyn 兼容性被称为 "object safety"（对象安全），因此此 trait 不是对象安全的。</i></p>')),
]


# ============================================================
# io/struct.BufReader.html (24 issues)
# ============================================================
add('io/struct.BufReader.html', [
    (E('<p>The <code>BufReader</code> struct adds buffering to any reader.</p>'),
     E('<p><code>BufReader</code> 结构体为任何读取器添加缓冲。</p>')),
    (E('<p>It can be excessively inefficient to work directly with a <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a>\ninstance. A <code>BufReader</code> performs large, infrequent reads on the underlying\n<a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> and maintains an in-memory buffer of the results.</p>'),
     E('<p>直接使用 <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> 实例的效率可能非常低下。\n<code>BufReader</code> 在底层的 <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> 上执行少量且不频繁的大块读取，并维护结果到内存缓冲区。</p>')),
    (E('<p><code>BufReader</code> can improve the speed of programs that make <em>small</em> and\n<em>repeated</em> read calls to the same file or network socket. It does not\nhelp when reading very large amounts at once, or reading just one or a few\ntimes. It also provides no advantage when reading from a source that is\nalready in memory, like a <code>Vec&lt;u8&gt;</code>.</p>'),
     E('<p><code>BufReader</code> 可以提升对同一文件或网络套接字进行<em>少量</em>且<em>重复</em>读取调用的程序速度。\n但它在一次性读取大量数据、只读一次或几次的情况下没有帮助。\n对于从内存中读取的数据（如 <code>Vec&lt;u8&gt;</code>），它也不会带来任何优势。</p>')),
    (E('<p>When the <code>BufReader</code> is dropped, the contents of its buffer will be\ndiscarded. Creating multiple instances of a <code>BufReader</code> on the same\nstream can cause data loss.</p>'),
     E('<p>当 <code>BufReader</code> 被丢弃时，其缓冲区中的内容也会被丢弃。\n在同一流上创建多个 <code>BufReader</code> 实例可能会导致数据丢失。</p>')),
    (E('<p>Creates a new <code>BufReader</code> with a default buffer capacity. The default is currently 8 KB,\nbut may change in the future.</p>'),
     E('<p>使用默认缓冲区容量创建一个新的 <code>BufReader</code>。当前默认为 8 KB，但未来可能会更改。</p>')),
    (E('<p>Creates a new <code>BufReader</code> with the specified buffer capacity.</p>'),
     E('<p>使用指定的缓冲区容量创建一个新的 <code>BufReader</code>。</p>')),
    (E('<p>Gets a reference to the underlying reader.</p>'),
     E('<p>获取底层读取器的引用。</p>')),
    (E('<p>It is inadvisable to directly read from the underlying reader.</p>'),
     E('<p>不建议直接读取底层读取器。</p>')),
    (E('<p>Gets a mutable reference to the underlying reader.</p>'),
     E('<p>获取底层读取器的可变引用。</p>')),
    (E('<p>Gets a pinned mutable reference to the underlying reader.</p>'),
     E('<p>获取底层读取器的固定可变引用（pinned mutable reference）。</p>')),
    (E('<p>Consumes this <code>BufReader</code>, returning the underlying reader.</p>'),
     E('<p>消耗此 <code>BufReader</code>，返回底层的读取器。</p>')),
    (E('<p>Note that any leftover data in the internal buffer is lost.</p>'),
     E('<p>注意，内部缓冲区中任何剩余的数据都将丢失。</p>')),
    (E('<p>Returns a reference to the internally buffered data.</p>'),
     E('<p>返回对内部缓冲数据的引用。</p>')),
    (E('<p>Unlike <code>fill_buf</code>, this will not attempt to fill the buffer if it is empty.</p>'),
     E('<p>与 <code>fill_buf</code> 不同，如果缓冲区为空，此方法不会尝试填充它。</p>')),
    (E('<p>Seeks to an offset, in bytes, in the underlying reader.</p>'),
     E('<p>在底层读取器中按字节偏移量定位。</p>')),
    (E('<p>The position used for seeking with <code>SeekFrom::Current(_)</code> is the\nposition the underlying reader would be at if the <code>BufReader</code> had no\ninternal buffer.</p>'),
     E('<p>使用 <code>SeekFrom::Current(_)</code> 进行定位时，所用的位置是假设 <code>BufReader</code> 没有内部缓冲区时底层读取器应处的位置。</p>')),
    (E('<p>Seeking always discards the internal buffer, even if the seek position\nwould otherwise fall within it. This guarantees that calling\n<code>.into_inner()</code> immediately after a seek yields the underlying reader\nat the same position.</p>'),
     E('<p>定位操作始终会丢弃内部缓冲区，即使定位的位置本应落在该缓冲区内。\n这保证在定位之后立即调用 <code>.into_inner()</code> 得到的底层读取器与定位时所处的位置一致。</p>')),
    (E('<p>See <a href="trait.AsyncSeek.html" title="trait tokio::io::AsyncSeek"><code>AsyncSeek</code></a> for more details.</p>'),
     E('<p>更多详情请参阅 <a href="trait.AsyncSeek.html" title="trait tokio::io::AsyncSeek"><code>AsyncSeek</code></a>。</p>')),
    (E('<p>Note: In the edge case where you’re seeking with <code>SeekFrom::Current(n)</code>\nwhere <code>n</code> minus the internal buffer length overflows an <code>i64</code>, two\nseeks will be performed instead of one. If the second seek returns\n<code>Err</code>, the underlying reader will be left at the same position it would\nhave if you called <code>seek</code> with <code>SeekFrom::Current(0)</code>.</p>'),
     E('<p>注意：在边界情况下，当你使用 <code>SeekFrom::Current(n)</code> 进行定位时，如果 <code>n</code> 减去内部缓冲区长度会溢出 <code>i64</code>，则会执行两次定位而不是一次。\n如果第二次定位返回 <code>Err</code>，则底层读取器将停留在与使用 <code>SeekFrom::Current(0)</code> 调用 <code>seek</code> 相同的位置上。</p>')),
])


# ============================================================
# io/struct.BufStream.html (22 issues)
# ============================================================
add('io/struct.BufStream.html', [
    (E('<p>Wraps a type that is <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> and <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a>, and buffers its input and output.</p>'),
     E('<p>包装一个同时实现 <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> 和 <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> 的类型，并对其输入和输出进行缓冲。</p>')),
    (E('<p>It can be excessively inefficient to work directly with something that implements <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a>\nand <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a>. For example, every <code>write</code>, however small, has to traverse the syscall\ninterface, and similarly, every read has to do the same. The <a href="struct.BufWriter.html" title="struct tokio::io::BufWriter"><code>BufWriter</code></a> and <a href="struct.BufReader.html" title="struct tokio::io::BufReader"><code>BufReader</code></a>\ntypes aid with these problems respectively, but do so in only one direction. <code>BufStream</code> wraps\none in the other so that both directions are buffered. See their documentation for details.</p>'),
     E('<p>直接使用同时实现 <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> 和 <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> 的类型可能效率很低。\n例如，无论 <code>write</code> 多小都必须经过系统调用接口，每次读取也是如此。\n<a href="struct.BufWriter.html" title="struct tokio::io::BufWriter"><code>BufWriter</code></a> 和 <a href="struct.BufReader.html" title="struct tokio::io::BufReader"><code>BufReader</code></a> 分别用来缓解这两个问题，但只能在一个方向上起作用。\n<code>BufStream</code> 将其中一个包装在另一个之中，使两个方向都被缓冲。详情请参阅它们的文档。</p>')),
    (E('<p>Wraps a type in both <a href="struct.BufWriter.html" title="struct tokio::io::BufWriter"><code>BufWriter</code></a> and <a href="struct.BufReader.html" title="struct tokio::io::BufReader"><code>BufReader</code></a>.</p>'),
     E('<p>将一个类型同时包装到 <a href="struct.BufWriter.html" title="struct tokio::io::BufWriter"><code>BufWriter</code></a> 和 <a href="struct.BufReader.html" title="struct tokio::io::BufReader"><code>BufReader</code></a> 中。</p>')),
    (E('<p>See the documentation for those types and <a href="struct.BufStream.html" title="struct tokio::io::BufStream"><code>BufStream</code></a> for details.</p>'),
     E('<p>详情请参阅这些类型以及 <a href="struct.BufStream.html" title="struct tokio::io::BufStream"><code>BufStream</code></a> 的文档。</p>')),
    (E('<p>Creates a <code>BufStream</code> with the specified <a href="struct.BufReader.html" title="struct tokio::io::BufReader"><code>BufReader</code></a> capacity and <a href="struct.BufWriter.html" title="struct tokio::io::BufWriter"><code>BufWriter</code></a>\ncapacity.</p>'),
     E('<p>使用指定的 <a href="struct.BufReader.html" title="struct tokio::io::BufReader"><code>BufReader</code></a> 容量和 <a href="struct.BufWriter.html" title="struct tokio::io::BufWriter"><code>BufWriter</code></a> 容量创建一个 <code>BufStream</code>。</p>')),
    (E('<p>Gets a reference to the underlying I/O object.</p>'),
     E('<p>获取底层 I/O 对象的引用。</p>')),
    (E('<p>It is inadvisable to directly read from the underlying I/O object.</p>'),
     E('<p>不建议直接从底层 I/O 对象进行读取。</p>')),
    (E('<p>Gets a mutable reference to the underlying I/O object.</p>'),
     E('<p>获取底层 I/O 对象的可变引用。</p>')),
    (E('<p>Gets a pinned mutable reference to the underlying I/O object.</p>'),
     E('<p>获取底层 I/O 对象的固定可变引用。</p>')),
    (E('<p>Consumes this <code>BufStream</code>, returning the underlying I/O object.</p>'),
     E('<p>消耗此 <code>BufStream</code>，返回底层的 I/O 对象。</p>')),
    (E('<p>Seek to an offset, in bytes, in the underlying stream.</p>'),
     E('<p>在底层流中按字节偏移量定位。</p>')),
    (E('<p>The position used for seeking with <code>SeekFrom::Current(_)</code> is the\nposition the underlying stream would be at if the <code>BufStream</code> had no\ninternal buffer.</p>'),
     E('<p>使用 <code>SeekFrom::Current(_)</code> 进行定位时，所用的位置是假设 <code>BufStream</code> 没有内部缓冲区时底层流应处的位置。</p>')),
    (E('<p>Seeking always discards the internal buffer, even if the seek position\nwould otherwise fall within it. This guarantees that calling\n<code>.into_inner()</code> immediately after a seek yields the underlying reader\nat the same position.</p>'),
     E('<p>定位操作始终会丢弃内部缓冲区，即使定位的位置本应落在该缓冲区内。\n这保证在定位之后立即调用 <code>.into_inner()</code> 得到的底层读取器与定位时所处的位置一致。</p>')),
    (E('<p>See <a href="trait.AsyncSeek.html" title="trait tokio::io::AsyncSeek"><code>AsyncSeek</code></a> for more details.</p>'),
     E('<p>更多详情请参阅 <a href="trait.AsyncSeek.html" title="trait tokio::io::AsyncSeek"><code>AsyncSeek</code></a>。</p>')),
    (E('<p>Note: In the edge case where you’re seeking with <code>SeekFrom::Current(n)</code>\nwhere <code>n</code> minus the internal buffer length overflows an <code>i64</code>, two\nseeks will be performed instead of one. If the second seek returns\n<code>Err</code>, the underlying reader will be left at the same position it would\nhave if you called <code>seek</code> with <code>SeekFrom::Current(0)</code>.</p>'),
     E('<p>注意：在边界情况下，当你使用 <code>SeekFrom::Current(n)</code> 进行定位时，如果 <code>n</code> 减去内部缓冲区长度会溢出 <code>i64</code>，则会执行两次定位而不是一次。\n如果第二次定位返回 <code>Err</code>，则底层读取器将停留在与使用 <code>SeekFrom::Current(0)</code> 调用 <code>seek</code> 相同的位置上。</p>')),
])


# ============================================================
# io/struct.BufWriter.html (19 issues)
# ============================================================
add('io/struct.BufWriter.html', [
    (E('<p>Wraps a writer and buffers its output.</p>'),
     E('<p>包装一个写入器并对其输出进行缓冲。</p>')),
    (E('<p>It can be excessively inefficient to work directly with something that\nimplements <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a>. A <code>BufWriter</code> keeps an in-memory buffer of data and\nwrites it to an underlying writer in large, infrequent batches.</p>'),
     E('<p>直接使用实现 <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> 的类型可能效率很低。\n<code>BufWriter</code> 在内存中维护一个数据缓冲区，然后以少量但较大的批次写入到底层写入器。</p>')),
    (E('<p><code>BufWriter</code> can improve the speed of programs that make <em>small</em> and\n<em>repeated</em> write calls to the same file or network socket. It does not\nhelp when writing very large amounts at once, or writing just one or a few\ntimes. It also provides no advantage when writing to a destination that is\nin memory, like a <code>Vec&lt;u8&gt;</code>.</p>'),
     E('<p><code>BufWriter</code> 可以提升对同一文件或网络套接字进行<em>少量</em>且<em>重复</em>写入调用的程序速度。\n但它在一次性写入大量数据、只写一次或几次的情况下没有帮助。\n对于写入到内存中的目标（如 <code>Vec&lt;u8&gt;</code>），它也不会带来任何优势。</p>')),
    (E('<p>When the <code>BufWriter</code> is dropped, the contents of its buffer will be\ndiscarded. Creating multiple instances of a <code>BufWriter</code> on the same\nstream can cause data loss. If you need to write out the contents of its\nbuffer, you must manually call flush before the writer is dropped.</p>'),
     E('<p>当 <code>BufWriter</code> 被丢弃时，其缓冲区中的内容也会被丢弃。\n在同一流上创建多个 <code>BufWriter</code> 实例可能会导致数据丢失。\n如果需要将缓冲区内容写出，则必须在写入器被丢弃之前手动调用 flush。</p>')),
    (E('<p>Creates a new <code>BufWriter</code> with a default buffer capacity. The default is currently 8 KB,\nbut may change in the future.</p>'),
     E('<p>使用默认缓冲区容量创建一个新的 <code>BufWriter</code>。当前默认为 8 KB，但未来可能会更改。</p>')),
    (E('<p>Creates a new <code>BufWriter</code> with the specified buffer capacity.</p>'),
     E('<p>使用指定的缓冲区容量创建一个新的 <code>BufWriter</code>。</p>')),
    (E('<p>Gets a reference to the underlying writer.</p>'),
     E('<p>获取底层写入器的引用。</p>')),
    (E('<p>Gets a mutable reference to the underlying writer.</p>'),
     E('<p>获取底层写入器的可变引用。</p>')),
    (E('<p>It is inadvisable to directly write to the underlying writer.</p>'),
     E('<p>不建议直接写入到底层写入器。</p>')),
    (E('<p>Gets a pinned mutable reference to the underlying writer.</p>'),
     E('<p>获取底层写入器的固定可变引用。</p>')),
    (E('<p>Consumes this <code>BufWriter</code>, returning the underlying writer.</p>'),
     E('<p>消耗此 <code>BufWriter</code>，返回底层的写入器。</p>')),
    (E('<p>Returns a reference to the internally buffered data.</p>'),
     E('<p>返回对内部缓冲数据的引用。</p>')),
    (E('<p>Seek to the offset, in bytes, in the underlying writer.</p>'),
     E('<p>在底层写入器中按字节偏移量定位。</p>')),
    (E('<p>Seeking always writes out the internal buffer before seeking.</p>'),
     E('<p>定位前始终会先写出内部缓冲区的内容。</p>')),
])


# ============================================================
# io/struct.Chain.html (10 issues)
# ============================================================
add('io/struct.Chain.html', [
    (E('<p>Stream for the <a href="trait.AsyncReadExt.html#method.chain" title="method tokio::io::AsyncReadExt::chain"><code>chain</code></a> method.</p>'),
     E('<p><a href="trait.AsyncReadExt.html#method.chain" title="method tokio::io::AsyncReadExt::chain"><code>chain</code></a> 方法返回的流。</p>')),
    (E('<p>Gets references to the underlying readers in this <code>Chain</code>.</p>'),
     E('<p>获取此 <code>Chain</code> 中底层读取器的引用。</p>')),
    (E('<p>Gets mutable references to the underlying readers in this <code>Chain</code>.</p>'),
     E('<p>获取此 <code>Chain</code> 中底层读取器的可变引用。</p>')),
    (E('<p>Care should be taken to avoid modifying the internal I/O state of the\nunderlying readers as doing so may corrupt the internal state of this\n<code>Chain</code>.</p>'),
     E('<p>注意不要修改底层读取器的内部 I/O 状态，\n因为这样做可能会破坏此 <code>Chain</code> 的内部状态。</p>')),
    (E('<p>Gets pinned mutable references to the underlying readers in this <code>Chain</code>.</p>'),
     E('<p>获取此 <code>Chain</code> 中底层读取器的固定可变引用。</p>')),
    (E('<p>Consumes the <code>Chain</code>, returning the wrapped readers.</p>'),
     E('<p>消耗此 <code>Chain</code>，返回被包装的读取器。</p>')),
])


# ============================================================
# io/struct.Interest.html (19 issues)
# ============================================================
add('io/struct.Interest.html', [
    (E('<p>Readiness event interest.</p>'),
     E('<p>就绪事件关注项（interest）。</p>')),
    (E('<p>Specifies the readiness events the caller is interested in when awaiting on\nI/O resource readiness states.</p>'),
     E('<p>指定在等待 I/O 资源就绪状态时调用方感兴趣的就绪事件。</p>')),
    (E('<p>Interest in all readable events.</p>'),
     E('<p>对所有可读事件感兴趣。</p>')),
    (E('<p>Readable interest includes read-closed events.</p>'),
     E('<p>可读兴趣包含读关闭事件。</p>')),
    (E('<p>Interest in all writable events.</p>'),
     E('<p>对所有可写事件感兴趣。</p>')),
    (E('<p>Writable interest includes write-closed events.</p>'),
     E('<p>可写兴趣包含写关闭事件。</p>')),
    (E('<p>Interest in error events.</p>'),
     E('<p>对错误事件感兴趣。</p>')),
    (E('<p>Passes error interest to the underlying OS selector.\nBehavior is platform-specific, read your platform’s documentation.</p>'),
     E('<p>将错误兴趣传递给底层 OS 选择器。\n行为因平台而异，请阅读你所使用平台的文档。</p>')),
    (E('<p>Returns true if the value includes readable interest.</p>'),
     E('<p>如果该值包含可读兴趣，则返回 true。</p>')),
    (E('<p>Returns true if the value includes writable interest.</p>'),
     E('<p>如果该值包含可写兴趣，则返回 true。</p>')),
    (E('<p>Returns true if the value includes error interest.</p>'),
     E('<p>如果该值包含错误兴趣，则返回 true。</p>')),
    (E('<p>Add together two <code>Interest</code> values.</p>'),
     E('<p>将两个 <code>Interest</code> 值相加。</p>')),
    (E('<p>This function works from a <code>const</code> context.</p>'),
     E('<p>此函数可以在 <code>const</code> 上下文中使用。</p>')),
    (E('<p>Remove <code>Interest</code> from <code>self</code>.</p>'),
     E('<p>从 <code>self</code> 中移除 <code>Interest</code>。</p>')),
    (E('<p>Interests present in <code>other</code> but <em>not</em> in <code>self</code> are ignored.</p>'),
     E('<p>仅移除 <code>self</code> 中存在的那些 <code>Interest</code>；\n存在于 <code>other</code> 但<em>不</em>存在于 <code>self</code> 中的兴趣将被忽略。</p>')),
    (E('<p>Returns <code>None</code> if the set would be empty after removing <code>Interest</code>.</p>'),
     E('<p>如果在移除 <code>Interest</code> 后集合为空，则返回 <code>None</code>。</p>')),
])


# ============================================================
# io/struct.Join.html (11 issues)
# ============================================================
add('io/struct.Join.html', [
    (E('<p>Joins two values implementing <code>AsyncRead</code> and <code>AsyncWrite</code> into a\nsingle handle.</p>'),
     E('<p>将分别实现 <code>AsyncRead</code> 和 <code>AsyncWrite</code> 的两个值合并为单个句柄。</p>')),
    (E('<p>Splits this <code>Join</code> back into its <code>AsyncRead</code> and <code>AsyncWrite</code>\ncomponents.</p>'),
     E('<p>将此 <code>Join</code> 拆分回其 <code>AsyncRead</code> 和 <code>AsyncWrite</code> 组件。</p>')),
    (E('<p>Returns a reference to the inner reader.</p>'),
     E('<p>返回对内部读取器的引用。</p>')),
    (E('<p>Returns a reference to the inner writer.</p>'),
     E('<p>返回对内部写入器的引用。</p>')),
    (E('<p>Returns a mutable reference to the inner reader.</p>'),
     E('<p>返回对内部读取器的可变引用。</p>')),
    (E('<p>Returns a mutable reference to the inner writer.</p>'),
     E('<p>返回对内部写入器的可变引用。</p>')),
    (E('<p>Returns a pinned mutable reference to the inner reader.</p>'),
     E('<p>返回对内部读取器的固定可变引用。</p>')),
    (E('<p>Returns a pinned mutable reference to the inner writer.</p>'),
     E('<p>返回对内部写入器的固定可变引用。</p>')),
])


# ============================================================
# io/struct.Lines.html (15 issues)
# ============================================================
add('io/struct.Lines.html', [
    (E('<p>Reads lines from an <a href="trait.AsyncBufRead.html" title="trait tokio::io::AsyncBufRead"><code>AsyncBufRead</code></a>.</p>'),
     E('<p>从 <a href="trait.AsyncBufRead.html" title="trait tokio::io::AsyncBufRead"><code>AsyncBufRead</code></a> 读取行。</p>')),
    (E('<p>A <code>Lines</code> can be turned into a <code>Stream</code> with <a href="https://docs.rs/tokio-stream/0.1/tokio_stream/wrappers/struct.LinesStream.html"><code>LinesStream</code></a>.</p>'),
     E('<p><code>Lines</code> 可以通过 <a href="https://docs.rs/tokio-stream/0.1/tokio_stream/wrappers/struct.LinesStream.html"><code>LinesStream</code></a> 转换为 <code>Stream</code>。</p>')),
    (E('<p>This type is usually created using the <a href="trait.AsyncBufReadExt.html#method.lines" title="method tokio::io::AsyncBufReadExt::lines"><code>lines</code></a> method.</p>'),
     E('<p>此类型通常通过 <a href="trait.AsyncBufReadExt.html#method.lines" title="method tokio::io::AsyncBufReadExt::lines"><code>lines</code></a> 方法创建。</p>')),
    (E('<p>Returns the next line in the stream.</p>'),
     E('<p>返回流中的下一行。</p>')),
    (E('<p>Obtains a mutable reference to the underlying reader.</p>'),
     E('<p>获取底层读取器的可变引用。</p>')),
    (E('<p>Obtains a reference to the underlying reader.</p>'),
     E('<p>获取底层读取器的引用。</p>')),
    (E('<p>Unwraps this <code>Lines&lt;R&gt;</code>, returning the underlying reader.</p>'),
     E('<p>解包此 <code>Lines&lt;R&gt;</code>，返回底层的读取器。</p>')),
    (E('<p>Note that any leftover data in the internal buffer is lost.\nTherefore, a following read from the underlying reader may lead to data loss.</p>'),
     E('<p>注意，内部缓冲区中任何剩余的数据都会丢失。\n因此，接下来从底层读取器进行读取可能会导致数据丢失。</p>')),
    (E('<p>Polls for the next line in the stream.</p>'),
     E('<p>轮询流中的下一行。</p>')),
    (E('<p>This method returns:</p>'),
     E('<p>此方法返回：</p>')),
    (E('<p>When the method returns <code>Poll::Pending</code>, the <code>Waker</code> in the provided\n<code>Context</code> is scheduled to receive a wakeup when more bytes become\navailable on the underlying IO resource.  Note that on multiple calls to\n<code>poll_next_line</code>, only the <code>Waker</code> from the <code>Context</code> passed to the most\nrecent call is scheduled to receive a wakeup.</p>'),
     E('<p>当方法返回 <code>Poll::Pending</code> 时，传入的 <code>Context</code> 中的 <code>Waker</code> 会被调度，\n以便在底层 I/O 资源上有更多字节可用时收到唤醒通知。\n请注意，对 <code>poll_next_line</code> 的多次调用中，\n只有最近一次调用传入的 <code>Context</code> 中的 <code>Waker</code> 会被调度接收唤醒。</p>')),
])


# ============================================================
# io/struct.ReadBuf.html (43 issues)
# ============================================================
add('io/struct.ReadBuf.html', [
    (E('<p>A wrapper around a byte buffer that is incrementally filled and initialized.</p>'),
     E('<p>对字节缓冲区的包装，以增量方式填充和初始化。</p>')),
    (E('<p>This type is a sort of \xe2\x80\x9cdouble cursor\xe2\x80\x9d. It tracks three regions in the\nbuffer: a region at the beginning of the buffer that has been logically\nfilled with data, a region that has been initialized at some point but not\nyet logically filled, and a region at the end that may be uninitialized.\nThe filled region is guaranteed to be a subset of the initialized region.</p>'),
     E('<p>此类型类似于\xe2\x80\x9c双光标\xe2\x80\x9d。它在缓冲区中跟踪三个区域：\n缓冲区开头处已经被逻辑填充数据的区域、\n曾经被初始化但尚未被逻辑填充的区域，\n以及末尾可能未被初始化的区域。\n已填充区域保证是已初始化区域的子集。</p>')),
    (E('<p>In summary, the contents of the buffer can be visualized as:</p>'),
     E('<p>概括而言，缓冲区的内容可以可视化如下：</p>')),
    (E('<p>It is undefined behavior to de-initialize any bytes from the uninitialized\nregion, since it is merely unknown whether this region is uninitialized or\nnot, and if part of it turns out to be initialized, it must stay initialized.</p>'),
     E('<p>对未初始化区域中的任何字节执行反初始化是未定义行为，\n因为仅仅是不清楚该区域是否已初始化；\n如果其中某些部分实际上是已初始化的，那么它必须保持已初始化状态。</p>')),
    (E('<p>Creates a new <code>ReadBuf</code> from a fully initialized buffer.</p>'),
     E('<p>从一个完全初始化的缓冲区创建一个新的 <code>ReadBuf</code>。</p>')),
    (E('<p>Creates a new <code>ReadBuf</code> from a buffer that may be uninitialized.</p>'),
     E('<p>从一个可能未初始化的缓冲区创建一个新的 <code>ReadBuf</code>。</p>')),
    (E('<p>The internal cursor will mark the entire buffer as uninitialized. If\nthe buffer is known to be partially initialized, then use <code>assume_init</code>\nto move the internal cursor.</p>'),
     E('<p>内部光标会将整个缓冲区标记为未初始化。\n如果已知缓冲区是部分初始化的，那么可以使用 <code>assume_init</code> 来移动内部光标。</p>')),
    (E('<p>Returns the total capacity of the buffer.</p>'),
     E('<p>返回缓冲区的总容量。</p>')),
    (E('<p>Returns a shared reference to the filled portion of the buffer.</p>'),
     E('<p>返回对缓冲区已填充部分的共享引用。</p>')),
    (E('<p>Returns a mutable reference to the filled portion of the buffer.</p>'),
     E('<p>返回对缓冲区已填充部分的可变引用。</p>')),
    (E('<p>Returns a new <code>ReadBuf</code> comprised of the unfilled section up to <code>n</code>.</p>'),
     E('<p>返回一个由至多 <code>n</code> 个未填充字节组成的新 <code>ReadBuf</code>。</p>')),
    (E('<p>Returns a shared reference to the initialized portion of the buffer.</p>'),
     E('<p>返回对缓冲区已初始化部分的共享引用。</p>')),
    (E('<p>This includes the filled portion.</p>'),
     E('<p>其中包括已填充的部分。</p>')),
    (E('<p>Returns a mutable reference to the initialized portion of the buffer.</p>'),
     E('<p>返回对缓冲区已初始化部分的可变引用。</p>')),
    (E('<p>Returns a mutable reference to the entire buffer, without ensuring that it has been fully\ninitialized.</p>'),
     E('<p>返回对整个缓冲区的可变引用，不保证它已被完全初始化。</p>')),
    (E('<p>The elements between 0 and <code>self.filled().len()</code> are filled, and those between 0 and\n<code>self.initialized().len()</code> are initialized (and so can be converted to a <code>&amp;mut [u8]</code>).</p>'),
     E('<p>下标在 0 到 <code>self.filled().len()</code> 之间的元素已被填充，\n0 到 <code>self.initialized().len()</code> 之间的元素已被初始化（因此可以转换为 <code>&amp;mut [u8]</code>）。</p>')),
    (E('<p>The caller of this method must ensure that these invariants are upheld. For example, if the\ncaller initializes some of the uninitialized section of the buffer, it must call\n<a href="struct.ReadBuf.html#method.assume_init" title="method tokio::io::ReadBuf::assume_init"><code>assume_init</code></a> with the number of bytes initialized.</p>'),
     E('<p>此方法的调用方必须确保这些不变量得到遵守。\n例如，如果调用方对缓冲区中部分未初始化部分执行了初始化，\n则必须使用已初始化的字节数调用 <a href="struct.ReadBuf.html#method.assume_init" title="method tokio::io::ReadBuf::assume_init"><code>assume_init</code></a>。</p>')),
    (E('<p>The caller must not de-initialize portions of the buffer that have already been initialized.\nThis includes any bytes in the region marked as uninitialized by <code>ReadBuf</code>.</p>'),
     E('<p>调用方不得对已经初始化的缓冲区部分执行反初始化。\n其中也包括被 <code>ReadBuf</code> 标记为未初始化区域中的任何字节。</p>')),
    (E('<p>Returns a mutable reference to the unfilled part of the buffer without ensuring that it has been fully\ninitialized.</p>'),
     E('<p>返回对缓冲区未填充部分的可变引用，不保证它已被完全初始化。</p>')),
    (E('<p>Returns a mutable reference to the unfilled part of the buffer, ensuring it is fully initialized.</p>'),
     E('<p>返回对缓冲区未填充部分的可变引用，确保它已被完全初始化。</p>')),
    (E('<p>Since <code>ReadBuf</code> tracks the region of the buffer that has been initialized, this is effectively \xe2\x80\x9cfree\xe2\x80\x9d after\nthe first use.</p>'),
     E('<p>由于 <code>ReadBuf</code> 会跟踪缓冲区中已初始化的区域，\n所以在首次使用之后，这个操作实际上是\xe2\x80\x9c免费\xe2\x80\x9d的。</p>')),
    (E('<p>Returns a mutable reference to the first <code>n</code> bytes of the unfilled part of the buffer, ensuring it is\nfully initialized.</p>'),
     E('<p>返回对缓冲区未填充部分前 <code>n</code> 个字节的可变引用，确保它们已被完全初始化。</p>')),
    (E('<p>Panics if <code>self.remaining()</code> is less than <code>n</code>.</p>'),
     E('<p>如果 <code>self.remaining()</code> 小于 <code>n</code>，则 panic。</p>')),
    (E('<p>Returns the number of bytes at the end of the slice that have not yet been filled.</p>'),
     E('<p>返回切片末尾尚未填充的字节数。</p>')),
    (E('<p>Clears the buffer, resetting the filled region to empty.</p>'),
     E('<p>清空缓冲区，将已填充区域重置为空。</p>')),
    (E('<p>The number of initialized bytes is not changed, and the contents of the buffer are not modified.</p>'),
     E('<p>已初始化的字节数保持不变，缓冲区的内容也不会被修改。</p>')),
    (E('<p>Advances the size of the filled region of the buffer.</p>'),
     E('<p>推进缓冲区已填充区域的大小。</p>')),
    (E('<p>Panics if the filled region of the buffer would become larger than the initialized region.</p>'),
     E('<p>如果缓冲区已填充区域变得大于已初始化区域，则 panic。</p>')),
    (E('<p>Sets the size of the filled region of the buffer.</p>'),
     E('<p>设置缓冲区已填充区域的大小。</p>')),
    (E('<p>Note that this can be used to <em>shrink</em> the filled region of the buffer in addition to growing it (for\nexample, by a <code>AsyncRead</code> implementation that compresses data in-place).</p>'),
     E('<p>请注意，除了扩大已填充区域之外，\n此方法也可以用来<em>缩小</em>已填充区域（例如，由 <code>AsyncRead</code> 实现原地压缩数据时）。</p>')),
    (E('<p>Asserts that the first <code>n</code> unfilled bytes of the buffer are initialized.</p>'),
     E('<p>断言缓冲区中前 <code>n</code> 个未填充字节已被初始化。</p>')),
    (E('<p><code>ReadBuf</code> assumes that bytes are never de-initialized, so this method does nothing when called with fewer\nbytes than are already known to be initialized.</p>'),
     E('<p><code>ReadBuf</code> 假定字节永远不会被反初始化，\n因此当使用比已知已初始化字节数更少的字节调用此方法时，它不会执行任何操作。</p>')),
    (E('<p>The caller must ensure that <code>n</code> unfilled bytes of the buffer have already been initialized.</p>'),
     E('<p>调用方必须确保缓冲区中 <code>n</code> 个未填充字节已被初始化。</p>')),
    (E('<p>Appends data to the buffer, advancing the written position and possibly also the initialized position.</p>'),
     E('<p>将数据追加到缓冲区，推进已写入位置，并可能也会推进已初始化位置。</p>')),
    (E('<p>Panics if <code>self.remaining()</code> is less than <code>buf.len()</code>.</p>'),
     E('<p>如果 <code>self.remaining()</code> 小于 <code>buf.len()</code>，则 panic。</p>')),
])# ============================================================
# io/struct.ReadHalf.html (7 issues)
# ============================================================
add('io/struct.ReadHalf.html', [
    (E('<p>The readable half of a value returned from <a href="fn.split.html" title="fn tokio::io::split"><code>split</code></a>.</p>'),
     E('<p>由 <a href="fn.split.html" title="fn tokio::io::split"><code>split</code></a> 返回的值的可读一半。</p>')),
    (E('<p>Checks if this <code>ReadHalf</code> and some <code>WriteHalf</code> were split from the same\nstream.</p>'),
     E('<p>检查此 <code>ReadHalf</code> 与某个 <code>WriteHalf</code> 是否从同一个流拆分而来。</p>')),
    (E('<p>Reunites with a previously split <code>WriteHalf</code>.</p>'),
     E('<p>与之前拆分出的 <code>WriteHalf</code> 重新合并。</p>')),
    (E('<p>If this <code>ReadHalf</code> and the given <code>WriteHalf</code> do not originate from the\nsame <code>split</code> operation this method will panic.\nThis can be checked ahead of time by calling <a href="struct.ReadHalf.html#method.is_pair_of" title="method tokio::io::ReadHalf::is_pair_of"><code>is_pair_of()</code></a>.</p>'),
     E('<p>如果此 <code>ReadHalf</code> 与给定的 <code>WriteHalf</code> 不是来自同一次 <code>split</code> 操作，\n此方法将 panic。\n可以事先通过调用 <a href="struct.ReadHalf.html#method.is_pair_of" title="method tokio::io::ReadHalf::is_pair_of"><code>is_pair_of()</code></a> 进行检查。</p>')),
])


# ============================================================
# io/struct.Ready.html (18 issues)
# ============================================================
add('io/struct.Ready.html', [
    (E('<p>Describes the readiness state of an I/O resources.</p>'),
     E('<p>描述 I/O 资源的就绪状态。</p>')),
    (E('<p><code>Ready</code> tracks which operation an I/O resource is ready to perform.</p>'),
     E('<p><code>Ready</code> 用于跟踪 I/O 资源已就绪可执行的操作。</p>')),
    (E('<p>Returns the empty <code>Ready</code> set.</p>'),
     E('<p>返回空的 <code>Ready</code> 集合。</p>')),
    (E('<p>Returns a <code>Ready</code> representing readable readiness.</p>'),
     E('<p>返回表示可读就绪的 <code>Ready</code>。</p>')),
    (E('<p>Returns a <code>Ready</code> representing writable readiness.</p>'),
     E('<p>返回表示可写就绪的 <code>Ready</code>。</p>')),
    (E('<p>Returns a <code>Ready</code> representing read closed readiness.</p>'),
     E('<p>返回表示读关闭就绪的 <code>Ready</code>。</p>')),
    (E('<p>Returns a <code>Ready</code> representing write closed readiness.</p>'),
     E('<p>返回表示写关闭就绪的 <code>Ready</code>。</p>')),
    (E('<p>Returns a <code>Ready</code> representing error readiness.</p>'),
     E('<p>返回表示错误就绪的 <code>Ready</code>。</p>')),
    (E('<p>Returns a <code>Ready</code> representing readiness for all operations.</p>'),
     E('<p>返回表示对所有操作都就绪的 <code>Ready</code>。</p>')),
    (E('<p>Returns true if <code>Ready</code> is the empty set.</p>'),
     E('<p>如果 <code>Ready</code> 是空集，则返回 true。</p>')),
    (E('<p>Returns <code>true</code> if the value includes <code>readable</code>.</p>'),
     E('<p>如果该值包含 <code>readable</code>，则返回 <code>true</code>。</p>')),
    (E('<p>Returns <code>true</code> if the value includes writable <code>readiness</code>.</p>'),
     E('<p>如果该值包含 writable <code>readiness</code>，则返回 <code>true</code>。</p>')),
    (E('<p>Returns <code>true</code> if the value includes read-closed <code>readiness</code>.</p>'),
     E('<p>如果该值包含 read-closed <code>readiness</code>，则返回 <code>true</code>。</p>')),
    (E('<p>Returns <code>true</code> if the value includes write-closed <code>readiness</code>.</p>'),
     E('<p>如果该值包含 write-closed <code>readiness</code>，则返回 <code>true</code>。</p>')),
    (E('<p>Returns <code>true</code> if the value includes error <code>readiness</code>.</p>'),
     E('<p>如果该值包含 error <code>readiness</code>，则返回 <code>true</code>。</p>')),
])


# ============================================================
# io/struct.SimplexStream.html (7 issues)
# ============================================================
add('io/struct.SimplexStream.html', [
    (E('<p>A unidirectional pipe to read and write bytes in memory.</p>'),
     E('<p>用于在内存中读写字节的单向管道。</p>')),
    (E('<p>It can be constructed by <a href="fn.simplex.html" title="fn tokio::io::simplex"><code>simplex</code></a> function which will create a pair of\nreader and writer or by calling <a href="struct.SimplexStream.html#method.new_unsplit" title="associated function tokio::io::SimplexStream::new_unsplit"><code>SimplexStream::new_unsplit</code></a> that will\ncreate a handle for both reading and writing.</p>'),
     E('<p>它可以通过 <a href="fn.simplex.html" title="fn tokio::io::simplex"><code>simplex</code></a> 函数构造，该函数会创建一对读取器和写入器；\n也可以通过调用 <a href="struct.SimplexStream.html#method.new_unsplit" title="associated function tokio::io::SimplexStream::new_unsplit"><code>SimplexStream::new_unsplit</code></a> 构造，\n该函数会创建一个既可读又可写的句柄。</p>')),
    (E('<p>Creates unidirectional buffer that acts like in memory pipe. To create split\nversion with separate reader and writer you can use <a href="fn.simplex.html" title="fn tokio::io::simplex"><code>simplex</code></a> function.</p>'),
     E('<p>创建一个像内存中管道一样的单向缓冲区。要创建带分离读取器和写入器的拆分版本，可以使用 <a href="fn.simplex.html" title="fn tokio::io::simplex"><code>simplex</code></a> 函数。</p>')),
    (E('<p>The <code>max_buf_size</code> argument is the maximum amount of bytes that can be\nwritten to a buffer before the it returns <code>Poll::Pending</code>.</p>'),
     E('<p><code>max_buf_size</code> 参数是在返回 <code>Poll::Pending</code> 之前可以写入缓冲区的最大字节数。</p>')),
])


# ============================================================
# io/struct.Split.html (10 issues)
# ============================================================
add('io/struct.Split.html', [
    (E('<p>Splitter for the <a href="trait.AsyncBufReadExt.html#method.split" title="method tokio::io::AsyncBufReadExt::split"><code>split</code></a> method.</p>'),
     E('<p><a href="trait.AsyncBufReadExt.html#method.split" title="method tokio::io::AsyncBufReadExt::split"><code>split</code></a> 方法使用的分割器。</p>')),
    (E('<p>A <code>Split</code> can be turned into a <code>Stream</code> with <a href="https://docs.rs/tokio-stream/0.1/tokio_stream/wrappers/struct.SplitStream.html"><code>SplitStream</code></a>.</p>'),
     E('<p><code>Split</code> 可以通过 <a href="https://docs.rs/tokio-stream/0.1/tokio_stream/wrappers/struct.SplitStream.html"><code>SplitStream</code></a> 转换为 <code>Stream</code>。</p>')),
    (E('<p>Returns the next segment in the stream.</p>'),
     E('<p>返回流中的下一段。</p>')),
    (E('<p>Polls for the next segment in the stream.</p>'),
     E('<p>轮询流中的下一段。</p>')),
    (E('<p>When the method returns <code>Poll::Pending</code>, the <code>Waker</code> in the provided\n<code>Context</code> is scheduled to receive a wakeup when more bytes become\navailable on the underlying IO resource.</p>'),
     E('<p>当方法返回 <code>Poll::Pending</code> 时，传入的 <code>Context</code> 中的 <code>Waker</code> 会被调度，\n以便在底层 I/O 资源上有更多字节可用时收到唤醒通知。</p>')),
    (E('<p>Note that on multiple calls to <code>poll_next_segment</code>, only the <code>Waker</code>\nfrom the <code>Context</code> passed to the most recent call is scheduled to\nreceive a wakeup.</p>'),
     E('<p>请注意，对 <code>poll_next_segment</code> 的多次调用中，\n只有最近一次调用传入的 <code>Context</code> 中的 <code>Waker</code> 会被调度接收唤醒。</p>')),
])


# ============================================================
# io/struct.Take.html (13 issues)
# ============================================================
add('io/struct.Take.html', [
    (E('<p>Stream for the <a href="trait.AsyncReadExt.html#method.take" title="method tokio::io::AsyncReadExt::take"><code>take</code></a> method.</p>'),
     E('<p><a href="trait.AsyncReadExt.html#method.take" title="method tokio::io::AsyncReadExt::take"><code>take</code></a> 方法返回的流。</p>')),
    (E('<p>Returns the remaining number of bytes that can be\nread before this instance will return EOF.</p>'),
     E('<p>返回此实例返回 EOF 之前还可以读取的剩余字节数。</p>')),
    (E('<p>This instance may reach <code>EOF</code> after reading fewer bytes than indicated by\nthis method if the underlying <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> instance reaches EOF.</p>'),
     E('<p>如果底层的 <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> 实例达到 EOF，\n那么此实例可能在读取比此方法指示的字节数更少之后就会达到 <code>EOF</code>。</p>')),
    (E('<p>Sets the number of bytes that can be read before this instance will\nreturn EOF. This is the same as constructing a new <code>Take</code> instance, so\nthe amount of bytes read and the previous limit value don’t matter when\ncalling this method.</p>'),
     E('<p>设置此实例返回 EOF 之前可以读取的字节数。\n这等同于构造一个新的 <code>Take</code> 实例，\n因此调用此方法时已读取的字节数和之前的限制值都无关紧要。</p>')),
    (E('<p>Gets a reference to the underlying reader.</p>'),
     E('<p>获取底层读取器的引用。</p>')),
    (E('<p>Gets a mutable reference to the underlying reader.</p>'),
     E('<p>获取底层读取器的可变引用。</p>')),
    (E('<p>Care should be taken to avoid modifying the internal I/O state of the\nunderlying reader as doing so may corrupt the internal limit of this\n<code>Take</code>.</p>'),
     E('<p>注意不要修改底层读取器的内部 I/O 状态，\n因为这样做可能会破坏此 <code>Take</code> 的内部限制。</p>')),
    (E('<p>Gets a pinned mutable reference to the underlying reader.</p>'),
     E('<p>获取底层读取器的固定可变引用。</p>')),
    (E('<p>Consumes the <code>Take</code>, returning the wrapped reader.</p>'),
     E('<p>消耗此 <code>Take</code>，返回被包装的读取器。</p>')),
])


# ============================================================
# io/struct.WriteHalf.html (5 issues)
# ============================================================
add('io/struct.WriteHalf.html', [
    (E('<p>The writable half of a value returned from <a href="fn.split.html" title="fn tokio::io::split"><code>split</code></a>.</p>'),
     E('<p>由 <a href="fn.split.html" title="fn tokio::io::split"><code>split</code></a> 返回的值的可写一半。</p>')),
    (E('<p>Checks if this <code>WriteHalf</code> and some <code>ReadHalf</code> were split from the same\nstream.</p>'),
     E('<p>检查此 <code>WriteHalf</code> 与某个 <code>ReadHalf</code> 是否从同一个流拆分而来。</p>')),
])


# ============================================================
# io/trait.AsyncBufRead.html (11 issues)
# ============================================================
add('io/trait.AsyncBufRead.html', [
    (E('<p>Reads bytes asynchronously.</p>'),
     E('<p>异步读取字节。</p>')),
    (E('<p>This trait is analogous to <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.BufRead.html" title="trait std::io::BufRead"><code>std::io::BufRead</code></a>, but integrates with\nthe asynchronous task system. In particular, the <a href="trait.AsyncBufRead.html#tymethod.poll_fill_buf" title="method tokio::io::AsyncBufRead::poll_fill_buf"><code>poll_fill_buf</code></a> method,\nunlike <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.BufRead.html#tymethod.fill_buf" title="method std::io::BufRead::fill_buf"><code>BufRead::fill_buf</code></a>, will automatically queue the current task for wakeup\nand return if data is not yet available, rather than blocking the calling\nthread.</p>'),
     E('<p>此 trait 类似于 <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.BufRead.html" title="trait std::io::BufRead"><code>std::io::BufRead</code></a>，但与异步任务系统集成。\n特别地，<a href="trait.AsyncBufRead.html#tymethod.poll_fill_buf" title="method tokio::io::AsyncBufRead::poll_fill_buf"><code>poll_fill_buf</code></a> 方法与 <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.BufRead.html#tymethod.fill_buf" title="method std::io::BufRead::fill_buf"><code>BufRead::fill_buf</code></a> 不同，\n当数据尚不可用时，它会自动将当前任务排入唤醒队列并立即返回，\n而不是阻塞调用线程。</p>')),
    (E('<p>Utilities for working with <code>AsyncBufRead</code> values are provided by\n<a href="trait.AsyncBufReadExt.html" title="trait tokio::io::AsyncBufReadExt"><code>AsyncBufReadExt</code></a>.</p>'),
     E('<p>用于处理 <code>AsyncBufRead</code> 值的工具方法由 <a href="trait.AsyncBufReadExt.html" title="trait tokio::io::AsyncBufReadExt"><code>AsyncBufReadExt</code></a> 提供。</p>')),
    (E('<p>Attempts to return the contents of the internal buffer, filling it with more data\nfrom the inner reader if it is empty.</p>'),
     E('<p>尝试返回内部缓冲区的内容，如果内部缓冲区为空，则从内部读取器填充更多数据。</p>')),
    (E('<p>On success, returns <code>Poll::Ready(Ok(buf))</code>.</p>'),
     E('<p>成功时，返回 <code>Poll::Ready(Ok(buf))</code>。</p>')),
    (E('<p>If no data is available for reading, the method returns\n<code>Poll::Pending</code> and arranges for the current task (via\n<code>cx.waker().wake_by_ref()</code>) to receive a notification when the object becomes\nreadable or is closed.</p>'),
     E('<p>如果没有可读取的数据，此方法返回 <code>Poll::Pending</code>，\n并安排当前任务（通过 <code>cx.waker().wake_by_ref()</code>）\n在该对象变为可读或被关闭时收到通知。</p>')),
    (E('<p>This function is a lower-level call. It needs to be paired with the\n<a href="trait.AsyncBufRead.html#tymethod.consume" title="method tokio::io::AsyncBufRead::consume"><code>consume</code></a> method to function properly. When calling this\nmethod, none of the contents will be \xe2\x80\x9cread\xe2\x80\x9d in the sense that later\ncalling <a href="trait.AsyncRead.html#tymethod.poll_read" title="method tokio::io::AsyncRead::poll_read"><code>poll_read</code></a> may return the same contents. As such, <a href="trait.AsyncBufRead.html#tymethod.consume" title="method tokio::io::AsyncBufRead::consume"><code>consume</code></a> must\nbe called with the number of bytes that are consumed from this buffer to\nensure that the bytes are never returned twice.</p>'),
     E('<p>此函数是较低级别的调用。要使其正常工作，需要与\n<a href="trait.AsyncBufRead.html#tymethod.consume" title="method tokio::io::AsyncBufRead::consume"><code>consume</code></a> 方法配对使用。\n调用此方法时，其中的内容不会被视为已\xe2\x80\x9c读\xe2\x80\x9d，\n因此随后调用 <a href="trait.AsyncRead.html#tymethod.poll_read" title="method tokio::io::AsyncRead::poll_read"><code>poll_read</code></a> 仍可能返回相同的内容。\n因此，必须使用从此缓冲区消费的字节数调用 <a href="trait.AsyncBufRead.html#tymethod.consume" title="method tokio::io::AsyncBufRead::consume"><code>consume</code></a>，\n以确保相同的字节不会被返回两次。</p>')),
    (E('<p>An empty buffer returned indicates that the stream has reached EOF.</p>'),
     E('<p>返回空缓冲区表示流已达到 EOF。</p>')),
    (E('<p>Tells this buffer that <code>amt</code> bytes have been consumed from the buffer,\nso they should no longer be returned in calls to <a href="trait.AsyncRead.html#tymethod.poll_read" title="method tokio::io::AsyncRead::poll_read"><code>poll_read</code></a>.</p>'),
     E('<p>通知此缓冲区已有 <code>amt</code> 个字节被消费，\n因此后续调用 <a href="trait.AsyncRead.html#tymethod.poll_read" title="method tokio::io::AsyncRead::poll_read"><code>poll_read</code></a> 时不应再返回这些字节。</p>')),
    (E('<p>This function is a lower-level call. It needs to be paired with the\n<a href="trait.AsyncBufRead.html#tymethod.poll_fill_buf" title="method tokio::io::AsyncBufRead::poll_fill_buf"><code>poll_fill_buf</code></a> method to function properly. This function does\nnot perform any I/O, it simply informs this object that some amount of\nits buffer, returned from <a href="trait.AsyncBufRead.html#tymethod.poll_fill_buf" title="method tokio::io::AsyncBufRead::poll_fill_buf"><code>poll_fill_buf</code></a>, has been consumed and should\nno longer be returned. As such, this function may do odd things if\n<a href="trait.AsyncBufRead.html#tymethod.poll_fill_buf" title="method tokio::io::AsyncBufRead::poll_fill_buf"><code>poll_fill_buf</code></a> isn’t called before calling it.</p>'),
     E('<p>此函数是较低级别的调用。要使其正常工作，需要与\n<a href="trait.AsyncBufRead.html#tymethod.poll_fill_buf" title="method tokio::io::AsyncBufRead::poll_fill_buf"><code>poll_fill_buf</code></a> 方法配对使用。\n此函数不执行任何 I/O 操作，它只是通知此对象：\n从 <a href="trait.AsyncBufRead.html#tymethod.poll_fill_buf" title="method tokio::io::AsyncBufRead::poll_fill_buf"><code>poll_fill_buf</code></a> 返回的缓冲区中已有部分被消费，\n不应再返回这些内容。因此，如果在调用此函数之前没有调用\n<a href="trait.AsyncBufRead.html#tymethod.poll_fill_buf" title="method tokio::io::AsyncBufRead::poll_fill_buf"><code>poll_fill_buf</code></a>，则可能产生异常行为。</p>')),
    (E('<p>The <code>amt</code> must be <code>&lt;=</code> the number of bytes in the buffer returned by\n<a href="trait.AsyncBufRead.html#tymethod.poll_fill_buf" title="method tokio::io::AsyncBufRead::poll_fill_buf"><code>poll_fill_buf</code></a>.</p>'),
     E('<p><code>amt</code> 必须 <code>&lt;=</code> 由 <a href="trait.AsyncBufRead.html#tymethod.poll_fill_buf" title="method tokio::io::AsyncBufRead::poll_fill_buf"><code>poll_fill_buf</code></a> 返回的缓冲区中的字节数。</p>')),
])


# ============================================================
# io/trait.AsyncBufReadExt.html (39 issues)
# ============================================================
add('io/trait.AsyncBufReadExt.html', [
    (E('<p>An extension trait which adds utility methods to <a href="trait.AsyncBufRead.html" title="trait tokio::io::AsyncBufRead"><code>AsyncBufRead</code></a> types.</p>'),
     E('<p>一个为 <a href="trait.AsyncBufRead.html" title="trait tokio::io::AsyncBufRead"><code>AsyncBufRead</code></a> 类型添加实用方法的扩展 trait。</p>')),
    (E('<p>Reads all bytes into <code>buf</code> until the delimiter <code>byte</code> or EOF is reached.</p>'),
     E('<p>读取所有字节到 <code>buf</code>，直到遇到分隔符字节 <code>byte</code> 或 EOF。</p>')),
    (E('<p>This function will read bytes from the underlying stream until the\ndelimiter or EOF is found. Once found, all bytes up to, and including,\nthe delimiter (if found) will be appended to <code>buf</code>.</p>'),
     E('<p>此函数从底层流读取字节，直到找到分隔符或 EOF。\n一旦找到，分隔符（包括分隔符本身，如果找到）之前的所有字节都将追加到 <code>buf</code>。</p>')),
    (E('<p>If successful, this function will return the total number of bytes read.</p>'),
     E('<p>如果成功，此函数将返回读取的总字节数。</p>')),
    (E('<p>If this function returns <code>Ok(0)</code>, the stream has reached EOF.</p>'),
     E('<p>如果此函数返回 <code>Ok(0)</code>，则流已达到 EOF。</p>')),
    (E('<p>This function will ignore all instances of <a href="https://doc.rust-lang.org/1.95.0/std/io/error/enum.ErrorKind.html#variant.Interrupted" title="variant std::io::error::ErrorKind::Interrupted"><code>ErrorKind::Interrupted</code></a> and\nwill otherwise return any errors returned by <a href="trait.AsyncBufRead.html#tymethod.poll_fill_buf" title="method tokio::io::AsyncBufRead::poll_fill_buf"><code>fill_buf</code></a>.</p>'),
     E('<p>此函数会忽略所有 <a href="https://doc.rust-lang.org/1.95.0/std/io/error/enum.ErrorKind.html#variant.Interrupted" title="variant std::io::error::ErrorKind::Interrupted"><code>ErrorKind::Interrupted</code></a> 实例，\n其它情况下会原样返回 <a href="trait.AsyncBufRead.html#tymethod.poll_fill_buf" title="method tokio::io::AsyncBufRead::poll_fill_buf"><code>fill_buf</code></a> 返回的错误。</p>')),
    (E('<p>If an I/O error is encountered then all bytes read so far will be\npresent in <code>buf</code> and its length will have been adjusted appropriately.</p>'),
     E('<p>如果遇到 I/O 错误，那么到目前为止读取的所有字节都将保留在 <code>buf</code> 中，\n并且其长度已相应调整。</p>')),
    (E('<p>If the method is used as the event in a\n<a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> statement and some other branch\ncompletes first, then some data may have been partially read. Any\npartially read bytes are appended to <code>buf</code>, and the method can be\ncalled again to continue reading until <code>byte</code>.</p>'),
     E('<p>如果在 <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> 语句中将此方法作为事件，\n而其他分支先完成，则可能已经部分读取了一些数据。\n部分读取的字节会追加到 <code>buf</code> 中，\n可以再次调用此方法继续读取，直到读到 <code>byte</code> 为止。</p>')),
    (E('<p>This method returns the total number of bytes read. If you cancel\nthe call to <code>read_until</code> and then call it again to continue reading,\nthe counter is reset.</p>'),
     E('<p>此方法返回读取的总字节数。\n如果取消对 <code>read_until</code> 的调用之后再调用它继续读取，\n计数器会被重置。</p>')),
    (E('<p><a href="https://doc.rust-lang.org/1.95.0/std/io/cursor/struct.Cursor.html" title="struct std::io::cursor::Cursor"><code>std::io::Cursor</code></a> is a type that implements <code>BufRead</code>. In\nthis example, we use <a href="https://doc.rust-lang.org/1.95.0/std/io/cursor/struct.Cursor.html" title="struct std::io::cursor::Cursor"><code>Cursor</code></a> to read all the bytes in a byte slice\nin hyphen delimited segments:</p>'),
     E('<p><a href="https://doc.rust-lang.org/1.95.0/std/io/cursor/struct.Cursor.html" title="struct std::io::cursor::Cursor"><code>std::io::Cursor</code></a> 是一个实现了 <code>BufRead</code> 的类型。\n在此示例中，我们使用 <a href="https://doc.rust-lang.org/1.95.0/std/io/cursor/struct.Cursor.html" title="struct std::io::cursor::Cursor"><code>Cursor</code></a> 以连字符分隔的段读取字节切片中的所有字节：</p>')),
    (E('<p>Reads all bytes until a newline (the 0xA byte) is reached, and append\nthem to the provided buffer.</p>'),
     E('<p>读取所有字节直到换行符（0xA 字节），并将其追加到提供的缓冲区中。</p>')),
    (E('<p>This function will read bytes from the underlying stream until the\nnewline delimiter (the 0xA byte) or EOF is found. Once found, all bytes\nup to, and including, the delimiter (if found) will be appended to\n<code>buf</code>.</p>'),
     E('<p>此函数从底层流读取字节，直到找到换行分隔符（0xA 字节）或 EOF。\n一旦找到，分隔符（包括分隔符本身，如果找到）之前的所有字节都将追加到 <code>buf</code>。</p>')),
    (E('<p>This function has the same error semantics as <a href="trait.AsyncBufReadExt.html#method.read_until" title="method tokio::io::AsyncBufReadExt::read_until"><code>read_until</code></a> and will\nalso return an error if the read bytes are not valid UTF-8. If an I/O\nerror is encountered then <code>buf</code> may contain some bytes already read in\nthe event that all data read so far was valid UTF-8.</p>'),
     E('<p>此函数与 <a href="trait.AsyncBufReadExt.html#method.read_until" title="method tokio::io::AsyncBufReadExt::read_until"><code>read_until</code></a> 具有相同的错误语义，\n并且当读取的字节不是有效的 UTF-8 时也会返回错误。\n如果遇到 I/O 错误，且目前为止读取的所有数据都是有效的 UTF-8，\n那么 <code>buf</code> 可能包含一些已读取的字节。</p>')),
    (E('<p>This function does not behave like <a href="trait.AsyncBufReadExt.html#method.read_until" title="method tokio::io::AsyncBufReadExt::read_until"><code>read_until</code></a> because of the\nrequirement that a string contains only valid utf-8. If you need a\ncancellation safe <code>read_line</code>, there are three options:</p>'),
     E('<p>此函数的行为与 <a href="trait.AsyncBufReadExt.html#method.read_until" title="method tokio::io::AsyncBufReadExt::read_until"><code>read_until</code></a> 不同，\n因为字符串要求仅包含有效的 utf-8。\n如果你需要可取消安全的 <code>read_line</code>，有三种选择：</p>')),
    (E('<p><a href="https://doc.rust-lang.org/1.95.0/std/io/cursor/struct.Cursor.html" title="struct std::io::cursor::Cursor"><code>std::io::Cursor</code></a> is a type that implements\n<code>AsyncBufRead</code>. In this example, we use <a href="https://doc.rust-lang.org/1.95.0/std/io/cursor/struct.Cursor.html" title="struct std::io::cursor::Cursor"><code>Cursor</code></a> to read all the\nlines in a byte slice:</p>'),
     E('<p><a href="https://doc.rust-lang.org/1.95.0/std/io/cursor/struct.Cursor.html" title="struct std::io::cursor::Cursor"><code>std::io::Cursor</code></a> 是一个实现了\n<code>AsyncBufRead</code> 的类型。\n在此示例中，我们使用 <a href="https://doc.rust-lang.org/1.95.0/std/io/cursor/struct.Cursor.html" title="struct std::io::cursor::Cursor"><code>Cursor</code></a> 读取字节切片中的所有行：</p>')),
    (E('<p>Returns a stream of the contents of this reader split on the byte\n<code>byte</code>.</p>'),
     E('<p>返回一个流，内容是按字节 <code>byte</code> 切分后的此读取器的片段。</p>')),
    (E('<p>This method is the asynchronous equivalent to\n<a href="https://doc.rust-lang.org/1.95.0/std/io/trait.BufRead.html#method.split" title="method std::io::BufRead::split"><code>BufRead::split</code></a>.</p>'),
     E('<p>此方法是 <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.BufRead.html#method.split" title="method std::io::BufRead::split"><code>BufRead::split</code></a> 的异步等价物。</p>')),
    (E('<p>The stream returned from this function will yield instances of\n<a href="https://doc.rust-lang.org/1.95.0/std/io/error/type.Result.html" title="type std::io::error::Result"><code>io::Result</code></a><code>&lt;</code><a href="https://doc.rust-lang.org/1.95.0/core/option/enum.Option.html" title="enum core::option::Option"><code>Option</code></a><code>&lt;</code><a href="https://doc.rust-lang.org/1.95.0/alloc/vec/struct.Vec.html" title="struct alloc::vec::Vec"><code>Vec&lt;u8&gt;</code></a><code>&gt;&gt;</code>. Each vector returned will <em>not</em> have\nthe delimiter byte at the end.</p>'),
     E('<p>此函数返回的流会产生\n<a href="https://doc.rust-lang.org/1.95.0/std/io/error/type.Result.html" title="type std::io::error::Result"><code>io::Result</code></a><code>&lt;</code><a href="https://doc.rust-lang.org/1.95.0/core/option/enum.Option.html" title="enum core::option::Option"><code>Option</code></a><code>&lt;</code><a href="https://doc.rust-lang.org/1.95.0/alloc/vec/struct.Vec.html" title="struct alloc::vec::Vec"><code>Vec&lt;u8&gt;</code></a><code>&gt;&gt;</code> 实例。\n返回的每个向量末尾<em>不会</em>包含分隔符字节。</p>')),
    (E('<p>Each item of the stream has the same error semantics as\n<a href="trait.AsyncBufReadExt.html#method.read_until" title="method tokio::io::AsyncBufReadExt::read_until"><code>AsyncBufReadExt::read_until</code></a>.</p>'),
     E('<p>流中每个项目的错误语义与\n<a href="trait.AsyncBufReadExt.html#method.read_until" title="method tokio::io::AsyncBufReadExt::read_until"><code>AsyncBufReadExt::read_until</code></a> 相同。</p>')),
    (E('<p>Returns the contents of the internal buffer, filling it with more\ndata from the inner reader if it is empty.</p>'),
     E('<p>返回内部缓冲区的内容，如果内部缓冲区为空，则从内部读取器填充更多数据。</p>')),
    (E('<p>This function is a lower-level call. It needs to be paired with the\n<a href="trait.AsyncBufReadExt.html#method.consume" title="method tokio::io::AsyncBufReadExt::consume"><code>consume</code></a> method to function properly. When calling this method,\nnone of the contents will be \xe2\x80\x9cread\xe2\x80\x9d in the sense that later calling\n<code>read</code> may return the same contents. As such, <a href="trait.AsyncBufReadExt.html#method.consume" title="method tokio::io::AsyncBufReadExt::consume"><code>consume</code></a> must be\ncalled with the number of bytes that are consumed from this buffer\nto ensure that the bytes are never returned twice.</p>'),
     E('<p>此函数是较低级别的调用。要使其正常工作，需要与\n<a href="trait.AsyncBufReadExt.html#method.consume" title="method tokio::io::AsyncBufReadExt::consume"><code>consume</code></a> 方法配对使用。\n调用此方法时，其中的内容不会被视为已\xe2\x80\x9c读\xe2\x80\x9d，\n因此随后调用 <code>read</code> 仍可能返回相同的内容。\n因此，必须使用从此缓冲区消费的字节数调用 <a href="trait.AsyncBufReadExt.html#method.consume" title="method tokio::io::AsyncBufReadExt::consume"><code>consume</code></a>，\n以确保相同的字节不会被返回两次。</p>')),
    (E('<p>This function will return an I/O error if the underlying reader was\nread, but returned an error.</p>'),
     E('<p>如果底层读取器被读取但返回了错误，则此函数将返回该 I/O 错误。</p>')),
    (E('<p>Tells this buffer that <code>amt</code> bytes have been consumed from the\nbuffer, so they should no longer be returned in calls to <a href="trait.AsyncReadExt.html#method.read" title="method tokio::io::AsyncReadExt::read"><code>read</code></a>.</p>'),
     E('<p>通知此缓冲区已有 <code>amt</code> 个字节被消费，\n因此后续调用 <a href="trait.AsyncReadExt.html#method.read" title="method tokio::io::AsyncReadExt::read"><code>read</code></a> 时不应再返回这些字节。</p>')),
    (E('<p>This function is a lower-level call. It needs to be paired with the\n<a href="trait.AsyncBufReadExt.html#method.fill_buf" title="method tokio::io::AsyncBufReadExt::fill_buf"><code>fill_buf</code></a> method to function properly. This function does not\nperform any I/O, it simply informs this object that some amount of\nits buffer, returned from <a href="trait.AsyncBufReadExt.html#method.fill_buf" title="method tokio::io::AsyncBufReadExt::fill_buf"><code>fill_buf</code></a>, has been consumed and should\nno longer be returned. As such, this function may do odd things if\n<a href="trait.AsyncBufReadExt.html#method.fill_buf" title="method tokio::io::AsyncBufReadExt::fill_buf"><code>fill_buf</code></a> isn’t called before calling it.</p>'),
     E('<p>此函数是较低级别的调用。要使其正常工作，需要与\n<a href="trait.AsyncBufReadExt.html#method.fill_buf" title="method tokio::io::AsyncBufReadExt::fill_buf"><code>fill_buf</code></a> 方法配对使用。\n此函数不执行任何 I/O 操作，它只是通知此对象：\n从 <a href="trait.AsyncBufReadExt.html#method.fill_buf" title="method tokio::io::AsyncBufReadExt::fill_buf"><code>fill_buf</code></a> 返回的缓冲区中已有部分被消费，\n不应再返回这些内容。因此，如果在调用此函数之前没有调用\n<a href="trait.AsyncBufReadExt.html#method.fill_buf" title="method tokio::io::AsyncBufReadExt::fill_buf"><code>fill_buf</code></a>，则可能产生异常行为。</p>')),
    (E('<p>The <code>amt</code> must be less than the number of bytes in the buffer\nreturned by <a href="trait.AsyncBufReadExt.html#method.fill_buf" title="method tokio::io::AsyncBufReadExt::fill_buf"><code>fill_buf</code></a>.</p>'),
     E('<p><code>amt</code> 必须小于由 <a href="trait.AsyncBufReadExt.html#method.fill_buf" title="method tokio::io::AsyncBufReadExt::fill_buf"><code>fill_buf</code></a> 返回的缓冲区中的字节数。</p>')),
    (E('<p>Returns a stream over the lines of this reader.\nThis method is the async equivalent to <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.BufRead.html#method.lines" title="method std::io::BufRead::lines"><code>BufRead::lines</code></a>.</p>'),
     E('<p>返回此读取器各行的流。\n此方法是 <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.BufRead.html#method.lines" title="method std::io::BufRead::lines"><code>BufRead::lines</code></a> 的异步等价物。</p>')),
    (E('<p>The stream returned from this function will yield instances of\n<a href="https://doc.rust-lang.org/1.95.0/std/io/error/type.Result.html" title="type std::io::error::Result"><code>io::Result</code></a><code>&lt;</code><a href="https://doc.rust-lang.org/1.95.0/core/option/enum.Option.html" title="enum core::option::Option"><code>Option</code></a><code>&lt;</code><a href="https://doc.rust-lang.org/1.95.0/alloc/string/struct.String.html" title="struct alloc::string::String"><code>String</code></a><code>&gt;&gt;</code>. Each string returned will <em>not</em> have a newline\nbyte (the 0xA byte) or <code>CRLF</code> (0xD, 0xA bytes) at the end.</p>'),
     E('<p>此函数返回的流会产生\n<a href="https://doc.rust-lang.org/1.95.0/std/io/error/type.Result.html" title="type std::io::error::Result"><code>io::Result</code></a><code>&lt;</code><a href="https://doc.rust-lang.org/1.95.0/core/option/enum.Option.html" title="enum core::option::Option"><code>Option</code></a><code>&lt;</code><a href="https://doc.rust-lang.org/1.95.0/alloc/string/struct.String.html" title="struct alloc::string::String"><code>String</code></a><code>&gt;&gt;</code> 实例。\n返回的每个字符串末尾<em>不会</em>包含换行字节（0xA 字节）或 <code>CRLF</code>（0xD、0xA 字节）。</p>')),
    (E('<p>Each line of the stream has the same error semantics as <a href="trait.AsyncBufReadExt.html#method.read_line" title="method tokio::io::AsyncBufReadExt::read_line"><code>AsyncBufReadExt::read_line</code></a>.</p>'),
     E('<p>流中每一行的错误语义与 <a href="trait.AsyncBufReadExt.html#method.read_line" title="method tokio::io::AsyncBufReadExt::read_line"><code>AsyncBufReadExt::read_line</code></a> 相同。</p>')),
    (E('<p><a href="https://doc.rust-lang.org/1.95.0/std/io/cursor/struct.Cursor.html" title="struct std::io::cursor::Cursor"><code>std::io::Cursor</code></a> is a type that implements <code>BufRead</code>. In\nthis example, we use <a href="https://doc.rust-lang.org/1.95.0/std/io/cursor/struct.Cursor.html" title="struct std::io::cursor::Cursor"><code>Cursor</code></a> to iterate over all the lines in a byte\nslice.</p>'),
     E('<p><a href="https://doc.rust-lang.org/1.95.0/std/io/cursor/struct.Cursor.html" title="struct std::io::cursor::Cursor"><code>std::io::Cursor</code></a> 是一个实现了 <code>BufRead</code> 的类型。\n在此示例中，我们使用 <a href="https://doc.rust-lang.org/1.95.0/std/io/cursor/struct.Cursor.html" title="struct std::io::cursor::Cursor"><code>Cursor</code></a> 迭代字节切片中的所有行。</p>')),
])# ============================================================
# io/trait.AsyncRead.html (11 issues)
# ============================================================
add('io/trait.AsyncRead.html', [
    (E('<p>Reads bytes from a source.</p>'),
     E('<p>从源读取字节。</p>')),
    (E('<p>This trait is analogous to the <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.Read.html" title="trait std::io::Read"><code>std::io::Read</code></a> trait, but integrates with\nthe asynchronous task system. In particular, the <code>poll_read</code> method,\nunlike <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.Read.html#tymethod.read" title="method std::io::Read::read"><code>Read::read</code></a>, will automatically queue the current task for wakeup\nand return if data is not yet available, rather than blocking the calling\nthread.</p>'),
     E('<p>此 trait 类似于 <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.Read.html" title="trait std::io::Read"><code>std::io::Read</code></a> trait，但与异步任务系统集成。\n特别地，<code>poll_read</code> 方法与 <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.Read.html#tymethod.read" title="method std::io::Read::read"><code>Read::read</code></a> 不同，\n当数据尚不可用时，它会自动将当前任务排入唤醒队列并立即返回，\n而不是阻塞调用线程。</p>')),
    (E('<p>Specifically, this means that the <code>poll_read</code> function will return one of\nthe following:</p>'),
     E('<p>具体来说，这意味着 <code>poll_read</code> 函数将返回以下之一：</p>')),
    (E('<p><code>Poll::Ready(Ok(()))</code> means that data was immediately read and placed into\nthe output buffer. The amount of data read can be determined by the\nincrease in the length of the slice returned by <code>ReadBuf::filled</code>. If the\ndifference is 0, either EOF has been reached, or the output buffer had zero\ncapacity (i.e. <code>buf.remaining()</code> == 0).</p>'),
     E('<p><code>Poll::Ready(Ok(()))</code> 表示数据已立即读取并放入输出缓冲区。\n读取的数据量可以通过 <code>ReadBuf::filled</code> 返回的切片长度的增量来确定。\n如果增量为 0，则要么已到达 EOF，要么输出缓冲区的容量为零（即 <code>buf.remaining()</code> == 0）。</p>')),
    (E('<p><code>Poll::Pending</code> means that no data was read into the buffer\nprovided. The I/O object is not currently readable but may become readable\nin the future. Most importantly, <strong>the current future’s task is scheduled to\nget unparked when the object is readable</strong>. This means that like\n<code>Future::poll</code> you’ll receive a notification when the I/O object is\nreadable again.</p>'),
     E('<p><code>Poll::Pending</code> 表示没有数据被读入提供的缓冲区。\nI/O 对象当前不可读，但未来可能变为可读。\n最重要的是，<strong>当前 future 的任务被安排在该对象可读时被唤醒</strong>。\n这意味着与 <code>Future::poll</code> 类似，\n当 I/O 对象再次可读时你将收到通知。</p>')),
    (E('<p><code>Poll::Ready(Err(e))</code> for other errors are standard I/O errors coming from the\nunderlying object.</p>'),
     E('<p>其它错误的 <code>Poll::Ready(Err(e))</code> 是来自底层对象的标准 I/O 错误。</p>')),
    (E('<p>This trait importantly means that the <code>read</code> method only works in the\ncontext of a future’s task. The object may panic if used outside of a task.</p>'),
     E('<p>此 trait 重要的含义是：<code>read</code> 方法仅在 future 任务的上下文中工作。\n如果在任务外使用该对象，则可能会 panic。</p>')),
    (E('<p>Utilities for working with <code>AsyncRead</code> values are provided by\n<a href="trait.AsyncReadExt.html" title="trait tokio::io::AsyncReadExt"><code>AsyncReadExt</code></a>.</p>'),
     E('<p>用于处理 <code>AsyncRead</code> 值的工具方法由 <a href="trait.AsyncReadExt.html" title="trait tokio::io::AsyncReadExt"><code>AsyncReadExt</code></a> 提供。</p>')),
    (E('<p>Attempts to read from the <code>AsyncRead</code> into <code>buf</code>.</p>'),
     E('<p>尝试从 <code>AsyncRead</code> 读取到 <code>buf</code>。</p>')),
    (E('<p>On success, returns <code>Poll::Ready(Ok(()))</code> and places data in the\nunfilled portion of <code>buf</code>. If no data was read (<code>buf.filled().len()</code> is\nunchanged), it implies that EOF has been reached, or the output buffer\nhad zero capacity (i.e. <code>buf.remaining()</code> == 0).</p>'),
     E('<p>成功时，返回 <code>Poll::Ready(Ok(()))</code> 并将数据放入 <code>buf</code> 的未填充部分。\n如果没有读取到数据（<code>buf.filled().len()</code> 不变），\n则意味着已到达 EOF，或者输出缓冲区的容量为零（即 <code>buf.remaining()</code> == 0）。</p>')),
    (E('<p>If no data is available for reading, the method returns <code>Poll::Pending</code>\nand arranges for the current task (via <code>cx.waker()</code>) to receive a\nnotification when the object becomes readable or is closed.</p>'),
     E('<p>如果没有可读取的数据，此方法返回 <code>Poll::Pending</code>，\n并安排当前任务（通过 <code>cx.waker()</code>）在该对象变为可读或被关闭时收到通知。</p>')),
])


# ============================================================
# io/trait.AsyncSeek.html (23 issues)
# ============================================================
add('io/trait.AsyncSeek.html', [
    (E('<p>Seek bytes asynchronously.</p>'),
     E('<p>异步定位字节。</p>')),
    (E('<p>This trait is analogous to the <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.Seek.html" title="trait std::io::Seek"><code>std::io::Seek</code></a> trait, but integrates\nwith the asynchronous task system. In particular, the <code>start_seek</code>\nmethod, unlike <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.Seek.html#tymethod.seek" title="method std::io::Seek::seek"><code>Seek::seek</code></a>, will not block the calling thread.</p>'),
     E('<p>此 trait 类似于 <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.Seek.html" title="trait std::io::Seek"><code>std::io::Seek</code></a> trait，但与异步任务系统集成。\n特别地，<code>start_seek</code> 方法与 <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.Seek.html#tymethod.seek" title="method std::io::Seek::seek"><code>Seek::seek</code></a> 不同，它不会阻塞调用线程。</p>')),
    (E('<p>Utilities for working with <code>AsyncSeek</code> values are provided by\n<a href="trait.AsyncSeekExt.html" title="trait tokio::io::AsyncSeekExt"><code>AsyncSeekExt</code></a>.</p>'),
     E('<p>用于处理 <code>AsyncSeek</code> 值的工具方法由 <a href="trait.AsyncSeekExt.html" title="trait tokio::io::AsyncSeekExt"><code>AsyncSeekExt</code></a> 提供。</p>')),
    (E('<p>Attempts to seek to an offset, in bytes, in a stream.</p>'),
     E('<p>尝试按字节偏移量在流中定位。</p>')),
    (E('<p>A seek beyond the end of a stream is allowed, but behavior is defined\nby the implementation.</p>'),
     E('<p>允许定位到超出流末尾的位置，但具体行为由实现定义。</p>')),
    (E('<p>If this function returns successfully, then the job has been submitted.\nTo find out when it completes, call <code>poll_complete</code>.</p>'),
     E('<p>如果此函数成功返回，那么任务已被提交。\n要了解何时完成，请调用 <code>poll_complete</code>。</p>')),
    (E('<p>This function can return <a href="https://doc.rust-lang.org/1.95.0/std/io/error/enum.ErrorKind.html#variant.Other" title="variant std::io::error::ErrorKind::Other"><code>io::ErrorKind::Other</code></a> in case there is\nanother seek in progress. To avoid this, it is advisable that any call\nto <code>start_seek</code> is preceded by a call to <code>poll_complete</code> to ensure all\npending seeks have completed.</p>'),
     E('<p>如果有另一个定位正在进行，此函数可能返回 <a href="https://doc.rust-lang.org/1.95.0/std/io/error/enum.ErrorKind.html#variant.Other" title="variant std::io::error::ErrorKind::Other"><code>io::ErrorKind::Other</code></a>。\n为避免这种情况，建议在任何 <code>start_seek</code> 调用之前先调用 <code>poll_complete</code>，\n以确保所有挂起的定位都已完成。</p>')),
    (E('<p>Waits for a seek operation to complete.</p>'),
     E('<p>等待定位操作完成。</p>')),
    (E('<p>If the seek operation completed successfully, this method returns the\nnew position from the start of the stream. That position can be used\nlater with <a href="https://doc.rust-lang.org/1.95.0/std/io/enum.SeekFrom.html#variant.Start" title="variant std::io::SeekFrom::Start"><code>SeekFrom::Start</code></a>.</p>'),
     E('<p>如果定位操作成功完成，此方法将返回从流开头算起的新位置。\n该位置稍后可与 <a href="https://doc.rust-lang.org/1.95.0/std/io/enum.SeekFrom.html#variant.Start" title="variant std::io::SeekFrom::Start"><code>SeekFrom::Start</code></a> 一起使用。</p>')),
    (E('<p>The position returned by calling this method can only be relied on right\nafter <code>start_seek</code>. If you have changed the position by e.g. reading or\nwriting since calling <code>start_seek</code>, then it is unspecified whether the\nreturned position takes that position change into account. Similarly, if\n<code>start_seek</code> has never been called, then it is unspecified whether\n<code>poll_complete</code> returns the actual position or some other placeholder\nvalue (such as 0).</p>'),
     E('<p>此方法返回的位置仅在 <code>start_seek</code> 之后立即有效。\n如果在调用 <code>start_seek</code> 之后通过读取或写入等方式更改了位置，\n那么返回的位置是否考虑该位置变化是未指定的。\n类似地，如果从未调用过 <code>start_seek</code>，\n那么 <code>poll_complete</code> 是否返回实际位置或其它占位值（如 0）也是未指定的。</p>')),
    (E('<p>Seeking to a negative offset is considered an error.</p>'),
     E('<p>定位到负偏移量被视为错误。</p>')),
    # BufReader impl
    (E('<p>The position used for seeking with <code>SeekFrom::Current(_)</code> is the\nposition the underlying reader would be at if the <code>BufReader</code> had no\ninternal buffer.</p>'),
     E('<p>使用 <code>SeekFrom::Current(_)</code> 进行定位时，所用的位置是假设 <code>BufReader</code> 没有内部缓冲区时底层读取器应处的位置。</p>')),
    (E('<p>Seeking always discards the internal buffer, even if the seek position\nwould otherwise fall within it. This guarantees that calling\n<code>.into_inner()</code> immediately after a seek yields the underlying reader\nat the same position.</p>'),
     E('<p>定位操作始终会丢弃内部缓冲区，即使定位的位置本应落在该缓冲区内。\n这保证在定位之后立即调用 <code>.into_inner()</code> 得到的底层读取器与定位时所处的位置一致。</p>')),
    (E('<p>See <a href="trait.AsyncSeek.html" title="trait tokio::io::AsyncSeek"><code>AsyncSeek</code></a> for more details.</p>'),
     E('<p>更多详情请参阅 <a href="trait.AsyncSeek.html" title="trait tokio::io::AsyncSeek"><code>AsyncSeek</code></a>。</p>')),
    (E('<p>Note: In the edge case where you’re seeking with <code>SeekFrom::Current(n)</code>\nwhere <code>n</code> minus the internal buffer length overflows an <code>i64</code>, two\nseeks will be performed instead of one. If the second seek returns\n<code>Err</code>, the underlying reader will be left at the same position it would\nhave if you called <code>seek</code> with <code>SeekFrom::Current(0)</code>.</p>'),
     E('<p>注意：在边界情况下，当你使用 <code>SeekFrom::Current(n)</code> 进行定位时，如果 <code>n</code> 减去内部缓冲区长度会溢出 <code>i64</code>，则会执行两次定位而不是一次。\n如果第二次定位返回 <code>Err</code>，则底层读取器将停留在与使用 <code>SeekFrom::Current(0)</code> 调用 <code>seek</code> 相同的位置上。</p>')),
    # BufStream impl
    (E('<p>Seek to an offset, in bytes, in the underlying stream.</p>'),
     E('<p>在底层流中按字节偏移量定位。</p>')),
    (E('<p>The position used for seeking with <code>SeekFrom::Current(_)</code> is the\nposition the underlying stream would be at if the <code>BufStream</code> had no\ninternal buffer.</p>'),
     E('<p>使用 <code>SeekFrom::Current(_)</code> 进行定位时，所用的位置是假设 <code>BufStream</code> 没有内部缓冲区时底层流应处的位置。</p>')),
    # BufWriter impl
    (E('<p>Seek to the offset, in bytes, in the underlying writer.</p>'),
     E('<p>在底层写入器中按字节偏移量定位。</p>')),
    (E('<p>Seeking always writes out the internal buffer before seeking.</p>'),
     E('<p>定位前始终会先写出内部缓冲区的内容。</p>')),
])


# ============================================================
# io/trait.AsyncSeekExt.html (11 issues)
# ============================================================
add('io/trait.AsyncSeekExt.html', [
    (E('<p>An extension trait that adds utility methods to <a href="trait.AsyncSeek.html" title="trait tokio::io::AsyncSeek"><code>AsyncSeek</code></a> types.</p>'),
     E('<p>一个为 <a href="trait.AsyncSeek.html" title="trait tokio::io::AsyncSeek"><code>AsyncSeek</code></a> 类型添加实用方法的扩展 trait。</p>')),
    (E('<p>See <a href="index.html" title="mod tokio::io">module</a> documentation for more details.</p>'),
     E('<p>更多详情请参阅 <a href="index.html" title="mod tokio::io">module</a> 文档。</p>')),
    (E('<p>Creates a future which will seek an IO object, and then yield the\nnew position in the object and the object itself.</p>'),
     E('<p>创建一个 future，对 IO 对象进行定位，然后产出该对象的新位置以及该对象本身。</p>')),
    (E('<p>In the case of an error the buffer and the object will be discarded, with\nthe error yielded.</p>'),
     E('<p>如果出现错误，缓冲区和对象将被丢弃，并产出错误。</p>')),
    (E('<p>Creates a future which will rewind to the beginning of the stream.</p>'),
     E('<p>创建一个 future，将倒回到流的开头。</p>')),
    (E('<p>This is convenience method, equivalent to <code>self.seek(SeekFrom::Start(0))</code>.</p>'),
     E('<p>这是一个便捷方法，等价于 <code>self.seek(SeekFrom::Start(0))</code>。</p>')),
    (E('<p>Creates a future which will return the current seek position from the\nstart of the stream.</p>'),
     E('<p>创建一个 future，返回从流开头算起的当前定位位置。</p>')),
    (E('<p>This is equivalent to <code>self.seek(SeekFrom::Current(0))</code>.</p>'),
     E('<p>这等价于 <code>self.seek(SeekFrom::Current(0))</code>。</p>')),
])


# ============================================================
# io/trait.AsyncWrite.html (32 issues)
# ============================================================
add('io/trait.AsyncWrite.html', [
    (E('<p>Writes bytes asynchronously.</p>'),
     E('<p>异步写入字节。</p>')),
    (E('<p>This trait is analogous to the <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.Write.html" title="trait std::io::Write"><code>std::io::Write</code></a> trait, but integrates with\nthe asynchronous task system. In particular, the <a href="trait.AsyncWrite.html#tymethod.poll_write" title="method tokio::io::AsyncWrite::poll_write"><code>poll_write</code></a> method,\nunlike <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.Write.html#tymethod.write" title="method std::io::Write::write"><code>Write::write</code></a>, will automatically queue the current task for wakeup\nand return if data is not yet available, rather than blocking the calling\nthread.</p>'),
     E('<p>此 trait 类似于 <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.Write.html" title="trait std::io::Write"><code>std::io::Write</code></a> trait，但与异步任务系统集成。\n特别地，<a href="trait.AsyncWrite.html#tymethod.poll_write" title="method tokio::io::AsyncWrite::poll_write"><code>poll_write</code></a> 方法与 <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.Write.html#tymethod.write" title="method std::io::Write::write"><code>Write::write</code></a> 不同，\n当数据尚不可用时，它会自动将当前任务排入唤醒队列并立即返回，\n而不是阻塞调用线程。</p>')),
    (E('<p>Specifically, this means that the <a href="trait.AsyncWrite.html#tymethod.poll_write" title="method tokio::io::AsyncWrite::poll_write"><code>poll_write</code></a> function will return one of\nthe following:</p>'),
     E('<p>具体来说，这意味着 <a href="trait.AsyncWrite.html#tymethod.poll_write" title="method tokio::io::AsyncWrite::poll_write"><code>poll_write</code></a> 函数将返回以下之一：</p>')),
    (E('<p><code>Poll::Ready(Ok(n))</code> means that <code>n</code> bytes of data was immediately\nwritten.</p>'),
     E('<p><code>Poll::Ready(Ok(n))</code> 表示 <code>n</code> 个字节的数据已立即被写入。</p>')),
    (E('<p><code>Poll::Pending</code> means that no data was written from the buffer\nprovided. The I/O object is not currently writable but may become writable\nin the future. Most importantly, <strong>the current future’s task is scheduled\nto get unparked when the object is writable</strong>. This means that like\n<code>Future::poll</code> you’ll receive a notification when the I/O object is\nwritable again.</p>'),
     E('<p><code>Poll::Pending</code> 表示没有从提供的缓冲区写入数据。\nI/O 对象当前不可写，但未来可能变为可写。\n最重要的是，<strong>当前 future 的任务被安排在该对象可写时被唤醒</strong>。\n这意味着与 <code>Future::poll</code> 类似，\n当 I/O 对象再次可写时你将收到通知。</p>')),
    (E('<p><code>Poll::Ready(Err(e))</code> for other errors are standard I/O errors coming from the\nunderlying object.</p>'),
     E('<p>其它错误的 <code>Poll::Ready(Err(e))</code> 是来自底层对象的标准 I/O 错误。</p>')),
    (E('<p>Utilities for working with <code>AsyncWrite</code> values are provided by\n<a href="trait.AsyncWriteExt.html" title="trait tokio::io::AsyncWriteExt"><code>AsyncWriteExt</code></a>. Most users will interact with <code>AsyncWrite</code> types through\nthese extension methods, which provide ergonomic async functions such as\n<code>write_all</code> and <code>flush</code>.</p>'),
     E('<p>用于处理 <code>AsyncWrite</code> 值的工具方法由 <a href="trait.AsyncWriteExt.html" title="trait tokio::io::AsyncWriteExt"><code>AsyncWriteExt</code></a> 提供。\n大多数用户通过这些扩展方法与 <code>AsyncWrite</code> 类型交互，\n这些扩展方法提供了诸如 <code>write_all</code> 和 <code>flush</code> 等易用的异步函数。</p>')),
    (E('<p>Attempt to write bytes from <code>buf</code> into the object.</p>'),
     E('<p>尝试将 <code>buf</code> 中的字节写入对象。</p>')),
    (E('<p>On success, returns <code>Poll::Ready(Ok(num_bytes_written))</code>. If successful,\nthen it must be guaranteed that <code>n &lt;= buf.len()</code>. A return value of <code>0</code>\ntypically means that the underlying object is no longer able to accept\nbytes and will likely not be able to in the future as well, or that the\nbuffer provided is empty.</p>'),
     E('<p>成功时，返回 <code>Poll::Ready(Ok(num_bytes_written))</code>。\n如果成功，则必须保证 <code>n &lt;= buf.len()</code>。\n返回值为 <code>0</code> 通常表示底层对象已经无法再接受字节，\n未来可能也无法再接受；或者提供的缓冲区为空。</p>')),
    (E('<p>If the object is not ready for writing, the method returns\n<code>Poll::Pending</code> and arranges for the current task (via\n<code>cx.waker()</code>) to receive a notification when the object becomes\nwritable or is closed.</p>'),
     E('<p>如果对象尚未准备好写入，此方法返回 <code>Poll::Pending</code>，\n并安排当前任务（通过 <code>cx.waker()</code>）在该对象变为可写或被关闭时收到通知。</p>')),
    (E('<p>Attempts to flush the object, ensuring that any buffered data reach\ntheir destination.</p>'),
     E('<p>尝试刷新对象，确保任何缓冲的数据都到达目的地。</p>')),
    (E('<p>On success, returns <code>Poll::Ready(Ok(()))</code>.</p>'),
     E('<p>成功时，返回 <code>Poll::Ready(Ok(()))</code>。</p>')),
    (E('<p>If flushing cannot immediately complete, this method returns\n<code>Poll::Pending</code> and arranges for the current task (via\n<code>cx.waker()</code>) to receive a notification when the object can make\nprogress towards flushing.</p>'),
     E('<p>如果刷新不能立即完成，此方法返回 <code>Poll::Pending</code>，\n并安排当前任务（通过 <code>cx.waker()</code>）在该对象可以推进刷新时收到通知。</p>')),
    (E('<p>Initiates or attempts to shut down this writer, returning success when\nthe I/O connection has completely shut down.</p>'),
     E('<p>启动或尝试关闭此写入器，当 I/O 连接已完全关闭时返回成功。</p>')),
    (E('<p>This method is intended to be used for asynchronous shutdown of I/O\nconnections. For example this is suitable for implementing shutdown of a\nTLS connection or calling <code>TcpStream::shutdown</code> on a proxied connection.\nProtocols sometimes need to flush out final pieces of data or otherwise\nperform a graceful shutdown handshake, reading/writing more data as\nappropriate. This method is the hook for such protocols to implement the\ngraceful shutdown logic.</p>'),
     E('<p>此方法旨在用于 I/O 连接的异步关闭。\n例如，它适用于实现 TLS 连接的关闭，\n或在代理连接上调用 <code>TcpStream::shutdown</code>。\n协议有时需要刷新出最后的数据或执行优雅的关闭握手，\n并根据需要读取/写入更多数据。\n此方法就是供这些协议实现优雅关闭逻辑的钩子。</p>')),
    (E('<p>This <code>shutdown</code> method is required by implementers of the\n<code>AsyncWrite</code> trait. Wrappers typically just want to proxy this call\nthrough to the wrapped type, and base types will typically implement\nshutdown logic here or just return <code>Ok(().into())</code>. Note that if you’re\nwrapping an underlying <code>AsyncWrite</code> a call to <code>shutdown</code> implies that\ntransitively the entire stream has been shut down. After your wrapper’s\nshutdown logic has been executed you should shut down the underlying\nstream.</p>'),
     E('<p><code>AsyncWrite</code> trait 的实现者需要提供此 <code>shutdown</code> 方法。\n包装类型通常只需将此调用代理给被包装的类型，\n基础类型通常会在这里实现关闭逻辑或直接返回 <code>Ok(().into())</code>。\n请注意，如果你包装了底层的 <code>AsyncWrite</code>，\n对 <code>shutdown</code> 的调用意味着整个流都会被传递性地关闭。\n在你的包装器的关闭逻辑执行完毕后，应当关闭底层的流。</p>')),
    (E('<p>Invocation of a <code>shutdown</code> implies an invocation of <code>flush</code>. Once this\nmethod returns <code>Ready</code> it implies that a flush successfully happened\nbefore the shutdown happened. That is, callers don’t need to call\n<code>flush</code> before calling <code>shutdown</code>. They can rely that by calling\n<code>shutdown</code> any pending buffered data will be written out.</p>'),
     E('<p>调用 <code>shutdown</code> 隐含着调用 <code>flush</code>。\n一旦此方法返回 <code>Ready</code>，就意味着在关闭之前已经成功执行了一次 flush。\n也就是说，调用方无需在调用 <code>shutdown</code> 之前调用 <code>flush</code>。\n可以依赖：通过调用 <code>shutdown</code>，所有挂起的缓冲数据都会被写出。</p>')),
    (E('<p>This function returns a <code>Poll&lt;io::Result&lt;()&gt;&gt;</code> classified as such:</p>'),
     E('<p>此函数返回分类如下的 <code>Poll&lt;io::Result&lt;()&gt;&gt;</code>：</p>')),
    (E('<p><code>Poll::Ready(Ok(()))</code> - indicates that the connection was\nsuccessfully shut down and is now safe to deallocate/drop/close\nresources associated with it. This method means that the current task\nwill no longer receive any notifications due to this method and the\nI/O object itself is likely no longer usable.</p>'),
     E('<p><code>Poll::Ready(Ok(()))</code> —— 表示连接已成功关闭，\n现在可以安全地释放/丢弃/关闭与其相关的资源。\n此方法意味着由于此方法当前任务不再接收任何通知，\nI/O 对象本身可能也无法再使用。</p>')),
    (E('<p><code>Poll::Pending</code> - indicates that shutdown is initiated but could\nnot complete just yet. This may mean that more I/O needs to happen to\ncontinue this shutdown operation. The current task is scheduled to\nreceive a notification when it’s otherwise ready to continue the\nshutdown operation. When woken up this method should be called again.</p>'),
     E('<p><code>Poll::Pending</code> —— 表示关闭已经启动，但目前尚未完成。\n这可能意味着需要更多的 I/O 才能继续此关闭操作。\n当前任务被安排在可以继续关闭操作时收到通知。\n被唤醒后应再次调用此方法。</p>')),
    (E('<p><code>Poll::Ready(Err(e))</code> - indicates a fatal error has happened with shutdown,\nindicating that the shutdown operation did not complete successfully.\nThis typically means that the I/O object is no longer usable.</p>'),
     E('<p><code>Poll::Ready(Err(e))</code> —— 表示关闭过程中发生了致命错误，\n说明关闭操作未成功完成。\n这通常意味着 I/O 对象已经无法再使用。</p>')),
    (E('<p>This function can return normal I/O errors through <code>Err</code>, described\nabove. Additionally this method may also render the underlying\n<code>Write::write</code> method no longer usable (e.g. will return errors in the\nfuture). It’s recommended that once <code>shutdown</code> is called the\n<code>write</code> method is no longer called.</p>'),
     E('<p>此函数可以通过 <code>Err</code> 返回上述普通 I/O 错误。\n此外，此方法还可能使底层的 <code>Write::write</code> 方法不再可用（在未来返回错误）。\n建议一旦调用了 <code>shutdown</code>，就不再调用 <code>write</code> 方法。</p>')),
    (E('<p>This function will panic if not called within the context of a future’s\ntask.</p>'),
     E('<p>如果不在 future 任务的上下文中调用此函数，它将 panic。</p>')),
    (E('<p>Like <a href="trait.AsyncWrite.html#tymethod.poll_write" title="method tokio::io::AsyncWrite::poll_write"><code>poll_write</code></a>, except that it writes from a slice of buffers.</p>'),
     E('<p>与 <a href="trait.AsyncWrite.html#tymethod.poll_write" title="method tokio::io::AsyncWrite::poll_write"><code>poll_write</code></a> 类似，但它从一个缓冲区切片中写入数据。</p>')),
    (E('<p>Data is copied from each buffer in order, with the final buffer\nread from possibly being only partially consumed. This method must\nbehave as a call to <a href="https://doc.rust-lang.org/1.95.0/core/macro.write.html" title="macro core::write"><code>write</code></a> with the buffers concatenated would.</p>'),
     E('<p>数据按顺序从每个缓冲区复制，最后一个被读取的缓冲区可能仅被部分消费。\n此方法必须表现得如同调用 <a href="https://doc.rust-lang.org/1.95.0/core/macro.write.html" title="macro core::write"><code>write</code></a> 来写入这些缓冲区拼接起来的数据一样。</p>')),
    (E('<p>The default implementation calls <a href="trait.AsyncWrite.html#tymethod.poll_write" title="method tokio::io::AsyncWrite::poll_write"><code>poll_write</code></a> with either the first nonempty\nbuffer provided, or an empty one if none exists.</p>'),
     E('<p>默认实现会使用提供的第一个非空缓冲区调用 <a href="trait.AsyncWrite.html#tymethod.poll_write" title="method tokio::io::AsyncWrite::poll_write"><code>poll_write</code></a>，\n如果不存在非空缓冲区，则使用一个空缓冲区。</p>')),
    (E('<p>This should be implemented as a single \xe2\x80\x9catomic\xe2\x80\x9d write action. If any\ndata has been partially written, it is wrong to return an error or\npending.</p>'),
     E('<p>此方法应实现为单个\xe2\x80\x9c原子\xe2\x80\x9d写入操作。\n如果已经部分写入了数据，那么返回错误或 pending 都是错误的。</p>')),
    (E('<p>Determines if this writer has an efficient <a href="trait.AsyncWrite.html#method.poll_write_vectored" title="method tokio::io::AsyncWrite::poll_write_vectored"><code>poll_write_vectored</code></a>\nimplementation.</p>'),
     E('<p>判断此写入器是否具有高效的 <a href="trait.AsyncWrite.html#method.poll_write_vectored" title="method tokio::io::AsyncWrite::poll_write_vectored"><code>poll_write_vectored</code></a> 实现。</p>')),
    (E('<p>If a writer does not override the default <a href="trait.AsyncWrite.html#method.poll_write_vectored" title="method tokio::io::AsyncWrite::poll_write_vectored"><code>poll_write_vectored</code></a>\nimplementation, code using it may want to avoid the method all together\nand coalesce writes into a single buffer for higher performance.</p>'),
     E('<p>如果写入器没有覆盖默认的 <a href="trait.AsyncWrite.html#method.poll_write_vectored" title="method tokio::io::AsyncWrite::poll_write_vectored"><code>poll_write_vectored</code></a> 实现，\n那么使用它的代码可能希望完全避免该方法，\n将写入合并到单个缓冲区中以获得更高的性能。</p>')),
    (E('<p>The default implementation returns <code>false</code>.</p>'),
     E('<p>默认实现返回 <code>false</code>。</p>')),
])


# ============================================================
# io/index.html (18 issues)
# ============================================================
add('io/index.html', [
    (E('<p>Traits, helpers, and type definitions for asynchronous I/O functionality.</p>'),
     E('<p>异步 I/O 功能的 trait、辅助函数和类型定义。</p>')),
    (E('<p>This module is the asynchronous version of <code>std::io</code>. Primarily, it\ndefines two traits, <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> and <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a>, which are asynchronous\nversions of the <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.Read.html" title="trait std::io::Read"><code>Read</code></a> and <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.Write.html" title="trait std::io::Write"><code>Write</code></a> traits in the standard library.</p>'),
     E('<p>此模块是 <code>std::io</code> 的异步版本。\n它主要定义了两个 trait：<a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> 和 <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a>，\n它们是标准库中 <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.Read.html" title="trait std::io::Read"><code>Read</code></a> 和 <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.Write.html" title="trait std::io::Write"><code>Write</code></a> trait 的异步版本。</p>')),
    (E('<p>Like the standard library’s <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.Read.html" title="trait std::io::Read"><code>Read</code></a> and <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.Write.html" title="trait std::io::Write"><code>Write</code></a> traits, <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> and\n<a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> provide the most general interface for reading and writing\ninput and output. Unlike the standard library’s traits, however, they are\n<em>asynchronous</em> \xe2\x80\x94 meaning that reading from or writing to a <code>tokio::io</code>\ntype will <em>yield</em> to the Tokio scheduler when IO is not ready, rather than\nblocking. This allows other tasks to run while waiting on IO.</p>'),
     E('<p>与标准库的 <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.Read.html" title="trait std::io::Read"><code>Read</code></a> 和 <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.Write.html" title="trait std::io::Write"><code>Write</code></a> trait 类似，<a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> 和\n<a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> 提供了读写输入输出的最通用接口。\n但与标准库的 trait 不同，它们是<em>异步</em>的 ——\n这意味着从 <code>tokio::io</code> 类型读取或写入数据在 IO 未就绪时会<em>让出</em>给 Tokio 调度器，\n而不是阻塞。这样可以在等待 IO 时运行其他任务。</p>')),
    (E('<p>Another difference is that <code>AsyncRead</code> and <code>AsyncWrite</code> only contain\ncore methods needed to provide asynchronous reading and writing\nfunctionality. Instead, utility methods are defined in the <a href="trait.AsyncReadExt.html" title="trait tokio::io::AsyncReadExt"><code>AsyncReadExt</code></a>\nand <a href="trait.AsyncWriteExt.html" title="trait tokio::io::AsyncWriteExt"><code>AsyncWriteExt</code></a> extension traits. These traits are automatically\nimplemented for all values that implement <code>AsyncRead</code> and <code>AsyncWrite</code>\nrespectively.</p>'),
     E('<p>另一个区别是，<code>AsyncRead</code> 和 <code>AsyncWrite</code> 仅包含提供异步读写功能所需的核心方法。\n而工具方法则定义在 <a href="trait.AsyncReadExt.html" title="trait tokio::io::AsyncReadExt"><code>AsyncReadExt</code></a> 和 <a href="trait.AsyncWriteExt.html" title="trait tokio::io::AsyncWriteExt"><code>AsyncWriteExt</code></a> 扩展 trait 中。\n这些 trait 会自动为实现了 <code>AsyncRead</code> 和 <code>AsyncWrite</code> 的所有值实现。</p>')),
    (E('<p>End users will rarely interact directly with <code>AsyncRead</code> and\n<code>AsyncWrite</code>. Instead, they will use the async functions defined in the\nextension traits. Library authors are expected to implement <code>AsyncRead</code>\nand <code>AsyncWrite</code> in order to provide types that behave like byte streams.</p>'),
     E('<p>最终用户很少会直接与 <code>AsyncRead</code> 和 <code>AsyncWrite</code> 交互，\n而是使用扩展 trait 中定义的异步函数。\n库的作者需要实现 <code>AsyncRead</code> 和 <code>AsyncWrite</code>，\n以便提供表现为字节流行为的类型。</p>')),
    (E('<p>Even with these differences, Tokio’s <code>AsyncRead</code> and <code>AsyncWrite</code> traits\ncan be used in almost exactly the same manner as the standard library’s\n<code>Read</code> and <code>Write</code>. Most types in the standard library that implement <code>Read</code>\nand <code>Write</code> have asynchronous equivalents in <code>tokio</code> that implement\n<code>AsyncRead</code> and <code>AsyncWrite</code>, such as <a href="../fs/struct.File.html" title="struct tokio::fs::File"><code>File</code></a> and <a href="../net/struct.TcpStream.html" title="struct tokio::net::TcpStream"><code>TcpStream</code></a>.</p>'),
     E('<p>尽管存在这些差异，Tokio 的 <code>AsyncRead</code> 和 <code>AsyncWrite</code> trait\n几乎可以以与标准库的 <code>Read</code> 和 <code>Write</code> 完全相同的方式使用。\n标准库中大多数实现 <code>Read</code> 和 <code>Write</code> 的类型，\n在 <code>tokio</code> 中都有实现了 <code>AsyncRead</code> 和 <code>AsyncWrite</code> 的异步等价物，\n例如 <a href="../fs/struct.File.html" title="struct tokio::fs::File"><code>File</code></a> 和 <a href="../net/struct.TcpStream.html" title="struct tokio::net::TcpStream"><code>TcpStream</code></a>。</p>')),
    (E('<p>For example, the standard library documentation introduces <code>Read</code> by\n<a href="https://doc.rust-lang.org/1.95.0/std/io/index.html#read-and-write" title="mod std::io">demonstrating</a> reading some bytes from a <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.File.html" title="struct std::fs::File"><code>std::fs::File</code></a>. We\ncan do the same with <a href="../fs/struct.File.html" title="struct tokio::fs::File"><code>tokio::fs::File</code></a>:</p>'),
     E('<p>例如，标准库文档通过<a href="https://doc.rust-lang.org/1.95.0/std/io/index.html#read-and-write" title="mod std::io">演示</a>从 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.File.html" title="struct std::fs::File"><code>std::fs::File</code></a> 读取一些字节来介绍 <code>Read</code>。\n我们也可以用 <a href="../fs/struct.File.html" title="struct tokio::fs::File"><code>tokio::fs::File</code></a> 做到同样的事情：</p>')),
    (E('<p>Byte-based interfaces are unwieldy and can be inefficient, as we’d need to be\nmaking near-constant calls to the operating system. To help with this,\n<code>std::io</code> comes with <a href="https://doc.rust-lang.org/1.95.0/std/io/index.html#bufreader-and-bufwriter" title="mod std::io">support for <em>buffered</em> readers and writers</a>,\nand therefore, <code>tokio::io</code> does as well.</p>'),
     E('<p>基于字节的接口使用起来很繁琐，效率也可能很低，因为我们几乎需要不停地调用操作系统。\n为了解决这个问题，<code>std::io</code> 提供了<a href="https://doc.rust-lang.org/1.95.0/std/io/index.html#bufreader-and-bufwriter" title="mod std::io">对<em>缓冲</em>读取器和写入器的支持</a>，\n因此 <code>tokio::io</code> 也提供了这样的支持。</p>')),
    (E('<p>Tokio provides an async version of the <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.BufRead.html" title="trait std::io::BufRead"><code>std::io::BufRead</code></a> trait,\n<a href="trait.AsyncBufRead.html" title="trait tokio::io::AsyncBufRead"><code>AsyncBufRead</code></a>; and async <a href="struct.BufReader.html" title="struct tokio::io::BufReader"><code>BufReader</code></a> and <a href="struct.BufWriter.html" title="struct tokio::io::BufWriter"><code>BufWriter</code></a> structs, which\nwrap readers and writers. These wrappers use a buffer, reducing the number\nof calls and providing nicer methods for accessing exactly what you want.</p>'),
     E('<p>Tokio 提供了 <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.BufRead.html" title="trait std::io::BufRead"><code>std::io::BufRead</code></a> trait 的异步版本\n<a href="trait.AsyncBufRead.html" title="trait tokio::io::AsyncBufRead"><code>AsyncBufRead</code></a>，以及异步的 <a href="struct.BufReader.html" title="struct tokio::io::BufReader"><code>BufReader</code></a> 和 <a href="struct.BufWriter.html" title="struct tokio::io::BufWriter"><code>BufWriter</code></a> 结构体，\n它们包装了读取器和写入器。这些包装器使用缓冲区，减少了调用次数，\n并提供了更方便的方法来精确访问你想要的内容。</p>')),
    (E('<p>For example, <a href="struct.BufReader.html" title="struct tokio::io::BufReader"><code>BufReader</code></a> works with the <a href="trait.AsyncBufRead.html" title="trait tokio::io::AsyncBufRead"><code>AsyncBufRead</code></a> trait to add\nextra methods to any async reader:</p>'),
     E('<p>例如，<a href="struct.BufReader.html" title="struct tokio::io::BufReader"><code>BufReader</code></a> 与 <a href="trait.AsyncBufRead.html" title="trait tokio::io::AsyncBufRead"><code>AsyncBufRead</code></a> trait 一起工作，\n为任何异步读取器添加额外的方法：</p>')),
    (E('<p><a href="struct.BufWriter.html" title="struct tokio::io::BufWriter"><code>BufWriter</code></a> doesn’t add any new ways of writing; it just buffers every call\nto <a href="trait.AsyncWriteExt.html#method.write" title="method tokio::io::AsyncWriteExt::write"><code>write</code></a>. However, you <strong>must</strong> flush\n<a href="struct.BufWriter.html" title="struct tokio::io::BufWriter"><code>BufWriter</code></a> to ensure that any buffered data is written.</p>'),
     E('<p><a href="struct.BufWriter.html" title="struct tokio::io::BufWriter"><code>BufWriter</code></a> 不会添加任何新的写入方式；它只是缓冲对\n<a href="trait.AsyncWriteExt.html#method.write" title="method tokio::io::AsyncWriteExt::write"><code>write</code></a> 的每次调用。\n然而，你<strong>必须</strong> flush <a href="struct.BufWriter.html" title="struct tokio::io::BufWriter"><code>BufWriter</code></a> 以确保所有缓冲的数据都被写入。</p>')),
    (E('<p>Because they are traits, we can implement <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> and <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> for\nour own types, as well. Note that these traits must only be implemented for\nnon-blocking I/O types that integrate with the futures type system. In\nother words, these types must never block the thread, and instead the\ncurrent task is notified when the I/O resource is ready.</p>'),
     E('<p>因为它们是 trait，我们也可以为自己的类型实现 <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> 和 <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a>。\n请注意，这些 trait 只能为与 futures 类型系统集成的非阻塞 I/O 类型实现。\n换句话说，这些类型绝不能阻塞线程，\n而应在 I/O 资源就绪时通知当前任务。</p>')),
    (E('<p>It is often convenient to encapsulate the reading and writing of bytes in a\n<a href="https://docs.rs/futures/0.3/futures/stream/trait.Stream.html"><code>Stream</code></a> or <a href="https://docs.rs/futures/0.3/futures/sink/trait.Sink.html"><code>Sink</code></a> of data.</p>'),
     E('<p>通常，将字节的读写封装在数据的\n<a href="https://docs.rs/futures/0.3/futures/stream/trait.Stream.html"><code>Stream</code></a> 或 <a href="https://docs.rs/futures/0.3/futures/sink/trait.Sink.html"><code>Sink</code></a> 中会很方便。</p>')),
    (E('<p>Tokio provides simple wrappers for converting <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> to <a href="https://docs.rs/futures/0.3/futures/stream/trait.Stream.html"><code>Stream</code></a>\nand vice-versa in the <a href="https://docs.rs/tokio-util">tokio-util</a> crate, see <a href="https://docs.rs/tokio-util/latest/tokio_util/io/struct.ReaderStream.html"><code>ReaderStream</code></a> and\n<a href="https://docs.rs/tokio-util/latest/tokio_util/io/struct.StreamReader.html"><code>StreamReader</code></a>.</p>'),
     E('<p>Tokio 在 <a href="https://docs.rs/tokio-util">tokio-util</a> crate 中提供了简单的包装器，\n用于在 <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> 与 <a href="https://docs.rs/futures/0.3/futures/stream/trait.Stream.html"><code>Stream</code></a> 之间互相转换，\n请参阅 <a href="https://docs.rs/tokio-util/latest/tokio_util/io/struct.ReaderStream.html"><code>ReaderStream</code></a> 和\n<a href="https://docs.rs/tokio-util/latest/tokio_util/io/struct.StreamReader.html"><code>StreamReader</code></a>。</p>')),
    (E('<p>There are also utility traits that abstract the asynchronous buffering\nnecessary to write your own adaptors for encoding and decoding bytes to/from\nyour structured data, allowing to transform something that implements\n<a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a>/<a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> into a <a href="https://docs.rs/futures/0.3/futures/stream/trait.Stream.html"><code>Stream</code></a>/<a href="https://docs.rs/futures/0.3/futures/sink/trait.Sink.html"><code>Sink</code></a>, see <a href="https://docs.rs/tokio-util/latest/tokio_util/codec/trait.Decoder.html"><code>Decoder</code></a> and\n<a href="https://docs.rs/tokio-util/latest/tokio_util/codec/trait.Encoder.html"><code>Encoder</code></a> in the <a href="https://docs.rs/tokio-util/latest/tokio_util/codec/index.html">tokio-util::codec</a> module.</p>'),
     E('<p>还有一些工具 trait 抽象了编写自己的字节与结构化数据编码/解码适配器所需的异步缓冲，\n允许将实现 <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a>/<a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> 的对象转换为\n<a href="https://docs.rs/futures/0.3/futures/stream/trait.Stream.html"><code>Stream</code></a>/<a href="https://docs.rs/futures/0.3/futures/sink/trait.Sink.html"><code>Sink</code></a>，\n请参阅 <a href="https://docs.rs/tokio-util/latest/tokio_util/codec/index.html">tokio-util::codec</a> 模块中的\n<a href="https://docs.rs/tokio-util/latest/tokio_util/codec/trait.Decoder.html"><code>Decoder</code></a> 和\n<a href="https://docs.rs/tokio-util/latest/tokio_util/codec/trait.Encoder.html"><code>Encoder</code></a>。</p>')),
    (E('<p>Tokio provides asynchronous APIs to standard <a href="fn.stdin.html" title="fn tokio::io::stdin">input</a>, <a href="fn.stdout.html" title="fn tokio::io::stdout">output</a>, and <a href="fn.stderr.html" title="fn tokio::io::stderr">error</a>.\nThese APIs are very similar to the ones provided by <code>std</code>, but they also\nimplement <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> and <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a>.</p>'),
     E('<p>Tokio 提供了标准<a href="fn.stdin.html" title="fn tokio::io::stdin">输入</a>、<a href="fn.stdout.html" title="fn tokio::io::stdout">输出</a>和<a href="fn.stderr.html" title="fn tokio::io::stderr">错误</a>的异步 API。\n这些 API 与 <code>std</code> 提供的 API 非常相似，但它们还实现了\n<a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> 和 <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a>。</p>')),
    (E('<p>Note that the standard input / output APIs  <strong>must</strong> be used from the\ncontext of the Tokio runtime, as they require Tokio-specific features to\nfunction. Calling these functions outside of a Tokio runtime will panic.</p>'),
     E('<p>请注意，标准输入/输出 API <strong>必须</strong>在 Tokio 运行时的上下文中使用，\n因为它们需要 Tokio 特有的功能才能工作。\n在 Tokio 运行时之外调用这些函数将导致 panic。</p>')),
    (E('<p>Additionally, <a href="https://doc.rust-lang.org/1.95.0/std/io/error/struct.Error.html" title="struct std::io::error::Error"><code>Error</code></a>, <a href="https://doc.rust-lang.org/1.95.0/std/io/error/enum.ErrorKind.html" title="enum std::io::error::ErrorKind"><code>ErrorKind</code></a>, <a href="https://doc.rust-lang.org/1.95.0/std/io/error/type.Result.html" title="type std::io::error::Result"><code>Result</code></a>, and <a href="https://doc.rust-lang.org/1.95.0/std/io/enum.SeekFrom.html" title="enum std::io::SeekFrom"><code>SeekFrom</code></a> are\nre-exported from <code>std::io</code> for ease of use.</p>'),
     E('<p>此外，<a href="https://doc.rust-lang.org/1.95.0/std/io/error/struct.Error.html" title="struct std::io::error::Error"><code>Error</code></a>、<a href="https://doc.rust-lang.org/1.95.0/std/io/error/enum.ErrorKind.html" title="enum std::io::error::ErrorKind"><code>ErrorKind</code></a>、<a href="https://doc.rust-lang.org/1.95.0/std/io/error/type.Result.html" title="type std::io::error::Result"><code>Result</code></a> 和 <a href="https://doc.rust-lang.org/1.95.0/std/io/enum.SeekFrom.html" title="enum std::io::SeekFrom"><code>SeekFrom</code></a> 从\n<code>std::io</code> 重新导出，以方便使用。</p>')),
])# ============================================================
# io/trait.AsyncReadExt.html (182 issues)
# Many patterns are repetitive integer read methods. Use a builder.
# ============================================================
def gen_int_read_pairs(bits, signed, endian):
    """Generate pairs for an integer read method like read_u8, read_i32_le, etc."""
    sign_word = 'signed' if signed else 'unsigned'
    sign_char = 's' if signed else 'u'
    endian_word = 'little-endian' if endian == 'le' else 'big-endian'
    bits_str = str(bits)
    # Special case for 8-bit (no endianness distinction)
    if bits == 8:
        desc_zh = f'<p>从底层读取器读取一个有符号 8 位整数。</p>' if signed else f'<p>从底层读取器读取一个无符号 8 位整数。</p>'
        example_zh = f'<p>从 <code>AsyncRead</code> 读取无符号 8 位整数：</p>'
    else:
        desc_zh = f'<p>从底层读取器以{endian_word}字节序读取一个有符号 {bits}-位整数。</p>' if signed else f'<p>从底层读取器以{endian_word}字节序读取一个无符号 {bits}-位整数。</p>'
        if endian == 'be':
            example_zh = f'<p>从 <code>AsyncRead</code> 读取有符号 {bits} 位大端整数：</p>' if signed else f'<p>从 <code>AsyncRead</code> 读取无符号 {bits} 位大端整数：</p>'
        else:
            example_zh = f'<p>从 <code>AsyncRead</code> 读取有符号 {bits} 位小端整数：</p>' if signed else f'<p>从 <code>AsyncRead</code> 读取无符号 {bits} 位小端整数：</p>'

    pairs = []

    if bits == 8:
        # u8 / i8
        if signed:
            pairs.append((E('<p>Reads a signed 8 bit integer from the underlying reader.</p>'), E(desc_zh)))
            pairs.append((E('<p>Read unsigned 8 bit integers from an <code>AsyncRead</code>:</p>'),
                         E('<p>从 <code>AsyncRead</code> 读取有符号 8 位整数：</p>')))
        else:
            pairs.append((E('<p>Reads an unsigned 8 bit integer from the underlying reader.</p>'), E(desc_zh)))
            pairs.append((E('<p>Read unsigned 8 bit integers from an <code>AsyncRead</code>:</p>'), E(example_zh)))
    else:
        # 16/32/64/128 bit, big/little endian
        if endian == 'be':
            if signed:
                pairs.append((E(f'<p>Reads a signed {bits}-bit integer in big-endian order from the\nunderlying reader.</p>'),
                             E(f'<p>从底层读取器以大端字节序读取一个有符号 {bits}-位整数。</p>')))
                pairs.append((E(f'<p>Read signed {bits} bit big-endian integers from a <code>AsyncRead</code>:</p>'),
                             E(f'<p>从 <code>AsyncRead</code> 读取有符号 {bits} 位大端整数：</p>')))
            else:
                pairs.append((E(f'<p>Reads an unsigned {bits}-bit integer in big-endian order from the\nunderlying reader.</p>'),
                             E(f'<p>从底层读取器以大端字节序读取一个无符号 {bits}-位整数。</p>')))
                pairs.append((E(f'<p>Read unsigned {bits} bit big-endian integers from a <code>AsyncRead</code>:</p>'),
                             E(f'<p>从 <code>AsyncRead</code> 读取无符号 {bits} 位大端整数：</p>')))
        else:
            if signed:
                pairs.append((E(f'<p>Reads a signed {bits}-bit integer in little-endian order from the\nunderlying reader.</p>'),
                             E(f'<p>从底层读取器以小端字节序读取一个有符号 {bits}-位整数。</p>')))
                pairs.append((E(f'<p>Read signed {bits} bit little-endian integers from a <code>AsyncRead</code>:</p>'),
                             E(f'<p>从 <code>AsyncRead</code> 读取有符号 {bits} 位小端整数：</p>')))
            else:
                pairs.append((E(f'<p>Reads an unsigned {bits}-bit integer in little-endian order from the\nunderlying reader.</p>'),
                             E(f'<p>从底层读取器以小端字节序读取一个无符号 {bits}-位整数。</p>')))
                pairs.append((E(f'<p>Read unsigned {bits} bit little-endian integers from a <code>AsyncRead</code>:</p>'),
                             E(f'<p>从 <code>AsyncRead</code> 读取无符号 {bits} 位小端整数：</p>')))
    return pairs


def gen_float_read_pairs(bits, endian):
    """Generate pairs for an float read method like read_f32_be, read_f64_le."""
    pairs = []
    if endian == 'be':
        desc = f'<p>Reads an {bits}-bit floating point type in big-endian order from the\nunderlying reader.</p>'
        desc_zh = f'<p>从底层读取器以大端字节序读取一个 {bits}-位浮点类型。</p>'
        example_zh = f'<p>从 <code>AsyncRead</code> 读取 {bits}-位浮点类型：</p>'
    else:
        desc = f'<p>Reads an {bits}-bit floating point type in little-endian order from the\nunderlying reader.</p>'
        desc_zh = f'<p>从底层读取器以小端字节序读取一个 {bits}-位浮点类型。</p>'
        example_zh = f'<p>从 <code>AsyncRead</code> 读取 {bits}-位浮点类型：</p>'

    pairs.append((E(desc), E(desc_zh)))
    pairs.append((E(f'<p>Read {bits}-bit floating point type from a <code>AsyncRead</code>:</p>'),
                 E(example_zh)))
    return pairs


async_read_ext_pairs = []

# Module-level description
async_read_ext_pairs.extend([
    (E('<p>Reads bytes from a source.</p>'), E('<p>从源读取字节。</p>')),
    (E('<p>Implemented as an extension trait, adding utility methods to all\n<a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> types. Callers will tend to import this trait instead of\n<a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a>.</p>'),
     E('<p>实现为一个扩展 trait，为所有\n<a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> 类型添加实用方法。\n调用方倾向于导入此 trait 而不是\n<a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a>。</p>')),
    (E('<p>See <a href="index.html" title="mod tokio::io">module</a> documentation for more details.</p>'),
     E('<p>更多详情请参阅 <a href="index.html" title="mod tokio::io">module</a> 文档。</p>')),
    # chain
    (E('<p>Creates a new <code>AsyncRead</code> instance that chains this stream with\n<code>next</code>.</p>'),
     E('<p>创建一个新的 <code>AsyncRead</code> 实例，将此流与 <code>next</code> 链接起来。</p>')),
    (E('<p>The returned <code>AsyncRead</code> instance will first read all bytes from this object\nuntil EOF is encountered. Afterwards the output is equivalent to the\noutput of <code>next</code>.</p>'),
     E('<p>返回的 <code>AsyncRead</code> 实例将首先从此对象读取所有字节，直到遇到 EOF。\n之后其输出与 <code>next</code> 的输出等价。</p>')),
    (E('<p><a href="../fs/struct.File.html" title="struct tokio::fs::File"><code>File</code></a>s implement <code>AsyncRead</code>:</p>'),
     E('<p><a href="../fs/struct.File.html" title="struct tokio::fs::File"><code>File</code></a> 实现了 <code>AsyncRead</code>：</p>')),
    # read
    (E('<p>Pulls some bytes from this source into the specified buffer,\nreturning how many bytes were read.</p>'),
     E('<p>从此源读取一些字节到指定的缓冲区，返回读取的字节数。</p>')),
    (E('<p>This method does not provide any guarantees about whether it\ncompletes immediately or asynchronously.</p>'),
     E('<p>此方法不保证是立即完成还是异步完成。</p>')),
    (E('<p>If the return value of this method is <code>Ok(n)</code>, then it must be\nguaranteed that <code>0 &lt;= n &lt;= buf.len()</code>. A nonzero <code>n</code> value indicates\nthat the buffer <code>buf</code> has been filled in with <code>n</code> bytes of data from\nthis source. If <code>n</code> is <code>0</code>, then it can indicate one of two\nscenarios:</p>'),
     E('<p>如果此方法的返回值是 <code>Ok(n)</code>，那么必须保证 <code>0 &lt;= n &lt;= buf.len()</code>。\n非零的 <code>n</code> 值表示缓冲区 <code>buf</code> 已从该源填充了 <code>n</code> 个字节的数据。\n如果 <code>n</code> 是 <code>0</code>，则可能表示以下两种情况之一：</p>')),
    (E('<p>No guarantees are provided about the contents of <code>buf</code> when this\nfunction is called, implementations cannot rely on any property of the\ncontents of <code>buf</code> being true. It is recommended that <em>implementations</em>\nonly write data to <code>buf</code> instead of reading its contents.</p>'),
     E('<p>此函数被调用时，<code>buf</code> 的内容没有任何保证，\n实现不能依赖 <code>buf</code> 内容的任何属性。\n建议<em>实现</em>只将数据写入 <code>buf</code>，而不要读取其内容。</p>')),
    (E('<p>Correspondingly, however, <em>callers</em> of this method may not assume\nany guarantees about how the implementation uses <code>buf</code>. It is\npossible that the code that’s supposed to write to the buffer might\nalso read from it. It is your responsibility to make sure that <code>buf</code>\nis initialized before calling <code>read</code>.</p>'),
     E('<p>相应地，<em>调用方</em>也不能假设实现如何使用 <code>buf</code> 的任何保证。\n本应写入缓冲区的代码也可能读取它。\n在调用 <code>read</code> 之前，你有责任确保 <code>buf</code> 已初始化。</p>')),
    (E('<p>If this function encounters any form of I/O or other error, an error\nvariant will be returned. If an error is returned then it must be\nguaranteed that no bytes were read.</p>'),
     E('<p>如果此函数遇到任何形式的 I/O 或其它错误，将返回一个错误变体。\n如果返回错误，则必须保证没有读取任何字节。</p>')),
    # read_buf
    (E('<p>Pulls some bytes from this source into the specified buffer,\nadvancing the buffer’s internal cursor.</p>'),
     E('<p>从此源读取一些字节到指定的缓冲区，推进缓冲区的内部光标。</p>')),
    (E('<p>Usually, only a single <code>read</code> syscall is issued, even if there is\nmore space in the supplied buffer.</p>'),
     E('<p>通常，即使提供的缓冲区有更多空间，也只会发出单个 <code>read</code> 系统调用。</p>')),
    (E('<p>A nonzero <code>n</code> value indicates that the buffer <code>buf</code> has been filled\nin with <code>n</code> bytes of data from this source. If <code>n</code> is <code>0</code>, then it\ncan indicate one of two scenarios:</p>'),
     E('<p>非零的 <code>n</code> 值表示缓冲区 <code>buf</code> 已从该源填充了 <code>n</code> 个字节的数据。\n如果 <code>n</code> 是 <code>0</code>，则可能表示以下两种情况之一：</p>')),
    # read_exact
    (E('<p><a href="../fs/struct.File.html" title="struct tokio::fs::File"><code>File</code></a> implements <code>Read</code> and <a href="../../bytes/bytes_mut/struct.BytesMut.html" title="struct bytes::bytes_mut::BytesMut"><code>BytesMut</code></a> implements <a href="../../bytes/buf/buf_mut/trait.BufMut.html" title="trait bytes::buf::buf_mut::BufMut"><code>BufMut</code></a>:</p>'),
     E('<p><a href="../fs/struct.File.html" title="struct tokio::fs::File"><code>File</code></a> 实现了 <code>Read</code>，<a href="../../bytes/bytes_mut/struct.BytesMut.html" title="struct bytes::bytes_mut::BytesMut"><code>BytesMut</code></a> 实现了 <a href="../../bytes/buf/buf_mut/trait.BufMut.html" title="trait bytes::buf::buf_mut::BufMut"><code>BufMut</code></a>：</p>')),
    (E('<p>Reads the exact number of bytes required to fill <code>buf</code>.</p>'),
     E('<p>读取精确数量的字节以填满 <code>buf</code>。</p>')),
    (E('<p>This function reads as many bytes as necessary to completely fill\nthe specified buffer <code>buf</code>.</p>'),
     E('<p>此函数读取必要的字节数，以完全填满指定的缓冲区 <code>buf</code>。</p>')),
    (E('<p>If the operation encounters an \xe2\x80\x9cend of file\xe2\x80\x9d before completely\nfilling the buffer, it returns an error of the kind\n<a href="https://doc.rust-lang.org/1.95.0/std/io/error/enum.ErrorKind.html#variant.UnexpectedEof" title="variant std::io::error::ErrorKind::UnexpectedEof"><code>ErrorKind::UnexpectedEof</code></a>. The contents of <code>buf</code> are unspecified\nin this case.</p>'),
     E('<p>如果在完全填满缓冲区之前遇到\xe2\x80\x9c文件末尾\xe2\x80\x9d，\n则返回类型为\n<a href="https://doc.rust-lang.org/1.95.0/std/io/error/enum.ErrorKind.html#variant.UnexpectedEof" title="variant std::io::error::ErrorKind::UnexpectedEof"><code>ErrorKind::UnexpectedEof</code></a> 的错误。\n在这种情况下，<code>buf</code> 的内容未指定。</p>')),
    (E('<p>If any other read error is encountered then the operation\nimmediately returns. The contents of <code>buf</code> are unspecified in this\ncase.</p>'),
     E('<p>如果遇到任何其它读取错误，则操作立即返回。\n在这种情况下，<code>buf</code> 的内容未指定。</p>')),
    (E('<p>If this operation returns an error, it is unspecified how many bytes\nit has read, but it will never read more than would be necessary to\ncompletely fill the buffer.</p>'),
     E('<p>如果此操作返回错误，则已读取的字节数未指定，\n但它绝不会读取超过填满缓冲区所需的字节数。</p>')),
    (E('<p><a href="../fs/struct.File.html" title="struct tokio::fs::File"><code>File</code></a>s implement <code>Read</code>:</p>'),
     E('<p><a href="../fs/struct.File.html" title="struct tokio::fs::File"><code>File</code></a> 实现了 <code>Read</code>：</p>')),
])

# Integer read methods (using helper)
for bits in [8]:
    for signed in [False, True]:
        async_read_ext_pairs.extend(gen_int_read_pairs(bits, signed, 'be'))

for bits in [16, 32, 64, 128]:
    for signed in [False, True]:
        for endian in ['be', 'le']:
            async_read_ext_pairs.extend(gen_int_read_pairs(bits, signed, endian))

# Common pairs for integer reads (buffered + same errors)
async_read_ext_pairs.extend([
    (E('<p>It is recommended to use a buffered reader to avoid excessive\nsyscalls.</p>'),
     E('<p>建议使用缓冲读取器以避免过多的系统调用。</p>')),
    (E('<p>This method returns the same errors as <a href="trait.AsyncReadExt.html#method.read_exact" title="method tokio::io::AsyncReadExt::read_exact"><code>AsyncReadExt::read_exact</code></a>.</p>'),
     E('<p>此方法返回的错误与 <a href="trait.AsyncReadExt.html#method.read_exact" title="method tokio::io::AsyncReadExt::read_exact"><code>AsyncReadExt::read_exact</code></a> 相同。</p>')),
    (E('<p>This method is cancel safe. If this method is used as an event in a\n<a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> statement and some other branch\ncompletes first, it is guaranteed that no data were read.</p>'),
     E('<p>此方法是可取消安全的。如果在 <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> 语句中将其作为事件，\n而其他分支先完成，则保证不会读取任何数据。</p>')),
])

# Float read methods
for bits in [32, 64]:
    for endian in ['be', 'le']:
        async_read_ext_pairs.extend(gen_float_read_pairs(bits, endian))

# read_to_end
async_read_ext_pairs.extend([
    (E('<p>Reads all bytes until EOF in this source, placing them into <code>buf</code>.</p>'),
     E('<p>读取此源中直到 EOF 的所有字节，将它们放入 <code>buf</code>。</p>')),
    (E('<p>All bytes read from this source will be appended to the specified\nbuffer <code>buf</code>. This function will continuously call <a href="trait.AsyncReadExt.html#method.read" title="method tokio::io::AsyncReadExt::read"><code>read()</code></a> to\nappend more data to <code>buf</code> until <a href="trait.AsyncReadExt.html#method.read" title="method tokio::io::AsyncReadExt::read"><code>read()</code></a> returns <code>Ok(0)</code>.</p>'),
     E('<p>从此源读取的所有字节都将追加到指定的缓冲区 <code>buf</code> 中。\n此函数会持续调用 <a href="trait.AsyncReadExt.html#method.read" title="method tokio::io::AsyncReadExt::read"><code>read()</code></a> 以向 <code>buf</code> 追加更多数据，\n直到 <a href="trait.AsyncReadExt.html#method.read" title="method tokio::io::AsyncReadExt::read"><code>read()</code></a> 返回 <code>Ok(0)</code>。</p>')),
    (E('<p>If successful, the total number of bytes read is returned.</p>'),
     E('<p>如果成功，则返回读取的总字节数。</p>')),
    (E('<p>If a read error is encountered then the <code>read_to_end</code> operation\nimmediately completes. Any bytes which have already been read will\nbe appended to <code>buf</code>.</p>'),
     E('<p>如果遇到读取错误，则 <code>read_to_end</code> 操作立即完成。\n已经读取的任何字节都将追加到 <code>buf</code> 中。</p>')),
    (E('<p>(See also the <a href="../fs/fn.read.html" title="fn tokio::fs::read"><code>tokio::fs::read</code></a> convenience function for reading from a\nfile.)</p>'),
     E('<p>（另请参阅便捷函数 <a href="../fs/fn.read.html" title="fn tokio::fs::read"><code>tokio::fs::read</code></a> 用于从文件读取。）</p>')),
    # read_to_string
    (E('<p>Reads all bytes until EOF in this source, appending them to <code>buf</code>.</p>'),
     E('<p>读取此源中直到 EOF 的所有字节，将它们追加到 <code>buf</code>。</p>')),
    (E('<p>If successful, the number of bytes which were read and appended to\n<code>buf</code> is returned.</p>'),
     E('<p>如果成功，则返回读取并追加到 <code>buf</code> 中的字节数。</p>')),
    (E('<p>If the data in this stream is <em>not</em> valid UTF-8 then an error is\nreturned and <code>buf</code> is unchanged.</p>'),
     E('<p>如果此流中的数据<em>不是</em>有效的 UTF-8，则返回错误且 <code>buf</code> 不变。</p>')),
    (E('<p>See <a href="trait.AsyncReadExt.html#method.read_to_end" title="method tokio::io::AsyncReadExt::read_to_end"><code>read_to_end</code></a> for other error semantics.</p>'),
     E('<p>有关其它错误语义，请参阅 <a href="trait.AsyncReadExt.html#method.read_to_end" title="method tokio::io::AsyncReadExt::read_to_end"><code>read_to_end</code></a>。</p>')),
    (E('<p>(See also the <a href="../fs/fn.read_to_string.html" title="fn tokio::fs::read_to_string"><code>crate::fs::read_to_string</code></a> convenience function for\nreading from a file.)</p>'),
     E('<p>（另请参阅便捷函数 <a href="../fs/fn.read_to_string.html" title="fn tokio::fs::read_to_string"><code>crate::fs::read_to_string</code></a> 用于从文件读取。）</p>')),
    # take
    (E('<p>Creates an adaptor which reads at most <code>limit</code> bytes from it.</p>'),
     E('<p>创建一个适配器，最多从中读取 <code>limit</code> 个字节。</p>')),
    (E('<p>This function returns a new instance of <code>AsyncRead</code> which will read\nat most <code>limit</code> bytes, after which it will always return EOF\n(<code>Ok(0)</code>). Any read errors will not count towards the number of\nbytes read and future calls to <a href="trait.AsyncReadExt.html#method.read" title="method tokio::io::AsyncReadExt::read"><code>read()</code></a> may succeed.</p>'),
     E('<p>此函数返回一个新的 <code>AsyncRead</code> 实例，\n它最多读取 <code>limit</code> 个字节，\n之后将始终返回 EOF（<code>Ok(0)</code>）。\n任何读取错误都不会计入已读取的字节数，\n后续对 <a href="trait.AsyncReadExt.html#method.read" title="method tokio::io::AsyncReadExt::read"><code>read()</code></a> 的调用仍可能成功。</p>')),
])

add('io/trait.AsyncReadExt.html', async_read_ext_pairs)# ============================================================
# io/trait.AsyncWriteExt.html (153 issues)
# Many patterns are repetitive integer write methods. Use a builder.
# ============================================================
def gen_int_write_pairs(bits, signed, endian):
    """Generate pairs for an integer write method like write_u8, write_i32_le, etc."""
    pairs = []
    if bits == 8:
        if signed:
            desc_zh = f'<p>向底层写入器写入一个有符号 8 位整数。</p>'
            example_zh = f'<p>向 <code>AsyncWrite</code> 写入有符号 8 位整数：</p>'
        else:
            desc_zh = f'<p>向底层写入器写入一个无符号 8 位整数。</p>'
            example_zh = f'<p>向 <code>AsyncWrite</code> 写入无符号 8 位整数：</p>'
    else:
        endian_word = 'little-endian' if endian == 'le' else 'big-endian'
        endian_zh = '小端字节序' if endian == 'le' else '大端字节序'
        if signed:
            desc_zh = f'<p>以{endian_zh}字节序向底层写入器写入一个有符号 {bits}-位整数。</p>'
        else:
            desc_zh = f'<p>以{endian_zh}字节序向底层写入器写入一个无符号 {bits}-位整数。</p>'
        endian_zh_word = '小端' if endian == 'le' else '大端'
        sign_word = '有符号' if signed else '无符号'
        example_zh = f'<p>向 <code>AsyncWrite</code> 写入{sign_word} {bits} 位{endian_zh_word}整数：</p>'

    if bits == 8:
        if signed:
            pairs.append((E('<p>Writes a signed 8-bit integer to the underlying writer.</p>'), E(desc_zh)))
        else:
            pairs.append((E('<p>Writes an unsigned 8-bit integer to the underlying writer.</p>'), E(desc_zh)))
    else:
        if endian == 'be':
            if signed:
                pairs.append((E(f'<p>Writes a signed {bits}-bit integer in big-endian order to the\nunderlying writer.</p>'),
                             E(f'<p>以大端字节序向底层写入器写入一个有符号 {bits}-位整数。</p>')))
                pairs.append((E(f'<p>Write signed {bits}-bit integers to a <code>AsyncWrite</code>:</p>'),
                             E(f'<p>向 <code>AsyncWrite</code> 写入有符号 {bits} 位大端整数：</p>')))
            else:
                pairs.append((E(f'<p>Writes an unsigned {bits}-bit integer in big-endian order to the\nunderlying writer.</p>'),
                             E(f'<p>以大端字节序向底层写入器写入一个无符号 {bits}-位整数。</p>')))
                pairs.append((E(f'<p>Write unsigned {bits}-bit integers to a <code>AsyncWrite</code>:</p>'),
                             E(f'<p>向 <code>AsyncWrite</code> 写入无符号 {bits} 位大端整数：</p>')))
        else:
            if signed:
                pairs.append((E(f'<p>Writes a signed {bits}-bit integer in little-endian order to the\nunderlying writer.</p>'),
                             E(f'<p>以小端字节序向底层写入器写入一个有符号 {bits}-位整数。</p>')))
                pairs.append((E(f'<p>Write signed {bits}-bit integers to a <code>AsyncWrite</code>:</p>'),
                             E(f'<p>向 <code>AsyncWrite</code> 写入有符号 {bits} 位小端整数：</p>')))
            else:
                pairs.append((E(f'<p>Writes an unsigned {bits}-bit integer in little-endian order to the\nunderlying writer.</p>'),
                             E(f'<p>以小端字节序向底层写入器写入一个无符号 {bits}-位整数。</p>')))
                pairs.append((E(f'<p>Write unsigned {bits}-bit integers to a <code>AsyncWrite</code>:</p>'),
                             E(f'<p>向 <code>AsyncWrite</code> 写入无符号 {bits} 位小端整数：</p>')))
    return pairs


def gen_float_write_pairs(bits, endian):
    """Generate pairs for a float write method like write_f32_be, write_f64_le."""
    pairs = []
    endian_zh = '小端字节序' if endian == 'le' else '大端字节序'
    if endian == 'be':
        desc = f'<p>Writes an {bits}-bit floating point type in big-endian order to the\nunderlying writer.</p>'
        example_zh = f'<p>向 <code>AsyncWrite</code> 写入 {bits}-位浮点类型：</p>'
    else:
        desc = f'<p>Writes an {bits}-bit floating point type in little-endian order to the\nunderlying writer.</p>'
        example_zh = f'<p>向 <code>AsyncWrite</code> 写入 {bits}-位浮点类型：</p>'

    pairs.append((E(desc), E(f'<p>以{endian_zh}向底层写入器写入一个 {bits}-位浮点类型。</p>')))
    pairs.append((E(f'<p>Write {bits}-bit floating point type to a <code>AsyncWrite</code>:</p>'),
                 E(example_zh)))
    return pairs


async_write_ext_pairs = []

# Module-level description
async_write_ext_pairs.extend([
    (E('<p>Writes bytes to a sink.</p>'), E('<p>将字节写入到接收器（sink）。</p>')),
    (E('<p>Implemented as an extension trait, adding utility methods to all\n<a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> types. Callers will tend to import this trait instead of\n<a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a>.</p>'),
     E('<p>实现为一个扩展 trait，为所有\n<a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> 类型添加实用方法。\n调用方倾向于导入此 trait 而不是\n<a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a>。</p>')),
    (E('<p>See <a href="index.html" title="mod tokio::io">module</a> documentation for more details.</p>'),
     E('<p>更多详情请参阅 <a href="index.html" title="mod tokio::io">module</a> 文档。</p>')),
    # write
    (E('<p>Writes a buffer into this writer, returning how many bytes were\nwritten.</p>'),
     E('<p>将缓冲区写入此写入器，返回写入的字节数。</p>')),
    (E('<p>This function will attempt to write the entire contents of <code>buf</code>, but\nthe entire write may not succeed, or the write may also generate an\nerror. A call to <code>write</code> represents <em>at most one</em> attempt to write to\nany wrapped object.</p>'),
     E('<p>此函数将尝试写入 <code>buf</code> 的全部内容，但整个写入可能不会成功，\n或者写入也可能产生错误。\n对 <code>write</code> 的一次调用最多表示对任何包装对象的一次写入尝试。</p>')),
    (E('<p>If the return value is <code>Ok(n)</code> then it must be guaranteed that <code>n &lt;= buf.len()</code>. A return value of <code>0</code> typically means that the\nunderlying object is no longer able to accept bytes and will likely\nnot be able to in the future as well, or that the buffer provided is\nempty.</p>'),
     E('<p>如果返回值是 <code>Ok(n)</code>，则必须保证 <code>n &lt;= buf.len()</code>。\n返回值为 <code>0</code> 通常表示底层对象已经无法再接受字节，\n未来可能也无法再接受；或者提供的缓冲区为空。</p>')),
    (E('<p>Each call to <code>write</code> may generate an I/O error indicating that the\noperation could not be completed. If an error is returned then no bytes\nin the buffer were written to this writer.</p>'),
     E('<p>每次对 <code>write</code> 的调用都可能产生 I/O 错误，\n表明该操作无法完成。如果返回错误，\n那么缓冲区中没有任何字节被写入此写入器。</p>')),
    (E('<p>It is <strong>not</strong> considered an error if the entire buffer could not be\nwritten to this writer.</p>'),
     E('<p>如果整个缓冲区无法写入此写入器，这<strong>不</strong>被视为错误。</p>')),
    (E('<p>This method is cancellation safe in the sense that if it is used as\nthe event in a <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> statement and some\nother branch completes first, then it is guaranteed that no data was\nwritten to this <code>AsyncWrite</code>.</p>'),
     E('<p>此方法是可取消安全的：如果在 <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> 语句中将其作为事件，\n而其他分支先完成，则保证不会向此 <code>AsyncWrite</code> 写入任何数据。</p>')),
    # write_vectored
    (E('<p>Like <a href="trait.AsyncWriteExt.html#method.write" title="method tokio::io::AsyncWriteExt::write"><code>write</code></a>, except that it writes from a slice of buffers.</p>'),
     E('<p>与 <a href="trait.AsyncWriteExt.html#method.write" title="method tokio::io::AsyncWriteExt::write"><code>write</code></a> 类似，但从一组缓冲区中写入数据。</p>')),
    (E('<p>See <a href="trait.AsyncWrite.html#method.poll_write_vectored" title="method tokio::io::AsyncWrite::poll_write_vectored"><code>AsyncWrite::poll_write_vectored</code></a> for more details.</p>'),
     E('<p>更多详情请参阅 <a href="trait.AsyncWrite.html#method.poll_write_vectored" title="method tokio::io::AsyncWrite::poll_write_vectored"><code>AsyncWrite::poll_write_vectored</code></a>。</p>')),
    # write_buf
    (E('<p>Writes a buffer into this writer, advancing the buffer’s internal\ncursor.</p>'),
     E('<p>将缓冲区写入此写入器，推进缓冲区的内部光标。</p>')),
    (E('<p>This function will attempt to write the entire contents of <code>buf</code>, but\nthe entire write may not succeed, or the write may also generate an\nerror. After the operation completes, the buffer’s\ninternal cursor is advanced by the number of bytes written. A\nsubsequent call to <code>write_buf</code> using the <strong>same</strong> <code>buf</code> value will\nresume from the point that the first call to <code>write_buf</code> completed.\nA call to <code>write_buf</code> represents <em>at most one</em> attempt to write to any\nwrapped object.</p>'),
     E('<p>此函数将尝试写入 <code>buf</code> 的全部内容，但整个写入可能不会成功，\n或者写入也可能产生错误。\n操作完成后，缓冲区的内部光标会按写入的字节数向前推进。\n使用<strong>同一个</strong> <code>buf</code> 值对 <code>write_buf</code> 的后续调用，\n将从上一次 <code>write_buf</code> 调用完成时的位置继续。\n对 <code>write_buf</code> 的一次调用最多表示对任何包装对象的一次写入尝试。</p>')),
    # write_all_buf
    (E('<p><a href="../fs/struct.File.html" title="struct tokio::fs::File"><code>File</code></a> implements <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> and <a href="https://doc.rust-lang.org/1.95.0/std/io/cursor/struct.Cursor.html" title="struct std::io::cursor::Cursor"><code>Cursor</code></a><code>&lt;&amp;[u8]&gt;</code> implements <a href="../../bytes/buf/buf_impl/trait.Buf.html" title="trait bytes::buf::buf_impl::Buf"><code>Buf</code></a>:</p>'),
     E('<p><a href="../fs/struct.File.html" title="struct tokio::fs::File"><code>File</code></a> 实现了 <a href="trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a>，\n<a href="https://doc.rust-lang.org/1.95.0/std/io/cursor/struct.Cursor.html" title="struct std::io::cursor::Cursor"><code>Cursor</code></a><code>&lt;&amp;[u8]&gt;</code> 实现了 <a href="../../bytes/buf/buf_impl/trait.Buf.html" title="trait bytes::buf::buf_impl::Buf"><code>Buf</code></a>：</p>')),
    (E('<p>Attempts to write an entire buffer into this writer.</p>'),
     E('<p>尝试将整个缓冲区写入此写入器。</p>')),
    (E('<p>This method will continuously call <a href="trait.AsyncWriteExt.html#method.write" title="method tokio::io::AsyncWriteExt::write"><code>write</code></a> until\n<a href="../../bytes/buf/buf_impl/trait.Buf.html#method.has_remaining" title="method bytes::buf::buf_impl::Buf::has_remaining"><code>buf.has_remaining()</code></a> returns false. This method will not\nreturn until the entire buffer has been successfully written or an error occurs. The\nfirst error generated will be returned.</p>'),
     E('<p>此方法会持续调用 <a href="trait.AsyncWriteExt.html#method.write" title="method tokio::io::AsyncWriteExt::write"><code>write</code></a>，\n直到 <a href="../../bytes/buf/buf_impl/trait.Buf.html#method.has_remaining" title="method bytes::buf::buf_impl::Buf::has_remaining"><code>buf.has_remaining()</code></a> 返回 false。\n此方法在缓冲区被完全写入或发生错误之前不会返回。\n返回生成的第一个错误。</p>')),
    (E('<p>The buffer is advanced after each chunk is successfully written. After failure,\n<code>src.chunk()</code> will return the chunk that failed to write.</p>'),
     E('<p>缓冲区在每次成功写入一块后都会推进。\n失败后，<code>src.chunk()</code> 将返回写入失败的那个块。</p>')),
    (E('<p>If <code>write_all_buf</code> is used as the event in a\n<a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> statement and some other branch\ncompletes first, then the data in the provided buffer may have been\npartially written. However, it is guaranteed that the provided\nbuffer has been <a href="../../bytes/buf/buf_impl/trait.Buf.html#tymethod.advance" title="method bytes::buf::buf_impl::Buf::advance">advanced</a> by the amount of bytes that have been\npartially written.</p>'),
     E('<p>如果在 <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> 语句中将 <code>write_all_buf</code> 作为事件，\n而其他分支先完成，那么提供的缓冲区中的数据可能被部分写入。\n但可以保证提供的缓冲区已<a href="../../bytes/buf/buf_impl/trait.Buf.html#tymethod.advance" title="method bytes::buf::buf_impl::Buf::advance">推进</a>了已被部分写入的字节数。</p>')),
    # write_all
    (E('<p>This method will continuously call <a href="trait.AsyncWriteExt.html#method.write" title="method tokio::io::AsyncWriteExt::write"><code>write</code></a> until there is no more data\nto be written. This method will not return until the entire buffer\nhas been successfully written or such an error occurs. The first\nerror generated from this method will be returned.</p>'),
     E('<p>此方法会持续调用 <a href="trait.AsyncWriteExt.html#method.write" title="method tokio::io::AsyncWriteExt::write"><code>write</code></a>，\n直到没有更多数据可写。\n此方法在缓冲区被完全写入或发生错误之前不会返回。\n返回此方法生成的第一个错误。</p>')),
    (E('<p>This method is not cancellation safe. If it is used as the event\nin a <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> statement and some\nother branch completes first, then the provided buffer may have been\npartially written, but future calls to <code>write_all</code> will start over\nfrom the beginning of the buffer.</p>'),
     E('<p>此方法不可取消安全。如果在 <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> 语句中将其作为事件，\n而其他分支先完成，那么提供的缓冲区可能被部分写入，\n但后续对 <code>write_all</code> 的调用将从缓冲区的开头重新开始。</p>')),
    (E('<p>This function will return the first error that <a href="trait.AsyncWriteExt.html#method.write" title="method tokio::io::AsyncWriteExt::write"><code>write</code></a> returns.</p>'),
     E('<p>此函数将返回 <a href="trait.AsyncWriteExt.html#method.write" title="method tokio::io::AsyncWriteExt::write"><code>write</code></a> 返回的第一个错误。</p>')),
])

# Integer write methods
for bits in [8]:
    for signed in [False, True]:
        async_write_ext_pairs.extend(gen_int_write_pairs(bits, signed, 'be'))

for bits in [16, 32, 64, 128]:
    for signed in [False, True]:
        for endian in ['be', 'le']:
            async_write_ext_pairs.extend(gen_int_write_pairs(bits, signed, endian))

# Common pairs for integer writes
async_write_ext_pairs.extend([
    (E('<p>It is recommended to use a buffered writer to avoid excessive\nsyscalls.</p>'),
     E('<p>建议使用缓冲写入器以避免过多的系统调用。</p>')),
    (E('<p>This method returns the same errors as <a href="trait.AsyncWriteExt.html#method.write_all" title="method tokio::io::AsyncWriteExt::write_all"><code>AsyncWriteExt::write_all</code></a>.</p>'),
     E('<p>此方法返回的错误与 <a href="trait.AsyncWriteExt.html#method.write_all" title="method tokio::io::AsyncWriteExt::write_all"><code>AsyncWriteExt::write_all</code></a> 相同。</p>')),
])

# Float write methods
for bits in [32, 64]:
    for endian in ['be', 'le']:
        async_write_ext_pairs.extend(gen_float_write_pairs(bits, endian))

# flush, shutdown
async_write_ext_pairs.extend([
    (E('<p>Flushes this output stream, ensuring that all intermediately buffered\ncontents reach their destination.</p>'),
     E('<p>刷新此输出流，确保所有中间缓冲的内容都到达目的地。</p>')),
    (E('<p>It is considered an error if not all bytes could be written due to\nI/O errors or EOF being reached.</p>'),
     E('<p>如果由于 I/O 错误或到达 EOF 而无法写入所有字节，则视为错误。</p>')),
    (E('<p>This method is cancel safe.</p>'),
     E('<p>此方法是可取消安全的。</p>')),
    (E('<p>If <code>flush</code> is used as the event in a <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a>\nstatement and some other branch completes first, then the data in the\nbuffered data in this <code>AsyncWrite</code> may have been partially flushed.\nHowever, it is guaranteed that the buffer is advanced by the amount of\nbytes that have been partially flushed.</p>'),
     E('<p>如果在 <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> 语句中将 <code>flush</code> 作为事件，\n而其他分支先完成，那么此 <code>AsyncWrite</code> 缓冲区中的数据可能被部分刷新。\n但可以保证缓冲区已按已被部分刷新的字节数推进。</p>')),
    (E('<p>Shuts down the output stream, ensuring that the value can be dropped\ncleanly.</p>'),
     E('<p>关闭输出流，确保该值能被干净地丢弃。</p>')),
    (E('<p>Similar to <a href="trait.AsyncWriteExt.html#method.flush" title="method tokio::io::AsyncWriteExt::flush"><code>flush</code></a>, all intermediately buffered content is written to\nthe underlying stream. Once the operation completes, the caller should\nno longer attempt to write to the stream. For example, the\n<code>TcpStream</code> implementation will issue a <code>shutdown(Write)</code> sys call.</p>'),
     E('<p>与 <a href="trait.AsyncWriteExt.html#method.flush" title="method tokio::io::AsyncWriteExt::flush"><code>flush</code></a> 类似，所有中间缓冲的内容都会写入到底层流。\n操作完成后，调用方不应再尝试向流写入数据。\n例如，<code>TcpStream</code> 的实现会发出 <code>shutdown(Write)</code> 系统调用。</p>')),
])

add('io/trait.AsyncWriteExt.html', async_write_ext_pairs)


# ============================================================
# main()
# ============================================================
def main():
    """Apply all pairs to files."""
    total_replacements = 0
    files_modified = 0

    # Apply common pairs first
    for rel, pairs in PLAN:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            continue

    # Process all files
    for rel, pairs in PLAN:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            print(f'NOT FOUND: {path}')
            continue
        try:
            original = read_bytes(rel)
        except Exception as e:
            print(f'ERROR reading {path}: {e}')
            continue

        content = original
        local_replacements = 0
        unmatched = []

        for en_b, zh_b in pairs:
            # Try LF first
            if en_b in content:
                count = content.count(en_b)
                local_replacements += count
                content = content.replace(en_b, zh_b)
                continue
            # Try CRLF variant
            en_crlf = en_b.replace(b'\n', b'\r\n')
            zh_crlf = zh_b.replace(b'\n', b'\r\n')
            if en_crlf in content:
                count = content.count(en_crlf)
                local_replacements += count
                content = content.replace(en_crlf, zh_crlf)
                continue
            unmatched.append(en_b[:80])

        if content != original:
            write_bytes(rel, content)
            files_modified += 1
            print(f'{rel}: {local_replacements} replacements' + (f' ({len(unmatched)} unmatched patterns!)' if unmatched else ''))
            if unmatched:
                for u in unmatched[:5]:
                    print(f'   UNMATCHED: {u!r}...')
                if len(unmatched) > 5:
                    print(f'   ... and {len(unmatched)-5} more unmatched')
        else:
            print(f'{rel}: NO changes' + (f' ({len(unmatched)} unmatched patterns!)' if unmatched else ''))
            if unmatched:
                for u in unmatched[:5]:
                    print(f'   UNMATCHED: {u!r}...')

        total_replacements += local_replacements

    print(f'\nTotal: {total_replacements} replacements across {files_modified} files')


if __name__ == '__main__':
    main()