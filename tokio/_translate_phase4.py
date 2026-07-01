#!/usr/bin/env python3
"""tokio 第四阶段：翻译 AsyncReadExt / AsyncWriteExt / AsyncBufReadExt / AsyncSeekExt
四个 trait extension 文件中的方法描述。每个方法的描述都以一段简短英文 + "Equivalent to:" 形式存在。

策略：直接对每个方法的描述开头几句做 replace（保留 "Equivalent to:" 后面的代码块）。
"""
import os

BASE = r'D:/Administrator/Documents/Code/rust_doc_all/tokio'

# AsyncReadExt methods - 简单方法描述
READ_EXT = [
    # chain
    (b'Creates a new <code>AsyncRead</code> instance that chains this stream with another.',
     b'Creates a new <a href="trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> instance that chains this stream with another.'),
    # All other AsyncReadExt methods use the same pattern: "Pulls/Reads/...", " Equivalent to:"
]

# Translation table for AsyncReadExt method names -> description
READ_METHOD_DESC = {
    'chain': ('Creates a new <code>AsyncRead</code> instance that chains this stream with\nanother.\nThe returned <code>AsyncRead</code> instance will first read all bytes from this object\nuntil EOF is encountered. Afterwards the output is equivalent to the\noutput of <code>next</code>.',
              '创建一个新的 <code>AsyncRead</code> 实例，将此流与另一个流链接起来。\n返回的 <code>AsyncRead</code> 实例将首先从此对象读取所有字节直到 EOF。之后的输出等同于 <code>next</code> 的输出。'),
    'read': ('Pulls some bytes from this source into the specified buffer,\nreturning how many bytes were read.',
             '从此源拉取一些字节到指定的缓冲中，返回读取的字节数。'),
    'read_buf': ('Pulls some bytes from this source into the specified buffer,\nadvancing the buffer’s internal cursor.',
                 '从此源拉取一些字节到指定的缓冲中，前进缓冲的内部游标。'),
    'read_exact': ('Reads the exact number of bytes required to fill <code>buf</code>.',
                   '读取填充 <code>buf</code> 所需的精确字节数。'),
    'read_u8': ('Reads an unsigned 8 bit integer from the underlying reader.',
                '从底层读取器读取一个无符号 8 位整数。'),
    'read_i8': ('Reads a signed 8 bit integer from the underlying reader.',
                '从底层读取器读取一个有符号 8 位整数。'),
    'read_u16': ('Reads an unsigned 16-bit integer in big-endian order from the\nunderlying reader.',
                 '从底层读取器以大端顺序读取一个无符号 16 位整数。'),
    'read_i16': ('Reads a signed 16-bit integer in big-endian order from the\nunderlying reader.',
                 '从底层读取器以大端顺序读取一个有符号 16 位整数。'),
    'read_u32': ('Reads an unsigned 32-bit integer in big-endian order from the\nunderlying reader.',
                 '从底层读取器以大端顺序读取一个无符号 32 位整数。'),
    'read_i32': ('Reads a signed 32-bit integer in big-endian order from the\nunderlying reader.',
                 '从底层读取器以大端顺序读取一个有符号 32 位整数。'),
    'read_u64': ('Reads an unsigned 64-bit integer in big-endian order from the\nunderlying reader.',
                 '从底层读取器以大端顺序读取一个无符号 64 位整数。'),
    'read_i64': ('Reads an signed 64-bit integer in big-endian order from the\nunderlying reader.',
                 '从底层读取器以大端顺序读取一个有符号 64 位整数。'),
    'read_u128': ('Reads an unsigned 128-bit integer in big-endian order from the\nunderlying reader.',
                  '从底层读取器以大端顺序读取一个无符号 128 位整数。'),
    'read_i128': ('Reads an signed 128-bit integer in big-endian order from the\nunderlying reader.',
                  '从底层读取器以大端顺序读取一个有符号 128 位整数。'),
    'read_f32': ('Reads an 32-bit floating point type in big-endian order from the\nunderlying reader.',
                 '从底层读取器以大端顺序读取一个 32 位浮点类型。'),
    'read_f64': ('Reads an 64-bit floating point type in big-endian order from the\nunderlying reader.',
                 '从底层读取器以大端顺序读取一个 64 位浮点类型。'),
    'read_u16_le': ('Reads an unsigned 16-bit integer in little-endian order from the\nunderlying reader.',
                    '从底层读取器以小端顺序读取一个无符号 16 位整数。'),
    'read_i16_le': ('Reads a signed 16-bit integer in little-endian order from the\nunderlying reader.',
                    '从底层读取器以小端顺序读取一个有符号 16 位整数。'),
    'read_u32_le': ('Reads an unsigned 32-bit integer in little-endian order from the\nunderlying reader.',
                    '从底层读取器以小端顺序读取一个无符号 32 位整数。'),
    'read_i32_le': ('Reads a signed 32-bit integer in little-endian order from the\nunderlying reader.',
                    '从底层读取器以小端顺序读取一个有符号 32 位整数。'),
    'read_u64_le': ('Reads an unsigned 64-bit integer in little-endian order from the\nunderlying reader.',
                    '从底层读取器以小端顺序读取一个无符号 64 位整数。'),
    'read_i64_le': ('Reads an signed 64-bit integer in little-endian order from the\nunderlying reader.',
                    '从底层读取器以小端顺序读取一个有符号 64 位整数。'),
    'read_u128_le': ('Reads an unsigned 128-bit integer in little-endian order from the\nunderlying reader.',
                     '从底层读取器以小端顺序读取一个无符号 128 位整数。'),
    'read_i128_le': ('Reads an signed 128-bit integer in little-endian order from the\nunderlying reader.',
                     '从底层读取器以小端顺序读取一个有符号 128 位整数。'),
    'read_f32_le': ('Reads an 32-bit floating point type in little-endian order from the\nunderlying reader.',
                    '从底层读取器以小端顺序读取一个 32 位浮点类型。'),
    'read_f64_le': ('Reads an 64-bit floating point type in little-endian order from the\nunderlying reader.',
                    '从底层读取器以小端顺序读取一个 64 位浮点类型。'),
    'read_to_end': ('Reads all bytes until EOF in this source, placing them into <code>buf</code>.',
                    '从此源读取所有字节直到 EOF，将它们放入 <code>buf</code>。'),
    'read_to_string': ('Reads all bytes until EOF in this source, appending them to <code>buf</code>.',
                       '从此源读取所有字节直到 EOF，将它们追加到 <code>buf</code>。'),
    'take': ('Creates an adaptor which reads at most <code>limit</code> bytes from it.\nThis function returns a new instance of <code>AsyncRead</code> which will read\nat most <code>limit</code> bytes, after which it will always return EOF\n(<code>Ok(0)</code>). Any read errors will not count towards the number of\nbytes read and future calls to <code>read()</code> may succeed.',
             '创建一个适配器，从其中最多读取 <code>limit</code> 个字节。\n此函数返回 <code>AsyncRead</code> 的一个新实例，最多读取 <code>limit</code> 个字节，之后将始终返回 EOF（<code>Ok(0)</code>）。任何读取错误将不计入已读取字节数，且对 <code>read()</code> 的后续调用仍可能成功。'),
}

