#!/usr/bin/env python3
"""tokio 第十一阶段：补译剩余 cancel-safety (with <a>) + Command.html + Ctrl*.html。"""
import os

BASE = r'D:/Administrator/Documents/Code/rust_doc_all/tokio'

# 模式统一以 LF 写入。源文件是 CRLF, main() 中自动展开为 CRLF 匹配。

# === cancel-safety patterns ===
# 模式 A: This method is not cancellation safe. If the method is used as the\nevent in a <a...
PAT_A_EN = 'This method is not cancellation safe. If the method is used as the\nevent in a <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> statement and some\nother branch completes first, then some data may be lost.'
PAT_A_ZH = '此方法不是取消安全的。若将此方法用作\n<a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> 语句中的事件，且其他分支先完成，则可能会丢失一些数据。'

# 模式 B: read_exact style
PAT_B_EN = 'This method is not cancellation safe. If the method is used as the\nevent in a <a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> statement and some\nother branch completes first, then some data may already have been\nread into <code>buf</code>.'
PAT_B_ZH = '此方法不是取消安全的。若将此方法用作\n<a href="../macro.select.html" title="macro tokio::select"><code>tokio::select!</code></a> 语句中的事件，且其他分支先完成，则可能已经读取了一些数据到 <code>buf</code> 中。'

# 模式 C: <code>tokio::select!</code> (not <a>)
PAT_C_EN = 'This method is not cancellation safe. If the method is used as the\nevent in a <code>tokio::select!</code> statement and some\nother branch completes first, then some data may be lost.'
PAT_C_ZH = '此方法不是取消安全的。若将此方法用作\n<code>tokio::select!</code> 语句中的事件，且其他分支先完成，则可能会丢失一些数据。'

# 模式 D: <code>... may already have been
PAT_D_EN = 'This method is not cancellation safe. If the method is used as the\nevent in a <code>tokio::select!</code> statement and some\nother branch completes first, then some data may already have been\nread into <code>buf</code>.'
PAT_D_ZH = '此方法不是取消安全的。若将此方法用作\n<code>tokio::select!</code> 语句中的事件，且其他分支先完成，则可能已经读取了一些数据到 <code>buf</code> 中。'

# === Command.html patterns ===
PAT_CMD1_EN = 'Constructs a new Command for launching the program at\npath program, with the following default configuration:'
PAT_CMD1_ZH = '构造一个用于启动 path 路径程序的新 Command，并采用以下默认配置：'

PAT_CMD2_EN = 'If program is not an absolute path, the PATH will be searched in\nan OS-defined way.'
PAT_CMD2_ZH = '若 program 不是绝对路径，将以操作系统定义的方式搜索 PATH。'

PAT_CMD3_EN = 'The search path to be used may be controlled by setting the\nPATH environment variable on the Command,\nbut this has some implementation limitations on Windows\n(see issue rust-lang/rust#37519).'
PAT_CMD3_ZH = '可通过在 Command 上设置 PATH 环境变量来控制要使用的搜索路径，\n但在 Windows 上有一些实现限制（参见 rust-lang/rust#37519）。'

PAT_CMD4_EN = 'Note that Tokio specific options will be lost. Currently, this only applies to kill_on_drop.'
PAT_CMD4_ZH = '请注意，tokio 特有的选项将丢失。目前，这仅影响 kill_on_drop。'

PAT_CMD5_EN = 'To pass a single argument see arg.'
PAT_CMD5_ZH = '若要传递单个参数，请参阅 arg。'

PAT_CMD6_EN = 'Inserts or updates an environment variable mapping.'
PAT_CMD6_ZH = '插入或更新一个环境变量映射。'

PAT_CMD7_EN = 'Removes an environment variable mapping.'
PAT_CMD7_ZH = '删除一个环境变量映射。'

PAT_CMD8_EN = 'Sets the working directory for the child process.'
PAT_CMD8_ZH = '为子进程设置工作目录。'

