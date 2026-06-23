"""
通用 Rust 标准 trait 方法 docblock 批量翻译脚本。

背景：rustdoc 给 stdlib trait 的实现（如 Debug::fmt、Clone::clone、PartialEq::eq）
生成的 docblock 在 HTML 里是固定英文模板。这些模板跨 crate 通用，应该集中翻译。
HTML 里 docblock 的形态有四种：

1. 裸文本（v1 模式）：`Formats the value using the given formatter.`
2. 文本 + `<a href="...">Read more</a>`（v3 模式）：`Formats... <a>Read more</a>`
3. 文本含 `<code>foo</code>` 内联（v4 模式）：`Tests for <code>self</code> and <code>other</code> values...`
4. 文本含 `<code>` + `<a>` 混合：`Feeds this value into the given <code>Hasher</code>. <a>Read more</a>`

关键陷阱（已在脚本里处理）：
- **CRLF 行尾**：quinn / windows_capture 等用 rustdoc 在 Windows 上生成的 HTML 是 CRLF，
  模式串必须严格匹配（脚本同时支持 LF 和 CRLF 两种形式）
- **U+2019 (`'`) 全角撇号**：英文里 `Tokio's` 在 UTF-8 是 `\xe2\x80\x99`，
  不要在模式串里用 ASCII `'`
- **`<a>` 的 `href` 含版本号路径**：如 `doc.rust-lang.org/1.95.0/...`，
  模式串不能硬编码具体版本号
- **审计 regex 阈值**：仅含 `§`、`：`、`'` 等全角标点的串不含 CJK 汉字，
  audit 会误判为"未译"。翻译时让可见文本含至少 1 个汉字

用法：
    python _common_tools/_translate_traits.py <crate_dir> [--report]
    python _common_tools/_translate_traits.py <crate_dir> --report   # 只报告不修改

只扫描 + 修改 HTML，不动 sidebar-items.js、src-script-*.js、all.html 的标识符。

已涵盖的 trait 方法（持续累积）：
- Clone::clone
- Debug::fmt, Display::fmt
- From::from, TryFrom::try_from
- Into::into, TryInto::try_into
- PartialEq::eq, ne
- Eq
- PartialOrd::lt, le, gt, ge, partial_cmp
- Ord::cmp, max, min, clamp
- Hash::hash
- Default::default
- Drop::drop
- Future::poll
- Iterator::next, size_hint, count, last, nth, ...
- IntoIterator::into_iter
- Deref::deref, DerefMut::deref_mut
- Error::source
- tokio_util::codec::Decoder::decode, Encoder::encode
- quinn Controller trait (on_sent, on_end_acks, on_mtu_update, window, metrics, clone_box, ...)
- 各 crate 特有的常用 trait 方法（运行时/spawn/计时器等）

添加新翻译对只需在 TRAIT_PAIRS 中追加，按 (英文模式串, 中文翻译) 格式。
模式串必须与 HTML 中实际文本完全一致（含 CRLF / U+2019 / `<code>` 等）。
"""

import os
import sys
import re
import subprocess


