"""翻译 h2 章节标题 (无 class="section-header" 的用户内容 h2) + 对应 sidebar TOC 链接。

涵盖：
- tokio: 30+ unique h2 (Cancellation, Usage, Syntax, AsyncRead and AsyncWrite, 等)
- bytes: Memory layout, Sharing, Growth
- rustls_pki_types: Making one
- quinn: About QUIC
- rcgen: Supported characters

每对 (anchor_pattern, h2_text, zh_text) 同时翻译：
  <h2 id="anchor"><a class="doc-anchor" href="#anchor">§</a>TEXT</h2>
  <a href="#anchor" title="TEXT">TEXT</a>

anchor_pattern 可能是多个候选 ID（rustdoc 生成的 ID 有时与原文不完全一致）。

用法：
  python _common_tools/_translate_section_h2.py [--dry]
"""
import os
import re
import sys
import argparse

# (anchor_candidates, h2_text_in_html, h2_text_in_zh, sidebar_link_text_in_zh)
# 如果 anchor 是 None，则按 h2_text 匹配（grep 风格）
# h2_text_in_html 必须精确匹配 HTML 中的内容（可能含 <code> 标签）
PAIRS = [
    # === tokio ===
    # time module
    (['cancellation'], 'Cancellation', '取消', '取消'),
    # macro
    (['syntax'], 'Syntax', '语法', '语法'),
    (['usage'], 'Usage', '用法', '用法'),
    # io module
    (['asyncread-and-asyncwrite'],
     '<code>AsyncRead</code> and <code>AsyncWrite</code>',
     '<code>AsyncRead</code> 与 <code>AsyncWrite</code>',
     'AsyncRead 与 AsyncWrite'),
    (['standard-input-and-output'], 'Standard input and output', '标准输入与输出', '标准输入与输出'),
    (['std-re-exports'], '<code>std</code> re-exports', '<code>std</code> 重导出', 'std 重导出'),
    # net module
    (['organization'], 'Organization', '组织结构', '组织结构'),
    (['streams'], 'Streams', '流', '流'),
    # UdpSocket
    (['example-one-to-many-bind'], 'Example: one to many (bind)', '示例：一对多（bind）', '示例：一对多（bind）'),
    (['example-one-to-one-connect'], 'Example: one to one (connect)', '示例：一对一（connect）', '示例：一对一（connect）'),
    (['example-splitting-with-arc'], 'Example: Splitting with <code>Arc</code>', '示例：使用 <code>Arc</code> 分割', '示例：使用 Arc 分割'),
    # ToSocketAddrs
    (['dns'], 'DNS', 'DNS', 'DNS'),
    (['calling'], 'Calling', '调用', '调用'),
    # watch
    (['closing'], 'Closing', '关闭', '关闭'),
    # runtime/index
    (['detailed-runtime-behavior'], 'Detailed runtime behavior', '详细的 runtime 行为', '详细的 runtime 行为'),
    (['performance-tuning'], 'Performance tuning', '性能调优', '性能调优'),
    # Runtime
    (['shutdown'], 'Shutdown', '关闭', '关闭'),
    (['sharing'], 'Sharing', '共享', '共享'),
    # stream
    (['why-was-stream-not-included-in-tokio-10', 'why-was-stream-not-included-in-tokio-1-0'],
     'Why was <code>Stream</code> not included in Tokio 1.0?',
     '为什么 Tokio 1.0 没有包含 <code>Stream</code>？',
     '为什么 Tokio 1.0 没有包含 Stream？'),
    # sync
    (['message-passing'], 'Message passing', '消息传递', '消息传递'),
    (['state-synchronization'], 'State synchronization', '状态同步', '状态同步'),
    (['runtime-compatibility'], 'Runtime compatibility', 'Runtime 兼容性', 'Runtime 兼容性'),
    # Mutex
    (['which-kind-of-mutex-should-you-use', 'which-kind-of-mutex-should-you-use-'],
     'Which kind of mutex should you use?',
     '应该使用哪种 mutex？',
     '应该使用哪种 mutex？'),
    (['examples'], 'Examples:', '示例：', '示例：'),
    # oneshot Receiver
    (['cancellation-safety'], 'Cancellation safety', '取消安全性', '取消安全性'),
    # watch
    (['thread-safety'], 'Thread safety', '线程安全性', '线程安全性'),
    # spawn
    (['using-send-values-from-a-task'],
     'Using <code>!Send</code> values from a task',
     '在 task 中使用 <code>!Send</code> 值',
     '在 task 中使用 !Send 值'),
    (['when-to-use-spawn_blocking-vs-dedicated-threads'],
     'When to use <code>spawn_blocking</code> vs dedicated threads',
     '何时使用 <code>spawn_blocking</code>，何时使用专用线程',
     '何时使用 spawn_blocking，何时使用专用线程'),
    (['related-ap-is-and-patterns-for-bridging-asynchronous-and-blocking-code',
      'related-apis-and-patterns-for-bridging-asynchronous-and-blocking-code'],
     'Related APIs and patterns for bridging asynchronous and blocking code',
     '桥接异步与阻塞代码的相关 API 与模式',
     '桥接异步与阻塞代码的相关 API 与模式'),
    # JoinSet
    (['task-id-guarantees'], 'Task ID guarantees', 'Task ID 保证', 'Task ID 保证'),
    # LocalSet
    (['use-with-run_until', 'use-with-run-until'],
     'Use with <code>run_until</code>',
     '与 <code>run_until</code> 一起使用',
     '与 run_until 一起使用'),

    # === bytes (3) ===
    (['memory-layout'], 'Memory layout', '内存布局', '内存布局'),
    (['growth'], 'Growth', '增长', '增长'),

    # === rustls_pki_types (1) ===
    (['making-one'], 'Making one', '构造一个', '构造一个'),

    # === quinn (1) ===
    (['about-quic'], 'About QUIC', '关于 QUIC', '关于 QUIC'),

    # === rcgen (1) ===
    (['supported-characters'], 'Supported characters', '支持的字符', '支持的字符'),
]


