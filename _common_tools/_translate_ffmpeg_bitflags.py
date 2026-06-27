"""translate_bitflags.py: 翻译 bitflags crate 生成的标准 docblock 模板。

bitflags 1.x / 2.x 生成的 docblock 经常是分多个 `<p>` 输出，模板之间还可能
有 `<code>` 包裹的内联代码（如 `<code>self</code>`），简单的字符串 replace
匹配不到。本脚本用「剥 HTML 标签 + 规整空白 + 模式匹配」的方式翻译。
"""
import os
import re
import sys

# (正则模式, 中文翻译) - 模式是剥完 HTML 标签 + 折叠空白后的纯文本
# 关键规整规则：
# 1. 句末标点前可能有空格（如 "self ." → "self."）
# 2. `&amp;` 已通过 html.unescape 解码为 `&`
# 3. U+2019 撇号已规范为 ASCII '
# 4. <code>...</code> 已剥掉，只剩内文本
BITFLAGS_PATTERNS = [
    # Get a flags value with all bits unset
    (r'^Get a flags value with all bits unset\s*\.$',
     '获取一个所有位均为 0 的 flags 值。'),
    # Get a flags value with all known bits set
    (r'^Get a flags value with all known bits set\s*\.$',
     '获取一个所有已知位均为 1 的 flags 值。'),
    # Get the underlying bits value...
    (r'^Get the underlying bits value\s*\.\s+The returned value is exactly the bits set in this flags value\s*\.$',
     '获取底层的位值。返回值正是该 flags 值中已设置的位。'),
    # Convert from a bits value...
    (r'^Convert from a bits value\s*\.\s+This method will return None if any unknown bits are set\s*\.$',
     '从位值转换。若设置了任何未知位，则该方法将返回 None。'),
    # Convert from a bits value, unsetting any unknown bits
    (r'^Convert from a bits value, unsetting any unknown bits\s*\.$',
     '从位值转换，未知的位会被清除。'),
    # Convert from a bits value exactly
    (r'^Convert from a bits value exactly\s*\.$',
     '按位值原样转换（保留所有位）。'),
    # Get a flags value with the bits of a flag with the given name set...
    (r'^Get a flags value with the bits of a flag with the given name set\s*\.\s+This method will return None if name is empty or doesn\'t correspond to any named flag\s*\.$',
     '获取一个 flags 值，其位为具有给定名称的 flag 所对应的位。若 name 为空或不与任何已命名的 flag 对应，则该方法将返回 None。'),
    # Whether all bits in self are unset
    (r'^Whether all bits in self are unset\s*\.$',
     '判断 self 中的所有位是否都未设置。'),
    # Whether all known bits in this flags value are set
    (r'^Whether all known bits in this flags value are set\s*\.$',
     '判断该 flags 值的所有已知位是否都已设置。'),
    # Whether any set bits in other are also set in self
    (r'^Whether any set bits in other are also set in self\s*\.$',
     '判断 other 中是否至少有一位也在 self 中被设置。'),
    # Whether all set bits in other are also set in self
    (r'^Whether all set bits in other are also set in self\s*\.$',
     '判断 other 中所有已设置的位是否都在 self 中被设置（即 self ⊇ other）。'),
    # The bitwise or ( | ) of the bits in self and other
    (r'^The bitwise or \( \| \) of the bits in self and other\s*\.$',
     'self 与 other 的按位或（|）。'),
    # The bitwise and ( & ) of the bits in self and other
    (r'^The bitwise and \( & \) of the bits in self and other\s*\.$',
     'self 与 other 的按位与（&）。'),
    # The bitwise exclusive-or ( ^ ) of the bits in self and other
    (r'^The bitwise exclusive-or \( \^ \) of the bits in self and other\s*\.$',
     'self 与 other 的按位异或（^）。'),
    # The intersection of self with the complement of other ( &! )... (remove/difference/sub)
    (r'^The intersection of self with the complement of other \( &! \)\s*\.\s+This method is not equivalent to self & !other when other has unknown bits set\s*\.\s+(?:remove|difference|sub) won\'t truncate other , but the ! operator will\s*\.$',
     'self 与 other 的补的交集（&!）。当 other 含有未知位时，该方法不等价于 self & !other。该方法不会截断 other，而 ! 运算符会。'),
    # The intersection of self with the complement of other ( &! )
    (r'^The intersection of self with the complement of other \( &! \)\s*\.$',
     'self 与 other 的补的交集（&!）。'),
    # The bitwise complement ( ~ )
    (r'^The bitwise complement \( ~ \) of this flags value\s*\.$',
     '该 flags 值的按位取反（~）。'),
    # The bitwise negation ( ! ) of the bits in self, truncating the result
    (r'^The bitwise negation \( ! \) of the bits in self , truncating the result\s*\.$',
     '对 self 的位按位取反（!），并截断结果。'),
    # Call insert when value is true or remove when value is false
    (r'^Call insert when value is true or remove when value is false\s*\.$',
     '当 value 为 true 时调用 insert，当 value 为 false 时调用 remove。'),
    # Yield a set of contained named flags values
    (r'^Yield a set of contained named flags values\s*\.$',
     '逐个产出该 flags 值中所包含的已命名 flag。'),
    # Yield a set of contained named flags values along with their names
    (r'^Yield a set of contained named flags values along with their names\s*\.$',
     '逐个产出该 flags 值中所包含的已命名 flag 及其名称。'),
    # Each yielded flags value will correspond to a defined named flag...
    (r'^Each yielded flags value will correspond to a defined named flag\s*\.\s+Any unknown bits will be yielded together as a final flags value\s*\.$',
     '每个产出的 flag 值对应一个已定义的具名 flag。任何未知位将作为最终的 flags 值一起产出。'),
    # The value of all known bits, i.e. the value of `Self::all()` at compile-time
    (r'^The value of all known bits, i\.e\. the value of `Self::all\(\)` at compile-time\s*\.$',
     '所有已知位的值，即编译期 `Self::all()` 的值。'),
    # Returns the number of flags stored in self
    (r'^Returns the number of flags stored in self\s*\.$',
     '返回 self 中存储的 flag 个数。'),
    # The bitwise or ( | ) of the bits in each flags value
    (r'^The bitwise or \( \| \) of the bits in each flags value\s*\.$',
     '对每个 flags 值按位取或（|）。'),

    # ===== ffmpeg resampling context 专用 =====
    (r'^Create a resampler with the given definitions\s*\.$',
     '使用给定的定义创建一个重采样器。'),
    (r'^Create a resampler with the given definitions and custom options dictionary\s*\.$',
     '使用给定的定义与自定义选项字典创建一个重采样器。'),
    (r'^Get the input definition\s*\.$',
     '获取输入定义。'),
    (r'^Get the output definition\s*\.$',
     '获取输出定义。'),
    (r'^Get the remaining delay\s*\.$',
     '获取剩余延迟。'),
    (r'^Run the resampler from the given input to the given output\s*\.\s+When there are internal frames to process it will return Ok\(Some\(Delay \{ \.\. \}\)\)\s*\.$',
     '使用给定的输入与输出运行重采样器。当存在待处理的内部帧时，'
     '它将返回 Ok(Some(Delay { .. }))。'),
    (r'^Convert one of the remaining internal frames\s*\.\s+When there are no more internal frames Ok\(None\) will be returned\s*\.$',
     '转换一个剩余的内部帧。当不再有内部帧时，返回 Ok(None)。'),

    # ===== ffmpeg decoder/encoder flush =====
    (r'^Sends a NULL packet to the decoder to signal end of stream and enter\s+draining mode\s*\.$',
     '向解码器发送一个 NULL 包以表示流的结束并进入排空模式。'),
    (r'^Sends a NULL packet to the encoder to signal end of stream and enter\s+draining mode\s*\.$',
     '向编码器发送一个 NULL 包以表示流的结束并进入排空模式。'),

    # ===== ffmpeg util error Other variant =====
    (r'^For AVERROR\(e\) wrapping POSIX error codes, e\.g\. AVERROR\(EAGAIN\)\s*\.$',
     '用于包装 POSIX 错误码的 AVERROR(e)，例如 AVERROR(EAGAIN)。'),
]

