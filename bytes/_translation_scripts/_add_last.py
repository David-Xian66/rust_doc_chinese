"""Add the last 2 translations."""
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('bytes/_buf_translations.json', 'r', encoding='utf-8') as f:
    T = json.load(f)

T.update({
    'The caller must not read from the referenced memory and must not write\nuninitialized bytes to the slice either. This is because BufMut implementation\nthat created the UninitSlice knows which parts are initialized. Writing uninitialized\nbytes to the slice may cause the BufMut to read those bytes and trigger undefined\nbehavior.': '调用方不得读取所引用的内存，也不得向切片写入未初始化的字节。这是因为创建 <code>UninitSlice</code> 的 <code>BufMut</code> 实现知道哪些部分是初始化的。向切片写入未初始化的字节可能导致 <code>BufMut</code> 之后读取这些字节并触发未定义行为。',

    'This function should never panic. chunk_mut() should return an empty\nslice if and only if remaining_mut() returns 0. In other words,\nchunk_mut() returning an empty slice implies that remaining_mut() will\nreturn 0 and remaining_mut() returning 0 implies that chunk_mut() will\nreturn an empty slice.': '此函数不应 panic。<code>chunk_mut()</code> 返回空切片当且仅当 <code>remaining_mut()</code> 返回 0。换言之，<code>chunk_mut()</code> 返回空切片意味着 <code>remaining_mut()</code> 将返回 0，而 <code>remaining_mut()</code> 返回 0 意味着 <code>chunk_mut()</code> 将返回空切片。',
})

with open('bytes/_buf_translations.json', 'w', encoding='utf-8') as f:
    json.dump(T, f, ensure_ascii=False, indent=2)

print(f'Total: {len(T)}')