WRITE_METHOD_DESC = {
    'write': ('Writes a buffer into this writer, returning how many bytes were\nwritten.',
              '将一个缓冲写入此写入器，返回写入的字节数。'),
    'write_vectored': ('Like <code>write</code>, except that it writes from a slice of buffers.',
                       '与 <code>write</code> 类似，但从一个缓冲切片中写入。'),
    'write_buf': ('Writes a buffer into this writer, advancing the buffer’s internal\ncursor.',
                  '将一个缓冲写入此写入器，前进缓冲的内部游标。'),
    'write_all_buf': ('Attempts to write an entire buffer into this writer.',
                      '尝试将整个缓冲写入此写入器。'),
    'flush': ('Flushes this output stream, ensuring that all intermediately buffered\ncontents reach their destination.',
              '刷新此输出流，确保所有中间缓冲的内容到达目的地。'),
    'shutdown': ('Shuts down the output stream, ensuring that the value can be dropped\ncleanly.',
                 '关闭输出流，确保此值能被干净地丢弃。'),
    'write_all': ('Writes an entire buffer into this writer.',
                  '将整个缓冲写入此写入器。'),
    'write_u8': ('Writes an unsigned 8-bit integer to the underlying writer.',
                 '向底层写入器写入一个无符号 8 位整数。'),
    'write_i8': ('Writes a signed 8-bit integer to the underlying writer.',
                 '向底层写入器写入一个有符号 8 位整数。'),
    'write_u16': ('Writes an unsigned 16-bit integer in big-endian order to the\nunderlying writer.',
                  '向底层写入器以大端顺序写入一个无符号 16 位整数。'),
    'write_i16': ('Writes a signed 16-bit integer in big-endian order to the\nunderlying writer.',
                  '向底层写入器以大端顺序写入一个有符号 16 位整数。'),
    'write_u32': ('Writes an unsigned 32-bit integer in big-endian order to the\nunderlying writer.',
                  '向底层写入器以大端顺序写入一个无符号 32 位整数。'),
    'write_i32': ('Writes a signed 32-bit integer in big-endian order to the\nunderlying writer.',
                  '向底层写入器以大端顺序写入一个有符号 32 位整数。'),
    'write_u64': ('Writes an unsigned 64-bit integer in big-endian order to the\nunderlying writer.',
                  '向底层写入器以大端顺序写入一个无符号 64 位整数。'),
    'write_i64': ('Writes a signed 64-bit integer in big-endian order to the\nunderlying writer.',
                  '向底层写入器以大端顺序写入一个有符号 64 位整数。'),
    'write_u128': ('Writes an unsigned 128-bit integer in big-endian order to the\nunderlying writer.',
                   '向底层写入器以大端顺序写入一个无符号 128 位整数。'),
    'write_i128': ('Writes an signed 128-bit integer in big-endian order to the\nunderlying writer.',
                   '向底层写入器以大端顺序写入一个有符号 128 位整数。'),
    'write_f32': ('Writes an 32-bit floating point type in big-endian order to the\nunderlying writer.',
                  '向底层写入器以大端顺序写入一个 32 位浮点类型。'),
    'write_f64': ('Writes an 64-bit floating point type in big-endian order to the\nunderlying writer.',
                  '向底层写入器以大端顺序写入一个 64 位浮点类型。'),
    'write_u16_le': ('Writes an unsigned 16-bit integer in little-endian order to the\nunderlying writer.',
                     '向底层写入器以小端顺序写入一个无符号 16 位整数。'),
    'write_i16_le': ('Writes a signed 16-bit integer in little-endian order to the\nunderlying writer.',
                     '向底层写入器以小端顺序写入一个有符号 16 位整数。'),
    'write_u32_le': ('Writes an unsigned 32-bit integer in little-endian order to the\nunderlying writer.',
                     '向底层写入器以小端顺序写入一个无符号 32 位整数。'),
    'write_i32_le': ('Writes a signed 32-bit integer in little-endian order to the\nunderlying writer.',
                     '向底层写入器以小端顺序写入一个有符号 32 位整数。'),
    'write_u64_le': ('Writes an unsigned 64-bit integer in little-endian order to the\nunderlying writer.',
                     '向底层写入器以小端顺序写入一个无符号 64 位整数。'),
    'write_i64_le': ('Writes an signed 64-bit integer in little-endian order to the\nunderlying writer.',
                     '向底层写入器以小端顺序写入一个有符号 64 位整数。'),
    'write_u128_le': ('Writes an unsigned 128-bit integer in little-endian order to the\nunderlying writer.',
                      '向底层写入器以小端顺序写入一个无符号 128 位整数。'),
    'write_i128_le': ('Writes an signed 128-bit integer in little-endian order to the\nunderlying writer.',
                      '向底层写入器以小端顺序写入一个有符号 128 位整数。'),
    'write_f32_le': ('Writes an 32-bit floating point type in little-endian order to the\nunderlying writer.',
                     '向底层写入器以小端顺序写入一个 32 位浮点类型。'),
    'write_f64_le': ('Writes an 64-bit floating point type in little-endian order to the\nunderlying writer.',
                     '向底层写入器以小端顺序写入一个 64 位浮点类型。'),
}

