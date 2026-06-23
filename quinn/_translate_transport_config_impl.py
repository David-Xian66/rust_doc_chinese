"""Translate all impl-section docblocks in quinn/struct.TransportConfig.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/struct.TransportConfig.html'

TRANSLATIONS = [
    # 1. max_concurrent_bidi_streams
    ('<p>Maximum number of incoming bidirectional streams that may be open concurrently</p>\n<p>Must be nonzero for the peer to open any bidirectional streams.</p>\n<p>Worst-case memory use is directly proportional to <code>max_concurrent_bidi_streams * stream_receive_window</code>, with an upper bound proportional to <code>receive_window</code>.</p>',
     '<p>同时处于打开状态的入站双向流的最大数量</p>\n<p>必须为非零值，对端才能打开任何双向流。</p>\n<p>最坏情况下内存占用与 <code>max_concurrent_bidi_streams * stream_receive_window</code> 成正比，上界则与 <code>receive_window</code> 成正比。</p>'),
    # 2. max_concurrent_uni_streams
    ('<p>Variant of <code>max_concurrent_bidi_streams</code> affecting unidirectional streams</p>',
     '<p><code>max_concurrent_bidi_streams</code> 的变体，作用于单向流</p>'),
    # 3. max_idle_timeout
    ('<p>Maximum duration of inactivity to accept before timing out the connection.</p>\n<p>The true idle timeout is the minimum of this and the peer’s own max idle timeout. <code>None</code>\nrepresents an infinite timeout. Defaults to 30 seconds.</p>\n<p><strong>WARNING</strong>: If a peer or its network path malfunctions or acts maliciously, an infinite\nidle timeout can result in permanently hung futures!</p>',
     '<p>在连接因不活跃而超时之前所允许的最大空闲时长。</p>\n<p>实际的空闲超时取本配置与对端自身最大空闲超时两者中的较小值。<code>None</code> 表示无限空闲超时。默认为 30 秒。</p>\n<p><strong>警告</strong>：若对端或其网络路径出现故障或存在恶意行为，无限的空闲超时可能导致 future 永久挂起！</p>'),
    # 4. stream_receive_window
    ('<p>Maximum number of bytes the peer may transmit without acknowledgement on any one stream\nbefore becoming blocked.</p>\n<p>This should be set to at least the expected connection latency multiplied by the maximum\ndesired throughput. Setting this smaller than <code>receive_window</code> helps ensure that a single\nstream doesn’t monopolize receive buffers, which may otherwise occur if the application\nchooses not to read from a large stream for a time while still requiring data on other\nstreams.</p>',
     '<p>对端在任意单个流上未被确认即可发送的字节上限，达到此上限后将被阻塞。</p>\n<p>该值至少应设置为预期连接延迟与期望最大吞吐量的乘积。将其设置为小于 <code>receive_window</code> 的值有助于避免单个流独占接收缓冲区——若应用程序在一段时间内不读取大流但仍需要其他流上的数据，就可能出现这种情况。</p>'),
    # 5. receive_window
    ('<p>Maximum number of bytes the peer may transmit across all streams of a connection before\nbecoming blocked.</p>\n<p>This should be set to at least the expected connection latency multiplied by the maximum\ndesired throughput. Larger values can be useful to allow maximum throughput within a\nstream while another is blocked.</p>',
     '<p>对端在整个连接的所有流上未被确认即可发送的字节上限，达到此上限后将被阻塞。</p>\n<p>该值至少应设置为预期连接延迟与期望最大吞吐量的乘积。设置为较大的值可以在某个流被阻塞时仍允许其他流达到最大吞吐量。</p>'),
    # 6. send_window
    ('<p>Maximum number of bytes to transmit to a peer without acknowledgment</p>\n<p>Provides an upper bound on memory when communicating with peers that issue large amounts of\nflow control credit. Endpoints that wish to handle large numbers of connections robustly\nshould take care to set this low enough to guarantee memory exhaustion does not occur if\nevery connection uses the entire window.</p>',
     '<p>在对端未确认的情况下可发送的最大字节数</p>\n<p>当与分配大量流控信用额的对端通信时，该设置给出了内存占用的上界。希望稳健处理大量连接的端点应将其设置得足够低，以确保即使每个连接都使用完整窗口也不会出现内存耗尽。</p>'),
    # 7. send_fairness
    ('<p>Whether to implement fair queuing for send streams having the same priority.</p>\n<p>When enabled, connections schedule data from outgoing streams having the same priority in a\nround-robin fashion. When disabled, streams are scheduled in the order they are written to.</p>\n<p>Note that this only affects streams with the same priority. Higher priority streams always\ntake precedence over lower priority streams.</p>\n<p>Disabling fairness can reduce fragmentation and protocol overhead for workloads that use\nmany small streams.</p>',
     '<p>是否对具有相同优先级的发送流实现公平排队。</p>\n<p>启用后，连接会以轮询方式调度相同优先级的各出站流上的数据；禁用时，流将按写入顺序进行调度。</p>\n<p>注意该设置仅影响具有相同优先级的流。较高优先级的流始终优先于较低优先级的流。</p>\n<p>对于使用大量小流的工作负载，禁用公平性可以降低碎片化和协议开销。</p>'),
    # 8. packet_threshold
    ('<p>Maximum reordering in packet number space before FACK style loss detection considers a\npacket lost. Should not be less than 3, per RFC5681.</p>',
     '<p>在 FACK 风格的丢包检测将数据包判定为丢失之前，所允许的包号空间最大重排度。根据 RFC5681，该值不应小于 3。</p>'),
    # 9. time_threshold
    ('<p>Maximum reordering in time space before time based loss detection considers a packet lost,\nas a factor of RTT</p>',
     '<p>在基于时间的丢包检测将数据包判定为丢失之前所允许的时间维最大重排度，以 RTT 的倍数表示</p>'),
    # 10. initial_rtt
    ('<p>The RTT used before an RTT sample is taken</p>',
     '<p>在获得首个 RTT 样本之前所使用的 RTT</p>'),
    # 11. initial_mtu
    ('<p>The initial value to be used as the maximum UDP payload size before running MTU discovery\n(see <a href="struct.TransportConfig.html#method.mtu_discovery_config" title="method quinn::TransportConfig::mtu_discovery_config"><code>TransportConfig::mtu_discovery_config</code></a>).</p>\n<p>Must be at least 1200, which is the default, and known to be safe for typical internet\napplications. Larger values are more efficient, but increase the risk of packet loss due to\nexceeding the network path’s IP MTU. If the provided value is higher than what the network\npath actually supports, packet loss will eventually trigger black hole detection and bring\nit down to <a href="struct.TransportConfig.html#method.min_mtu" title="method quinn::TransportConfig::min_mtu"><code>TransportConfig::min_mtu</code></a>.</p>',
     '<p>在运行 MTU 发现之前（参见 <a href="struct.TransportConfig.html#method.mtu_discovery_config" title="method quinn::TransportConfig::mtu_discovery_config"><code>TransportConfig::mtu_discovery_config</code></a>）使用的 UDP 最大负载初始值。</p>\n<p>该值至少必须为 1200（即默认值），已知对典型互联网应用是安全的。更大的值更高效，但会增加因超过网络路径 IP MTU 而丢包的风险。如果所设值高于网络路径实际支持的值，丢包最终将触发黑洞检测并将其降至 <a href="struct.TransportConfig.html#method.min_mtu" title="method quinn::TransportConfig::min_mtu"><code>TransportConfig::min_mtu</code></a>。</p>'),
    # 12. min_mtu
    ('<p>The maximum UDP payload size guaranteed to be supported by the network.</p>\n<p>Must be at least 1200, which is the default, and lower than or equal to\n<a href="struct.TransportConfig.html#method.initial_mtu" title="method quinn::TransportConfig::initial_mtu"><code>TransportConfig::initial_mtu</code></a>.</p>\n<p>Real-world MTUs can vary according to ISP, VPN, and properties of intermediate network links\noutside of either endpoint’s control. Extreme care should be used when raising this value\noutside of private networks where these factors are fully controlled. If the provided value\nis higher than what the network path actually supports, the result will be unpredictable and\ncatastrophic packet loss, without a possibility of repair. Prefer\n<a href="struct.TransportConfig.html#method.initial_mtu" title="method quinn::TransportConfig::initial_mtu"><code>TransportConfig::initial_mtu</code></a> together with\n<a href="struct.TransportConfig.html#method.mtu_discovery_config" title="method quinn::TransportConfig::mtu_discovery_config"><code>TransportConfig::mtu_discovery_config</code></a> to set a maximum UDP payload size that robustly\nadapts to the network.</p>',
     '<p>网络保证支持的最大 UDP 负载大小。</p>\n<p>至少必须为 1200（即默认值），且应小于等于 <a href="struct.TransportConfig.html#method.initial_mtu" title="method quinn::TransportConfig::initial_mtu"><code>TransportConfig::initial_mtu</code></a>。</p>\n<p>实际 MTU 会因 ISP、VPN 以及两端都无法控制的中转网络链路属性而异。在私网以外、这些因素完全不可控的环境中调高该值必须格外小心。如果所设值高于网络路径实际支持的值，将导致无法预测的灾难性丢包且无法恢复。请优先使用 <a href="struct.TransportConfig.html#method.initial_mtu" title="method quinn::TransportConfig::initial_mtu"><code>TransportConfig::initial_mtu</code></a> 配合 <a href="struct.TransportConfig.html#method.mtu_discovery_config" title="method quinn::TransportConfig::mtu_discovery_config"><code>TransportConfig::mtu_discovery_config</code></a> 来设定一个能稳健适配网络的最大 UDP 负载大小。</p>'),
    # 13. mtu_discovery_config
    ('<p>Specifies the MTU discovery config (see <a href="struct.MtuDiscoveryConfig.html" title="struct quinn::MtuDiscoveryConfig"><code>MtuDiscoveryConfig</code></a> for details).</p>\n<p>Enabled by default.</p>',
     '<p>指定 MTU 发现配置（详见 <a href="struct.MtuDiscoveryConfig.html" title="struct quinn::MtuDiscoveryConfig"><code>MtuDiscoveryConfig</code></a>）。</p>\n<p>默认启用。</p>'),
    # 14. pad_to_mtu
    ('<p>Pad UDP datagrams carrying application data to current maximum UDP payload size</p>\n<p>Disabled by default. UDP datagrams containing loss probes are exempt from padding.</p>\n<p>Enabling this helps mitigate traffic analysis by network observers, but it increases\nbandwidth usage. Without this mitigation precise plain text size of application datagrams as\nwell as the total size of stream write bursts can be inferred by observers under certain\nconditions. This analysis requires either an uncongested connection or application datagrams\ntoo large to be coalesced.</p>',
     '<p>将携带应用层数据的 UDP 数据报填充至当前最大 UDP 负载大小</p>\n<p>默认禁用。包含丢包探测包的 UDP 数据报不受填充影响。</p>\n<p>启用此选项有助于缓解网络观察者的流量分析，但会增加带宽占用。在不启用此缓解措施的情况下，在某些条件下观察者可以推断出应用数据报的精确明文大小以及流写入突发的总大小。这要求要么连接处于非拥塞状态，要么应用数据报过大以至于无法合并。</p>'),
    # 15. ack_frequency_config
    ('<p>Specifies the ACK frequency config (see <a href="struct.AckFrequencyConfig.html" title="struct quinn::AckFrequencyConfig"><code>AckFrequencyConfig</code></a> for details)</p>\n<p>The provided configuration will be ignored if the peer does not support the acknowledgement\nfrequency QUIC extension.</p>\n<p>Defaults to <code>None</code>, which disables controlling the peer’s acknowledgement frequency. Even\nif set to <code>None</code>, the local side still supports the acknowledgement frequency QUIC\nextension and may use it in other ways.</p>',
     '<p>指定 ACK 频率配置（详见 <a href="struct.AckFrequencyConfig.html" title="struct quinn::AckFrequencyConfig"><code>AckFrequencyConfig</code></a>）</p>\n<p>如果对端不支持 ACK 频率 QUIC 扩展，所提供的配置将被忽略。</p>\n<p>默认为 <code>None</code>，表示不控制对端的 ACK 频率。即便设为 <code>None</code>，本地端仍支持 ACK 频率 QUIC 扩展，并可以以其他方式使用它。</p>'),
    # 16. persistent_congestion_threshold
    ('<p>Number of consecutive PTOs after which network is considered to be experiencing persistent congestion.</p>',
     '<p>在网络被认为正在经历持续拥塞之前，连续 PTO（Probe Timeout）的次数。</p>'),
    # 17. keep_alive_interval
    ('<p>Period of inactivity before sending a keep-alive packet</p>\n<p>Keep-alive packets prevent an inactive but otherwise healthy connection from timing out.</p>\n<p><code>None</code> to disable, which is the default. Only one side of any given connection needs keep-alive\nenabled for the connection to be preserved. Must be set lower than the idle_timeout of both\npeers to be effective.</p>',
     '<p>在发送 keep-alive 包之前允许的不活跃时长</p>\n<p>keep-alive 包可以防止一条虽然空闲但本身健康的连接因超时而被关闭。</p>\n<p>设为 <code>None</code> 表示禁用（默认）。对于任意一条连接，只要任一端启用了 keep-alive，该连接就能保持。生效前提是该值必须小于两端 idle_timeout 的较小值。</p>'),
    # 18. crypto_buffer_size
    ('<p>Maximum quantity of out-of-order crypto layer data to buffer</p>',
     '<p>可被缓冲的乱序加密层数据最大数量</p>'),
    # 19. allow_spin
    ('<p>Whether the implementation is permitted to set the spin bit on this connection</p>\n<p>This allows passive observers to easily judge the round trip time of a connection, which can\nbe useful for network administration but sacrifices a small amount of privacy.</p>',
     '<p>是否允许实现在本连接上设置 spin bit</p>\n<p>启用后，被动的网络观察者即可轻松判断连接的往返时延，这对网络管理有用，但会牺牲少量隐私。</p>'),
    # 20. datagram_receive_buffer_size
    ('<p>Maximum number of incoming application datagram bytes to buffer, or None to disable\nincoming datagrams</p>\n<p>The peer is forbidden to send single datagrams larger than this size. If the aggregate size\nof all datagrams that have been received from the peer but not consumed by the application\nexceeds this value, old datagrams are dropped until it is no longer exceeded.</p>',
     '<p>入站应用层数据报可缓冲的最大字节数；设为 None 则禁收入站数据报</p>\n<p>对端被禁止发送大于此值的单个数据报。若对端发来但应用层尚未消费的所有数据报总大小超过此值，则旧的数据报将被丢弃，直到不再超过为止。</p>'),
    # 21. datagram_send_buffer_size
    ('<p>Maximum number of outgoing application datagram bytes to buffer</p>\n<p>While datagrams are sent ASAP, it is possible for an application to generate data faster\nthan the link, or even the underlying hardware, can transmit them. This limits the amount of\nmemory that may be consumed in that case. When the send buffer is full and a new datagram is\nsent, older datagrams are dropped until sufficient space is available.</p>',
     '<p>出站应用层数据报可缓冲的最大字节数</p>\n<p>虽然数据报会尽快发出，但应用生成数据的速度仍可能超过链路甚至底层硬件的发送能力。该设置限制了这种情况下可能消耗的内存量。当发送缓冲区已满又要发送新数据报时，旧的数据报将被丢弃，直到腾出足够的空间。</p>'),
    # 22. congestion_controller_factory
    ('<p>How to construct new <code>congestion::Controller</code>s</p>\n<p>Typically the refcounted configuration of a <code>congestion::Controller</code>,\ne.g. a <code>congestion::NewRenoConfig</code>.</p>',
     '<p>如何构造新的 <code>congestion::Controller</code></p>\n<p>通常为某个 <code>congestion::Controller</code> 的引用计数化配置，例如 <code>congestion::NewRenoConfig</code>。</p>'),
    # 23. enable_segmentation_offload
    ('<p>Whether to use “Generic Segmentation Offload” to accelerate transmits, when supported by the\nenvironment</p>\n<p>Defaults to <code>true</code>.</p>\n<p>GSO dramatically reduces CPU consumption when sending large numbers of packets with the same\nheaders, such as when transmitting bulk data on a connection. However, it is not supported\nby all network interface drivers or packet inspection tools. <code>quinn-udp</code> will attempt to\ndisable GSO automatically when unavailable, but this can lead to spurious packet loss at\nstartup, temporarily degrading performance.</p>',
     '<p>当运行环境支持时，是否启用“Generic Segmentation Offload”来加速发送</p>\n<p>默认为 <code>true</code>。</p>\n<p>在发送大量具有相同包头的数据包（例如在一条连接上传输大批量数据）时，GSO 可以显著降低 CPU 占用。但并非所有网卡驱动或抓包工具都支持。当不可用时，<code>quinn-udp</code> 会尝试自动关闭 GSO，但这可能在启动时引入偶发丢包，使性能暂时下降。</p>'),
    # 24. From impl
    ('<p>Returns the argument unchanged.</p>',
     '<p>原样返回该参数。</p>'),
    # 25. From impl
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
