"""Translate 13 untranslated docblocks in quinn/struct.RecvStream.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/struct.RecvStream.html'

TRANSLATIONS = [
    ('<p>Read data contiguously from the stream.</p>\n<p>Yields the number of bytes read into <code>buf</code> on success, or <code>None</code> if the stream was finished.</p>\n<p>This operation is cancel-safe.</p>',
     '<p>从流中连续读取数据。</p>\n<p>成功时返回已读入 <code>buf</code> 的字节数；若流已结束，则返回 <code>None</code>。</p>\n<p>此操作是取消安全的。</p>'),
    ('<p>Read an exact number of bytes contiguously from the stream.</p>\n<p>See <a href="struct.RecvStream.html#method.read" title="method quinn::RecvStream::read"><code>read()</code></a> for details. This operation is <em>not</em> cancel-safe.</p>',
     '<p>从流中连续读取指定数量的字节。</p>\n<p>详见 <a href="struct.RecvStream.html#method.read" title="method quinn::RecvStream::read"><code>read()</code></a>。此操作<em>不</em>是取消安全的。</p>'),
    ('<p>Attempts to read from the stream into the provided buffer</p>\n<p>On success, returns <code>Poll::Ready(Ok(num_bytes_read))</code> and places data into <code>buf</code>. If this\nreturns zero bytes read (and <code>buf</code> has a non-zero length), that indicates that the remote\nside has <a href="struct.SendStream.html#method.finish" title="method quinn::SendStream::finish"><code>finish</code></a>ed the stream and the local side has already read all bytes.</p>\n<p>If no data is available for reading, this returns <code>Poll::Pending</code> and arranges for the\ncurrent task (via <code>cx.waker()</code>) to be notified when the stream becomes readable or is\nclosed.</p>',
     '<p>尝试从流中读取数据到所提供的缓冲区</p>\n<p>成功时返回 <code>Poll::Ready(Ok(num_bytes_read))</code>，并将数据放入 <code>buf</code>。如果返回读取到的字节数为零（且 <code>buf</code> 长度非零），表示远端已经 <a href="struct.SendStream.html#method.finish" title="method quinn::SendStream::finish"><code>finish</code></a> 了流，且本地端已读取完所有字节。</p>\n<p>如果没有可读数据，则返回 <code>Poll::Pending</code>，并安排当前任务（经由 <code>cx.waker()</code>）在流变为可读或被关闭时收到通知。</p>'),
    ('<p>Attempts to read from the stream into the provided buffer, which may be uninitialized</p>\n<p>On success, returns <code>Poll::Ready(Ok(()))</code> and places data into the unfilled portion of\n<code>buf</code>. If this does not write any bytes to <code>buf</code> (and <code>buf.remaining()</code> is non-zero), that\nindicates that the remote side has <a href="struct.SendStream.html#method.finish" title="method quinn::SendStream::finish"><code>finish</code></a>ed the stream and the local side has already\nread all bytes.</p>\n<p>If no data is available for reading, this returns <code>Poll::Pending</code> and arranges for the\ncurrent task (via <code>cx.waker()</code>) to be notified when the stream becomes readable or is\nclosed.</p>',
     '<p>尝试从流中读取数据到所提供的缓冲区（缓冲区可能未初始化）</p>\n<p>成功时返回 <code>Poll::Ready(Ok(()))</code>，并将数据放入 <code>buf</code> 的未填充区域。如果未向 <code>buf</code> 写入任何字节（且 <code>buf.remaining()</code> 非零），表示远端已经 <a href="struct.SendStream.html#method.finish" title="method quinn::SendStream::finish"><code>finish</code></a> 了流，且本地端已读取完所有字节。</p>\n<p>如果没有可读数据，则返回 <code>Poll::Pending</code>，并安排当前任务（经由 <code>cx.waker()</code>）在流变为可读或被关闭时收到通知。</p>'),
    ('<p>Read the next segment of data</p>\n<p>Yields <code>None</code> if the stream was finished. Otherwise, yields a segment of data and its\noffset in the stream. If <code>ordered</code> is <code>true</code>, the chunk’s offset will be immediately after\nthe last data yielded by <code>read()</code> or <code>read_chunk()</code>. If <code>ordered</code> is <code>false</code>, segments may\nbe received in any order, and the <code>Chunk</code>’s <code>offset</code> field can be used to determine\nordering in the caller. Unordered reads are less prone to head-of-line blocking within a\nstream, but require the application to manage reassembling the original data.</p>\n<p>Slightly more efficient than <code>read</code> due to not copying. Chunk boundaries do not correspond\nto peer writes, and hence cannot be used as framing.</p>\n<p>This operation is cancel-safe.</p>',
     '<p>读取下一段数据</p>\n<p>若流已结束，返回 <code>None</code>；否则返回一段数据及其在流中的偏移。若 <code>ordered</code> 为 <code>true</code>，数据块的偏移紧跟在 <code>read()</code> 或 <code>read_chunk()</code> 上次返回的数据之后；若为 <code>false</code>，各段可能按任意顺序到达，调用方可借助 <code>Chunk</code> 的 <code>offset</code> 字段自行确定顺序。无序读取更不易在单个流中产生队头阻塞，但应用需自行管理原始数据的重组。</p>\n<p>因为无需拷贝，所以略高于 <code>read</code> 的效率。数据块的边界与对端的写入不对应，因此不能用作分帧。</p>\n<p>此操作是取消安全的。</p>'),
    ('<p>Read the next segments of data</p>\n<p>Fills <code>bufs</code> with the segments of data beginning immediately after the\nlast data yielded by <code>read</code> or <code>read_chunk</code>, or <code>None</code> if the stream was\nfinished.</p>\n<p>Slightly more efficient than <code>read</code> due to not copying. Chunk boundaries\ndo not correspond to peer writes, and hence cannot be used as framing.</p>\n<p>This operation is cancel-safe.</p>',
     '<p>读取接下来若干段数据</p>\n<p>使用紧接在 <code>read</code> 或 <code>read_chunk</code> 上次返回数据之后的数据段填满 <code>bufs</code>；若流已结束则返回 <code>None</code>。</p>\n<p>因为无需拷贝，所以略高于 <code>read</code> 的效率。数据块的边界与对端的写入不对应，因此不能用作分帧。</p>\n<p>此操作是取消安全的。</p>'),
    ('<p>Convenience method to read all remaining data into a buffer</p>\n<p>Fails with <a href="enum.ReadToEndError.html#variant.TooLong" title="variant quinn::ReadToEndError::TooLong"><code>ReadToEndError::TooLong</code></a> on reading more than <code>size_limit</code> bytes, discarding\nall data read. Uses unordered reads to be more efficient than using <code>AsyncRead</code> would\nallow. <code>size_limit</code> should be set to limit worst-case memory use.</p>\n<p>If unordered reads have already been made, the resulting buffer may have gaps containing\narbitrary data.</p>\n<p>This operation is <em>not</em> cancel-safe.</p>',
     '<p>将所有剩余数据读取到一个缓冲区的便捷方法</p>\n<p>若读取字节数超过 <code>size_limit</code>，则返回 <a href="enum.ReadToEndError.html#variant.TooLong" title="variant quinn::ReadToEndError::TooLong"><code>ReadToEndError::TooLong</code></a>，并丢弃已读取的全部数据。该方法使用无序读取，比使用 <code>AsyncRead</code> 接口更高效。<code>size_limit</code> 用于限制最坏情况下的内存占用。</p>\n<p>若此前已做过无序读取，结果缓冲区中可能出现包含任意数据的间隙。</p>\n<p>此操作<em>不</em>是取消安全的。</p>'),
    ('<p>Stop accepting data</p>\n<p>Discards unread data and notifies the peer to stop transmitting. Once stopped, further\nattempts to operate on a stream will yield <code>ClosedStream</code> errors.</p>',
     '<p>停止接受数据</p>\n<p>丢弃尚未读取的数据，并通知对端停止发送。停止之后，任何再对该流进行的操作都将返回 <code>ClosedStream</code> 错误。</p>'),
    ('<p>Check if this stream has been opened during 0-RTT.</p>\n<p>In which case any non-idempotent request should be considered dangerous at the application\nlevel. Because read data is subject to replay attacks.</p>',
     '<p>检查该流是否在 0-RTT 期间被打开。</p>\n<p>若为 0-RTT 流，则任何非幂等请求在应用层都应视为存在危险，因为读取到的数据可能遭受重放攻击。</p>'),
    ('<p>Get the identity of this stream</p>',
     '<p>获取该流的标识</p>'),
    ('<p>Completes when the stream has been reset by the peer or otherwise closed</p>\n<p>Yields <code>Some</code> with the reset error code when the stream is reset by the peer. Yields <code>None</code>\nwhen the stream was previously <a href="struct.RecvStream.html#method.stop" title="method quinn::RecvStream::stop"><code>stop()</code></a>ed, or when the stream was\n<a href="struct.SendStream.html#method.finish" title="method quinn::SendStream::finish"><code>finish()</code></a>ed by the peer and all data has been received, after\nwhich it is no longer meaningful for the stream to be reset.</p>\n<p>This operation is cancel-safe.</p>',
     '<p>当对端重置或以其他方式关闭流时完成</p>\n<p>若对端重置了该流，返回带有重置错误码的 <code>Some</code>。若流此前已被 <a href="struct.RecvStream.html#method.stop" title="method quinn::RecvStream::stop"><code>stop()</code></a>，或对端已 <a href="struct.SendStream.html#method.finish" title="method quinn::SendStream::finish"><code>finish()</code></a> 且所有数据均已收到，则返回 <code>None</code>；此后该流被重置便不再有意义。</p>\n<p>此操作是取消安全的。</p>'),
    ('</h4></section></summary><div class="docblock"><p>Returns the argument unchanged.</p>',
     '</h4></section></summary><div class="docblock"><p>原样返回该参数。</p>'),
    ('<p>Calls <code>U::from(self)</code>.</p>\n<p>That is, this conversion is whatever the implementation of\n<code><a href="https://doc.rust-lang.org/1.95.0/core/convert/trait.From.html" title="trait core::convert::From">From</a>&lt;T&gt; for U</code> chooses to do.</p>',
     '<p>调用 <code>U::from(self)</code>。</p>\n<p>也就是说，此转换行为完全由\n<code><a href="https://doc.rust-lang.org/1.95.0/core/convert/trait.From.html" title="trait core::convert::From">From</a>&lt;T&gt; for U</code> 的实现决定。</p>'),
]


def main():
    with open(PATH, 'r', encoding='utf-8') as f:
        c = f.read()

    found = 0
    missed = []
    for old, new in TRANSLATIONS:
        if old in c:
            c = c.replace(old, new)
            found += 1
        else:
            missed.append(old[:80])

    with open(PATH, 'w', encoding='utf-8') as f:
        f.write(c)

    cjk = re.findall(r'[一-鿿]', c)
    print(f'Found: {found}/{len(TRANSLATIONS)} docblocks')
    print(f'CJK: {len(cjk)}')
    if missed:
        print('Missed docblocks:')
        for m in missed:
            print(f'  {m!r}')


if __name__ == '__main__':
    main()