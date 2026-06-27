#!/usr/bin/env python3
"""
翻译 tokio/ 下所有 .html 中 <span class="comment">// ...</span> 内的英文注释。

输入: tokio/ 下所有 .html
输出: 同名 .html（就地修改）

设计要点：
- 对每个 <span class="comment">...</span>，按 \\n 切分成行
- 每行用 regex 匹配 ^(\\s*)//\\s+(.*?)\\s*$ 提取前导空白与注释文本
- 注释文本查 dict 得中文
- 重建该行：{indent}// {zh}，保留 \\r
- 字典未覆盖则保留英文原文（仅打印 warning）
- 不动其他 HTML 结构（<pre>、<code>、<span class="kw"> 等）
"""
import os
import re
import sys

# 字典：(英文注释文本（去除前导 // 和首尾空白） -> 中文译文)
COMMENT_PAIRS = [
    # === sync (one remaining: '...') ===
    ('...', '...'),

    # === io / AsyncBufRead ===
    ('Flush the buffer before it goes out of scope.', '在缓冲区离开作用域前刷新它。'),
    ('Remove all interests at once.', '一次性移除所有关注。'),
    ('Removing all interests from the set returns `None`.', '从集合中移除所有关注会返回 `None`。'),
    ('Unless flushed or shut down, the contents of the buffer is discarded on drop.', '除非刷新或关闭，否则缓冲区的内容会在 drop 时被丢弃。'),
    ('Write a byte to the buffer.', '向缓冲区写入一个字节。'),

    # === net / TcpSocket / TcpStream / UdpSocket / pipe / Pipe ===
    ('Connect to a peer', '连接到对等方'),
    ('Try to read data, this may still fail with `WouldBlock`', '尝试读取数据，这仍可能因 `WouldBlock` 而失败'),
    ('if the readiness event is a false positive.', '因为就绪事件可能是误报。'),
    ('Try to write data, this may still fail with `WouldBlock`', '尝试写入数据，这仍可能因 `WouldBlock` 而失败'),
    ('Try to send data, this may still fail with `WouldBlock`', '尝试发送数据，这仍可能因 `WouldBlock` 而失败'),
    ('Try to recv data, this may still fail with `WouldBlock`', '尝试接收数据，这仍可能因 `WouldBlock` 而失败'),
    ('Creating the buffer **after** the `await` prevents it from', '在 `await` **之后** 创建缓冲区可以防止它'),
    ('being stored in the async task.', '被存储在异步任务中。'),
    ('The buffer is **not** included in the async task and will only exist', '该缓冲区**不**属于异步任务的一部分，仅存在于'),
    ('on the stack.', '栈上。'),
    ('The buffer is **not** included in the async task and will', '该缓冲区**不**属于异步任务的一部分，'),
    ('only exist on the stack.', '仅存在于栈上。'),
    ('Wait for the pipe to be readable', '等待管道可读'),
    ('Wait for the pipe to be writable', '等待管道可写'),
    ('Wait for the socket to be readable', '等待 socket 可读'),
    ('Wait for the socket to be writable', '等待 socket 可写'),
    ('On platforms with Berkeley-derived sockets, this allows to quickly', '在基于 Berkeley 套接字的平台上，这允许快速'),
    ('rebind a socket, without needing to wait for the OS to clean up the', '重新绑定一个 socket，而无需等待操作系统清理'),
    ('previous one.', '先前的那个。'),
    ('On Windows, this allows rebinding sockets which are actively in use,', '在 Windows 上，这允许重新绑定正在使用的 socket，'),
    ('which allows "socket hijacking", so we explicitly don\'t set it here.', '但这会导致 "socket hijacking"，因此我们显式不在此处设置。'),
    ('https://docs.microsoft.com/en-us/windows/win32/winsock/using-so-reuseaddr-and-so-exclusiveaddruse', 'https://docs.microsoft.com/en-us/windows/win32/winsock/using-so-reuseaddr-and-so-exclusiveaddruse'),
    ('Note: the actual backlog used by `TcpListener::bind` is platform-dependent,', '注意：`TcpListener::bind` 实际使用的 backlog 取决于平台，'),
    ('as Tokio relies on Mio\'s default backlog value configuration. The `1024` here is only', '因为 Tokio 依赖 Mio 的默认 backlog 配置。此处的 `1024` 仅作'),
    ('illustrative and does not reflect the real value used.', '说明，并不反映实际使用的值。'),
    ('Bind socket', '绑定 socket'),
    ('Bind a UDP socket', '绑定一个 UDP socket'),
    ('Create a socket', '创建一个 socket'),
    ('Construct the next server to be connected before sending the one', '在将已有的 server 发送到任务之前，先构造下一个'),
    ('we already have of onto a task. This ensures that the server', '待连接的 server。这可确保 server 在任务结束前'),
    ('isn\'t closed (after it\'s done in the task) before a new one is', '不会先关闭（任务结束后），新的 server 才可用，'),
    ('available. Otherwise the client might error with', '否则客户端可能会报'),
    ('`io::ErrorKind::NotFound`.', '`io::ErrorKind::NotFound` 错误。'),
    ('The first server needs to be constructed early so that clients can', '需要尽早构造第一个 server，以便客户端'),
    ('be correctly connected. Otherwise calling .wait will cause the client to', '能正确连接。否则调用 .wait 会导致客户端'),
    ('error.', '出错。'),
    ('Here we also make use of `first_pipe_instance`, which will ensure that', '这里还使用了 `first_pipe_instance`，以确保'),
    ('there are no other servers up and running already.', '当前没有其它 server 已在运行。'),
    ('Write fails with an OS-specific error after client has been', '在客户端断开连接后，写入会以'),
    ('disconnected.', '操作系统特定的错误失败。'),
    ('Forcibly disconnect the client.', '强制断开客户端。'),
    ('The first server needs to be constructed early so that clients can', '需要尽早构造第一个 server，以便客户端'),  # duplicate safe

    # === runtime / runtime::Handle ===
    ('Create the runtime', '创建 runtime'),
    ('Spawn a future onto the runtime', '在 runtime 上派生 future'),
    ('Spawn a blocking function onto the runtime', '在 runtime 上派生阻塞函数'),
    ('Spawn a future onto the runtime using the handle', '使用 handle 在 runtime 上派生 future'),
    ('Spawn a blocking function onto the runtime using the handle', '使用 handle 在 runtime 上派生阻塞函数'),
    ('Use the runtime...', '使用 runtime...'),
    ('Use the handle...', '使用 handle...'),
    ('Use the connected client...', '使用已连接的客户端...'),
    ('use the connected client.', '使用已连接的客户端。'),
    ('Await the result of the spawned task.', '等待派生任务的结果。'),
    ('`res` is the value returned from the thread', '`res` 是从线程返回的值'),
    ('By entering the context, we tie `tokio::spawn` to this executor.', '通过进入此上下文，我们将 `tokio::spawn` 绑定到此执行器。'),
    ('Had we not used `rt.enter` below, this would panic.', '如果下面没有使用 `rt.enter`，这里会 panic。'),
    ('This next line would cause a panic because we haven\'t entered the runtime', '下面这一行会导致 panic，因为我们尚未进入 runtime'),
    ('and created an EnterGuard', '并创建 EnterGuard'),
    ('let handle2 = Handle::current(); // panic', 'let handle2 = Handle::current(); // panic'),
    ('So we create a guard here with Handle::enter();', '因此我们在这里用 Handle::enter() 创建一个 guard；'),
    ('In a loop, read data from the socket and write the data back.', '在循环中，从 socket 读取数据并将其写回。'),
    ('Now we can call Handle::current();', '现在我们可以调用 Handle::current()；'),
    ('Notice that the handle is created outside of this thread and then moved in', '注意，handle 是在该线程外创建然后移入的'),
    ('Using Handle::block_on to run async code in the new thread.', '使用 Handle::block_on 在新线程中运行 async 代码。'),
    ('Resume the panic on the main task', '在主任务上恢复 panic'),
    ('Stop looping `future` will be polled after completion', '停止循环 `future` 在完成后仍会被轮询'),
    ('Do stuff w/ rc', '用 rc 做些操作'),

    # === task / spawn / LocalSet / JoinHandle / coop ===
    ('This call will make them start running in the background', '此调用会让它们在后台开始运行'),
    ('immediately.', '立即开始。'),
    ('`Rc` does not implement `Send`, and thus may not be sent between', '`Rc` 没有实现 `Send`，因此不能在线程间'),
    ('threads safely.', '安全地发送。'),
    ('Because the `async` block here moves `nonsend_data`, the future is `!Send`.', '因为这里的 `async` 块会移动 `nonsend_data`，所以 future 是 `!Send` 的。'),
    ('Since `tokio::spawn` requires the spawned future to implement `Send`, this', '由于 `tokio::spawn` 要求派生的 future 实现 `Send`，'),
    ('will not compile.', '这段代码无法编译。'),
    ('`spawn_local` ensures that the future is spawned on the local', '`spawn_local` 确保 future 被派生到本地'),
    ('task set.', '任务集上。'),
    ('This struct describes the task you want to spawn. Here we include', '该结构体描述要派生的任务。这里我们给出一个'),
    ('some simple examples. The oneshot channel allows sending a response', '简单的示例。oneshot 通道允许向派生者'),
    ('to the spawner.', '发送响应。'),
    ('If the while loop returns, then all the LocalSpawner', '如果 while 循环返回，则所有 LocalSpawner'),
    ('objects have been dropped.', '对象都已被丢弃。'),
    ('This will return once all senders are dropped and all', '这将在所有发送端被丢弃且所有'),
    ('spawned tasks have returned.', '派生任务返回后返回。'),
    ('This task may do !Send stuff. We use printing a number as an example,', '此任务可能会执行 !Send 的操作。我们以打印数字为例，'),
    ('but it could be anything.', '但它可以是任何操作。'),
    ('The Task struct is an enum to support spawning many different kinds', 'Task 结构体是一个 enum，以支持派生多种不同类型'),
    ('of operations.', '的操作。'),
    ('Spawn a future on the local set. This future will be run when', '在本地集上派生一个 future。此 future 将在我们'),
    ('we call `run_until` to drive the task set.', '调用 `run_until` 驱动任务集时运行。'),
    ('When `run` finishes, we can spawn _more_ futures, which will', '当 `run` 结束后，我们可以再派生 _更多_ future，它们'),
    ('run in subsequent calls to `run_until`.', '会在后续的 `run_until` 调用中运行。'),
    ('Wait for the task to finish', '等待任务完成'),
    ('Wait for the task before we end the test.', '在结束测试前等待任务。'),
    ('We make sure that the new task has time to run, before the main', '我们确保新任务有时间运行，然后主任务'),
    ('task returns.', '才返回。'),
    ('The returned result indicates that the task failed.', '返回的结果表明任务失败。'),
    ('This will be called, even though the JoinHandle is dropped.', '即使 JoinHandle 已被丢弃，此函数仍会被调用。'),
    ('do some other stuff here', '在此处做些其它事情'),
    ('do some stuff here', '在此处做些事情'),
    ('do some compute-heavy work or call synchronous code', '执行一些计算密集型工作或调用同步代码'),
    ('do work here', '在此处工作'),
    ('do work with socket here', '在此处使用 socket 工作'),
    ('do something async', '执行一些异步操作'),
    ('perform some work here...', '在此处执行一些工作...'),
    ('some work here', '此处为一些工作'),
    ('some blocking work here', '此处为一些阻塞工作'),
    ('error.', '错误。'),
    ('Yield, allowing the newly-spawned task to execute first.', '让出执行权，让新派生的任务先执行。'),
    ('And await', '并等待'),
    ('And here, we can take task local value', '这里可以取到 task 本地值'),
    ('Force the `Rc` to stay in a scope with no `.await`', '强制让 `Rc` 留在没有 `.await` 的作用域中'),
    ('Construct a local task set that can run `!Send` futures.', '构造一个可以运行 `!Send` future 的本地任务集。'),
    ('This will always be ready. If coop was in effect, this code would be forced to yield', '这将始终就绪。如果 coop 生效，此代码将被迫让出'),
    ('periodically. However, if left unconstrained, then this code will never yield.', '执行权，周期性地让出。但如果不受限制，此代码将永远不会让出。'),
    ('We received a value, so consume budget.', '我们收到了一个值，因此消耗预算。'),
    ('it is the underlying future that exhausted the budget', '是底层 future 耗尽了预算'),
    ('Pass ownership of the value back to the asynchronous context', '将该值的所有权交还给异步上下文'),
    ('Inside an async block or function.', '在 async 块或函数内。'),
    ('Some blocking work here', '此处为一些阻塞工作'),  # alternate

    # === time / Interval / MissedTickBehavior / timeout / timeout_at / interval_at ===
    ('First tick resolves immediately after creation', '第一次 tick 在创建后立即解析'),
    ('ticks after 10ms', '在 10ms 后 tick'),
    ('ticks after 50ms', '在 50ms 后 tick'),
    ('ticks every 2 milliseconds', '每 2 毫秒 tick 一次'),
    ('ticks immediately', '立即 tick'),
    ('approximately 0ms have elapsed. The first tick completes immediately.', '大约已过去 0ms。第一次 tick 立即完成。'),
    ('approximately 20ms have elapsed.', '大约已过去 20ms。'),
    ('approximately 70ms have elapsed.', '大约已过去 70ms。'),
    ('approximately 150ms have elapsed.', '大约已过去 150ms。'),
    ('approximately 170ms have elapsed.', '大约已过去 170ms。'),
    ('approximately 180ms have elapsed.', '大约已过去 180ms。'),
    ('approximately 250ms have elapsed.', '大约已过去 250ms。'),
    ('The `Interval` has missed a tick', '`Interval` 错过了一次 tick'),
    ('Since we have exceeded our timeout, this will resolve immediately', '由于已超过 timeout，这会立即解析'),
    ('Since we are more than 100ms after the start of `interval`, this will', '由于距 `interval` 开始已超过 100ms，因此'),
    ('also resolve immediately.', '也会立即解析。'),
    ('Also resolves immediately, because it was supposed to resolve at', '也会立即解析，因为它本应在 `interval` 开始后'),
    ('150ms after the start of `interval`', '150ms 时解析'),
    ('Since we have gotten to 200ms after the start of `interval`, this', '由于距 `interval` 开始已过去 200ms，因此这'),
    ('will resolve after 50ms', '将在 50ms 后解析'),
    ('But this one, rather than also resolving immediately, as might happen', '但这个不会像 `Burst` 或 `Skip` 行为那样立即'),
    ('with the `Burst` or `Skip` behaviors, will not resolve until', '解析，而是在上面调用 `tick` 之后'),
    ('50ms after the call to `tick` up above. That is, in `tick`, when we', '50ms 后才解析。即在 `tick` 中，当我们识别到'),
    ('recognize that we missed a tick, we schedule the next tick to happen', '错过了一次 tick 时，我们将下一次 tick 安排为'),
    ('50ms (or whatever the `period` is) from right then, not from when', '从此刻起 50ms（或 `period` 设定的值）后，而不是'),
    ('were *supposed* to tick', '本应 tick 的时刻起'),
    ('This one will resolve after 25ms, 100ms after the start of', '这个将在 25ms 后解析，即 `interval` 开始后 100ms，'),
    ('`interval`, which is the closest multiple of `period` from the start', '这是 `period` 在 `interval` 开始的最近倍数，'),
    ('of `interval` after the call to `tick` up above.', '发生在上面 `tick` 调用之后。'),
    ('0ns', '0ns'),
    ('Since we have exceeded our timeout, this will resolve immediately', '由于已超过 timeout，这会立即解析'),  # duplicate safe
    ('Wrap the future with a `Timeout` set to expire 10 milliseconds into the', '将 future 包装在一个 `Timeout` 中，设置为 10 毫秒后'),
    ('future.', '过期。'),
    ('Wrap the future with a `Timeout` set to expire in 10 milliseconds.', '将 future 包装在一个 `Timeout` 中，设置为 10 毫秒后过期。'),
    ('if this takes more than 2 milliseconds, a tick will be delayed', '如果这耗时超过 2 毫秒，tick 会被延迟'),
    ('evaluate the timeout', '评估 timeout'),

    # === macros / 一些通用占位 ===
    ('Complete the TaskLocalFuture', '完成 TaskLocalFuture'),
    ('Resolves immediately', '立即解析'),
    ('Use `StreamExt::next` to obtain a `Future` that resolves to the next value', '使用 `StreamExt::next` 获取一个解析为下一个值的 `Future`'),
    ('Initial input', '初始输入'),
    ('future。', 'future。'),  # 原句末尾就是全角句号
    ('None', 'None'),
    ('future.', 'future。'),
    ('to the spawner.', '发送给派生者。'),
    ('spawn the root task', '派生根任务'),
    ('Spawn the root task', '派生根任务'),
    ('Spawn the server loop.', '派生 server 循环。'),
    ('Wait for a client to connect.', '等待客户端连接。'),
    ('Wait for a client to become connected.', '等待客户端连接。'),
    ('Do some async work', '执行一些异步工作'),
    ('Write some data', '写入一些数据'),
    ('Write some data.', '写入一些数据。'),
    ('Write the data back', '将数据写回'),
    ('Read the data', '读取数据'),
    ('Peek at the data', '窥探数据'),
    ('send to remote_addr', '发送到 remote_addr'),
    ('recv from remote_addr', '从 remote_addr 接收'),
    ('use `sock`', '使用 `sock`'),
    ('use the listener', '使用 listener'),
    ('Process each socket concurrently.', '并发处理每个 socket。'),
    ('the address the socket is bound to', 'socket 绑定的地址'),
    ('socket closed', 'socket 已关闭'),
    ('send to remote_addr', '发送到 remote_addr'),  # dup
    ('recv from remote_addr', '从 remote_addr 接收'),  # dup
    ('of operations.', '的操作。'),
    ('check if the future is ready', '检查 future 是否就绪'),
    ('Stand in for complex computation', '代表复杂计算'),
    ('Stand-in for compute-heavy work or using synchronous APIs', '代表计算密集型工作或使用同步 API'),
    ('False-positive, continue', '误报，继续'),
    ('Writable false positive.', '可写误报。'),
    ('task returns.', '任务返回。'),
    ('Here we sleep to make sure that the first task returns before.', '这里休眠以确保第一个任务先返回。'),
    ('We ignore failures to send the response.', '我们忽略发送响应时的失败。'),
    ('OK: since, we\'ve closed the other instance.', 'OK：因为我们已经关闭了另一个实例。'),
    ('Second server errs, since it\'s not the first instance.', '第二个 server 出错，因为不是第一个实例。'),
    ('Still too many servers even if we specify a higher value!', '即使指定更高的值，server 数量仍然过多！'),
    ('Too many servers!', 'server 数量过多！'),
    ('Server must be created in order for the client creation to succeed.', '必须先创建 server，客户端创建才能成功。'),
    ('Wrap it a cooperative wrapper', '用协作包装器包装它'),
    ('Send a message', '发送一条消息'),

    # === 一些 short ones ===
    ('read a line into buffer', '将一行读入缓冲区'),
    ('read up to 10 bytes', '读取最多 10 个字节'),
    ('be correctly connected. Otherwise calling .wait will cause the client to', '能正确连接。否则调用 .wait 会导致客户端'),
    ('task returns.', '任务返回。'),
]


