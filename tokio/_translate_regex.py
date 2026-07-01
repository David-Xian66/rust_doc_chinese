"""Translation using regex-based flexible whitespace matching.

rustdoc wraps long lines at ~80 chars, so exact byte matching fails.
Use re.sub with \s+ allowing flexible whitespace.
"""
import os, re, sys

TOKIO_ROOT = 'D:/Administrator/Documents/Code/rust_doc_all/tokio'

def rb(en_text):
    """Compile regex pattern from EN text, treating whitespace flexibly."""
    # Escape HTML special chars, but replace \n / spaces with \s+
    escaped = re.escape(en_text)
    # Allow flexible whitespace
    escaped = escaped.replace(r'\ ', r'\s+')
    escaped = escaped.replace(r'\n', r'\s+')
    # The \s+ above already absorbs \r\n, \n, etc.
    return re.compile(escaped.encode('utf-8') if isinstance(escaped, str) else escaped, re.DOTALL)

# (en_pattern, zh_replacement)
PAIRS = [
    # fs/struct.File.html
    (rb('<p>Get the maximum buffer size for the underlying <a href="../io/trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> / <a href="../io/trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> operation.</p>'),
     '<p>获取底层 <a href="../io/trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> / <a href="../io/trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> 操作的最大缓冲区大小。</p>'),

    # io/struct.BufReader.html
    (rb('<p>Creates a new <code>BufReader</code> with a default buffer capacity. The default is currently 8 KB, but may change in the future.</p>'),
     '<p>使用默认缓冲区容量创建一个新的 <code>BufReader</code>。默认容量目前为 8 KB，未来可能会更改。</p>'),
    (rb('<p>Creates a new <code>BufReader</code> with the specified buffer capacity.</p>'),
     '<p>使用指定的缓冲区容量创建一个新的 <code>BufReader</code>。</p>'),
    (rb('<p>Gets a reference to the underlying reader. It is inadvisable to directly read from the underlying reader.</p>'),
     '<p>获取底层 reader 的引用。不建议直接从底层 reader 读取。</p>'),
    (rb('<p>Gets a mutable reference to the underlying reader. It is inadvisable to directly read from the underlying reader.</p>'),
     '<p>获取底层 reader 的可变引用。不建议直接从底层 reader 读取。</p>'),
    (rb('<p>Gets a pinned mutable reference to the underlying reader. It is inadvisable to directly read from the underlying reader.</p>'),
     '<p>获取底层 reader 的固定可变引用。不建议直接从底层 reader 读取。</p>'),
    (rb('<p>Consumes this <code>BufReader</code>, returning the underlying reader. Note that any leftover data in the internal buffer is lost.</p>'),
     '<p>消费此 <code>BufReader</code>，返回底层 reader。请注意，内部缓冲区中的任何剩余数据都会丢失。</p>'),
    (rb('<p>Returns a reference to the internally buffered data. Unlike <code>fill_buf</code>, this will not attempt to fill the buffer if it is empty.</p>'),
     '<p>返回内部缓冲数据的引用。与 <code>fill_buf</code> 不同，如果缓冲区为空，它不会尝试填充缓冲区。</p>'),
    (rb('<p>Returns a mutable reference to the internally buffered data.</p>'),
     '<p>返回内部缓冲数据的可变引用。</p>'),
    (rb('<p>Returns a pinned mutable reference to the internally buffered data.</p>'),
     '<p>返回内部缓冲数据的固定可变引用。</p>'),
    (rb('<p>Read bytes from this <code>BufReader</code> into the provided buffer.</p>'),
     '<p>从此 <code>BufReader</code> 读取字节到提供的缓冲区中。</p>'),
    (rb('<p>Write bytes from the provided buffer into this <code>BufReader</code>.</p>'),
     '<p>从提供的缓冲区写入字节到此 <code>BufReader</code>。</p>'),

    # io/struct.BufStream.html
    (rb('<p>Wraps a type in both <code>BufWriter</code> and <code>BufReader</code>. See the documentation for those types and <code>BufStream</code> for details.</p>'),
     '<p>将一个类型同时包装为 <code>BufWriter</code> 和 <code>BufReader</code>。详情请参见这些类型和 <code>BufStream</code> 的文档。</p>'),
    (rb('<p>Creates a <code>BufStream</code> with the specified <code>BufReader</code> capacity and <code>BufWriter</code> capacity. See the documentation for those types and <code>BufStream</code> for details.</p>'),
     '<p>使用指定的 <code>BufReader</code> 容量和 <code>BufWriter</code> 容量创建一个 <code>BufStream</code>。详情请参见这些类型和 <code>BufStream</code> 的文档。</p>'),
    (rb('<p>Gets a reference to the underlying I/O object. It is inadvisable to directly read from the underlying I/O object.</p>'),
     '<p>获取底层 I/O 对象的引用。不建议直接从底层 I/O 对象读取。</p>'),
    (rb('<p>Gets a mutable reference to the underlying I/O object. It is inadvisable to directly read from the underlying I/O object.</p>'),
     '<p>获取底层 I/O 对象的可变引用。不建议直接从底层 I/O 对象读取。</p>'),
    (rb('<p>Gets a pinned mutable reference to the underlying I/O object. It is inadvisable to directly read from the underlying I/O object.</p>'),
     '<p>获取底层 I/O 对象的固定可变引用。不建议直接从底层 I/O 对象读取。</p>'),
    (rb('<p>Consumes this <code>BufStream</code>, returning the underlying I/O object. Note that any leftover data in the internal buffer is lost.</p>'),
     '<p>消费此 <code>BufStream</code>，返回底层 I/O 对象。请注意，内部缓冲区中的任何剩余数据都会丢失。</p>'),

    # io/struct.BufWriter.html
    (rb('<p>Creates a new <code>BufWriter</code> with a default buffer capacity. The default is currently 8 KB, but may change in the future.</p>'),
     '<p>使用默认缓冲区容量创建一个新的 <code>BufWriter</code>。默认容量目前为 8 KB，未来可能会更改。</p>'),
    (rb('<p>Creates a new <code>BufWriter</code> with the specified buffer capacity.</p>'),
     '<p>使用指定的缓冲区容量创建一个新的 <code>BufWriter</code>。</p>'),
    (rb('<p>Gets a reference to the underlying writer.</p>'),
     '<p>获取底层 writer 的引用。</p>'),
    (rb('<p>Gets a mutable reference to the underlying writer. It is inadvisable to directly write to the underlying writer.</p>'),
     '<p>获取底层 writer 的可变引用。不建议直接写入底层 writer。</p>'),
    (rb('<p>Gets a pinned mutable reference to the underlying writer. It is inadvisable to directly write to the underlying writer.</p>'),
     '<p>获取底层 writer 的固定可变引用。不建议直接写入底层 writer。</p>'),
    (rb('<p>Consumes this <code>BufWriter</code>, returning the underlying writer. Note that any leftover data in the internal buffer is lost.</p>'),
     '<p>消费此 <code>BufWriter</code>，返回底层 writer。请注意，内部缓冲区中的任何剩余数据都会丢失。</p>'),
    (rb('<p>Returns a reference to the internally buffered data.</p>'),
     '<p>返回内部缓冲数据的引用。</p>'),
    (rb('<p>Read bytes from this <code>BufWriter</code> into the provided buffer.</p>'),
     '<p>从此 <code>BufWriter</code> 读取字节到提供的缓冲区中。</p>'),

    # io/struct.Chain.html
    (rb('<p>Gets references to the underlying readers in this <code>Chain</code>.</p>'),
     '<p>获取此 <code>Chain</code> 中底层 reader 的引用。</p>'),
    (rb('<p>Gets mutable references to the underlying readers in this <code>Chain</code>. Care should be taken to avoid modifying the internal I/O state of the underlying readers as doing so may corrupt the internal state of this <code>Chain</code>.</p>'),
     '<p>获取此 <code>Chain</code> 中底层 reader 的可变引用。需要注意避免修改底层 reader 的内部 I/O 状态，因为这样做可能会损坏此 <code>Chain</code> 的内部状态。</p>'),
    (rb('<p>Gets pinned mutable references to the underlying readers in this <code>Chain</code>. Care should be taken to avoid modifying the internal I/O state of the underlying readers as doing so may corrupt the internal state of this <code>Chain</code>.</p>'),
     '<p>获取此 <code>Chain</code> 中底层 reader 的固定可变引用。需要注意避免修改底层 reader 的内部 I/O 状态，因为这样做可能会损坏此 <code>Chain</code> 的内部状态。</p>'),
    (rb('<p>Consumes the <code>Chain</code>, returning the wrapped readers.</p>'),
     '<p>消费此 <code>Chain</code>，返回被包装的 reader。</p>'),

    # io/struct.Join.html
    (rb('<p>Splits this <code>Join</code> back into its <code>AsyncRead</code> and <code>AsyncWrite</code> components.</p>'),
     '<p>将此 <code>Join</code> 拆分为其 <code>AsyncRead</code> 和 <code>AsyncWrite</code> 组件。</p>'),
    (rb('<p>Returns a reference to the inner reader.</p>'),
     '<p>返回内部 reader 的引用。</p>'),
    (rb('<p>Returns a mutable reference to the inner writer.</p>'),
     '<p>返回内部 writer 的可变引用。</p>'),
    (rb('<p>Returns a pinned mutable reference to the inner writer.</p>'),
     '<p>返回内部 writer 的固定可变引用。</p>'),
    (rb('<p>Returns a reference to the inner writer.</p>'),
     '<p>返回内部 writer 的引用。</p>'),

    # io/struct.Lines.html
    (rb('<p>Obtains a reference to the underlying reader.</p>'),
     '<p>获取底层 reader 的引用。</p>'),
    (rb('<p>Obtains a mutable reference to the underlying reader.</p>'),
     '<p>获取底层 reader 的可变引用。</p>'),
    (rb('<p>Returns the contents of the internal buffer as a <code>LinesStream</code>.</p>'),
     '<p>将内部缓冲区的内容作为 <code>LinesStream</code> 返回。</p>'),

    # io/struct.ReadHalf.html
    (rb('<p>Checks if this <code>ReadHalf</code> and some <code>WriteHalf</code> were split from the same stream.</p>'),
     '<p>检查此 <code>ReadHalf</code> 与某个 <code>WriteHalf</code> 是否从同一个流拆分而来。</p>'),
    (rb('<p>Reunites with a previously split <code>WriteHalf</code>.</p>'),
     '<p>与之前拆分的 <code>WriteHalf</code> 重新合并。</p>'),
    (rb('<p>If this <code>ReadHalf</code> and the given <code>WriteHalf</code> do not originate from the same split operation this method will panic. This can be checked ahead of time by calling <code>is_pair_of()</code>.</p>'),
     '<p>如果此 <code>ReadHalf</code> 与给定的 <code>WriteHalf</code> 不是来自同一次拆分操作，此方法将 panic。可以事先通过调用 <code>is_pair_of()</code> 来检查。</p>'),
    (rb('<p>Returns whether the readable half has been closed.</p>'),
     '<p>返回可读一半是否已被关闭。</p>'),

    # io/struct.SimplexStream.html
    (rb('<p>Creates unidirectional buffer that acts like in memory pipe. To create split version with separate reader and writer you can use simplex function.</p>'),
     '<p>创建一个表现得像内存管道的单向缓冲区。若要创建带有独立 reader 和 writer 的拆分版本，可以使用 simplex 函数。</p>'),
    (rb('<p>The max_buf_size argument is the maximum amount of bytes that can be written to a buffer before the it returns <code>Poll::Pending</code>.</p>'),
     '<p><code>max_buf_size</code> 参数是缓冲区在返回 <code>Poll::Pending</code> 之前可写入的最大字节数。</p>'),
    (rb('<p>Returns a reference to the read end.</p>'),
     '<p>返回读端的引用。</p>'),
    (rb('<p>Returns a reference to the write end.</p>'),
     '<p>返回写端的引用。</p>'),
    (rb('<p>Split this <code>SimplexStream</code> into separate read and write halves.</p>'),
     '<p>将此 <code>SimplexStream</code> 拆分为独立的读半和写半。</p>'),

    # io/struct.Take.html
    (rb('<p>Returns the remaining number of bytes that can be read before this instance will return EOF.</p>'),
     '<p>返回此实例在返回 EOF 之前可以读取的剩余字节数。</p>'),
    (rb('<p>This instance may reach EOF after reading fewer bytes than indicated by this method if the underlying <a href="../io/trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> instance reaches EOF.</p>'),
     '<p>如果底层 <a href="../io/trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> 实例已到达 EOF，则此实例读取的字节数可能少于本方法指示的值。</p>'),
    (rb('<p>Sets the number of bytes that can be read before this instance will return EOF. This is the same as constructing a new <code>Take</code> instance, so the amount of bytes read and the previous limit value don\xe2\x80\x99t matter when calling this method.</p>'),
     '<p>设置此实例在返回 EOF 之前可以读取的字节数。这与构造一个新的 <code>Take</code> 实例相同，因此调用此方法时已读取的字节数和先前的限制值无关紧要。</p>'),
    (rb('<p>Returns the limit of bytes that can be read.</p>'),
     '<p>返回可读取的字节限制。</p>'),
    (rb('<p>Sets the limit of bytes that can be read.</p>'),
     '<p>设置可读取的字节限制。</p>'),
    (rb('<p>Gets a reference to the underlying reader.</p>'),
     '<p>获取底层 reader 的引用。</p>'),
    (rb('<p>Gets a mutable reference to the underlying reader.</p>'),
     '<p>获取底层 reader 的可变引用。</p>'),
    (rb('<p>Gets a mutable reference to the underlying reader. Care should be taken to avoid modifying the internal I/O state of the underlying reader as doing so may corrupt the internal limit of this <code>Take</code>.</p>'),
     '<p>获取底层 reader 的可变引用。需要注意避免修改底层 reader 的内部 I/O 状态，因为这样做可能会损坏此 <code>Take</code> 的内部限制。</p>'),
    (rb('<p>Gets a pinned mutable reference to the underlying reader. Care should be taken to avoid modifying the internal I/O state of the underlying reader as doing so may corrupt the internal limit of this <code>Take</code>.</p>'),
     '<p>获取底层 reader 的固定可变引用。需要注意避免修改底层 reader 的内部 I/O 状态，因为这样做可能会损坏此 <code>Take</code> 的内部限制。</p>'),
    (rb('<p>Consumes the <code>Take</code>, returning the wrapped reader.</p>'),
     '<p>消费此 <code>Take</code>，返回被包装的 reader。</p>'),

    # io/struct.WriteHalf.html
    (rb('<p>Checks if this <code>WriteHalf</code> and some <code>ReadHalf</code> were split from the same stream.</p>'),
     '<p>检查此 <code>WriteHalf</code> 与某个 <code>ReadHalf</code> 是否从同一个流拆分而来。</p>'),
    (rb('<p>Returns whether the writeable half has been closed.</p>'),
     '<p>返回可写一半是否已被关闭。</p>'),
]


def main():
    # Compile all patterns
    compiled = []
    for pattern, repl in PAIRS:
        compiled.append((pattern, repl))

    total_hits = 0
    modified = 0
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
            for pattern, repl in compiled:
                # Need bytes-aware substitution
                # Use re.sub with bytes pattern and string replacement
                # But pattern has special chars we want to preserve as literals
                count_before = len(pattern.findall(new))
                if count_before > 0:
                    new = pattern.sub(repl.encode('utf-8'), new)
                    local_hits += count_before
            if new != raw:
                with open(path, 'wb') as fh:
                    fh.write(new)
                modified += 1
            total_hits += local_hits

    print(f'Modified files: {modified}')
    print(f'Total replacements: {total_hits}')


if __name__ == '__main__':
    main()