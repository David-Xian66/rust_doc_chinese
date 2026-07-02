"""Fourth pass - handle remaining patterns with correct line breaks."""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))


def read_bytes(rel):
    with open(os.path.join(ROOT, rel), 'rb') as f:
        return f.read()


def write_bytes(rel, data):
    with open(os.path.join(ROOT, rel), 'wb') as f:
        f.write(data)


def E(s):
    return s.encode('utf-8')


LQ = b'\xe2\x80\x9c'  # "
RQ = b'\xe2\x80\x9d'  # "

# Note: actual files use <a href=...>tokio::select!</a> statement (no \r\n)
# and various other patterns without extra newlines

PAIRS = {
    'io/struct.ReadBuf.html': [
        (E('<p>Since <code>ReadBuf</code> tracks the region of the buffer that has been initialized, this is effectively ') + LQ + E('free') + RQ + E(' after\r\nthe first use.</p>'),
         E('<p>由于 <code>ReadBuf</code> 会跟踪缓冲区中已被初始化的区域，因此首次使用之后这实际上是') + LQ + E('免费的') + RQ + E('。</p>')),
    ],
    'io/trait.AsyncBufRead.html': [
        # Long poll_fill_buf with <a href> wrapping "consume" - actual has <code>consume</code>
        (E('<p>This function is a lower-level call. It needs to be paired with the\r\n<a href="trait.AsyncBufRead.html#tymethod.consume" title="method tokio::io::AsyncBufRead::consume"><code>consume</code></a> method to function properly. When calling this\r\nmethod, none of the contents will be ') + LQ + E('read') + RQ + E(' in the sense that later\r\ncalling <a href="trait.AsyncRead.html#tymethod.poll_read" title="method tokio::io::AsyncRead::poll_read"><code>poll_read</code></a> may return the same contents. As such, <a href="trait.AsyncBufRead.html#tymethod.consume" title="method tokio::io::AsyncBufRead::consume"><code>consume</code></a> must\r\nbe called with the number of bytes that are consumed from this buffer to\r\nensure that the bytes are never returned twice.</p>'),
         E('<p>此函数是较低级别的调用。要使其正常工作，需要与\r\n<a href="trait.AsyncBufRead.html#tymethod.consume" title="method tokio::io::AsyncBufRead::consume"><code>consume</code></a> 方法配对使用。\r\n调用此方法时，其中的内容不会被视为已') + LQ + E('读') + RQ + E('，\r\n因此随后调用 <a href="trait.AsyncRead.html#tymethod.poll_read" title="method tokio::io::AsyncRead::poll_read"><code>poll_read</code></a> 仍可能返回相同的内容。\r\n因此，必须使用从此缓冲区消费的字节数调用 <a href="trait.AsyncBufRead.html#tymethod.consume" title="method tokio::io::AsyncBufRead::consume"><code>consume</code></a>，\r\n以确保相同的字节不会被返回两次。</p>')),
    ],
    'io/trait.AsyncBufReadExt.html': [
        (E('<p>This method is not cancellation safe. If the method is used as the\r\nevent in a <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> statement and some\r\nother branch completes first, then some data may have been partially\r\nread, and this data is lost. There are no guarantees regarding the\r\ncontents of <code>buf</code> when the call is cancelled. The current\r\nimplementation replaces <code>buf</code> with the empty string, but this may\r\nchange in the future.</p>'),
         E('<p>此方法不是可取消安全的。如果在 <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> 语句中将其作为事件，\r\n而其他分支先完成，则可能已经部分读取了一些数据，\r\n这些数据将丢失。取消调用时 <code>buf</code> 的内容没有任何保证。\r\n当前实现会将 <code>buf</code> 替换为空字符串，但未来可能会改变。</p>')),
        (E('<p>This function is a lower-level call. It needs to be paired with the\r\n<a href="trait.AsyncBufReadExt.html#method.consume" title="method tokio::io::AsyncBufReadExt::consume"><code>consume</code></a> method to function properly. When calling this method,\r\nnone of the contents will be ') + LQ + E('read') + RQ + E(' in the sense that later calling\r\n<code>read</code> may return the same contents. As such, <a href="trait.AsyncBufReadExt.html#method.consume" title="method tokio::io::AsyncBufReadExt::consume"><code>consume</code></a> must be\r\ncalled with the number of bytes that are consumed from this buffer\r\nto ensure that the bytes are never returned twice.</p>'),
         E('<p>此函数是较低级别的调用。要使其正常工作，需要与\r\n<a href="trait.AsyncBufReadExt.html#method.consume" title="method tokio::io::AsyncBufReadExt::consume"><code>consume</code></a> 方法配对使用。\r\n调用此方法时，其中的内容不会被视为已') + LQ + E('读') + RQ + E('，\r\n因此随后调用 <code>read</code> 仍可能返回相同的内容。\r\n因此，必须使用从此缓冲区消费的字节数调用 <a href="trait.AsyncBufReadExt.html#method.consume" title="method tokio::io::AsyncBufReadExt::consume"><code>consume</code></a>，\r\n以确保相同的字节不会被返回两次。</p>')),
        (E('<p>This method is cancel safe. If you use it as the event in a\r\n<a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> statement and some other branch\r\ncompletes first, then it is guaranteed that no data was read.</p>'),
         E('<p>此方法是可取消安全的。如果在 <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> 语句中将其作为事件，\r\n而其他分支先完成，则可以保证没有数据被读取。</p>')),
    ],
    'io/trait.AsyncReadExt.html': [
        # "This method is cancel safe" - no \r\n between </a> and statement
        (E('<p>This method is cancel safe. If you use it as the event in a\r\n<a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> statement and some other branch\r\ncompletes first, then it is guaranteed that no data was read.</p>'),
         E('<p>此方法是可取消安全的。如果在 <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> 语句中将其作为事件，\r\n而其他分支先完成，则可以保证没有数据被读取。</p>')),
        # "This method is not cancellation safe" - already have been, into buf
        (E('<p>This method is not cancellation safe. If the method is used as the\r\nevent in a <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> statement and some\r\nother branch completes first, then some data may already have been\r\nread into <code>buf</code>.</p>'),
         E('<p>此方法不是可取消安全的。如果在 <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> 语句中将其作为事件，\r\n而其他分支先完成，则可能已经有一些数据被读入 <code>buf</code>。</p>')),
        # "This method is not cancellation safe" - may be lost (single line version)
        (E('<p>This method is not cancellation safe. If the method is used as the\r\nevent in a <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> statement and some\r\nother branch completes first, then some data may be lost.</p>'),
         E('<p>此方法不是可取消安全的。如果在 <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> 语句中将其作为事件，\r\n而其他分支先完成，则可能会丢失部分数据。</p>')),
        # "end of file" with smart quotes
        (E('<p>If the operation encounters an ') + LQ + E('end of file') + RQ + E(' before completely\r\nfilling the buffer, it returns an error of the kind\r\n<a href="https://doc.rust-lang.org/1.95.0/std/io/error/enum.ErrorKind.html#variant.UnexpectedEof" title="variant std::io::error::ErrorKind::UnexpectedEof"><code>ErrorKind::UnexpectedEof</code></a>. The contents of <code>buf</code> are unspecified\r\nin this case.</p>'),
         E('<p>如果在完全填满缓冲区之前遇到') + LQ + E('文件结尾') + RQ + E('，\r\n它将返回 <a href="https://doc.rust-lang.org/1.95.0/std/io/error/enum.ErrorKind.html#variant.UnexpectedEof" title="variant std::io::error::ErrorKind::UnexpectedEof"><code>ErrorKind::UnexpectedEof</code></a> 类型的错误。\r\n在这种情况下，<code>buf</code> 的内容是未指定的。</p>')),
    ],
    'io/trait.AsyncWriteExt.html': [
        (E('<p>This method is not cancellation safe. If it is used as the event\r\nin a <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> statement and some other\r\nbranch completes first, then the provided buffer may have been\r\npartially written, but future calls to <code>write_all</code> will start over\r\nfrom the beginning of the buffer.</p>'),
         E('<p>此方法不是可取消安全的。如果在 <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> 语句中将其作为事件，\r\n而其他分支先完成，则提供的缓冲区可能已被部分写入，\r\n但下次调用 <code>write_all</code> 将从缓冲区的开头重新开始。</p>')),
    ],
}


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
            if en_b in content:
                count = content.count(en_b)
                local_replacements += count
                content = content.replace(en_b, zh_b)
                continue
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
