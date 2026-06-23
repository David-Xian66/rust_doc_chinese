"""quinn 第 2 阶段：批量翻译 trait method docblock（v4 raw HTML 模式）

按 CLAUDE.md 中 "rustls_pki_types 又一次升级" 的方法：
- 保留 <a href="...">Read more</a> 结构，只替换文本节点和 <a> 的文本
"""
import os
import re

# 标准 Rust stdlib trait 方法的 docblock 翻译
# 模式: (英文文本节点, 中文文本节点)
TRAIT_PAIRS = [
    # Clone::clone
    ('Returns a duplicate of the value.',
     '返回值的副本。'),

    # Debug::fmt
    ('Formats the value using the given formatter.',
     '使用给定的格式化器格式化此值。'),

    # From::from (impl From<X> for Y, 也包括 TryFrom, Into, TryInto)
    ('Converts to this type from the input type.',
     '从输入类型转换为此类型。'),

    # PartialEq::eq
    ('Tests for self and other values to be equal, and is used by == .',
     '测试 self 与 other 值是否相等，供 == 运算符使用。'),

    # Hash::hash
    ('Feeds this value into the given Hasher .',
     '将此值送入给定的 Hasher。'),

    # Ord::cmp
    ('This method returns an Ordering between self and other .',
     '此方法返回 self 与 other 之间的 Ordering。'),

    # PartialOrd::partial_cmp
    ('This method returns an ordering between self and other values if one exists.',
     '若存在，此方法返回 self 与 other 值之间的排序关系。'),

    # Drop::drop
    ('Executes the destructor for this type.',
     '执行此类型的析构函数。'),

    # Future::poll
    ('Attempts to resolve the future to a final value, registering the current task for wakeup if the value is not yet available.',
     '尝试将 Future 解析为最终值，若值尚不可用则注册当前任务以备唤醒。'),

    # Display::fmt （部分实现）
    # Already covered above

    # std::error::Error::source
    ('Returns the lower-level source of this error, if any.',
     '返回此错误的更底层来源（若有）。'),

    # IntoIterator::into_iter (少见)
    # Default::default
    ('Returns the "default value" for a type.',
     '返回一个类型的"默认值"。'),

    # TryFrom::try_from
    # already covered
]

# Read more → 更多信息
READ_MORE_PAIRS = [
    ('<a href="', '<a href="'),  # placeholder
]


def apply_pairs(text):
    """应用所有翻译对"""
    applied = []
    for en, zh in TRAIT_PAIRS:
        # 模式 1: bare text
        if en in text:
            text = text.replace(en, zh)
            applied.append(('bare', en[:40]))
        # 模式 2: text + <a href="...">Read more</a>
        # 形如: "Feeds this value into the given Hasher . <a href=\"...\">Read more</a>"
        # 这里我们直接做 partial replace - 先替换文本，再替换 Read more
        # 实际上 bare replace 已经把前导文本替换了，剩下的 <a>Read more</a> 留给 Read more pass

    # Read more 替换 - 注意 Read more 是固定模式
    if '>Read more</a>' in text:
        count = text.count('>Read more</a>')
        text = text.replace('>Read more</a>', '>更多信息</a>')
        applied.append(('Read more', f'{count} occurrences'))

    return text, applied


# 跑
total_files = 0
total_replacements = 0
per_file_report = {}

for root, dirs, files in os.walk('quinn'):
    for fn in files:
        if not fn.endswith('.html'):
            continue
        path = os.path.join(root, fn)
        with open(path, 'rb') as f:
            before = f.read().decode('utf-8')
        after, applied = apply_pairs(before)
        if after != before:
            with open(path, 'wb') as f:
                f.write(after.encode('utf-8'))
            total_files += 1
            per_file_report[os.path.relpath(path, 'quinn')] = len(applied)
            total_replacements += len(applied)

print(f'Modified {total_files} files, {total_replacements} replacements')
print('\nPer-file replacement count:')
for f, c in sorted(per_file_report.items(), key=lambda x: -x[1])[:20]:
    print(f'  {f}: {c}')

# 重新跑 audit
print('\n=== Re-audit ===')
import subprocess
result = subprocess.run(['python', '_common_tools/comprehensive_audit.py', 'quinn', 'quinn'],
                       capture_output=True, text=True)
for line in result.stdout.split('\n')[:15]:
    print(line)