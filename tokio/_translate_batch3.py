"""Batch 3: translate remaining AsyncReadExt/AsyncWriteExt method docs + bufstream/simplex/take."""
import os, re

TOKIO_ROOT = 'D:/Administrator/Documents/Code/rust_doc_all/tokio'

# (regex_pattern_bytes_or_str, replacement)
# Use bytes-level regex to allow flexible whitespace

PATTERNS = [
    # ========== io/struct.BufStream.html remaining ==========
    (re.compile(rb'<p>Wraps a type in both <code>BufWriter</code> and <code>BufReader</code>\.\s*See the documentation for those types and <code>BufStream</code> for details\.</p>'),
     '<p>将一个类型同时包装为 <code>BufWriter</code> 和 <code>BufReader</code>。详情请参见这些类型和 <code>BufStream</code> 的文档。</p>'.encode('utf-8')),
    (re.compile(rb'<p>Creates a <code>BufStream</code> with the specified <code>BufReader</code> capacity and <code>BufWriter</code> capacity\.\s*See the documentation for those types and <code>BufStream</code> for details\.</p>'),
     '<p>使用指定的 <code>BufReader</code> 容量和 <code>BufWriter</code> 容量创建一个 <code>BufStream</code>。详情请参见这些类型和 <code>BufStream</code> 的文档。</p>'.encode('utf-8')),

    # ========== io/struct.SimplexStream.html ==========
    (re.compile(rb'<p>Creates unidirectional buffer that acts like in memory pipe\.\s*To create split version with separate reader and writer you can use simplex function\.\s*The max_buf_size argument is the maximum amount of bytes that can be written to a buffer before the it returns <code>Poll::Pending</code>\.</p>'),
     '<p>创建一个表现得像内存管道的单向缓冲区。若要创建带有独立 reader 和 writer 的拆分版本，可以使用 simplex 函数。<code>max_buf_size</code> 参数是缓冲区在返回 <code>Poll::Pending</code> 之前可写入的最大字节数。</p>'.encode('utf-8')),

    # ========== io/struct.Take.html remaining ==========
    (re.compile(rb'<p>Sets the number of bytes that can be read before this instance will return EOF\.\s*This is the same as constructing a new <code>Take</code> instance, so the amount of bytes read and the previous limit value don\xe2\x80\x99t matter when calling this method\.</p>'),
     '<p>设置此实例在返回 EOF 之前可以读取的字节数。这与构造一个新的 <code>Take</code> 实例相同，因此调用此方法时已读取的字节数和先前的限制值无关紧要。</p>'.encode('utf-8')),
    (re.compile(rb'<p>Gets a pinned mutable reference to the underlying reader\.\s*Care should be taken to avoid modifying the internal I/O state of the underlying reader as doing so may corrupt the internal limit of this <code>Take</code>\.</p>'),
     '<p>获取底层 reader 的固定可变引用。需要注意避免修改底层 reader 的内部 I/O 状态，因为这样做可能会损坏此 <code>Take</code> 的内部限制。</p>'.encode('utf-8')),

    # ========== io/trait.AsyncBufReadExt.html ==========
    (re.compile(rb'<p>Reads all bytes until a newline \(the 0xA byte\) is reached, and append them to the provided buffer\.\s*</p>'),
     '<p>读取所有字节直到遇到换行符（0xA 字节），并将它们追加到提供的缓冲区中。</p>'.encode('utf-8')),
    (re.compile(rb'<p>Returns the contents of the internal buffer, filling it with more data from the inner reader if it is empty\.\s*This function is a lower-level call\.\s*It needs to be paired with the <code>consume</code> method to function properly\.\s*When calling this method, none of the contents will be [\xe2\x80\x9c"]read[\xe2\x80\x9d"] in the sense that later calls to <code>read</code> will not return the same contents\.\s*</p>'),
     '<p>返回内部缓冲区的内容，如果为空则从内部 reader 填充更多数据。此函数是一个较低级别的调用。它需要与 <code>consume</code> 方法配合使用才能正常工作。调用此方法时，内容不会被"读取"，因为后续对 <code>read</code> 的调用不会返回相同的内容。</p>'.encode('utf-8')),
    (re.compile(rb'<p>Tells this buffer that <code>amt</code> bytes have been consumed from the buffer, so they should no longer be returned in calls to <code>read</code>\.\s*This function is a lower-level call\.\s*It needs to be paired with the <code>fill_buf</code> method to function properly\.\s*This function does not perform any I/O, it simply informs this object that some data has been consumed\.\s*</p>'),
     '<p>告知此缓冲区 <code>amt</code> 字节已从缓冲区消费，因此在后续 <code>read</code> 调用中不应再返回这些字节。此函数是一个较低级别的调用。它需要与 <code>fill_buf</code> 方法配合使用才能正常工作。此函数不执行任何 I/O，只是通知此对象某些数据已被消费。</p>'.encode('utf-8')),

    # ========== io/trait.AsyncReadExt.html - read family ==========
    # Reads signed/unsigned integers of various widths
    (re.compile(rb'<p>Reads an unsigned (\d+)-bit integer in big-endian order from the underlying reader\.\s*</p>'),
     None),  # placeholder
    (re.compile(rb'<p>Reads an signed (\d+)-bit integer in big-endian order from the underlying reader\.\s*</p>'),
     None),
    (re.compile(rb'<p>Reads an unsigned (\d+)-bit integer in little-endian order from the underlying reader\.\s*</p>'),
     None),
    (re.compile(rb'<p>Reads a signed (\d+)-bit integer in little-endian order from the underlying reader\.\s*</p>'),
     None),
    (re.compile(rb'<p>Reads a signed (\d+)-bit integer in big-endian order from the underlying reader\.\s*</p>'),
     None),
    (re.compile(rb'<p>Reads an (\d+)-bit floating point type in big-endian order from the underlying reader\.\s*</p>'),
     None),
    (re.compile(rb'<p>Reads an (\d+)-bit floating point type in little-endian order from the underlying reader\.\s*</p>'),
     None),
    (re.compile(rb'<p>Reads an unsigned 8 bit integer from the underlying reader\.\s*</p>'),
     b'<p>\xe4\xbb\x8e\xe5\xba\x95\xe5\xb1\x82 reader \xe8\xaf\xbb\xe5\x8f\x96\xe4\xb8\x80\xe4\xb8\xaa\xe6\x97\xa0\xe7\xac\xa6\xe5\x8f\xb7 8 \xe4\xbd\x8d\xe6\x95\xb4\xe6\x95\xb0\xe3\x80\x82</p>'),
    (re.compile(rb'<p>Reads a signed 8 bit integer from the underlying reader\.\s*</p>'),
     b'<p>\xe4\xbb\x8e\xe5\xba\x95\xe5\xb1\x82 reader \xe8\xaf\xbb\xe5\x8f\x96\xe4\xb8\x80\xe4\xb8\xaa\xe6\x9c\x89\xe7\xac\xa6\xe5\x8f\xb7 8 \xe4\xbd\x8d\xe6\x95\xb4\xe6\x95\xb0\xe3\x80\x82</p>'),
    (re.compile(rb'<p>Pulls some bytes from this source into the specified buffer, returning how many bytes were read\.\s*</p>'),
     b'<p>\xe4\xbb\x8e\xe6\xad\xa4\xe6\xba\x90\xe6\x8a\xbd\xe5\x8f\x96\xe4\xb8\x80\xe4\xba\x9b\xe5\xad\x97\xe8\x8a\x82\xe5\x88\xb0\xe6\x8c\x87\xe5\xae\x9a\xe7\x9a\x84\xe7\xbc\x93\xe5\x86\xb2\xe5\x8c\xba\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e\xe8\xaf\xbb\xe5\x8f\x96\xe4\xba\x86\xe5\xa4\x9a\xe5\xb0\x91\xe5\xad\x97\xe8\x8a\x82\xe3\x80\x82</p>'),
    (re.compile(rb'<p>Pulls some bytes from this source into the specified buffer, advancing the buffer\xe2\x80\x99s internal cursor\.\s*</p>'),
     b'<p>\xe4\xbb\x8e\xe6\xad\xa4\xe6\xba\x90\xe6\x8a\xbd\xe5\x8f\x96\xe4\xb8\x80\xe4\xba\x9b\xe5\xad\x97\xe8\x8a\x82\xe5\x88\xb0\xe6\x8c\x87\xe5\xae\x9a\xe7\x9a\x84\xe7\xbc\x93\xe5\x86\xb2\xe5\x8c\xba\xef\xbc\x8c\xe5\xb9\xb6\xe5\x89\x8d\xe8\xbf\x9b\xe7\xbc\x93\xe5\x86\xb2\xe5\x8c\xba\xe7\x9a\x84\xe5\x86\x85\xe9\x83\xa8\xe6\x9c\x88\xe6\xa0\x87\xe3\x80\x82</p>'),
    (re.compile(rb'<p>Reads the exact number of bytes required to fill <code>buf</code>\.\s*</p>'),
     b'<p>\xe8\xaf\xbb\xe5\x8f\x96\xe5\x85\x85\xe6\xbb\xa1 <code>buf</code> \xe6\x89\x80\xe9\x9c\x80\xe7\x9a\x84\xe5\xad\x97\xe8\x8a\x82\xe6\x95\xb0\xe3\x80\x82</p>'),

    # ========== io/trait.AsyncSeekExt.html ==========
    (re.compile(rb'<p>Seeks to an offset, in bytes, in a stream\.\s*</p>'),
     b'<p>\xe5\x9c\xa8\xe6\xb5\x81\xe4\xb8\xad\xe5\xaf\xbb\xe6\x89\xbe\xe5\x88\xb0\xe6\x8c\x87\xe5\xae\x9a\xe7\x9a\x84\xe5\xad\x97\xe8\x8a\x82\xe5\x81\x8f\xe7\xa7\xbb\xe9\x87\x8f\xe3\x80\x82</p>'),

    # ========== io/trait.AsyncWriteExt.html ==========
    (re.compile(rb'<p>Writes a buffer into this writer, returning how many bytes were written\.\s*</p>'),
     b'<p>\xe5\xb0\x86\xe7\xbc\x93\xe5\x86\xb2\xe5\x8c\xba\xe5\x86\x99\xe5\x85\xa5\xe6\xad\xa4 writer\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e\xe5\x86\x99\xe5\x85\xa5\xe4\xba\x86\xe5\xa4\x9a\xe5\xb0\x91\xe5\xad\x97\xe8\x8a\x82\xe3\x80\x82</p>'),
    (re.compile(rb'<p>Attempts to write an entire buffer into this writer\.\s*</p>'),
     b'<p>\xe5\xb0\x9d\xe8\xaf\x95\xe5\xb0\x86\xe6\x95\xb4\xe4\xb8\xaa\xe7\xbc\x93\xe5\x86\xb2\xe5\x8c\xba\xe5\x86\x99\xe5\x85\xa5\xe6\xad\xa4 writer\xe3\x80\x82</p>'),
    (re.compile(rb'<p>Flushes this output stream, ensuring all intermediately buffered contents reach their destination\.\s*</p>'),
     b'<p>\xe5\x88\xb7\xe6\x96\xb0\xe6\xad\xa4\xe8\xbe\x93\xe5\x87\xba\xe6\xb5\x81\xef\xbc\x8c\xe7\xa1\xae\xe4\xbf\x9d\xe6\x89\x80\xe6\x9c\x89\xe5\x9c\xa8\xe4\xb8\xad\xe9\x97\xb4\xe7\xbc\x93\xe5\x86\xb2\xe7\x9a\x84\xe5\x86\x85\xe5\xae\xb9\xe9\x83\xbd\xe5\x88\xb0\xe8\xbe\xbe\xe7\x9b\xae\xe7\x9a\x84\xe5\x9c\xb0\xe3\x80\x82</p>'),
    (re.compile(rb'<p>Writes an unsigned (\d+)-bit integer in big-endian order to the underlying writer\.\s*</p>'),
     None),
    (re.compile(rb'<p>Writes a signed (\d+)-bit integer in big-endian order to the underlying writer\.\s*</p>'),
     None),
    (re.compile(rb'<p>Writes an unsigned (\d+)-bit integer in little-endian order to the underlying writer\.\s*</p>'),
     None),
    (re.compile(rb'<p>Writes a signed (\d+)-bit integer in little-endian order to the underlying writer\.\s*</p>'),
     None),
    (re.compile(rb'<p>Writes a (\d+)-bit floating point type in big-endian order to the underlying writer\.\s*</p>'),
     None),
    (re.compile(rb'<p>Writes a (\d+)-bit floating point type in little-endian order to the underlying writer\.\s*</p>'),
     None),
    (re.compile(rb'<p>Writes an unsigned 8 bit integer to the underlying writer\.\s*</p>'),
     b'<p>\xe5\xb0\x86\xe4\xb8\x80\xe4\xb8\xaa\xe6\x97\xa0\xe7\xac\xa6\xe5\x8f\xb7 8 \xe4\xbd\x8d\xe6\x95\xb4\xe6\x95\xb0\xe5\x86\x99\xe5\x85\xa5\xe5\xba\x95\xe5\xb1\x82 writer\xe3\x80\x82</p>'),
    (re.compile(rb'<p>Writes a signed 8 bit integer to the underlying writer\.\s*</p>'),
     b'<p>\xe5\xb0\x86\xe4\xb8\x80\xe4\xb8\xaa\xe6\x9c\x89\xe7\xac\xa6\xe5\x8f\xb7 8 \xe4\xbd\x8d\xe6\x95\xb4\xe6\x95\xb0\xe5\x86\x99\xe5\x85\xa5\xe5\xba\x95\xe5\xb1\x82 writer\xe3\x80\x82</p>'),
]


