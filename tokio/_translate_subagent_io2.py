"""Supplementary translation script for io/ - second pass.
Translates the remaining untranslated <p> blocks after the first script.
"""
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


# Universal patterns - apply to multiple files
# These are the "Equivalent to:", "This method is cancel safe" patterns that
# appear after every read/write method.

# Cancellation safety: short version (single line)
PAIRS = {
    'io/struct.BufStream.html': [
        (E('<p>Note that any leftover data in the internal buffer is lost.</p>'),
         E('<p>请注意内部缓冲区中的任何剩余数据都将丢失。</p>')),
    ],
    'io/struct.BufWriter.html': [
        (E('<p>Note that any leftover data in the internal buffer is lost.</p>'),
         E('<p>请注意内部缓冲区中的任何剩余数据都将丢失。</p>')),
    ],
    'io/struct.Lines.html': [
        (E('<p>This method is cancellation safe.</p>'),
         E('<p>此方法是可取消安全的。</p>')),
    ],
    'io/struct.ReadBuf.html': [
        (E('<p>Since ReadBuf tracks the region of the buffer that has been initialized, this is effectively ��free�� after\r\nthe first use.</p>'),
         E('<p>由于 ReadBuf 会跟踪缓冲区中已被初始化的区域，因此首次使用之后这实际上是��免费的��。</p>')),
        (E('<p>The number of initialized bytes is not changed.</p>'),
         E('<p>已初始化的字节数不会改变。</p>')),
    ],
    'io/struct.Split.html': [
        (E('<p>This method returns:</p>'),
         E('<p>此方法返回：</p>')),
    ],
    'io/trait.AsyncBufRead.html': [
        # Long poll_fill_buf text
        (E('<p>This function is a lower-level call. It needs to be paired with the\r\nconsume method to function properly. When calling this\r\nmethod, none of the contents will be ��read�� in the sense that later\r\ncalling <a href="trait.AsyncRead.html#tymethod.poll_read" title="method tokio::io::AsyncRead::poll_read"><code>poll_read</code></a> may return the same contents. As such, <a href="trait.AsyncBufRead.html#tymethod.consume" title="method tokio::io::AsyncBufRead::consume"><code>consume</code></a> must\r\nbe called with the number of bytes that are consumed from this buffer to\r\nensure that the bytes are never returned twice.</p>'),
         E('<p>此函数是较低级别的调用。要使其正常工作，需要与\r\nconsume 方法配对使用。调用此方法时，其中的内容不会被视为已��读����，\r\n因此随后调用 <a href="trait.AsyncRead.html#tymethod.poll_read" title="method tokio::io::AsyncRead::poll_read"><code>poll_read</code></a> 仍可能返回相同的内容。\r\n因此，必须使用从此缓冲区消费的字节数调用 <a href="trait.AsyncBufRead.html#tymethod.consume" title="method tokio::io::AsyncBufRead::consume"><code>consume</code></a>，\r\n以确保相同的字节不会被返回两次。</p>')),
    ],
    'io/trait.AsyncBufReadExt.html': [
        (E('<p>Equivalent to:</p>'),
         E('<p>等价于：</p>')),
        (E('<p>An empty buffer returned indicates that the stream has reached EOF.</p>'),
         E('<p>返回空缓冲区表示流已达到 EOF。</p>')),
        (E('<p>This method is cancel safe. If you use it as the event in a\r\ntokio::select! statement and some other branch\r\ncompletes first, then it is guaranteed that no data was read.</p>'),
         E('<p>此方法是可取消安全的。如果在 <code>tokio::select!</code> 语句中将其作为事件，\r\n而其他分支先完成，则可以保证没有数据被读取。</p>')),
        (E('<p>This method is not cancellation safe. If the method is used as the\r\nevent in a tokio::select! statement and some\r\nother branch completes first, then some data may have been partially\r\nread, and this data is lost.</p>'),
         E('<p>此方法不是可取消安全的。如果在 <code>tokio::select!</code> 语句中将其作为事件，\r\n而其他分支先完成，则可能已经部分读取了一些数据，\r\n这些数据将会丢失。</p>')),
        (E('<p>This function is a lower-level call. It needs to be paired with the\r\nconsume method to function properly. When calling this method,\r\nnone of the contents will be ��read�� in the sense that later calling\r\n<code>read</code> may return the same contents. As such, <a href="trait.AsyncBufReadExt.html#method.consume" title="method tokio::io::AsyncBufReadExt::consume"><code>consume</code></a> must be\r\ncalled with the number of bytes that are consumed from this buffer\r\nto ensure that the bytes are never returned twice.</p>'),
         E('<p>此函数是较低级别的调用。要使其正常工作，需要与\r\nconsume 方法配对使用。调用此方法时，其中的内容不会被视为已��读����，\r\n因此随后调用 <code>read</code> 仍可能返回相同的内容。\r\n因此，必须使用从此缓冲区消费的字节数调用 <a href="trait.AsyncBufReadExt.html#method.consume" title="method tokio::io::AsyncBufReadExt::consume"><code>consume</code></a>，\r\n以确保相同的字节不会被返回两次。</p>')),
    ],
    'io/trait.AsyncReadExt.html': [
        (E('<p>Equivalent to:</p>'),
         E('<p>等价于：</p>')),
        (E('<p>This method is cancel safe. If you use it as the event in a\r\ntokio::select! statement and some other branch\r\ncompletes first, then it is guaranteed that no data was read.</p>'),
         E('<p>此方法是可取消安全的。如果在 <code>tokio::select!</code> 语句中将其作为事件，\r\n而其他分支先完成，则可以保证没有数据被读取。</p>')),
        (E('<p>If the operation encounters an ��end of file�� before completely\r\nfilling the buffer, it returns an error of the kind\r\nErrorKind::UnexpectedEof. The contents of buf are unspecified\r\nin this case.</p>'),
         E('<p>如果在完全填满缓冲区之前遇到��文件结尾��，\r\n它将返回 <code>ErrorKind::UnexpectedEof</code> 类型的错误。\r\n在这种情况下，<code>buf</code> 的内容是未指定的。</p>')),
        (E('<p>This method is not cancellation safe. If the method is used as the\r\nevent in a tokio::select! statement and some\r\nother branch completes first, then some data may already have been\r\nread into buf.</p>'),
         E('<p>此方法不是可取消安全的。如果在 <code>tokio::select!</code> 语句中将其作为事件，\r\n而其他分支先完成，则可能已经有一些数据被读入 <code>buf</code>。</p>')),
        (E('<p>This method is not cancellation safe. If the method is used as the\r\nevent in a tokio::select! statement and some\r\nother branch completes first, then some data may be lost.</p>'),
         E('<p>此方法不是可取消安全的。如果在 <code>tokio::select!</code> 语句中将其作为事件，\r\n而其他分支先完成，则可能会丢失部分数据。</p>')),
    ],
    'io/trait.AsyncSeek.html': [
        (E('<p>Seeks to an offset, in bytes, in the underlying reader.</p>'),
         E('<p>在底层读取器中按字节偏移量定位。</p>')),
    ],
    'io/trait.AsyncWrite.html': [
        (E('<p>On success, returns <code>Poll::Ready(Ok(num_bytes_written))</code>.</p>'),
         E('<p>成功时，返回 <code>Poll::Ready(Ok(num_bytes_written))</code>。</p>')),
        (E('<p>This should be implemented as a single ��atomic�� write action. If any\r\ndata has been partially written, it is wrong to return an error or\r\npending.</p>'),
         E('<p>此方法应实现为单个��原子��写入操作。\r\n如果已经部分写入了数据，那么返回错误或 pending 都是错误的。</p>')),
    ],
    'io/trait.AsyncWriteExt.html': [
        (E('<p>Equivalent to:</p>'),
         E('<p>等价于：</p>')),
        (E('<p>This method is not cancellation safe. If it is used as the event\r\nin a tokio::select! statement and some other\r\nbranch completes first, then the provided buffer may have been\r\npartially written, but the data written by this method is lost.</p>'),
         E('<p>此方法不是可取消安全的。如果在 <code>tokio::select!</code> 语句中将其作为事件，\r\n而其他分支先完成，则提供的缓冲区可能已被部分写入，\r\n但此方法写入的数据将丢失。</p>')),
        (E('<p>Write unsigned 8 bit integers to a AsyncWrite:</p>'),
         E('<p>向 <code>AsyncWrite</code> 写入无符号 8 位整数：</p>')),
        (E('<p>Write signed 8 bit integers to a AsyncWrite:</p>'),
         E('<p>向 <code>AsyncWrite</code> 写入有符号 8 位整数：</p>')),
    ],
}