BUFREAD_METHOD_DESC = {
    'fill_buf': ('Returns the contents of the internal buffer, filling it with more\ndata from the inner reader if it is empty.',
                 '返回内部缓冲的内容，如果内部缓冲为空，则从内部读取器读取更多数据填充。'),
    'consume': ('Tells this buffer that <code>amt</code> bytes have been consumed from the\nbuffer, so they should no longer be returned in calls to <code>read</code>.',
                '通知此缓冲已有 <code>amt</code> 个字节被消费，这些字节不应再在 <code>read</code> 调用中返回。'),
    'read_until': ('Reads all bytes into <code>buf</code> until the delimiter byte or EOF is\nreached.',
                   '读取所有字节到 <code>buf</code>，直到遇到分隔字节或 EOF。'),
    'read_line': ('Reads all bytes until a newline (the 0xA byte) is reached, and append\nthem to the provided <code>String</code> buffer.',
                  '读取所有字节直到遇到换行符（0xA 字节），并将它们追加到提供的 <code>String</code> 缓冲。'),
    'lines': ('Returns a stream of the lines of this reader.',
              '返回此读取器的行流。'),
    'split': ('Returns a stream of the lines of this reader.',
              '返回此读取器的行流。'),
}

SEEK_METHOD_DESC = {
    'seek': ('Creates a future which will seek an IO object, and then yield the\nnew position in the object and the object itself.',
             '创建一个将定位 IO 对象，然后产出对象中的新位置以及对象本身的 Future。'),
    'rewind': ('Creates a future which will rewind to the beginning of the stream.',
               '创建一个将倒回到流开头的 Future。'),
    'stream_position': ('Creates a future which will return the current seek position from the\nunderlying object.',
                        '创建一个 Future，返回底层对象的当前定位位置。'),
}


