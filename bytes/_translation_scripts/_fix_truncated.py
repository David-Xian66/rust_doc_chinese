"""Fix truncated translation keys."""
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('bytes/_buf_translations.json', 'r', encoding='utf-8') as f:
    T = json.load(f)

# Fix truncated keys
fixes = {
    'When processing a Bytes buffer with other tools, one often gets a\n&amp;[u8] which is in fact a slice of the Bytes, i.e. a subset of it.\nThis function turns that &amp;[u8] into another Bytes, as if one had\ncalled self.slice': '使用其他工具处理 <code>Bytes</code> 缓冲区时，经常会得到 <code>&amp;[u8]</code>，它实际上是 <code>Bytes</code> 的一个切片，即其子集。本函数将该 <code>&amp;[u8]</code> 转换为另一个 <code>Bytes</code>，如同调用 <code>self.slice</code> 并传入与 subset 对应的偏移量。',
    'Afterwards self contains elements [0, at), and the returned Bytes\ncontains elements [at, len). It’s guaranteed that the memory does not\nmove, that is, the address of self does not change, and the addr': '此后 <code>self</code> 包含元素 <code>[0, at)</code>，返回的 <code>Bytes</code> 包含元素 <code>[at, len)</code>。保证内存不会移动，即 <code>self</code> 的地址不变，且返回切片的地址也不变。',
    'The owner will be transferred to the constructed Bytes object, which\nwill ensure it is dropped once all remaining clones of the constructed\nobject are dropped. The owner will then be responsible for': 'owner 将被转移到已构造的 <a href="struct.Bytes.html" title="struct bytes::Bytes">Bytes</a> 对象中，确保在已构造对象的所有剩余克隆都被丢弃后被释放。然后 owner 将负责释放指定的内存。',
    'If self is unique for the entire original buffer, this will succeed\nand return a BytesMut with the contents of self without copying.\nIf self is not unique for the entire original buffer, this will f': '若 <code>self</code> 在整个原始缓冲区中是唯一的，则此调用成功，并返回包含 <code>self</code> 内容（无拷贝）的 <code>BytesMut</code>。若 <code>self</code> 在整个原始缓冲区中不是唯一的，则此调用失败并返回 self。',
    'If bytes is unique for the entire original buffer, this will return a\nBytesMut with the contents of bytes without copying.\nIf bytes is not unique for the entire original buffer, this will make\na co': '若 <code>bytes</code> 在整个原始缓冲区中是唯一的，则返回包含 <code>bytes</code> 内容（无拷贝）的 <code>BytesMut</code>。若 <code>bytes</code> 在整个原始缓冲区中不是唯一的，则会对原始缓冲区中 <code>bytes</code> 子集进行复制。',

    'Afterwards self contains elements [0, at), and the returned\nBytesMut contains elements [at, capacity). It’s guaranteed that the\nmemory does not move, that is, the address of self does not change,\na': '此后 <code>self</code> 包含元素 <code>[0, at)</code>，返回的 <code>BytesMut</code> 包含元素 <code>[at, capacity)</code>。保证内存不会移动，即 <code>self</code> 的地址不变，且返回切片的地址也不变。',
    'Before allocating new buffer space, the function will attempt to reclaim\nspace in the existing buffer. If the current handle references a view\ninto a larger original buffer, and all other handles re': '在分配新缓冲区空间之前，本函数会尝试回收现有缓冲区中的空间。若当前句柄引用的是较大原始缓冲区的视图，并且引用同一原始缓冲区其他部分的所有其他句柄都已丢弃，则当前视图可被复制到缓冲区开头。',
    'This optimization will only happen if shifting the data from the current\nview to the front of the buffer is not too expensive in terms of the\n(amortized) time required. The precise condition is subj': '仅当将数据从当前视图移动到缓冲区开头的（摊销）时间开销不太大时，才会执行此优化。具体条件可能会变化；目前要求被移动数据的长度至少与：',
    'If the two BytesMut objects were previously contiguous and not mutated\nin a way that causes re-allocation i.e., if other was created by\ncalling split_off on this BytesMut, then this is an O(1) opera': '若两个 <code>BytesMut</code> 对象先前是连续的，且未以导致重新分配的方式被修改，即 <code>other</code> 是通过对此 <code>BytesMut</code> 调用 <code>split_off</code> 创建的，则此操作为 <code>O(1)</code>，仅减少引用计数并设置一些索引。否则此方法的行为与将 <code>other</code> 的字节追加到 <code>self</code> 末尾相同。',
    'If the two BytesMut objects were previously contiguous, i.e., if\nother was created by calling split_off on this BytesMut, then\nthis is an O(1) operation that just decreases a reference\ncount and se': '若两个 <code>BytesMut</code> 对象先前是连续的，即 <code>other</code> 是通过对此 <code>BytesMut</code> 调用 <code>split_off</code> 创建的，则此操作为 <code>O(1)</code>，仅减少引用计数并设置一些索引。否则此方法的行为与将 <code>other</code> 的字节追加到 <code>self</code> 末尾相同。',

    'The caller must not read from the referenced memory and must not write\nuninitialized bytes to the slice either. This is because BufMut implementation\nthat created the UninitSlice knows which parts a': '调用方不得读取所引用的内存，也不得向切片写入未初始化的字节。这是因为创建 <code>UninitSlice</code> 的 <code>BufMut</code> 实现知道哪些部分是初始化的——若跳过此规则，则后续读取未初始化内存会导致未定义行为。',
}

T.update(fixes)

with open('bytes/_buf_translations.json', 'w', encoding='utf-8') as f:
    json.dump(T, f, ensure_ascii=False, indent=2)

print(f'Total: {len(T)}')