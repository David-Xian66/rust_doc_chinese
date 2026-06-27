"""Round 4: Translate remaining untranslated docblocks with proper Unicode chars."""
import os
import re

BASE = 'D:/Administrator/Documents/Code/rust_doc_all/rcgen'

# All Unicode chars: ' ' ' – – ' — ' """' '' ¶ §

JOBS = [
    # ----- enum.BasicConstraints.html: top docblock -----
    (
        'enum.BasicConstraints.html',
        [
            ('<p>The path length constraint (only relevant for CA certificates)</p>',
             '<p>路径长度约束（仅对 CA 证书有意义）</p>'),
            ('<p>Sets an optional upper limit on the length of the intermediate certificate chain\r\n'
             'length allowed for this CA certificate (not including the end entity certificate).</p>',
             '<p>设置一个可选的上限，以限制允许使用的中间证书链路长度（不包括终端实体证书）。</p>'),
        ],
    ),
    # ----- enum.CidrSubnet.html -----
    (
        'enum.CidrSubnet.html',
        [
            ('<p>CIDR subnet, as per <a href="https://tools.ietf.org/html/rfc4632">RFC 4632</a></p>',
             '<p>CIDR 子网，遵循 <a href="https://tools.ietf.org/html/rfc4632">RFC 4632</a> 的规定</p>'),
            ('<p>You might know CIDR subnets better by their textual representation\r\n'
             'where they consist of an ip address followed by a slash and a prefix\r\n'
             'number, for example <code>192.168.99.0/24</code>.</p>',
             '<p>你可能更熟悉 CIDR 子网的文本表示形式：由一个 IP 地址后接斜杠与一个前缀数字组成，\n'
             '例如 <code>192.168.99.0/24</code>。</p>'),
            ('<p>The first field in the enum is the address, the second is the mask.\r\n'
             'Both are specified in network byte order.</p>',
             '<p>枚举的第一个字段是地址，第二个字段是掩码。两者均以网络字节序表示。</p>'),
            ('<p>Obtains the CidrSubnet from an ip address\r\n'
             'as well as the specified prefix number.</p>',
             '<p>从一个 IP 地址与指定的前缀长度构造 <code>CidrSubnet</code>。</p>'),
            ('<p>Obtains the CidrSubnet from an IPv4 address in network byte order\r\n'
             'as well as the specified prefix.</p>',
             '<p>从一个以网络字节序表示的 IPv4 地址与指定的前缀长度构造 <code>CidrSubnet</code>。</p>'),
            ('<p>Obtains the CidrSubnet from an IPv6 address in network byte order\r\n'
             'as well as the specified prefix.</p>',
             '<p>从一个以网络字节序表示的 IPv6 地址与指定的前缀长度构造 <code>CidrSubnet</code>。</p>'),
            ('<p>Obtains the CidrSubnet from the well-known\r\n'
             'addr/prefix notation.</p>',
             '<p>从常见的 addr/prefix 表示法构造 <code>CidrSubnet</code>。</p>'),
        ],
    ),
    # ----- enum.ExtendedKeyUsagePurpose.html -----
    (
        'enum.ExtendedKeyUsagePurpose.html',
        [
            ('<p>One of the purposes contained in the extended key usage extension</p>',
             '<p>extended key usage 扩展中包含的某个用途</p>'),
        ],
    ),
    # ----- enum.GeneralSubtree.html -----
    (
        'enum.GeneralSubtree.html',
        [
            ('<p>General Subtree type.</p>',
             '<p>General Subtree（通用子树）类型。</p>'),
            ('<p>This type has similarities to the SanType enum but is not equal.\r\n'
             'For example, GeneralSubtree has CIDR subnets for ip addresses\r\n'
             'while SanType has IP addresses.</p>',
             '<p>该类型与 <code>SanType</code> 枚举相似但并不相同。\n'
             '例如，<code>GeneralSubtree</code> 中的 IP 地址是 CIDR 子网形式，而 <code>SanType</code> 中则是纯 IP 地址形式。</p>'),
            ('<p>Also known as E-Mail address</p>',
             '<p>也称为电子邮件地址</p>'),
        ],
    ),
    # ----- enum.KeyIdMethod.html -----
    (
        'enum.KeyIdMethod.html',
        [
            ('<p>Method to generate key identifiers from public keys.</p>',
             '<p>从公钥生成密钥标识符（Key Identifier）的方法。</p>'),
            ('<p>Key identifiers should be derived from the public key data. RFC 7093 defines\r\n'
             'three methods to do so using a choice of SHA256 (method 1), SHA384 (method 2), or SHA512\r\n'
             '(method 3). In each case the first 160 bits of the hash are used as the key identifier\r\n'
             'to match the output length that would be produced were SHA1 used (a legacy option defined in RFC 5280).\r\n'
             'In addition to the RFC 7093 mechanisms, rcgen supports using a pre-specified key identifier.\r\n'
             'This can be helpful when working with an existing <a href="struct.Certificate.html" title="struct rcgen::Certificate"><code>Certificate</code></a>.</p>',
             '<p>密钥标识符应从公钥数据派生。RFC 7093 规定了三种实现方式：分别使用 SHA256（方法 1）、\n'
             'SHA384（方法 2）或 SHA512（方法 3）。在每种情况下，均取哈希值的前 160 位作为密钥标识符，\n'
             '以匹配使用 SHA1（RFC 5280 中定义的遗留选项）时所产生输出的长度。\n'
             '除 RFC 7093 规定的机制外，rcgen 还支持使用预先指定的密钥标识符，\n'
             '这在与现有的 <a href="struct.Certificate.html" title="struct rcgen::Certificate"><code>Certificate</code></a> 协作时尤为便利。</p>'),
            ('<p>RFC 7093 method 1 - a truncated SHA256 digest.</p>',
             '<p>RFC 7093 方法 1 —— 截取的 SHA256 摘要。</p>'),
            ('<p>RFC 7093 method 2 - a truncated SHA384 digest.</p>',
             '<p>RFC 7093 方法 2 —— 截取的 SHA384 摘要。</p>'),
            ('<p>RFC 7093 method 3 - a truncated SHA512 digest.</p>',
             '<p>RFC 7093 方法 3 —— 截取的 SHA512 摘要。</p>'),
            ('<p>Pre-specified identifier. The exact given value is used as the key identifier.</p>',
             '<p>预先指定的标识符。直接使用给定的值作为密钥标识符。</p>'),
        ],
    ),
    # ----- enum.KeyUsagePurpose.html -----
    (
        'enum.KeyUsagePurpose.html',
        [
            ('<p>One of the purposes contained in the key usage extension</p>',
             '<p>key usage 扩展中包含的某个用途</p>'),
        ],
    ),
    # ----- enum.OtherNameValue.html -----
    (
        'enum.OtherNameValue.html',
        [
            ('<p>An OtherName value, defined in RFC 5280§4.1.2.4.</p>',
             '<p>一个 OtherName 值，定义见 RFC 5280 §4.1.2.4。</p>'),
            ('<p>While the standard specifies this could be any ASN.1 type rcgen limits\r\n'
             'the value to a UTF-8 encoded string as this will cover the most common\r\n'
             'use cases, for instance smart card user principal names (UPN).</p>',
             '<p>尽管标准规定它可以是任意 ASN.1 类型，rcgen 将其值限定为 UTF-8 编码的字符串，\n'
             '因为这已能覆盖最常见的用例，例如智能卡用户主体名称（UPN）。</p>'),
        ],
    ),
    # ----- enum.RevocationReason.html -----
    (
        'enum.RevocationReason.html',
        [
            ('<p>Identifies the reason a certificate was revoked. See RFC 5280 §5.3.1</p>',
             '<p>指明证书被吊销的原因。参见 RFC 5280 §5.3.1</p>'),
        ],
    ),
    # ----- enum.IsCa.html -----
    (
        'enum.IsCa.html',
        [
            ('<p>Whether the certificate is allowed to sign other certificates</p>',
             '<p>该证书是否允许对其他证书进行签名</p>'),
        ],
    ),
    # ----- enum.CrlScope.html -----
    (
        'enum.CrlScope.html',
        [
            ('<p>Describes the scope of a CRL for an issuing distribution point extension.</p>',
             '<p>为 issuing distribution point 扩展描述一个 CRL 的覆盖范围。</p>'),
            ('<p>The CRL contains only end-entity user certificates.</p>',
             '<p>该 CRL 仅包含终端用户证书。</p>'),
            ('<p>The CRL contains only CA certificates.</p>',
             '<p>该 CRL 仅包含 CA 证书。</p>'),
        ],
    ),
    # ----- enum.DnType.html -----
    (
        'enum.DnType.html',
        [
            ('<p>The attribute type of a distinguished name entry</p>',
             '<p>一个 distinguished name 条目的属性类型</p>'),
        ],
    ),
    # ----- enum.DnValue.html -----
    (
        'enum.DnValue.html',
        [
            ('<p>A distinguished name entry</p>',
             '<p>一个 distinguished name 条目</p>'),
        ],
    ),
    # ----- enum.Error.html -----
    (
        'enum.Error.html',
        [
            ('<p>The error type of the rcgen crate</p>',
             '<p>rcgen crate 的错误类型</p>'),
        ],
    ),
    # ----- enum.SanType.html -----
    (
        'enum.SanType.html',
        [
            ('<p>The type of subject alt name</p>',
             '<p>主题备用名称（Subject Alternative Name）的类型</p>'),
        ],
    ),
    # ----- enum.InvalidAsn1String.html -----
    (
        'enum.InvalidAsn1String.html',
        [
            ('<p>Invalid ASN.1 string type</p>',
             '<p>非法的 ASN.1 字符串类型</p>'),
        ],
    ),
    # ----- enum.RevocationReason.html -----
    # ----- index.html -----
    (
        'index.html',
        [
            ('<p>The most simple way of using this crate is by calling\r\n'
             'the <a href="fn.generate_simple_self_signed.html" title="fn rcgen::generate_simple_self_signed"><code>generate_simple_self_signed</code></a> function.\r\n'
             'For more customization abilities, construct a <a href="struct.CertificateParams.html" title="struct rcgen::CertificateParams"><code>CertificateParams</code></a> and\r\n'
             'a key pair to call <a href="struct.CertificateParams.html#method.signed_by" title="method rcgen::CertificateParams::signed_by"><code>CertificateParams::signed_by()</code></a> or\r\n'
             '<a href="struct.CertificateParams.html#method.self_signed" title="method rcgen::CertificateParams::self_signed"><code>CertificateParams::self_signed()</code></a>.</p>',
             '<p>使用本 crate 最简单的方式是调用 <a href="fn.generate_simple_self_signed.html" title="fn rcgen::generate_simple_self_signed"><code>generate_simple_self_signed</code></a> 函数。\n'
             '如果需要更强的定制能力，可以构造一个 <a href="struct.CertificateParams.html" title="struct rcgen::CertificateParams"><code>CertificateParams</code></a> 与一个密钥对，然后调用\n'
             '<a href="struct.CertificateParams.html#method.signed_by" title="method rcgen::CertificateParams::signed_by"><code>CertificateParams::signed_by()</code></a> 或\n'
             '<a href="struct.CertificateParams.html#method.self_signed" title="method rcgen::CertificateParams::self_signed"><code>CertificateParams::self_signed()</code></a>。</p>'),
        ],
    ),
    # ----- struct.Attribute.html -----
    (
        'struct.Attribute.html',
        [
            ('<p>A PKCS #10 CSR attribute, as defined in RFC 5280 and constrained by RFC 2986.</p>',
             '<p>一个 PKCS #10 CSR 属性，定义见 RFC 5280，并由 RFC 2986 加以约束。</p>'),
            ('<p>AttributeType of the Attribute, defined as an OBJECT IDENTIFIER.</p>',
             '<p>属性的 AttributeType，定义为 OBJECT IDENTIFIER。</p>'),
            ('<p>DER-encoded values of the Attribute, defined by RFC 2986 as:</p>',
             '<p>属性的 DER 编码值，由 RFC 2986 定义如下：</p>'),
        ],
    ),
    # ----- struct.Certificate.html -----
    (
        'struct.Certificate.html',
        [
            ('<p>An issued certificate</p>',
             '<p>一份已颁发的证书</p>'),
        ],
    ),
    # ----- struct.CertificateParams.html -----
    (
        'struct.CertificateParams.html',
        [
            ('<p>Parameters used for certificate generation</p>',
             '<p>用于生成证书的参数</p>'),
            ('<p>Calculates a subject key identifier for the certificate subject’s public key.\r\n'
             'This key identifier is used in the SubjectKeyIdentifier X.509v3 extension.</p>',
             '<p>为证书 subject 的公钥计算 subject key identifier。\n'
             '该密钥标识符用于 SubjectKeyIdentifier 这个 X.509v3 扩展。</p>'),
            ('<p>Generate and serialize a certificate signing request (CSR) with custom PKCS #10 attributes.\r\n'
             'as defined in <a href="https://datatracker.ietf.org/doc/html/rfc2986#section-4">RFC 2986</a>.</p>',
             '<p>生成并将一个带有自定义 PKCS #10 属性的证书签名请求（CSR）序列化，\n'
             '属性定义见 <a href="https://datatracker.ietf.org/doc/html/rfc2986#section-4">RFC 2986</a>。</p>'),
            ('<p>The constructed CSR will contain attributes based on the certificate parameters,\r\n'
             'and include the subject public key information from <code>subject_key</code>. Additionally,\r\n'
             'the CSR will be self-signed using the subject key.</p>',
             '<p>所构造的 CSR 将包含基于证书参数得到的属性，\n'
             '并携带来自 <code>subject_key</code> 的 subject 公钥信息。\n'
             '此外，CSR 将使用 subject 密钥进行自签名。</p>'),
            ('<p>Note that subsequent invocations of <code>serialize_request_with_attributes()</code> will not produce the exact\r\n'
             'same output.</p>',
             '<p>请注意，重复调用 <code>serialize_request_with_attributes()</code> 不会得到完全相同的输出。</p>'),
        ],
    ),
    # ----- struct.CertificateRevocationList.html -----
    (
        'struct.CertificateRevocationList.html',
        [
            ('<p>A certificate revocation list (CRL)</p>',
             '<p>一个证书吊销列表（CRL）</p>'),
        ],
    ),
    # ----- struct.CertificateRevocationListParams.html -----
    (
        'struct.CertificateRevocationListParams.html',
        [
            ('<p>Parameters used for certificate revocation list (CRL) generation</p>',
             '<p>用于生成证书吊销列表（CRL）的参数</p>'),
        ],
    ),
    # ----- struct.CertificateSigningRequest.html -----
    (
        'struct.CertificateSigningRequest.html',
        [
            ('<p>A certificate signing request (CSR) that can be encoded to PEM or DER.</p>',
             '<p>一个可被编码为 PEM 或 DER 形式的证书签名请求（CSR）。</p>'),
        ],
    ),
    # ----- struct.CertificateSigningRequestParams.html -----
    (
        'struct.CertificateSigningRequestParams.html',
        [
            ('<p>Parameters for a certificate signing request</p>',
             '<p>证书签名请求的参数</p>'),
            ('<p>Generate a new certificate based on the requested parameters, signed by the provided\r\n'
             'issuer.</p>',
             '<p>根据所请求的参数生成一份新证书，由所提供的颁发者签名。</p>'),
            ('<p>The returned certificate will have its issuer field set to the subject of the provided\r\n'
             '<code>issuer</code>, and the authority key identifier extension will be populated using the subject\r\n'
             'public key of <code>issuer</code>. It will be signed by <code>issuer_key</code>.</p>',
             '<p>返回的证书会将其 issuer 字段设置为所提供 <code>issuer</code> 的 subject，\n'
             '并使用 <code>issuer</code> 的 subject 公钥填充 authority key identifier 扩展。\n'
             '该证书将由 <code>issuer_key</code> 进行签名。</p>'),
            ('<p>Note that no validation of the <code>issuer</code> certificate is performed. Rcgen will not require\r\n'
             'the certificate to be a CA certificate, or have key usage extensions that allow signing.</p>',
             '<p>请注意，<code>issuer</code> 证书不会经过任何验证。rcgen 不会强制要求该证书是 CA 证书，\n'
             '也不会要求其具有允许签名的 key usage 扩展。</p>'),
            ('<p>The returned <a href="struct.Certificate.html" title="struct rcgen::Certificate"><code>Certificate</code></a> may be serialized using <a href="struct.Certificate.html#method.der" title="method rcgen::Certificate::der"><code>Certificate::der</code></a> and\r\n'
             '<a href="struct.Certificate.html#method.pem" title="method rcgen::Certificate::pem"><code>Certificate::pem</code></a>.</p>',
             '<p>返回的 <a href="struct.Certificate.html" title="struct rcgen::Certificate"><code>Certificate</code></a> 可通过 <a href="struct.Certificate.html#method.der" title="method rcgen::Certificate::der"><code>Certificate::der</code></a> 与\n'
             '<a href="struct.Certificate.html#method.pem" title="method rcgen::Certificate::pem"><code>Certificate::pem</code></a> 进行序列化。</p>'),
        ],
    ),
    # ----- struct.CertifiedIssuer.html -----
    (
        'struct.CertifiedIssuer.html',
        [
            ('<p>An <a href="struct.Issuer.html" title="struct rcgen::Issuer"><code>Issuer</code></a> wrapper that also contains the issuer’s <a href="struct.Certificate.html" title="struct rcgen::Certificate"><code>Certificate</code></a>.</p>',
             '<p>一个 <a href="struct.Issuer.html" title="struct rcgen::Issuer"><code>Issuer</code></a> 包装，同时包含颁发者的 <a href="struct.Certificate.html" title="struct rcgen::Certificate"><code>Certificate</code></a>。</p>'),
        ],
    ),
    # ----- struct.CertifiedKey.html -----
    (
        'struct.CertifiedKey.html',
        [
            ('<p>An issued certificate, together with the subject keypair.</p>',
             '<p>一份已颁发的证书，连同其 subject 密钥对。</p>'),
            ('<p>An issued certificate.</p>',
             '<p>一份已颁发的证书。</p>'),
            ('<p>The certificate’s subject signing key.</p>',
             '<p>该证书的 subject 签名密钥。</p>'),
        ],
    ),
    # ----- struct.CrlDistributionPoint.html -----
    (
        'struct.CrlDistributionPoint.html',
        [
            ('<p>A certificate revocation list (CRL) distribution point, to be included in a certificate’s distribution points extension or a CRL’s issuing distribution point extension</p>',
             '<p>一个证书吊销列表（CRL）分发点，可包含在证书的 distribution points 扩展或 CRL 的 issuing distribution point 扩展中</p>'),
        ],
    ),
    # ----- struct.CrlIssuingDistributionPoint.html -----
    (
        'struct.CrlIssuingDistributionPoint.html',
        [
            ('<p>A certificate revocation list (CRL) issuing distribution point, to be included in a CRL’s issuing distribution point extension.</p>',
             '<p>一个证书吊销列表（CRL）颁发分发点，包含在 CRL 的 issuing distribution point 扩展中。</p>'),
        ],
    ),
    # ----- struct.CustomExtension.html -----
    (
        'struct.CustomExtension.html',
        [
            ('<p>A custom extension of a certificate, as specified in\r\n'
             '<a href="https://tools.ietf.org/html/rfc5280#section-4.2">RFC 5280</a></p>',
             '<p>证书的一个自定义扩展，定义见 <a href="https://tools.ietf.org/html/rfc5280#section-4.2">RFC 5280</a></p>'),
        ],
    ),
    # ----- struct.DistinguishedName.html -----
    (
        'struct.DistinguishedName.html',
        [
            ('<p>Distinguished name used e.g. for the issuer and subject fields of a certificate</p>',
             '<p>用于（例如）证书 issuer 与 subject 字段的 distinguished name</p>'),
        ],
    ),
    # ----- struct.DistinguishedNameIterator.html -----
    (
        'struct.DistinguishedNameIterator.html',
        [
            ('<p>Iterator over <a href="struct.DistinguishedName.html" title="struct rcgen::DistinguishedName"><code>DistinguishedName</code></a> entries</p>',
             '<p>对 <a href="struct.DistinguishedName.html" title="struct rcgen::DistinguishedName"><code>DistinguishedName</code></a> 条目的迭代器</p>'),
        ],
    ),
    # ----- struct.Issuer.html -----
    (
        'struct.Issuer.html',
        [
            ('<p>An issuer that can sign certificates.</p>',
             '<p>一个能够对证书进行签名的颁发者。</p>'),
            ('<p>Encapsulates the distinguished name, key identifier method, key usages and signing key\r\n'
             'of the issuing certificate.</p>',
             '<p>它封装了颁发证书的 distinguished name、密钥标识符生成方法、key usage 与签名密钥。</p>'),
        ],
    ),
    # ----- struct.KeyPair.html -----
    (
        'struct.KeyPair.html',
        [
            ('<p>A key pair used to sign certificates and CSRs</p>',
             '<p>用于对证书和 CSR 进行签名的密钥对</p>'),
            ('<p>Generate a new random <a href="static.PKCS_ECDSA_P256_SHA256.html" title="static rcgen::PKCS_ECDSA_P256_SHA256"><code>PKCS_ECDSA_P256_SHA256</code></a> key pair</p>',
             '<p>生成一个新的随机 <a href="static.PKCS_ECDSA_P256_SHA256.html" title="static rcgen::PKCS_ECDSA_P256_SHA256"><code>PKCS_ECDSA_P256_SHA256</code></a> 密钥对</p>'),
            ('<p>Generate a new random key pair for the specified signature algorithm</p>',
             '<p>为指定的签名算法生成一个新的随机密钥对</p>'),
            ('<p>If you’re not sure which algorithm to use, <a href="static.PKCS_ECDSA_P256_SHA256.html" title="static rcgen::PKCS_ECDSA_P256_SHA256"><code>PKCS_ECDSA_P256_SHA256</code></a> is a good choice.\r\n'
             'If passed an RSA signature algorithm, it depends on the backend whether we return\r\n'
             'a generated key or an error for key generation being unavailable.\r\n'
             'Currently, only <code>aws-lc-rs</code> supports RSA key generation.</p>',
             '<p>若你不确定该使用哪种算法，<a href="static.PKCS_ECDSA_P256_SHA256.html" title="static rcgen::PKCS_ECDSA_P256_SHA256"><code>PKCS_ECDSA_P256_SHA256</code></a> 是一个不错的选择。\n'
             '若传入的是一种 RSA 签名算法，则取决于后端实现：可能返回生成的密钥，\n'
             '也可能因不支持密钥生成而返回错误。目前只有 <code>aws-lc-rs</code> 支持 RSA 密钥生成。</p>'),
            # method.from_pkcs8_der_and_sign_algo (short 1st p, then 2 separate p's)
            ('<p>Obtains the key pair from a DER formatted key\r\n'
             'using the specified <a href="struct.SignatureAlgorithm.html" title="struct rcgen::SignatureAlgorithm"><code>SignatureAlgorithm</code></a></p>',
             '<p>从 DER 格式的密钥解析出密钥对，并使用指定的 <a href="struct.SignatureAlgorithm.html" title="struct rcgen::SignatureAlgorithm"><code>SignatureAlgorithm</code></a></p>'),
            ('<p>The key must be a DER-encoded plaintext private key; as specified in PKCS #8/RFC 5958;</p>',
             '<p>密钥必须是 DER 编码的明文私钥；规定见 PKCS #8 / RFC 5958；</p>'),
            ('<p>Appears as “PRIVATE KEY” in PEM files\r\n'
             'Same as <a href="struct.KeyPair.html#method.from_pkcs8_pem_and_sign_algo" title="associated function rcgen::KeyPair::from_pkcs8_pem_and_sign_algo">from_pkcs8_pem_and_sign_algo</a>.</p>',
             '<p>在 PEM 文件中以 “PRIVATE KEY” 形式出现。\n'
             '同 <a href="struct.KeyPair.html#method.from_pkcs8_pem_and_sign_algo" title="associated function rcgen::KeyPair::from_pkcs8_pem_and_sign_algo">from_pkcs8_pem_and_sign_algo</a>。</p>'),
            # method.from_pkcs8_der_and_sign_algo (single docblock, with TryFrom, "..." smart quotes)
            ('<p>Obtains the key pair from a DER formatted key using the specified <a href="struct.SignatureAlgorithm.html" title="struct rcgen::SignatureAlgorithm"><code>SignatureAlgorithm</code></a></p>',
             '<p>从 DER 格式的密钥解析出密钥对，并使用指定的 <a href="struct.SignatureAlgorithm.html" title="struct rcgen::SignatureAlgorithm"><code>SignatureAlgorithm</code></a></p>'),
            ('<p>If you have a <a href="../rustls_pki_types/struct.PrivatePkcs8KeyDer.html" title="struct rustls_pki_types::PrivatePkcs8KeyDer"><code>PrivatePkcs8KeyDer</code></a>, you can usually rely on the <a href="https://doc.rust-lang.org/1.95.0/core/convert/trait.TryFrom.html" title="trait core::convert::TryFrom"><code>TryFrom</code></a> implementation\r\n'
             'to obtain a <a href="struct.KeyPair.html" title="struct rcgen::KeyPair"><code>KeyPair</code></a> – it will determine the correct <a href="struct.SignatureAlgorithm.html" title="struct rcgen::SignatureAlgorithm"><code>SignatureAlgorithm</code></a> for you.\r\n'
             'However, sometimes multiple signature algorithms fit for the same DER key. In those instances,\r\n'
             'you can use this function to precisely specify the <code>SignatureAlgorithm</code>.</p>',
             '<p>若你拥有一个 <a href="../rustls_pki_types/struct.PrivatePkcs8KeyDer.html" title="struct rustls_pki_types::PrivatePkcs8KeyDer"><code>PrivatePkcs8KeyDer</code></a>，通常可以依赖 <a href="https://doc.rust-lang.org/1.95.0/core/convert/trait.TryFrom.html" title="trait core::convert::TryFrom"><code>TryFrom</code></a> 实现来得到一个 <a href="struct.KeyPair.html" title="struct rcgen::KeyPair"><code>KeyPair</code></a>——\n'
             '它会为你确定正确的 <a href="struct.SignatureAlgorithm.html" title="struct rcgen::SignatureAlgorithm"><code>SignatureAlgorithm</code></a>。\n'
             '不过，有时同一段 DER 密钥可能匹配多种签名算法。这种情况下，你可以使用本函数精确地指定 <code>SignatureAlgorithm</code>。</p>'),
            ('<p><a href="https://docs.rs/rustls-pemfile/latest/rustls_pemfile/fn.private_key.html"><code>rustls_pemfile::private_key()</code></a> is often used to obtain a <a href="https://docs.rs/rustls-pki-types/latest/rustls_pki_types/enum.PrivateKeyDer.html"><code>PrivateKeyDer</code></a> from PEM\r\n'
             'input. If the obtained <a href="https://docs.rs/rustls-pki-types/latest/rustls_pki_types/enum.PrivateKeyDer.html"><code>PrivateKeyDer</code></a> is a <code>Pkcs8</code> variant, you can use its contents\r\n'
             'as input for this function. Alternatively, if you already have a byte slice containing DER,\r\n'
             'it can trivially be converted into <a href="../rustls_pki_types/struct.PrivatePkcs8KeyDer.html" title="struct rustls_pki_types::PrivatePkcs8KeyDer"><code>PrivatePkcs8KeyDer</code></a> using the <a href="https://doc.rust-lang.org/1.95.0/core/convert/trait.Into.html" title="trait core::convert::Into"><code>Into</code></a> trait.</p>',
             '<p><a href="https://docs.rs/rustls-pemfile/latest/rustls_pemfile/fn.private_key.html"><code>rustls_pemfile::private_key()</code></a> 常用于从 PEM 输入得到 <a href="https://docs.rs/rustls-pki-types/latest/rustls_pki_types/enum.PrivateKeyDer.html"><code>PrivateKeyDer</code></a>。\n'
             '若得到的 <a href="https://docs.rs/rustls-pki-types/latest/rustls_pki_types/enum.PrivateKeyDer.html"><code>PrivateKeyDer</code></a> 是 <code>Pkcs8</code> 变体，你可以将它的内容作为本函数的输入。\n'
             '另外，若你已经有一段包含 DER 数据的字节切片，使用 <a href="https://doc.rust-lang.org/1.95.0/core/convert/trait.Into.html" title="trait core::convert::Into"><code>Into</code></a> trait 便可轻松地将其转换为 <a href="../rustls_pki_types/struct.PrivatePkcs8KeyDer.html" title="struct rustls_pki_types::PrivatePkcs8KeyDer"><code>PrivatePkcs8KeyDer</code></a>。</p>'),
            # method.from_pem_and_sign_algo
            ('<p>Obtains the key pair from a PEM formatted key\r\n'
             'using the specified <a href="struct.SignatureAlgorithm.html" title="struct rcgen::SignatureAlgorithm"><code>SignatureAlgorithm</code></a></p>',
             '<p>从 PEM 格式的密钥解析出密钥对，并使用指定的 <a href="struct.SignatureAlgorithm.html" title="struct rcgen::SignatureAlgorithm"><code>SignatureAlgorithm</code></a></p>'),
            ('<p>If <code>aws_lc_rs</code> feature is used, then the key must be a DER-encoded plaintext private key; as specified in PKCS #8/RFC 5958, SEC1/RFC 5915, or PKCS#1/RFC 3447;\r\n'
             'Appears as “PRIVATE KEY”, “RSA PRIVATE KEY”, or “EC PRIVATE KEY” in PEM files.</p>',
             '<p>若使用了 <code>aws_lc_rs</code> feature，则该密钥必须是 DER 编码的明文私钥；\n'
             '规定见 PKCS #8 / RFC 5958、SEC1 / RFC 5915 或 PKCS#1 / RFC 3447；\n'
             '在 PEM 文件中以 “PRIVATE KEY”、“RSA PRIVATE KEY” 或 “EC PRIVATE KEY” 形式出现。</p>'),
            ('<p>Otherwise if the <code>ring</code> feature is used, then the key must be a DER-encoded plaintext private key; as specified in PKCS #8/RFC 5958;\r\n'
             'Appears as “PRIVATE KEY” in PEM files.</p>',
             '<p>若使用的是 <code>ring</code> feature，则该密钥必须是 DER 编码的明文私钥；\n'
             '规定见 PKCS #8 / RFC 5958；在 PEM 文件中以 “PRIVATE KEY” 形式出现。</p>'),
            ('<p>Same as <a href="struct.KeyPair.html#method.from_pem_and_sign_algo" title="associated function rcgen::KeyPair::from_pem_and_sign_algo">from_pem_and_sign_algo</a>.</p>',
             '<p>同 <a href="struct.KeyPair.html#method.from_pem_and_sign_algo" title="associated function rcgen::KeyPair::from_pem_and_sign_algo">from_pem_and_sign_algo</a>。</p>'),
            # method.from_der_and_sign_algo (3 p's)
            ('<p>Note that using the <code>ring</code> feature, this function only support <a href="../rustls_pki_types/enum.PrivateKeyDer.html#variant.Pkcs8" title="variant rustls_pki_types::PrivateKeyDer::Pkcs8"><code>PrivateKeyDer::Pkcs8</code></a> variant.\r\n'
             'Consider using the <code>aws_lc_rs</code> features to support <a href="../rustls_pki_types/enum.PrivateKeyDer.html" title="enum rustls_pki_types::PrivateKeyDer"><code>PrivateKeyDer</code></a> fully.</p>',
             '<p>请注意，若使用 <code>ring</code> feature，本函数仅支持 <a href="../rustls_pki_types/enum.PrivateKeyDer.html#variant.Pkcs8" title="variant rustls_pki_types::PrivateKeyDer::Pkcs8"><code>PrivateKeyDer::Pkcs8</code></a> 变体。\n'
             '若需要完整支持 <a href="../rustls_pki_types/enum.PrivateKeyDer.html" title="enum rustls_pki_types::PrivateKeyDer"><code>PrivateKeyDer</code></a>，请考虑启用 <code>aws_lc_rs</code> feature。</p>'),
            ('<p>You can use <a href="https://docs.rs/rustls-pemfile/latest/rustls_pemfile/fn.private_key.html"><code>rustls_pemfile::private_key</code></a> to get the <code>key</code> input. If\r\n'
             'you have already a byte slice, just calling <code>try_into()</code> will convert it to a <a href="../rustls_pki_types/enum.PrivateKeyDer.html" title="enum rustls_pki_types::PrivateKeyDer"><code>PrivateKeyDer</code></a>.</p>',
             '<p>你可以使用 <a href="https://docs.rs/rustls-pemfile/latest/rustls_pemfile/fn.private_key.html"><code>rustls_pemfile::private_key</code></a> 来获取密钥输入。\n'
             '若你已有字节切片，只需调用 <code>try_into()</code> 即可将其转换为 <a href="../rustls_pki_types/enum.PrivateKeyDer.html" title="enum rustls_pki_types::PrivateKeyDer"><code>PrivateKeyDer</code></a>。</p>'),
            ('<p>The key is in raw format, as how <a href="../ring/signature/trait.KeyPair.html#tymethod.public_key" title="method ring::signature::KeyPair::public_key"><code>KeyPair::public_key()</code></a>\r\n'
             'would output, and how <a href="../ring/signature/struct.UnparsedPublicKey.html#method.verify" title="method ring::signature::UnparsedPublicKey::verify"><code>UnparsedPublicKey::verify()</code></a>\r\n'
             'would accept.</p>',
             '<p>密钥为原始格式，与 <a href="../ring/signature/trait.KeyPair.html#tymethod.public_key" title="method ring::signature::KeyPair::public_key"><code>KeyPair::public_key()</code></a> 的输出以及\n'
             '<a href="../ring/signature/struct.UnparsedPublicKey.html#method.verify" title="method ring::signature::UnparsedPublicKey::verify"><code>UnparsedPublicKey::verify()</code></a> 所接受的格式一致。</p>'),
            ('<p>Returns (possibly multiple) compatible <a href="struct.SignatureAlgorithm.html" title="struct rcgen::SignatureAlgorithm"><code>SignatureAlgorithm</code></a>’s\r\n'
             'that the key can be used with</p>',
             '<p>返回（可能多个）此密钥可兼容使用的 <a href="struct.SignatureAlgorithm.html" title="struct rcgen::SignatureAlgorithm"><code>SignatureAlgorithm</code></a></p>'),
            ('<p>Returns a reference to the serialized key pair (including the private key)\r\n'
             'in PKCS#8 format in DER</p>',
             '<p>返回该密钥对（包括私钥）以 PKCS#8 DER 格式序列化结果的引用</p>'),
            # method.public_key_raw (TBD, but listed in audit as method.der_bytes via PublicKeyData trait)
        ],
    ),
    # ----- struct.NameConstraints.html -----
    (
        'struct.NameConstraints.html',
        [
            ('<p>The NameConstraints extension (only relevant for CA certificates)</p>',
             '<p>NameConstraints 扩展（仅对 CA 证书有意义）</p>'),
        ],
    ),
    # ----- struct.PublicKey.html -----
    (
        'struct.PublicKey.html',
        [
            ('<p>A public key, extracted from a CSR</p>',
             '<p>从一份 CSR 中提取出的公钥</p>'),
        ],
    ),
    # ----- struct.RevokedCertParams.html -----
    (
        'struct.RevokedCertParams.html',
        [
            ('<p>Parameters used for describing a revoked certificate included in a <a href="struct.CertificateRevocationList.html" title="struct rcgen::CertificateRevocationList"><code>CertificateRevocationList</code></a>.</p>',
             '<p>用于描述包含在 <a href="struct.CertificateRevocationList.html" title="struct rcgen::CertificateRevocationList"><code>CertificateRevocationList</code></a> 中的已吊销证书的参数。</p>'),
        ],
    ),
    # ----- struct.SerialNumber.html -----
    (
        'struct.SerialNumber.html',
        [
            ('<p>A certificate serial number.</p>',
             '<p>证书的序列号。</p>'),
        ],
    ),
    # ----- struct.SignatureAlgorithm.html -----
    (
        'struct.SignatureAlgorithm.html',
        [
            ('<p>Signature algorithm type</p>',
             '<p>签名算法类型</p>'),
            ('<p>Retrieve the SignatureAlgorithm for the provided OID</p>',
             '<p>为给定的 OID 获取对应的 <a href="struct.SignatureAlgorithm.html" title="struct rcgen::SignatureAlgorithm"><code>SignatureAlgorithm</code></a></p>'),
        ],
    ),
    # ----- struct.SubjectPublicKeyInfo.html -----
    (
        'struct.SubjectPublicKeyInfo.html',
        [
            ('<p>A public key</p>',
             '<p>一个公钥</p>'),
        ],
    ),
    # ----- trait.PublicKeyData.html -----
    (
        'trait.PublicKeyData.html',
        [
            ('<p>The public key data of a key pair</p>',
             '<p>一个密钥对的公钥数据</p>'),
        ],
    ),
    # ----- trait.SigningKey.html -----
    (
        'trait.SigningKey.html',
        [
            ('<p>A key that can be used to sign messages</p>',
             '<p>一个可用于对消息进行签名的密钥</p>'),
        ],
    ),
    # ----- type.RcgenError.html -----
    (
        'type.RcgenError.html',
        [
            ('<p>Type-alias for the old name of <a href="enum.Error.html" title="enum rcgen::Error"><code>Error</code></a>.</p>',
             '<p>旧名称 <a href="enum.Error.html" title="enum rcgen::Error"><code>Error</code></a> 的类型别名。</p>'),
        ],
    ),
    # ----- string/index.html -----
    (
        'string/index.html',
        [
            ('<p>ASN.1 string types</p>',
             '<p>ASN.1 字符串类型</p>'),
        ],
    ),
    # ----- string/struct.BmpString.html -----
    (
        'string/struct.BmpString.html',
        [
            ('<p>Returns a byte slice of this <code>BmpString</code>’s contents.</p>',
             '<p>返回该 <code>BmpString</code> 内容对应的字节切片。</p>'),
            ('<p>The inverse of this method is <a href="struct.BmpString.html#method.from_utf16be" title="associated function rcgen::string::BmpString::from_utf16be">from_utf16be</a>.</p>',
             '<p>本方法的反操作是 <a href="struct.BmpString.html#method.from_utf16be" title="associated function rcgen::string::BmpString::from_utf16be">from_utf16be</a>。</p>'),
            ('<p>Converts a <code>&amp;str</code> to a <a href="struct.BmpString.html" title="struct rcgen::string::BmpString"><code>BmpString</code></a>.</p>',
             '<p>将一个 <code>&amp;str</code> 转换为 <a href="struct.BmpString.html" title="struct rcgen::string::BmpString"><code>BmpString</code></a>。</p>'),
            ('<p>Any character not in the <a href="struct.BmpString.html" title="struct rcgen::string::BmpString"><code>BmpString</code></a> charset will be rejected.\r\n'
             'See <a href="struct.BmpString.html" title="struct rcgen::string::BmpString"><code>BmpString</code></a> documentation for more information.</p>',
             '<p>任何不属于 <a href="struct.BmpString.html" title="struct rcgen::string::BmpString"><code>BmpString</code></a> 字符集的字符都将被拒绝。\n'
             '更多信息请参见 <a href="struct.BmpString.html" title="struct rcgen::string::BmpString"><code>BmpString</code></a> 文档。</p>'),
            ('<p>The result is allocated on the heap.</p>',
             '<p>结果将在堆上分配。</p>'),
            ('<p>Converts a <a href="https://doc.rust-lang.org/1.95.0/alloc/string/struct.String.html" title="struct alloc::string::String"><code>String</code></a> into a <a href="struct.BmpString.html" title="struct rcgen::string::BmpString"><code>BmpString</code></a></p>',
             '<p>将一个 <a href="https://doc.rust-lang.org/1.95.0/alloc/string/struct.String.html" title="struct alloc::string::String"><code>String</code></a> 转换为 <a href="struct.BmpString.html" title="struct rcgen::string::BmpString"><code>BmpString</code></a></p>'),
            ('<p>Parsing a <a href="struct.BmpString.html" title="struct rcgen::string::BmpString"><code>BmpString</code></a> allocates memory since the UTF-8 to UTF-16 conversion requires a memory allocation.</p>',
             '<p>解析 <a href="struct.BmpString.html" title="struct rcgen::string::BmpString"><code>BmpString</code></a> 时会进行内存分配，因为 UTF-8 到 UTF-16 的转换需要一次内存分配。</p>'),
        ],
    ),
    # ----- string/struct.Ia5String.html -----
    (
        'string/struct.Ia5String.html',
        [
            ('<p>Extracts a string slice containing the entire <code>Ia5String</code>.</p>',
             '<p>提取包含整个 <code>Ia5String</code> 的字符串切片。</p>'),
            ('<p>Converts a <code>&amp;str</code> to a <a href="struct.Ia5String.html" title="struct rcgen::string::Ia5String"><code>Ia5String</code></a>.</p>',
             '<p>将一个 <code>&amp;str</code> 转换为 <a href="struct.Ia5String.html" title="struct rcgen::string::Ia5String"><code>Ia5String</code></a>。</p>'),
            ('<p>Any character not in the <a href="struct.Ia5String.html" title="struct rcgen::string::Ia5String"><code>Ia5String</code></a> charset will be rejected.\r\n'
             'See <a href="struct.Ia5String.html" title="struct rcgen::string::Ia5String"><code>Ia5String</code></a> documentation for more information.</p>',
             '<p>任何不属于 <a href="struct.Ia5String.html" title="struct rcgen::string::Ia5String"><code>Ia5String</code></a> 字符集的字符都将被拒绝。\n'
             '更多信息请参见 <a href="struct.Ia5String.html" title="struct rcgen::string::Ia5String"><code>Ia5String</code></a> 文档。</p>'),
            ('<p>Converts a <a href="https://doc.rust-lang.org/1.95.0/alloc/string/struct.String.html" title="struct alloc::string::String"><code>String</code></a> into a <a href="struct.Ia5String.html" title="struct rcgen::string::Ia5String"><code>Ia5String</code></a></p>',
             '<p>将一个 <a href="https://doc.rust-lang.org/1.95.0/alloc/string/struct.String.html" title="struct alloc::string::String"><code>String</code></a> 转换为 <a href="struct.Ia5String.html" title="struct rcgen::string::Ia5String"><code>Ia5String</code></a></p>'),
        ],
    ),
    # ----- string/struct.PrintableString.html -----
    (
        'string/struct.PrintableString.html',
        [
            ('<p>Extracts a string slice containing the entire <code>PrintableString</code>.</p>',
             '<p>提取包含整个 <code>PrintableString</code> 的字符串切片。</p>'),
            ('<p>Converts a <code>&amp;str</code> to a <a href="struct.PrintableString.html" title="struct rcgen::string::PrintableString"><code>PrintableString</code></a>.</p>',
             '<p>将一个 <code>&amp;str</code> 转换为 <a href="struct.PrintableString.html" title="struct rcgen::string::PrintableString"><code>PrintableString</code></a>。</p>'),
            ('<p>Any character not in the <a href="struct.PrintableString.html" title="struct rcgen::string::PrintableString"><code>PrintableString</code></a> charset will be rejected.\r\n'
             'See <a href="struct.PrintableString.html" title="struct rcgen::string::PrintableString"><code>PrintableString</code></a> documentation for more information.</p>',
             '<p>任何不属于 <a href="struct.PrintableString.html" title="struct rcgen::string::PrintableString"><code>PrintableString</code></a> 字符集的字符都将被拒绝。\n'
             '更多信息请参见 <a href="struct.PrintableString.html" title="struct rcgen::string::PrintableString"><code>PrintableString</code></a> 文档。</p>'),
            ('<p>Converts a <a href="https://doc.rust-lang.org/1.95.0/alloc/string/struct.String.html" title="struct alloc::string::String"><code>String</code></a> into a <a href="struct.PrintableString.html" title="struct rcgen::string::PrintableString"><code>PrintableString</code></a></p>',
             '<p>将一个 <a href="https://doc.rust-lang.org/1.95.0/alloc/string/struct.String.html" title="struct alloc::string::String"><code>String</code></a> 转换为 <a href="struct.PrintableString.html" title="struct rcgen::string::PrintableString"><code>PrintableString</code></a></p>'),
        ],
    ),
    # ----- string/struct.TeletexString.html -----
    (
        'string/struct.TeletexString.html',
        [
            ('<p>Extracts a string slice containing the entire <code>TeletexString</code>.</p>',
             '<p>提取包含整个 <code>TeletexString</code> 的字符串切片。</p>'),
            ('<p>Returns a byte slice of this <code>TeletexString</code>’s contents.</p>',
             '<p>返回该 <code>TeletexString</code> 内容对应的字节切片。</p>'),
            ('<p>Converts a <code>&amp;str</code> to a <a href="struct.TeletexString.html" title="struct rcgen::string::TeletexString"><code>TeletexString</code></a>.</p>',
             '<p>将一个 <code>&amp;str</code> 转换为 <a href="struct.TeletexString.html" title="struct rcgen::string::TeletexString"><code>TeletexString</code></a>。</p>'),
            ('<p>Any character not in the <a href="struct.TeletexString.html" title="struct rcgen::string::TeletexString"><code>TeletexString</code></a> charset will be rejected.\r\n'
             'See <a href="struct.TeletexString.html" title="struct rcgen::string::TeletexString"><code>TeletexString</code></a> documentation for more information.</p>',
             '<p>任何不属于 <a href="struct.TeletexString.html" title="struct rcgen::string::TeletexString"><code>TeletexString</code></a> 字符集的字符都将被拒绝。\n'
             '更多信息请参见 <a href="struct.TeletexString.html" title="struct rcgen::string::TeletexString"><code>TeletexString</code></a> 文档。</p>'),
            ('<p>Converts a <a href="https://doc.rust-lang.org/1.95.0/alloc/string/struct.String.html" title="struct alloc::string::String"><code>String</code></a> into a <a href="struct.TeletexString.html" title="struct rcgen::string::TeletexString"><code>TeletexString</code></a></p>',
             '<p>将一个 <a href="https://doc.rust-lang.org/1.95.0/alloc/string/struct.String.html" title="struct alloc::string::String"><code>String</code></a> 转换为 <a href="struct.TeletexString.html" title="struct rcgen::string::TeletexString"><code>TeletexString</code></a></p>'),
        ],
    ),
    # ----- string/struct.UniversalString.html -----
    (
        'string/struct.UniversalString.html',
        [
            ('<p>Returns a byte slice of this <code>UniversalString</code>’s contents.</p>',
             '<p>返回该 <code>UniversalString</code> 内容对应的字节切片。</p>'),
            ('<p>The inverse of this method is <a href="struct.UniversalString.html#method.from_utf32be" title="associated function rcgen::string::UniversalString::from_utf32be">from_utf32be</a>.</p>',
             '<p>本方法的反操作是 <a href="struct.UniversalString.html#method.from_utf32be" title="associated function rcgen::string::UniversalString::from_utf32be">from_utf32be</a>。</p>'),
            ('<p>Converts a <code>&amp;str</code> to a <a href="struct.UniversalString.html" title="struct rcgen::string::UniversalString"><code>UniversalString</code></a>.</p>',
             '<p>将一个 <code>&amp;str</code> 转换为 <a href="struct.UniversalString.html" title="struct rcgen::string::UniversalString"><code>UniversalString</code></a>。</p>'),
            ('<p>Any character not in the <a href="struct.UniversalString.html" title="struct rcgen::string::UniversalString"><code>UniversalString</code></a> charset will be rejected.\r\n'
             'See <a href="struct.UniversalString.html" title="struct rcgen::string::UniversalString"><code>UniversalString</code></a> documentation for more information.</p>',
             '<p>任何不属于 <a href="struct.UniversalString.html" title="struct rcgen::string::UniversalString"><code>UniversalString</code></a> 字符集的字符都将被拒绝。\n'
             '更多信息请参见 <a href="struct.UniversalString.html" title="struct rcgen::string::UniversalString"><code>UniversalString</code></a> 文档。</p>'),
            ('<p>Converts a <a href="https://doc.rust-lang.org/1.95.0/alloc/string/struct.String.html" title="struct alloc::string::String"><code>String</code></a> into a <a href="struct.UniversalString.html" title="struct rcgen::string::UniversalString"><code>UniversalString</code></a></p>',
             '<p>将一个 <a href="https://doc.rust-lang.org/1.95.0/alloc/string/struct.String.html" title="struct alloc::string::String"><code>String</code></a> 转换为 <a href="struct.UniversalString.html" title="struct rcgen::string::UniversalString"><code>UniversalString</code></a></p>'),
            ('<p>Parsing a <a href="struct.UniversalString.html" title="struct rcgen::string::UniversalString"><code>UniversalString</code></a> allocates memory since the UTF-8 to UTF-32 conversion requires a memory allocation.</p>',
             '<p>解析 <a href="struct.UniversalString.html" title="struct rcgen::string::UniversalString"><code>UniversalString</code></a> 时会进行内存分配，因为 UTF-8 到 UTF-32 的转换需要一次内存分配。</p>'),
        ],
    ),
    # ----- fn.date_time_ymd.html -----
    (
        'fn.date_time_ymd.html',
        [
            ('<p>Helper to obtain an <code>OffsetDateTime</code> from year, month, day values</p>',
             '<p>用于从年、月、日值构造 <code>OffsetDateTime</code> 的辅助函数</p>'),
            ('<p>The year, month, day values are assumed to be in UTC.</p>',
             '<p>年、月、日值均按 UTC 时区解释。</p>'),
            ('<p>This helper function serves two purposes: first, so that you don’t\r\n'
             'have to import the time crate yourself in order to specify date\r\n'
             'information, second so that users don’t have to type unproportionately\r\n'
             'long code just to generate an instance of <a href="../time/offset_date_time/struct.OffsetDateTime.html" title="struct time::offset_date_time::OffsetDateTime"><code>OffsetDateTime</code></a>.</p>',
             '<p>本辅助函数有两个用途：第一，避免你为指定日期信息而必须自行导入 time crate；\n'
             '第二，避免用户为生成一个 <a href="../time/offset_date_time/struct.OffsetDateTime.html" title="struct time::offset_date_time::OffsetDateTime"><code>OffsetDateTime</code></a> 实例而不得不书写不成比例的冗长代码。</p>'),
        ],
    ),
    # ----- fn.generate_simple_self_signed.html -----
    (
        'fn.generate_simple_self_signed.html',
        [
            ('<p>KISS function to generate a self signed certificate</p>',
             '<p>用于生成自签名证书的 KISS 函数</p>'),
            ('<p>Given a set of domain names you want your certificate to be valid for,\r\n'
             'this function fills in the other generation parameters with\r\n'
             'reasonable defaults and generates a self signed certificate\r\n'
             'and key pair as output.</p>',
             '<p>给定你希望证书对其有效的域名集合后，本函数会使用合理的默认值填充其他生成参数，\n'
             '并最终生成一份自签名证书以及对应的密钥对。</p>'),
        ],
    ),
    # ----- static.PKCS_ECDSA_P256_SHA256.html -----
    (
        'static.PKCS_ECDSA_P256_SHA256.html',
        [
            ('<p>ECDSA signing using the P-256 curves and SHA-256 hashing as per RFC 5758</p>',
             '<p>使用 P-256 曲线的 ECDSA 签名以及 SHA-256 杂凑，遵循 RFC 5758</p>'),
        ],
    ),
    (
        'static.PKCS_ECDSA_P384_SHA384.html',
        [
            ('<p>ECDSA signing using the P-384 curves and SHA-384 hashing as per RFC 5758</p>',
             '<p>使用 P-384 曲线的 ECDSA 签名以及 SHA-384 杂凑，遵循 RFC 5758</p>'),
        ],
    ),
    (
        'static.PKCS_ED25519.html',
        [
            ('<p>Ed25519 signing as per RFC 8032</p>',
             '<p>Ed25519 签名，遵循 RFC 8032</p>'),
        ],
    ),
    (
        'static.PKCS_RSA_SHA256.html',
        [
            ('<p>RSA signing using the SHA-256 hashing as per RFC 8017</p>',
             '<p>使用 SHA-256 杂凑的 RSA 签名，遵循 RFC 8017</p>'),
        ],
    ),
    (
        'static.PKCS_RSA_SHA384.html',
        [
            ('<p>RSA signing using the SHA-384 hashing as per RFC 8017</p>',
             '<p>使用 SHA-384 杂凑的 RSA 签名，遵循 RFC 8017</p>'),
        ],
    ),
    (
        'static.PKCS_RSA_SHA512.html',
        [
            ('<p>RSA signing using the SHA-512 hashing as per RFC 8017</p>',
             '<p>使用 SHA-512 杂凑的 RSA 签名，遵循 RFC 8017</p>'),
        ],
    ),
    # ----- impl trait method docblocks (PublicKeyData/SigningKey) -----
    # These trait method docblocks appear in BOTH:
    #   - trait.PublicKeyData.html (definition)
    #   - struct.KeyPair.html, struct.PublicKey.html, struct.SubjectPublicKeyInfo.html (impl)
    # The "subject public key info" variant (with the RFC link) is the trait definition.
    # The "DER format" / "key pair" versions are impl docblocks.
    # We need to translate BOTH variants.
    (
        'trait.PublicKeyData.html',
        [
            ('<p>The public key in DER format</p>',
             '<p>DER 格式的公钥</p>'),
            ('<p>The algorithm used by the key pair</p>',
             '<p>该密钥对所使用的算法</p>'),
            ('<p>The public key data in DER format</p>',
             '<p>DER 格式的公钥数据</p>'),
            ('<p>The key is formatted according to the X.509 SubjectPublicKeyInfo struct.\r\n'
             'See <a href="https://tools.ietf.org/html/rfc5280#section-4.1">RFC 5280 section 4.1</a>.</p>',
             '<p>该密钥依据 X.509 SubjectPublicKeyInfo 结构进行格式化。\n'
             '参见 <a href="https://tools.ietf.org/html/rfc5280#section-4.1">RFC 5280 §4.1</a>。</p>'),
            ('<p>Formats the value using the given formatter. <a href="https://doc.rust-lang.org/1.95.0/core/fmt/trait.Debug.html" title="trait core::fmt::Debug">Read more</a></p>',
             '<p>使用给定的格式化器格式化该值。<a href="https://doc.rust-lang.org/1.95.0/core/fmt/trait.Debug.html" title="trait core::fmt::Debug">更多信息</a></p>'),
            ('<p>Feeds this value into the given <code>Hasher</code>. <a href="https://doc.rust-lang.org/1.95.0/core/hash/trait.Hash.html" title="trait core::hash::Hash">Read more</a></p>',
             '<p>将该值送入给定的 <code>Hasher</code>。<a href="https://doc.rust-lang.org/1.95.0/core/hash/trait.Hash.html" title="trait core::hash::Hash">更多信息</a></p>'),
            ('<p>Tests for <code>self</code> and <code>other</code> values to be equal, and is used by <code>==</code>. <a href="https://doc.rust-lang.org/1.95.0/core/cmp/trait.PartialEq.html" title="trait core::cmp::PartialEq">Read more</a></p>',
             '<p>判断 <code>self</code> 与 <code>other</code> 是否相等，供 <code>==</code> 使用。<a href="https://doc.rust-lang.org/1.95.0/core/cmp/trait.PartialEq.html" title="trait core::cmp::PartialEq">更多信息</a></p>'),
            ('<p>Tests for <code>!=</code>. The default implementation is almost always sufficient, and should not be overridden without very good reason. <a href="https://doc.rust-lang.org/1.95.0/core/cmp/trait.PartialEq.html" title="trait core::cmp::PartialEq">Read more</a></p>',
             '<p>测试 <code>!=</code>。默认实现几乎总是足够的，没有充分的理由不应被重写。<a href="https://doc.rust-lang.org/1.95.0/core/cmp/trait.PartialEq.html" title="trait core::cmp::PartialEq">更多信息</a></p>'),
            ('<p>Performs the conversion. <a href="https://doc.rust-lang.org/1.95.0/core/convert/trait.From.html" title="trait core::convert::From">Read more</a></p>',
             '<p>执行转换。<a href="https://doc.rust-lang.org/1.95.0/core/convert/trait.From.html" title="trait core::convert::From">更多信息</a></p>'),
            ('<p>Returns a copy of the value. <a href="https://doc.rust-lang.org/1.95.0/core/clone/trait.Clone.html" title="trait core::clone::Clone">Read more</a></p>',
             '<p>返回该值的副本。<a href="https://doc.rust-lang.org/1.95.0/core/clone/trait.Clone.html" title="trait core::clone::Clone">更多信息</a></p>'),
        ],
    ),
    # ----- trait.SigningKey.html -----
    (
        'trait.SigningKey.html',
        [
            ('<p>Signs <code>msg</code> using the selected algorithm</p>',
             '<p>使用所选算法对 <code>msg</code> 进行签名</p>'),
            ('<p>Formats the value using the given formatter. <a href="https://doc.rust-lang.org/1.95.0/core/fmt/trait.Debug.html" title="trait core::fmt::Debug">Read more</a></p>',
             '<p>使用给定的格式化器格式化该值。<a href="https://doc.rust-lang.org/1.95.0/core/fmt/trait.Debug.html" title="trait core::fmt::Debug">更多信息</a></p>'),
            ('<p>Feeds this value into the given <code>Hasher</code>. <a href="https://doc.rust-lang.org/1.95.0/core/hash/trait.Hash.html" title="trait core::hash::Hash">Read more</a></p>',
             '<p>将该值送入给定的 <code>Hasher</code>。<a href="https://doc.rust-lang.org/1.95.0/core/hash/trait.Hash.html" title="trait core::hash::Hash">更多信息</a></p>'),
            ('<p>Tests for <code>self</code> and <code>other</code> values to be equal, and is used by <code>==</code>. <a href="https://doc.rust-lang.org/1.95.0/core/cmp/trait.PartialEq.html" title="trait core::cmp::PartialEq">Read more</a></p>',
             '<p>判断 <code>self</code> 与 <code>other</code> 是否相等，供 <code>==</code> 使用。<a href="https://doc.rust-lang.org/1.95.0/core/cmp/trait.PartialEq.html" title="trait core::cmp::PartialEq">更多信息</a></p>'),
            ('<p>Tests for <code>!=</code>. The default implementation is almost always sufficient, and should not be overridden without very good reason. <a href="https://doc.rust-lang.org/1.95.0/core/cmp/trait.PartialEq.html" title="trait core::cmp::PartialEq">Read more</a></p>',
             '<p>测试 <code>!=</code>。默认实现几乎总是足够的，没有充分的理由不应被重写。<a href="https://doc.rust-lang.org/1.95.0/core/cmp/trait.PartialEq.html" title="trait core::cmp::PartialEq">更多信息</a></p>'),
            ('<p>Returns a copy of the value. <a href="https://doc.rust-lang.org/1.95.0/core/clone/trait.Clone.html" title="trait core::clone::Clone">Read more</a></p>',
             '<p>返回该值的副本。<a href="https://doc.rust-lang.org/1.95.0/core/clone/trait.Clone.html" title="trait core::clone::Clone">更多信息</a></p>'),
        ],
    ),
    # ----- impl-Hash (algorithm-1) trait method docblocks (for KeyPair, PublicKey, SubjectPublicKeyInfo, SignatureAlgorithm) -----
    # These are displayed in each impl block
    (
        'struct.KeyPair.html',
        [
            # 28th OWN untranslated was for KeyPair's der_bytes, algorithm-1, sign (impl PublicKeyData + impl SigningKey)
            ('<p>Sign the provided message bytestring using <code>Self</code>.\r\n'
             'Returns the signature as a DER-encoded <code>Document</code>.</p>',
             '<p>使用 <code>Self</code> 对给定的消息字节串进行签名。\n'
             '返回以 DER 编码的 <code>Document</code> 作为签名结果。</p>'),
        ],
    ),
    (
        'struct.PublicKey.html',
        [
            ('<p>The public key in DER format</p>',
             '<p>DER 格式的公钥</p>'),
            ('<p>The algorithm used by the key pair</p>',
             '<p>该密钥对所使用的算法</p>'),
        ],
    ),
    (
        'struct.SubjectPublicKeyInfo.html',
        [
            ('<p>The public key in DER format</p>',
             '<p>DER 格式的公钥</p>'),
            ('<p>The algorithm used by the key pair</p>',
             '<p>该密钥对所使用的算法</p>'),
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