PAT_CMD9_EN = "If the program path is relative (e.g., \"./script.sh\"), it\xe2\x80\x99s ambiguous\nwhether it should be interpreted relative to the parent\xe2\x80\x99s working\ndirectory or relative to current_dir. The behavior in this cas"
PAT_CMD9_ZH = "\xe5\xa6\x82\xe6\x9e\x9c\xe7\xa8\x8b\xe5\xba\x8f\xe8\xb7\xaf\xe5\xbe\x84\xe6\x98\xaf\xe7\x9b\xb8\xe5\xaf\xb9\xe8\xb7\xaf\xe5\xbe\x84\xef\xbc\x88\xe4\xbe\x8b\xe5\xa6\x82 \"./script.sh\"\xef\xbc\x89\xef\xbc\x8c\xe9\x82\xa3\xe4\xb9\x88\xe5\xba\x94\xe8\xaf\xa5\xe7\x9b\xb8\xe5\xaf\xb9\xe4\xba\x8e\xe7\x88\xb6\xe8\xbf\x9b\xe7\xa8\x8b\xe7\x9a\x84\xe5\xb7\xa5\xe4\xbd\x9c\xe7\x9b\xae\xe5\xbd\x95\xe8\xa7\xa3\xe9\x87\x8a\xef\xbc\x8c\xe8\xbf\x98\xe6\x98\xaf\xe7\x9b\xb8\xe5\xaf\xb9\xe4\xba\x8e current_dir \xe8\xa7\xa3\xe9\x87\x8a\xe5\xae\x9e\xe4\xb8\x8d\xe6\x98\x8e\xe7\xa1\xae"

PAT_CMD10_EN = "Sets configuration for the child process\xe2\x80\x99s standard input (stdin) handle."
PAT_CMD10_ZH = "\xe4\xb8\xba\xe5\xad\x90\xe8\xbf\x9b\xe7\xa8\x8b\xe7\x9a\x84\xe6\xa0\x87\xe5\x87\x86\xe8\xbe\x93\xe5\x85\xa5\xef\xbc\x88stdin\xef\xbc\x89handle \xe8\xae\xbe\xe7\xbd\xae\xe9\x85\x8d\xe7\xbd\xae"

# === Ctrl*.html patterns ===
PAT_CTRL_EN = 'Polls to receive the next signal notification event, outside of an\nasync context.'
PAT_CTRL_ZH = '在异步上下文之外轮询以接收下一个信号通知事件。'

# === ReadHalf.unsplit ===
PAT_RH1_EN = 'If this ReadHalf and the given WriteHalf do not originate from the\nsame split operation this method will panic.\nThis can be checked ahead of time by calling is_pair_of().'
PAT_RH1_ZH = '若此 ReadHalf 与给定的 WriteHalf 不是来自同一次拆分操作，此方法将 panic。\n可通过提前调用 is_pair_of() 进行检查。'

PAIRS = [
    (PAT_A_EN, PAT_A_ZH),
    (PAT_B_EN, PAT_B_ZH),
    (PAT_C_EN, PAT_C_ZH),
    (PAT_D_EN, PAT_D_ZH),
    (PAT_CMD1_EN, PAT_CMD1_ZH),
    (PAT_CMD2_EN, PAT_CMD2_ZH),
    (PAT_CMD3_EN, PAT_CMD3_ZH),
    (PAT_CMD4_EN, PAT_CMD4_ZH),
    (PAT_CMD5_EN, PAT_CMD5_ZH),
    (PAT_CMD6_EN, PAT_CMD6_ZH),
    (PAT_CMD7_EN, PAT_CMD7_ZH),
    (PAT_CMD8_EN, PAT_CMD8_ZH),
    (PAT_CMD9_EN, PAT_CMD9_ZH),
    (PAT_CMD10_EN, PAT_CMD10_ZH),
    (PAT_CTRL_EN, PAT_CTRL_ZH),
    (PAT_RH1_EN, PAT_RH1_ZH),
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

    print(f'Phase 11: {files_changed}/{total_files} files, {total_replacements} replacements')


if __name__ == '__main__':
    main()