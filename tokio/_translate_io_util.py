"""Batch 2: translate remaining untranslated docblocks.

After running _translate_macros.py:
- 100 OWN docblocks + 245 Top-doc still untranslated
- Most are io-util related (BufReader, AsyncReadExt, etc.)
- HTML uses <a href=...><code>X</code></a> inline links

This script reads audit_full.txt and applies byte-level translations.
"""
import os, re

TOKIO_ROOT = 'D:/Administrator/Documents/Code/rust_doc_all/tokio'

def b(s):
    return s.replace('\n', '\r\n').encode('utf-8')

def c(s):
    return s.replace('\n', '\r\n').encode('utf-8')

# (en_bytes_with_crlf, zh_bytes_with_crlf)
PAIRS = [
    # ============== fs/struct.File.html ==============
    (b('<p>Get the maximum buffer size for the underlying <a href="../io/trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> / <a href="../io/trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> operation.</p>'),
     c('<p>获取底层 <a href="../io/trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> / <a href="../io/trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> 操作的最大缓冲区大小。</p>')),

    # ============== io/struct.BufReader.html ==============
    (b('<p>Creates a new <code>BufReader</code> with a default buffer capacity. The default is currently 8 KB, but may change in the future.</p>'),
     c('<p>使用默认缓冲区容量创建一个新的 <code>BufReader</code>。默认容量目前为 8 KB，未来可能会更改。</p>')),
    (b('<p>Creates a new <code>BufReader</code> with the specified buffer capacity.</p>'),
     c('<p>使用指定的缓冲区容量创建一个新的 <code>BufReader</code>。</p>')),
    (b('<p>Gets a reference to the underlying reader. It is inadvisable to directly read from the underlying reader.</p>'),
     c('<p>获取底层 reader 的引用。不建议直接从底层 reader 读取。</p>')),
    (b('<p>Gets a mutable reference to the underlying reader. It is inadvisable to directly read from the underlying reader.</p>'),
     c('<p>获取底层 reader 的可变引用。不建议直接从底层 reader 读取。</p>')),
    (b('<p>Gets a pinned mutable reference to the underlying reader. It is inadvisable to directly read from the underlying reader.</p>'),
     c('<p>获取底层 reader 的固定可变引用。不建议直接从底层 reader 读取。</p>')),
    (b('<p>Consumes this <code>BufReader</code>, returning the underlying reader. Note that any leftover data in the internal buffer is lost.</p>'),
     c('<p>消费此 <code>BufReader</code>，返回底层 reader。请注意，内部缓冲区中的任何剩余数据都会丢失。</p>')),
    (b('<p>Returns a reference to the internally buffered data. Unlike <code>fill_buf</code>, this will not attempt to fill the buffer if it is empty.</p>'),
     c('<p>返回内部缓冲数据的引用。与 <code>fill_buf</code> 不同，如果缓冲区为空，它不会尝试填充缓冲区。</p>')),
    (b('<p>Returns a mutable reference to the internally buffered data.</p>'),
     c('<p>返回内部缓冲数据的可变引用。</p>')),
    (b('<p>Returns a pinned mutable reference to the internally buffered data.</p>'),
     c('<p>返回内部缓冲数据的固定可变引用。</p>')),
    (b('<p>Read bytes from this <code>BufReader</code> into the provided buffer.</p>'),
     c('<p>从此 <code>BufReader</code> 读取字节到提供的缓冲区中。</p>')),
    (b('<p>Write bytes from the provided buffer into this <code>BufReader</code>.</p>'),
     c('<p>从提供的缓冲区写入字节到此 <code>BufReader</code>。</p>')),

    # ============== io/struct.BufStream.html ==============
    (b('<p>Wraps a type in both <code>BufWriter</code> and <code>BufReader</code>. See the documentation for those types and <code>BufStream</code> for details.</p>'),
     c('<p>将一个类型同时包装为 <code>BufWriter</code> 和 <code>BufReader</code>。详情请参见这些类型和 <code>BufStream</code> 的文档。</p>')),
    (b('<p>Creates a <code>BufStream</code> with the specified <code>BufReader</code> capacity and <code>BufWriter</code> capacity. See the documentation for those types and <code>BufStream</code> for details.</p>'),
     c('<p>使用指定的 <code>BufReader</code> 容量和 <code>BufWriter</code> 容量创建一个 <code>BufStream</code>。详情请参见这些类型和 <code>BufStream</code> 的文档。</p>')),
    (b('<p>Gets a reference to the underlying I/O object. It is inadvisable to directly read from the underlying I/O object.</p>'),
     c('<p>获取底层 I/O 对象的引用。不建议直接从底层 I/O 对象读取。</p>')),
    (b('<p>Gets a mutable reference to the underlying I/O object. It is inadvisable to directly read from the underlying I/O object.</p>'),
     c('<p>获取底层 I/O 对象的可变引用。不建议直接从底层 I/O 对象读取。</p>')),
    (b('<p>Gets a pinned mutable reference to the underlying I/O object. It is inadvisable to directly read from the underlying I/O object.</p>'),
     c('<p>获取底层 I/O 对象的固定可变引用。不建议直接从底层 I/O 对象读取。</p>')),
    (b('<p>Consumes this <code>BufStream</code>, returning the underlying I/O object. Note that any leftover data in the internal buffer is lost.</p>'),
     c('<p>消费此 <code>BufStream</code>，返回底层 I/O 对象。请注意，内部缓冲区中的任何剩余数据都会丢失。</p>')),

    # ============== io/struct.BufWriter.html ==============
    (b('<p>Creates a new <code>BufWriter</code> with a default buffer capacity. The default is currently 8 KB, but may change in the future.</p>'),
     c('<p>使用默认缓冲区容量创建一个新的 <code>BufWriter</code>。默认容量目前为 8 KB，未来可能会更改。</p>')),
    (b('<p>Creates a new <code>BufWriter</code> with the specified buffer capacity.</p>'),
     c('<p>使用指定的缓冲区容量创建一个新的 <code>BufWriter</code>。</p>')),
    (b('<p>Gets a reference to the underlying writer.</p>'),
     c('<p>获取底层 writer 的引用。</p>')),
    (b('<p>Gets a mutable reference to the underlying writer. It is inadvisable to directly write to the underlying writer.</p>'),
     c('<p>获取底层 writer 的可变引用。不建议直接写入底层 writer。</p>')),
    (b('<p>Gets a pinned mutable reference to the underlying writer. It is inadvisable to directly write to the underlying writer.</p>'),
     c('<p>获取底层 writer 的固定可变引用。不建议直接写入底层 writer。</p>')),
    (b('<p>Consumes this <code>BufWriter</code>, returning the underlying writer. Note that any leftover data in the internal buffer is lost.</p>'),
     c('<p>消费此 <code>BufWriter</code>，返回底层 writer。请注意，内部缓冲区中的任何剩余数据都会丢失。</p>')),
    (b('<p>Returns a reference to the internally buffered data.</p>'),
     c('<p>返回内部缓冲数据的引用。</p>')),
    (b('<p>Read bytes from this <code>BufWriter</code> into the provided buffer.</p>'),
     c('<p>从此 <code>BufWriter</code> 读取字节到提供的缓冲区中。</p>')),

    # ============== io/struct.Chain.html ==============
    (b('<p>Gets references to the underlying readers in this <code>Chain</code>.</p>'),
     c('<p>获取此 <code>Chain</code> 中底层 reader 的引用。</p>')),
    (b('<p>Gets mutable references to the underlying readers in this <code>Chain</code>. Care should be taken to avoid modifying the internal I/O state of the underlying readers as doing so may corrupt the internal state of this <code>Chain</code>.</p>'),
     c('<p>获取此 <code>Chain</code> 中底层 reader 的可变引用。需要注意避免修改底层 reader 的内部 I/O 状态，因为这样做可能会损坏此 <code>Chain</code> 的内部状态。</p>')),
    (b('<p>Gets pinned mutable references to the underlying readers in this <code>Chain</code>. Care should be taken to avoid modifying the internal I/O state of the underlying readers as doing so may corrupt the internal state of this <code>Chain</code>.</p>'),
     c('<p>获取此 <code>Chain</code> 中底层 reader 的固定可变引用。需要注意避免修改底层 reader 的内部 I/O 状态，因为这样做可能会损坏此 <code>Chain</code> 的内部状态。</p>')),
    (b('<p>Consumes the <code>Chain</code>, returning the wrapped readers.</p>'),
     c('<p>消费此 <code>Chain</code>，返回被包装的 reader。</p>')),

    # ============== io/struct.Join.html ==============
    (b('<p>Splits this <code>Join</code> back into its <code>AsyncRead</code> and <code>AsyncWrite</code> components.</p>'),
     c('<p>将此 <code>Join</code> 拆分为其 <code>AsyncRead</code> 和 <code>AsyncWrite</code> 组件。</p>')),
    (b('<p>Returns a reference to the inner reader.</p>'),
     c('<p>返回内部 reader 的引用。</p>')),
    (b('<p>Returns a mutable reference to the inner writer.</p>'),
     c('<p>返回内部 writer 的可变引用。</p>')),
    (b('<p>Returns a pinned mutable reference to the inner writer.</p>'),
     c('<p>返回内部 writer 的固定可变引用。</p>')),
    (b('<p>Returns a reference to the inner writer.</p>'),
     c('<p>返回内部 writer 的引用。</p>')),

    # ============== io/struct.Lines.html ==============
    (b('<p>Obtains a reference to the underlying reader.</p>'),
     c('<p>获取底层 reader 的引用。</p>')),
    (b('<p>Obtains a mutable reference to the underlying reader.</p>'),
     c('<p>获取底层 reader 的可变引用。</p>')),
    (b('<p>Returns the contents of the internal buffer as a <code>LinesStream</code>.</p>'),
     c('<p>将内部缓冲区的内容作为 <code>LinesStream</code> 返回。</p>')),

    # ============== io/struct.ReadHalf.html ==============
    (b('<p>Checks if this <code>ReadHalf</code> and some <code>WriteHalf</code> were split from the same stream.</p>'),
     c('<p>检查此 <code>ReadHalf</code> 与某个 <code>WriteHalf</code> 是否从同一个流拆分而来。</p>')),
    (b('<p>Reunites with a previously split <code>WriteHalf</code>.</p>'),
     c('<p>与之前拆分的 <code>WriteHalf</code> 重新合并。</p>')),
    (b('<p>If this <code>ReadHalf</code> and the given <code>WriteHalf</code> do not originate from the same split operation this method will panic. This can be checked ahead of time by calling <code>is_pair_of()</code>.</p>'),
     c('<p>如果此 <code>ReadHalf</code> 与给定的 <code>WriteHalf</code> 不是来自同一次拆分操作，此方法将 panic。可以事先通过调用 <code>is_pair_of()</code> 来检查。</p>')),
    (b('<p>Returns whether the readable half has been closed.</p>'),
     c('<p>返回可读一半是否已被关闭。</p>')),

    # ============== io/struct.SimplexStream.html ==============
    (b('<p>Creates unidirectional buffer that acts like in memory pipe. To create split version with separate reader and writer you can use simplex function.</p>'),
     c('<p>创建一个表现得像内存管道的单向缓冲区。若要创建带有独立 reader 和 writer 的拆分版本，可以使用 simplex 函数。</p>')),
    (b('<p>The max_buf_size argument is the maximum amount of bytes that can be written to a buffer before the it returns <code>Poll::Pending</code>.</p>'),
     c('<p><code>max_buf_size</code> 参数是缓冲区在返回 <code>Poll::Pending</code> 之前可写入的最大字节数。</p>')),
    (b('<p>Returns a reference to the read end.</p>'),
     c('<p>返回读端的引用。</p>')),
    (b('<p>Returns a reference to the write end.</p>'),
     c('<p>返回写端的引用。</p>')),
    (b('<p>Split this <code>SimplexStream</code> into separate read and write halves.</p>'),
     c('<p>将此 <code>SimplexStream</code> 拆分为独立的读半和写半。</p>')),

    # ============== io/struct.Take.html ==============
    (b('<p>Returns the remaining number of bytes that can be read before this instance will return EOF.</p>'),
     c('<p>返回此实例在返回 EOF 之前可以读取的剩余字节数。</p>')),
    (b('<p>This instance may reach EOF after reading fewer bytes than indicated by this method if the underlying <a href="../io/trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> instance reaches EOF.</p>'),
     c('<p>如果底层 <a href="../io/trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> 实例已到达 EOF，则此实例读取的字节数可能少于本方法指示的值。</p>')),
    (b('<p>Sets the number of bytes that can be read before this instance will return EOF. This is the same as constructing a new <code>Take</code> instance, so the amount of bytes read and the previous limit value don\xe2\x80\x99t matter when calling this method.</p>'),
     c('<p>设置此实例在返回 EOF 之前可以读取的字节数。这与构造一个新的 <code>Take</code> 实例相同，因此调用此方法时已读取的字节数和先前的限制值无关紧要。</p>')),
    (b('<p>Returns the limit of bytes that can be read.</p>'),
     c('<p>返回可读取的字节限制。</p>')),
    (b('<p>Sets the limit of bytes that can be read.</p>'),
     c('<p>设置可读取的字节限制。</p>')),
    (b('<p>Gets a reference to the underlying reader.</p>'),
     c('<p>获取底层 reader 的引用。</p>')),
    (b('<p>Gets a mutable reference to the underlying reader.</p>'),
     c('<p>获取底层 reader 的可变引用。</p>')),
    (b('<p>Gets a mutable reference to the underlying reader. Care should be taken to avoid modifying the internal I/O state of the underlying reader as doing so may corrupt the internal limit of this <code>Take</code>.</p>'),
     c('<p>获取底层 reader 的可变引用。需要注意避免修改底层 reader 的内部 I/O 状态，因为这样做可能会损坏此 <code>Take</code> 的内部限制。</p>')),
    (b('<p>Gets a pinned mutable reference to the underlying reader. Care should be taken to avoid modifying the internal I/O state of the underlying reader as doing so may corrupt the internal limit of this <code>Take</code>.</p>'),
     c('<p>获取底层 reader 的固定可变引用。需要注意避免修改底层 reader 的内部 I/O 状态，因为这样做可能会损坏此 <code>Take</code> 的内部限制。</p>')),
    (b('<p>Consumes the <code>Take</code>, returning the wrapped reader.</p>'),
     c('<p>消费此 <code>Take</code>，返回被包装的 reader。</p>')),

    # ============== io/struct.WriteHalf.html ==============
    (b('<p>Checks if this <code>WriteHalf</code> and some <code>ReadHalf</code> were split from the same stream.</p>'),
     c('<p>检查此 <code>WriteHalf</code> 与某个 <code>ReadHalf</code> 是否从同一个流拆分而来。</p>')),
    (b('<p>Returns whether the writeable half has been closed.</p>'),
     c('<p>返回可写一半是否已被关闭。</p>')),
]


