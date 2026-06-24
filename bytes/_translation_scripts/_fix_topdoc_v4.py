"""Fix BufMut top-doc."""
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

TOPDOC = [
    [
        '<p>Write bytes to a buffer</p>',
        '<p>向缓冲区写入字节</p>'
    ],
    [
        '<p>A buffer stores bytes in memory such that write operations are infallible.\nThe underlying storage may or may not be in contiguous memory. A <code>BufMut</code>\nvalue is a cursor into the buffer. Writing to <code>BufMut</code> advances the cursor\nposition.</p>',
        '<p>缓冲区将字节存储在内存中，以便写入操作不会失败。底层存储可能连续也可能不连续。<code>BufMut</code> 值是指向缓冲区的游标。向 <code>BufMut</code> 写入会推进游标位置。</p>'
    ],
    [
        '<p>The simplest <code>BufMut</code> is a <code>Vec&lt;u8&gt;</code>.</p>',
        '<p>最简单的 <code>BufMut</code> 是 <code>Vec&lt;u8&gt;</code>。</p>'
    ],
]

normalized = [[old.replace('\r\n', '\n'), new.replace('\r\n', '\n')] for old, new in TOPDOC]
with open('bytes/_topdoc_apply_v4.json', 'w', encoding='utf-8') as f:
    json.dump(normalized, f, ensure_ascii=False, indent=2)

print(f'Wrote {len(normalized)} pairs')