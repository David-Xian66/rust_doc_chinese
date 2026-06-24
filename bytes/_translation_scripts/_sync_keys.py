"""Sync translation keys with actual data text.

For each unmatched entry, use the actual stripped text as the key.
Map to Chinese translation (manually).
"""
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('bytes/_untranslated_own_p.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Manual translations for all unmatched
UNMATCHED_TRANSLATIONS = {
    # struct.Bytes.html
    ('struct.Bytes.html', 'method.from_owner'): {
        'full_p_prefix': 'The owner will be transferred to the constructed Bytes object',
        'zh': 'owner 将被转移到已构造的 <a href="struct.Bytes.html" title="struct bytes::Bytes">Bytes</a> 对象中，确保在已构造对象的所有剩余克隆都被丢弃后被释放。然后 owner 将负责释放指定的内存。',
    },
    ('struct.Bytes.html', 'method.split_off'): {
        'full_p_prefix': 'Afterwards self contains elements [0, at), and the returned Bytes',
        'zh': '此后 <code>self</code> 包含元素 <code>[0, at)</code>，返回的 <code>Bytes</code> 包含元素 <code>[at, len)</code>。保证内存不会移动，即 <code>self</code> 的地址不变，且返回切片的地址也不变。',
    },
    ('struct.Bytes.html', 'method.try_into_mut'): {
        'full_p_prefix': 'If self is unique for the entire original buffer, this will succeed',
        'zh': '若 <code>self</code> 在整个原始缓冲区中是唯一的，则此调用成功，并返回包含 <code>self</code> 内容（无拷贝）的 <code>BytesMut</code>。若 <code>self</code> 在整个原始缓冲区中不是唯一的，则此调用失败并返回 self。',
    },
    ('struct.Bytes.html', 'method.from-4'): {
        'full_p_prefix': 'If bytes is unique for the entire original buffer, this will return a',
        'zh': '若 <code>bytes</code> 在整个原始缓冲区中是唯一的，则返回包含 <code>bytes</code> 内容（无拷贝）的 <code>BytesMut</code>。若 <code>bytes</code> 在整个原始缓冲区中不是唯一的，则会对原始缓冲区中 <code>bytes</code> 子集进行复制。',
    },

    # struct.BytesMut.html
    ('struct.BytesMut.html', 'method.freeze'): {
        'full_p_prefix': 'The conversion is zero cost and is used to indicate that the slice',
        'zh': '此转换零开销，用于表示句柄所引用的切片将不再被修改。转换完成后，句柄可被克隆并在线程间共享。',
    },
    ('struct.BytesMut.html', 'method.split_off'): {
        'full_p_prefix': 'Afterwards self contains elements [0, at), and the returned',
        'zh': '此后 <code>self</code> 包含元素 <code>[0, at)</code>，返回的 <code>BytesMut</code> 包含元素 <code>[at, capacity)</code>。保证内存不会移动，即 <code>self</code> 的地址不变，且返回切片的地址也不变。',
    },
    ('struct.BytesMut.html', 'method.reserve'): {
        'full_p_prefix': 'Before allocating new buffer space, the function will attempt to reclaim',
        'zh': '在分配新缓冲区空间之前，本函数会尝试回收现有缓冲区中的空间。若当前句柄引用的是较大原始缓冲区的视图，并且引用同一原始缓冲区其他部分的所有其他句柄都已丢弃，则当前视图可被复制到缓冲区开头。',
    },
    ('struct.BytesMut.html', 'method.reserve'): {
        'full_p_prefix': 'This optimization will only happen if shifting the data from the current',
        'zh': '仅当将数据从当前视图移动到缓冲区开头的（摊销）时间开销不太大时，才会执行此优化。具体条件可能会变化；目前要求被移动数据的长度至少与：',
    },
    ('struct.BytesMut.html', 'method.unsplit'): {
        'full_p_prefix': 'If the two BytesMut objects were previously contiguous and not mutated',
        'zh': '若两个 <code>BytesMut</code> 对象先前是连续的，且未以导致重新分配的方式被修改，即 <code>other</code> 是通过对此 <code>BytesMut</code> 调用 <code>split_off</code> 创建的，则此操作为 <code>O(1)</code>，仅减少引用计数并设置一些索引。否则此方法的行为与将 <code>other</code> 的字节追加到 <code>self</code> 末尾相同。',
    },
    ('struct.BytesMut.html', 'method.try_unsplit'): {
        'full_p_prefix': 'If the two BytesMut objects were previously contiguous, i.e., if',
        'zh': '若两个 <code>BytesMut</code> 对象先前是连续的，即 <code>other</code> 是通过对此 <code>BytesMut</code> 调用 <code>split_off</code> 创建的，则此操作为 <code>O(1)</code>，仅减少引用计数并设置一些索引。否则此方法的行为与将 <code>other</code> 的字节追加到 <code>self</code> 末尾相同。',
    },
    ('struct.BytesMut.html', 'method.from'): {
        'full_p_prefix': 'If bytes is unique for the entire original buffer, this will return a',
        'zh': '若 <code>bytes</code> 在整个原始缓冲区中是唯一的，则返回包含 <code>bytes</code> 内容（无拷贝）的 <code>BytesMut</code>。若 <code>bytes</code> 在整个原始缓冲区中不是唯一的，则会对原始缓冲区中 <code>bytes</code> 子集进行复制。',
    },
}

# For each unmatched entry, find the actual full_p and use it as the new key
with open('bytes/_buf_translations.json', 'r', encoding='utf-8') as f:
    T = json.load(f)

for path, entries in data.items():
    # Build id-keyed translations for this path
    path_trans = {}
    for (p, id_), info in UNMATCHED_TRANSLATIONS.items():
        if p == path:
            path_trans.setdefault(id_, []).append(info)

    for entry in entries:
        id_ = entry['id']
        if id_ not in path_trans:
            continue
        full_p = entry['full_p']
        stripped = entry['text'].strip()
        # Find which translation to apply
        for info in path_trans[id_]:
            if info['full_p_prefix'] in stripped or stripped.startswith(info['full_p_prefix']):
                # Add new key with actual full text
                T[stripped] = info['zh']
                break

with open('bytes/_buf_translations.json', 'w', encoding='utf-8') as f:
    json.dump(T, f, ensure_ascii=False, indent=2)

print(f'Total: {len(T)}')