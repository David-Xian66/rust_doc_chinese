"""Translate 14 untranslated docblocks in quinn/struct.SendStream.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/struct.SendStream.html'

TRANSLATIONS = [
    # 1. write
    ('<p>Write a buffer into this stream, returning how many bytes were written</p>\n<p>Unless this method errors, it waits until some amount of <code>buf</code> can be written into this\nstream, and then writes as much as it can without waiting again. Due to congestion and flow\ncontrol, this may be shorter than <code>buf.len()</code>. On success this yields the length of the\nprefix that was written.</p>\n<h5 id="cancel-safety"><a class="doc-anchor" href="#cancel-safety">§</a>Cancel safety</h5>\n<p>This method is cancellation safe. If this does not resolve, no bytes were written.</p>',
     '<p>将一个缓冲区写入该流，并返回实际写入的字节数</p>\n<p>除非此方法出错，否则它会一直等到 <code>buf</code> 中的部分字节可以写入该流，然后尽可能多地写入而不再等待。受拥塞控制与流量控制影响，实际写入长度可能小于 <code>buf.len()</code>。成功时返回已写入前缀的长度。</p>\n<h5 id="cancel-safety"><a class="doc-anchor" href="#cancel-safety">§</a>取消安全性</h5>\n<p>该方法是取消安全的。如果它没有完成，不会写入任何字节。</p>'),
    # 2. write_all
    ('<p>Write a buffer into this stream in its entirety</p>\n<p>This method repeatedly calls <a href="struct.SendStream.html#method.write" title="method quinn::SendStream::write"><code>write</code></a> until all bytes are written, or an\nerror occurs.</p>\n<h5 id="cancel-safety-1"><a class="doc-anchor" href="#cancel-safety-1">§</a>Cancel safety</h5>\n<p>This method is <em>not</em> cancellation safe. Even if this does not resolve, some prefix of <code>buf</code>\nmay have been written when previously polled.</p>',
     '<p>将整个缓冲区完整写入该流</p>\n<p>此方法会反复调用 <a href="struct.SendStream.html#method.write" title="method quinn::SendStream::write"><code>write</code></a>，直至所有字节写完或发生错误。</p>\n<h5 id="cancel-safety-1"><a class="doc-anchor" href="#cancel-safety-1">§</a>取消安全性</h5>\n<p>该方法<em>不</em>是取消安全的。即使未完成，此前轮询中也可能已经写入了 <code>buf</code> 的某个前缀。</p>'),
    # 3. write_chunks
    ('<p>Write a slice of <a href="../bytes/bytes/struct.Bytes.html" title="struct bytes::bytes::Bytes"><code>Bytes</code></a> into this stream, returning how much was written</p>\n<p>Bytes to try to write are provided to this method as an array of cheaply cloneable chunks.\nUnless this method errors, it waits until some amount of those bytes can be written into\nthis stream, and then writes as much as it can without waiting again. Due to congestion and\nflow control, this may be less than the total number of bytes.</p>\n<p>On success, this method both mutates <code>bufs</code> and yields an informative <a href="struct.Written.html" title="struct quinn::Written"><code>Written</code></a> struct\nindicating how much was written:</p>\n<ul>\n<li><a href="../bytes/bytes/struct.Bytes.html" title="struct bytes::bytes::Bytes"><code>Bytes</code></a> chunks that were fully written are mutated to be <a href="../bytes/bytes/struct.Bytes.html#method.is_empty" title="method bytes::bytes::Bytes::is_empty">empty</a>.</li>\n<li>If a <a href="../bytes/bytes/struct.Bytes.html" title="struct bytes::bytes::Bytes"><code>Bytes</code></a> chunk was partially written, it is <a href="../bytes/bytes/struct.Bytes.html#method.split_to" title="method bytes::bytes::Bytes::split_to">split to</a> contain\nonly the suffix of bytes that were not written.</li>\n<li>The yielded <a href="struct.Written.html" title="struct quinn::Written"><code>Written</code></a> struct indicates how many chunks were fully written as well as\nhow many bytes were written.</li>\n</ul>\n<h5 id="cancel-safety-2"><a class="doc-anchor" href="#cancel-safety-2">§</a>Cancel safety</h5>\n<p>This method is cancellation safe. If this does not resolve, no bytes were written.</p>',
     '<p>将一段 <a href="../bytes/bytes/struct.Bytes.html" title="struct bytes::bytes::Bytes"><code>Bytes</code></a> 切片写入该流，并返回实际写入的数量</p>\n<p>待写入的字节以一组廉价可克隆的数据块形式提供。除非此方法出错，否则它会等到部分字节可以写入，然后尽可能多地写入而不再等待。受拥塞控制与流量控制影响，实际写入可能少于总字节数。</p>\n<p>成功时，此方法会修改 <code>bufs</code> 并返回一个描述写入情况的 <a href="struct.Written.html" title="struct quinn::Written"><code>Written</code></a> 结构体：</p>\n<ul>\n<li>完全写入的 <a href="../bytes/bytes/struct.Bytes.html" title="struct bytes::bytes::Bytes"><code>Bytes</code></a> 数据块会被修改为<a href="../bytes/bytes/struct.Bytes.html#method.is_empty" title="method bytes::bytes::Bytes::is_empty">空</a>。</li>\n<li>若某 <a href="../bytes/bytes/struct.Bytes.html" title="struct bytes::bytes::Bytes"><code>Bytes</code></a> 数据块被部分写入，则会<a href="../bytes/bytes/struct.Bytes.html#method.split_to" title="method bytes::bytes::Bytes::split_to">切分为</a>只保留尚未写入的后缀字节。</li>\n<li>返回的 <a href="struct.Written.html" title="struct quinn::Written"><code>Written</code></a> 结构体会同时报告完整写入的数据块数和字节数。</li>\n</ul>\n<h5 id="cancel-safety-2"><a class="doc-anchor" href="#cancel-safety-2">§</a>取消安全性</h5>\n<p>该方法是取消安全的。如果未完成，不会写入任何字节。</p>'),
    # 4. write_chunk
    ('<p>Write a single <a href="../bytes/bytes/struct.Bytes.html" title="struct bytes::bytes::Bytes"><code>Bytes</code></a> into this stream in its entirety</p>\n<p>Bytes to write are provided to this method as an single cheaply cloneable chunk. This\nmethod repeatedly calls <a href="struct.SendStream.html#method.write_chunks" title="method quinn::SendStream::write_chunks"><code>write_chunks</code></a> until all bytes are written,\nor an error occurs.</p>\n<h5 id="cancel-safety-3"><a class="doc-anchor" href="#cancel-safety-3">§</a>Cancel safety</h5>\n<p>This method is <em>not</em> cancellation safe. Even if this does not resolve, some bytes may have\nbeen written when previously polled.</p>',
     '<p>将单个 <a href="../bytes/bytes/struct.Bytes.html" title="struct bytes::bytes::Bytes"><code>Bytes</code></a> 数据块完整写入该流</p>\n<p>待写入的字节以单个廉价可克隆的数据块形式提供。此方法会反复调用 <a href="struct.SendStream.html#method.write_chunks" title="method quinn::SendStream::write_chunks"><code>write_chunks</code></a>，直至所有字节写完或发生错误。</p>\n<h5 id="cancel-safety-3"><a class="doc-anchor" href="#cancel-safety-3">§</a>取消安全性</h5>\n<p>该方法<em>不</em>是取消安全的。即使未完成，此前轮询中也可能已经写入了部分字节。</p>'),
    # 5. write_all_chunks
    ('<p>Write a slice of <a href="../bytes/bytes/struct.Bytes.html" title="struct bytes::bytes::Bytes"><code>Bytes</code></a> into this stream in its entirety</p>\n<p>Bytes to write are provided to this method as an array of cheaply cloneable chunks. This\nmethod repeatedly calls <a href="struct.SendStream.html#method.write_chunks" title="method quinn::SendStream::write_chunks"><code>write_chunks</code></a> until all bytes are written,\nor an error occurs. This method mutates <code>bufs</code> by mutating all chunks to be\n<a href="../bytes/bytes/struct.Bytes.html#method.is_empty" title="method bytes::bytes::Bytes::is_empty">empty</a>.</p>\n<h5 id="cancel-safety-4"><a class="doc-anchor" href="#cancel-safety-4">§</a>Cancel safety</h5>\n<p>This method is <em>not</em> cancellation safe. Even if this does not resolve, some bytes may have\nbeen written when previously polled.</p>',
     '<p>将一段 <a href="../bytes/bytes/struct.Bytes.html" title="struct bytes::bytes::Bytes"><code>Bytes</code></a> 切片完整写入该流</p>\n<p>待写入的字节以一组廉价可克隆的数据块形式提供。此方法会反复调用 <a href="struct.SendStream.html#method.write_chunks" title="method quinn::SendStream::write_chunks"><code>write_chunks</code></a>，直至所有字节写完或发生错误。此方法会把 <code>bufs</code> 中的所有数据块都修改为<a href="../bytes/bytes/struct.Bytes.html#method.is_empty" title="method bytes::bytes::Bytes::is_empty">空</a>。</p>\n<h5 id="cancel-safety-4"><a class="doc-anchor" href="#cancel-safety-4">§</a>取消安全性</h5>\n<p>该方法<em>不</em>是取消安全的。即使未完成，此前轮询中也可能已经写入了部分字节。</p>'),
    # 6. finish
    ('<p>Notify the peer that no more data will ever be written to this stream</p>\n<p>It is an error to write to a <a href="struct.SendStream.html" title="struct quinn::SendStream"><code>SendStream</code></a> after <code>finish()</code>ing it. <a href="struct.SendStream.html#method.reset" title="method quinn::SendStream::reset"><code>reset()</code></a>\nmay still be called after <code>finish</code> to abandon transmission of any stream data that might\nstill be buffered.</p>\n<p>To wait for the peer to receive all buffered stream data, see <a href="struct.SendStream.html#method.stopped" title="method quinn::SendStream::stopped"><code>stopped()</code></a>.</p>\n<p>May fail if <a href="struct.SendStream.html#method.finish" title="method quinn::SendStream::finish"><code>finish()</code></a> or <a href="struct.SendStream.html#method.reset" title="method quinn::SendStream::reset"><code>reset()</code></a> was previously\ncalled. This error is harmless and serves only to indicate that the caller may have\nincorrect assumptions about the stream’s state.</p>',
     '<p>通知对端，此后将不会再向该流写入任何数据</p>\n<p>在 <code>finish()</code> 之后向 <a href="struct.SendStream.html" title="struct quinn::SendStream"><code>SendStream</code></a> 写入数据是错误的。在 <code>finish</code> 之后仍可调用 <a href="struct.SendStream.html#method.reset" title="method quinn::SendStream::reset"><code>reset()</code></a> 来丢弃可能仍在缓冲区中的所有流数据。</p>\n<p>若需等待对端接收完所有缓冲的流数据，请参阅 <a href="struct.SendStream.html#method.stopped" title="method quinn::SendStream::stopped"><code>stopped()</code></a>。</p>\n<p>如果之前已调用过 <a href="struct.SendStream.html#method.finish" title="method quinn::SendStream::finish"><code>finish()</code></a> 或 <a href="struct.SendStream.html#method.reset" title="method quinn::SendStream::reset"><code>reset()</code></a>，本方法可能失败。该错误无害，仅用于提示调用者可能对流的状态存在错误假设。</p>'),
    # 7. reset
    ('<p>Close the send stream immediately.</p>\n<p>No new data can be written after calling this method. Locally buffered data is dropped, and\npreviously transmitted data will no longer be retransmitted if lost. If an attempt has\nalready been made to finish the stream, the peer may still receive all written data.</p>\n<p>May fail if <a href="struct.SendStream.html#method.finish" title="method quinn::SendStream::finish"><code>finish()</code></a> or <a href="struct.SendStream.html#method.reset" title="method quinn::SendStream::reset"><code>reset()</code></a> was previously\ncalled. This error is harmless and serves only to indicate that the caller may have\nincorrect assumptions about the stream’s state.</p>',
     '<p>立即关闭发送流。</p>\n<p>调用此方法之后不可再写入任何新数据。本地缓冲的数据将被丢弃，此前已发送的数据若丢失也不会再重传。如果已经调用过 <code>finish</code>，对端仍可能收到全部已写入的数据。</p>\n<p>如果之前已调用过 <a href="struct.SendStream.html#method.finish" title="method quinn::SendStream::finish"><code>finish()</code></a> 或 <a href="struct.SendStream.html#method.reset" title="method quinn::SendStream::reset"><code>reset()</code></a>，本方法可能失败。该错误无害，仅用于提示调用者可能对流的状态存在错误假设。</p>'),
    # 8. set_priority
    ('<p>Set the priority of the send stream</p>\n<p>Every send stream has an initial priority of 0. Locally buffered data from streams with\nhigher priority will be transmitted before data from streams with lower priority. Changing\nthe priority of a stream with pending data may only take effect after that data has been\ntransmitted. Using many different priority levels per connection may have a negative\nimpact on performance.</p>',
     '<p>设置发送流的优先级</p>\n<p>每个发送流的初始优先级为 0。本地缓冲的数据中，优先级较高的流会先于优先级较低的流被发送。修改尚有未发送数据的流的优先级，可能要等到这些数据被发送后才会生效。在每个连接上使用过多不同的优先级等级可能对性能产生负面影响。</p>'),
    # 9. priority
    ('<p>Get the priority of the send stream</p>',
     '<p>获取发送流的优先级</p>'),
    # 10. stopped
    ('<p>Completes when the peer stops the stream or reads the stream to completion</p>\n<p>Yields <code>Some</code> with the stop error code if the peer stops the stream. Yields <code>None</code> if the\nlocal side <a href="struct.SendStream.html#method.finish" title="method quinn::SendStream::finish"><code>finish()</code></a>es the stream and then the peer acknowledges receipt\nof all stream data (although not necessarily the processing of it), after which the peer\nclosing the stream is no longer meaningful.</p>\n<p>For a variety of reasons, the peer may not send acknowledgements immediately upon receiving\ndata. As such, relying on <code>stopped</code> to know when the peer has read a stream to completion\nmay introduce more latency than using an application-level response of some sort.</p>',
     '<p>当对端停止该流或将该流读取完毕时完成</p>\n<p>若对端停止该流，则返回带有停止错误码的 <code>Some</code>。若本地端先 <a href="struct.SendStream.html#method.finish" title="method quinn::SendStream::finish"><code>finish()</code></a> 了流，随后对端确认收完所有流数据（虽然不一定已处理完），则返回 <code>None</code>，此后对端关闭流便不再有意义。</p>\n<p>出于多种原因，对端在收到数据后未必立即发送确认。因此，依靠 <code>stopped</code> 来判断对端何时将流读至完成，可能比采用某种应用层响应方式引入更大的延迟。</p>'),
    # 11. id
    ('<p>Get the identity of this stream</p>',
     '<p>获取该流的标识</p>'),
    # 12. poll_write
    ('<p>Attempt to write bytes from buf into the stream.</p>\n<p>On success, returns Poll::Ready(Ok(num_bytes_written)).</p>\n<p>If the stream is not ready for writing, the method returns Poll::Pending and arranges\nfor the current task (via cx.waker().wake_by_ref()) to receive a notification when the\nstream becomes writable or is closed.</p>',
     '<p>尝试将 <code>buf</code> 中的字节写入流中。</p>\n<p>成功时返回 <code>Poll::Ready(Ok(num_bytes_written))</code>。</p>\n<p>若流暂时不可写，该方法返回 <code>Poll::Pending</code>，并安排当前任务（经由 <code>cx.waker().wake_by_ref()</code>）在流变为可写或被关闭时收到通知。</p>'),
    # 13. From impl
    ('</h4></section></summary><div class="docblock"><p>Returns the argument unchanged.</p>',
     '</h4></section></summary><div class="docblock"><p>原样返回该参数。</p>'),
    # 14. From boilerplate
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