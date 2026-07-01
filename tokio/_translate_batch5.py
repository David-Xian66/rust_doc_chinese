"""Batch 5: handle line-wrapped read_uN/read_iN patterns.

rustdoc wraps lines at ~80 chars. The actual format is:
<p>Reads an unsigned 16-bit integer in big-endian order from the
underlying reader.</p>
"""
import os, re

TOKIO_ROOT = 'D:/Administrator/Documents/Code/rust_doc_all/tokio'

def b(s):
    return s.replace('\n', '\r\n').encode('utf-8')

def c(s):
    return s.replace('\n', '\r\n').encode('utf-8')


def gen_read8_pairs():
    """8-bit reads have no big/little endian and may have line wrap."""
    return [
        # read_u8
        (b('<p>Reads an unsigned 8 bit integer from the underlying reader.</p>'),
         c('<p>从底层 reader 读取一个无符号 8 位整数。</p>')),
        # read_i8 - "Reads a signed 8 bit integer from the underlying reader." OR "Reads an signed 8 bit integer from the underlying reader."
        (b('<p>Reads a signed 8 bit integer from the underlying reader.</p>'),
         c('<p>从底层 reader 读取一个有符号 8 位整数。</p>')),
        (b('<p>Reads an signed 8 bit integer from the underlying reader.</p>'),
         c('<p>从底层 reader 读取一个有符号 8 位整数。</p>')),
    ]


def gen_write8_pairs():
    return [
        (b('<p>Writes an unsigned 8 bit integer to the underlying writer.</p>'),
         c('<p>将一个无符号 8 位整数写入底层 writer。</p>')),
        (b('<p>Writes a signed 8 bit integer to the underlying writer.</p>'),
         c('<p>将一个有符号 8 位整数写入底层 writer。</p>')),
        (b('<p>Writes an signed 8 bit integer to the underlying writer.</p>'),
         c('<p>将一个有符号 8 位整数写入底层 writer。</p>')),
    ]


def gen_read_int_pairs():
    """read_uN/read_iN with line wrap. The wrap is at 'from the' -> 'underlying'."""
    pairs = []
    for w in [16, 32, 64, 128]:
        for signed in ['unsigned', 'signed']:
            article = 'a' if signed == 'signed' else 'an'
            for endian in ['big-endian', 'little-endian']:
                endian_zh = '大' if endian == 'big-endian' else '小'
                signed_zh = '无' if signed == 'unsigned' else '有'
                # Two forms: line wrap and no wrap
                en_wrapped = f'<p>Reads {article} {signed} {w}-bit integer in {endian} order from the underlying reader.</p>'
                en_unwrapped = f'<p>Reads {article} {signed} {w}-bit integer in {endian} order from the\r\nunderlying reader.</p>'
                zh_text = f'<p>以{endian_zh}端字节序从底层 reader 读取一个{signed_zh}符号 {w} 位整数。</p>'
                pairs.append((b(en_wrapped), c(zh_text)))
                pairs.append((b(en_unwrapped), c(zh_text)))
    return pairs


def gen_write_int_pairs():
    pairs = []
    for w in [16, 32, 64, 128]:
        for signed in ['unsigned', 'signed']:
            article = 'a' if signed == 'signed' else 'an'
            for endian in ['big-endian', 'little-endian']:
                endian_zh = '大' if endian == 'big-endian' else '小'
                signed_zh = '无' if signed == 'unsigned' else '有'
                en_wrapped = f'<p>Writes {article} {signed} {w}-bit integer in {endian} order to the underlying writer.</p>'
                en_unwrapped = f'<p>Writes {article} {signed} {w}-bit integer in {endian} order to the\r\nunderlying writer.</p>'
                zh_text = f'<p>以{endian_zh}端字节序将一个{signed_zh}符号 {w} 位整数写入底层 writer。</p>'
                pairs.append((b(en_wrapped), c(zh_text)))
                pairs.append((b(en_unwrapped), c(zh_text)))
    return pairs


def gen_read_float_pairs():
    pairs = []
    for w in [32, 64]:
        for endian in ['big-endian', 'little-endian']:
            endian_zh = '大' if endian == 'big-endian' else '小'
            en_wrapped = f'<p>Reads an {w}-bit floating point type in {endian} order from the underlying reader.</p>'
            en_unwrapped = f'<p>Reads an {w}-bit floating point type in {endian} order from the\r\nunderlying reader.</p>'
            zh_text = f'<p>以{endian_zh}端字节序从底层 reader 读取一个 {w} 位浮点数。</p>'
            pairs.append((b(en_wrapped), c(zh_text)))
            pairs.append((b(en_unwrapped), c(zh_text)))
    return pairs


def gen_write_float_pairs():
    pairs = []
    for w in [32, 64]:
        for endian in ['big-endian', 'little-endian']:
            endian_zh = '大' if endian == 'big-endian' else '小'
            en_wrapped = f'<p>Writes {w}-bit floating point type in {endian} order to the underlying writer.</p>'
            en_unwrapped = f'<p>Writes {w}-bit floating point type in {endian} order to the\r\nunderlying writer.</p>'
            zh_text = f'<p>以{endian_zh}端字节序将一个 {w} 位浮点数写入底层 writer。</p>'
            pairs.append((b(en_wrapped), c(zh_text)))
            pairs.append((b(en_unwrapped), c(zh_text)))
    return pairs


PAIRS = []
PAIRS.extend(gen_read8_pairs())
PAIRS.extend(gen_write8_pairs())
PAIRS.extend(gen_read_int_pairs())
PAIRS.extend(gen_write_int_pairs())
PAIRS.extend(gen_read_float_pairs())
PAIRS.extend(gen_write_float_pairs())


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