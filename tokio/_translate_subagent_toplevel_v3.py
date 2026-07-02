#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Translate remaining untranslated content in tokio top-level files.

Uses bytes mode for HTML editing to preserve CRLF and special UTF-8 chars.
"""
import os

CRLF = b'\r\n'

# Patterns from actual file content (extracted via _dump_blocks.py)
PAIRS = []

def add(en, zh):
    if isinstance(en, str): en = en.encode('utf-8')
    if isinstance(zh, str): zh = zh.encode('utf-8')
    PAIRS.append((en, zh))

# ============== tokio/attr.main.html h3 ==============
add(
    b'<h3 id="multi-threaded"><a class="doc-anchor" href="#multi-threaded">\xc2\xa7</a>Multi-threaded</h3>',
    '<h3 id="multi-threaded"><a class="doc-anchor" href="#multi-threaded">\xc2\xa7</a>多线程</h3>'.encode('utf-8')
)
add(
    b'<h3 id="current-thread"><a class="doc-anchor" href="#current-thread">\xc2\xa7</a>Current-thread</h3>',
    '<h3 id="current-thread"><a class="doc-anchor" href="#current-thread">\xc2\xa7</a>当前线程</h3>'.encode('utf-8')
)
add(
    b'<h3 id="local"><a class="doc-anchor" href="#local">\xc2\xa7</a>Local</h3>',
    '<h3 id="local"><a class="doc-anchor" href="#local">\xc2\xa7</a>本地</h3>'.encode('utf-8')
)
add(
    b'<h3 id="set-the-name-of-the-runtime"><a class="doc-anchor" href="#set-the-name-of-the-runtime">\xc2\xa7</a>Set the name of the runtime</h3>',
    '<h3 id="set-the-name-of-the-runtime"><a class="doc-anchor" href="#set-the-name-of-the-runtime">\xc2\xa7</a>设置运行时名称</h3>'.encode('utf-8')
)
add(
    b'<h3 id="using-the-multi-threaded-runtime"><a class="doc-anchor" href="#using-the-multi-threaded-runtime">\xc2\xa7</a>Using the multi-threaded runtime</h3>',
    '<h3 id="using-the-multi-threaded-runtime"><a class="doc-anchor" href="#using-the-multi-threaded-runtime">\xc2\xa7</a>使用多线程运行时</h3>'.encode('utf-8')
)
add(
    b'<h3 id="using-the-current-thread-runtime"><a class="doc-anchor" href="#using-the-current-thread-runtime">\xc2\xa7</a>Using the current-thread runtime</h3>',
    '<h3 id="using-the-current-thread-runtime"><a class="doc-anchor" href="#using-the-current-thread-runtime">\xc2\xa7</a>使用当前线程运行时</h3>'.encode('utf-8')
)
add(
    b'<h3 id="using-the-local-runtime"><a class="doc-anchor" href="#using-the-local-runtime">\xc2\xa7</a>Using the local runtime</h3>',
    '<h3 id="using-the-local-runtime"><a class="doc-anchor" href="#using-the-local-runtime">\xc2\xa7</a>使用本地运行时</h3>'.encode('utf-8')
)
add(
    b'<h3 id="set-number-of-worker-threads"><a class="doc-anchor" href="#set-number-of-worker-threads">\xc2\xa7</a>Set number of worker threads</h3>',
    '<h3 id="set-number-of-worker-threads"><a class="doc-anchor" href="#set-number-of-worker-threads">\xc2\xa7</a>设置工作线程数</h3>'.encode('utf-8')
)
add(
    b'<h3 id="configure-the-runtime-to-start-with-time-paused"><a class="doc-anchor" href="#configure-the-runtime-to-start-with-time-paused">\xc2\xa7</a>Configure the runtime to start with time paused</h3>',
    '<h3 id="configure-the-runtime-to-start-with-time-paused"><a class="doc-anchor" href="#configure-the-runtime-to-start-with-time-paused">\xc2\xa7</a>配置运行时启动时暂停时间</h3>'.encode('utf-8')
)
add(
    b'<h3 id="rename-package"><a class="doc-anchor" href="#rename-package">\xc2\xa7</a>Rename package</h3>',
    '<h3 id="rename-package"><a class="doc-anchor" href="#rename-package">\xc2\xa7</a>重命名包</h3>'.encode('utf-8')
)
add(
    b'<h3 id="configure-unhandled-panic-behavior"><a class="doc-anchor" href="#configure-unhandled-panic-behavior">\xc2\xa7</a>Configure unhandled panic behavior</h3>',
    '<h3 id="configure-unhandled-panic-behavior"><a class="doc-anchor" href="#configure-unhandled-panic-behavior">\xc2\xa7</a>配置未处理 panic 的行为</h3>'.encode('utf-8')
)

# ============== tokio/attr.test.html h3/h4 ==============
add(
    b'<h3 id="usage"><a class="doc-anchor" href="#usage">\xc2\xa7</a>Usage</h3>',
    '<h3 id="usage"><a class="doc-anchor" href="#usage">\xc2\xa7</a>用法</h3>'.encode('utf-8')
)
add(
    b'<h4 id="set-the-name-of-the-runtime"><a class="doc-anchor" href="#set-the-name-of-the-runtime">\xc2\xa7</a>Set the name of the runtime</h4>',
    '<h4 id="set-the-name-of-the-runtime"><a class="doc-anchor" href="#set-the-name-of-the-runtime">\xc2\xa7</a>设置运行时名称</h4>'.encode('utf-8')
)
add(
    b'<h4 id="using-the-multi-thread-runtime"><a class="doc-anchor" href="#using-the-multi-thread-runtime">\xc2\xa7</a>Using the multi-thread runtime</h4>',
    '<h4 id="using-the-multi-thread-runtime"><a class="doc-anchor" href="#using-the-multi-thread-runtime">\xc2\xa7</a>使用多线程运行时</h4>'.encode('utf-8')
)
add(
    b'<h4 id="using-current-thread-runtime"><a class="doc-anchor" href="#using-current-thread-runtime">\xc2\xa7</a>Using current thread runtime</h4>',
    '<h4 id="using-current-thread-runtime"><a class="doc-anchor" href="#using-current-thread-runtime">\xc2\xa7</a>使用当前线程运行时</h4>'.encode('utf-8')
)
add(
    b'<h4 id="set-number-of-worker-threads"><a class="doc-anchor" href="#set-number-of-worker-threads">\xc2\xa7</a>Set number of worker threads</h4>',
    '<h4 id="set-number-of-worker-threads"><a class="doc-anchor" href="#set-number-of-worker-threads">\xc2\xa7</a>设置工作线程数</h4>'.encode('utf-8')
)
add(
    b'<h4 id="configure-the-runtime-to-start-with-time-paused"><a class="doc-anchor" href="#configure-the-runtime-to-start-with-time-paused">\xc2\xa7</a>Configure the runtime to start with time paused</h4>',
    '<h4 id="configure-the-runtime-to-start-with-time-paused"><a class="doc-anchor" href="#configure-the-runtime-to-start-with-time-paused">\xc2\xa7</a>配置运行时启动时暂停时间</h4>'.encode('utf-8')
)
add(
    b'<h4 id="rename-package"><a class="doc-anchor" href="#rename-package">\xc2\xa7</a>Rename package</h4>',
    '<h4 id="rename-package"><a class="doc-anchor" href="#rename-package">\xc2\xa7</a>重命名包</h4>'.encode('utf-8')
)
add(
    b'<h4 id="configure-unhandled-panic-behavior"><a class="doc-anchor" href="#configure-unhandled-panic-behavior">\xc2\xa7</a>Configure unhandled panic behavior</h4>',
    '<h4 id="configure-unhandled-panic-behavior"><a class="doc-anchor" href="#configure-unhandled-panic-behavior">\xc2\xa7</a>配置未处理 panic 的行为</h4>'.encode('utf-8')
)

# ============== tokio/macro.join.html h3 ==============
add(
    b'<h3 id="runtime-characteristics"><a class="doc-anchor" href="#runtime-characteristics">\xc2\xa7</a>Runtime characteristics</h3>',
    '<h3 id="runtime-characteristics"><a class="doc-anchor" href="#runtime-characteristics">\xc2\xa7</a>运行时特征</h3>'.encode('utf-8')
)
add(
    b'<h3 id="fairness"><a class="doc-anchor" href="#fairness">\xc2\xa7</a>Fairness</h3>',
    '<h3 id="fairness"><a class="doc-anchor" href="#fairness">\xc2\xa7</a>公平性</h3>'.encode('utf-8')
)

# ============== tokio/macro.select.html h3/h4 ==============
add(
    b'<h3 id="avoid-racy-if-preconditions"><a class="doc-anchor" href="#avoid-racy-if-preconditions">\xc2\xa7</a>Avoid racy <code>if</code> preconditions</h3>',
    '<h3 id="avoid-racy-if-preconditions"><a class="doc-anchor" href="#avoid-racy-if-preconditions">\xc2\xa7</a>避免存在竞争条件的 <code>if</code> 前置条件</h3>'.encode('utf-8')
)
add(
    b'<h3 id="merging-streams"><a class="doc-anchor" href="#merging-streams">\xc2\xa7</a>Merging Streams</h3>',
    '<h3 id="merging-streams"><a class="doc-anchor" href="#merging-streams">\xc2\xa7</a>合并流</h3>'.encode('utf-8')
)
add(
    b'<h3 id="racing-futures"><a class="doc-anchor" href="#racing-futures">\xc2\xa7</a>Racing Futures</h3>',
    '<h3 id="racing-futures"><a class="doc-anchor" href="#racing-futures">\xc2\xa7</a>Future 竞速</h3>'.encode('utf-8')
)
add(
    b'<h4 id="example-with-select"><a class="doc-anchor" href="#example-with-select">\xc2\xa7</a>Example with <code>select!</code></h4>',
    '<h4 id="example-with-select"><a class="doc-anchor" href="#example-with-select">\xc2\xa7</a>使用 <code>select!</code> 的示例</h4>'.encode('utf-8')
)
add(
    b'<h4 id="moving-to-merge"><a class="doc-anchor" href="#moving-to-merge">\xc2\xa7</a>Moving to <code>merge</code></h4>',
    '<h4 id="moving-to-merge"><a class="doc-anchor" href="#moving-to-merge">\xc2\xa7</a>改用 <code>merge</code></h4>'.encode('utf-8')
)

# ============== tokio/index.html h3 ==============
add(
    b'<h3 id="cpu-bound-tasks-and-blocking-code"><a class="doc-anchor" href="#cpu-bound-tasks-and-blocking-code">\xc2\xa7</a>CPU-bound tasks and blocking code</h3>',
    '<h3 id="cpu-bound-tasks-and-blocking-code"><a class="doc-anchor" href="#cpu-bound-tasks-and-blocking-code">\xc2\xa7</a>CPU 密集型任务与阻塞代码</h3>'.encode('utf-8')
)
add(
    b'<h3 id="asynchronous-io"><a class="doc-anchor" href="#asynchronous-io">\xc2\xa7</a>Asynchronous IO</h3>',
    '<h3 id="asynchronous-io"><a class="doc-anchor" href="#asynchronous-io">\xc2\xa7</a>异步 I/O</h3>'.encode('utf-8')
)
add(
    b'<h3 id="unstable-features"><a class="doc-anchor" href="#unstable-features">\xc2\xa7</a>Unstable features</h3>',
    '<h3 id="unstable-features"><a class="doc-anchor" href="#unstable-features">\xc2\xa7</a>不稳定特性</h3>'.encode('utf-8')
)
add(
    b'<h3 id="wasm-support"><a class="doc-anchor" href="#wasm-support">\xc2\xa7</a><code>WASM</code> support</h3>',
    '<h3 id="wasm-support"><a class="doc-anchor" href="#wasm-support">\xc2\xa7</a><code>WASM</code> 支持</h3>'.encode('utf-8')
)
add(
    b'<h3 id="unstable-wasm-support"><a class="doc-anchor" href="#unstable-wasm-support">\xc2\xa7</a>Unstable <code>WASM</code> support</h3>',
    '<h3 id="unstable-wasm-support"><a class="doc-anchor" href="#unstable-wasm-support">\xc2\xa7</a>不稳定的 <code>WASM</code> 支持</h3>'.encode('utf-8')
)

# ============== tokio/index.html dd items ==============
add(
    b'<dd>TCP/UDP/Unix bindings for <code>tokio</code>.</dd>',
    '<dd>tokio 的 TCP/UDP/Unix 绑定。</dd>'.encode('utf-8')
)
add(
    b'<dd>Due to the <code>Stream</code> trait\xe2\x80\x99s inclusion in <code>std</code> landing later than Tokio\xe2\x80\x99s 1.0\r\nrelease, most of the Tokio stream utilities have been moved into the <a href="https://docs.rs/tokio-stream"><code>tokio-stream</code></a>\r\ncrate.</dd>',
    '<dd>由于 <code>Stream</code> trait 进入 <code>std</code> 的时间晚于 Tokio 1.0 发布，\r\nTokio 大部分流相关工具已移至 <a href="https://docs.rs/tokio-stream"><code>tokio-stream</code></a> crate。</dd>'.encode('utf-8')
)
add(
    b'<dd>Waits on multiple concurrent branches, returning when <strong>all</strong> branches\r\ncomplete.</dd>',
    '<dd>等待多个并发分支，<strong>所有</strong>分支完成后返回。</dd>'.encode('utf-8')
)
add(
    b'<dd>Waits on multiple concurrent branches, returning when the <strong>first</strong> branch\r\ncompletes, cancelling the remaining branches.</dd>',
    '<dd>等待多个并发分支，<strong>首个</strong>分支完成后返回，\r\n并取消其余分支。</dd>'.encode('utf-8')
)
add(
    b'<dd>Declares a new task-local key of type <a href="task/struct.LocalKey.html" title="struct tokio::task::LocalKey"><code>tokio::task::LocalKey</code></a>.</dd>',
    '<dd>声明一个 <a href="task/struct.LocalKey.html" title="struct tokio::task::LocalKey"><code>tokio::task::LocalKey</code></a> 类型的新任务局部键。</dd>'.encode('utf-8')
)
add(
    b'<dd>Waits on multiple concurrent branches, returning when <strong>all</strong> branches\r\ncomplete with <code>Ok(_)</code> or on the first <code>Err(_)</code>.</dd>',
    '<dd>等待多个并发分支，<strong>所有</strong>分支以 <code>Ok(_)</code> 完成\r\n或首个 <code>Err(_)</code> 出现时返回。</dd>'.encode('utf-8')
)
add(
    b'<dd>Marks async function to be executed by the selected runtime. This macro\r\nhelps set up a <code>Runtime</code> without requiring the user to use\r\n<a href="../tokio/runtime/struct.Runtime.html">Runtime</a> or\r\n<a href="../tokio/runtime/struct.Builder.html">Builder</a> directly.</dd>',
    '<dd>将 async 函数标记为由所选运行时执行。该宏\r\n帮助设置 <code>Runtime</code>，无需用户直接使用\r\n<a href="../tokio/runtime/struct.Runtime.html">Runtime</a> 或\r\n<a href="../tokio/runtime/struct.Builder.html">Builder</a>。</dd>'.encode('utf-8')
)
add(
    b'<dd>Marks async function to be executed by runtime, suitable to test environment.\r\nThis macro helps set up a <code>Runtime</code> without requiring the user to use\r\n<a href="../tokio/runtime/struct.Runtime.html">Runtime</a> or\r\n<a href="../tokio/runtime/struct.Builder.html">Builder</a> directly.</dd>',
    '<dd>将 async 函数标记为由运行时执行，适合测试环境使用。\r\n该宏帮助设置 <code>Runtime</code>，无需用户直接使用\r\n<a href="../tokio/runtime/struct.Runtime.html">Runtime</a> 或\r\n<a href="../tokio/runtime/struct.Builder.html">Builder</a>。</dd>'.encode('utf-8')
)

# ============== tokio/index.html p[5] ==============
add(
    b'<p>Tokio is great for writing applications and most users in this case shouldn\xe2\x80\x99t\r\nworry too much about what features they should pick. If you\xe2\x80\x99re unsure, we suggest\r\ngoing with <code>full</code> to ensure that you don\xe2\x80\x99t run into any road blocks while you\xe2\x80\x99re\r\nbuilding your application.</p>',
    '<p>Tokio 非常适合编写应用程序，这种情况下大多数用户\r\n不必太担心应该选择哪些特性。如果你不确定，我们建议\r\n使用 <code>full</code>，以确保在开发过程中\r\n不会遇到任何障碍。</p>'.encode('utf-8')
)
# index.html p[7] partial translation - the second half needs translation
add(
    b'<p>\xe4\xbd\x9c\xe4\xb8\xba\xe4\xb8\x80\xe4\xb8\xaa\xe5\xba\x93\xe7\x9a\x84\xe4\xbd\x9c\xe8\x80\x85\xef\xbc\x8c\xe4\xbd\xa0\xe7\x9a\x84\xe7\x9b\xae\xe6\xa0\x87\xe5\xba\x94\xe8\xaf\xa5\xe6\x98\xaf\xe6\x8f\x90\xe4\xbe\x9b\xe4\xb8\x80\xe4\xb8\xaa\xe5\x9f\xba\xe4\xba\x8e Tokio \xe7\x9a\x84\xe6\x9c\x80\xe8\xbd\xbb\xe9\x87\x8f\xe7\x9a\x84 crate\xe3\x80\x82\r\n\xe4\xb8\xba\xe4\xba\x86\xe5\xae\x9e\xe7\x8e\xb0\xe8\xbf\x99\xe4\xb8\x80\xe7\x82\xb9\xef\xbc\x8c\xe4\xbd\xa0\xe5\xba\x94\xe8\xaf\xa5\xe4\xbf\x9d\xe8\xaf\x81\xe5\x8f\xaa\xe5\x90\xaf\xe7\x94\xa8\xe4\xbd\xa0\xe9\x9c\x80\xe8\xa6\x81\xe7\x9a\x84\xe7\x89\xb9\xe6\x80\xa7\xe3\x80\x82\xe8\xbf\x99\xe6\xa0\xb7\xe7\x94\xa8\xe6\x88\xb7\xe5\x8f\xaf\xe4\xbb\xa5our crate without having\r\nto enable unnecessary features.</p>',
    '<p>作为一个库的作者，你的目标应该是提供一个基于 Tokio 的最轻量的 crate。\r\n为了实现这一点，你应该保证只启用你需要的特性。这样用户可以在引入你的 crate 时不必启用\r\n不必要的特性。</p>'.encode('utf-8')
)

# index.html p[9] has "tokio::task module provides important tools for working with tasks:" - second half untranslated
add(
    b'<p>Rust \xe4\xb8\xad\xe7\x9a\x84\xe5\xbc\x82\xe6\xad\xa5\xe7\xa8\x8b\xe5\xba\x8f\xe5\x9f\xba\xe4\xba\x8e\xe8\xbd\xbb\xe9\x87\x8f\xe7\xba\xa7\xe3\x80\x81\xe9\x9d\x9e\xe9\x98\xbb\xe5\xa1\x9e\xe7\x9a\x84\r\n\xe6\x89\xa7\xe8\xa1\x8c\xe5\x8d\x95\xe5\x85\x83\xef\xbc\x8c\xe7\xa7\xb0\xe4\xb8\xba <a href="#working-with-tasks"><em>tasks</em></a>\xe3\x80\x82<a href="task/index.html" title="mod tokio::task"><code>tokio::task</code></a> module provides\r\nimportant tools for working with tasks:</p>',
    '<p>Rust 中的异步程序基于轻量级、非阻塞的\r\n执行单元，称为 <a href="#working-with-tasks"><em>tasks</em></a>。<a href="task/index.html" title="mod tokio::task"><code>tokio::task</code></a> 模块提供了\r\n使用任务的重要工具：</p>'.encode('utf-8')
)

# index.html p[11]: already partial chinese, fix to make whole paragraph
add(
    b'<p><a href="sync/index.html" title="mod tokio::sync"><code>tokio::sync</code></a> \xe6\xa8\xa1\xe5\x9d\x97\xe5\x8c\x85\xe5\x90\xab\xe7\x94\xa8\xe4\xba\x8e\xe9\x9c\x80\xe8\xa6\x81\xe9\x80\x9a\xe4\xbf\xa1\xe6\x88\x96\xe5\x85\xb1\xe4\xba\xab\xe6\x95\xb0\xe6\x8d\xae\xe6\x97\xb6\xe4\xbd\xbf\xe7\x94\xa8\xe7\x9a\x84\xe5\x90\x8c\xe6\xad\xa5\xe5\x8e\x9f\xe8\xaf\xad\xef\xbc\x8c\xe5\x8c\x85\xe6\x8b\xac\xef\xbc\x9a</p>',
    '<p><a href="sync/index.html" title="mod tokio::sync"><code>tokio::sync</code></a> 模块包含需要通信或共享数据时使用的同步原语，包括：</p>'.encode('utf-8')
)

# index.html p[13]: already partial chinese, second half English
add(
    b'<p><a href="time/index.html" title="mod tokio::time"><code>tokio::time</code></a> \xe6\xa8\xa1\xe5\x9d\x97\xe6\x8f\x90\xe4\xbe\x9b\xe7\x94\xa8\xe4\xba\x8e\xe8\xb7\x9f\xe8\xb8\xaa\xe6\x97\xb6\xe9\x97\xb4\xe5\x92\x8c\r\n\xe8\xb0\x83\xe5\xba\xa6\xe4\xbb\xbb\xe5\x8a\xa1\xe7\x9a\x84\xe5\xb7\xa5\xe5\x85\xb7\xe3\x80\x82\xe5\x8c\x85\xe6\x8b\xac\xe4\xb8\xba\xe4\xbb\xbb\xe5\x8a\xa1\xe8\xae\xbe\xe7\xbd\xae<a href="time/fn.timeout.html" title="fn tokio::time::timeout">\xe8\xb6\x85\xe6\x97\xb6</a>\xef\xbc\x8c\r\n\xe5\xb0\x86<a href="time/fn.sleep.html" title="fn tokio::time::sleep">\xe4\xbb\xbb\xe5\x8a\xa1\xe7\x9d\xa1\xe7\x9c\xa0</a> work to run in the future, or <a href="time/fn.interval.html" title="fn tokio::time::interval">repeating an operation at an\r\ninterval</a>.</p>',
    '<p><a href="time/index.html" title="mod tokio::time"><code>tokio::time</code></a> 模块提供用于跟踪时间和\r\n调度任务的工具。包括为任务设置<a href="time/fn.timeout.html" title="fn tokio::time::timeout">超时</a>，\r\n将任务<a href="time/fn.sleep.html" title="fn tokio::time::sleep">休眠</a>以在未来运行，或者<a href="time/fn.interval.html" title="fn tokio::time::interval">按固定间隔重复运行</a>。</p>'.encode('utf-8')
)

# index.html p[15]: partial chinese, second half English
add(
    b'<p>Finally, Tokio provides a <em>runtime</em> for executing asynchronous tasks. Most\r\napplications can use the <a href="attr.main.html"><code>#[tokio::main]</code></a> macro to run their code on the\r\nTokio \xe8\xbf\x90\xe8\xa1\x8c\xe6\x97\xb6\xe3\x80\x82 However, this macro provides only basic configuration options. As\r\nan alternative, the <a href="runtime/index.html" title="mod tokio::runtime"><code>tokio::runtime</code></a> module provides more powerful APIs for configuring\r\nand managing runtimes. You should use that module if the <code>#[tokio::main]</code> macro doesn\xe2\x80\x99t\r\nprovide the functionality you need.</p>',
    '<p>此外，Tokio 提供了用于执行异步任务的 <em>运行时</em>。大多数\r\n应用程序可以使用 <a href="attr.main.html"><code>#[tokio::main]</code></a> 宏在 Tokio 运行时上运行代码。\r\n不过，该宏只提供基本的配置选项。作为\r\n替代方案，<a href="runtime/index.html" title="mod tokio::runtime"><code>tokio::runtime</code></a> 模块提供了更强大的 API 来配置和管理运行时。\r\n如果 <code>#[tokio::main]</code> 宏无法满足你的需求，应该使用该模块。</p>'.encode('utf-8')
)

# index.html p[16]: partial chinese, more untranslated
add(
    b'<p>\xe4\xbd\xbf\xe7\x94\xa8\xe8\xbf\x90\xe8\xa1\x8c\xe6\x97\xb6\xe9\x9c\x80\xe8\xa6\x81\xe2\x80\x9crt\xe2\x80\x9d \xe6\x88\x96\xe2\x80\x9crt-multi-thread\xe2\x80\x9d \xe7\x89\xb9\xe6\x80\xa7\xe6\xa0\x87\xe5\xbf\x97\xef\xbc\x8c\xe5\x88\x86\xe5\x88\xab\xe7\x94\xa8\xe4\xba\x8e\r\n\xe5\x90\xaf\xe7\x94\xa8 <a href="runtime/index.html#current-thread-scheduler">\xe5\x8d\x95\xe7\xba\xbf\xe7\xa8\x8b\xe8\xb0\x83\xe5\xba\xa6\xe5\x99\xa8</a> \xe5\x92\x8c <a href="runtime/index.html#multi-thread-scheduler">\xe5\xa4\x9a\xe7\xba\xbf\xe7\xa8\x8b\r\n\xe8\xb0\x83\xe5\xba\xa6\xe5\x99\xa8</a>\xe3\x80\x82\xe5\x8f\x82\xe9\x98\x85 <a href="runtime/index.html#runtime-scheduler"><code>runtime</code> \xe6\xa8\xa1\xe5\x9d\x97\r\ndocumentation</a> for details. In addition, the \xe2\x80\x9cmacros\xe2\x80\x9d feature\r\nflag enables the <code>#[tokio::main]</code> and <code>#[tokio::test]</code> attributes.</p>',
    '<p>使用运行时需要“rt”或“rt-multi-thread”特性标志，分别用于\r\n启用 <a href="runtime/index.html#current-thread-scheduler">单线程调度器</a> 和 <a href="runtime/index.html#multi-thread-scheduler">多线程\r\n调度器</a>。详见 <a href="runtime/index.html#runtime-scheduler"><code>runtime</code> 模块文档</a>。\r\n此外，“macros”特性标志会启用 <code>#[tokio::main]</code> 和 <code>#[tokio::test]</code> 属性。</p>'.encode('utf-8')
)

# index.html p[17]: partial chinese, end English "ng threads."
add(
    b'<p>Tokio \xe5\x8f\xaf\xe4\xbb\xa5\xe9\x80\x9a\xe8\xbf\x87\xe5\x9c\xa8\xe5\x90\x84\xe4\xb8\xaa\xe7\xba\xbf\xe7\xa8\x8b\xe4\xb8\x8a\xe9\x87\x8d\xe5\xa4\x8d\xe4\xba\xa4\xe6\x8d\xa2\xe5\xbd\x93\xe5\x89\x8d\xe8\xbf\x90\xe8\xa1\x8c\xe7\x9a\x84\xe4\xbb\xbb\xe5\x8a\xa1\xef\xbc\x8c\r\n\xe5\x9c\xa8\xe5\x87\xa0\xe4\xb8\xaa\xe7\xba\xbf\xe7\xa8\x8b\xe4\xb8\x8a\xe5\xb9\xb6\xe5\x8f\x91\xe8\xbf\x90\xe8\xa1\x8c\xe8\xae\xb8\xe5\xa4\x9a\xe4\xbb\xbb\xe5\x8a\xa1\xe3\x80\x82\xe4\xbd\x86\xe8\xbf\x99\xe7\xa7\x8d\xe4\xba\xa4\xe6\x8d\xa2\xe5\x8f\xaa\xe8\x83\xbd\xe5\x9c\xa8 <code>.await</code> \xe7\x82\xb9\xe5\x8f\x91\xe7\x94\x9f\xef\xbc\x8c\r\n\xe5\x9b\xa0\xe6\xad\xa4\xe9\x95\xbf\xe6\x97\xb6\xe9\x97\xb4\xe4\xb8\x8d\xe5\x88\xb0\xe8\xbe\xbe <code>.await</code> \xe7\x9a\x84\xe4\xbb\xa3\xe7\xa0\x81\xe4\xbc\x9a\xe9\x98\xbb\xe5\xa1\x9e\xe5\x85\xb6\xe4\xbb\x96\xe4\xbb\xbb\xe5\x8a\xa1\xe7\x9a\x84\xe8\xbf\x90\xe8\xa1\x8c\xe3\x80\x82\xe4\xb8\xba\xe4\xba\x86\r\n\xe7\xbc\x96\xe5\x86\x99\xe4\xba\xa4\xe6\x8d\xa2ng threads.</p>',
    '<p>Tokio 可以通过在各个线程上重复交换当前运行的任务，\r\n在几个线程上并发运行许多任务。但这种交换只能在 <code>.await</code> 点发生，\r\n因此长时间不到达 <code>.await</code> 的代码会阻塞其他任务的运行。为了\r\n应对这一点，Tokio 提供了两类线程。</p>'.encode('utf-8')
)

# index.html p[19]: partial chinese, end English
add(
    b'<p>\xe9\x98\xbb\xe5\xa1\x9e\xe7\xba\xbf\xe7\xa8\x8b\xe6\x98\xaf\xe6\x8c\x89\xe9\x9c\x80\xe6\xb1\x82\xe6\xb4\xbe\xe7\x94\x9f\xe7\x9a\x84\xef\xbc\x8c\xe5\x8f\xaf\xe7\x94\xa8\xe4\xba\x8e\xe8\xbf\x90\xe8\xa1\x8c\xe9\x98\xbb\xe5\xa1\x9e\xe4\xbb\xa3\xe7\xa0\x81\xef\xbc\x8c\xe5\x90\xa6\xe5\x88\x99\xe4\xbb\x96\xe4\xbb\xbb\xe5\x8a\xa1\xe4\xbc\x9a\xe5\x8f\x97\xe5\x88\xb0\xe9\x98\xbb\xe5\xa1\x9e\xe3\x80\x82\r\n\xe5\xae\x83\xe4\xbb\xac\xe5\x9c\xa8\xe4\xb8\x80\xe6\xae\xb5\xe6\x97\xb6\xe9\x97\xb4\xe5\x86\x85\xe6\x9c\xaa\xe8\xa2\xab\xe4\xbd\xbf\xe7\x94\xa8\xe6\x97\xb6\xe4\xbc\x9a\xe4\xbf\x9d\xe6\x8c\x81\xe6\xb4\xbb\xe8\xb7\x83\xef\xbc\x8c\xe8\xaf\xa5\xe6\x97\xb6\xe9\x97\xb4\xe5\x8f\xaf\xe9\x80\x9a\xe8\xbf\x87 <a href="runtime/struct.Builder.html#method.thread_keep_alive" title="method tokio::runtime::Builder::thread_keep_alive"><code>thread_keep_alive</code></a> \xe9\x85\x8d\xe7\xbd\xae\xe3\x80\x82\r\nSince it is not possible for Tokio to swap out blocking tasks, like it\r\ncan do with asynchronous code, the upper limit on the number of blocking\r\nthreads is very large. These limits can be configured on the <a href="runtime/struct.Builder.html" title="struct tokio::runtime::Builder"><code>Builder</code></a>.</p>',
    '<p>阻塞线程是按需求派生的，可用于运行阻塞代码，否则其他任务会受到阻塞。\r\n它们在一段时间内未被使用时会保持活跃，该时间可通过 <a href="runtime/struct.Builder.html#method.thread_keep_alive" title="method tokio::runtime::Builder::thread_keep_alive"><code>thread_keep_alive</code></a> 配置。\r\n由于 Tokio 无法像对异步代码那样换出阻塞任务，\r\n阻塞线程数量的上限非常大。这些限制可在 <a href="runtime/struct.Builder.html" title="struct tokio::runtime::Builder"><code>Builder</code></a> 上配置。</p>'.encode('utf-8')
)

# index.html p[21]: all English
add(
    b'<p>If your code is CPU-bound and you wish to limit the number of threads used\r\nto run it, you should use a separate thread pool dedicated to CPU bound tasks.\r\nFor example, you could consider using the <a href="https://docs.rs/rayon">rayon</a> library for CPU-bound\r\ntasks. It is also possible to create an extra Tokio runtime dedicated to\r\nCPU-bound tasks, but if you do this, you should be careful that the extra\r\nruntime runs <em>only</em> CPU-bound tasks, as IO-bound tasks on that runtime\r\nwill behave poorly.</p>',
    '<p>如果你的代码是 CPU 密集型的，并且希望限制用于运行它的线程数，\r\n那么应该使用一个专用于 CPU 密集型任务的独立线程池。\r\n例如，可以考虑使用 <a href="https://docs.rs/rayon">rayon</a> 库来处理 CPU 密集型任务。\r\n也可以创建一个专用于 CPU 密集型任务的额外 Tokio 运行时，\r\n但这样做时要小心，该额外运行时应<em>只</em>运行 CPU 密集型任务，\r\n否则该运行时上的 I/O 密集型任务表现会很差。</p>'.encode('utf-8')
)

# index.html p[24]: partial, end English
add(
    b'<p><a href="io/index.html" title="mod tokio::io"><code>tokio::io</code></a> \xe6\xa8\xa1\xe5\x9d\x97\xe6\x8f\x90\xe4\xbe\x9b Tokio \xe7\x9a\x84\xe5\xbc\x82\xe6\xad\xa5\xe6\xa0\xb8\xe5\xbf\x83 I/O \xe5\x8e\x9f\xe8\xaf\xad\xef\xbc\x8c\r\n\xe5\x8c\x85\xe6\x8b\xac <a href="io/trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> \xe3\x80\x81 <a href="io/trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a>, and <a href="io/trait.AsyncBufRead.html" title="trait tokio::io::AsyncBufRead"><code>AsyncBufRead</code></a> traits. In addition,\r\nwhen the \xe2\x80\x9cio-util\xe2\x80\x9d feature flag is enabled, it also provides combinators and\r\nfunctions for working with these traits, forming as an asynchronous\r\ncounterpart to <a href="https://doc.rust-lang.org/1.95.0/std/io/index.html" title="mod std::io"><code>std::io</code></a>.</p>',
    '<p><a href="io/index.html" title="mod tokio::io"><code>tokio::io</code></a> 模块提供 Tokio 的异步核心 I/O 原语，\r\n包括 <a href="io/trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a>、 <a href="io/trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> 和 <a href="io/trait.AsyncBufRead.html" title="trait tokio::io::AsyncBufRead"><code>AsyncBufRead</code></a> trait。此外，\r\n当启用“io-util”特性标志时，它还提供与这些 trait 配合使用的组合子和函数，\r\n作为 <a href="https://doc.rust-lang.org/1.95.0/std/io/index.html" title="mod std::io"><code>std::io</code></a> 的异步对应物。</p>'.encode('utf-8')
)

# index.html p[27]: all English
add(
    b'<p>Tokio uses a set of <a href="https://doc.rust-lang.org/cargo/reference/manifest.html#the-features-section">feature flags</a> to reduce the amount of compiled code. It\r\nis possible to just enable certain features over others. By default, Tokio\r\ndoes not enable any features but allows one to enable a subset for their use\r\ncase. Below is a list of the available feature flags. You may also notice\r\nabove each function, struct and trait there is listed one or more feature flags\r\nthat are required for that item to be used. If you are new to Tokio it is\r\nrecommended that you use the <code>full</code> feature flag which will enable all public APIs.\r\nBeware though that this will pull in many extra dependencies that you may not\r\nneed.</p>',
    '<p>Tokio 使用一组 <a href="https://doc.rust-lang.org/cargo/reference/manifest.html#the-features-section">特性标志</a> 来减少编译后的代码量。\r\n可以选择性地启用某些特性。默认情况下，Tokio\r\n不启用任何特性，但允许用户根据用例启用一个子集。\r\n以下是可用特性标志的列表。你可能还会注意到，\r\n在每个函数、结构和 trait 上方都列出了使用该项所需的\r\n一个或多个特性标志。如果你是 Tokio 的新手，\r\n建议使用 <code>full</code> 特性标志来启用所有公开的 API。\r\n不过请注意，这会引入许多你可能不需要的额外依赖。</p>'.encode('utf-8')
)

# index.html p[31]: partial, end English
add(
    b'<p>\xe8\xbf\x99\xe4\xb8\xaa\xe6\xa0\x87\xe5\xbf\x97\xe5\x90\xaf\xe7\x94\xa8 <strong>\xe4\xb8\x8d\xe7\xa8\xb3\xe5\xae\x9a</strong> \xe7\x89\xb9\xe6\x80\xa7\xe3\x80\x82\xe8\xbf\x99\xe4\xba\x9b\xe7\x89\xb9\xe6\x80\xa7\xe7\x9a\x84\xe5\x85\xac\xe5\xbc\x80 API\r\n\xe5\x8f\xaf\xe8\x83\xbd\xe4\xbc\x9a\xe5\x9c\xa8 1.x \xe5\x8f\x91\xe5\xb8\x83\xe4\xb8\xad\xe6\x96\xad\xe5\xbc\x83\xe3\x80\x82\xe4\xb8\xba\xe4\xba\x86\xe5\x90\xaf\xe7\x94\xa8\xe8\xbf\x99\xe4\xba\x9b\xe7\x89\xb9\xe6\x80\xa7\xef\xbc\x8c\xe7\xbc\x96\xe8\xaf\x91\xe6\x97\xb6\xe5\xbf\x85\xe9\xa1\xbb\xe5\xb0\x86 <code>--cfg tokio_unstable</code> \xe5\x8f\x82\xe6\x95\xb0\xe4\xbc\xa0\xe9\x80\x92\xe7\xbb\x99 <code>rustc</code>\xe3\x80\x82\r\n\xe8\xbf\x99\xe7\xa7\x8d\xe6\x98\xbe\xe5\xbc\x8f\xe7\x9a\x84\xe6\x8a\x91\xe5\x85\xa5\xe4\xbd\xbf\xe5\xbe\x97\xe8\xbf\x99\xe4\xba\x9b\xe7\x89\xb9\xe6\x80\xa7\xe6\x98\xaf\xe6\x98\x8e\xe7\xa1\xae\xe7\x9a\x84\xe9\x80\x89\xe6\x8b\xa9\xe6\x80\xa7\xe5\xbc\x80\xe5\x90\xaf\xef\xbc\x8c\r\nsince Cargo <a href="https://internals.rust-lang.org/t/feature-request-unstable-opt-in-non-transitive-crate-features/16193#why-not-a-crate-feature-2">does not yet directly support such opt-ins</a>.</p>',
    '<p>这个标志启用 <strong>不稳定</strong> 特性。这些特性的公开 API\r\n可能会在 1.x 发布中舍弃。为了启用这些特性，编译时必须将 <code>--cfg tokio_unstable</code> 参数传递给 <code>rustc</code>。\r\n这种显式的抑入使得这些特性是明确的选择性开启，\r\n因为 Cargo <a href="https://internals.rust-lang.org/t/feature-request-unstable-opt-in-non-transitive-crate-features/16193#why-not-a-crate-feature-2">尚未直接支持此类选择性开启</a>。</p>'.encode('utf-8')
)

# index.html p[33]: all English
add(
    b'<p>Alternatively, you can specify it with an environment variable:</p>',
    '<p>或者，你也可以通过环境变量来指定：</p>'.encode('utf-8')
)
# index.html p[34]: all English
add(
    b'<p>Tokio currently guarantees support for the following platforms:</p>',
    '<p>Tokio 目前保证支持以下平台：</p>'.encode('utf-8')
)

# ============== tokio/attr.main.html remaining p ==============
add(
    b'<p>Marks async function to be executed by the selected runtime. This macro\r\nhelps set up a <code>Runtime</code> without requiring the user to use\r\n<a href="../tokio/runtime/struct.Runtime.html">Runtime</a> or\r\n<a href="../tokio/runtime/struct.Builder.html">Builder</a> directly.</p>',
    '<p>将 async 函数标记为由所选运行时执行。该宏\r\n帮助设置 <code>Runtime</code>，无需用户直接使用\r\n<a href="../tokio/runtime/struct.Runtime.html">Runtime</a> 或\r\n<a href="../tokio/runtime/struct.Builder.html">Builder</a>。</p>'.encode('utf-8')
)
add(
    b'<p>Note: This macro can be used on any function and not just the <code>main</code>\r\nfunction. Using it on a non-main function makes the function behave as if it\r\nwas synchronous by starting a new runtime each time it is called. If the\r\nfunction is called often, it is preferable to create the runtime using the\r\nruntime builder so the runtime can be reused across calls.</p>',
    '<p>注意：该宏可以应用于任何函数，而不仅仅是 <code>main</code>\r\n函数。在非 main 函数上使用它时，每次调用都会启动一个新运行时，使函数\r\n表现为同步行为。如果该函数被频繁调用，\r\n建议使用运行时构建器创建运行时，以便在多次调用之间复用。</p>'.encode('utf-8')
)
add(
    b'<p>The macro can be configured with a <code>flavor</code> parameter to select\r\ndifferent runtime configurations.</p>',
    '<p>该宏可以使用 <code>flavor</code> 参数进行配置，以选择\r\n不同的运行时配置。</p>'.encode('utf-8')
)
add(
    b'<p>To use the multi-threaded runtime, the macro can be configured using</p>',
    '<p>要使用多线程运行时，可通过如下方式配置该宏</p>'.encode('utf-8')
)
add(
    b'<p>The <code>worker_threads</code> option configures the number of worker threads, and\r\ndefaults to the number of cpus on the system. This is the default flavor.</p>',
    '<p><code>worker_threads</code> 选项用于配置工作线程数，\r\n默认为系统上的 CPU 数量。这是默认的 flavor。</p>'.encode('utf-8')
)
add(
    b'<p>Note: The multi-threaded runtime requires the <code>rt-multi-thread</code> feature\r\nflag.</p>',
    '<p>注意：多线程运行时需要 <code>rt-multi-thread</code> 特性\r\n标志。</p>'.encode('utf-8')
)
add(
    b'<p>To use the single-threaded runtime known as the <code>current_thread</code> runtime,\r\nthe macro can be configured using</p>',
    '<p>要使用称为 <code>current_thread</code> 运行时的单线程运行时，\r\n可通过如下方式配置该宏</p>'.encode('utf-8')
)
add(
    b'<p>To use the <a href="../tokio/runtime/struct.LocalRuntime.html">local runtime</a>, the macro can be configured using</p>',
    '<p>要使用 <a href="../tokio/runtime/struct.LocalRuntime.html">本地运行时</a>，可通过如下方式配置该宏</p>'.encode('utf-8')
)
add(
    b'<p>Arguments are allowed for any functions, aside from <code>main</code> which is special.</p>',
    '<p>除 <code>main</code> 是特殊的外，任何函数都允许带参数。</p>'.encode('utf-8')
)
add(
    b'<p>Equivalent code not using <code>#[tokio::main]</code></p>',
    '<p>不使用 <code>#[tokio::main]</code> 的等价代码</p>'.encode('utf-8')
)
add(
    b'<p>The <a href="../tokio/runtime/struct.LocalRuntime.html">local runtime</a> is similar to the current-thread runtime but\r\nsupports <a href="../tokio/task/fn.spawn_local.html"><code>task::spawn_local</code></a>.</p>',
    '<p><a href="../tokio/runtime/struct.LocalRuntime.html">本地运行时</a> 与当前线程运行时类似，但\r\n支持 <a href="../tokio/task/fn.spawn_local.html"><code>task::spawn_local</code></a>。</p>'.encode('utf-8')
)
add(
    b'<p>Note that <code>start_paused</code> requires the <code>test-util</code> feature to be enabled.</p>',
    '<p>注意，<code>start_paused</code> 需要启用 <code>test-util</code> 特性。</p>'.encode('utf-8')
)
add(
    b'<p>Available options are <code>shutdown_runtime</code> and <code>ignore</code>. For more details, see\r\n<a href="../tokio/runtime/struct.Builder.html#method.unhandled_panic"><code>Builder::unhandled_panic</code></a>.</p>',
    '<p>可用选项有 <code>shutdown_runtime</code> 和 <code>ignore</code>。更多详情，请参阅\r\n<a href="../tokio/runtime/struct.Builder.html#method.unhandled_panic"><code>Builder::unhandled_panic</code></a>。</p>'.encode('utf-8')
)
add(
    b'<p>This option is only compatible with the <code>current_thread</code> runtime.</p>',
    '<p>该选项仅与 <code>current_thread</code> 运行时兼容。</p>'.encode('utf-8')
)
add(
    b'<p><strong>Note</strong>: This option depends on Tokio\xe2\x80\x99s <a href="../tokio/index.html#unstable-features">unstable API</a>. See <a href="../tokio/index.html#unstable-features">the\r\ndocumentation on unstable features</a> for details on how to enable\r\nTokio\xe2\x80\x99s unstable features.</p>',
    '<p><strong>注意</strong>：该选项依赖于 Tokio 的<a href="../tokio/index.html#unstable-features">不稳定 API</a>。详见<a href="../tokio/index.html#unstable-features">不稳定特性的相关文档</a>，\r\n了解如何启用 Tokio 的不稳定特性。</p>'.encode('utf-8')
)

# ============== tokio/attr.test.html remaining p ==============
add(
    b'<p>Marks async function to be executed by runtime, suitable to test environment.\r\nThis macro helps set up a <code>Runtime</code> without requiring the user to use\r\n<a href="../tokio/runtime/struct.Runtime.html">Runtime</a> or\r\n<a href="../tokio/runtime/struct.Builder.html">Builder</a> directly.</p>',
    '<p>将 async 函数标记为由运行时执行，适合测试环境使用。\r\n该宏帮助设置 <code>Runtime</code>，无需用户直接使用\r\n<a href="../tokio/runtime/struct.Runtime.html">Runtime</a> 或\r\n<a href="../tokio/runtime/struct.Builder.html">Builder</a>。</p>'.encode('utf-8')
)
add(
    b'<p>To use the multi-threaded runtime, the macro can be configured using</p>',
    '<p>要使用多线程运行时，可通过如下方式配置该宏</p>'.encode('utf-8')
)
add(
    b'<p>The <code>worker_threads</code> option configures the number of worker threads, and\r\ndefaults to the number of cpus on the system.</p>',
    '<p><code>worker_threads</code> 选项用于配置工作线程数，\r\n默认为系统上的 CPU 数量。</p>'.encode('utf-8')
)
add(
    b'<p>Note: The multi-threaded runtime requires the <code>rt-multi-thread</code> feature\r\nflag.</p>',
    '<p>注意：多线程运行时需要 <code>rt-multi-thread</code> 特性\r\n标志。</p>'.encode('utf-8')
)
add(
    b'<p>Equivalent code not using <code>#[tokio::test]</code></p>',
    '<p>不使用 <code>#[tokio::test]</code> 的等价代码</p>'.encode('utf-8')
)
add(
    b'<p>Note that <code>start_paused</code> requires the <code>test-util</code> feature to be enabled.</p>',
    '<p>注意，<code>start_paused</code> 需要启用 <code>test-util</code> 特性。</p>'.encode('utf-8')
)
add(
    b'<p>Available options are <code>shutdown_runtime</code> and <code>ignore</code>. For more details, see\r\n<a href="../tokio/runtime/struct.Builder.html#method.unhandled_panic"><code>Builder::unhandled_panic</code></a>.</p>',
    '<p>可用选项有 <code>shutdown_runtime</code> 和 <code>ignore</code>。更多详情，请参阅\r\n<a href="../tokio/runtime/struct.Builder.html#method.unhandled_panic"><code>Builder::unhandled_panic</code></a>。</p>'.encode('utf-8')
)
add(
    b'<p>This option is only compatible with the <code>current_thread</code> runtime.</p>',
    '<p>该选项仅与 <code>current_thread</code> 运行时兼容。</p>'.encode('utf-8')
)
add(
    b'<p><strong>Note</strong>: This option depends on Tokio\xe2\x80\x99s <a href="../tokio/index.html#unstable-features">unstable API</a>. See <a href="../tokio/index.html#unstable-features">the\r\ndocumentation on unstable features</a> for details on how to enable\r\nTokio\xe2\x80\x99s unstable features.</p>',
    '<p><strong>注意</strong>：该选项依赖于 Tokio 的<a href="../tokio/index.html#unstable-features">不稳定 API</a>。详见<a href="../tokio/index.html#unstable-features">不稳定特性的相关文档</a>，\r\n了解如何启用 Tokio 的不稳定特性。</p>'.encode('utf-8')
)

# ============== tokio/macro.join.html remaining p ==============
add(
    b'<p>Waits on multiple concurrent branches, returning when <strong>all</strong> branches\r\ncomplete.</p>',
    '<p>等待多个并发分支，<strong>所有</strong>分支完成后返回。</p>'.encode('utf-8')
)
add(
    b'<p>The <code>join!</code> macro must be used inside of async functions, closures, and\r\nblocks.</p>',
    '<p><code>join!</code> 宏必须在 async 函数、闭包和\r\n块内部使用。</p>'.encode('utf-8')
)
add(
    b'<p>The <code>join!</code> macro takes a list of async expressions and evaluates them\r\nconcurrently on the same task. Each async expression evaluates to a future\r\nand the futures from each expression are multiplexed on the current task.</p>',
    '<p><code>join!</code> 宏接受一组 async 表达式，并在同一个任务上\r\n并发地对它们求值。每个 async 表达式都会被求值为一个 future，\r\n来自每个表达式的 future 会在当前任务上进行多路复用。</p>'.encode('utf-8')
)
add(
    b'<p>When working with async expressions returning <code>Result</code>, <code>join!</code> will wait\r\nfor <strong>all</strong> branches complete regardless if any complete with <code>Err</code>. Use\r\n<a href="macro.try_join.html" title="macro tokio::try_join"><code>try_join!</code></a> to return early when <code>Err</code> is encountered.</p>',
    '<p>对于返回 <code>Result</code> 的 async 表达式，<code>join!</code> 会等待\r\n<strong>所有</strong>分支完成，无论其中是否有以 <code>Err</code> 完成的。遇到 <code>Err</code> 时若要提早返回，\r\n请使用 <a href="macro.try_join.html" title="macro tokio::try_join"><code>try_join!</code></a>。</p>'.encode('utf-8')
)
add(
    b'<p>The supplied futures are stored inline and do not require allocating a\r\n<code>Vec</code>.</p>',
    '<p>所提供的 future 是内联存储的，无需分配\r\n<code>Vec</code>。</p>'.encode('utf-8')
)
add(
    b'<p>By running all async expressions on the current task, the expressions are\r\nable to run <strong>concurrently</strong> but not in <strong>parallel</strong>. This means all\r\nexpressions are run on the same thread and if one branch blocks the thread,\r\nall other expressions will be unable to continue. If parallelism is\r\nrequired, spawn each async expression using <a href="task/fn.spawn.html" title="fn tokio::task::spawn"><code>tokio::spawn</code></a> and pass the\r\njoin handle to <code>join!</code>.</p>',
    '<p>通过在当前任务上运行所有 async 表达式，这些表达式\r\n能够<strong>并发</strong>运行，但不能<strong>并行</strong>运行。这意味着所有\r\n表达式都在同一线程上运行，如果某个分支阻塞了该线程，\r\n所有其他表达式将无法继续。如果需要并行执行，\r\n可以使用 <a href="task/fn.spawn.html" title="fn tokio::task::spawn"><code>tokio::spawn</code></a> 生成每个 async 表达式，并将\r\njoin handle 传给 <code>join!</code>。</p>'.encode('utf-8')
)
add(
    b'<p>By default, <code>join!</code>\xe2\x80\x99s generated future rotates which contained\r\nfuture is polled first whenever it is woken.</p>',
    '<p>默认情况下，<code>join!</code> 生成的 future 在每次被唤醒时，\r\n会轮换哪一个被包含的 future 最先被 poll。</p>'.encode('utf-8')
)
add(
    b'<p>This behavior can be overridden by adding <code>biased;</code> to the beginning of the\r\nmacro usage. See the examples for details. This will cause <code>join</code> to poll\r\nthe futures in the order they appear from top to bottom.</p>',
    '<p>可以通过在宏使用的开头添加 <code>biased;</code> 来覆盖此行为。\r\n详情请参阅示例。这会使 <code>join</code> 按照 future\r\n从上到下出现的顺序对其进行 poll。</p>'.encode('utf-8')
)
add(
    b'<p>But there is an important caveat to this mode. It becomes your responsibility\r\nto ensure that the polling order of your futures is fair. If for example you\r\nare joining a stream and a shutdown future, and the stream has a\r\nhuge volume of messages that takes a long time to finish processing per poll, you should\r\nplace the shutdown future earlier in the <code>join!</code> list to ensure that it is\r\nalways polled, and will not be delayed due to the stream future taking a long time to return\r\n<code>Poll::Pending</code>.</p>',
    '<p>但在这种模式下有一个重要的注意事项。确保 future 的 poll 顺序是公平的就成了你的\r\n责任。例如，如果你要 join 一个流和一个关闭 future，且该流\r\n每次 poll 时都有大量消息需要长时间处理，那么你应该\r\n把关闭 future 放在 <code>join!</code> 列表的更前面，以确保它\r\n始终被 poll，而不会因流 future 长时间返回 <code>Poll::Pending</code> 而被延迟。</p>'.encode('utf-8')
)
add(
    b'<p>Basic join with two branches</p>',
    '<p>两分支的基本 join</p>'.encode('utf-8')
)
add(
    b'<p>Using the <code>biased;</code> mode to control polling order.</p>',
    '<p>使用 <code>biased;</code> 模式来控制 poll 顺序。</p>'.encode('utf-8')
)

# ============== tokio/macro.select.html remaining p ==============
add(
    b'<p>Waits on multiple concurrent branches, returning when the <strong>first</strong> branch\r\ncompletes, cancelling the remaining branches.</p>',
    '<p>等待多个并发分支，<strong>首个</strong>分支完成后返回，\r\n并取消其余分支。</p>'.encode('utf-8')
)
add(
    b'<p>The <code>select!</code> macro must be used inside of async functions, closures, and\r\nblocks.</p>',
    '<p><code>select!</code> 宏必须在 async 函数、闭包和\r\n块内部使用。</p>'.encode('utf-8')
)
add(
    b'<p>The <code>select!</code> macro accepts one or more branches with the following pattern:</p>',
    '<p><code>select!</code> 宏接受一个或多个具有以下模式的分支：</p>'.encode('utf-8')
)
add(
    b'<p>Additionally, the <code>select!</code> macro may include a single, optional <code>else</code>\r\nbranch, which evaluates if none of the other branches match their patterns:</p>',
    '<p>此外，<code>select!</code> 宏可以包含一个可选的 <code>else</code>\r\n分支，当没有其他分支匹配其模式时该分支会被求值：</p>'.encode('utf-8')
)
add(
    b'<p>The macro aggregates all <code>&lt;async expression&gt;</code> expressions and runs them\r\nconcurrently on the <strong>current</strong> task. Once the <strong>first</strong> expression\r\ncompletes with a value that matches its <code>&lt;pattern&gt;</code>, the <code>select!</code> macro\r\nreturns the result of evaluating the completed branch\xe2\x80\x99s <code>&lt;handler&gt;</code>\r\nexpression.</p>',
    '<p>该宏会汇总所有 <code>&lt;async expression&gt;</code> 表达式，并在<strong>当前</strong>\r\n任务上并发地运行它们。一旦<strong>首个</strong>表达式\r\n以匹配其 <code>&lt;pattern&gt;</code> 的值完成，<code>select!</code> 宏\r\n就会返回对已完成分支的 <code>&lt;handler&gt;</code> 表达式求值的结果。</p>'.encode('utf-8')
)
add(
    b'<p>Additionally, each branch may include an optional <code>if</code> precondition. If the\r\nprecondition returns <code>false</code>, then the branch is disabled. The provided\r\n<code>&lt;async expression&gt;</code> is still evaluated but the resulting future is never\r\npolled. This capability is useful when using <code>select!</code> within a loop.</p>',
    '<p>此外，每个分支可以包含一个可选的 <code>if</code> 前置条件。如果\r\n前置条件返回 <code>false</code>，则该分支会被禁用。提供的\r\n<code>&lt;async expression&gt;</code> 仍会被求值，但生成的 future 永远不会被\r\npoll。在循环中使用 <code>select!</code> 时，这一能力非常有用。</p>'.encode('utf-8')
)
add(
    b'<p>The complete lifecycle of a <code>select!</code> expression is as follows:</p>',
    '<p><code>select!</code> 表达式的完整生命周期如下：</p>'.encode('utf-8')
)
add(
    b'<p>By running all async expressions on the current task, the expressions are\r\nable to run <strong>concurrently</strong> but not in <strong>parallel</strong>. This means all\r\nexpressions are run on the same thread and if one branch blocks the thread,\r\nall other expressions will be unable to continue. If parallelism is\r\nrequired, spawn each async expression using <a href="task/fn.spawn.html" title="fn tokio::task::spawn"><code>tokio::spawn</code></a> and pass the\r\njoin handle to <code>select!</code>.</p>',
    '<p>通过在当前任务上运行所有 async 表达式，这些表达式\r\n能够<strong>并发</strong>运行，但不能<strong>并行</strong>运行。这意味着所有\r\n表达式都在同一线程上运行，如果某个分支阻塞了该线程，\r\n所有其他表达式将无法继续。如果需要并行执行，\r\n可以使用 <a href="task/fn.spawn.html" title="fn tokio::task::spawn"><code>tokio::spawn</code></a> 生成每个 async 表达式，并将\r\njoin handle 传给 <code>select!</code>。</p>'.encode('utf-8')
)
add(
    b'<p>By default, <code>select!</code> randomly picks a branch to check first. This provides\r\nsome level of fairness when calling <code>select!</code> in a loop with branches that\r\nare always ready.</p>',
    '<p>默认情况下，<code>select!</code> 会随机选择一个分支优先检查。这\r\n在循环中调用 <code>select!</code> 且分支总是 ready 的情况下提供了一定程度的公平性。</p>'.encode('utf-8')
)
add(
    b'<p>This behavior can be overridden by adding <code>biased;</code> to the beginning of the\r\nmacro usage. See the examples for details. This will cause <code>select</code> to poll\r\nthe futures in the order they appear from top to bottom. There are a few\r\nreasons you may want this:</p>',
    '<p>可以通过在宏使用的开头添加 <code>biased;</code> 来覆盖此行为。\r\n详情请参阅示例。这会使 <code>select</code> 按照 future\r\n从上到下出现的顺序对其进行 poll。出于以下几个原因，你可能\r\n希望这样做：</p>'.encode('utf-8')
)
add(
    b'<p>But there is an important caveat to this mode. It becomes your responsibility\r\nto ensure that the polling order of your futures is fair. If for example you\r\nare selecting between a stream and a shutdown future, and the stream has a\r\nhuge volume of messages and zero or nearly zero time between them, you should\r\nplace the shutdown future earlier in the <code>select!</code> list to ensure that it is\r\nalways polled, and will not be ignored due to the stream being constantly\r\nready.</p>',
    '<p>但在这种模式下有一个重要的注意事项。确保 future 的 poll 顺序是公平的就成了你的\r\n责任。例如，如果你要在流和关闭 future 之间进行 select，且该流\r\n有大量消息且消息之间几乎没有时间间隔，\r\n那么应该把关闭 future 放在 <code>select!</code> 列表的更前面，\r\n以确保它始终被 poll，而不会因流一直\r\nready 而被忽略。</p>'.encode('utf-8')
)
add(
    b'<p>The <code>select!</code> macro panics if all branches are disabled <strong>and</strong> there is no\r\nprovided <code>else</code> branch. A branch is disabled when the provided <code>if</code>\r\nprecondition returns <code>false</code> <strong>or</strong> when the pattern does not match the\r\nresult of <code>&lt;async expression&gt;</code>.</p>',
    '<p>如果所有分支都被禁用<strong>且</strong>没有提供\r\n<code>else</code> 分支，<code>select!</code> 宏会 panic。分支在所提供的 <code>if</code>\r\n前置条件返回 <code>false</code> 时被禁用，\r\n<strong>或者</strong>当模式不匹配 <code>&lt;async expression&gt;</code> 的结果时也会被禁用。</p>'.encode('utf-8')
)
add(
    b'<p>When using <code>select!</code> in a loop to receive messages from multiple sources,\r\nyou should make sure that the receive call is cancellation safe to avoid\r\nlosing messages. This section goes through various common methods and\r\ndescribes whether they are cancel safe.  The lists in this section are not\r\nexhaustive.</p>',
    '<p>在循环中使用 <code>select!</code> 从多个来源接收消息时，\r\n应确保接收调用是 cancellation safe 的，以避免\r\n丢失消息。本节介绍各种常见方法，\r\n并说明它们是否可安全取消。本节中的列表并不\r\n详尽。</p>'.encode('utf-8')
)
add(
    b'<p>The following methods are not cancellation safe because they use a queue for\r\nfairness and cancellation makes you lose your place in the queue:</p>',
    '<p>以下方法不可安全取消，因为它们使用队列来实现\r\n公平性，取消会丢失在队列中的位置：</p>'.encode('utf-8')
)
add(
    b'<p>To determine whether your own methods are cancellation safe, look for the\r\nlocation of uses of <code>.await</code>. This is because when an asynchronous method is\r\ncancelled, that always happens at an <code>.await</code>. If your function behaves\r\ncorrectly even if it is restarted while waiting at an <code>.await</code>, then it is\r\ncancellation safe.</p>',
    '<p>要判断你自己的方法是否可安全取消，请查找\r\n<code>.await</code> 的使用位置。这是因为当异步方法\r\n被取消时，总是发生在某个 <code>.await</code> 处。如果你的函数\r\n即便在 <code>.await</code> 处等待时重启也能正确\r\n执行，那么它就是可安全取消的。</p>'.encode('utf-8')
)
add(
    b'<p>Cancellation safety can be defined in the following way: If you have a\r\nfuture that has not yet completed, then it must be a no-op to drop that\r\nfuture and recreate it. This definition is motivated by the situation where\na <code>select!</code> is used in a loop. Without this guarantee, you would lose your\r\nprogress when another branch completes and you restart the <code>select!</code> by\r\ngoing around the loop.</p>',
    '<p>可以按以下方式定义取消安全性：如果你有一个\r\n尚未完成的 future，那么丢弃该\r\nfuture 并重新创建它必须是一个无操作。这个定义源于\r\n在循环中使用 <code>select!</code> 的场景。如果没有\r\n这个保证，当另一个分支完成且你绕回循环重新启动 <code>select!</code> 时，\r\n就会丢失进度。</p>'.encode('utf-8')
)
add(
    b'<p>Be aware that cancelling something that is not cancellation safe is not\r\nnecessarily wrong. For example, if you are cancelling a task because the\r\napplication is shutting down, then you probably don\xe2\x80\x99t care that partially\r\nread data is lost.</p>',
    '<p>请注意，取消一个不可安全取消的操作并不\r\n一定是错误的。例如，如果因为\r\n应用程序正在关闭而取消某个任务，那么\r\n可能并不在意部分读取的数据丢失。</p>'.encode('utf-8')
)
add(
    b'<p>Basic select with two branches.</p>',
    '<p>两分支的基本 select。</p>'.encode('utf-8')
)
add(
    b'<p>Basic stream selecting.</p>',
    '<p>基本的流选择。</p>'.encode('utf-8')
)
add(
    b'<p>Collect the contents of two streams. In this example, we rely on pattern\r\nmatching and the fact that <code>stream::iter</code> is \xe2\x80\x9cfused\xe2\x80\x9d, i.e. once the stream\r\nis complete, all calls to <code>next()</code> return <code>None</code>.</p>',
    '<p>收集两个流的内容。在本例中，我们依赖于模式\r\n匹配以及 <code>stream::iter</code> 是“fused”的事实，即流\r\n完成后，对 <code>next()</code> 的所有调用都会返回 <code>None</code>。</p>'.encode('utf-8')
)
add(
    b'<p>Using the same future in multiple <code>select!</code> expressions can be done by passing\r\na reference to the future. Doing so requires the future to be <a href="https://doc.rust-lang.org/1.95.0/core/marker/trait.Unpin.html" title="trait core::marker::Unpin"><code>Unpin</code></a>. A\r\nfuture can be made <a href="https://doc.rust-lang.org/1.95.0/core/marker/trait.Unpin.html" title="trait core::marker::Unpin"><code>Unpin</code></a> by either using <a href="https://doc.rust-lang.org/1.95.0/alloc/boxed/struct.Box.html#method.pin" title="associated function alloc::boxed::Box::pin"><code>Box::pin</code></a> or stack pinning.</p>',
    '<p>在多个 <code>select!</code> 表达式中使用同一个 future，可以通过\r\n传递该 future 的引用来实现。这要求 future 是 <a href="https://doc.rust-lang.org/1.95.0/core/marker/trait.Unpin.html" title="trait core::marker::Unpin"><code>Unpin</code></a> 的。\r\n通过 <a href="https://doc.rust-lang.org/1.95.0/alloc/boxed/struct.Box.html#method.pin" title="associated function alloc::boxed::Box::pin"><code>Box::pin</code></a> 或栈固定，可以使 future 成为 <a href="https://doc.rust-lang.org/1.95.0/core/marker/trait.Unpin.html" title="trait core::marker::Unpin"><code>Unpin</code></a>。</p>'.encode('utf-8')
)
add(
    b'<p>Joining two values using <code>select!</code>.</p>',
    '<p>使用 <code>select!</code> 合并两个值。</p>'.encode('utf-8')
)
add(
    b'<p>Using the <code>biased;</code> mode to control polling order.</p>',
    '<p>使用 <code>biased;</code> 模式来控制 poll 顺序。</p>'.encode('utf-8')
)
add(
    b'<p>Given that <code>if</code> preconditions are used to disable <code>select!</code> branches, some\r\ncaution must be used to avoid missing values.</p>',
    '<p>由于使用 <code>if</code> 前置条件来禁用 <code>select!</code> 分支，\r\n因此必须谨慎以避免遗漏值。</p>'.encode('utf-8')
)
add(
    b'<p>For example, here is <strong>incorrect</strong> usage of <code>sleep</code> with <code>if</code>. The objective\r\nis to repeatedly run an asynchronous task for up to 50 milliseconds.\r\nHowever, there is a potential for the <code>sleep</code> completion to be missed.</p>',
    '<p>例如，下面是对 <code>sleep</code> 与 <code>if</code> 的<strong>不正确</strong>用法。目标是\r\n重复运行一个异步任务，持续时间不超过 50 毫秒。\r\n但有可能错过 <code>sleep</code> 完成的事件。</p>'.encode('utf-8')
)
add(
    b'<p>In the above example, <code>sleep.is_elapsed()</code> may return <code>true</code> even if\r\n<code>sleep.poll()</code> never returned <code>Ready</code>. This opens up a potential race\r\ncondition where <code>sleep</code> expires between the <code>while !sleep.is_elapsed()</code>\r\ncheck and the call to <code>select!</code> resulting in the <code>some_async_work()</code> call to\r\nrun uninterrupted despite the sleep having elapsed.</p>',
    '<p>在上面的示例中，即便 <code>sleep.poll()</code> 始终没有返回 <code>Ready</code>，<code>sleep.is_elapsed()</code> 仍可能返回 <code>true</code>。\r\n这会引发潜在的竞态条件：当 <code>sleep</code> 在 <code>while !sleep.is_elapsed()</code>\r\n检查和 <code>select!</code> 调用之间到期时，<code>some_async_work()</code>\r\n会被不间断地运行，即便 sleep 已经过去。</p>'.encode('utf-8')
)
add(
    b'<p>The <code>select!</code> macro is a powerful tool for managing multiple asynchronous\r\nbranches, enabling tasks to run concurrently within the same thread. However,\r\nits use can introduce challenges, particularly around cancellation safety, which\r\ncan lead to subtle and hard-to-debug errors. For many use cases, ecosystem\r\nalternatives may be preferable as they mitigate these concerns by offering\r\nclearer syntax, more predictable control flow, and reducing the need to manually\r\nhandle issues like fuse semantics or cancellation safety.</p>',
    '<p><code>select!</code> 宏是管理多个异步\r\n分支的强大工具，使任务能够在同一线程内并发运行。然而，\r\n它的使用会引入一些挑战，尤其是在取消安全方面，\r\n这可能导致难以察觉且难以调试的错误。在许多用例中，\r\n生态中的替代方案可能更可取，因为它们通过提供\r\n更清晰的语法、更可预测的控制流，以及减少对手动\r\n处理 fuse 语义或取消安全等问题的需要，缓解了这些问题。</p>'.encode('utf-8')
)
add(
    b'<p>For cases where <code>loop { select! { ... } }</code> is used to poll multiple tasks,\r\nstream merging offers a concise alternative, inherently handle cancellation-safe\r\nprocessing, removing the risk of data loss. Libraries such as <a href="https://docs.rs/tokio-stream/latest/tokio_stream/"><code>tokio_stream</code></a>,\r\n<a href="https://docs.rs/futures/latest/futures/stream/"><code>futures::stream</code></a> and <a href="https://docs.rs/futures-concurrency/latest/futures_concurrency/"><code>futures_concurrency</code></a> provide tools for merging\r\nstreams and handling their outputs sequentially.</p>',
    '<p>对于使用 <code>loop { select! { ... } }</code> 来 poll 多个任务的\r\n情况，流合并提供了一种简洁的替代方案，天然支持安全的\r\n取消处理，消除了数据丢失的风险。<a href="https://docs.rs/tokio-stream/latest/tokio_stream/"><code>tokio_stream</code></a>、\r\n<a href="https://docs.rs/futures/latest/futures/stream/"><code>futures::stream</code></a> 和 <a href="https://docs.rs/futures-concurrency/latest/futures_concurrency/"><code>futures_concurrency</code></a> 等库提供了合并\r\n流并按顺序处理其输出的工具。</p>'.encode('utf-8')
)
add(
    b'<p>By using merge, you can unify multiple asynchronous tasks into a single stream,\r\neliminating the need to manage tasks manually and reducing the risk of\r\nunintended behavior like data loss.</p>',
    '<p>通过使用 merge，可以将多个异步任务统一为一个流，\r\n无需手动管理任务，并降低数据丢失等\r\n意外行为的风险。</p>'.encode('utf-8')
)
add(
    b'<p>If you need to wait for the first completion among several asynchronous tasks,\r\necosystem utilities such as\r\n<a href="https://docs.rs/futures/latest/futures/"><code>futures</code></a>,\r\n<a href="https://docs.rs/futures-lite/latest/futures_lite/"><code>futures-lite</code></a> or\r\n<a href="https://docs.rs/futures-concurrency/latest/futures_concurrency/"><code>futures-concurrency</code></a>\r\nprovide streamlined syntax for racing futures:</p>',
    '<p>如果需要在多个异步任务中等待\r\n最先完成的一个，\r\n<a href="https://docs.rs/futures/latest/futures/"><code>futures</code></a>、\r\n<a href="https://docs.rs/futures-lite/latest/futures_lite/"><code>futures-lite</code></a> 或\r\n<a href="https://docs.rs/futures-concurrency/latest/futures_concurrency/"><code>futures-concurrency</code></a>\r\n等生态工具提供了\r\n用于 Future 竞速的简洁语法：</p>'.encode('utf-8')
)

# ============== tokio/macro.try_join.html remaining p ==============
add(
    b'<p>Waits on multiple concurrent branches, returning when <strong>all</strong> branches\r\ncomplete with <code>Ok(_)</code> or on the first <code>Err(_)</code>.</p>',
    '<p>等待多个并发分支，<strong>所有</strong>分支以 <code>Ok(_)</code> 完成\r\n或首个 <code>Err(_)</code> 出现时返回。</p>'.encode('utf-8')
)
add(
    b'<p>The <code>try_join!</code> macro must be used inside of async functions, closures, and\r\nblocks.</p>',
    '<p><code>try_join!</code> 宏必须在 async 函数、闭包和\r\n块内部使用。</p>'.encode('utf-8')
)
add(
    b'<p>Similar to <a href="macro.join.html" title="macro tokio::join"><code>join!</code></a>, the <code>try_join!</code> macro takes a list of async\r\nexpressions and evaluates them concurrently on the same task. Each async\r\nexpression evaluates to a future and the futures from each expression are\r\nmultiplexed on the current task. The <code>try_join!</code> macro returns when <strong>all</strong>\r\nbranches return with <code>Ok</code> or when the <strong>first</strong> branch returns with <code>Err</code>.</p>',
    '<p>类似于 <a href="macro.join.html" title="macro tokio::join"><code>join!</code></a>，<code>try_join!</code> 宏接受一组 async\r\n表达式，并在同一任务上并发地对它们求值。每个 async\r\n表达式都会被求值为一个 future，来自每个表达式的 future 会在当前任务上进行多路复用。<code>try_join!</code> 宏在<strong>所有</strong>\r\n分支返回 <code>Ok</code> 或<strong>首个</strong>分支返回 <code>Err</code> 时返回。</p>'.encode('utf-8')
)
add(
    b'<p>The supplied futures are stored inline and do not require allocating a\r\n<code>Vec</code>.</p>',
    '<p>所提供的 future 是内联存储的，无需分配\r\n<code>Vec</code>。</p>'.encode('utf-8')
)
add(
    b'<p>By running all async expressions on the current task, the expressions are\r\nable to run <strong>concurrently</strong> but not in <strong>parallel</strong>. This means all\r\nexpressions are run on the same thread and if one branch blocks the thread,\r\nall other expressions will be unable to continue. If parallelism is\r\nrequired, spawn each async expression using <a href="task/fn.spawn.html" title="fn tokio::task::spawn"><code>tokio::spawn</code></a> and pass the\r\njoin handle to <code>try_join!</code>.</p>',
    '<p>通过在当前任务上运行所有 async 表达式，这些表达式\r\n能够<strong>并发</strong>运行，但不能<strong>并行</strong>运行。这意味着所有\r\n表达式都在同一线程上运行，如果某个分支阻塞了该线程，\r\n所有其他表达式将无法继续。如果需要并行执行，\r\n可以使用 <a href="task/fn.spawn.html" title="fn tokio::task::spawn"><code>tokio::spawn</code></a> 生成每个 async 表达式，并将\r\njoin handle 传给 <code>try_join!</code>。</p>'.encode('utf-8')
)
add(
    b'<p>By default, <code>try_join!</code>\xe2\x80\x99s generated future rotates which\r\ncontained future is polled first whenever it is woken.</p>',
    '<p>默认情况下，<code>try_join!</code> 生成的 future 在每次被唤醒时，\r\n会轮换哪一个被包含的 future 最先被 poll。</p>'.encode('utf-8')
)
add(
    b'<p>This behavior can be overridden by adding <code>biased;</code> to the beginning of the\r\nmacro usage. See the examples for details. This will cause <code>try_join</code> to poll\r\nthe futures in the order they appear from top to bottom.</p>',
    '<p>可以通过在宏使用的开头添加 <code>biased;</code> 来覆盖此行为。\r\n详情请参阅示例。这会使 <code>try_join</code> 按照 future\r\n从上到下出现的顺序对其进行 poll。</p>'.encode('utf-8')
)
add(
    b'<p>But there is an important caveat to this mode. It becomes your responsibility\r\nto ensure that the polling order of your futures is fair. If for example you\r\nare joining a stream and a shutdown future, and the stream has a\r\nhuge volume of messages that takes a long time to finish processing per poll, you should\r\nplace the shutdown future earlier in the <code>try_join!</code> list to ensure that it is\r\nalways polled, and will not be delayed due to the stream future taking a long time to return\r\n<code>Poll::Pending</code>.</p>',
    '<p>但在这种模式下有一个重要的注意事项。确保 future 的 poll 顺序是公平的就成了你的\r\n责任。例如，如果你要 join 一个流和一个关闭 future，且该流\r\n每次 poll 时都有大量消息需要长时间处理，\r\n那么你应该把关闭 future 放在 <code>try_join!</code> 列表的更前面，\r\n以确保它始终被 poll，而不会因流 future 长时间返回 <code>Poll::Pending</code> 而被延迟。</p>'.encode('utf-8')
)
add(
    b'<p>Basic <code>try_join</code> with two branches.</p>',
    '<p>两分支的基本 <code>try_join</code>。</p>'.encode('utf-8')
)
add(
    b'<p>Using <code>try_join!</code> with spawned tasks.</p>',
    '<p>在已派生的任务上使用 <code>try_join!</code>。</p>'.encode('utf-8')
)
add(
    b'<p>Using the <code>biased;</code> mode to control polling order.</p>',
    '<p>使用 <code>biased;</code> 模式来控制 poll 顺序。</p>'.encode('utf-8')
)

# ============== tokio/macro.pin.html remaining p ==============
add(
    b'<p>Calls to <code>async fn</code> return anonymous <a href="https://doc.rust-lang.org/1.95.0/core/future/future/trait.Future.html" title="trait core::future::future::Future"><code>Future</code></a> values that are <code>!Unpin</code>.\r\nThese values must be pinned before they can be polled. Calling <code>.await</code> will\r\nhandle this, but consumes the future. If it is required to call <code>.await</code> on\r\na <code>&amp;mut _</code> reference, the caller is responsible for pinning the future.</p>',
    '<p>调用 <code>async fn</code> 会返回匿名的 <a href="https://doc.rust-lang.org/1.95.0/core/future/future/trait.Future.html" title="trait core::future::future::Future"><code>Future</code></a> 值，这些值是 <code>!Unpin</code> 的。\r\n这些值在被 poll 之前必须先固定。调用 <code>.await</code> 会\r\n处理这一点，但会消费掉 future。如果需要在\r\n<code>&amp;mut _</code> 引用上调用 <code>.await</code>，则由调用者负责固定该 future。</p>'.encode('utf-8')
)
add(
    b'<p>Pinning may be done by allocating with <a href="https://doc.rust-lang.org/1.95.0/alloc/boxed/struct.Box.html#method.pin" title="associated function alloc::boxed::Box::pin"><code>Box::pin</code></a> or by using the stack\r\nwith the <code>pin!</code> macro.</p>',
    '<p>可以通过使用 <a href="https://doc.rust-lang.org/1.95.0/alloc/boxed/struct.Box.html#method.pin" title="associated function alloc::boxed::Box::pin"><code>Box::pin</code></a> 进行分配，或者通过 <code>pin!</code>\r\n宏使用栈来固定。</p>'.encode('utf-8')
)
add(
    b'<p>The following will <strong>fail to compile</strong>:</p>',
    '<p>下面的代码<strong>无法编译</strong>：</p>'.encode('utf-8')
)
add(
    b'<p>To make this work requires pinning:</p>',
    '<p>要让这段代码能够工作，需要进行固定：</p>'.encode('utf-8')
)
add(
    b'<p>Pinning is useful when using <code>select!</code> and stream operators that require <code>T: Stream + Unpin</code>.</p>',
    '<p>当使用 <code>select!</code> 以及需要 <code>T: Stream + Unpin</code> 的流操作符时，固定非常有用。</p>'.encode('utf-8')
)
add(
    b'<p>The <code>pin!</code> macro takes <strong>identifiers</strong> as arguments. It does <strong>not</strong> work\r\nwith expressions.</p>',
    '<p><code>pin!</code> 宏接受<strong>标识符</strong>作为参数。它<strong>不能</strong>用于\r\n表达式。</p>'.encode('utf-8')
)
add(
    b'<p>The following does not compile as an expression is passed to <code>pin!</code>.</p>',
    '<p>下面的代码无法编译，因为传给 <code>pin!</code> 的是一个表达式。</p>'.encode('utf-8')
)
add(
    b'<p>Using with select:</p>',
    '<p>与 select 一起使用：</p>'.encode('utf-8')
)
add(
    b'<p>Because assigning to a variable followed by pinning is common, there is also\r\na variant of the macro that supports doing both in one go.</p>',
    '<p>由于先赋值给变量再进行固定是常见操作，因此宏\r\n也提供了一个变体，可以一步完成这两件事。</p>'.encode('utf-8')
)

# ============== tokio/macro.task_local.html remaining p ==============
add(
    b'<p>Declares a new task-local key of type <a href="task/struct.LocalKey.html" title="struct tokio::task::LocalKey"><code>tokio::task::LocalKey</code></a>.</p>',
    '<p>声明一个 <a href="task/struct.LocalKey.html" title="struct tokio::task::LocalKey"><code>tokio::task::LocalKey</code></a> 类型的新任务局部键。</p>'.encode('utf-8')
)
add(
    b'<p>The macro wraps any number of static declarations and makes them local to the current task.\r\nPublicity and attributes for each static is preserved. For example:</p>',
    '<p>该宏可以包装任意数量的 static 声明，并将它们局部化到当前任务。\r\n每个 static 的可见性和属性都会被保留。例如：</p>'.encode('utf-8')
)
add(
    b'<p>See <a href="task/struct.LocalKey.html" title="struct tokio::task::LocalKey"><code>LocalKey</code> documentation</a> for more\r\ninformation.</p>',
    '<p>更多信息请参阅 <a href="task/struct.LocalKey.html" title="struct tokio::task::LocalKey"><code>LocalKey</code> 文档</a>。</p>'.encode('utf-8')
)

# Sort by length of en_bytes descending (longest first)
PAIRS.sort(key=lambda p: -len(p[0]))


def translate_file(path):
    with open(path, 'rb') as f:
        raw = f.read()
    original = raw
    n_replaced = 0
    for en, zh in PAIRS:
        if en in raw:
            n = raw.count(en)
            raw = raw.replace(en, zh)
            n_replaced += n
    if raw != original:
        with open(path, 'wb') as f:
            f.write(raw)
    return n_replaced


def main():
    targets = [
        'tokio/index.html',
        'tokio/attr.main.html',
        'tokio/attr.test.html',
        'tokio/macro.join.html',
        'tokio/macro.select.html',
        'tokio/macro.try_join.html',
        'tokio/macro.pin.html',
        'tokio/macro.task_local.html',
        'tokio/macro.join!.html',
        'tokio/macro.pin!.html',
        'tokio/all.html',
    ]
    total = 0
    for t in targets:
        n = translate_file(t)
        if n > 0:
            print(f'  {t}: {n} replacements')
            total += n
    print(f'\nTotal: {total} replacements')


if __name__ == '__main__':
    main()