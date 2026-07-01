"""Batch 7: translate remaining untranslated top-level paragraphs and remaining methods."""
import os, re

TOKIO_ROOT = 'D:/Administrator/Documents/Code/rust_doc_all/tokio'

def b(s):
    return s.replace('\n', '\r\n').encode('utf-8')

def c(s):
    return s.replace('\n', '\r\n').encode('utf-8')

# Manual pairs - each is exact byte match
PAIRS = [
    # ====== BufStream.html remaining ======
    (b('<p>Wraps a type in both <code>BufWriter</code> and <code>BufReader</code>.\n'
      'See the documentation for those types and <code>BufStream</code> for\n'
      'details.</p>'),
     c('<p>将一个类型同时包装为 <code>BufWriter</code> 和 <code>BufReader</code>。\n'
       '有关详情，请参见这些类型和 <code>BufStream</code> 的文档。</p>')),
    (b('<p>Creates a <code>BufStream</code> with the specified <code>BufReader</code>\n'
      'capacity and <code>BufWriter</code> capacity. See the documentation for those\n'
      'types and <code>BufStream</code> for details.</p>'),
     c('<p>使用指定的 <code>BufReader</code> 容量和 <code>BufWriter</code> 容量\n'
       '创建一个 <code>BufStream</code>。有关详情，请参见这些类型和 <code>BufStream</code> 的文档。</p>')),

    # ====== SimplexStream.html new_unsplit ======
    (b('<p>Creates unidirectional buffer that acts like in memory pipe.\n'
      'To create split version with separate reader and writer you can use\n'
      'simplex function.\n'
      'The max_buf_size argument is the maximum amount of bytes that can be\n'
      'written to a buffer before the it returns <code>Poll::Pending</code>.</p>'),
     c('<p>创建一个表现得像内存管道的单向缓冲区。\n'
       '若要创建带有独立 reader 和 writer 的拆分版本，可以使用 simplex 函数。\n'
       '<code>max_buf_size</code> 参数是缓冲区在返回 <code>Poll::Pending</code>\n'
       '之前可写入的最大字节数。</p>')),

    # ====== AsyncBufReadExt.html read_line, fill_buf, consume ======
    (b('<p>Reads all bytes until a newline (the 0xA byte) is reached, and append\n'
      'them to the provided buffer.</p>'),
     c('<p>读取所有字节直到遇到换行符（0xA 字节），并将它们追加到提供的缓冲区中。</p>')),
    (b('<p>Returns the contents of the internal buffer, filling it with more data\n'
      'from the inner reader if it is empty.</p>'),
     c('<p>返回内部缓冲区的内容，如果为空则从内部 reader 填充更多数据。</p>')),
    (b('<p>This function is a lower-level call. It needs to be paired with the\n'
      '<code>consume</code> method to function properly.</p>'),
     c('<p>此函数是一个较低级别的调用。它需要与 <code>consume</code> 方法配合使用才能正常工作。</p>')),
    (b('<p>When calling this method, none of the contents will be [\xe2\x80\x9c"]read[\xe2\x80\x9d"] in the\n'
      'sense that later calls to <code>read</code> will not return the same\n'
      'contents.</p>'),
     c('<p>调用此方法时，内容不会被"读取"，因为后续对 <code>read</code> 的调用\n'
       '不会返回相同的内容。</p>')),
    (b('<p>Tells this buffer that <code>amt</code> bytes have been consumed from the\n'
      'buffer, so they should no longer be returned in calls to <code>read</code>.\n'
      'This function is a lower-level call. It needs to be paired with the\n'
      '<code>fill_buf</code> method to function properly. This function does\n'
      'not perform any I/O, it simply informs this object that some data has\n'
      'been consumed.</p>'),
     c('<p>告知此缓冲区 <code>amt</code> 字节已从缓冲区消费，因此在后续\n'
       '<code>read</code> 调用中不应再返回这些字节。此函数是一个较低级别的调用。\n'
       '它需要与 <code>fill_buf</code> 方法配合使用才能正常工作。\n'
       '此函数不执行任何 I/O，只是通知此对象某些数据已被消费。</p>')),

    # ====== AsyncReadExt.html read, read_buf, read_exact, read_to_end, read_to_string ======
    (b('<p>Pulls some bytes from this source into the specified buffer, returning\n'
      'how many bytes were read.</p>'),
     c('<p>从此源读取一些字节到指定的缓冲区，返回读取的字节数。</p>')),
    (b('<p>Pulls some bytes from this source into the specified buffer, advancing\n'
      'the buffer\xe2\x80\x99s internal cursor.</p>'),
     c('<p>从此源读取一些字节到指定的缓冲区，并推进缓冲区的内部游标。</p>')),
    (b('<p>Reads the exact number of bytes required to fill <code>buf</code>.</p>'),
     c('<p>读取填满 <code>buf</code> 所需的精确字节数。</p>')),
    (b('<p>Reads all bytes until EOF in this source, placing them into <code>buf</code>.</p>'),
     c('<p>从此源读取所有字节直到 EOF，并将它们放入 <code>buf</code>。</p>')),
    (b('<p>Reads all bytes until EOF in this source, placing them into <code>buf</code>\n'
      'and appending to the string.</p>'),
     c('<p>从此源读取所有字节直到 EOF，将它们放入 <code>buf</code> 并追加到字符串。</p>')),

    # ====== AsyncSeekExt.html seek ======
    (b('<p>Seeks to an offset, in bytes, in a stream.</p>'),
     c('<p>在流中寻找给定的字节偏移量。</p>')),

    # ====== AsyncWriteExt.html write, write_all, flush, write_vectored, write_i64 ======
    (b('<p>Writes a buffer into this writer, returning how many bytes were written.</p>'),
     c('<p>将缓冲区写入此 writer，返回写入的字节数。</p>')),
    (b('<p>Attempts to write an entire buffer into this writer.</p>'),
     c('<p>尝试将整个缓冲区写入此 writer。</p>')),
    (b('<p>Flushes this output stream, ensuring all intermediately buffered contents\n'
      'reach their destination.</p>'),
     c('<p>刷新此输出流，确保所有中间缓冲的内容到达目的地。</p>')),
    (b('<p>Like <code>write</code>, except that it writes from a slice of buffers.</p>'),
     c('<p>与 <code>write</code> 类似，但从缓冲区切片中写入。</p>')),

    # write_i64 (the rare 'an signed' form)
    (b('<p>Writes an signed 64-bit integer in big-endian order to the underlying\n'
      'writer.</p>'),
     c('<p>以大端字节序将一个有符号 64 位整数写入底层 writer。</p>')),

    # ====== top-level attr.main.html ======
    (b('<p>To use the multi-threaded runtime, the macro can be configured using</p>'),
     c('<p>要使用多线程运行时，可通过以下方式配置该宏：</p>')),
    (b('<p>Note: The multi-threaded runtime requires the <code>rt-multi-thread</code> feature\n'
      'flag.</p>'),
     c('<p>注意：多线程运行时需要 <code>rt-multi-thread</code> 特性标志。</p>')),
    (b('<p>To use the single-threaded runtime known as the <code>current_thread</code> runtime,\n'
      'the macro can be configured using</p>'),
     c('<p>要使用称为 <code>current_thread</code> 运行时的单线程运行时，可通过以下方式配置该宏：</p>')),
    (b('<p>This option is only compatible with the <code>current_thread</code> runtime.</p>'),
     c('<p>此选项仅与 <code>current_thread</code> 运行时兼容。</p>')),

    # ====== macro.join.html remaining ======
    (b('<p>Waits on multiple concurrent branches, returning when all branches\n'
      'complete.</p>'),
     c('<p>等待多个并发分支，直到所有分支完成才返回。</p>')),
    (b('<p>When working with async expressions returning <code>Result</code>, <code>join!</code> will wait\n'
      'for all branches complete regardless if any complete with <code>Err</code>. Use\n'
      '<a href="macro.try_join.html" title="macro tokio::try_join"><code>try_join!</code></a> to return early when <code>Err</code> is encountered.</p>'),
     c('<p>当使用返回 <code>Result</code> 的 async 表达式时，<code>join!</code> 会等待\n'
       '所有分支完成，无论是否有分支以 <code>Err</code> 完成。若想在遇到 <code>Err</code> 时提前返回，请使用\n'
       '<a href="macro.try_join.html" title="macro tokio::try_join"><code>try_join!</code></a>。</p>')),
    (b('<p>By running all async expressions on the current task, the expressions are\n'
      'able to run concurrently but not in parallel. This means all\n'
      'expressions are run on the same thread and if one branch blocks the thread,\n'
      'all other expressions will be unable to continue. If parallelism is\n'
      'required, spawn each async expression using\n'
      '<a href="task/fn.spawn.html" title="fn tokio::task::spawn"><code>tokio::spawn</code></a>.</p>'),
     c('<p>由于所有 async 表达式都在当前任务上运行，这些表达式能够并发运行但不能并行执行。\n'
       '这意味着所有表达式都在同一线程上运行，如果一个分支阻塞了该线程，\n'
       '所有其他表达式都将无法继续。如果需要并行执行，请使用\n'
       '<a href="task/fn.spawn.html" title="fn tokio::task::spawn"><code>tokio::spawn</code></a>\n'
       '派生每个 async 表达式。</p>')),
    (b('<p>By default, <code>join!</code>\xe2\x80\x99s generated future rotates which contained\n'
      'future is polled first whenever it is woken.</p>'),
     c('<p>默认情况下，<code>join!</code> 生成的 future 在每次被唤醒时轮流选择最先 poll 的 future。</p>')),
    (b('<p>This behavior can be overridden by adding <code>biased;</code> to the beginning of the\n'
      'macro usage. See the examples for details. This will cause join to poll\n'
      'the futures in the order they appear from top to bottom.</p>'),
     c('<p>可以通过在宏用法开头添加 <code>biased;</code> 来覆盖此行为。详情请参见示例。\n'
       '这会让 join 按从上到下的顺序 poll future。</p>')),

    # ====== macro.select.html remaining ======
    (b('<p>Waits on multiple concurrent branches, returning when the first branch\n'
      'completes, cancelling the remaining branches.</p>'),
     c('<p>等待多个并发分支，当第一个分支完成时返回，并取消其余分支。</p>')),
    (b('<p><code>select!</code> can also use the <code>else</code> branch to run code when no branch\n'
      'matched, and the <code>if</code> guard on a branch to conditionally check whether that\n'
      'branch is eligible to be selected.</p>'),
     c('<p><code>select!</code> 还可以使用 <code>else</code> 分支在没有任何分支匹配时运行代码，\n'
       '并使用 <code>if</code> 守卫有条件地检查某个分支是否有资格被选中。</p>')),

    # ====== macro.try_join.html remaining ======
    (b('<p>Waits on multiple concurrent branches, returning when all branches\n'
      'complete with <code>Ok(_)</code> or on the first <code>Err(_)</code>.</p>'),
     c('<p>等待多个并发分支，直到所有分支以 <code>Ok(_)</code> 完成，或在第一个 <code>Err(_)</code> 时返回。</p>')),
    (b('<p>Similar to <a href="macro.join.html" title="macro tokio::join"><code>join!</code></a>, the <code>try_join!</code> macro takes a list of async\n'
      'expressions and evaluates them concurrently on the same task. Each async\n'
      'expression evaluates to a future and the futures from each expression are\n'
      'multiplexed on the current task. The <code>try_join!</code> macro returns when all\n'
      'branches return with <code>Ok</code>, or on the first <code>Err</code> returned by one of the branches.</p>'),
     c('<p>与 <a href="macro.join.html" title="macro tokio::join"><code>join!</code></a> 类似，<code>try_join!</code> 宏接受一个 async 表达式列表，\n'
       '并在同一任务上并发地执行它们。每个 async 表达式求值为一个 future，\n'
       '来自每个表达式的 future 在当前任务上多路复用。<code>try_join!</code> 宏在所有分支返回 <code>Ok</code> 时返回，\n'
       '或在某个分支返回第一个 <code>Err</code> 时返回。</p>')),
    (b('<p>By running all async expressions on the current task, the expressions are\n'
      'able to run concurrently but not in parallel. This means all\n'
      'expressions are run on the same thread and if one branch blocks the thread,\n'
      'all other expressions will be unable to continue. If parallelism is\n'
      'required, spawn each async expression using\n'
      '<a href="task/fn.spawn.html" title="fn tokio::task::spawn"><code>tokio::spawn</code></a>.</p>'),
     c('<p>由于所有 async 表达式都在当前任务上运行，这些表达式能够并发运行但不能并行执行。\n'
       '这意味着所有表达式都在同一线程上运行，如果一个分支阻塞了该线程，\n'
       '所有其他表达式都将无法继续。如果需要并行执行，请使用\n'
       '<a href="task/fn.spawn.html" title="fn tokio::task::spawn"><code>tokio::spawn</code></a>\n'
       '派生每个 async 表达式。</p>')),
    (b('<p>By default, <code>try_join!</code>\xe2\x80\x99s generated future rotates which\n'
      'contained future is polled first whenever it is woken.</p>'),
     c('<p>默认情况下，<code>try_join!</code> 生成的 future 在每次被唤醒时轮流选择最先 poll 的 future。</p>')),
    (b('<p>This behavior can be overridden by adding <code>biased;</code> to the beginning of the\n'
      'macro usage. See the examples for details. This will cause try_join to poll\n'
      'the futures in the order they appear from top to bottom.</p>'),
     c('<p>可以通过在宏用法开头添加 <code>biased;</code> 来覆盖此行为。详情请参见示例。\n'
       '这会让 try_join 按从上到下的顺序 poll future。</p>')),
]


def main():
    hits = 0
    modified = 0
    missed_pairs = []
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
                    local_hits += 1
            if new != raw:
                with open(path, 'wb') as fh:
                    fh.write(new)
                modified += 1
                hits += local_hits

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
            missed_pairs.append(old[:80].decode('utf-8', errors='replace'))

    print(f'Modified files: {modified}')
    print(f'Pair matches (total): {hits}')
    print(f'Pairs never applied: {len(missed_pairs)}')
    for m in missed_pairs[:20]:
        print(f'  {m!r}')


if __name__ == '__main__':
    main()