def translate_int_pattern(m):
    """Translate 'Reads an unsigned N-bit integer in BE order' patterns."""
    s = m.group(0).decode('utf-8')
    n = m.group(1).decode('utf-8')
    # Original: "Reads an unsigned N-bit integer in big-endian order from the underlying reader."
    s_zh = f'<p>以大端字节序从底层 reader 读取一个无符号 {n} 位整数。</p>'
    return s_zh.encode('utf-8')


def translate_signed_int_pattern(m):
    s = m.group(0).decode('utf-8')
    n = m.group(1).decode('utf-8')
    s_zh = f'<p>以大端字节序从底层 reader 读取一个有符号 {n} 位整数。</p>'
    return s_zh.encode('utf-8')


def translate_le_unsigned_int_pattern(m):
    s = m.group(0).decode('utf-8')
    n = m.group(1).decode('utf-8')
    s_zh = f'<p>以小端字节序从底层 reader 读取一个无符号 {n} 位整数。</p>'
    return s_zh.encode('utf-8')


def translate_le_signed_int_pattern(m):
    s = m.group(0).decode('utf-8')
    n = m.group(1).decode('utf-8')
    s_zh = f'<p>以小端字节序从底层 reader 读取一个有符号 {n} 位整数。</p>'
    return s_zh.encode('utf-8')


