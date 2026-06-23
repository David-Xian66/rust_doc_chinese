"""Translate the final 7 remaining untranslated docblocks."""

import os
import re

BASE = 'D:/Administrator/Documents/Code/rust_doc_all/quinn'

TRANSLATIONS = [
    # trait.AsyncTimer.html — 2 blocks
    (
        'trait.AsyncTimer.html',
        [
            ('<p>Update the timer to expire at <code>i</code></p>',
             '<p>将定时器更新为在 <code>i</code> 时刻触发</p>'),
            ('<p>Check whether the timer has expired, and register to be woken if not</p>',
             '<p>检查定时器是否已到期；若尚未到期则注册为等待唤醒</p>'),
        ],
    ),
    # trait.TokenStore.html — 2 blocks
    (
        'trait.TokenStore.html',
        [
            ('<p>Potentially store a token for later one-time use</p>\n<p>Called when a NEW_TOKEN frame is received from the server.</p>',
             '<p>可能地存储一个令牌以供后续一次性使用</p>\n<p>在从服务器收到 NEW_TOKEN 帧时调用。</p>'),
            ('<p>Try to find and take a token that was stored with the given server name</p>\n<p>The same token must never be returned from <code>take</code> twice, as doing so can be used to\nde-anonymize a client’s traffic.</p>\n<p>Called when trying to connect to a server. It is always ok for this to return <code>None</code>.</p>',
             '<p>尝试查找并取出一个先前以给定服务器名存储的令牌</p>\n<p>同一令牌绝不能被 <code>take</code> 返回两次，否则可能被用于对客户端流量进行去匿名化。</p>\n<p>在尝试连接服务器时调用。此处始终允许返回 <code>None</code>。</p>'),
        ],
    ),
    # crypto/trait.AeadKey.html — 2 blocks
    (
        'crypto/trait.AeadKey.html',
        [
            ('<p>Method for sealing message <code>data</code></p>',
             '<p>对消息 <code>data</code> 进行密封（seal）的方法</p>'),
            ('<p>Method for opening a sealed message <code>data</code></p>',
             '<p>对已密封的消息 <code>data</code> 进行开解（open）的方法</p>'),
        ],
    ),
    # trait.TimeSource.html — 1 block
    (
        'trait.TimeSource.html',
        [
            ('<p>Get <a href="https://doc.rust-lang.org/1.95.0/std/time/struct.SystemTime.html#method.now" title="associated function std::time::SystemTime::now"><code>SystemTime::now()</code></a> or the mocked equivalent</p>',
             '<p>获取 <a href="https://doc.rust-lang.org/1.95.0/std/time/struct.SystemTime.html#method.now" title="associated function std::time::SystemTime::now"><code>SystemTime::now()</code></a>，或在测试中返回相应的 mock 值</p>'),
        ],
    ),
    # trait.TokenLog.html — 1 block
    (
        'trait.TokenLog.html',
        [
            ('<p>Record that the token was used and, ideally, return a token reuse error if the token may\nhave been already used previously</p>\n<p>False negatives and false positives are both permissible. Called when a client uses an\naddress validation token.</p>\n<p>Parameters:</p>\n<ul>\n<li><code>nonce</code>: A server-generated random unique value for the token.</li>\n<li><code>issued</code>: The time the server issued the token.</li>\n<li><code>lifetime</code>: The expiration time of address validation tokens sent via NEW_TOKEN frames,\nas configured by <a href="struct.ValidationTokenConfig.html#method.lifetime" title="method quinn::ValidationTokenConfig::lifetime"><code>ServerValidationTokenConfig::lifetime</code></a>.</li>\n</ul>\n<h6 id="security--performance"><a class="doc-anchor" href="#security--performance">§</a>Security &amp; Performance</h6>\n<p>To the extent that it is possible to repeatedly trigger false negatives (returning <code>Ok</code> for\na token which has been reused), an attacker could use the server to perform <a href="https://en.wikipedia.org/wiki/Denial-of-service_attack#Amplification">amplification\nattacks</a>. The QUIC specification requires that this be limited, if not prevented fully.</p>\n<p>A false positive (returning <code>Err</code> for a token which has never been used) is not a security\nvulnerability; it is permissible for a <code>TokenLog</code> to always return <code>Err</code>. A false positive\ncauses the token to be ignored, which may cause the transmission of some 0.5-RTT data to be\ndelayed until the handshake completes, if a sufficient amount of 0.5-RTT data it sent.</p>',
             '<p>记录该令牌已被使用，并在理想情况下当令牌可能曾被使用时返回令牌重用错误</p>\n<p>误报与漏报都是允许的。在客户端使用地址验证令牌时调用。</p>\n<p>参数：</p>\n<ul>\n<li><code>nonce</code>：服务器为该令牌生成的随机唯一值。</li>\n<li><code>issued</code>：服务器签发该令牌的时间。</li>\n<li><code>lifetime</code>：通过 NEW_TOKEN 帧发送的地址验证令牌的过期时间，由 <a href="struct.ValidationTokenConfig.html#method.lifetime" title="method quinn::ValidationTokenConfig::lifetime"><code>ServerValidationTokenConfig::lifetime</code></a> 配置。</li>\n</ul>\n<h6 id="security--performance"><a class="doc-anchor" href="#security--performance">§</a>安全与性能</h6>\n<p>在攻击者能够反复触发漏报（即对已被重用的令牌仍返回 <code>Ok</code>）的范围内，攻击者可能借此对服务器发起 <a href="https://en.wikipedia.org/wiki/Denial-of-service_attack#Amplification">放大攻击</a>。QUIC 规范要求将该风险限制在一定范围内，即使不能完全避免。</p>\n<p>误报（对从未被使用过的令牌返回 <code>Err</code>）并非安全漏洞；<code>TokenLog</code> 始终返回 <code>Err</code> 也是允许的。误报会导致该令牌被忽略，从而使部分 0.5-RTT 数据——若已发送了足够多的 0.5-RTT 数据——需要等到握手完成后才能继续传输。</p>'),
        ],
    ),
    # trait.UdpPoller.html — 1 block
    (
        'trait.UdpPoller.html',
        [
            ('<p>Check whether the associated socket is likely to be writable</p>\n<p>Must be called after <a href="trait.AsyncUdpSocket.html#tymethod.try_send" title="method quinn::AsyncUdpSocket::try_send"><code>AsyncUdpSocket::try_send</code></a> returns <a href="https://doc.rust-lang.org/1.95.0/std/io/error/enum.ErrorKind.html#variant.WouldBlock" title="variant std::io::error::ErrorKind::WouldBlock"><code>io::ErrorKind::WouldBlock</code></a> to\nregister the task associated with <code>cx</code> to be woken when a send should be attempted\nagain. Unlike in <a href="https://doc.rust-lang.org/1.95.0/core/future/future/trait.Future.html#tymethod.poll" title="method core::future::future::Future::poll"><code>Future::poll</code></a>, a <a href="trait.UdpPoller.html" title="trait quinn::UdpPoller"><code>UdpPoller</code></a> may be reused indefinitely no matter how\nmany times <code>poll_writable</code> returns <a href="https://doc.rust-lang.org/1.95.0/core/task/poll/enum.Poll.html#variant.Ready" title="variant core::task::poll::Poll::Ready"><code>Poll::Ready</code></a>.</p>',
             '<p>检查相关套接字是否可能可写</p>\n<p>必须在 <a href="trait.AsyncUdpSocket.html#tymethod.try_send" title="method quinn::AsyncUdpSocket::try_send"><code>AsyncUdpSocket::try_send</code></a> 返回 <a href="https://doc.rust-lang.org/1.95.0/std/io/error/enum.ErrorKind.html#variant.WouldBlock" title="variant std::io::error::ErrorKind::WouldBlock"><code>io::ErrorKind::WouldBlock</code></a> 之后调用，\n以便将 <code>cx</code> 关联的任务注册为在下次可发送时唤醒。与 <a href="https://doc.rust-lang.org/1.95.0/core/future/future/trait.Future.html#tymethod.poll" title="method core::future::future::Future::poll"><code>Future::poll</code></a> 不同，<a href="trait.UdpPoller.html" title="trait quinn::UdpPoller"><code>UdpPoller</code></a> 可以无限次复用，\n无论 <code>poll_writable</code> 返回多少次 <a href="https://doc.rust-lang.org/1.95.0/core/task/poll/enum.Poll.html#variant.Ready" title="variant core::task::poll::Poll::Ready"><code>Poll::Ready</code></a>。</p>'),
        ],
    ),
    # crypto/trait.ClientConfig.html — 1 block
    (
        'crypto/trait.ClientConfig.html',
        [
            ('<p>Start a client session with this configuration</p>',
             '<p>使用该配置启动一个客户端会话</p>'),
        ],
    ),
]


def main():
    total_files = 0
    total_found = 0
    for rel, pairs in TRANSLATIONS:
        path = os.path.join(BASE, rel)
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        orig = c
        found = 0
        missed = []
        for old, new in pairs:
            if old in c:
                c = c.replace(old, new)
                found += 1
            else:
                missed.append(old[:80])
        if c != orig:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(c)
            total_files += 1
            total_found += found
            cjk = re.findall(r'[一-鿿]', c)
            print(f'  {rel}: {found}/{len(pairs)} CJK={len(cjk)}')
            for m in missed:
                print(f'    MISSED: {m!r}')
    print(f'Updated {total_files} files; total replacements: {total_found}')


if __name__ == '__main__':
    main()