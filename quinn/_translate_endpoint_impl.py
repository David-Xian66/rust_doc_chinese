"""Translate all impl-section method docblocks in quinn/struct.Endpoint.html."""

import os, re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/struct.Endpoint.html'

# Each entry: (old, new) where old is the entire docblock <div class="docblock">...</div>
# The old strings are taken exactly from the source file.
TRANSLATIONS = [
    # 1. client (3 paragraphs + code example)
    (
        '<div class="docblock"><p>Helper to construct an endpoint for use with outgoing connections only</p>\n<p>Note that <code>addr</code> is the <em>local</em> address to bind to, which should usually be a wildcard\naddress like <code>0.0.0.0:0</code> or <code>[::]:0</code>, which allow communication with any reachable IPv4 or\nIPv6 address respectively from an OS-assigned port.</p>\n<p>If an IPv6 address is provided, attempts to make the socket dual-stack so as to allow\ncommunication with both IPv4 and IPv6 addresses. As such, calling <code>Endpoint::client</code> with\nthe address <code>[::]:0</code> is a reasonable default to maximize the ability to connect to other\naddress. For example:</p>',
        '<div class="docblock"><p>辅助函数，用于构造一个仅用于出站连接的端点</p>\n<p>注意，<code>addr</code> 是要绑定的<em>本地</em>地址，通常应当是通配地址，例如 <code>0.0.0.0:0</code> 或 <code>[::]:0</code>，分别允许通过操作系统分配的端口与任意可达的 IPv4 或 IPv6 地址通信。</p>\n<p>如果提供的是 IPv6 地址，则会尝试让该套接字支持双栈，以便同时与 IPv4 和 IPv6 地址通信。因此，使用 <code>[::]:0</code> 调用 <code>Endpoint::client</code> 是一个合理的默认值，可最大化与其他地址建立连接的能力。例如：</p>',
    ),
    # 2. stats
    (
        '<div class="docblock"><p>Returns relevant stats from this Endpoint</p>',
        '<div class="docblock"><p>返回该 Endpoint 的相关统计信息</p>',
    ),
    # 3. server (2 paragraphs)
    (
        '<div class="docblock"><p>Helper to construct an endpoint for use with both incoming and outgoing connections</p>\n<p>Platform defaults for dual-stack sockets vary. For example, any socket bound to a wildcard\nIPv6 address on Windows will not by default be able to communicate with IPv4\naddresses. Portable applications should bind an address that matches the family they wish to\ncommunicate within.</p>',
        '<div class="docblock"><p>辅助函数，用于构造一个既支持入站又支持出站连接的端点</p>\n<p>双栈套接字在各个平台上的默认行为并不一致。例如，在 Windows 上，绑定到 IPv6 通配地址的套接字默认无法与 IPv4 地址通信。可移植的应用应绑定一个与它希望通信的地址族相匹配的地址。</p>',
    ),
    # 4. new
    (
        '<div class="docblock"><p>Construct an endpoint with arbitrary configuration and socket</p>',
        '<div class="docblock"><p>使用任意配置和套接字构造一个端点</p>',
    ),
    # 5. new_with_abstract_socket (2 paragraphs)
    (
        '<div class="docblock"><p>Construct an endpoint with arbitrary configuration and pre-constructed abstract socket</p>\n<p>Useful when <code>socket</code> has additional state (e.g. sidechannels) attached for which shared\nownership is needed.</p>',
        '<div class="docblock"><p>使用任意配置与预先构造的抽象套接字构造一个端点</p>\n<p>当 <code>socket</code> 附带一些额外的状态（例如用于旁路通信的 side channel），且这些状态需要共享所有权时，本方法非常有用。</p>',
    ),
    # 6. accept (2 paragraphs)
    (
        '<div class="docblock"><p>Get the next incoming connection attempt from a client</p>\n<p>Yields <a href="struct.Incoming.html" title="struct quinn::Incoming"><code>Incoming</code></a>s, or <code>None</code> if the endpoint is <a href="struct.Endpoint.html#method.close" title="method quinn::Endpoint::close"><code>close</code></a>d. <a href="struct.Incoming.html" title="struct quinn::Incoming"><code>Incoming</code></a>\ncan be <code>await</code>ed to obtain the final <a href="struct.Connection.html" title="struct quinn::Connection"><code>Connection</code></a>, or used to e.g.\nfilter connection attempts or force address validation, or converted into an intermediate\n<code>Connecting</code> future which can be used to e.g. send 0.5-RTT data.</p>',
        '<div class="docblock"><p>获取来自客户端的下一个入站连接尝试</p>\n<p>产生一系列 <a href="struct.Incoming.html" title="struct quinn::Incoming"><code>Incoming</code></a>，若端点已被 <a href="struct.Endpoint.html#method.close" title="method quinn::Endpoint::close"><code>close</code></a> 则返回 <code>None</code>。<a href="struct.Incoming.html" title="struct quinn::Incoming"><code>Incoming</code></a> 可以被 <code>await</code> 以获得最终的 <a href="struct.Connection.html" title="struct quinn::Connection"><code>Connection</code></a>，也可以用于例如过滤连接尝试、强制地址校验，或转换为一个中间的 <code>Connecting</code> future（进而可以用于发送 0.5-RTT 数据等）。</p>',
    ),
    # 7. set_default_client_config
    (
        '<div class="docblock"><p>Set the client configuration used by <code>connect</code></p>',
        '<div class="docblock"><p>设置 <code>connect</code> 所使用的客户端配置</p>',
    ),
    # 8. connect (3 paragraphs)
    (
        '<div class="docblock"><p>Connect to a remote endpoint</p>\n<p><code>server_name</code> must be covered by the certificate presented by the server. This prevents a\nconnection from being intercepted by an attacker with a valid certificate for some other\nserver.</p>\n<p>May fail immediately due to configuration errors, or in the future if the connection could\nnot be established.</p>',
        '<div class="docblock"><p>连接到一个远程端点</p>\n<p><code>server_name</code> 必须能被服务器出示的证书所覆盖。这可以防止拥有针对其他服务器有效证书的攻击者拦截该连接。</p>\n<p>可能由于配置错误而立即失败，也可能在未来由于连接无法建立而失败。</p>',
    ),
    # 9. connect_with (2 paragraphs)
    (
        '<div class="docblock"><p>Connect to a remote endpoint using a custom configuration.</p>\n<p>See <a href="struct.Endpoint.html#method.connect" title="method quinn::Endpoint::connect"><code>connect()</code></a> for details.</p>',
        '<div class="docblock"><p>使用自定义配置连接到一个远程端点。</p>\n<p>详细信息请参阅 <a href="struct.Endpoint.html#method.connect" title="method quinn::Endpoint::connect"><code>connect()</code></a>。</p>',
    ),
    # 10. rebind (2 paragraphs)
    (
        '<div class="docblock"><p>Switch to a new UDP socket</p>\n<p>See <a href="struct.Endpoint.html#method.rebind_abstract" title="method quinn::Endpoint::rebind_abstract"><code>Endpoint::rebind_abstract()</code></a> for details.</p>',
        '<div class="docblock"><p>切换到一个新的 UDP 套接字</p>\n<p>详细信息请参阅 <a href="struct.Endpoint.html#method.rebind_abstract" title="method quinn::Endpoint::rebind_abstract"><code>Endpoint::rebind_abstract()</code></a>。</p>',
    ),
    # 11. rebind_abstract (3 paragraphs)
    (
        '<div class="docblock"><p>Switch to a new UDP socket</p>\n<p>Allows the endpoint’s address to be updated live, affecting all active connections. Incoming\nconnections and connections to servers unreachable from the new address will be lost.</p>\n<p>On error, the old UDP socket is retained.</p>',
        '<div class="docblock"><p>切换到一个新的 UDP 套接字</p>\n<p>允许端点的地址被实时更新，影响所有活跃连接。从新地址无法到达的入站连接以及与服务器之间的连接将会丢失。</p>\n<p>出错时，旧的 UDP 套接字会被保留。</p>',
    ),
    # 12. set_server_config (2 paragraphs)
    (
        '<div class="docblock"><p>Replace the server configuration, affecting new incoming connections only</p>\n<p>Useful for e.g. refreshing TLS certificates without disrupting existing connections.</p>',
        '<div class="docblock"><p>替换服务器配置，仅影响后续的入站连接</p>\n<p>典型用途包括：在不中断现有连接的情况下刷新 TLS 证书。</p>',
    ),
    # 13. local_addr
    (
        '<div class="docblock"><p>Get the local <code>SocketAddr</code> the underlying socket is bound to</p>',
        '<div class="docblock"><p>获取底层套接字所绑定到的本地 <code>SocketAddr</code></p>',
    ),
    # 14. open_connections
    (
        '<div class="docblock"><p>Get the number of connections that are currently open</p>',
        '<div class="docblock"><p>获取当前处于打开状态的连接数量</p>',
    ),
    # 15. close (2 paragraphs)
    (
        '<div class="docblock"><p>Close all of this endpoint’s connections immediately and cease accepting new connections.</p>\n<p>See <a href="struct.Connection.html#method.close" title="method quinn::Connection::close"><code>Connection::close()</code></a> for details.</p>',
        '<div class="docblock"><p>立即关闭本端点的所有连接，并停止接受新的连接。</p>\n<p>详细信息请参阅 <a href="struct.Connection.html#method.close" title="method quinn::Connection::close"><code>Connection::close()</code></a>。</p>',
    ),
    # 16. wait_idle (3 paragraphs)
    (
        '<div class="docblock"><p>Wait for all connections on the endpoint to be cleanly shut down</p>\n<p>Waiting for this condition before exiting ensures that a good-faith effort is made to notify\npeers of recent connection closes, whereas exiting immediately could force them to wait out\nthe idle timeout period.</p>\n<p>Does not proactively close existing connections or cause incoming connections to be\nrejected. Consider calling <a href="struct.Endpoint.html#method.close" title="method quinn::Endpoint::close"><code>close()</code></a> if that is desired.</p>',
        '<div class="docblock"><p>等待端点上的所有连接被干净地关闭</p>\n<p>在退出前等待该条件可以保证诚实地通知对端最近的连接关闭事件；而立刻退出则可能迫使对端不得不等完整个空闲超时时段。</p>\n<p>该方法不会主动关闭现有连接，也不会使新的入站连接被拒绝。如果有这些需求，请考虑调用 <a href="struct.Endpoint.html#method.close" title="method quinn::Endpoint::close"><code>close()</code></a>。</p>',
    ),
]


def main():
    with open(PATH, 'r', encoding='utf-8') as f:
        c = f.read()

    found = 0
    missed = []
    for old, new in TRANSLATIONS:
        if old in c:
            c = c.replace(old, new)
            found += 1
        else:
            missed.append(old[:80])

    with open(PATH, 'w', encoding='utf-8') as f:
        f.write(c)

    cjk = re.findall(r'[一-鿿]', c)
    print(f'Found: {found}/{len(TRANSLATIONS)} docblocks')
    print(f'CJK: {len(cjk)}')
    if missed:
        print('Missed docblocks:')
        for m in missed:
            print(f'  {m!r}')


if __name__ == '__main__':
    main()