# Patterns with signed N-bit integer (singular form, not "a signed" but "an signed")
# These appear in read_i64, read_i128 (i.e. bits > 8 where the article changes)
def gen_signed_singular_read_pairs(bits, endian):
    """Generate pairs for read_iN where the article is 'an' (i64, i128)."""
    pairs = []
    desc_text = f'<p>Reads an signed {bits}-bit integer in {endian}-endian order from the\nunderlying reader.</p>'.encode('utf-8')
    desc_zh = f'<p>从底层读取器以{"大" if endian == "big" else "小"}端字节序读取一个有符号 {bits}-位整数。</p>'.encode('utf-8')
    pairs.append((desc_text, desc_zh))
    return pairs

def gen_signed_singular_write_pairs(bits, endian):
    """Generate pairs for write_iN where the article is 'an' (i64, i128)."""
    pairs = []
    desc_text = f'<p>Writes an signed {bits}-bit integer in {endian}-endian order to the\nunderlying writer.</p>'.encode('utf-8')
    desc_zh = f'<p>以{"大" if endian == "big" else "小"}端字节序向底层写入器写入一个有符号 {bits}-位整数。</p>'.encode('utf-8')
    pairs.append((desc_text, desc_zh))
    return pairs

# Add to AsyncReadExt
read_ext_extra = []
for bits in [64, 128]:
    for endian_en, endian_zh in [('big', '大'), ('little', '小')]:
        read_ext_extra.extend(gen_signed_singular_read_pairs(bits, endian_en))

