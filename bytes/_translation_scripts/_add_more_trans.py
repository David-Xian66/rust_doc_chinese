"""Add more long-form translations."""
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('bytes/_buf_translations.json', 'r', encoding='utf-8') as f:
    T = json.load(f)

T.update({
    # Bytes more
    'The owner will be transferred to the constructed Bytes object, which\nwill ensure it is dropped once all remaining clones of the constructed\nobject are dropped. The owner will then be responsible for': 'owner 将被转移到已构造的 <a href="struct.Bytes.html" title="struct bytes::Bytes">Bytes</a> 对象中，确保在已构造对象的所有剩余克隆都被丢弃后被释放。然后 owner 将负责释放指定的内存。',
    'When processing a Bytes buffer with other tools, one often gets a\n&amp;[u8] which is in fact a slice of the Bytes, i.e. a subset of it.\nThis function turns that &amp;[u8] into another Bytes, as if one': '使用其他工具处理 <code>Bytes</code> 缓冲区时，经常会得到 <code>&amp;[u8]</code>，它实际上是 <code>Bytes</code> 的一个切片，即其子集。本函数将该 <code>&amp;[u8]</code> 转换为另一个 <code>Bytes</code>，如同调用 <code>self.slice',
    'Afterwards self contains elements [0, at), and the returned Bytes\ncontains elements [at, len). It’s guaranteed that the memory does not\nmove, that is, the address of self does not change, and the addr': '此后 <code>self</code> 包含元素 <code>[0, at)</code>，返回的 <code>Bytes</code> 包含元素 <code>[at, len)</code>。保证内存不会移动，即 <code>self</code> 的地址不变，且返回切片的地址不变。',
    'If self is unique for the entire original buffer, this will succeed\nand return a BytesMut with the contents of self without copying.\nIf self is not unique for the entire original buffer, this will f': '若 <code>self</code> 在整个原始缓冲区中是唯一的，则此调用成功，并返回包含 <code>self</code> 内容（无拷贝）的 <code>BytesMut</code>。若 <code>self</code> 在整个原始缓冲区中不是唯一的，则此调用失败并返回 self。',
    'If bytes is unique for the entire original buffer, this will return a\nBytesMut with the contents of bytes without copying.\nIf bytes is not unique for the entire original buffer, this will make\na co': '若 <code>bytes</code> 在整个原始缓冲区中是唯一的，则返回包含 <code>bytes</code> 内容（无拷贝）的 <code>BytesMut</code>。若 <code>bytes</code> 在整个原始缓冲区中不是唯一的，则会对原始缓冲区中 <code>bytes</code> 子集进行复制。',

    # BytesMut more
    'The conversion is zero cost and is used to indicate that the slice\nreferenced by the handle will no longer be mutated. Once the conversion\nis done, the handle can be cloned and shared across threads': '此转换零开销，用于表示句柄所引用的切片将不再被修改。转换完成后，句柄可被克隆并在线程间共享。',
    'Afterwards self contains elements [0, at), and the returned\nBytesMut contains elements [at, capacity). It’s guaranteed that the\nmemory does not move, that is, the address of self does not change,\na': '此后 <code>self</code> 包含元素 <code>[0, at)</code>，返回的 <code>BytesMut</code> 包含元素 <code>[at, capacity)</code>。保证内存不会移动，即 <code>self</code> 的地址不变，且返回切片的地址不变。',
    'Before allocating new buffer space, the function will attempt to reclaim\nspace in the existing buffer. If the current handle references a view\ninto a larger original buffer, and all other handles re': '在分配新缓冲区空间之前，本函数会尝试回收现有缓冲区中的空间。若当前句柄引用的是较大原始缓冲区的视图，并且引用同一原始缓冲区其他部分的所有其他句柄都已丢弃，则当前视图可被复制到缓冲区开头。',
    'This optimization will only happen if shifting the data from the current\nview to the front of the buffer is not too expensive in terms of the\n(amortized) time required. The precise condition is subj': '仅当将数据从当前视图移动到缓冲区开头的（摊销）时间开销不太大时，才会执行此优化。具体条件可能会变化；目前要求被移动数据的长度至少与：',
    'If the two BytesMut objects were previously contiguous and not mutated\nin a way that causes re-allocation i.e., if other was created by\ncalling split_off on this BytesMut, then this is an O(1) opera': '若两个 <code>BytesMut</code> 对象先前是连续的，且未以导致重新分配的方式被修改，即 <code>other</code> 是通过对此 <code>BytesMut</code> 调用 <code>split_off</code> 创建的，则此操作为 <code>O(1)</code>，仅减少引用计数并设置一些索引。否则此方法的行为与将 <code>other</code> 的字节追加到 <code>self</code> 末尾相同。',
    'If the two BytesMut objects were previously contiguous, i.e., if\nother was created by calling split_off on this BytesMut, then\nthis is an O(1) operation that just decreases a reference\ncount and se': '若两个 <code>BytesMut</code> 对象先前是连续的，即 <code>other</code> 是通过对此 <code>BytesMut</code> 调用 <code>split_off</code> 创建的，则此操作为 <code>O(1)</code>，仅减少引用计数并设置一些索引。否则此方法的行为与将 <code>other</code> 的字节追加到 <code>self</code> 末尾相同。',

    # UninitSlice
    'The caller must ensure that ptr references a valid memory region owned\nby the caller representing a byte slice for the duration of \'a.': '调用方必须确保 <code>ptr</code> 引用了由调用方拥有的有效内存区域，且在 \'a 的整个生命周期内代表一个字节切片。',
    'The caller must not read from the referenced memory and must not\nwrite uninitialized bytes to the slice either.': '调用方不得读取所引用的内存，也不得向切片写入未初始化的字节。',
    'Return a &amp;mut [MaybeUninit&lt;u8&gt;] to this slice’s buffer.': '返回此切片缓冲区的 <code>&amp;mut [MaybeUninit&lt;u8&gt;]</code>。',
    'The caller must not read from the referenced memory and must not write\nuninitialized bytes to the slice either. This is because BufMut implementation\nthat created the UninitSlice knows which parts a': '调用方不得读取所引用的内存，也不得向切片写入未初始化的字节。这是因为创建 <code>UninitSlice</code> 的 <code>BufMut</code> 实现知道哪些部分是初始化的——如果跳过此规则，则后续读取未初始化内存会导致未定义行为。',
    'Returns the number of bytes in the slice.': '返回切片中的字节数。',

    # Buf more
    'This function should never panic. chunk() should return an empty\nslice if and only if remaining() returns 0. In other words,\nchunk() returning an empty slice implies that remaining() will\nreturn 0 ': '此函数不应 panic。<code>chunk()</code> 返回空切片当且仅当 <code>remaining()</code> 返回 0。换言之，<code>chunk()</code> 返回空切片意味着 <code>remaining()</code> 将返回 0，',
    'Consumes len bytes inside self and returns new instance of Bytes\nwith this data.': '消耗 self 中的 <code>len</code> 字节，并返回包含此数据的新 <code>Bytes</code> 实例。',
    'This function returns a new value which implements Read by adapting\nthe Read trait functions to the Buf trait functions. Given that\nBuf operations are infallible, none of the Read functions will\nre': '此函数返回一个新值，通过将 <code>Read</code> trait 函数适配到 <code>Buf</code> trait 函数来实现 <code>Read</code>。由于 <code>Buf</code> 操作是 infallible 的，<code>Read</code> 函数不会返回错误。',

    # BufMut more
    'Returns a mutable slice starting at the current BufMut position and of\nlength between 0 and BufMut::remaining_mut(). Note that this can be shorter than the\nwhole remainder of the buffer (this allows': '返回从当前 <code>BufMut</code> 位置开始、长度介于 0 和 <code>BufMut::remaining_mut()</code> 之间的可变切片。注意这可能比缓冲区剩余总量更短（允许非连续的内部表示）。',
    'This function should never panic. chunk_mut() should return an empty\nslice if and only if remaining_mut() returns 0. In other words,\nchunk_mut() returning an empty slice implies that remaining_mut()': '此函数不应 panic。<code>chunk_mut()</code> 返回空切片当且仅当 <code>remaining_mut()</code> 返回 0。换言之，<code>chunk_mut()</code> 返回空切片意味着 <code>remaining_mut()</code> 将返回 0，',
    'This function returns a new value which implements Write by adapting\nthe Write trait functions to the BufMut trait functions. Given that\nBufMut operations are infallible, none of the Write functions': '此函数返回一个新值，通过将 <code>Write</code> trait 函数适配到 <code>BufMut</code> trait 函数来实现 <code>Write</code>。由于 <code>BufMut</code> 操作是 infallible 的，<code>Write</code> 函数不会返回错误。',
})

with open('bytes/_buf_translations.json', 'w', encoding='utf-8') as f:
    json.dump(T, f, ensure_ascii=False, indent=2)

print(f'Total: {len(T)}')