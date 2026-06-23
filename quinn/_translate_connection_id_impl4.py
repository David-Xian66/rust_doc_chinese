"""Translate final 10 untranslated docblocks in quinn/struct.ConnectionId.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/struct.ConnectionId.html'

TRANSLATIONS = [
    # 1. rchunks_exact_mut (long with example)
    ('<p>Returns an iterator over <code>chunk_size</code> elements of the slice at a time, starting at the end\nof the slice.</p>\n<p>The chunks are mutable slices, and do not overlap. If <code>chunk_size</code> does not divide the\nlength of the slice, then the last up to <code>chunk_size-1</code> elements will be omitted and can be\nretrieved from the <code>into_remainder</code> function of the iterator.</p>\n<p>Due to each chunk having exactly <code>chunk_size</code> elements, the compiler can often optimize the\nresulting code better than in the case of <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.chunks_mut" title="method slice::chunks_mut"><code>chunks_mut</code></a>.</p>\n<p>See <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.rchunks_mut" title="method slice::rchunks_mut"><code>rchunks_mut</code></a> for a variant of this iterator that also returns the remainder as a\nsmaller chunk, and <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.chunks_exact_mut" title="method slice::chunks_exact_mut"><code>chunks_exact_mut</code></a> for the same iterator but starting at the beginning\nof the slice.</p>\n<p>If your <code>chunk_size</code> is a constant, consider using <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.as_rchunks_mut" title="method slice::as_rchunks_mut"><code>as_rchunks_mut</code></a> instead, which will\ngive references to arrays of exactly that length, rather than slices.</p>\n<h5 id="panics-14"><a class="doc-anchor" href="#panics-14">§</a>Panics</h5>\n<p>Panics if <code>chunk_size</code> is zero.</p>\n<h5 id="examples-48"><a class="doc-anchor" href="#examples-48">§</a>Examples</h5>',
     '<p>返回一个迭代器，每次遍历切片的 <code>chunk_size</code> 个元素，从切片末尾开始。</p>\n<p>各块为可变切片且互不重叠。若 <code>chunk_size</code> 不能整除切片长度，开头最多 <code>chunk_size-1</code> 个元素将被略过，可通过迭代器的 <code>into_remainder</code> 函数取回。</p>\n<p>由于每块恰好包含 <code>chunk_size</code> 个元素，编译器通常能比 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.chunks_mut" title="method slice::chunks_mut"><code>chunks_mut</code></a> 更优化所生成的代码。</p>\n<p>若希望迭代器将剩余元素也作为较小的块返回，请参阅 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.rchunks_mut" title="method slice::rchunks_mut"><code>rchunks_mut</code></a>；若希望从切片开头开始，请参阅 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.chunks_exact_mut" title="method slice::chunks_exact_mut"><code>chunks_exact_mut</code></a>。</p>\n<p>若 <code>chunk_size</code> 为编译期常量，建议改用 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.as_rchunks_mut" title="method slice::as_rchunks_mut"><code>as_rchunks_mut</code></a>。</p>\n<h5 id="panics-14"><a class="doc-anchor" href="#panics-14">§</a>Panics</h5>\n<p>若 <code>chunk_size</code> 为零则 panic。</p>\n<h5 id="examples-48"><a class="doc-anchor" href="#examples-48">§</a>示例</h5>'),
    # 2. as_slice
    ('<p>Returns the same slice <code>&amp;[T]</code>.</p>\n<p>This method is redundant when used directly on <code>&amp;[T]</code>, but\nit helps dereferencing other “container” types to slices,\nfor example <code>Box&lt;[T]&gt;</code> or <code>Arc&lt;[T]&gt;</code>.</p>',
     '<p>返回同一切片 <code>&amp;[T]</code>。</p>\n<p>直接在 <code>&amp;[T]</code> 上调用此方法属于冗余操作，但其有助于把其他“容器”类型解引用为切片，例如 <code>Box&lt;[T]&gt;</code> 或 <code>Arc&lt;[T]&gt;</code>。</p>'),
    # 3. as_mut_slice
    ('<p>Returns the same slice <code>&amp;mut [T]</code>.</p>\n<p>This method is redundant when used directly on <code>&amp;mut [T]</code>, but\nit helps dereferencing other “container” types to slices,\nfor example <code>Box&lt;[T]&gt;</code> or <code>MutexGuard&lt;[T]&gt;</code>.</p>',
     '<p>返回同一可变切片 <code>&amp;mut [T]</code>。</p>\n<p>直接在 <code>&amp;mut [T]</code> 上调用此方法属于冗余操作，但其有助于把其他“容器”类型解引用为切片，例如 <code>Box&lt;[T]&gt;</code> 或 <code>MutexGuard&lt;[T]&gt;</code>。</p>'),
    # 4. to_vec
    ('<p>Copies <code>self</code> into a new <code>Vec</code>.</p>\n<h5 id="examples-123"><a class="doc-anchor" href="#examples-123">§</a>Examples</h5>',
     '<p>将 <code>self</code> 拷贝到一个新的 <code>Vec</code> 中。</p>\n<h5 id="examples-123"><a class="doc-anchor" href="#examples-123">§</a>示例</h5>'),
    # 5. to_vec_in
    ('<p>Copies <code>self</code> into a new <code>Vec</code> with an allocator.</p>\n<h5 id="examples-124"><a class="doc-anchor" href="#examples-124">§</a>Examples</h5>',
     '<p>使用指定分配器，将 <code>self</code> 拷贝到一个新的 <code>Vec</code> 中。</p>\n<h5 id="examples-124"><a class="doc-anchor" href="#examples-124">§</a>示例</h5>'),
    # 6. concat
    ('<p>Flattens a slice of <code>T</code> into a single value <code>Self::Output</code>.</p>\n<h5 id="examples-126"><a class="doc-anchor" href="#examples-126">§</a>Examples</h5>',
     '<p>将 <code>T</code> 类型的切片扁平化为单个值 <code>Self::Output</code>。</p>\n<h5 id="examples-126"><a class="doc-anchor" href="#examples-126">§</a>示例</h5>'),
    # 7. join
    ('<p>Flattens a slice of <code>T</code> into a single value <code>Self::Output</code>, placing a\ngiven separator between each.</p>\n<h5 id="examples-127"><a class="doc-anchor" href="#examples-127">§</a>Examples</h5>',
     '<p>将 <code>T</code> 类型的切片扁平化为单个值 <code>Self::Output</code>，并在每两个相邻元素之间插入给定的分隔符。</p>\n<h5 id="examples-127"><a class="doc-anchor" href="#examples-127">§</a>示例</h5>'),
    # 8. connect (deprecated)
    ('<p>Flattens a slice of <code>T</code> into a single value <code>Self::Output</code>, placing a\ngiven separator between each.</p>\n<h5 id="examples-128"><a class="doc-anchor" href="#examples-128">§</a>Examples</h5>',
     '<p>将 <code>T</code> 类型的切片扁平化为单个值 <code>Self::Output</code>，并在每两个相邻元素之间插入给定的分隔符。</p>\n<h5 id="examples-128"><a class="doc-anchor" href="#examples-128">§</a>示例</h5>'),
    # 9. From impl
    ('</h4></section></summary><div class="docblock"><p>Returns the argument unchanged.</p>',
     '</h4></section></summary><div class="docblock"><p>原样返回该参数。</p>'),
    # 10. From boilerplate
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