def main():
    hits = 0
    modified = 0
    missed = []
    for dp, dirs, files in os.walk(TOKIO_ROOT):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__' and not d.endswith('_old')]
        for f in files:
            if not f.endswith('.html'):
                continue
            path = os.path.join(dp, f)
            with open(path, 'rb') as fh:
                raw = fh.read()
            new = raw
            local_hits = 0
            for old, zn in PAIRS:
                if old in new:
                    new = new.replace(old, zn)
                    local_hits += new.count(zn) - raw.count(zn)
            if new != raw:
                with open(path, 'wb') as fh:
                    fh.write(new)
                modified += 1
                hits += local_hits

    # Check missed pairs
    for old, _ in PAIRS:
        found = False
        for dp, dirs, files in os.walk(TOKIO_ROOT):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__' and not d.endswith('_old')]
            for f in files:
                if not f.endswith('.html'):
                    continue
                with open(os.path.join(dp, f), 'rb') as fh:
                    if old in fh.read():
                        found = True
                        break
            if found:
                break
        if not found:
            missed.append(old[:80].decode('utf-8', errors='replace'))

    print(f'Modified files: {modified}')
    print(f'Total replacements applied: {hits}')
    print(f'Missed pairs: {len(missed)}')
    for m in missed[:10]:
        print(f'  {m!r}')


if __name__ == '__main__':
    main()