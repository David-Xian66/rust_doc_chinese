"""Add remaining 8 translations."""
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('bytes/_buf_translations.json', 'r', encoding='utf-8') as f:
    T = json.load(f)

RSQUO = '’'

T.update({
    'Before allocating new buffer space, the function will attempt to reclaim\nspace in the existing buffer. If the current handle references a view\ninto a larger original buffer, and all other handles referencing part\nof the same original buffer have been dropped, then the current view\ncan be copied/shifted to the front of the buffer and the handle can take ownership of the full buffer, provided that the full buffer is large enough to fit the requested additional capacity.': '在分配新缓冲区空间之前，本函数会尝试回收现有缓冲区中的空间。若当前句柄引用的是较大原始缓冲区的视图，并且引用同一原始缓冲区其他部分的所有其他句柄都已丢弃，则当前视图可被复制或移动到缓冲区开头，句柄可获取完整缓冲区的所有权，前提是完整缓冲区足够容纳所请求的额外容量。',

    'The caller must not read from the referenced memory and must not write\nuninitialized bytes to the slice either. This is because BufMut implementation\nthat created the UninitSlice knows which parts are initialized. Writing uninitialized\nbytes to the slice may cause the BufMut to read those bytes a': '调用方不得读取所引用的内存，也不得向切片写入未初始化的字节。这是因为创建 <code>UninitSlice</code> 的 <code>BufMut</code> 实现知道哪些部分是初始化的。向切片写入未初始化的字节可能导致 <code>BufMut</code> 之后读取这些字节并触发未定义行为。',

    'This function should never panic. chunk() should return an empty\nslice if and only if remaining() returns 0. In other words,\nchunk() returning an empty slice implies that remaining() will\nreturn 0 and remaining() returning 0 implies that chunk() will\nreturn an empty slice.': '此函数不应 panic。<code>chunk()</code> 返回空切片当且仅当 <code>remaining()</code> 返回 0。换言之，<code>chunk()</code> 返回空切片意味着 <code>remaining()</code> 将返回 0，而 <code>remaining()</code> 返回 0 意味着 <code>chunk()</code> 将返回空切片。',

    'This function returns a new value which implements Read by adapting\nthe Read trait functions to the Buf trait functions. Given that\nBuf operations are infallible, none of the Read functions will\nreturn with Err.': '此函数返回一个新值，通过将 <code>Read</code> trait 函数适配到 <code>Buf</code> trait 函数来实现 <code>Read</code>。由于 <code>Buf</code> 操作是 infallible 的，<code>Read</code> 函数都不会返回 <code>Err</code>。',

    'Implementations of remaining_mut should ensure that the return value\ndoes not change unless a call is made to advance_mut or any other\nfunction that is documented to change the BufMut’s current position.': f'<code>remaining_mut</code> 的实现应确保返回值不会改变，除非调用了 <code>advance_mut</code> 或任何其他文档明确会改变 <code>BufMut{RSQUO}s</code> 当前位置的函数。',

    'Returns a mutable slice starting at the current BufMut position and of\nlength between 0 and BufMut::remaining_mut(). Note that this can be shorter than the\nwhole remainder of the buffer (this allows non-continuous implementation).': '返回从当前 <code>BufMut</code> 位置开始、长度介于 0 和 <code>BufMut::remaining_mut()</code> 之间的可变切片。注意这可能比缓冲区剩余总量更短（允许非连续的内部实现）。',

    'This function should never panic. chunk_mut() should return an empty\nslice if and only if remaining_mut() returns 0. In other words,\nchunk_mut() returning an empty slice implies that remaining_mut() will\nreturn 0 and remaining_mut() returning 0 implies that chunk_mut() will\nreturn an empty slice': '此函数不应 panic。<code>chunk_mut()</code> 返回空切片当且仅当 <code>remaining_mut()</code> 返回 0。换言之，<code>chunk_mut()</code> 返回空切片意味着 <code>remaining_mut()</code> 将返回 0，而 <code>remaining_mut()</code> 返回 0 意味着 <code>chunk_mut()</code> 将返回空切片。',

    'This function returns a new value which implements Write by adapting\nthe Write trait functions to the BufMut trait functions. Given that\nBufMut operations are infallible, none of the Write functions will\nreturn with Err.': '此函数返回一个新值，通过将 <code>Write</code> trait 函数适配到 <code>BufMut</code> trait 函数来实现 <code>Write</code>。由于 <code>BufMut</code> 操作是 infallible 的，<code>Write</code> 函数都不会返回 <code>Err</code>。',
})

with open('bytes/_buf_translations.json', 'w', encoding='utf-8') as f:
    json.dump(T, f, ensure_ascii=False, indent=2)

print(f'Total: {len(T)}')