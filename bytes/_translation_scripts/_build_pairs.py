#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build bytes/_translate_pairs.json from current bytes/ state (CRLF post-chrome).
Outputs flat [[old, new], ...] JSON consumable by replace_in_files.py.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CRLF = '\r\n'
SECTION = '§'  # § (U+00A7)
RSQUO = '’'   # ’ (U+2019) right single quotation mark


def crlf(*lines):
    return CRLF.join(lines)


def pairs_for_chrome():
    p = []
    # all.html: title + meta description
    p.append([
        '<meta name="description" content="List of all items in this crate"><title>List of all items in this crate</title>',
        '<meta name="description" content="本 crate 内所有条目列表"><title>本 crate 内所有条目列表</title>',
    ])
    # all.html: h1 "List of all items"
    p.append([
        '<div class="main-heading"><h1>List of all items</h1><rustdoc-toolbar></rustdoc-toolbar></div>',
        '<div class="main-heading"><h1>所有条目列表</h1><rustdoc-toolbar></rustdoc-toolbar></div>',
    ])
    # index.html sidebar Re-exports
    p.append([
        '<a href="#reexports" title="Re-exports">Re-exports</a>',
        '<a href="#reexports" title="Re-exports">重新导出</a>',
    ])
    return p


def pairs_for_index():
    p = []
    p.append(['<p>Provides abstractions for working with bytes.</p>',
              '<p>提供用于处理字节的抽象。</p>'])
    p.append([
        crlf('<p>The <code>bytes</code> crate provides an efficient byte buffer structure',
             '(<a href="struct.Bytes.html" title="struct bytes::Bytes"><code>Bytes</code></a>) and traits for working with buffer',
             'implementations (<a href="buf/trait.Buf.html" title="trait bytes::buf::Buf"><code>Buf</code></a>, <a href="buf/trait.BufMut.html" title="trait bytes::buf::BufMut"><code>BufMut</code></a>).</p>'),
        crlf('<p><code>bytes</code> crate 提供了一种高效的字节缓冲结构',
             '（<a href="struct.Bytes.html" title="struct bytes::Bytes"><code>Bytes</code></a>），以及用于处理缓冲实现',
             '的 trait（<a href="buf/trait.Buf.html" title="trait bytes::buf::Buf"><code>Buf</code></a>、<a href="buf/trait.BufMut.html" title="trait bytes::buf::BufMut"><code>BufMut</code></a>）。</p>'),
    ])
    p.append([
        crlf('<p><code>Bytes</code> is an efficient container for storing and operating on contiguous',
             'slices of memory. It is intended for use primarily in networking code, but',
             'could have applications elsewhere as well.</p>'),
        crlf('<p><code>Bytes</code> 是一个用于存储和操作连续内存切片的高效容器。',
             '它主要面向网络编程场景，但',
             '在其他场景下也同样适用。</p>'),
    ])
    p.append([
        crlf('<p><code>Bytes</code> values facilitate zero-copy network programming by allowing multiple',
             '<code>Bytes</code> objects to point to the same underlying memory. This is managed by',
             'using a reference count to track when the memory is no longer needed and can',
             'be freed.</p>'),
        crlf('<p><code>Bytes</code> 通过允许多个 <code>Bytes</code> 对象',
             '指向同一段底层内存来简化零拷贝网络编程。它通过引用计数',
             '来追踪内存何时不再需要，',
             '从而可以释放。</p>'),
    ])
    p.append([
        crlf('<p>A <code>Bytes</code> handle can be created directly from an existing byte store (such as <code>&amp;[u8]</code>',
             'or <code>Vec&lt;u8&gt;</code>), but usually a <code>BytesMut</code> is used first and written to. For',
             'example:</p>'),
        crlf('<p>可以直接从现有字节存储（如 <code>&amp;[u8]</code>',
             '或 <code>Vec&lt;u8&gt;</code>）构造 <code>Bytes</code> 句柄，但通常先使用 <code>BytesMut</code> 写入再冻结。例如：</p>'),
    ])
    p.append([
        crlf('<p>In the above example, only a single buffer of 1024 is allocated. The handles',
             '<code>a</code> and <code>b</code> will share the underlying buffer and maintain indices tracking',
             'the view into the buffer represented by the handle.</p>'),
        crlf('<p>上面的示例中只分配了一个 1024 大小的缓冲区。句柄',
             '<code>a</code> 和 <code>b</code> 共享该底层缓冲区，并通过索引',
             '维护各自所代表的缓冲区视图。</p>'),
    ])
    p.append([
        '<p>See the <a href="struct.Bytes.html" title="struct bytes::Bytes">struct docs</a> for more details.</p>',
        '<p>更多细节参见 <a href="struct.Bytes.html" title="struct bytes::Bytes">结构体文档</a>。</p>',
    ])
    p.append([
        crlf('<p>These two traits provide read and write access to buffers. The underlying',
             'storage may or may not be in contiguous memory. For example, <code>Bytes</code> is a',
             'buffer that guarantees contiguous memory, but a <a href="https://en.wikipedia.org/wiki/Rope_(data_structure)">rope</a> stores the bytes in',
             'disjoint chunks. <code>Buf</code> and <code>BufMut</code> maintain cursors tracking the current',
             'position in the underlying byte storage. When bytes are read or written, the',
             'cursor is advanced.</p>'),
        crlf('<p>这两个 trait 提供对缓冲区的读写访问。底层',
             '存储不一定在连续内存中。例如，<code>Bytes</code> 是保证内存连续的',
             '缓冲区，而 <a href="https://en.wikipedia.org/wiki/Rope_(data_structure)">rope（绳索）</a> 则将字节分散存储在',
             '不相邻的多个块中。<code>Buf</code> 和 <code>BufMut</code> 通过游标维护当前',
             '在底层字节存储中的位置；每当读取或写入字节时，',
             '游标都会推进。</p>'),
    ])
    p.append([
        crlf('<p>At first glance, it may seem that <code>Buf</code> and <code>BufMut</code> overlap in',
             'functionality with <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.Read.html" title="trait std::io::Read"><code>std::io::Read</code></a> and <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.Write.html" title="trait std::io::Write"><code>std::io::Write</code></a>. However, they',
             'serve different purposes. A buffer is the value that is provided as an',
             'argument to <code>Read::read</code> and <code>Write::write</code>. <code>Read</code> and <code>Write</code> may then',
             'perform a syscall, which has the potential of failing. Operations on <code>Buf</code>',
             'and <code>BufMut</code> are infallible.</p>'),
        crlf('<p>乍看之下，<code>Buf</code> 和 <code>BufMut</code> 在功能上似乎与',
             '<a href="https://doc.rust-lang.org/1.95.0/std/io/trait.Read.html" title="trait std::io::Read"><code>std::io::Read</code></a> 和 <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.Write.html" title="trait std::io::Write"><code>std::io::Write</code></a> 重叠。但二者',
             '用途不同。缓冲区（buffer）是作为参数',
             '传给 <code>Read::read</code> 和 <code>Write::write</code> 的值；<code>Read</code> 和 <code>Write</code>',
             '可能会触发系统调用（syscall），存在失败的可能。而 <code>Buf</code>',
             '和 <code>BufMut</code> 的操作则是不可失败的（infallible）。</p>'),
    ])
    return p


