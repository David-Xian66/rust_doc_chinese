"""quinn 第 2.5 阶段：处理带 <code> 内嵌的 trait docblock"""
import os
import re

# 文本中含有 <code> 内嵌代码的 trait docblock
CODE_PAIRS = [
    # PartialEq::eq - "Tests for <code>self</code> and <code>other</code> values to be equal, and is used by <code>==</code>."
    ('Tests for <code>self</code> and <code>other</code> values to be equal, and is used by <code>==</code>.',
     '测试 <code>self</code> 与 <code>other</code> 值是否相等，供 <code>==</code> 运算符使用。'),

    # PartialEq::ne (常见)
    ('Tests for <code>self</code> and <code>other</code> values to be not equal, and is used by <code>!=</code>.',
     '测试 <code>self</code> 与 <code>other</code> 值是否不相等，供 <code>!=</code> 运算符使用。'),

    # PartialOrd::lt / gt / le / ge (常见)
    ('Tests less than (for <code>self</code> and <code>other</code>) and is used by the <code>&lt;</code> operator.',
     '测试小于（针对 <code>self</code> 与 <code>other</code>），供 <code>&lt;</code> 运算符使用。'),
    ('Tests less than or equal to (for <code>self</code> and <code>other</code>) and is used by the <code>&lt;=</code> operator.',
     '测试小于等于（针对 <code>self</code> 与 <code>other</code>），供 <code>&lt;=</code> 运算符使用。'),
    ('Tests greater than (for <code>self</code> and <code>other</code>) and is used by the <code>&gt;</code> operator.',
     '测试大于（针对 <code>self</code> 与 <code>other</code>），供 <code>&gt;</code> 运算符使用。'),
    ('Tests greater than or equal to (for <code>self</code> and <code>other</code>) and is used by the <code>&gt;=</code> operator.',
     '测试大于等于（针对 <code>self</code> 与 <code>other</code>），供 <code>&gt;=</code> 运算符使用。'),

    # TryFrom / TryInto 常见
    # Already covered as bare text

    # Hash::hash with <code>
    ('Feeds this value into the given <code>Hasher</code>.',
     '将此值送入给定的 <code>Hasher</code>。'),

    # Ord::cmp with <code>
    ('This method returns an <code>Ordering</code> between <code>self</code> and <code>other</code>.',
     '此方法返回 <code>self</code> 与 <code>other</code> 之间的 <code>Ordering</code>。'),

    # PartialOrd::partial_cmp with <code>
    ('This method returns an ordering between <code>self</code> and <code>other</code> values if one exists.',
     '若存在，此方法返回 <code>self</code> 与 <code>other</code> 值之间的排序关系。'),
]


def apply_pairs(text):
    applied = []
    for en, zh in CODE_PAIRS:
        if en in text:
            text = text.replace(en, zh)
            applied.append(en[:60])
    return text, applied


total = 0
modified = 0
for root, dirs, fs in os.walk('quinn'):
    for fn in fs:
        if not fn.endswith('.html'):
            continue
        path = os.path.join(root, fn)
        with open(path, 'rb') as f:
            before = f.read().decode('utf-8')
        after, applied = apply_pairs(before)
        if after != before:
            with open(path, 'wb') as f:
                f.write(after.encode('utf-8'))
            modified += 1
            total += len(applied)

print(f'Modified {modified} files, {total} replacements')

# 再 audit
import subprocess
result = subprocess.run(['python', '_common_tools/comprehensive_audit.py', 'quinn', 'quinn'],
                       capture_output=True, text=True)
for line in result.stdout.split('\n')[:25]:
    print(line)