def translate_float_pattern(m):
    s = m.group(0).decode('utf-8')
    n = m.group(1).decode('utf-8')
    s_zh = f'<p>以大端字节序从底层 reader 读取一个 {n} 位浮点数。</p>'
    return s_zh.encode('utf-8')


def translate_float_le_pattern(m):
    s = m.group(0).decode('utf-8')
    n = m.group(1).decode('utf-8')
    s_zh = f'<p>以小端字节序从底层 reader 读取一个 {n} 位浮点数。</p>'
    return s_zh.encode('utf-8')


def translate_write_int_be(m):
    n = m.group(1).decode('utf-8')
    return f'<p>以大端字节序将一个无符号 {n} 位整数写入底层 writer。</p>'.encode('utf-8')


def translate_write_int_be_signed(m):
    n = m.group(1).decode('utf-8')
    return f'<p>以大端字节序将一个有符号 {n} 位整数写入底层 writer。</p>'.encode('utf-8')


def translate_write_int_le(m):
    n = m.group(1).decode('utf-8')
    return f'<p>以小端字节序将一个无符号 {n} 位整数写入底层 writer。</p>'.encode('utf-8')


def translate_write_int_le_signed(m):
    n = m.group(1).decode('utf-8')
    return f'<p>以小端字节序将一个有符号 {n} 位整数写入底层 writer。</p>'.encode('utf-8')