def pairs_for_struct_bytes():
    p = []
    p.append(['<p>A cheaply cloneable and sliceable chunk of contiguous memory.</p>',
              '<p>一段可廉价克隆、可切片访问的连续内存。</p>'])
    p.append([
        crlf('<p><code>Bytes</code> is an efficient container for storing and operating on contiguous',
             'slices of memory. It is intended for use primarily in networking code, but',
             'could have applications elsewhere as well.</p>'),
        crlf('<p><code>Bytes</code> 是一个用于存储和操作连续内存切片的高效容器。',
             '它主要面向网络编程场景，但',
             '在其他场景下也同样适用。</p>'),
    ])
    p.append([
        '<p><code>Bytes</code> values facilitate zero-copy network programming by allowing multiple\r\n<code>Bytes</code> objects to point to the same underlying memory.</p>',
        '<p><code>Bytes</code> 通过允许多个 <code>Bytes</code> 对象\r\n指向同一段底层内存来简化零拷贝网络编程。</p>',
    ])
    p.append([
        crlf('<p><code>Bytes</code> does not have a single implementation. It is an interface, whose',
             'exact behavior is implemented through dynamic dispatch in several underlying',
             'implementations of <code>Bytes</code>.</p>'),
        crlf('<p><code>Bytes</code> 并没有单一的具体实现。它是一个接口，',
             '其具体行为由若干 <code>Bytes</code> 底层实现',
             '通过动态分派来提供。</p>'),
    ])
    p.append(['<p>All <code>Bytes</code> implementations must fulfill the following requirements:</p>',
              '<p>所有 <code>Bytes</code> 实现都必须满足以下要求：</p>'])
    p.append([
        '<li>They are cheaply cloneable and thereby shareable between an unlimited amount\r\nof components, for example by modifying a reference count.</li>',
        '<li>可廉价克隆，从而能在任意数量的组件之间共享（例如通过修改引用计数实现）。</li>',
    ])
    p.append(['<li>Instances can be sliced to refer to a subset of the original buffer.</li>',
              '<li>可以切片，以引用原缓冲区的一个子集。</li>'])
    return p