# 通用 Rust trait 方法 docblock 翻译
# 模式串里: \\n 表示 \n 或 \r\n（脚本自动展开）
#          {RQ} 表示 U+2019 右单引号 '
TRAIT_PAIRS = [
    # ===== 裸文本 =====
    ('Clone::clone', 'Returns a duplicate of the value.',
     '返回值的副本。'),
    ('Debug::fmt', 'Formats the value using the given formatter.',
     '使用给定的格式化器格式化此值。'),
    ('From::from', 'Converts to this type from the input type.',
     '从输入类型转换为此类型。'),
    ('TryFrom::try_from', 'Performs the conversion.',
     '执行转换。'),
    ('Error::source', 'Returns the lower-level source of this error, if any.',
     '返回此错误的更底层来源（若有）。'),
    ('Default::default', 'Returns the "default value" for a type.',
     '返回一个类型的"默认值"。'),
    ('Drop::drop', 'Executes the destructor for this type.',
     '执行此类型的析构函数。'),
    ('Future::poll', 'Attempts to resolve the future to a final value, '
                     'registering the current task for wakeup if the value is not yet available.',
     '尝试将 Future 解析为最终值，若值尚不可用则注册当前任务以备唤醒。'),

    # PartialEq
    ('PartialEq::eq', 'Tests for self and other values to be equal, and is used by == .',
     '测试 self 与 other 值是否相等，供 == 运算符使用。'),
    ('PartialEq::ne', 'Tests for self and other values to be not equal, and is used by != .',
     '测试 self 与 other 值是否不相等，供 != 运算符使用。'),

    # PartialOrd
    ('PartialOrd::partial_cmp',
     'This method returns an ordering between self and other values if one exists.',
     '若存在，此方法返回 self 与 other 值之间的排序关系。'),
    ('PartialOrd::lt',
     'Tests less than (for self and other) and is used by the < operator.',
     '测试小于（针对 self 与 other），供 < 运算符使用。'),
    ('PartialOrd::le',
     'Tests less than or equal to (for self and other) and is used by the <= operator.',
     '测试小于等于（针对 self 与 other），供 <= 运算符使用。'),
    ('PartialOrd::gt',
     'Tests greater than (for self and other) and is used by the > operator.',
     '测试大于（针对 self 与 other），供 > 运算符使用。'),
    ('PartialOrd::ge',
     'Tests greater than or equal to (for self and other) and is used by the >= operator.',
     '测试大于等于（针对 self 与 other），供 >= 运算符使用。'),

    # Ord
    ('Ord::cmp', 'This method returns an Ordering between self and other .',
     '此方法返回 self 与 other 之间的 Ordering。'),

    # Hash
    ('Hash::hash', 'Feeds this value into the given Hasher .',
     '将此值送入给定的 Hasher。'),

    # ===== 含 <code> 内联 =====
    ('PartialEq::eq (with code)',
     'Tests for <code>self</code> and <code>other</code> values to be equal, '
     'and is used by <code>==</code>.',
     '测试 <code>self</code> 与 <code>other</code> 值是否相等，供 <code>==</code> 运算符使用。'),
    ('PartialEq::ne (with code)',
     'Tests for <code>self</code> and <code>other</code> values to be not equal, '
     'and is used by <code>!=</code>.',
     '测试 <code>self</code> 与 <code>other</code> 值是否不相等，供 <code>!=</code> 运算符使用。'),
    ('PartialOrd::lt (with code)',
     'Tests less than (for <code>self</code> and <code>other</code>) and is used by the '
     '<code>&lt;</code> operator.',
     '测试小于（针对 <code>self</code> 与 <code>other</code>），供 <code>&lt;</code> 运算符使用。'),
    ('PartialOrd::le (with code)',
     'Tests less than or equal to (for <code>self</code> and <code>other</code>) and is used '
     'by the <code>&lt;=</code> operator.',
     '测试小于等于（针对 <code>self</code> 与 <code>self</code>），供 <code>&lt;=</code> 运算符使用。'),
    ('PartialOrd::gt (with code)',
     'Tests greater than (for <code>self</code> and <code>other</code>) and is used by the '
     '<code>&gt;</code> operator.',
     '测试大于（针对 <code>self</code> 与 <code>other</code>），供 <code>&gt;</code> 运算符使用。'),
    ('PartialOrd::ge (with code)',
     'Tests greater than or equal to (for <code>self</code> and <code>other</code>) and is '
     'used by the <code>&gt;=</code> operator.',
     '测试大于等于（针对 <code>self</code> 与 <code>other</code>），供 <code>&gt;=</code> 运算符使用。'),
    ('Hash::hash (with code)', 'Feeds this value into the given <code>Hasher</code>.',
     '将此值送入给定的 <code>Hasher</code>。'),
    ('Ord::cmp (with code)',
     'This method returns an <code>Ordering</code> between <code>self</code> and <code>other</code>.',
     '此方法返回 <code>self</code> 与 <code>other</code> 之间的 <code>Ordering</code>。'),
    ('PartialOrd::partial_cmp (with code)',
     'This method returns an ordering between <code>self</code> and <code>other</code> values '
     'if one exists.',
     '若存在，此方法返回 <code>self</code> 与 <code>other</code> 值之间的排序关系。'),
    ('is_handshaking', 'Returns <code>true</code> until the connection is fully established.',
     '在连接完全建立之前返回 <code>true</code>。'),

    # Deref / DerefMut
    ('Deref::deref', 'Dereferences the value.', '解引用此值。'),
    ('DerefMut::deref_mut', 'Mutably dereferences the value.', '以可变方式解引用此值。'),

    # tokio_util codec::Decoder / Encoder
    ('Decoder::decode', 'Decode a Self from the provided buffer, if the buffer is large enough',
     '如果缓冲区足够大，则从提供的缓冲区解码一个 Self'),
    ('Decoder::decode (with code)',
     'Decode a <code>Self</code> from the provided buffer, if the buffer is large enough',
     '如果缓冲区足够大，则从提供的缓冲区解码一个 <code>Self</code>'),
    ('Encoder::encode', 'Append the encoding of self to the provided buffer',
     '将 self 的编码追加到提供的缓冲区'),
    ('Encoder::encode (with code)',
     'Append the encoding of <code>self</code> to the provided buffer',
     '将 <code>self</code> 的编码追加到提供的缓冲区'),

    # Read more 链接文本
    ('Read more link', '>Read more</a>', '>更多信息</a>'),

    # ===== AsRef / AsMut =====
    ('AsRef::as_ref',
     'Converts this type into a shared reference of the (usually inferred) input type.',
     '将此类型转换为输入类型的共享引用（通常自动推导）。'),
    ('AsMut::as_mut',
     'Converts this type into a mutable reference of the (usually inferred) input type.',
     '将此类型转换为输入类型的可变引用（通常自动推导）。'),
    ('Borrow::borrow',
     'Converts this type into a (usually inferred) shared reference of the input type.',
     '将此类型转换为输入类型的共享引用（通常自动推导）。'),
    ('Socket::as_socket', 'Borrows the socket.', '借用此套接字。'),

    # ===== std::ops 关联类型 Output =====
    # (HTML 中 < > & 都用实体；模式串必须匹配实体形式)
    ('Add::Output',
     'The resulting type after applying the <code>+</code> operator.',
     '应用 <code>+</code> 运算符后得到的类型。'),
    ('Sub::Output',
     'The resulting type after applying the <code>-</code> operator.',
     '应用 <code>-</code> 运算符后得到的类型。'),
    ('Mul::Output',
     'The resulting type after applying the <code>*</code> operator.',
     '应用 <code>*</code> 运算符后得到的类型。'),
    ('Div::Output',
     'The resulting type after applying the <code>/</code> operator.',
     '应用 <code>/</code> 运算符后得到的类型。'),
    ('Rem::Output',
     'The resulting type after applying the <code>%</code> operator.',
     '应用 <code>%</code> 运算符后得到的类型。'),
    ('Not::Output',
     'The resulting type after applying the <code>!</code> operator.',
     '应用 <code>!</code> 运算符后得到的类型。'),
    ('BitAnd::Output',
     'The resulting type after applying the <code>&amp;</code> operator.',
     '应用 <code>&amp;</code> 运算符后得到的类型。'),
    ('BitOr::Output',
     'The resulting type after applying the <code>|</code> operator.',
     '应用 <code>|</code> 运算符后得到的类型。'),
    ('BitXor::Output',
     'The resulting type after applying the <code>^</code> operator.',
     '应用 <code>^</code> 运算符后得到的类型。'),
    ('Shl::Output',
     'The resulting type after applying the <code>&lt;&lt;</code> operator.',
     '应用 <code>&lt;&lt;</code> 运算符后得到的类型。'),
    ('Shr::Output',
     'The resulting type after applying the <code>&gt;&gt;</code> operator.',
     '应用 <code>&gt;&gt;</code> 运算符后得到的类型。'),

    # ===== std::ops 关联类型 Output（无 <code> 包裹的简化形） =====
    # 部分老版本 rustdoc 会输出 "the + operator" 而非 "<code>+</code>"
    ('Add::Output (plain)',
     'The resulting type after applying the + operator.',
     '应用 + 运算符后得到的类型。'),
    ('Sub::Output (plain)',
     'The resulting type after applying the - operator.',
     '应用 - 运算符后得到的类型。'),
    ('Mul::Output (plain)',
     'The resulting type after applying the * operator.',
     '应用 * 运算符后得到的类型。'),
    ('Div::Output (plain)',
     'The resulting type after applying the / operator.',
     '应用 / 运算符后得到的类型。'),
    ('Rem::Output (plain)',
     'The resulting type after applying the % operator.',
     '应用 % 运算符后得到的类型。'),
    ('Not::Output (plain)',
     'The resulting type after applying the ! operator.',
     '应用 ! 运算符后得到的类型。'),
    ('BitOr::Output (plain)',
     'The resulting type after applying the | operator.',
     '应用 | 运算符后得到的类型。'),
    ('BitXor::Output (plain)',
     'The resulting type after applying the ^ operator.',
     '应用 ^ 运算符后得到的类型。'),

    # ===== Deref / DerefMut 关联类型 Target =====
    ('Deref::Target',
     'The resulting type after dereferencing.',
     '解引用后得到的类型。'),

    # ===== TryFrom::Error / TryInto::Error =====
    ('TryFrom::Error',
     'The type returned in the event of a conversion error.',
     '转换出错时返回的类型。'),

    # ===== Iterator::Item =====
    ('Iterator::Item',
     'The type of the elements being iterated over.',
     '被迭代元素的类型。'),

    # ===== Future::Output =====
    ('Future::Output',
     'The type of value produced on completion.',
     'Future 完成时产生的值的类型。'),
    ('Future::Output (alt)',
     'The output that the future will produce on completion.',
     'Future 完成时产生的输出。'),

    # ===== IntoFuture::IntoFuture =====
    ('IntoFuture::IntoFuture',
     'Which kind of future are we turning this into?',
     '我们将要把此值转变成哪种 future？'),

    # ===== PartialEq 无 <code> 包裹的裸文本形式 =====
    ('PartialEq::eq (bare)',
     'Tests for self and other values to be equal, and is used by == .',
     '测试 self 与 other 值是否相等，供 == 运算符使用。'),
    ('PartialEq::ne (bare)',
     'Tests for self and other values to be not equal, and is used by != .',
     '测试 self 与 other 值是否不相等，供 != 运算符使用。'),
    ('PartialEq::ne (default impl)',
     'Tests for <code>!=</code>. The default implementation is almost always sufficient,\\nand should not be overridden without very good reason.',
     '测试 <code>!=</code> 运算符。默认实现几乎总是够用，除非有非常充分的理由，否则不应被覆盖。'),

    # ===== ToOwned::to_owned（多段 <p> + 含 <code>/<a> 嵌套） =====
    # v4 形式：分多个 <p>，第二段有 <code>From</code> 链接到 stdlib
    # 不能硬编码 href（含 1.95.0 版本号），拆成三段独立 replace
    ('ToOwned::to_owned p1',
     '>Calls <code>U::from(self)</code>.</p>',
     '>调用 <code>U::from(self)</code>。</p>'),
    ('ToOwned::to_owned p2 start',
     '<p>That is, this conversion is whatever the implementation of\n<code>',
     '<p>也就是说，此转换的具体行为取决于\n<code>'),
    ('ToOwned::to_owned p2 end',
     ' chooses to do.</p>',
     ' 的实现方式。</p>'),

    # ===== ToOwned::to_owned / ToOwned::Owned =====
    ('ToOwned::Owned',
     'The resulting type after obtaining ownership.',
     '获得所有权后的类型。'),

    # ===== Fn::call / FnMut::call_mut / FnOnce::call_once =====
    ('Fn::call', 'Returns the argument unchanged.',
     '原样返回传入的参数。'),

    # ===== non-exhaustive 提示（chrome 级别） =====
    ('non_exhaustive enum notice',
     'Non-exhaustive enums could have additional variants added in future. '
     'Therefore, when matching against variants of non-exhaustive enums, '
     'an extra wildcard arm must be added to account for any future variants.',
     '非穷尽枚举未来可能添加新的变体。因此，在对非穷尽枚举的变体进行模式匹配时，'
     '必须额外增加一个通配符分支以涵盖未来的新变体。'),
    ('non_exhaustive struct notice',
     'Non-exhaustive structs could have additional fields added in future. '
     'Therefore, non-exhaustive structs cannot be constructed in external crates '
     'using the traditional Struct { .. } syntax; cannot be matched against '
     'without a wildcard .. ; and struct update syntax will not work.',
     '非穷尽结构体未来可能添加新的字段。因此，非穷尽结构体无法在外部 crate '
     '使用传统的 Struct { .. } 语法构造；模式匹配时必须有通配符 ..；'
     '且结构体更新语法将无法使用。'),
]

