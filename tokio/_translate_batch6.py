"""Batch 6: regex-based translation of read_uN/read_iN.

Uses regex sub on bytes with flexible whitespace to handle line wrapping.
"""
import os, re

TOKIO_ROOT = 'D:/Administrator/Documents/Code/rust_doc_all/tokio'


def make_re_pattern_and_repl_read_int(w, signed, endian):
    """Create regex pattern and replacement."""
    article = 'a' if signed == 'signed' else 'an'
    # Match: <p>Reads <article> <signed> <w>-bit integer in <endian> order from the\s+underlying reader.</p>
    pattern_str = rf'<p>Reads {article} {signed} {w}-bit integer in {endian} order from the\s+underlying reader\.</p>'
    endian_zh = '大' if endian == 'big-endian' else '小'
    signed_zh = '无' if signed == 'unsigned' else '有'
    repl = f'<p>以{endian_zh}端字节序从底层 reader 读取一个{signed_zh}符号 {w} 位整数。</p>'
    return re.compile(pattern_str.encode('utf-8')), repl.encode('utf-8')


def make_re_pattern_and_repl_write_int(w, signed, endian):
    article = 'a' if signed == 'signed' else 'an'
    pattern_str = rf'<p>Writes {article} {signed} {w}-bit integer in {endian} order to the\s+underlying writer\.</p>'
    endian_zh = '大' if endian == 'big-endian' else '小'
    signed_zh = '无' if signed == 'unsigned' else '有'
    repl = f'<p>以{endian_zh}端字节序将一个{signed_zh}符号 {w} 位整数写入底层 writer。</p>'
    return re.compile(pattern_str.encode('utf-8')), repl.encode('utf-8')


def make_re_pattern_and_repl_read_float(w, endian):
    pattern_str = rf'<p>Reads an {w}-bit floating point type in {endian} order from the\s+underlying reader\.</p>'
    endian_zh = '大' if endian == 'big-endian' else '小'
    repl = f'<p>以{endian_zh}端字节序从底层 reader 读取一个 {w} 位浮点数。</p>'
    return re.compile(pattern_str.encode('utf-8')), repl.encode('utf-8')


def make_re_pattern_and_repl_write_float(w, endian):
    pattern_str = rf'<p>Writes {w}-bit floating point type in {endian} order to the\s+underlying writer\.</p>'
    endian_zh = '大' if endian == 'big-endian' else '小'
    repl = f'<p>以{endian_zh}端字节序将一个 {w} 位浮点数写入底层 writer。</p>'
    return re.compile(pattern_str.encode('utf-8')), repl.encode('utf-8')


def make_re_pattern_and_repl_read8():
    pairs = []
    # read_u8: <p>Reads an unsigned 8 bit integer from the underlying reader.</p>
    pairs.append((
        re.compile(rb'<p>Reads an unsigned 8 bit integer from the\s+underlying reader\.</p>'),
        '<p>从底层 reader 读取一个无符号 8 位整数。</p>'.encode('utf-8')
    ))
    # read_i8: "a" or "an"
    pairs.append((
        re.compile(rb'<p>Reads an? signed 8 bit integer from the\s+underlying reader\.</p>'),
        '<p>从底层 reader 读取一个有符号 8 位整数。</p>'.encode('utf-8')
    ))
    return pairs


def make_re_pattern_and_repl_write8():
    pairs = []
    pairs.append((
        re.compile(rb'<p>Writes an unsigned 8 bit integer to the\s+underlying writer\.</p>'),
        '<p>将一个无符号 8 位整数写入底层 writer。</p>'.encode('utf-8')
    ))
    pairs.append((
        re.compile(rb'<p>Writes an? signed 8 bit integer to the\s+underlying writer\.</p>'),
        '<p>将一个有符号 8 位整数写入底层 writer。</p>'.encode('utf-8')
    ))
    return pairs


PATTERNS = []  # (compiled_regex, repl_bytes)
PATTERNS.extend(make_re_pattern_and_repl_read8())
PATTERNS.extend(make_re_pattern_and_repl_write8())
for w in [16, 32, 64, 128]:
    for signed in ['unsigned', 'signed']:
        for endian in ['big-endian', 'little-endian']:
            PATTERNS.append(make_re_pattern_and_repl_read_int(w, signed, endian))
            PATTERNS.append(make_re_pattern_and_repl_write_int(w, signed, endian))
for w in [32, 64]:
    for endian in ['big-endian', 'little-endian']:
        PATTERNS.append(make_re_pattern_and_repl_read_float(w, endian))
        PATTERNS.append(make_re_pattern_and_repl_write_float(w, endian))


def main():
    hits = 0
    modified = 0
    missed = []
    for dp, dirs, files in os.walk(TOKIO_ROOT):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__' and not d.endswith('_old')]
        for f in files:
            if not f.endswith('.html'):
                continue
            path = os.path.join(dp, f)
            with open(path, 'rb') as fh:
                raw = fh.read()
            new = raw
            local_hits = 0
            for pat, repl in PATTERNS:
                if pat.search(new):
                    cnt = len(pat.findall(new))
                    new = pat.sub(repl, new)
                    local_hits += cnt
            if new != raw:
                with open(path, 'wb') as fh:
                    fh.write(new)
                modified += 1
                hits += local_hits

    for pat, _ in PATTERNS:
        found = False
        for dp, dirs, files in os.walk(TOKIO_ROOT):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__' and not d.endswith('_old')]
            for f in files:
                if not f.endswith('.html'):
                    continue
                with open(os.path.join(dp, f), 'rb') as fh:
                    if pat.search(fh.read()):
                        found = True
                        break
            if found:
                break
        if not found:
            missed.append(pat.pattern[:80].decode('utf-8', errors='replace'))

    print(f'Modified files: {modified}')
    print(f'Pair matches (total): {hits}')
    print(f'Patterns never applied: {len(missed)}')
    for m in missed[:20]:
        print(f'  {m!r}')


if __name__ == '__main__':
    main()