def translate_span(span_inner: str, dictionary: dict) -> tuple[str, int, list]:
    """
    给定 <span class="comment"> 与 </span> 之间的内容（含 \\r\\n 换行），
    逐行翻译 // 注释。返回 (new_inner, n_replaced, skipped)。
    """
    lines = span_inner.split('\n')
    out = []
    n = 0
    skipped = []
    for line in lines:
        m = re.match(r'^(\s*)//\s+(.*?)\s*$', line)
        if not m:
            out.append(line)
            continue
        indent, txt = m.group(1), m.group(2)
        if re.search(r'[一-鿿]', txt):
            out.append(line)
            continue
        if txt in dictionary:
            zh = dictionary[txt]
            if zh:
                out.append(f"{indent}// {zh}")
                n += 1
            else:
                out.append(None)  # 已合并，删除该行
                n += 1
        else:
            skipped.append(txt)
            out.append(line)
    parts = [p for p in out if p is not None]
    return '\n'.join(parts), n, skipped


def translate_file(path: str, dictionary: dict, dry: bool = False) -> tuple[int, list]:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    total = 0
    out = []
    pos = 0
    all_skipped = []
    for m in re.finditer(r'<span class="comment">(.*?)</span>', content, flags=re.DOTALL):
        out.append(content[pos:m.start()])
        new_inner, n, skipped = translate_span(m.group(1), dictionary)
        out.append(f'<span class="comment">{new_inner}</span>')
        total += n
        all_skipped.extend(skipped)
        pos = m.end()
    out.append(content[pos:])
    new_content = ''.join(out)
    if not dry and new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    return total, all_skipped