def translate_file(path, dry=False):
    """翻译一个 HTML 文件中的 h2 标题和对应 sidebar TOC 链接。"""
    with open(path, 'rb') as f:
        raw = f.read()

    n_changed = 0
    for anchors, en_html, zh_html, toc_zh in PAIRS:
        # 尝试每个候选 anchor
        h2_done = False
        for anchor in anchors:
            # 1) 翻译 h2: <h2 id="anchor"><a class="doc-anchor" href="#anchor">§</a>EN_HTML</h2>
            old_h2 = f'<h2 id="{anchor}"><a class="doc-anchor" href="#{anchor}">§</a>{en_html}</h2>'.encode('utf-8')
            new_h2 = f'<h2 id="{anchor}"><a class="doc-anchor" href="#{anchor}">§</a>{zh_html}</h2>'.encode('utf-8')
            if old_h2 in raw:
                if not dry:
                    raw = raw.replace(old_h2, new_h2)
                n_changed += 1
                print(f'  [h2] {anchor}')
                h2_done = True
                break

        if h2_done:
            continue

        # 2) 翻译 sidebar TOC: <a href="#anchor" title="EN_TEXT">EN_TEXT</a>
        # 注意: sidebar 的 en_text 是纯文本（不含 <code>），所以用 toc_zh 的英文版
        for anchor in anchors:
            # Sidebar link text 通常是纯文本
            en_text_for_toc = re.sub(r'<[^>]+>', '', en_html)
            old_link = f'<a href="#{anchor}" title="{en_text_for_toc}">{en_text_for_toc}</a>'.encode('utf-8')
            new_link = f'<a href="#{anchor}" title="{toc_zh}">{toc_zh}</a>'.encode('utf-8')
            if old_link in raw:
                if not dry:
                    raw = raw.replace(old_link, new_link)
                n_changed += 1
                print(f'  [toc] {anchor}')
                break

    if n_changed > 0 and not dry:
        with open(path, 'wb') as f:
            f.write(raw)
    return n_changed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry', action='store_true', help='dry run, do not modify files')
    args = parser.parse_args()

    crates = ['tokio', 'bytes', 'rustls_pki_types', 'quinn', 'rcgen']
    total_changed = 0
    for crate in crates:
        if not os.path.isdir(crate):
            print(f'[skip] {crate}: not a directory')
            continue
        n_crate = 0
        for root, dirs, files in os.walk(crate):
            if any(s in root for s in ['_old', '.git']):
                continue
            for f in files:
                if not f.endswith('.html'):
                    continue
                p = os.path.join(root, f)
                n = translate_file(p, dry=args.dry)
                if n > 0:
                    print(f'  {p}: {n} changes')
                    n_crate += n
        print(f'[{crate}] total: {n_crate} changes')
        total_changed += n_crate
    print(f'\nGrand total: {total_changed} changes')


if __name__ == '__main__':
    main()
