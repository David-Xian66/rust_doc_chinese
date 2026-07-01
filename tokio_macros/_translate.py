"""Translate tokio_macros crate."""
import os

TOKIO_MACROS_ROOT = 'D:/Administrator/Documents/Code/rust_doc_all/tokio_macros'

def b(s):
    return s.replace('\n', '\r\n').encode('utf-8')

def c(s):
    return s.replace('\n', '\r\n').encode('utf-8')

# (en_bytes_with_crlf, zh_bytes_with_crlf)
PAIRS = [
    # attr.main.html remaining
    (b('<p>Note: The multi-threaded runtime requires the <code>rt-multi-thread</code> feature\nflag.</p>'),
     c('<p>注意：多线程运行时需要 <code>rt-multi-thread</code> 特性标志。</p>')),
    (b('<p>To use the single-threaded runtime known as the <code>current_thread</code> runtime,\nthe macro can be configured using</p>'),
     c('<p>要使用称为 <code>current_thread</code> 运行时的单线程运行时，\n可通过以下方式配置该宏：</p>')),
    (b('<p>This option is only compatible with the <code>current_thread</code> runtime.</p>'),
     c('<p>此选项仅与 <code>current_thread</code> 运行时兼容。</p>')),
    (b('<p>Arguments are allowed for any functions, aside from <code>main</code> which is special.</p>'),
     c('<p>除 <code>main</code>（特殊）外，任何函数都允许使用参数。</p>')),

    # attr.test.html remaining (similar)
    (b('<p>Note: The multi-threaded runtime requires the rt-multi-thread feature flag.</p>'),
     c('<p>注意：多线程运行时需要 rt-multi-thread 特性标志。</p>')),
    (b('<p>To use the single-threaded runtime known as the current_thread runtime, the macro can be configured using</p>'),
     c('<p>要使用称为 current_thread 运行时的单线程运行时，可通过以下方式配置该宏：</p>')),
    (b('<p>This option is only compatible with the current_thread runtime.</p>'),
     c('<p>此选项仅与 current_thread 运行时兼容。</p>')),

    # attr.main_fail.html, attr.test_fail.html
    (b('<p>Always fails with the error message below.</p>'),
     c('<p>总是失败并返回下面的错误信息。</p>')),
    (b('<p>The <code>worker_threads</code> option configures the number of worker threads, and\ndefaults to the number of cpus on the system. This is the default\nruntime, so this only matters when overriding the default.</p>'),
     c('<p><code>worker_threads</code> 选项配置 worker 线程的数量，\n默认值为系统上的 CPU 数量。这是默认运行时，因此仅在覆盖默认值时才有意义。</p>')),
    (b('<p>The default test runtime is single-threaded.</p>'),
     c('<p>默认的 test 运行时是单线程的。</p>')),

    # attr.main_rt.html, attr.test_rt.html
    (b('<p>Marks async function to be executed by selected runtime. This macro helps set up a <code>Runtime</code>\nwithout requiring the user to use <a href="../tokio/runtime/struct.Runtime.html">Runtime</a> or\n<a href="../tokio/runtime/struct.Builder.html">Builder</a> directly.</p>'),
     c('<p>将 async 函数标记为由所选运行时执行。该宏帮助设置一个 <code>Runtime</code>，\n无需用户直接使用 <a href="../tokio/runtime/struct.Runtime.html">Runtime</a> 或\n<a href="../tokio/runtime/struct.Builder.html">Builder</a>。</p>')),
    (b('<p>Arguments are allowed for any functions aside from <code>main</code> which is special</p>'),
     c('<p>除 <code>main</code>（特殊）外，允许任何函数使用参数</p>')),
    (b('<p>Marks async function to be executed by runtime, suitable to test environment</p>'),
     c('<p>将 async 函数标记为由运行时执行，适用于测试环境</p>')),
]


def main():
    hits = 0
    modified = 0
    missed_pairs = []
    for dp, dirs, files in os.walk(TOKIO_MACROS_ROOT):
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
        for dp, dirs, files in os.walk(TOKIO_MACROS_ROOT):
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