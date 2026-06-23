"""Translate 5 untranslated docblocks in quinn/struct.AckFrequencyConfig.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/struct.AckFrequencyConfig.html'

TRANSLATIONS = [
    ('<p>The ack-eliciting threshold we will request the peer to use</p>\n<p>This threshold represents the number of ack-eliciting packets an endpoint may receive\nwithout immediately sending an ACK.</p>\n<p>The remote peer should send at least one ACK frame when more than this number of\nack-eliciting packets have been received. A value of 0 results in a receiver immediately\nacknowledging every ack-eliciting packet.</p>\n<p>Defaults to 1, which sends ACK frames for every other ack-eliciting packet.</p>',
     '<p>我们将请求对端使用的“可触发 ACK”阈值</p>\n<p>该阈值表示一个端点在不立即发送 ACK 的情况下，最多可接收的“可触发 ACK”包数量。</p>\n<p>对端在收到的“可触发 ACK”包数量超过该阈值时，至少应发送一个 ACK 帧。值为 0 时，接收方会对每一个“可触发 ACK”包立即确认。</p>\n<p>默认为 1，表示每隔一个“可触发 ACK”包发送 ACK 帧。</p>'),
    ('<p>The <code>max_ack_delay</code> we will request the peer to use</p>\n<p>This parameter represents the maximum amount of time that an endpoint waits before sending\nan ACK when the ack-eliciting threshold hasn’t been reached.</p>\n<p>The effective <code>max_ack_delay</code> will be clamped to be at least the peer’s <code>min_ack_delay</code>\ntransport parameter, and at most the greater of the current path RTT or 25ms.</p>\n<p>Defaults to <code>None</code>, in which case the peer’s original <code>max_ack_delay</code> will be used, as\nobtained from its transport parameters.</p>',
     '<p>我们将请求对端使用的 <code>max_ack_delay</code></p>\n<p>该参数表示当“可触发 ACK”阈值尚未达到时，端点在发送 ACK 之前最多等待的时间。</p>\n<p>实际生效的 <code>max_ack_delay</code> 会被裁剪：下限为对端的 <code>min_ack_delay</code> 传输参数，上限为当前路径 RTT 与 25ms 中的较大者。</p>\n<p>默认为 <code>None</code>，此时将使用对端传输参数中所声明的原始 <code>max_ack_delay</code>。</p>'),
    ('<p>The reordering threshold we will request the peer to use</p>\n<p>This threshold represents the amount of out-of-order packets that will trigger an endpoint\nto send an ACK, without waiting for <code>ack_eliciting_threshold</code> to be exceeded or for\n<code>max_ack_delay</code> to be elapsed.</p>\n<p>A value of 0 indicates out-of-order packets do not elicit an immediate ACK. A value of 1\nimmediately acknowledges any packets that are received out of order (this is also the\nbehavior when the extension is disabled).</p>\n<p>It is recommended to set this value to <a href="struct.TransportConfig.html#method.packet_threshold" title="method quinn::TransportConfig::packet_threshold"><code>TransportConfig::packet_threshold</code></a> minus one.\nSince the default value for <a href="struct.TransportConfig.html#method.packet_threshold" title="method quinn::TransportConfig::packet_threshold"><code>TransportConfig::packet_threshold</code></a> is 3, this value defaults\nto 2.</p>',
     '<p>我们将请求对端使用的乱序阈值</p>\n<p>该阈值表示在不等待 <code>ack_eliciting_threshold</code> 达到上限或 <code>max_ack_delay</code> 超时的情况下，触发端点立即发送 ACK 的乱序包数量。</p>\n<p>值为 0 表示乱序包不会触发立即 ACK；值为 1 则对每一个乱序到达的包立即确认（这也是禁用此扩展时的行为）。</p>\n<p>建议将该值设置为 <a href="struct.TransportConfig.html#method.packet_threshold" title="method quinn::TransportConfig::packet_threshold"><code>TransportConfig::packet_threshold</code></a> 减一。由于 <a href="struct.TransportConfig.html#method.packet_threshold" title="method quinn::TransportConfig::packet_threshold"><code>TransportConfig::packet_threshold</code></a> 的默认值为 3，因此该值默认为 2。</p>'),
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