def translate_write_float_be(m):
    n = m.group(1).decode('utf-8')
    return f'<p>以大端字节序将一个 {n} 位浮点数写入底层 writer。</p>'.encode('utf-8')


def translate_write_float_le(m):
    n = m.group(1).decode('utf-8')
    return f'<p>以小端字节序将一个 {n} 位浮点数写入底层 writer。</p>'.encode('utf-8')


# Mapping of patterns to their handlers
HANDLERS = {
    'Reads an unsigned (\\d+)-bit integer in big-endian order from the underlying reader\\.\\s*': translate_int_pattern,
    'Reads an signed (\\d+)-bit integer in big-endian order from the underlying reader\\.\\s*': translate_signed_int_pattern,
    'Reads an unsigned (\\d+)-bit integer in little-endian order from the underlying reader\\.\\s*': translate_le_unsigned_int_pattern,
    'Reads a signed (\\d+)-bit integer in little-endian order from the underlying reader\\.\\s*': translate_le_signed_int_pattern,
    'Reads a signed (\\d+)-bit integer in big-endian order from the underlying reader\\.\\s*': translate_signed_int_pattern,
    'Reads an (\\d+)-bit floating point type in big-endian order from the underlying reader\\.\\s*': translate_float_pattern,
    'Reads an (\\d+)-bit floating point type in little-endian order from the underlying reader\\.\\s*': translate_float_le_pattern,
    'Writes an unsigned (\\d+)-bit integer in big-endian order to the underlying writer\\.\\s*': translate_write_int_be,
    'Writes a signed (\\d+)-bit integer in big-endian order to the underlying writer\\.\\s*': translate_write_int_be_signed,
    'Writes an unsigned (\\d+)-bit integer in little-endian order to the underlying writer\\.\\s*': translate_write_int_le,
    'Writes a signed (\\d+)-bit integer in little-endian order to the underlying writer\\.\\s*': translate_write_int_le_signed,
    'Writes a (\\d+)-bit floating point type in big-endian order to the underlying writer\\.\\s*': translate_write_float_be,
    'Writes a (\\d+)-bit floating point type in little-endian order to the underlying writer\\.\\s*': translate_write_float_le,
}