# Add to AsyncWriteExt
write_ext_extra = []
for bits in [64, 128]:
    for endian_en, endian_zh in [('big', '大'), ('little', '小')]:
        write_ext_extra.extend(gen_signed_singular_write_pairs(bits, endian_en))

# Add "Read unsigned N-bit big/little-endian integers from a AsyncRead:" patterns
def gen_read_int_example_pairs(bits, signed, endian):
    """Generate pair for 'Read unsigned 32-bit big-endian integers from a AsyncRead:'"""
    pairs = []
    sign_word = 'signed' if signed else 'unsigned'
    sign_zh = '有符号' if signed else '无符号'
    endian_zh = '大端' if endian == 'be' else '小端'
    text = f'<p>Read {sign_word} {bits}-bit {"big" if endian == "be" else "little"}-endian integers from a <code>AsyncRead</code>:</p>'.encode('utf-8')
    zh = f'<p>从 <code>AsyncRead</code> 读取{sign_zh} {bits} 位{endian_zh}整数：</p>'.encode('utf-8')
    pairs.append((text, zh))
    return pairs

# For all integer read methods, add the example
read_ext_examples = []
for bits in [8, 16, 32, 64, 128]:
    for signed in [True, False]:
        # 8-bit has only one variant
        if bits == 8:
            sign_word = 'signed' if signed else 'unsigned'
            sign_zh = '有符号' if signed else '无符号'
            text = f'<p>Read {sign_word} 8 bit integers from an <code>AsyncRead</code>:</p>'.encode('utf-8')
            zh = f'<p>从 <code>AsyncRead</code> 读取{sign_zh} 8 位整数：</p>'.encode('utf-8')
            read_ext_examples.append((text, zh))
        else:
            for endian in ['be', 'le']:
                read_ext_examples.extend(gen_read_int_example_pairs(bits, signed, endian))

# For write methods
def gen_write_int_example_pairs(bits, signed, endian):
    pairs = []
    sign_word = 'signed' if signed else 'unsigned'
    sign_zh = '有符号' if signed else '无符号'
    endian_zh = '大端' if endian == 'be' else '小端'
    text = f'<p>Write {sign_word} {bits}-bit {"big" if endian == "be" else "little"}-endian integers to a <code>AsyncWrite</code>:</p>'.encode('utf-8')
    zh = f'<p>向 <code>AsyncWrite</code> 写入{sign_zh} {bits} 位{endian_zh}整数：</p>'.encode('utf-8')
    pairs.append((text, zh))
    return pairs

write_ext_examples = []
for bits in [8, 16, 32, 64, 128]:
    for signed in [True, False]:
        if bits == 8:
            sign_word = 'signed' if signed else 'unsigned'
            sign_zh = '有符号' if signed else '无符号'
            text = f'<p>Write {sign_word} 8 bit integers to a <code>AsyncWrite</code>:</p>'.encode('utf-8')
            zh = f'<p>向 <code>AsyncWrite</code> 写入{sign_zh} 8 位整数：</p>'.encode('utf-8')
            write_ext_examples.append((text, zh))
        else:
            for endian in ['be', 'le']:
                write_ext_examples.extend(gen_write_int_example_pairs(bits, signed, endian))

PAIRS.setdefault('io/trait.AsyncReadExt.html', []).extend(read_ext_extra)
PAIRS.setdefault('io/trait.AsyncReadExt.html', []).extend(read_ext_examples)
PAIRS.setdefault('io/trait.AsyncWriteExt.html', []).extend(write_ext_extra)
PAIRS.setdefault('io/trait.AsyncWriteExt.html', []).extend(write_ext_examples)


def main():
    total_replacements = 0
    files_modified = 0

    for rel, pairs in PAIRS.items():
        if not os.path.exists(os.path.join(ROOT, rel)):
            print(f'NOT FOUND: {rel}')
            continue
        original = read_bytes(rel)
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
            # Try CRLF
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
            print(f'{rel}: {local_replacements} replacements' + (f' ({len(unmatched)} unmatched)' if unmatched else ''))
            for u in unmatched[:5]:
                print(f'   UNMATCHED: {u!r}')
        else:
            print(f'{rel}: NO changes' + (f' ({len(unmatched)} unmatched)' if unmatched else ''))
            for u in unmatched[:5]:
                print(f'   UNMATCHED: {u!r}')

        total_replacements += local_replacements

    print(f'\nTotal: {total_replacements} replacements across {files_modified} files')


if __name__ == '__main__':
    main()