def pairs_for_struct_bytesmut():
    p = []
    p.append(['<p>A unique reference to a contiguous slice of memory.</p>',
              '<p>对一段连续内存切片的独占引用。</p>'])
    p.append([
        crlf('<p><code>BytesMut</code> represents a unique view into a potentially shared memory region.',
             'Given the uniqueness guarantee, owners of <code>BytesMut</code> handles are able to',
             'mutate the memory.</p>'),
        crlf('<p><code>BytesMut</code> 表示对一段可能共享的内存区域的独占视图。',
             '凭借该独占性保证，<code>BytesMut</code> 句柄的持有者',
             '可以修改该内存。</p>'),
    ])
    p.append([
        crlf('<p><code>BytesMut</code> can be thought of as containing a <code>buf: Arc&lt;Vec&lt;u8&gt;&gt;</code>, an offset',
             'into <code>buf</code>, a slice length, and a guarantee that no other <code>BytesMut</code> for the',
             'same <code>buf</code> overlaps with its slice. That guarantee means that a write lock',
             'is not required.</p>'),
        crlf('<p>可以把 <code>BytesMut</code> 视为包含一个 <code>buf: Arc&lt;Vec&lt;u8&gt;&gt;</code>、其在 <code>buf</code> 中的偏移量、',
             '切片长度，并保证同一 <code>buf</code> 上没有其他 <code>BytesMut</code>',
             '与它的切片重叠。这条保证意味着',
             '不需要写锁。</p>'),
    ])
    p.append([
        f'<p><code>BytesMut</code>{RSQUO}s <code>BufMut</code> implementation will implicitly grow its buffer as\r\nnecessary. However, explicitly reserving the required space up-front before\r\na series of inserts will be more efficient.</p>',
        f'<p><code>BytesMut</code>{RSQUO}s <code>BufMut</code> 实现会在必要时隐式扩容。\r\n不过，若在一连串插入之前预先\r\n预留出所需空间，效率会更高。</p>',
    ])
    return p


