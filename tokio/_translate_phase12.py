#!/usr/bin/env python3
"""tokio 第十二阶段：补译剩余 6 个未翻译 <p>。"""
import os

BASE = r'D:/Administrator/Documents/Code/rust_doc_all/tokio'

PAIRS = [
    # === ReadHalf.unsplit ===
    (
        'If this ReadHalf and the given WriteHalf do not originate from the\n'
        'same split operation this method will panic.\n'
        'This can be checked ahead of time by calling is_pair_of().',
        '若此 ReadHalf 与给定的 WriteHalf 不是来自同一次拆分操作，此方法将 panic。\n'
        '可通过提前调用 is_pair_of() 进行检查。'
    ),

    # === Command.spawn ===
    (
        'Similar to the behavior to the standard library, and unlike the futures\n'
        'paradigm of dropping-implies-cancellation, a spawned process will, by\n'
        'default, continue to execute even after the Child handle',
        '与标准库的行为类似，且不像 future 中"丢弃即取消"的范式，默认情况下，'
        '派生的进程即使在 Child handle 被丢弃后仍会继续执行。'
    ),
    (
        'The Command::kill_on_drop method can be used to modify this behavior\n'
        'and kill the child process if the Child wrapper is dropped before it\n'
        'has exited.',
        '可使用 Command::kill_on_drop 方法修改此行为，'
        '使得在 Child 包装器被丢弃前子进程尚未退出的情况下杀死子进程。'
    ),
    (
        'It is recommended to avoid dropping a Child process handle before it has been\n'
        'fully awaited if stricter cleanup guarantees are required.',
        '如果需要更严格的清理保证，建议在 Child 进程 handle 被完全 await 之前避免丢弃它。'
    ),

    # === Command.status ===
    (
        'By default, stdin, stdout and stderr are inherited from the parent.\n'
        'If any input/output handles are set to a pipe then they will be immediately\n'
        'closed after the child is spawned.',
        '默认情况下，stdin、stdout 与 stderr 继承自父进程。\n'
        '如果任何输入/输出 handle 被设置为 pipe，则它们会在子进程派生后立即关闭。'
    ),

    # === Command.output ===
    (
        'Executes the command as a child process, waiting for it to finish and\n'
        'collecting all of its output.',
        '作为子进程执行命令，等待其完成并收集其所有输出。'
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

    print(f'Phase 12: {files_changed}/{total_files} files, {total_replacements} replacements')


if __name__ == '__main__':
    main()