def translate_trait_file(filename, method_desc_dict):
    """Translate one trait extension file by replacing each method's entire docblock text."""
    p = os.path.join(BASE, filename)
    with open(p, 'rb') as f:
        c = f.read()

    original = c
    local = 0

    for method, (en, zh) in method_desc_dict.items():
        # The source uses these characters:
        # - ` (U+2019) right single quote for buffer's
        # - `\n` for line breaks (with CRLF in source)
        en_b = en.encode('utf-8')
        zh_b = zh.encode('utf-8')

        # Try LF version
        if en_b in c:
            c = c.replace(en_b, zh_b)
            local += 1
        # Try CRLF version
        en_crlf = en_b.replace(b'\n', b'\r\n')
        zh_crlf = zh_b.replace(b'\n', b'\r\n')
        if en_crlf != en_b and en_crlf in c:
            c = c.replace(en_crlf, zh_crlf)
            local += 1

    if c != original:
        with open(p, 'wb') as f:
            f.write(c)
        print(f'{filename}: {local} replacements')
    else:
        print(f'{filename}: 0 replacements (no match)')


def main():
    translate_trait_file('io/trait.AsyncReadExt.html', READ_METHOD_DESC)
    translate_trait_file('io/trait.AsyncWriteExt.html', WRITE_METHOD_DESC)
    translate_trait_file('io/trait.AsyncBufReadExt.html', BUFREAD_METHOD_DESC)
    translate_trait_file('io/trait.AsyncSeekExt.html', SEEK_METHOD_DESC)


if __name__ == '__main__':
    main()