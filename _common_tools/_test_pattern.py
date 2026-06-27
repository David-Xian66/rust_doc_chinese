import sys, re, time
sys.path.insert(0, '_common_tools')
from _translate_with_bs4 import TRANSLATION_PAIRS, replace_inline_tags_with_placeholders, restore_placeholders

inner = 'A <code>BarrierWaitResult</code> is returned by <code>wait</code> when all tasks in the <code>Barrier</code> have rendezvoused.'
ph, tags = replace_inline_tags_with_placeholders(inner)
print('Placeholdered:', repr(ph[:100]))

PH_ANY = r'\x01\d+\x02*'

def build_pattern(en):
    escaped = re.escape(en)
    parts = []
    i = 0
    while i < len(escaped):
        # Check for escape sequence
        if escaped[i] == '\\' and i + 1 < len(escaped):
            parts.append(escaped[i:i+2])
            i += 2
        else:
            parts.append(escaped[i])
            i += 1
    return ''.join(p + PH_ANY for p in parts)

en = 'A BarrierWaitResult is returned by wait when all tasks in the Barrier have rendezvoused.'
pat = build_pattern(en)
print('Pattern:', repr(pat[:200]))
print('Pattern len:', len(pat))

# Compile and test
start = time.time()
compiled = re.compile(pat)
result = compiled.sub('CHINESE', ph)
print(f'Compiled in {time.time()-start:.3f}s')
print('Sub result:', repr(result))

# Try with all pairs combined
print(f'\nTotal pairs: {len(TRANSLATION_PAIRS)}')
# Bucket by length
len_buckets = {}
for e, z in TRANSLATION_PAIRS:
    len_buckets.setdefault(len(e), []).append((e, z))
print(f'Length buckets: {sorted(len_buckets.keys())}')

# Test on biggest bucket
biggest_len = max(len_buckets.keys())
biggest_bucket = len_buckets[biggest_len]
print(f'Biggest bucket: length={biggest_len}, count={len(biggest_bucket)}')

start = time.time()
sorted_bucket = sorted(biggest_bucket, key=lambda x: -len(x[0]))
pattern_parts = []
en_to_zh = {}
for idx, (e, z) in enumerate(sorted_bucket):
    pattern_parts.append(f'(?P<E{idx}>{build_pattern(e)})')
    en_to_zh[f'E{idx}'] = (e, z)
big_pattern = '|'.join(pattern_parts)
print(f'Big pattern length: {len(big_pattern)}')
compiled_big = re.compile(big_pattern)
print(f'Compiled in {time.time()-start:.3f}s')

start = time.time()
result2 = compiled_big.sub('XXX', ph)
print(f'Sub on ph: {time.time()-start:.3f}s')
print('Sub result:', repr(result2[:100]))