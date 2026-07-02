"""Third pass - handle remaining patterns with smart quotes and long text."""
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


# Smart quotes encoded as bytes
LQ = b'\xe2\x80\x9c'  # "
RQ = b'\xe2\x80\x9d'  # "

PAIRS = {
    'io/struct.ReadBuf.html': [
        (E('<p>Since ReadBuf tracks the region of the buffer that has been initialized, this is effectively ') + LQ + E('free') + RQ + E(' after\r\nthe first use.</p>'),
         E('<p>由于 ReadBuf 会跟踪缓冲区中已被初始化的区域，因此首次使用之后这实际上是') + LQ + E('免费的') + RQ + E('。</p>')),
    ],
    'io/trait.AsyncBufRead.html': [
        # Long poll_fill_buf text with smart quotes
        (E('<p>This function is a lower-level call. It needs to be paired with the\r\nconsume method to function properly. When calling this\r\nmethod, none of the contents will be ') + LQ + E('read') + RQ + E(' in the sense that later\r\ncalling <a href="trait.AsyncRead.html#tymethod.poll_read" title="method tokio::io::AsyncRead::poll_read"><code>poll_read</code></a> may return the same contents. As such, <a href="trait.AsyncBufRead.html#tymethod.consume" title="method tokio::io::AsyncBufRead::consume"><code>consume</code></a> must\r\nbe called with the number of bytes that are consumed from this buffer to\r\nensure that the bytes are never returned twice.</p>'),
         E('<p>此函数是较低级别的调用。要使其正常工作，需要与\r\n<a href="trait.AsyncBufRead.html#tymethod.consume" title="method tokio::io::AsyncBufRead::consume"><code>consume</code></a> 方法配对使用。\r\n调用此方法时，其中的内容不会被视为已') + LQ + E('读') + RQ + E('，\r\n因此随后调用 <a href="trait.AsyncRead.html#tymethod.poll_read" title="method tokio::io::AsyncRead::poll_read"><code>poll_read</code></a> 仍可能返回相同的内容。\r\n因此，必须使用从此缓冲区消费的字节数调用 <a href="trait.AsyncBufRead.html#tymethod.consume" title="method tokio::io::AsyncBufRead::consume"><code>consume</code></a>，\r\n以确保相同的字节不会被返回两次。</p>')),
    ],
    'io/trait.AsyncBufReadExt.html': [
        # Long read_line text - 2 versions: with and without smart quotes
        (E('<p>This method is not cancellation safe. If the method is used as the\r\nevent in a tokio::select! statement and some\r\nother branch completes first, then some data may have been partially\r\nread, and this data is lost. There are no guarantees regarding the\r\ncontents of buf when the call is cancelled. The next call to read_line will resume reading from where this call left off.</p>'),
         E('<p>此方法不是可取消安全的。如果在 <code>tokio::select!</code> 语句中将其作为事件，\r\n而其他分支先完成，则可能已经部分读取了一些数据，\r\n这些数据将丢失。取消调用时 <code>buf</code> 的内容没有任何保证。\r\n下次调用 <code>read_line</code> 将从此调用中断的位置继续读取。</p>')),
        # Long fill_buf text
        (E('<p>This function is a lower-level call. It needs to be paired with the\r\nconsume method to function properly. When calling this method,\r\nnone of the contents will be ') + LQ + E('read') + RQ + E(' in the sense that later calling\r\n<code>read</code> may return the same contents. As such, <a href="trait.AsyncBufReadExt.html#method.consume" title="method tokio::io::AsyncBufReadExt::consume"><code>consume</code></a> must be\r\ncalled with the number of bytes that are consumed from this buffer\r\nto ensure that the bytes are never returned twice.</p>'),
         E('<p>此函数是较低级别的调用。要使其正常工作，需要与\r\n<a href="trait.AsyncBufReadExt.html#method.consume" title="method tokio::io::AsyncBufReadExt::consume"><code>consume</code></a> 方法配对使用。\r\n调用此方法时，其中的内容不会被视为已') + LQ + E('读') + RQ + E('，\r\n因此随后调用 <code>read</code> 仍可能返回相同的内容。\r\n因此，必须使用从此缓冲区消费的字节数调用 <a href="trait.AsyncBufReadExt.html#method.consume" title="method tokio::io::AsyncBufReadExt::consume"><code>consume</code></a>，\r\n以确保相同的字节不会被返回两次。</p>')),
        (E('<p>This method is cancel safe. If you use it as the event in a\r\ntokio::select! statement and some other branch\r\ncompletes first, then it is guaranteed that no data was read.</p>'),
         E('<p>此方法是可取消安全的。如果在 <code>tokio::select!</code> 语句中将其作为事件，\r\n而其他分支先完成，则可以保证没有数据被读取。</p>')),
    ],
    'io/trait.AsyncReadExt.html': [
        # Common "This method is cancel safe" with <a href> link
        (E('<p>This method is cancel safe. If you use it as the event in a\r\n<a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a>\r\nstatement and some other branch\r\ncompletes first, then it is guaranteed that no data was read.</p>'),
         E('<p>此方法是可取消安全的。如果在 <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> 语句中将其作为事件，\r\n而其他分支先完成，则可以保证没有数据被读取。</p>')),
        # Common "This method is not cancellation safe" with <a href> link
        (E('<p>This method is not cancellation safe. If the method is used as the\r\nevent in a <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a>\r\nstatement and some\r\nother branch completes first, then some data may already have been\r\nread into buf.</p>'),
         E('<p>此方法不是可取消安全的。如果在 <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> 语句中将其作为事件，\r\n而其他分支先完成，则可能已经有一些数据被读入 <code>buf</code>。</p>')),
        (E('<p>This method is not cancellation safe. If the method is used as the\r\nevent in a <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a>\r\nstatement and some\r\nother branch completes first, then some data may be lost.</p>'),
         E('<p>此方法不是可取消安全的。如果在 <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> 语句中将其作为事件，\r\n而其他分支先完成，则可能会丢失部分数据。</p>')),
        # "end of file" with smart quotes
        (E('<p>If the operation encounters an ') + LQ + E('end of file') + RQ + E(' before completely\r\nfilling the buffer, it returns an error of the kind\r\nErrorKind::UnexpectedEof. The contents of buf are unspecified\r\nin this case.</p>'),
         E('<p>如果在完全填满缓冲区之前遇到') + LQ + E('文件结尾') + RQ + E('，\r\n它将返回 <code>ErrorKind::UnexpectedEof</code> 类型的错误。\r\n在这种情况下，<code>buf</code> 的内容是未指定的。</p>')),
    ],
    'io/trait.AsyncWrite.html': [
        (E('<p>This should be implemented as a single ') + LQ + E('atomic') + RQ + E(' write action. If any\r\ndata has been partially written, it is wrong to return an error or\r\npending.</p>'),
         E('<p>此方法应实现为单个') + LQ + E('原子') + RQ + E('写入操作。\r\n如果已经部分写入了数据，那么返回错误或 pending 都是错误的。</p>')),
    ],
    'io/trait.AsyncWriteExt.html': [
        (E('<p>This method is not cancellation safe. If it is used as the event\r\nin a <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> statement and some other\r\nbranch completes first, then the provided buffer may have been\r\npartially written, but future calls to write_all will start over\r\nfrom the beginning of the buffer.</p>'),
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
