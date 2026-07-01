#!/usr/bin/env python3
"""tokio 第十阶段：补译 cancel-safety 句式 + 剩余 cmd/fs/AsyncReadExt 杂项。

模式串统一以 LF 写入，main() 中自动展开为 CRLF 匹配。
"""
import os

BASE = r'D:/Administrator/Documents/Code/rust_doc_all/tokio'

# 模式统一以 LF 写入
# ====== phase10 patterns ======

# 模式 A: 此方法是取消安全的。 If this method is used as an event in a\n<a...>tokio::select!</a> statement... completes first, it is guaranteed...
PAT_A1_EN = '此方法是取消安全的。 If this method is used as an event in a\n<a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> statement and some other branch\ncompletes first, it is guaranteed that no data were read.'
PAT_A1_ZH = '此方法是取消安全的。若将此方法用作\n<a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> 语句中的事件，且其他分支先完成，则保证尚未读取任何数据。'

# 模式 B: 此方法是取消安全的。若你将其作为事件用在\n<a...>tokio::select!</a> statement... completes first, it is guaranteed that no data was read.
PAT_B1_EN = '此方法是取消安全的。若你将其作为事件用在\n<a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> statement and some other branch\ncompletes first, it is guaranteed that no data was read.'
PAT_B1_ZH = '此方法是取消安全的。若你将其作为事件用在\n<a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> 语句中，且其他分支先完成，则保证尚未读取任何数据。'

# 模式 C: 此方法不是取消安全的。 If this method is used as the event in a\n<code>tokio::select!</code> statement... completes first, then some data may be lost.
PAT_C1_EN = '此方法不是取消安全的。 If this method is used as the event in a\n<code>tokio::select!</code> statement and some other branch\ncompletes first, then some data may be lost.'
PAT_C1_ZH = '此方法不是取消安全的。若将此方法用作\n<code>tokio::select!</code> 语句中的事件，且其他分支先完成，则可能会丢失一些数据。'

# 模式 D: 此方法不是取消安全的。 If this method is used as the event in a\n<code>tokio::select!</code> statement... completes first, then some data may already have been\nread into <code>buf</code>.
PAT_D1_EN = '此方法不是取消安全的。 If this method is used as the event in a\n<code>tokio::select!</code> statement and some other branch\ncompletes first, then some data may already have been\nread into <code>buf</code>.'
PAT_D1_ZH = '此方法不是取消安全的。若将此方法用作\n<code>tokio::select!</code> 语句中的事件，且其他分支先完成，则可能已经读取了一些数据到 <code>buf</code> 中。'

# 模式 E: "It is your responsibility to make sure that <code>buf</code>\nis initialized before calling <code>read</code>."
PAT_E1_EN = 'It is your responsibility to make sure that <code>buf</code>\nis initialized before calling <code>read</code>.'
PAT_E1_ZH = '请你负责确保在调用 <code>read</code> 之前 <code>buf</code> 已初始化。'

# 模式 F: "This method returns the same errors as <code>AsyncReadExt::read_exact</code>."
PAT_F1_EN = 'This method returns the same errors as <code>AsyncReadExt::read_exact</code>.'
PAT_F1_ZH = '此方法返回与 <code>AsyncReadExt::read_exact</code> 相同的错误。'

# 模式 G: Equivalent to: (in <h5>)
PAT_G1_EN = '<h5 id="examples">§</a>Equivalent to:</h5>'
PAT_G1_ZH = '<h5 id="examples">§</a>相当于：</h5>'

PAIRS = [
    (PAT_A1_EN, PAT_A1_ZH),
    (PAT_B1_EN, PAT_B1_ZH),
    (PAT_C1_EN, PAT_C1_ZH),
    (PAT_D1_EN, PAT_D1_ZH),
    (PAT_E1_EN, PAT_E1_ZH),
    (PAT_F1_EN, PAT_F1_ZH),
    (PAT_G1_EN, PAT_G1_ZH),
]


def main():
    pairs_b = [(en.encode('utf-8'), zh.encode('utf-8')) for en, zh in PAIRS]

    total_files = 0
    total_replacements = 0
    files_changed = 0

    for root, dirs, files in os.walk(BASE):
        for f in files:
            if not f.endswith('.html'):
                continue
            p = os.path.join(root, f)
            with open(p, 'rb') as fh:
                c = fh.read()
            original = c
            local = 0

            for en_b, zh_b in pairs_b:
                if en_b in c:
                    occurrences = c.count(en_b)
                    c = c.replace(en_b, zh_b)
                    local += occurrences
                # 模式本身是 LF，自动展开为 CRLF（rustdoc Windows 输出）
                en_crlf = en_b.replace(b'\n', b'\r\n')
                zh_crlf = zh_b.replace(b'\n', b'\r\n')
                if en_crlf != en_b and en_crlf in c:
                    occurrences = c.count(en_crlf)
                    c = c.replace(en_crlf, zh_crlf)
                    local += occurrences

            if c != original:
                with open(p, 'wb') as fh:
                    fh.write(c)
                files_changed += 1
                total_replacements += local
            total_files += 1

    print(f'Phase 10: {files_changed}/{total_files} files, {total_replacements} replacements')


if __name__ == '__main__':
    main()