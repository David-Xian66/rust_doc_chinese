"""Translate all 29 untranslated docblocks in quinn/crypto/rustls/enum.Error.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/crypto/rustls/enum.Error.html'

TRANSLATIONS = [
    # 1. non-exhaustive note
    ('Non-exhaustive enums could have additional variants added in future. Therefore, when matching against variants of non-exhaustive enums, an extra wildcard arm must be added to account for any future variants.',
     '非穷尽枚举将来可能添加额外的变体。因此，在对非穷尽枚举的变体进行模式匹配时，必须额外添加一个通配分支以容纳未来可能新增的变体。'),
    # 2. InappropriateMessage
    ('<p>We received a TLS message that isn’t valid right now.\n<code>expect_types</code> lists the message types we can expect right now.\n<code>got_type</code> is the type we found.  This error is typically\ncaused by a buggy TLS stack (the peer or this one), a broken\nnetwork, or an attack.</p>',
     '<p>我们收到了此刻并不合法的 TLS 消息。<code>expect_types</code> 列出当前阶段预期可能出现的消息类型；<code>got_type</code> 则是我们实际收到的类型。此错误通常由 TLS 协议栈存在 bug（对端或本端）、网络故障或攻击所致。</p>'),
    # 3. expect_types field
    ('<p>Which types we expected</p>',
     '<p>我们预期收到的类型</p>'),
    # 4. got_type field (used twice, but with different context)
    ('<p>What type we received</p>',
     '<p>我们实际收到的类型</p>'),
    # 5. InappropriateHandshakeMessage
    ('<p>We received a TLS handshake message that isn’t valid right now.\n<code>expect_types</code> lists the handshake message types we can expect\nright now.  <code>got_type</code> is the type we found.</p>',
     '<p>我们收到了此刻并不合法的 TLS 握手消息。<code>expect_types</code> 列出当前阶段预期可能出现的握手消息类型；<code>got_type</code> 则是我们实际收到的类型。</p>'),
    # 6. expect_types handshake
    ('<p>Which handshake type we expected</p>',
     '<p>我们预期收到的握手消息类型</p>'),
    # 7. got_type handshake
    ('<p>What handshake type we received</p>',
     '<p>我们实际收到的握手消息类型</p>'),
    # 8. InvalidEncryptedClientHello
    ('<p>An error occurred while handling Encrypted Client Hello (ECH).</p>',
     '<p>处理 ECH（Encrypted Client Hello）时发生错误。</p>'),
    # 9. InvalidMessage
    ('<p>The peer sent us a TLS message with invalid contents.</p>',
     '<p>对端发来了内容非法的 TLS 消息。</p>'),
    # 10. NoCertificatesPresented
    ('<p>The peer didn’t give us any certificates.</p>',
     '<p>对端未提供任何证书。</p>'),
    # 11. UnsupportedNameType
    ('<p>The certificate verifier doesn’t support the given type of name.</p>',
     '<p>证书验证器不支持所给名称的类型。</p>'),
    # 12. DecryptError
    ('<p>We couldn’t decrypt a message.  This is invariably fatal.</p>',
     '<p>无法解密某条消息。此错误总是致命的。</p>'),
    # 13. EncryptError
    ('<p>We couldn’t encrypt a message because it was larger than the allowed message size.\nThis should never happen if the application is using valid record sizes.</p>',
     '<p>由于消息大小超过允许上限，我们无法对其进行加密。只要应用程序使用了合法的记录大小，此错误就绝不会发生。</p>'),
    # 14. PeerIncompatible
    ('<p>The peer doesn’t support a protocol version/feature we require.\nThe parameter gives a hint as to what version/feature it is.</p>',
     '<p>对端不支持我们所需的某个协议版本或特性。参数给出具体是哪个版本或特性的提示。</p>'),
    # 15. PeerMisbehaved
    ('<p>The peer deviated from the standard TLS protocol.\nThe parameter gives a hint where.</p>',
     '<p>对端偏离了标准 TLS 协议。参数给出偏差位置的提示。</p>'),
    # 16. AlertReceived
    ('<p>We received a fatal alert.  This means the peer is unhappy.</p>',
     '<p>我们收到了致命告警。这表示对端不满意。</p>'),
    # 17. InvalidCertificate
    ('<p>We saw an invalid certificate.</p>\n<p>The contained error is from the certificate validation trait\nimplementation.</p>',
     '<p>发现了一张非法证书。</p>\n<p>其中包含的错误来自证书验证 trait 的实现。</p>'),
    # 18. InvalidCertRevocationList
    ('<p>A provided certificate revocation list (CRL) was invalid.</p>',
     '<p>所提供的证书吊销列表（CRL）无效。</p>'),
    # 19. General
    ('<p>A catch-all error for unlikely errors.</p>',
     '<p>用于兜底处理不太可能出现的错误。</p>'),
    # 20. FailedToGetCurrentTime
    ('<p>We failed to figure out what time it currently is.</p>',
     '<p>无法获取当前时间。</p>'),
    # 21. FailedToGetRandomBytes
    ('<p>We failed to acquire random bytes from the system.</p>',
     '<p>无法从系统获取随机字节。</p>'),
    # 22. HandshakeNotComplete
    ('<p>This function doesn’t work until the TLS handshake\nis complete.</p>',
     '<p>在 TLS 握手完成之前，该函数无法使用。</p>'),
    # 23. PeerSentOversizedRecord
    ('<p>The peer sent an oversized record/fragment.</p>',
     '<p>对端发送了过大的记录或分片。</p>'),
    # 24. NoApplicationProtocol
    ('<p>An incoming connection did not support any known application protocol.</p>',
     '<p>入站连接不支持任何已知的应用层协议。</p>'),
    # 25. BadMaxFragmentSize
    ('<p>The <code>max_fragment_size</code> value supplied in configuration was too small,\nor too large.</p>',
     '<p>配置中提供的 <code>max_fragment_size</code> 值过小或过大。</p>'),
    # 26. InconsistentKeys
    ('<p>Specific failure cases from <a href="../../../rustls/crypto/signer/struct.CertifiedKey.html#method.keys_match" title="method rustls::crypto::signer::CertifiedKey::keys_match"><code>keys_match</code></a> or a <a href="../../../rustls/crypto/signer/trait.SigningKey.html" title="trait rustls::crypto::signer::SigningKey"><code>crate::crypto::signer::SigningKey</code></a> that cannot produce a corresponding public key.</p>',
     '<p>来自 <a href="../../../rustls/crypto/signer/struct.CertifiedKey.html#method.keys_match" title="method rustls::crypto::signer::CertifiedKey::keys_match"><code>keys_match</code></a> 或无法产生对应公钥的 <a href="../../../rustls/crypto/signer/trait.SigningKey.html" title="trait rustls::crypto::signer::SigningKey"><code>crate::crypto::signer::SigningKey</code></a> 的特定失败情形。</p>'),
    # 27. Other
    ('<p>Any other error.</p>\n<p>This variant should only be used when the error is not better described by a more\nspecific variant. For example, if a custom crypto provider returns a\nprovider specific error.</p>\n<p>Enums holding this variant will never compare equal to each other.</p>',
     '<p>任何其他错误。</p>\n<p>此变体应仅在错误无法被更具体的变体准确描述时使用。例如，自定义加密提供者返回的特定错误。</p>\n<p>持有此变体的枚举值之间永远不会判等。</p>'),
    # 28. From impl
    ('</h4></section></summary><div class="docblock"><p>Returns the argument unchanged.</p>',
     '</h4></section></summary><div class="docblock"><p>原样返回该参数。</p>'),
    # 29. From boilerplate
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