def pairs_for_buf_index():
    p = []
    p.append(['<p>Utilities for working with buffers.</p>',
              '<p>缓冲区操作工具。</p>'])
    p.append([
        crlf('<p>A buffer is any structure that contains a sequence of bytes. The bytes may',
             'or may not be stored in contiguous memory. This module contains traits used',
             'to abstract over buffers as well as utilities for working with buffer types.</p>'),
        crlf('<p>缓冲区（buffer）是任何包含一段字节序列的结构。字节',
             '可能存储在连续内存中，也可能不连续。本模块提供了用于抽象缓冲区的 trait，',
             '以及用于处理缓冲区类型的工具。</p>'),
    ])
    p.append([
        crlf('<p>These are the two foundational traits for abstractly working with buffers.',
             'They can be thought as iterators for byte structures. They offer additional',
             'performance over <code>Iterator</code> by providing an API optimized for byte slices.</p>'),
        crlf('<p>这两个 trait 是抽象处理缓冲区的两个基础 trait。',
             '可以把它们视为字节结构的迭代器。它们通过提供面向字节切片优化的 API，',
             '在性能上优于 <code>Iterator</code>。</p>'),
    ])
    p.append([
        '<p>See <a href="trait.Buf.html" title="trait bytes::buf::Buf"><code>Buf</code></a> and <a href="trait.BufMut.html" title="trait bytes::buf::BufMut"><code>BufMut</code></a> for more details.</p>',
        '<p>更多细节请参见 <a href="trait.Buf.html" title="trait bytes::buf::Buf"><code>Buf</code></a> 和 <a href="trait.BufMut.html" title="trait bytes::buf::BufMut"><code>BufMut</code></a>。</p>',
    ])
    return p


