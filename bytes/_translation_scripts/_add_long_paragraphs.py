"""Add long-form paragraph translations for Bytes/BytesMut."""
import json

# Load existing translations
with open('bytes/_buf_translations.json', 'r', encoding='utf-8') as f:
    T = json.load(f)

# Add long-form translations
T.update({
    # Bytes
    'The owner will be transferred to the constructed Bytes object, which\nwill ensure it is dropped once all remaining clones of the constructed\nobject are dropped. The owner will then be responsible for': 'owner 将被转移到已构造的 <a href="struct.Bytes.html" title="struct bytes::Bytes">Bytes</a> 对象中，确保在已构造对象的所有剩余克隆都被丢弃后被释放。然后 owner 将负责释放指定的内存。',
    'Note that converting Bytes constructed from an owner into a BytesMut\nwill always create a deep copy of the buffer into newly allocated memory.': '请注意，将由 owner 构造的 <a href="struct.Bytes.html" title="struct bytes::Bytes">Bytes</a> 转换为 <a href="struct.BytesMut.html" title="struct bytes::BytesMut">BytesMut</a> 总会将缓冲区的深度拷贝到新分配的内存中。',
    'The result of this method may be invalidated immediately if another\nthread clones this value while this is being called. Ensure you have\nunique access to this value (&amp;mut Bytes) first if you need to be\ncertain the result is valid (i.e. for safety reasons).': '若在调用此方法时其他线程克隆此值，则该方法的结果可能立即失效。若需确保结果有效（例如出于安全考虑），请先确保你对此值具有唯一访问权限（<code>&amp;mut Bytes</code>）。',
    'Requires that begin &lt;= end and end &lt;= self.len(), otherwise slicing\nwill panic.': '要求 <code>begin &lt;= end</code> 且 <code>end &lt;= self.len()</code>，否则切片操作会 panic。',
    'When processing a Bytes buffer with other tools, one often gets a\n&amp;[u8] which is in fact a slice of the Bytes, i.e. a subset of it.\nThis function turns that &amp;[u8] into another Bytes, as if one had\ncalled self.slice': '使用其他工具处理 <code>Bytes</code> 缓冲区时，经常会得到 <code>&amp;[u8]</code>，它实际上是 <code>Bytes</code> 的一个切片，即其子集。本函数将该 <code>&amp;[u8]</code> 转换为另一个 <code>Bytes</code>，如同调用 <code>self.slice',
    'Requires that the given sub slice is in fact contained within the\nBytes buffer; otherwise this function will panic.': '要求给定的 <code>sub</code> 切片确实包含在 <code>Bytes</code> 缓冲区中；否则此函数会 panic。',
    'Afterwards self contains elements [0, at), and the returned Bytes\ncontains elements [at, len). It’s guaranteed that the memory does not\nmove, that is, the address of self does not change, and the address of\nthe returned slice is': '此后 <code>self</code> 包含元素 <code>[0, at)</code>，返回的 <code>Bytes</code> 包含元素 <code>[at, len)</code>。保证内存不会移动，即 <code>self</code> 的地址不变，且返回切片的地址不变。',
    'This is an O(1) operation that just increases the reference count and\nsets a few indices.': '此操作为 <code>O(1)</code>，仅增加引用计数并设置一些索引。',
    'Afterwards self contains elements [at, len), and the returned\nBytes contains elements [0, at).': '此后 <code>self</code> 包含元素 <code>[at, len)</code>，返回的 <code>Bytes</code> 包含元素 <code>[0, at)</code>。',
    'Shortens the buffer, keeping the first len bytes and dropping the\nrest.': '缩短缓冲区，保留前 <code>len</code> 字节，丢弃其余字节。',
    'If len is greater than the buffer’s current length, this has no\neffect.': '若 <code>len</code> 大于缓冲区的当前长度，则此操作无效。',
    'The split_off method can emulate truncate, but this causes the\nexcess bytes to be returned instead of dropped.': '<a href="struct.Bytes.html#method.split_off" title="method bytes::Bytes::split_off">split_off</a> 方法可以模拟 <code>truncate</code>，但这会导致多余的字节被返回而不是丢弃。',
    'If self is unique for the entire original buffer, this will succeed\nand return a BytesMut with the contents of self without copying.\nIf self is not unique for the entire original buffer, this will f': '若 <code>self</code> 在整个原始缓冲区中是唯一的，则此调用成功，并返回包含 <code>self</code> 内容（无拷贝）的 <code>BytesMut</code>。若 <code>self</code> 在整个原始缓冲区中不是唯一的，则此调用失败并返回 self。',
    'This will also always fail if the buffer was constructed via either\nfrom_owner or from_static.': '若缓冲区是通过 <a href="struct.Bytes.html#method.from_owner" title="associated function bytes::Bytes::from_owner">from_owner</a> 或 <a href="struct.Bytes.html#method.from_static" title="associated function bytes::Bytes::from_static">from_static</a> 构造的，则此调用也总是失败。',
    'If bytes is unique for the entire original buffer, this will return a\nBytesMut with the contents of bytes without copying.\nIf bytes is not unique for the entire original buffer, this will make\na co': '若 <code>bytes</code> 在整个原始缓冲区中是唯一的，则返回包含 <code>bytes</code> 内容（无拷贝）的 <code>BytesMut</code>。若 <code>bytes</code> 在整个原始缓冲区中不是唯一的，则会对原始缓冲区中 <code>bytes</code> 子集进行复制。',

    # BytesMut
    'The returned BytesMut will be able to hold at least capacity bytes\nwithout reallocating.': '返回的 <code>BytesMut</code> 在不重新分配的情况下至少可容纳 <code>capacity</code> 字节。',
    'It is important to note that this function does not specify the length\nof the returned BytesMut, but only the capacity.': '需要注意，本函数不指定返回的 <code>BytesMut</code> 的长度，只指定容量。',
    'Resulting object has length 0 and unspecified capacity.\nThis function does not allocate.': '生成的对象长度为 0，容量未指定。本函数不分配内存。',
    'The conversion is zero cost and is used to indicate that the slice\nreferenced by the handle will no longer be mutated. Once the conversion\nis done, the handle can be cloned and shared across threads': '此转换零开销，用于表示句柄所引用的切片将不再被修改。转换完成后，句柄可被克隆并在线程间共享。',
    'The resulting object has a length of len and a capacity greater\nthan or equal to len. The entire length of the object will be filled\nwith zeros.': '生成对象的长度为 <code>len</code>，容量大于或等于 <code>len</code>。对象的整个长度将填充为零。',
    'On some platforms or allocators this function may be faster than\na manual implementation.': '在某些平台或分配器上，本函数可能比手动实现更快。',
    'Afterwards self contains elements [0, at), and the returned\nBytesMut contains elements [at, capacity). It’s guaranteed that the\nmemory does not move, that is, the address of self does not change,\na': '此后 <code>self</code> 包含元素 <code>[0, at)</code>，返回的 <code>BytesMut</code> 包含元素 <code>[at, capacity)</code>。保证内存不会移动，即 <code>self</code> 的地址不变，且返回切片的地址不变。',
    'Panics if at &gt; capacity.': '若 <code>at &gt; capacity</code> 则 panic。',
    'Removes the bytes from the current view, returning them in a new\nBytesMut handle.': '从当前视图中移除字节，将其作为新的 <code>BytesMut</code> 句柄返回。',
    'Afterwards, self will be empty, but will retain any additional\ncapacity that it had before the operation. This is identical to\nself.split_to(self.len()).': '此后 <code>self</code> 将为空，但保留操作前已有的额外容量。这与 <code>self.split_to(self.len())</code> 等价。',
    'This is an O(1) operation that just increases the reference count and\nsets a few indices.': '此操作为 <code>O(1)</code>，仅增加引用计数并设置一些索引。',
    'Afterwards self contains elements [at, len), and the returned BytesMut\ncontains elements [0, at).': '此后 <code>self</code> 包含元素 <code>[at, len)</code>，返回的 <code>BytesMut</code> 包含元素 <code>[0, at)</code>。',
    'Existing underlying capacity is preserved.': '保留底层现有容量。',
    'Resizes the buffer so that len is equal to new_len.': '调整缓冲区大小，使 <code>len</code> 等于 <code>new_len</code>。',
    'If new_len is greater than len, the buffer is extended by the\ndifference with each additional byte set to value. If new_len is\nless than len, the buffer is simply truncated.': '若 <code>new_len</code> 大于 <code>len</code>，则将缓冲区扩展差值部分，每个新增字节设为 <code>value</code>。若 <code>new_len</code> 小于 <code>len</code>，则缓冲区直接被截断。',
    'This will explicitly set the size of the buffer without actually\nmodifying the data, so it is up to the caller to ensure that the data\nhas been initialized.': '这会显式设置缓冲区的大小而不实际修改数据，因此调用方负责确保数据已初始化。',
    'Reserves capacity for at least additional more bytes to be inserted\ninto the given BytesMut.': '为给定 <code>BytesMut</code> 中至少可插入的 <code>additional</code> 字节预留容量。',
    'More than additional bytes may be reserved in order to avoid frequent\nreallocations. A call to reserve may result in an allocation.': '为避免频繁重新分配，可能预留多于 <code>additional</code> 字节。调用 <code>reserve</code> 可能导致分配。',
    'Before allocating new buffer space, the function will attempt to reclaim\nspace in the existing buffer. If the current handle references a view\ninto a larger original buffer, and all other handles re': '在分配新缓冲区空间之前，本函数会尝试回收现有缓冲区中的空间。若当前句柄引用的是较大原始缓冲区的视图，并且引用同一原始缓冲区其他部分的所有其他句柄都已丢弃，则当前视图可被复制到缓冲区开头。',
    'This optimization will only happen if shifting the data from the current\nview to the front of the buffer is not too expensive in terms of the\n(amortized) time required. The precise condition is subj': '仅当将数据从当前视图移动到缓冲区开头的（摊销）时间开销不太大时，才会执行此优化。具体条件可能会变化；目前要求被移动数据的长度至少与：',
    'This method does not preserve data stored in the unused capacity.': '此方法不会保留未使用容量中存储的数据。',
    'In the following example, a new buffer is allocated.': '在下面的示例中，分配了新缓冲区。',
    'In the following example, the existing buffer is reclaimed.': '在下面的示例中，回收了现有缓冲区。',
    'Panics if the new capacity overflows usize.': '若新容量溢出 <code>usize</code> 则 panic。',
    'Attempts to cheaply reclaim already allocated capacity for at least additional more\nbytes to be inserted into the given BytesMut and returns true if it succeeded.': '尝试以低成本回收已分配容量，使给定 <code>BytesMut</code> 至少可插入 <code>additional</code> 字节；成功则返回 true。',
    'try_reclaim behaves exactly like reserve, except that it never allocates new storage\nand returns a bool indicating whether it was successful in doing so:': '<code>try_reclaim</code> 行为与 <code>reserve</code> 完全相同，只是它从不分配新存储，并返回一个 <code>bool</code> 指示是否成功：',
    'try_reclaim returns false under these conditions:': '<code>try_reclaim</code> 在以下条件下返回 false：',
    'Reclaiming the allocation cheaply is possible if the BytesMut has no outstanding\nreferences through other BytesMuts or Bytes which point to the same underlying\nstorage.': '若 <code>BytesMut</code> 没有其他指向同一底层存储的 <code>BytesMut</code> 或 <code>Bytes</code> 的未完成引用，则可以低成本回收分配。',
    'If this BytesMut object does not have enough capacity, it is resized\nfirst.': '若此 <code>BytesMut</code> 对象没有足够容量，则先调整大小。',
    'Clones the elements in the given range within this BytesMut and\nappends them to the end.': '克隆此 <code>BytesMut</code> 中给定 <code>range</code> 范围内的元素，并将其追加到末尾。',
    'Panics if range is out of bounds for this BytesMut.': '若 <code>range</code> 超出此 <code>BytesMut</code> 的范围则 panic。',
    'If the two BytesMut objects were previously contiguous, i.e., if\nother was created by calling split_off on this BytesMut, then\nthis is an O(1) operation that just decreases a reference\ncount and se': '若两个 <code>BytesMut</code> 对象先前是连续的，即 <code>other</code> 是通过对此 <code>BytesMut</code> 调用 <code>split_off</code> 创建的，则此操作为 <code>O(1)</code>，仅减少引用计数并设置一些索引。否则此方法的行为与将 <code>other</code> 的字节追加到 <code>self</code> 末尾相同。',
    'Returns the remaining spare capacity of the buffer as a slice of MaybeUninit&lt;u8&gt;.': '将缓冲区的剩余空闲容量作为 <code>MaybeUninit&lt;u8&gt;</code> 切片返回。',
    'The returned slice can be used to fill the buffer with data (e.g. by\nreading from a file) before marking the data as initialized using the\nset_len method.': '返回的切片可用于填充缓冲区数据（例如从文件读取），然后使用 <a href="struct.BytesMut.html#method.set_len" title="method bytes::BytesMut::set_len"><code>set_len</code></a> 方法将数据标记为已初始化。',
})

with open('bytes/_buf_translations.json', 'w', encoding='utf-8') as f:
    json.dump(T, f, ensure_ascii=False, indent=2)

print(f'Total translations: {len(T)}')