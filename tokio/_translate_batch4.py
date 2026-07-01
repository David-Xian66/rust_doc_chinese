"""Batch 4: translate AsyncReadExt/AsyncWriteExt's read_uN/write_uN methods.

Patterns:
- read_u8 / read_i8: no big/little endian suffix
- read_uN / read_iN (16+): "in big-endian order" or "in little-endian order"
- read_fN: floating point
- write_u8 / write_i8: same pattern
"""
import os, re

TOKIO_ROOT = 'D:/Administrator/Documents/Code/rust_doc_all/tokio'

def b(s):
    return s.replace('\n', '\r\n').encode('utf-8')

def c(s):
    return s.replace('\n', '\r\n').encode('utf-8')


def gen_pattern_and_repl_read8():
    """8-bit reads have no big/little endian."""
    return [
        (b('<p>Reads an unsigned 8 bit integer from the underlying reader.</p>'),
         c('<p>从底层 reader 读取一个无符号 8 位整数。</p>')),
        (b('<p>Reads a signed 8 bit integer from the underlying reader.</p>'),
         c('<p>从底层 reader 读取一个有符号 8 位整数。</p>')),
    ]


def gen_pattern_and_repl_write8():
    return [
        (b('<p>Writes an unsigned 8 bit integer to the underlying writer.</p>'),
         c('<p>将一个无符号 8 位整数写入底层 writer。</p>')),
        (b('<p>Writes a signed 8 bit integer to the underlying writer.</p>'),
         c('<p>将一个有符号 8 位整数写入底层 writer。</p>')),
    ]


def gen_pattern_and_repl_int(widths, suffix_be=True):
    """Generate patterns for read_uN/read_iN (N = 16, 32, 64, 128) BE/LE."""
    pairs = []
    for w in widths:
        for signed in ['unsigned', 'signed']:
            # Signed uses "a signed" (article), unsigned uses "an unsigned"
            article = 'a' if signed == 'signed' else 'an'
            for endian in ['big-endian', 'little-endian']:
                if endian == 'big-endian' and not suffix_be:
                    continue
                if endian == 'little-endian' and suffix_be:
                    continue
                en_text = f'<p>Reads {article} {signed} {w}-bit integer in {endian} order from the underlying reader.</p>'
                zh_text = f'<p>以{"大" if endian == "big-endian" else "小"}端字节序从底层 reader 读取一个{"无" if signed == "unsigned" else "有"}符号 {w} 位整数。</p>'
                pairs.append((b(en_text), c(zh_text)))
    return pairs


def gen_pattern_and_repl_write_int(widths, suffix_be=True):
    """Generate patterns for write_uN/write_iN BE/LE."""
    pairs = []
    for w in widths:
        for signed in ['unsigned', 'signed']:
            article = 'a' if signed == 'signed' else 'an'
            for endian in ['big-endian', 'little-endian']:
                if endian == 'big-endian' and not suffix_be:
                    continue
                if endian == 'little-endian' and suffix_be:
                    continue
                en_text = f'<p>Writes {article} {signed} {w}-bit integer in {endian} order to the underlying writer.</p>'
                zh_text = f'<p>以{"大" if endian == "big-endian" else "小"}端字节序将一个{"无" if signed == "unsigned" else "有"}符号 {w} 位整数写入底层 writer。</p>'
                pairs.append((b(en_text), c(zh_text)))
    return pairs


def gen_pattern_and_repl_float(widths, suffix_be=True):
    """Generate patterns for read_fN/write_fN BE/LE."""
    pairs = []
    for w in widths:
        article = 'a' if w == 32 else 'a'  # both 32 and 64 take "a" (a 32/64-bit)
        for endian in ['big-endian', 'little-endian']:
            if endian == 'big-endian' and not suffix_be:
                continue
            if endian == 'little-endian' and suffix_be:
                continue
            en_text = f'<p>Reads {article} {w}-bit floating point type in {endian} order from the underlying reader.</p>'
            zh_text = f'<p>以{"大" if endian == "big-endian" else "小"}端字节序从底层 reader 读取一个 {w} 位浮点数。</p>'
            pairs.append((b(en_text), c(zh_text)))
    return pairs


def gen_pattern_and_repl_write_float(widths, suffix_be=True):
    pairs = []
    for w in widths:
        for endian in ['big-endian', 'little-endian']:
            if endian == 'big-endian' and not suffix_be:
                continue
            if endian == 'little-endian' and suffix_be:
                continue
            en_text = f'<p>Writes {w}-bit floating point type in {endian} order to the underlying writer.</p>'
            zh_text = f'<p>以{"大" if endian == "big-endian" else "小"}端字节序将一个 {w} 位浮点数写入底层 writer。</p>'
            pairs.append((b(en_text), c(zh_text)))
    return pairs


# Build all pairs
PAIRS = []
PAIRS.extend(gen_pattern_and_repl_read8())
PAIRS.extend(gen_pattern_and_repl_write8())
# AsyncReadExt: read_u16, read_u32, read_u64, read_u128 in BE; read_u16_le etc. in LE
PAIRS.extend(gen_pattern_and_repl_int([16, 32, 64, 128], suffix_be=True))
PAIRS.extend(gen_pattern_and_repl_int([16, 32, 64, 128], suffix_be=False))
PAIRS.extend(gen_pattern_and_repl_float([32, 64], suffix_be=True))
PAIRS.extend(gen_pattern_and_repl_float([32, 64], suffix_be=False))
# AsyncWriteExt: write_u16, write_u32, etc.
PAIRS.extend(gen_pattern_and_repl_write_int([16, 32, 64, 128], suffix_be=True))
PAIRS.extend(gen_pattern_and_repl_write_int([16, 32, 64, 128], suffix_be=False))
PAIRS.extend(gen_pattern_and_repl_write_float([32, 64], suffix_be=True))
PAIRS.extend(gen_pattern_and_repl_write_float([32, 64], suffix_be=False))


def main():
    hits = 0
    modified = 0
    missed_pairs = []
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
            for old, zn in PAIRS:
                if old in new:
                    new = new.replace(old, zn)
                    local_hits += 1
            if new != raw:
                with open(path, 'wb') as fh:
                    fh.write(new)
                modified += 1
                hits += local_hits

    # Verify each pair was applied at least once
    for old, _ in PAIRS:
        found = False
        for dp, dirs, files in os.walk(TOKIO_ROOT):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__' and not d.endswith('_old')]
            for f in files:
                if not f.endswith('.html'):
                    continue
                with open(os.path.join(dp, f), 'rb') as fh:
                    if old in fh.read():
                        found = True
                        break
            if found:
                break
        if not found:
            missed_pairs.append(old[:80].decode('utf-8', errors='replace'))

    print(f'Modified files: {modified}')
    print(f'Pair matches (total): {hits}')
    print(f'Pairs never applied: {len(missed_pairs)}')
    for m in missed_pairs[:20]:
        print(f'  {m!r}')


if __name__ == '__main__':
    main()