def pairs_for_docblocks():
    p = []
    # Bytes::from_owner
    p.append([
        crlf('<div class="docblock"><p>Create <a href="struct.Bytes.html" title="struct bytes::Bytes">Bytes</a> with a buffer whose lifetime is controlled',
             'via an explicit owner.</p>',
             '<p>A common use case is to zero-copy construct from mapped memory.</p>'),
        crlf('<div class="docblock"><p>使用由显式所有者控制生命周期的缓冲区构造 <a href="struct.Bytes.html" title="struct bytes::Bytes">Bytes</a>。</p>',
             '<p>一个常见的用例是从内存映射中零拷贝构造。</p>'),
    ])
    # Bytes::copy_from_slice
    p.append(['<div class="docblock"><p>Creates <code>Bytes</code> instance from slice, by copying it.</p>' + CRLF + '</div>',
              '<div class="docblock"><p>通过复制切片内容创建一个 <code>Bytes</code> 实例。</p>' + CRLF + '</div>'])
    # Limit::into_inner
    p.append(['<div class="docblock"><p>Consumes this <code>Limit</code>, returning the underlying value.</p>' + CRLF + '</div>',
              '<div class="docblock"><p>消耗该 <code>Limit</code>，返回底层的值。</p>' + CRLF + '</div>'])
    # Limit::get_ref
    p.append([
        crlf('<div class="docblock"><p>Gets a reference to the underlying <code>BufMut</code>.</p>',
             '<p>It is inadvisable to directly write to the underlying <code>BufMut</code>.</p>',
             '</div>'),
        crlf('<div class="docblock"><p>获得底层 <code>BufMut</code> 的引用。</p>',
             '<p>不建议直接对底层 <code>BufMut</code> 进行写入。</p>',
             '</div>'),
    ])
    # Limit::get_mut
    p.append([
        crlf('<div class="docblock"><p>Gets a mutable reference to the underlying <code>BufMut</code>.</p>',
             '<p>It is inadvisable to directly write to the underlying <code>BufMut</code>.</p>',
             '</div>'),
        crlf('<div class="docblock"><p>获得底层 <code>BufMut</code> 的可变引用。</p>',
             '<p>不建议直接对底层 <code>BufMut</code> 进行写入。</p>',
             '</div>'),
    ])
    # Limit::limit (Note label translated)
    p.append([
        crlf('<div class="docblock"><p>Returns the maximum number of bytes that can be written</p>',
             f'<h5 id="note"><a class="doc-anchor" href="#note">{SECTION}</a>Note</h5>',
             '<p>If the inner <code>BufMut</code> has fewer bytes than indicated by this method then',
             'that is the actual number of available bytes.</p>',
             '</div>'),
        crlf('<div class="docblock"><p>返回可写入的最大字节数。</p>',
             f'<h5 id="note"><a class="doc-anchor" href="#note">{SECTION}</a>注意</h5>',
             '<p>如果底层 <code>BufMut</code> 可用的字节数少于本方法返回的值，',
             '则以实际可用字节数为准。</p>',
             '</div>'),
    ])
    # Limit::set_limit
    p.append([
        crlf('<div class="docblock"><p>Sets the maximum number of bytes that can be written.</p>',
             f'<h5 id="note-1"><a class="doc-anchor" href="#note-1">{SECTION}</a>Note</h5>',
             '<p>If the inner <code>BufMut</code> has fewer bytes than <code>lim</code> then that is the actual',
             'number of available bytes.</p>',
             '</div>'),
        crlf('<div class="docblock"><p>设置可写入的最大字节数。</p>',
             f'<h5 id="note-1"><a class="doc-anchor" href="#note-1">{SECTION}</a>注意</h5>',
             '<p>如果底层 <code>BufMut</code> 可用的字节数少于 <code>lim</code>，',
             '则以实际可用字节数为准。</p>',
             '</div>'),
    ])
    # Reader::get_mut
    p.append([
        crlf('<div class="docblock"><p>Gets a mutable reference to the underlying <code>Buf</code>.</p>',
             '<p>It is inadvisable to directly read from the underlying <code>Buf</code>.</p>',
             '</div>'),
        crlf('<div class="docblock"><p>获得底层 <code>Buf</code> 的可变引用。</p>',
             '<p>不建议直接从底层 <code>Buf</code> 进行读取。</p>',
             '</div>'),
    ])
    # Buf::chunks_vectored
    p.append([
        crlf('<div class="docblock"><p>Fills <code>dst</code> with potentially multiple slices starting at <code>self</code>’s',
             'current position.</p>',
             '<p>If the <code>Buf</code> is backed by disjoint slices of bytes, <code>chunk_vectored</code> enables',
             'fetching more than one slice at once. <code>dst</code> is a slice of <code>IoSlice</code>',
             'references, enabling the slice to be directly used with <a href="http://man7.org/linux/man-pages/man2/readv.2.html"><code>writev</code></a>',
             'without any further conversion. The sum of the lengths of all the',
             'buffers written to <code>dst</code> will be less than or equal to <code>Buf::remaining()</code>.</p>',
             '<p>The entries in <code>dst</code> will be overwritten, but the data <strong>contained</strong> by',
             'the slices <strong>will not</strong> be modified. The return value is the number of',
             'slices written to <code>dst</code>. If <code>Buf::remaining()</code> is non-zero, then this',
             'writes at least one non-empty slice to <code>dst</code>.</p>',
             '<p>This is a lower level function. Most operations are done with other',
             'functions.</p>',
             f'<h5 id="implementer-notes-3"><a class="doc-anchor" href="#implementer-notes-3">{SECTION}</a>Implementer notes</h5>',
             '<p>This function should never panic. Once the end of the buffer is reached,',
             'i.e., <code>Buf::remaining</code> returns 0, calls to <code>chunk_vectored</code> must return 0',
             'without mutating <code>dst</code>.</p>',
             '<p>Implementations should also take care to properly handle being called',
             'with <code>dst</code> being a zero length slice.</p>',
             '</div>'),
        crlf('<div class="docblock"><p>从 <code>self</code> 的当前位置开始，',
             '向 <code>dst</code> 中填充可能的多段切片。</p>',
             '<p>如果 <code>Buf</code> 由不相邻的字节切片支撑，<code>chunk_vectored</code> 允许',
             '一次性取出多段切片。<code>dst</code> 是一个 <code>IoSlice</code> 引用数组，',
             '其中的切片可直接配合 <a href="http://man7.org/linux/man-pages/man2/readv.2.html"><code>writev</code></a>',
             '使用而无需额外转换。所有写入 <code>dst</code> 的缓冲区',
             '长度之和应小于或等于 <code>Buf::remaining()</code>。</p>',
             '<p><code>dst</code> 中的元素会被覆盖，但切片<strong>包含</strong>的数据',
             '<strong>不会</strong>被修改。返回值是写入 <code>dst</code> 的切片个数。',
             '若 <code>Buf::remaining()</code> 非零，则本方法至少会向 <code>dst</code> 写入一段非空切片。</p>',
             '<p>这是一个底层函数，大多数操作应使用其他方法完成。</p>',
             f'<h5 id="implementer-notes-3"><a class="doc-anchor" href="#implementer-notes-3">{SECTION}</a>实现者须知</h5>',
             '<p>本方法绝不能 panic。一旦到达缓冲区末尾，',
             '即 <code>Buf::remaining</code> 返回 0，对 <code>chunk_vectored</code> 的调用必须返回 0，',
             '且不得修改 <code>dst</code>。</p>',
             '<p>实现还需注意正确处理 <code>dst</code> 为零长度切片的调用情形。</p>',
             '</div>'),
    ])
    # BufMut::put_slice
    p.append([
        crlf('<div class="docblock"><p>Transfer bytes into <code>self</code> from <code>src</code> and advance the cursor by the',
             'number of bytes written.</p>',
             '<p><code>self</code> must have enough remaining capacity to contain all of <code>src</code>.</p>'),
        crlf('<div class="docblock"><p>将 <code>src</code> 中的字节传入 <code>self</code>，并将游标',
             '前移已写入的字节数。</p>',
             '<p><code>self</code> 的剩余容量必须足以容纳整个 <code>src</code>。</p>'),
    ])
    # BufMut::put_bytes
    p.append([
        crlf('<div class="docblock"><p>Put <code>cnt</code> bytes <code>val</code> into <code>self</code>.</p>',
             '<p>Logically equivalent to calling <code>self.put_u8(val)</code> <code>cnt</code> times, but may work faster.</p>',
             '<p><code>self</code> must have at least <code>cnt</code> remaining capacity.</p>'),
        crlf('<div class="docblock"><p>向 <code>self</code> 写入 <code>cnt</code> 个字节 <code>val</code>。</p>',
             '<p>逻辑上等价于连续调用 <code>self.put_u8(val)</code> 共 <code>cnt</code> 次，但可能更快。</p>',
             '<p><code>self</code> 的剩余容量必须至少为 <code>cnt</code>。</p>'),
    ])
    return p


def main():
    all_pairs = []
    all_pairs.extend(pairs_for_chrome())
    all_pairs.extend(pairs_for_index())
    all_pairs.extend(pairs_for_struct_bytes())
    all_pairs.extend(pairs_for_struct_bytesmut())
    all_pairs.extend(pairs_for_buf_index())
    all_pairs.extend(pairs_for_docblocks())

    # Dedup
    seen = set()
    unique = []
    for old, new in all_pairs:
        # replace_in_files.py reads files in text mode with universal newlines,
        # so \r\n in the file becomes \n in the script's string. Normalize both
        # old and new to LF to keep the search key matching.
        old_n = old.replace('\r\n', '\n').replace('\r', '\n')
        new_n = new.replace('\r\n', '\n').replace('\r', '\n')
        if old_n in seen:
            continue
        seen.add(old_n)
        unique.append([old_n, new_n])

    out = os.path.join(HERE, '_pairs_flat.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(unique, f, ensure_ascii=False)
    print(f"Wrote {len(unique)} flat pairs to {out}")


if __name__ == '__main__':
    main()