def main():
    # Build final pattern list with handlers
    final_patterns = []  # (compiled_regex, replacement_or_handler)
    for pat, repl in PATTERNS:
        # Get the pattern's source string
        if pat.pattern.startswith(b'<p>Reads an unsigned'):
            handler = HANDLERS.get('Reads an unsigned (\\d+)-bit integer in big-endian order from the underlying reader\\.\\s*')
            final_patterns.append((pat, ('handler', handler)))
        elif pat.pattern.startswith(b'<p>Reads an signed'):
            handler = HANDLERS.get('Reads an signed (\\d+)-bit integer in big-endian order from the underlying reader\\.\\s*')
            final_patterns.append((pat, ('handler', handler)))
        elif pat.pattern.startswith(b'<p>Reads an unsigned') and b'little-endian' in pat.pattern:
            handler = HANDLERS.get('Reads an unsigned (\\d+)-bit integer in little-endian order from the underlying reader\\.\\s*')
            final_patterns.append((pat, ('handler', handler)))
        elif pat.pattern.startswith(b'<p>Reads a signed') and b'little-endian' in pat.pattern:
            handler = HANDLERS.get('Reads a signed (\\d+)-bit integer in little-endian order from the underlying reader\\.\\s*')
            final_patterns.append((pat, ('handler', handler)))
        elif pat.pattern.startswith(b'<p>Reads a signed') and b'big-endian' in pat.pattern:
            handler = HANDLERS.get('Reads a signed (\\d+)-bit integer in big-endian order from the underlying reader\\.\\s*')
            final_patterns.append((pat, ('handler', handler)))
        elif pat.pattern.startswith(b'<p>Reads an ') and b'floating' in pat.pattern and b'big-endian' in pat.pattern:
            handler = HANDLERS.get('Reads an (\\d+)-bit floating point type in big-endian order from the underlying reader\\.\\s*')
            final_patterns.append((pat, ('handler', handler)))
        elif pat.pattern.startswith(b'<p>Reads an ') and b'floating' in pat.pattern and b'little-endian' in pat.pattern:
            handler = HANDLERS.get('Reads an (\\d+)-bit floating point type in little-endian order from the underlying reader\\.\\s*')
            final_patterns.append((pat, ('handler', handler)))
        elif pat.pattern.startswith(b'<p>Writes an unsigned') and b'big-endian' in pat.pattern:
            handler = HANDLERS.get('Writes an unsigned (\\d+)-bit integer in big-endian order to the underlying writer\\.\\s*')
            final_patterns.append((pat, ('handler', handler)))
        elif pat.pattern.startswith(b'<p>Writes a signed') and b'big-endian' in pat.pattern:
            handler = HANDLERS.get('Writes a signed (\\d+)-bit integer in big-endian order to the underlying writer\\.\\s*')
            final_patterns.append((pat, ('handler', handler)))
        elif pat.pattern.startswith(b'<p>Writes an unsigned') and b'little-endian' in pat.pattern:
            handler = HANDLERS.get('Writes an unsigned (\\d+)-bit integer in little-endian order to the underlying writer\\.\\s*')
            final_patterns.append((pat, ('handler', handler)))
        elif pat.pattern.startswith(b'<p>Writes a signed') and b'little-endian' in pat.pattern:
            handler = HANDLERS.get('Writes a signed (\\d+)-bit integer in little-endian order to the underlying writer\\.\\s*')
            final_patterns.append((pat, ('handler', handler)))
        elif pat.pattern.startswith(b'<p>Writes a ') and b'floating' in pat.pattern and b'big-endian' in pat.pattern:
            handler = HANDLERS.get('Writes a (\\d+)-bit floating point type in big-endian order to the underlying writer\\.\\s*')
            final_patterns.append((pat, ('handler', handler)))
        elif pat.pattern.startswith(b'<p>Writes a ') and b'floating' in pat.pattern and b'little-endian' in pat.pattern:
            handler = HANDLERS.get('Writes a (\\d+)-bit floating point type in little-endian order to the underlying writer\\.\\s*')
            final_patterns.append((pat, ('handler', handler)))
        elif repl is None:
            print(f"WARNING: no repl for {pat.pattern[:60]!r}")
        else:
            final_patterns.append((pat, ('text', repl)))

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
            for pat, (kind, val) in final_patterns:
                if kind == 'handler':
                    count_before = len(pat.findall(new))
                    if count_before > 0:
                        new = pat.sub(val, new)
                        local_hits += count_before
                else:
                    count_before = len(pat.findall(new))
                    if count_before > 0:
                        new = pat.sub(val, new)
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