"""Round 5: Translate remaining top-doc paragraphs with embedded <a href>."""
import os
import re

BASE = 'D:/Administrator/Documents/Code/rust_doc_all/rcgen'

JOBS = [
    # ----- enum.ExtendedKeyUsagePurpose.html -----
    (
        'enum.ExtendedKeyUsagePurpose.html',
        [
            ('<p>One of the purposes contained in the <a href="https://tools.ietf.org/html/rfc5280#section-4.2.1.12">extended key usage extension</a></p>',
             '<p>extended key usage 扩展中包含的某个用途，参见 <a href="https://tools.ietf.org/html/rfc5280#section-4.2.1.12">RFC 5280 §4.2.1.12</a></p>'),
        ],
    ),
    # ----- enum.GeneralSubtree.html -----
    (
        'enum.GeneralSubtree.html',
        [
            ('<p>This type has similarities to the <a href="enum.SanType.html" title="enum rcgen::SanType"><code>SanType</code></a> enum but is not equal.\r\n'
             'For example, <code>GeneralSubtree</code> has CIDR subnets for ip addresses\r\n'
             'while <a href="enum.SanType.html" title="enum rcgen::SanType"><code>SanType</code></a> has IP addresses.</p>',
             '<p>该类型与 <a href="enum.SanType.html" title="enum rcgen::SanType"><code>SanType</code></a> 枚举相似但并不相同。\n'
             '例如，<code>GeneralSubtree</code> 中的 IP 地址是 CIDR 子网形式，\n'
             '而 <a href="enum.SanType.html" title="enum rcgen::SanType"><code>SanType</code></a> 中则是纯 IP 地址形式。</p>'),
        ],
    ),
    # ----- enum.KeyIdMethod.html -----
    (
        'enum.KeyIdMethod.html',
        [
            ('<p>Key identifiers should be derived from the public key data. <a href="https://www.rfc-editor.org/rfc/rfc7093">RFC 7093</a> defines\r\n'
             'three methods to do so using a choice of SHA256 (method 1), SHA384 (method 2), or SHA512\r\n'
             '(method 3). In each case the first 160 bits of the hash are used as the key identifier\r\n'
             'to match the output length that would be produced were SHA1 used (a legacy option defined in RFC 5280).</p>',
             '<p>密钥标识符应从公钥数据派生。<a href="https://www.rfc-editor.org/rfc/rfc7093">RFC 7093</a> 规定了三种实现方式：\n'
             '分别使用 SHA256（方法 1）、SHA384（方法 2）或 SHA512（方法 3）。\n'
             '在每种情况下，均取哈希值的前 160 位作为密钥标识符，\n'
             '以匹配使用 SHA1（RFC 5280 中定义的遗留选项）时所产生输出的长度。</p>'),
            ('<p>In addition to the RFC 7093 mechanisms, rcgen supports using a pre-specified key identifier.\r\n'
             'This can be helpful when working with an existing <code>Certificate</code>.</p>',
             '<p>除 RFC 7093 规定的机制外，rcgen 还支持使用预先指定的密钥标识符，\n'
             '这在与现有的 <code>Certificate</code> 协作时尤为便利。</p>'),
        ],
    ),
    # ----- enum.KeyUsagePurpose.html -----
    (
        'enum.KeyUsagePurpose.html',
        [
            ('<p>One of the purposes contained in the <a href="https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.1.3">key usage</a> extension</p>',
             '<p>key usage 扩展中包含的某个用途，参见 <a href="https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.1.3">RFC 5280 §4.2.1.3</a></p>'),
        ],
    ),
    # ----- enum.OtherNameValue.html -----
    (
        'enum.OtherNameValue.html',
        [
            # RFC 5280 + NBSP + 4.1.2.4
            ('<p>An <code>OtherName</code> value, defined in <a href="https://datatracker.ietf.org/doc/html/rfc5280#section-4.1.2.4">RFC 5280 §4.1.2.4</a>.</p>',
             '<p>一个 <code>OtherName</code> 值，定义见 <a href="https://datatracker.ietf.org/doc/html/rfc5280#section-4.1.2.4">RFC 5280 §4.1.2.4</a>。</p>'),
        ],
    ),
    # ----- enum.RevocationReason.html -----
    (
        'enum.RevocationReason.html',
        [
            ('<p>Identifies the reason a certificate was revoked.\r\n'
             'See <a href="https://www.rfc-editor.org/rfc/rfc5280#section-5.3.1">RFC 5280 §5.3.1</a></p>',
             '<p>指明证书被吊销的原因。\n'
             '参见 <a href="https://www.rfc-editor.org/rfc/rfc5280#section-5.3.1">RFC 5280 §5.3.1</a></p>'),
        ],
    ),
    # ----- index.html (3rd paragraph of top docblock) -----
    (
        'index.html',
        [
            ('<p>The most simple way of using this crate is by calling the\r\n'
             '<a href="fn.generate_simple_self_signed.html" title="fn rcgen::generate_simple_self_signed"><code>generate_simple_self_signed</code></a> function.\r\n'
             'For more customization abilities, construct a <a href="struct.CertificateParams.html" title="struct rcgen::CertificateParams"><code>CertificateParams</code></a> and\r\n'
             'a key pair to call <a href="struct.CertificateParams.html#method.signed_by" title="method rcgen::CertificateParams::signed_by"><code>CertificateParams::signed_by()</code></a> or\r\n'
             '<a href="struct.CertificateParams.html#method.self_signed" title="method rcgen::CertificateParams::self_signed"><code>CertificateParams::self_signed()</code></a>.</p>',
             '<p>使用本 crate 最简单的方式是调用 <a href="fn.generate_simple_self_signed.html" title="fn rcgen::generate_simple_self_signed"><code>generate_simple_self_signed</code></a> 函数。\n'
             '如果需要更强的定制能力，可以构造一个 <a href="struct.CertificateParams.html" title="struct rcgen::CertificateParams"><code>CertificateParams</code></a> 与一个密钥对，\n'
             '然后调用 <a href="struct.CertificateParams.html#method.signed_by" title="method rcgen::CertificateParams::signed_by"><code>CertificateParams::signed_by()</code></a> 或\n'
             '<a href="struct.CertificateParams.html#method.self_signed" title="method rcgen::CertificateParams::self_signed"><code>CertificateParams::self_signed()</code></a>。</p>'),
        ],
    ),
    # ----- static.PKCS_* -----
    (
        'static.PKCS_ECDSA_P256_SHA256.html',
        [
            ('<p>ECDSA signing using the P-256 curves and SHA-256 hashing as per <a href="https://tools.ietf.org/html/rfc5758#section-3.2">RFC 5758</a></p>',
             '<p>使用 P-256 曲线的 ECDSA 签名以及 SHA-256 杂凑，参见 <a href="https://tools.ietf.org/html/rfc5758#section-3.2">RFC 5758 §3.2</a></p>'),
        ],
    ),
    (
        'static.PKCS_ECDSA_P384_SHA384.html',
        [
            ('<p>ECDSA signing using the P-384 curves and SHA-384 hashing as per <a href="https://tools.ietf.org/html/rfc5758#section-3.2">RFC 5758</a></p>',
             '<p>使用 P-384 曲线的 ECDSA 签名以及 SHA-384 杂凑，参见 <a href="https://tools.ietf.org/html/rfc5758#section-3.2">RFC 5758 §3.2</a></p>'),
        ],
    ),
    (
        'static.PKCS_ED25519.html',
        [
            ('<p>ED25519 curve signing as per <a href="https://tools.ietf.org/html/rfc8410">RFC 8410</a></p>',
             '<p>ED25519 曲线签名，参见 <a href="https://tools.ietf.org/html/rfc8410">RFC 8410</a></p>'),
        ],
    ),
    (
        'static.PKCS_RSA_SHA256.html',
        [
            ('<p>RSA signing with PKCS#1 1.5 padding and SHA-256 hashing as per <a href="https://tools.ietf.org/html/rfc4055">RFC 4055</a></p>',
             '<p>使用 PKCS#1 1.5 填充与 SHA-256 杂凑的 RSA 签名，参见 <a href="https://tools.ietf.org/html/rfc4055">RFC 4055</a></p>'),
        ],
    ),
    (
        'static.PKCS_RSA_SHA384.html',
        [
            ('<p>RSA signing with PKCS#1 1.5 padding and SHA-384 hashing as per <a href="https://tools.ietf.org/html/rfc4055">RFC 4055</a></p>',
             '<p>使用 PKCS#1 1.5 填充与 SHA-384 杂凑的 RSA 签名，参见 <a href="https://tools.ietf.org/html/rfc4055">RFC 4055</a></p>'),
        ],
    ),
    (
        'static.PKCS_RSA_SHA512.html',
        [
            ('<p>RSA signing with PKCS#1 1.5 padding and SHA-512 hashing as per <a href="https://tools.ietf.org/html/rfc4055">RFC 4055</a></p>',
             '<p>使用 PKCS#1 1.5 填充与 SHA-512 杂凑的 RSA 签名，参见 <a href="https://tools.ietf.org/html/rfc4055">RFC 4055</a></p>'),
        ],
    ),
    # ----- struct.Attribute.html -----
    (
        'struct.Attribute.html',
        [
            ('<p>A PKCS #10 CSR attribute, as defined in <a href="https://datatracker.ietf.org/doc/html/rfc5280#appendix-A.1">RFC 5280</a> and constrained\r\n'
             'by <a href="https://datatracker.ietf.org/doc/html/rfc2986#section-4">RFC 2986</a>.</p>',
             '<p>一个 PKCS #10 CSR 属性，定义见 <a href="https://datatracker.ietf.org/doc/html/rfc5280#appendix-A.1">RFC 5280</a>，\n'
             '并由 <a href="https://datatracker.ietf.org/doc/html/rfc2986#section-4">RFC 2986</a> 加以约束。</p>'),
        ],
    ),
    # ----- struct.CrlDistributionPoint.html -----
    (
        'struct.CrlDistributionPoint.html',
        [
            ('<p>A certificate revocation list (CRL) distribution point, to be included in a certificate’s\r\n'
             '<a href="https://www.rfc-editor.org/rfc/rfc5280#section-4.2.1.13">distribution points extension</a> or\r\n'
             'a CRL’s <a href="https://datatracker.ietf.org/doc/html/rfc5280#section-5.2.5">issuing distribution point extension</a></p>',
             '<p>一个证书吊销列表（CRL）分发点，可包含在证书的 <a href="https://www.rfc-editor.org/rfc/rfc5280#section-4.2.1.13">distribution points extension</a> 或\n'
             'CRL 的 <a href="https://datatracker.ietf.org/doc/html/rfc5280#section-5.2.5">issuing distribution point extension</a> 扩展中</p>'),
        ],
    ),
    # ----- struct.CrlIssuingDistributionPoint.html -----
    (
        'struct.CrlIssuingDistributionPoint.html',
        [
            ('<p>A certificate revocation list (CRL) issuing distribution point, to be included in a CRL’s\r\n'
             '<a href="https://datatracker.ietf.org/doc/html/rfc5280#section-5.2.5">issuing distribution point extension</a>.</p>',
             '<p>一个证书吊销列表（CRL）颁发分发点，包含在 CRL 的 <a href="https://datatracker.ietf.org/doc/html/rfc5280#section-5.2.5">issuing distribution point extension</a> 扩展中。</p>'),
        ],
    ),
    # ----- struct.DistinguishedName.html -----
    (
        'struct.DistinguishedName.html',
        [
            ('<p>See also the RFC 5280 sections on the <a href="https://tools.ietf.org/html/rfc5280#section-4.1.2.4">issuer</a>\r\n'
             'and <a href="https://tools.ietf.org/html/rfc5280#section-4.1.2.6">subject</a> fields.</p>',
             '<p>另请参阅 RFC 5280 中有关 <a href="https://tools.ietf.org/html/rfc5280#section-4.1.2.4">issuer</a> 与\n'
             '<a href="https://tools.ietf.org/html/rfc5280#section-4.1.2.6">subject</a> 字段的小节。</p>'),
        ],
    ),
    # ----- struct.NameConstraints.html -----
    (
        'struct.NameConstraints.html',
        [
            ('<p>The <a href="https://tools.ietf.org/html/rfc5280#section-4.2.1.10">NameConstraints extension</a>\r\n'
             '(only relevant for CA certificates)</p>',
             '<p><a href="https://tools.ietf.org/html/rfc5280#section-4.2.1.10">NameConstraints 扩展</a>\n'
             '（仅对 CA 证书有意义）</p>'),
        ],
    ),
    # ----- string/struct.BmpString.html -----
    (
        'string/struct.BmpString.html',
        [
            ('<p>ASN.1 <code>BMPString</code> type.</p>',
             '<p>ASN.1 <code>BMPString</code> 类型。</p>'),
            ('<p>You can create a <code>BmpString</code> from <a href="https://doc.rust-lang.org/1.95.0/std/primitive.str.html" title="primitive str">a literal string</a> with <a href="struct.BmpString.html#method.try_from" title="associated function rcgen::string::BmpString::try_from"><code>BmpString::try_from</code></a>:</p>',
             '<p>你可以使用 <a href="struct.BmpString.html#method.try_from" title="associated function rcgen::string::BmpString::try_from"><code>BmpString::try_from</code></a> 从 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.str.html" title="primitive str">字符串字面量</a> 创建一个 <code>BmpString</code>：</p>'),
            ('<p><code>BMPString</code> is included for backward compatibility, <a href="https://datatracker.ietf.org/doc/html/rfc5280#page-25">RFC 5280</a> say it\r\n'
             'SHOULD NOT be used for certificates for new subjects.</p>',
             '<p>之所以保留 <code>BMPString</code> 仅为向后兼容，<a href="https://datatracker.ietf.org/doc/html/rfc5280#page-25">RFC 5280</a> 建议不要将其用于新主体的证书。</p>'),
            ('<p>The inverse of this method is <a href="struct.BmpString.html#method.from_utf16be" title="associated function rcgen::string::BmpString::from_utf16be"><code>from_utf16be</code></a>.</p>',
             '<p>本方法的反操作是 <a href="struct.BmpString.html#method.from_utf16be" title="associated function rcgen::string::BmpString::from_utf16be"><code>from_utf16be</code></a>。</p>'),
            ('<p>Parsing a <code>BmpString</code> allocates memory since the UTF-8 to UTF-16 conversion requires a memory allocation.</p>',
             '<p>解析 <code>BmpString</code> 时会进行内存分配，因为 UTF-8 到 UTF-16 的转换需要一次内存分配。</p>'),
        ],
    ),
]


def main():
    total_files = 0
    total_found = 0
    total_missed = 0
    for rel, pairs in JOBS:
        path = os.path.join(BASE, rel)
        if not os.path.exists(path):
            print(f'  MISSING file: {rel}')
            total_missed += len(pairs)
            continue
        with open(path, 'rb') as f:
            raw = f.read()
        orig = raw
        n_this = 0
        for old, new in pairs:
            old_b = old.encode('utf-8')
            new_b = new.encode('utf-8')
            if old_b in raw:
                raw = raw.replace(old_b, new_b)
                total_found += 1
                n_this += 1
            else:
                total_missed += 1
                preview = old_b[:120].decode('utf-8', errors='replace')
                print(f'  MISSED {rel}: {preview!r}')
        if raw != orig:
            with open(path, 'wb') as f:
                f.write(raw)
            total_files += 1
            text = raw.decode('utf-8', errors='replace')
            cjk = re.findall(r'[一-鿿]', text)
            print(f'  {rel}: {n_this} pairs, CJK={len(cjk)}')
    print(f'Updated {total_files} files; {total_found} found, {total_missed} missed')


if __name__ == '__main__':
    main()