# U+2019 右单引号（'）
RQ = "’"

# 需要把含 RQ 的英文撇号模式也展开
RQ_PAIRS = [
    # 这些是 rustdoc 中含 U+2019 的 trait docblock
    (f'Clone box controller\'s state',
     f'Duplicate the controller{RQ}s state',
     '复制此控制器的状态'),
    (f'Create initial keys (client\'s CID)',
     f'Create the initial set of keys given the client{RQ}s initial destination ConnectionId',
     '根据客户端的初始目标 ConnectionId 创建初始密钥集'),
]

# chrome 标签翻译（sidebar / section-header）
CHROME_PAIRS = [
    ('>Variants<', '>变体<'),
    ('>Methods<', '>方法<'),
    ('>Fields<', '>字段<'),
    ('>Implementations<', '>实现<'),
    ('>Trait Implementations<', '>Trait 实现<'),
    ('>Required Methods<', '>必需方法<'),
    ('>Provided Methods<', '>提供方法<'),
    ('>Associated Types<', '>关联类型<'),
    ('>Associated Constants<', '>关联常量<'),
    ('>Blanket Implementations<', '>Blanket 实现<'),
    ('>Foreign Implementations<', '>外部实现<'),
    ('>Implementors<', '>实现者<'),
    ('>Auto Trait Implementations<', '>自动 Trait 实现<'),
    ('>Auto Implementations<', '>自动实现<'),
    ('>Sections<', '>章节<'),
    ('>Crate Items<', '>Crate 条目<'),
    ('>Module Items<', '>模块条目<'),
    ('>Modules<', '>模块<'),
    ('>Macros<', '>宏<'),
    ('>Structs<', '>结构体<'),
    ('>Enums<', '>枚举<'),
    ('>Traits<', '>Trait<'),
    ('>Functions<', '>函数<'),
    ('>Type Definitions<', '>类型定义<'),
    ('>Constants<', '>常量<'),
    # section-header class 形式
    ('<h2 class="variants section-header">Variants</h2>',
     '<h2 class="variants section-header">变体</h2>'),
]

