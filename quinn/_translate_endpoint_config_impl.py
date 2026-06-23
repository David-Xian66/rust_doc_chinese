"""Translate 11 untranslated docblocks in quinn/struct.EndpointConfig.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/struct.EndpointConfig.html'

TRANSLATIONS = [
    ('<p>Create a default config with a particular <code>reset_key</code></p>',
     '<p>使用指定的 <code>reset_key</code> 创建一个默认配置</p>'),
    ('<p>Supply a custom connection ID generator factory</p>\n<p>Called once by each <code>Endpoint</code> constructed from this configuration to obtain the CID\ngenerator which will be used to generate the CIDs used for incoming packets on all\nconnections involving that  <code>Endpoint</code>. A custom CID generator allows applications to embed\ninformation in local connection IDs, e.g. to support stateless packet-level load balancers.</p>\n<p>Defaults to <a href="../quinn_proto/cid_generator/struct.HashedConnectionIdGenerator.html" title="struct quinn_proto::cid_generator::HashedConnectionIdGenerator"><code>HashedConnectionIdGenerator</code></a>.</p>',
     '<p>提供一个自定义的连接 ID 生成器工厂</p>\n<p>每个由本配置构造的 <code>Endpoint</code> 都会调用一次该工厂，以获取 CID 生成器，用于为该 <code>Endpoint</code> 所涉及的所有连接的入站包生成 CID。自定义 CID 生成器允许应用程序在本地连接 ID 中嵌入信息，例如支持无状态的数据包级负载均衡器。</p>\n<p>默认为 <a href="../quinn_proto/cid_generator/struct.HashedConnectionIdGenerator.html" title="struct quinn_proto::cid_generator::HashedConnectionIdGenerator"><code>HashedConnectionIdGenerator</code></a>。</p>'),
    ('<p>Private key used to send authenticated connection resets to peers who were\ncommunicating with a previous instance of this endpoint.</p>',
     '<p>用于向与本端点上一实例通信的对端发送已认证的连接重置所用的私钥。</p>'),
    ('<p>Maximum UDP payload size accepted from peers (excluding UDP and IP overhead).</p>\n<p>Must be greater or equal than 1200.</p>\n<p>Defaults to 1472, which is the largest UDP payload that can be transmitted in the typical\n1500 byte Ethernet MTU. Deployments on links with larger MTUs (e.g. loopback or Ethernet\nwith jumbo frames) can raise this to improve performance at the cost of a linear increase in\ndatagram receive buffer size.</p>',
     '<p>接受来自对端的最大 UDP 有效负载大小（不含 UDP 与 IP 头部开销）。</p>\n<p>必须大于或等于 1200。</p>\n<p>默认为 1472，这是可在典型 1500 字节以太网 MTU 中传输的最大 UDP 有效负载。在具有更大 MTU 的链路上（例如回环或使用巨型帧的以太网），可以增大该值以提升性能，代价是数据报接收缓冲区大小线性增长。</p>'),
    ('<p>Get the current value of <a href="struct.EndpointConfig.html#method.max_udp_payload_size" title="method quinn::EndpointConfig::max_udp_payload_size"><code>max_udp_payload_size</code></a></p>',
     '<p>获取 <a href="struct.EndpointConfig.html#method.max_udp_payload_size" title="method quinn::EndpointConfig::max_udp_payload_size"><code>max_udp_payload_size</code></a> 的当前值</p>'),
    ('<p>Override supported QUIC versions</p>',
     '<p>覆盖所支持的 QUIC 版本</p>'),
    ('<p>Whether to accept QUIC packets containing any value for the fixed bit</p>\n<p>Enabled by default. Helps protect against protocol ossification and makes traffic less\nidentifiable to observers. Disable if helping observers identify this traffic as QUIC is\ndesired.</p>',
     '<p>是否接受 QUIC 包头中 fixed bit 为任意取值的包</p>\n<p>默认开启。有助于防止协议僵化，并降低流量对观察者的可识别度。若希望让观察者能够将本流量识别为 QUIC，可关闭该选项。</p>'),
    ('<p>Minimum interval between outgoing stateless reset packets</p>\n<p>Defaults to 20ms. Limits the impact of attacks which flood an endpoint with garbage packets,\ne.g. <a href="https://bughunters.google.com/blog/5960150648750080/preventing-cross-service-udp-loops-in-quic#isakmp-ike-amplification-vs-quic">ISAKMP/IKE amplification</a>. Larger values provide a stronger defense, but may delay\ndetection of some error conditions by clients. Using a <a href="trait.ConnectionIdGenerator.html" title="trait quinn::ConnectionIdGenerator"><code>ConnectionIdGenerator</code></a> with a low\nrate of false positives in <a href="trait.ConnectionIdGenerator.html#method.validate" title="method quinn::ConnectionIdGenerator::validate"><code>validate</code></a> reduces the risk\nincurred by a small minimum reset interval.</p>',
     '<p>两条外发无状态重置包之间的最小间隔</p>\n<p>默认为 20ms。用于限制向端点发送垃圾包的攻击（例如 <a href="https://bughunters.google.com/blog/5960150648750080/preventing-cross-service-udp-loops-in-quic#isakmp-ike-amplification-vs-quic">ISAKMP/IKE amplification</a>）所造成的影响。较大的值能提供更强的防御，但可能延迟客户端对某些错误情况的检测。使用在 <a href="trait.ConnectionIdGenerator.html#method.validate" title="method quinn::ConnectionIdGenerator::validate"><code>validate</code></a> 中具有较低误报率的 <a href="trait.ConnectionIdGenerator.html" title="trait quinn::ConnectionIdGenerator"><code>ConnectionIdGenerator</code></a>，可以降低使用较小最小重置间隔所带来的风险。</p>'),
    ('<p>Optional seed to be used internally for random number generation</p>\n<p>By default, quinn will initialize an endpoint’s rng using a platform entropy source.\nHowever, you can seed the rng yourself through this method (e.g. if you need to run quinn\ndeterministically or if you are using quinn in an environment that doesn’t have a source of\nentropy available).</p>',
     '<p>供内部随机数生成使用的可选种子</p>\n<p>默认情况下，quinn 使用平台熵源初始化端点的随机数生成器。但你也可以通过本方法自行设定种子（例如需要确定性运行 quinn，或在无可用熵源的环境中运行）。</p>'),
    ('</h4></section></summary><div class="docblock"><p>Returns the argument unchanged.</p>',
     '</h4></section></summary><div class="docblock"><p>原样返回该参数。</p>'),
    ('<p>Calls <code>U::from(self)</code>.</p>\n<p>That is, this conversion is whatever the implementation of\n<code><a href="https://doc.rust-lang.org/1.95.0/core/convert/trait.From.html" title="trait core::convert::From">From</a>&lt;T&gt; for U</code> chooses to do.</p>',
     '<p>调用 <code>U::from(self)</code>。</p>\n<p>也就是说，此转换行为完全由\n<code><a href="https://doc.rust-lang.org/1.95.0/core/convert/trait.From.html" title="trait core::convert::From">From</a>&lt;T&gt; for U</code> 的实现决定。</p>'),
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