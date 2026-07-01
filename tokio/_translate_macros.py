"""Bytes-mode translation of tokio macros + attr docs.

Uses CRLF-aware byte patterns matching the actual rustdoc output format.
"""
import os

TOKIO_ROOT = 'D:/Administrator/Documents/Code/rust_doc_all/tokio'

def b(s):
    """str with \n -> bytes with \r\n."""
    return s.replace('\n', '\r\n').encode('utf-8')

def c(s):
    """ZH str with \n -> bytes with \r\n."""
    return s.replace('\n', '\r\n').encode('utf-8')

PAIRS = [
    # ============== attr.main.html ==============
    (b('<p>Marks async function to be executed by the selected runtime. This macro\n'
       'helps set up a <code>Runtime</code> without requiring the user to use\n'
       '<a href="../tokio/runtime/struct.Runtime.html">Runtime</a> or\n'
       '<a href="../tokio/runtime/struct.Builder.html">Builder</a> directly.</p>'),
     c('<p>将 async 函数标记为由所选运行时执行。该宏帮助设置一个 <code>Runtime</code>，\n'
       '无需用户直接使用\n'
       '<a href="../tokio/runtime/struct.Runtime.html">Runtime</a> 或\n'
       '<a href="../tokio/runtime/struct.Builder.html">Builder</a>。</p>')),

    (b('<p>Note: This macro is designed to be simplistic and targets applications that\n'
       'do not require a complex setup. If the provided functionality is not\n'
       'sufficient, you may be interested in using\n'
       '<a href="../tokio/runtime/struct.Builder.html">Builder</a>, which provides a more\n'
       'powerful interface.</p>'),
     c('<p>注意：该宏被设计为简单易用，面向不需要复杂配置的应用。如果所提供的功能不够用，\n'
       '您可以考虑使用\n'
       '<a href="../tokio/runtime/struct.Builder.html">Builder</a>，它提供更强大的接口。</p>')),

    (b('<p>Note: This macro can be used on any function and not just the <code>main</code>\n'
       'function. Using it on a non-main function makes the function behave as if it\n'
       'was synchronous by starting a new runtime each time it is called. If the\n'
       'function is called often, it is preferable to create the runtime using the\n'
       'runtime builder so the runtime can be reused across calls.</p>'),
     c('<p>注意：该宏可用于任何函数，不仅仅是 <code>main</code> 函数。在非 main 函数上使用它\n'
       '会让该函数表现得像同步函数一样（每次调用时启动一个新运行时）。如果该函数被频繁调用，\n'
       '建议使用 runtime builder 创建运行时，以便跨调用复用。</p>')),

    (b('<p>Note that the async function marked with this macro does not run as a\n'
       'worker. The expectation is that other tasks are spawned by the function here.\n'
       'Awaiting on other futures from the function provided here will not\n'
       'perform as fast as those spawned as workers.</p>'),
     c('<p>注意：由该宏标记的 async 函数不会作为 worker 运行。预期行为是此函数内部派生其他任务。\n'
       '在此处提供的函数中 await 其他 future 的性能不会像 worker 派生的任务那样快。</p>')),

    (b('<p>The macro can be configured with a <code>flavor</code> parameter to select\n'
       'different runtime configurations.</p>'),
     c('<p>该宏可通过 <code>flavor</code> 参数配置不同的运行时配置。</p>')),

    (b('<p>To use the multi-threaded runtime, the macro can be configured using\n'
       '<code>flavor = "multi_thread"</code></p>'),
     c('<p>要使用多线程运行时，可通过 <code>flavor = "multi_thread"</code> 配置该宏。</p>')),

    # ============== attr.test.html ==============
    (b('<p>Marks async function to be executed by runtime, suitable to test environment.\n'
       'This macro helps set up a <code>Runtime</code> without requiring the user to use\n'
       '<a href="../tokio/runtime/struct.Runtime.html">Runtime</a> or\n'
       '<a href="../tokio/runtime/struct.Builder.html">Builder</a> directly.</p>'),
     c('<p>将 async 函数标记为由运行时执行，适用于测试环境。该宏帮助设置一个 <code>Runtime</code>，\n'
       '无需用户直接使用\n'
       '<a href="../tokio/runtime/struct.Runtime.html">Runtime</a> 或\n'
       '<a href="../tokio/runtime/struct.Builder.html">Builder</a>。</p>')),

    # ============== macro.join.html ==============
    (b('<p>Waits on multiple concurrent branches, returning when all branches\n'
       'complete.</p>'),
     c('<p>等待多个并发分支，直到所有分支完成才返回。</p>')),

    (b('<p>The <code>join!</code> macro must be used inside of async functions, closures, and\n'
       'blocks.</p>'),
     c('<p><code>join!</code> 宏必须在 async 函数、闭包和块内使用。</p>')),

    (b('<p>The <code>join!</code> macro takes a list of async expressions and evaluates them\n'
       'concurrently on the same task. Each async expression evaluates to a future\n'
       'and the futures from each expression are multiplexed on the current task.</p>'),
     c('<p><code>join!</code> 宏接受一个 async 表达式列表，并在同一任务上并发地执行它们。\n'
       '每个 async 表达式求值为一个 future，来自每个表达式的 future 在当前任务上多路复用。</p>')),

    (b('<p>When working with async expressions returning <code>Result</code>, <code>join!</code> will wait\n'
       'for all branches complete regardless if any complete with <code>Err</code>. Use\n'
       '<a href="macro.try_join.html" title="macro tokio::try_join"><code>try_join!</code></a> to return early when <code>Err</code> is encountered.</p>'),
     c('<p>当使用返回 <code>Result</code> 的 async 表达式时，<code>join!</code> 会等待所有分支完成，\n'
       '无论是否有分支以 <code>Err</code> 完成。若想在遇到 <code>Err</code> 时提前返回，请使用\n'
       '<a href="macro.try_join.html" title="macro tokio::try_join"><code>try_join!</code></a>。</p>')),

    (b('<p>The supplied futures are stored inline and do not require allocating a\n'
       '<code>Vec</code>.</p>'),
     c('<p>所提供的 future 内联存储，无需分配 <code>Vec</code>。</p>')),

    (b('<p>By running all async expressions on the current task, the expressions are\n'
       'able to run concurrently but not in parallel. This means all\n'
       'expressions are run on the same thread and if one branch blocks the thread,\n'
       'all other expressions will be unable to continue. If parallelism is\n'
       'required, spawn each async expression using\n'
       '<a href="task/fn.spawn.html" title="fn tokio::task::spawn"><code>tokio::spawn</code></a>.</p>'),
     c('<p>由于所有 async 表达式都在当前任务上运行，这些表达式能够并发运行但不能并行执行。\n'
       '这意味着所有表达式都在同一线程上运行，如果一个分支阻塞了该线程，\n'
       '所有其他表达式都将无法继续。如果需要并行执行，请使用\n'
       '<a href="task/fn.spawn.html" title="fn tokio::task::spawn"><code>tokio::spawn</code></a>\n'
       '派生每个 async 表达式。</p>')),

    (b('<p>By default, <code>join!</code>\xe2\x80\x99s generated future rotates which contained\n'
       'future is polled first whenever it is woken.</p>'),
     c('<p>默认情况下，<code>join!</code> 生成的 future 在每次被唤醒时轮流选择最先 poll 的 future。</p>')),

    (b('<p>This behavior can be overridden by adding <code>biased;</code> to the beginning of the\n'
       'macro usage. See the examples for details. This will cause join to poll\n'
       'the futures in the order they appear from top to bottom.</p>'),
     c('<p>可以通过在宏用法开头添加 <code>biased;</code> 来覆盖此行为。详情请参见示例。\n'
       '这会让 join 按从上到下的顺序 poll future。</p>')),

    (b('<p>You may want this if your futures may interact in a way where known polling order is significant.</p>'),
     c('<p>如果您的 future 之间的交互中已知的 poll 顺序很重要，则可能需要这样做。</p>')),

    (b('<p>But there is an important caveat to this mode. It becomes your responsibility\n'
       'to ensure that the polling order of your futures is fair. If for example you\n'
       'are joining a stream and a shutdown future, and the stream has a\n'
       'huge volume of messages that takes a long time to finish processing per poll, yo'),
     c('<p>但此模式有一个重要的注意事项。您需要自行确保 future 的 poll 顺序是公平的。例如，如果您\n'
       'join 一个流和一个 shutdown future，并且该流每次 poll 需要处理大量消息，\n'
       '那么该流可能会一直阻止 shutdown future 被 poll，导致 shutdown future 永远无法执行。')),

    (b('<p>Basic join with two branches</p>'),
     c('<p>两个分支的基本 join</p>')),

    # ============== macro.select.html ==============
    (b('<p>Waits on multiple concurrent branches, returning when the first branch\n'
       'completes, cancelling the remaining branches.</p>'),
     c('<p>等待多个并发分支，当第一个分支完成时返回，并取消其余分支。</p>')),

    (b('<p>The <code>select!</code> macro must be used inside of async functions, closures, and\n'
       'blocks.</p>'),
     c('<p><code>select!</code> 宏必须在 async 函数、闭包和块内使用。</p>')),

    (b('<p>The <code>select!</code> macro accepts one or more branches with the following pattern:</p>'),
     c('<p><code>select!</code> 宏接受一个或多个具有以下模式的分支：</p>')),

    # ============== macro.try_join.html ==============
    (b('<p>Waits on multiple concurrent branches, returning when all branches\n'
       'complete with <code>Ok(_)</code> or on the first <code>Err(_)</code>.</p>'),
     c('<p>等待多个并发分支，直到所有分支以 <code>Ok(_)</code> 完成，或在第一个 <code>Err(_)</code> 时返回。</p>')),

    (b('<p>The <code>try_join!</code> macro must be used inside of async functions, closures, and\n'
       'blocks.</p>'),
     c('<p><code>try_join!</code> 宏必须在 async 函数、闭包和块内使用。</p>')),

    (b('<p>Similar to <a href="macro.join.html" title="macro tokio::join"><code>join!</code></a>, the <code>try_join!</code> macro takes a list of async\n'
       'expressions and evaluates them concurrently on the same task. Each async\n'
       'expression evaluates to a future and the futures from each expression are\n'
       'multiplexed on the current task. The <code>try_join!</code> macro returns when all\n'
       'branches return with <code>Ok</code>, or on the first <code>Err</code> returned by one of the branches.</p>'),
     c('<p>与 <a href="macro.join.html" title="macro tokio::join"><code>join!</code></a> 类似，<code>try_join!</code> 宏接受一个 async 表达式列表，\n'
       '并在同一任务上并发地执行它们。每个 async 表达式求值为一个 future，\n'
       '来自每个表达式的 future 在当前任务上多路复用。<code>try_join!</code> 宏在所有分支返回 <code>Ok</code> 时返回，\n'
       '或在某个分支返回第一个 <code>Err</code> 时返回。</p>')),
]


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
            for old, zn in PAIRS:
                if old in new:
                    new = new.replace(old, zn)
                    hits += 1
            if new != raw:
                with open(path, 'wb') as fh:
                    fh.write(new)
                modified += 1

    # Check which pairs got zero hits
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
            missed_pairs.append(old[:60].decode('utf-8', errors='replace'))

    print(f'Modified files: {modified}')
    print(f'Pair matches (total): {hits}')
    print(f'Pairs never applied: {len(missed_pairs)}')
    for m in missed_pairs:
        print(f'  {m!r}')


if __name__ == '__main__':
    main()