def main():
    if len(sys.argv) < 2:
        print("Usage: python _translate_code_comments.py <tokio_dir> [--apply]")
        sys.exit(1)
    tokio_dir = sys.argv[1]
    dry = '--apply' not in sys.argv
    if dry:
        print("DRY RUN: will not modify files")
    else:
        print("APPLY: will modify files in place")
    dictionary = dict(COMMENT_PAIRS)
    print(f"Dictionary: {len(dictionary)} entries")
    grand_total = 0
    grand_skipped = set()
    file_count = 0
    for root, dirs, files in os.walk(tokio_dir):
        # Skip backup dirs
        dirs[:] = [d for d in dirs if d not in ('_old', '_backups', '_scripts', '__pycache__', 'static.files', 'src')]
        for fname in files:
            if not fname.endswith('.html'):
                continue
            path = os.path.join(root, fname)
            n, skipped = translate_file(path, dictionary, dry=dry)
            if n:
                file_count += 1
            grand_total += n
            for s in skipped:
                grand_skipped.add(s)
    print(f"Files modified: {file_count}")
    print(f"Total: {grand_total} comment lines {'(dry)' if dry else 'translated'}")
    if grand_skipped:
        print(f"\n{len(grand_skipped)} unique untranslated comment texts (not in dict):")
        for s in sorted(grand_skipped):
            print(f"  {repr(s)}")


if __name__ == '__main__':
    main()
