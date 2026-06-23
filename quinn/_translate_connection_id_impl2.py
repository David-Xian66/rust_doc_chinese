"""Translate remaining 55 untranslated docblocks in quinn/struct.ConnectionId.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/struct.ConnectionId.html'

TRANSLATIONS = [
    # 1. buf_get (impl Buf)
    ('<p>Constructs cid by reading <code>len</code> bytes from a <code>Buf</code></p>',
     '<p>通过从 <code>Buf</code> 读取 <code>len</code> 个字节来构造 cid</p>'),
    # 2. advance
    ('<p>Callers need to assure that <code>buf.remaining() &gt;= len</code></p>',
     '<p>调用者需要保证 <code>buf.remaining() &gt;= len</code></p>'),
    # 3. is_ascii (alt impl, same name)
    ('<p>If this slice <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.is_ascii" title="method slice::is_ascii"><code>is_ascii</code></a>, returns it as a slice of\nASCII characters. Otherwise, returns <code>None</code>.</p>',
     '<p>若此切片 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.is_ascii" title="method slice::is_ascii"><code>is_ascii</code></a>，则将其作为 ASCII 字符切片返回；否则返回 <code>None</code>。</p>'),
    # 4. is_empty
    ('<p>Returns <code>true</code> if the slice has a length of 0.</p>',
     '<p>若切片长度为 0 则返回 <code>true</code>。</p>'),
    # 5. first
    ('<p>Returns the first element of the slice, or <code>None</code> if it is empty.</p>',
     '<p>返回切片的第一个元素；若切片为空则返回 <code>None</code>。</p>'),
    # 6. first_mut
    ('<p>Returns a mutable reference to the first element of the slice, or <code>None</code> if it is empty.</p>',
     '<p>返回切片第一个元素的可变引用；若切片为空则返回 <code>None</code>。</p>'),
    # 7. split_first
    ('<p>Returns the first and all the rest of the elements of the slice, or <code>None</code> if it is empty.</p>',
     '<p>返回第一个元素以及切片中剩余的所有元素；若切片为空则返回 <code>None</code>。</p>'),
    # 8. split_first_mut
    ('<p>Returns the first and all the rest of the elements of the slice, or <code>None</code> if it is empty.</p>',
     '<p>返回第一个元素以及切片中剩余元素的可变引用；若切片为空则返回 <code>None</code>。</p>'),
    # 9. split_last
    ('<p>Returns the last and all the rest of the elements of the slice, or <code>None</code> if it is empty.</p>',
     '<p>返回最后一个元素以及切片中剩余的所有元素；若切片为空则返回 <code>None</code>。</p>'),
    # 10. split_last_mut
    ('<p>Returns the last and all the rest of the elements of the slice, or <code>None</code> if it is empty.</p>',
     '<p>返回最后一个元素以及切片中剩余元素的可变引用；若切片为空则返回 <code>None</code>。</p>'),
    # 11. last
    ('<p>Returns the last element of the slice, or <code>None</code> if it is empty.</p>',
     '<p>返回切片的最后一个元素；若切片为空则返回 <code>None</code>。</p>'),
    # 12. last_mut
    ('<p>Returns a mutable reference to the last item in the slice, or <code>None</code> if it is empty.</p>',
     '<p>返回切片最后一个元素的可变引用；若切片为空则返回 <code>None</code>。</p>'),
    # 13. first_chunk
    ('<p>Returns an array reference to the first <code>N</code> items in the slice.</p>\n<p>If the slice is not at least <code>N</code> in length, this will return <code>None</code>.</p>',
     '<p>返回切片前 <code>N</code> 个元素的数组引用。</p>\n<p>若切片长度小于 <code>N</code>，则返回 <code>None</code>。</p>'),
    # 14. first_chunk_mut
    ('<p>Returns a mutable array reference to the first <code>N</code> items in the slice.</p>\n<p>If the slice is not at least <code>N</code> in length, this will return <code>None</code>.</p>',
     '<p>返回切片前 <code>N</code> 个元素的可变数组引用。</p>\n<p>若切片长度小于 <code>N</code>，则返回 <code>None</code>。</p>'),
    # 15. split_first_chunk
    ('<p>Returns an array reference to the first <code>N</code> items in the slice and the remaining slice.</p>\n<p>If the slice is not at least <code>N</code> in length, this will return <code>None</code>.</p>',
     '<p>返回切片前 <code>N</code> 个元素的数组引用以及剩余切片。</p>\n<p>若切片长度小于 <code>N</code>，则返回 <code>None</code>。</p>'),
    # 16. split_first_chunk_mut
    ('<p>Returns a mutable array reference to the first <code>N</code> items in the slice and the remaining\nslice.</p>\n<p>If the slice is not at least <code>N</code> in length, this will return <code>None</code>.</p>',
     '<p>返回切片前 <code>N</code> 个元素的可变数组引用以及剩余切片。</p>\n<p>若切片长度小于 <code>N</code>，则返回 <code>None</code>。</p>'),
    # 17. split_last_chunk
    ('<p>Returns an array reference to the last <code>N</code> items in the slice and the remaining slice.</p>\n<p>If the slice is not at least <code>N</code> in length, this will return <code>None</code>.</p>',
     '<p>返回切片末尾 <code>N</code> 个元素的数组引用以及剩余切片。</p>\n<p>若切片长度小于 <code>N</code>，则返回 <code>None</code>。</p>'),
    # 18. split_last_chunk_mut
    ('<p>Returns a mutable array reference to the last <code>N</code> items in the slice and the remaining\nslice.</p>\n<p>If the slice is not at least <code>N</code> in length, this will return <code>None</code>.</p>',
     '<p>返回切片末尾 <code>N</code> 个元素的可变数组引用以及剩余切片。</p>\n<p>若切片长度小于 <code>N</code>，则返回 <code>None</code>。</p>'),
    # 19. last_chunk
    ('<p>Returns an array reference to the last <code>N</code> items in the slice.</p>\n<p>If the slice is not at least <code>N</code> in length, this will return <code>None</code>.</p>',
     '<p>返回切片末尾 <code>N</code> 个元素的数组引用。</p>\n<p>若切片长度小于 <code>N</code>，则返回 <code>None</code>。</p>'),
    # 20. last_chunk_mut
    ('<p>Returns a mutable array reference to the last <code>N</code> items in the slice.</p>\n<p>If the slice is not at least <code>N</code> in length, this will return <code>None</code>.</p>',
     '<p>返回切片末尾 <code>N</code> 个元素的可变数组引用。</p>\n<p>若切片长度小于 <code>N</code>，则返回 <code>None</code>。</p>'),
    # 21. get_mut (alt impl)
    ('<p>Returns a mutable reference to an element or subslice depending on the\ntype of the index.</p>\n<p>See <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.get" title="method slice::get"><code>get</code></a> for a full description.</p>',
     '<p>依据索引类型返回对一个元素或子切片的可变引用。</p>\n<p>完整说明请参阅 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.get" title="method slice::get"><code>get</code></a>。</p>'),
    # 22. array_windows (alt impl)
    ('<p>Returns an iterator over all contiguous windows of length\n<code>size</code>. The windows overlap. If the slice is shorter than\n<code>size</code>, the iterator returns no values.</p>\n<p>If <code>size</code> is zero, the iterator behaves like <code>iter()</code>, yielding\nthe original slice as a single window. If <code>size</code> is <code>N</code> (the\n<a href="https://doc.rust-lang.org/1.95.0/core/primitive.array.html#impl-Array-%3Cconst-N%3E-for-T" title="type core::primitive::Array">size of the array</a>) the iterator yields\n<code>len - N + 1</code> windows of size <code>N</code>. If <code>size</code> is greater than the\nlength of the slice, the iterator yields no values.</p>\n<h5 id="panics"><a class="doc-anchor" href="#panics">§</a>Panics</h5>\n<p>Panics if <code>size</code> is zero.</p>',
     '<p>返回一个迭代器，遍历长度为 <code>size</code> 的所有连续窗口。各窗口相互重叠。若切片短于 <code>size</code>，则迭代器不产生任何元素。</p>\n<p>若 <code>size</code> 为零，迭代器行为类似 <code>iter()</code>，仅将原切片作为单个窗口产出。若 <code>size</code> 为 <code>N</code>（即<a href="https://doc.rust-lang.org/1.95.0/core/primitive.array.html#impl-Array-%3Cconst-N%3E-for-T" title="type core::primitive::Array">数组的大小</a>），则迭代器产出 <code>len - N + 1</code> 个大小为 <code>N</code> 的窗口。若 <code>size</code> 大于切片长度，则迭代器不产生任何值。</p>\n<h5 id="panics"><a class="doc-anchor" href="#panics">§</a>Panics</h5>\n<p>若 <code>size</code> 为零则 panic。</p>'),
    # 23. chunks
    ('<p>Returns an iterator over <code>chunk_size</code> elements of the slice at a time, starting at the\nbeginning of the slice.</p>\n<p>The first chunk returned by the iterator will contain the first <code>chunk_size</code> elements of\nthe slice; the second chunk will contain the next <code>chunk_size</code> elements; and so on until the\nfinal chunk, which will contain the remaining elements, less than <code>chunk_size</code>.</p>\n<p>If <code>chunk_size</code> is 0, the iterator behaves like <code>iter()</code>, yielding the original slice as a\nsingle chunk. If <code>chunk_size</code> is greater than the length of the slice, the iterator yields\nno values.</p>',
     '<p>返回一个迭代器，每次遍历切片的 <code>chunk_size</code> 个元素，从切片开头开始。</p>\n<p>迭代器返回的第一个块包含切片的前 <code>chunk_size</code> 个元素；第二个块包含接下来的 <code>chunk_size</code> 个元素；依此类推，直到最后一个块包含少于 <code>chunk_size</code> 个的剩余元素。</p>\n<p>若 <code>chunk_size</code> 为 0，则迭代器行为类似 <code>iter()</code>，将原切片作为单个块产出。若 <code>chunk_size</code> 大于切片长度，则迭代器不产生任何值。</p>'),
    # 24. chunks_mut
    ('<p>Returns an iterator over <code>chunk_size</code> elements of the slice at a time, starting at the\nbeginning of the slice.</p>\n<p>The first chunk returned by the iterator will contain the first <code>chunk_size</code> elements of\nthe slice; the second chunk will contain the next <code>chunk_size</code> elements; and so on until the\nfinal chunk, which will contain the remaining elements, less than <code>chunk_size</code>.</p>\n<p>If <code>chunk_size</code> is 0, the iterator behaves like <code>chunks_mut(0)</code>, yielding the original slice\nas a single chunk. If <code>chunk_size</code> is greater than the length of the slice, the iterator\nyields no values.</p>',
     '<p>返回一个迭代器，每次遍历切片的 <code>chunk_size</code> 个元素，从切片开头开始。</p>\n<p>迭代器返回的第一个块包含切片的前 <code>chunk_size</code> 个元素；第二个块包含接下来的 <code>chunk_size</code> 个元素；依此类推，直到最后一个块包含少于 <code>chunk_size</code> 个的剩余元素。</p>\n<p>若 <code>chunk_size</code> 为 0，则迭代器行为类似 <code>chunks_mut(0)</code>，将原切片作为单个块产出。若 <code>chunk_size</code> 大于切片长度，则迭代器不产生任何值。</p>'),
    # 25. chunks_exact
    ('<p>Returns an iterator over <code>chunk_size</code> elements of the slice at a time, starting at the\nbeginning of the slice.</p>\n<p>The first chunk returned by the iterator will contain the first <code>chunk_size</code> elements of\nthe slice; the second chunk will contain the next <code>chunk_size</code> elements; and so on until the\nfinal chunk, which may contain fewer than <code>chunk_size</code> elements.</p>\n<p>If <code>chunk_size</code> is 0, the iterator behaves like <code>iter()</code>, yielding the original slice as a\nsingle chunk. If <code>chunk_size</code> is greater than the length of the slice, the iterator yields\nno values.</p>',
     '<p>返回一个迭代器，每次遍历切片的 <code>chunk_size</code> 个元素，从切片开头开始。</p>\n<p>迭代器返回的第一个块包含切片的前 <code>chunk_size</code> 个元素；第二个块包含接下来的 <code>chunk_size</code> 个元素；依此类推，直到最后一个块可能包含少于 <code>chunk_size</code> 个的元素。</p>\n<p>若 <code>chunk_size</code> 为 0，则迭代器行为类似 <code>iter()</code>，将原切片作为单个块产出。若 <code>chunk_size</code> 大于切片长度，则迭代器不产生任何值。</p>'),
    # 26. chunks_exact_mut
    ('<p>Returns an iterator over <code>chunk_size</code> elements of the slice at a time, starting at the\nbeginning of the slice.</p>\n<p>The first chunk returned by the iterator will contain the first <code>chunk_size</code> elements of\nthe slice; the second chunk will contain the next <code>chunk_size</code> elements; and so on until the\nfinal chunk, which may contain fewer than <code>chunk_size</code> elements.</p>\n<p>If <code>chunk_size</code> is 0, the iterator behaves like <code>chunks_exact_mut(0)</code>, yielding the original\nslice as a single chunk. If <code>chunk_size</code> is greater than the length of the slice, the\niterator yields no values.</p>',
     '<p>返回一个迭代器，每次遍历切片的 <code>chunk_size</code> 个元素，从切片开头开始。</p>\n<p>迭代器返回的第一个块包含切片的前 <code>chunk_size</code> 个元素；第二个块包含接下来的 <code>chunk_size</code> 个元素；依此类推，直到最后一个块可能包含少于 <code>chunk_size</code> 个的元素。</p>\n<p>若 <code>chunk_size</code> 为 0，则迭代器行为类似 <code>chunks_exact_mut(0)</code>，将原切片作为单个块产出。若 <code>chunk_size</code> 大于切片长度，则迭代器不产生任何值。</p>'),
    # 27. rchunks
    ('<p>Returns an iterator over <code>chunk_size</code> elements of the slice at a time, starting at the end\nof the slice.</p>\n<p>The first chunk returned by the iterator will contain the last <code>chunk_size</code> elements of the\nslice; the second chunk will contain the previous <code>chunk_size</code> elements; and so on until the\nfinal chunk, which will contain the remaining elements, less than <code>chunk_size</code>.</p>\n<p>If <code>chunk_size</code> is 0, the iterator behaves like <code>iter()</code>, yielding the original slice as a\nsingle chunk. If <code>chunk_size</code> is greater than the length of the slice, the iterator yields\nno values.</p>',
     '<p>返回一个迭代器，每次遍历切片的 <code>chunk_size</code> 个元素，从切片末尾开始。</p>\n<p>迭代器返回的第一个块包含切片末尾的 <code>chunk_size</code> 个元素；第二个块包含前 <code>chunk_size</code> 个元素；依此类推，直到最后一个块包含少于 <code>chunk_size</code> 个的剩余元素。</p>\n<p>若 <code>chunk_size</code> 为 0，则迭代器行为类似 <code>iter()</code>，将原切片作为单个块产出。若 <code>chunk_size</code> 大于切片长度，则迭代器不产生任何值。</p>'),
    # 28. rchunks_mut
    ('<p>Returns an iterator over <code>chunk_size</code> elements of the slice at a time, starting at the end\nof the slice.</p>\n<p>The first chunk returned by the iterator will contain the last <code>chunk_size</code> elements of the\nslice; the second chunk will contain the previous <code>chunk_size</code> elements; and so on until the\nfinal chunk, which will contain the remaining elements, less than <code>chunk_size</code>.</p>\n<p>If <code>chunk_size</code> is 0, the iterator behaves like <code>rchunks_mut(0)</code>, yielding the original slice\nas a single chunk. If <code>chunk_size</code> is greater than the length of the slice, the iterator\nyields no values.</p>',
     '<p>返回一个迭代器，每次遍历切片的 <code>chunk_size</code> 个元素，从切片末尾开始。</p>\n<p>迭代器返回的第一个块包含切片末尾的 <code>chunk_size</code> 个元素；第二个块包含前 <code>chunk_size</code> 个元素；依此类推，直到最后一个块包含少于 <code>chunk_size</code> 个的剩余元素。</p>\n<p>若 <code>chunk_size</code> 为 0，则迭代器行为类似 <code>rchunks_mut(0)</code>，将原切片作为单个块产出。若 <code>chunk_size</code> 大于切片长度，则迭代器不产生任何值。</p>'),
    # 29. rchunks_exact
    ('<p>Returns an iterator over <code>chunk_size</code> elements of the slice at a time, starting at the\nbeginning of the slice.</p>\n<p>The first chunk returned by the iterator will contain the first <code>chunk_size</code> elements of\nthe slice; the second chunk will contain the next <code>chunk_size</code> elements; and so on until the\nfinal chunk, which may contain fewer than <code>chunk_size</code> elements.</p>\n<p>If <code>chunk_size</code> is 0, the iterator behaves like <code>iter()</code>, yielding the original slice as a\nsingle chunk. If <code>chunk_size</code> is greater than the length of the slice, the iterator yields\nno values.</p>',
     '<p>返回一个迭代器，每次遍历切片的 <code>chunk_size</code> 个元素，从切片开头开始。</p>\n<p>迭代器返回的第一个块包含切片的前 <code>chunk_size</code> 个元素；第二个块包含接下来的 <code>chunk_size</code> 个元素；依此类推，直到最后一个块可能包含少于 <code>chunk_size</code> 个的元素。</p>\n<p>若 <code>chunk_size</code> 为 0，则迭代器行为类似 <code>iter()</code>，将原切片作为单个块产出。若 <code>chunk_size</code> 大于切片长度，则迭代器不产生任何值。</p>'),
    # 30. rchunks_exact_mut
    ('<p>Returns an iterator over <code>chunk_size</code> elements of the slice at a time, starting at the end\nof the slice.</p>\n<p>The first chunk returned by the iterator will contain the last <code>chunk_size</code> elements of the\nslice; the second chunk will contain the previous <code>chunk_size</code> elements; and so on until the\nfinal chunk, which may contain fewer than <code>chunk_size</code> elements.</p>\n<p>If <code>chunk_size</code> is 0, the iterator behaves like <code>rchunks_exact_mut(0)</code>, yielding the original\nslice as a single chunk. If <code>chunk_size</code> is greater than the length of the slice, the\niterator yields no values.</p>',
     '<p>返回一个迭代器，每次遍历切片的 <code>chunk_size</code> 个元素，从切片末尾开始。</p>\n<p>迭代器返回的第一个块包含切片末尾的 <code>chunk_size</code> 个元素；第二个块包含前 <code>chunk_size</code> 个元素；依此类推，直到最后一个块可能包含少于 <code>chunk_size</code> 个的元素。</p>\n<p>若 <code>chunk_size</code> 为 0，则迭代器行为类似 <code>rchunks_exact_mut(0)</code>，将原切片作为单个块产出。若 <code>chunk_size</code> 大于切片长度，则迭代器不产生任何值。</p>'),
    # 31. split_at_checked
    ('<p>Divides one slice into two at an index, returning <code>None</code> if the slice is\nshorter than the index.</p>',
     '<p>在某个索引处将切片一分为二；若切片长度小于该索引则返回 <code>None</code>。</p>'),
    # 32. split_at_mut_checked
    ('<p>Divides one mutable slice into two at an index, returning <code>None</code> if the\nslice is shorter than the index.</p>',
     '<p>在某个索引处将可变切片一分为二；若切片长度小于该索引则返回 <code>None</code>。</p>'),
    # 33. split
    ('<p>Returns an iterator over subslices separated by elements that match\n<code>pred</code>. The matched element is not contained in the subslices.</p>',
     '<p>返回一个迭代器，遍历由满足 <code>pred</code> 的元素分隔开的子切片。匹配元素本身不包含在子切片中。</p>'),
    # 34. split_mut
    ('<p>Returns an iterator over mutable subslices separated by elements that\nmatch <code>pred</code>. The matched element is not contained in the subslices.</p>',
     '<p>返回一个迭代器，遍历由满足 <code>pred</code> 的元素分隔开的可变子切片。匹配元素本身不包含在子切片中。</p>'),
    # 35. split_inclusive
    ('<p>Returns an iterator over subslices separated by elements that match\n<code>pred</code>. The matched element is contained in the previous subslice.</p>',
     '<p>返回一个迭代器，遍历由满足 <code>pred</code> 的元素分隔开的子切片。匹配元素本身被包含在前一个子切片中。</p>'),
    # 36. split_inclusive_mut
    ('<p>Returns an iterator over mutable subslices separated by elements that\nmatch <code>pred</code>. The matched element is contained in the previous subslice.</p>',
     '<p>返回一个迭代器，遍历由满足 <code>pred</code> 的元素分隔开的可变子切片。匹配元素本身被包含在前一个子切片中。</p>'),
    # 37. rsplit
    ('<p>Returns an iterator over subslices separated by elements that match\n<code>pred</code>, starting from the end of the slice. The matched element is\nnot contained in the subslices.</p>',
     '<p>返回一个迭代器，从切片末尾开始遍历由满足 <code>pred</code> 的元素分隔开的子切片。匹配元素本身不包含在子切片中。</p>'),
    # 38. rsplit_mut
    ('<p>Returns an iterator over mutable subslices separated by elements that\nmatch <code>pred</code>, starting from the end of the slice. The matched element\nis not contained in the subslices.</p>',
     '<p>返回一个迭代器，从切片末尾开始遍历由满足 <code>pred</code> 的元素分隔开的可变子切片。匹配元素本身不包含在子切片中。</p>'),
    # 39. contains
    ('<p>Returns <code>true</code> if the slice contains an element with the given value.</p>\n<p>This operation is <em>O</em>(<em>n</em>).</p>\n<p>Note that if you have a sorted slice, <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.binary_search" title="method slice::binary_search"><code>binary_search</code></a> may be faster.</p>',
     '<p>若切片包含具有给定值的元素则返回 <code>true</code>。</p>\n<p>该操作的时间复杂度为 <em>O</em>(<em>n</em>)。</p>\n<p>注意，若切片已排序，使用 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.binary_search" title="method slice::binary_search"><code>binary_search</code></a> 可能更快。</p>'),
    # 40. starts_with
    ('<p>Returns <code>true</code> if <code>needle</code> is a prefix of the slice or equal to the slice.</p>',
     '<p>若 <code>needle</code> 是切片的前缀或与切片相等则返回 <code>true</code>。</p>'),
    # 41. ends_with
    ('<p>Returns <code>true</code> if <code>needle</code> is a suffix of the slice or equal to the slice.</p>',
     '<p>若 <code>needle</code> 是切片的后缀或与切片相等则返回 <code>true</code>。</p>'),
    # 42. rotate_left
    ('<p>Rotates the slice in-place such that the first <code>mid</code> elements of the\nslice move to the end, while the last <code>self.len() - mid</code> elements move\nto the front.</p>\n<p>After calling this function, the element previously at index <code>mid</code> will\nbecome the first element in the slice.</p>',
     '<p>将切片原地旋转，使得切片开头的 <code>mid</code> 个元素移到末尾，而末尾的 <code>self.len() - mid</code> 个元素移到开头。</p>\n<p>调用本函数后，原本索引为 <code>mid</code> 的元素将成为切片的第一个元素。</p>'),
    # 43. rotate_right
    ('<p>Rotates the slice in-place such that the first <code>self.len() - k</code>\nelements of the slice move to the end, while the last <code>k</code> elements move\nto the front.</p>\n<p>After calling this function, the element previously at index <code>self.len() - k</code>\nwill become the first element in the slice.</p>',
     '<p>将切片原地旋转，使得切片开头的 <code>self.len() - k</code> 个元素移到末尾，而末尾的 <code>k</code> 个元素移到开头。</p>\n<p>调用本函数后，原本索引为 <code>self.len() - k</code> 的元素将成为切片的第一个元素。</p>'),
    # 44. rotate_left (extra alt impl)
    ('<p>Moves the elements of this slice <code>N</code> places to the left, returning the\nrotated slice.</p>',
     '<p>将切片中的元素向左移动 <code>N</code> 个位置，返回旋转后的切片。</p>'),
    # 45. rotate_right (extra alt impl)
    ('<p>Moves the elements of this slice <code>N</code> places to the right, returning the\nrotated slice.</p>',
     '<p>将切片中的元素向右移动 <code>N</code> 个位置，返回旋转后的切片。</p>'),
    # 46. fill (alt impl)
    ('<p>Fills <code>self</code> with elements by cloning <code>value</code>.</p>',
     '<p>通过克隆 <code>value</code> 填充 <code>self</code>。</p>'),
    # 47. fill_with (alt impl)
    ('<p>Fills <code>self</code> with elements returned by calling a closure repeatedly.</p>',
     '<p>通过反复调用闭包所返回的元素填充 <code>self</code>。</p>'),
    # 48. fill_with (alt impl 2)
    ('<p>This method uses a closure to create new values. If you’d rather\n<a href="https://doc.rust-lang.org/1.95.0/core/clone/trait.Clone.html" title="trait core::clone::Clone">Clone</a> a given value, use <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.fill" title="method slice::fill"><code>fill</code></a>. If you want to use the\n<a href="https://doc.rust-lang.org/1.95.0/core/default/trait.Default.html" title="trait core::default::Default">Default</a> trait to generate values, use <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.fill_with" title="method slice::fill_with"><code>fill_with</code></a>.</p>',
     '<p>本方法使用闭包来创建新值。若希望克隆某个给定的值，请使用 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.fill" title="method slice::fill"><code>fill</code></a>。若希望使用 <a href="https://doc.rust-lang.org/1.95.0/core/default/trait.Default.html" title="trait core::default::Default">Default</a> trait 来生成值，请使用 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.fill_with" title="method slice::fill_with"><code>fill_with</code></a>。</p>'),
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