# 每个 (pattern, zh) 一一对应 pre-translated
COMPILED = [(re.compile(p, re.MULTILINE | re.DOTALL), zh) for p, zh in BITFLAGS_PATTERNS]


def normalize(text):
    """剥 HTML 标签 + 折叠空白 + 解 HTML 实体，返回纯文本。"""
    import html
    text = html.unescape(text)
    text = re.sub(r'<[^>]+>', ' ', text)
    # U+2019 right single quote -> ASCII
    text = text.replace('’', "'")
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_docblock_text(docblock_html):
    """把 docblock 内所有 <p> 文本拼起来（剥 HTML），返回 (full_text, list_of_p_texts)。"""
    p_texts = re.findall(r'<p[^>]*>([\s\S]*?)</p>', docblock_html)
    full = ' '.join(normalize(t) for t in p_texts)
    return full, p_texts


def translate_docblock(docblock_html):
    """对 docblock 检查是否有可翻译的多段组合。返回 (new_html, changed_count)。"""
    full_text, _ = extract_docblock_text(docblock_html)
    for pattern, zh in COMPILED:
        if pattern.match(full_text):
            # 把整个 docblock 替换成单一段翻译
            return f'<p>{zh}</p>', 1
    return docblock_html, 0


def scan_and_translate(crate_dir):
    total_files = 0
    total_mod = 0
    total_repl = 0
    for root, dirs, fs in os.walk(crate_dir):
        for fn in fs:
            if not fn.endswith('.html'):
                continue
            path = os.path.join(root, fn)
            with open(path, 'rb') as f:
                raw = f.read()
            try:
                content = raw.decode('utf-8')
            except UnicodeDecodeError:
                continue
            total_files += 1
            file_repl = 0
            # 用嵌套深度追踪找 docblock。每次替换后从头重新扫描。
            changed = True
            while changed:
                changed = False
                for m in re.finditer(r'<div class=[\'"]docblock[\'"]>', content):
                    start = m.end()
                    depth = 1
                    pos = start
                    while pos < len(content) and depth > 0:
                        next_open = content.find('<div', pos)
                        next_close = content.find('</div>', pos)
                        if next_close == -1:
                            break
                        if next_open != -1 and next_open < next_close:
                            depth += 1
                            pos = next_open + 4
                        else:
                            depth -= 1
                            pos = next_close + 6
                    end = pos - 6  # before </div>
                    db_html = content[start:end]
                    new_db, count = translate_docblock(db_html)
                    if count > 0:
                        content = content[:start] + new_db + content[end:]
                        file_repl += count
                        changed = True
                        break  # 从头重新扫描
            if file_repl > 0:
                with open(path, 'wb') as f:
                    f.write(content.encode('utf-8'))
                total_mod += 1
                total_repl += file_repl
                print('  %s: %d replacements' % (os.path.relpath(path, crate_dir), file_repl))
    print('\nScanned %d HTML files, modified %d, total %d replacements' % (total_files, total_mod, total_repl))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python _translate_ffmpeg_bitflags.py <crate_dir>')
        sys.exit(1)
    scan_and_translate(sys.argv[1])