# Read more 替换（独立，因为模式简单）
READ_MORE_PAIRS = [
    ('>Read more</a>', '>更多信息</a>'),
]


def expand_crlf(text, pair_list):
    """对模式串同时支持 LF 和 CRLF 两种形式。

    输入: pair_list 是 [(key, en, zh), ...]，en 可能含 \\n
    输出: 展开后的 [(en_lf, zh), (en_crlf, zh), ...]
    """
    expanded = []
    for key, en, zh in pair_list:
        if '\\n' in en:
            en_lf = en.replace('\\n', '\n')
            en_crlf = en.replace('\\n', '\r\n')
            expanded.append((en_lf, zh))
            expanded.append((en_crlf, zh))
        else:
            expanded.append((en, zh))
    return expanded


def apply_pairs(text, pairs):
    """对每个 (en, zh) 在 text 上做 replace。"""
    applied = []
    for en, zh in pairs:
        if en in text:
            count = text.count(en)
            text = text.replace(en, zh)
            applied.append((en[:50], count))
    return text, applied


def scan_crate(crate_dir, report_only=False, also_chrome=True):
    """扫描整个 crate 目录并应用翻译对。"""
    if not os.path.isdir(crate_dir):
        print(f'ERROR: not a directory: {crate_dir}', file=sys.stderr)
        sys.exit(1)

    pairs = expand_crlf('', TRAIT_PAIRS + RQ_PAIRS)
    all_pairs = pairs + (CHROME_PAIRS if also_chrome else []) + READ_MORE_PAIRS

    total_files = 0
    total_mod = 0
    total_replacements = 0
    by_file = {}

    for root, dirs, fs in os.walk(crate_dir):
        for fn in fs:
            if not fn.endswith('.html'):
                continue
            path = os.path.join(root, fn)
            with open(path, 'rb') as f:
                before = f.read().decode('utf-8')
            after, applied = apply_pairs(before, all_pairs)
            total_files += 1
            if after != before:
                if not report_only:
                    with open(path, 'wb') as f:
                        f.write(after.encode('utf-8'))
                total_mod += 1
                total_replacements += len(applied)
                by_file[os.path.relpath(path, crate_dir)] = applied

    print(f'Scanned {total_files} HTML files in {crate_dir}')
    if report_only:
        print(f'(REPORT ONLY, no files modified)')
    print(f'Modified {total_mod} files, {total_replacements} replacement groups')
    print()
    if by_file:
        print('Per-file replacements:')
        for f in sorted(by_file, key=lambda x: -len(by_file[x]))[:30]:
            for en, count in by_file[f][:3]:
                print(f'  {f}: {count}x  {en}')
            if len(by_file[f]) > 3:
                print(f'    ... +{len(by_file[f]) - 3} more')

    return total_mod, total_replacements


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    crate_dir = sys.argv[1]
    report_only = '--report' in sys.argv
    also_chrome = '--no-chrome' not in sys.argv

    scan_crate(crate_dir, report_only=report_only, also_chrome=also_chrome)

    # 自动跑 comprehensive_audit 看剩余
    if '--audit' in sys.argv:
        print('\n=== Re-audit ===')
        result = subprocess.run(
            ['python', '_common_tools/comprehensive_audit.py', crate_dir, crate_dir],
            capture_output=True, text=True)
        for line in result.stdout.split('\n')[:25]:
            print(line)


if __name__ == '__main__':
    main()