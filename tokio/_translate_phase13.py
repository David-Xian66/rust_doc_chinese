#!/usr/bin/env python3
"""tokio 第十三阶段：补译 ReadHalf.unsplit + Command.spawn 三个未译。"""
import os

BASE = r'D:/Administrator/Documents/Code/rust_doc_all/tokio'

PAIRS = [
    # === ReadHalf.unsplit (with <code> + <a> tags) ===
    (
        'If this <code>ReadHalf</code> and the given <code>WriteHalf</code> do not originate from the\n'
        'same <code>split</code> operation this method will panic.\n'
        'This can be checked ahead of time by calling <a href="struct.ReadHalf.html#method.is_pair_of" title="method tokio::io::ReadHalf::is_pair_of"><code>is_pair_of()</code></a>.',
        '若此 <code>ReadHalf</code> 与给定的 <code>WriteHalf</code> 不是来自同一次 <code>split</code> 操作，此方法将 panic。\n'
        '可通过提前调用 <a href="struct.ReadHalf.html#method.is_pair_of" title="method tokio::io::ReadHalf::is_pair_of"><code>is_pair_of()</code></a> 进行检查。'
    ),

    # === Command.spawn 第一段 (with <code>Child</code>) ===
    (
        'Similar to the behavior to the standard library, and unlike the futures\n'
        'paradigm of dropping-implies-cancellation, a spawned process will, by\n'
        'default, continue to execute even after the <code>Child</code> handle has been dropped.',
        '与标准库的行为类似，且不像 future 中"丢弃即取消"的范式，默认情况下，'
        '派生的进程即使在 <code>Child</code> handle 被丢弃后仍会继续执行。'
    ),

    # === Command.spawn 第二段 (with <a><code>Command::kill_on_drop</code></a>) ===
    (
        'The <a href="struct.Command.html#method.kill_on_drop" title="method tokio::process::Command::kill_on_drop"><code>Command::kill_on_drop</code></a> method can be used to modify this behavior\n'
        'and kill the child process if the <code>Child</code> wrapper is dropped before it\n'
        'has exited.',
        '可使用 <a href="struct.Command.html#method.kill_on_drop" title="method tokio::process::Command::kill_on_drop"><code>Command::kill_on_drop</code></a> 方法修改此行为，'
        '使得在 <code>Child</code> 包装器被丢弃前子进程尚未退出的情况下杀死子进程。'
    ),

    # === Command.spawn 第三段 (with <a><code>Child</code></a>) ===
    (
        'It is recommended to avoid dropping a <a href="struct.Child.html" title="struct tokio::process::Child"><code>Child</code></a> process handle before it has been\n'
        'fully <code>await</code>ed if stricter cleanup guarantees are required.',
        '如果需要更严格的清理保证，建议在 <a href="struct.Child.html" title="struct tokio::process::Child"><code>Child</code></a> 进程 handle 被完全 <code>await</code> 之前避免丢弃它。'
    ),
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

    print(f'Phase 13: {files_changed}/{total_files} files, {total_replacements} replacements')


if __name__ == '__main__':
    main()