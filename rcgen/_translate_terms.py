"""Translate all OWN untranslated docblocks in rcgen.

Helper `tr()` automatically converts ASCII ' to U+2019 (right single
quotation mark), "..." to "...""/"..."" (U+201C/201D), and -- to
U+2013 (en-dash), which matches the bytes in the rustdoc-generated HTML.

Run: python rcgen/_translate_terms.py
"""
import os
import re

BASE = 'D:/Administrator/Documents/Code/rust_doc_all/rcgen'


def tr(s: str) -> str:
    """Normalize ASCII punctuation to the forms rustdoc emits."""
    # "..."" → "...""  (open/close curly quotes)
    s = re.sub(r'(?<!\s)"(?=\S)', '“', s)   # opening curly
    s = re.sub(r'(?<=\S)"(?=[\s.,;!?)\]:}])', '”', s)  # closing curly
    # '...' → '...' (right single quote)
    s = re.sub(r"'", '’', s)
    # -- → –
    s = re.sub(r'--', '–', s)
    return s


# ----- Chrome 残余 -----
CHROME = [
    ('Type Aliases', '类型别名'),
    ('Statics', '静态项'),
    ('List of all items', '本 crate 中的所有条目'),
]


JOBS = [
    # ----- index.html -----
    (
        'index.html',
        [
            (tr('<p>Rust X.509 certificate generation utility</p>'),
             '<p>Rust 的 X.509 证书生成工具</p>'),
            (tr('<p>This crate provides a way to generate self signed X.509 certificates.</p>'),
             '<p>本 crate 提供一种生成自签名 X.509 证书的方法。</p>'),
            (tr('<p>The most simple way of using this crate is by calling\n'
                'the <a href="fn.generate_simple_self_signed.html" title="fn rcgen::generate_simple_self_signed"><code>generate_simple_self_signed</code></a> function.\n'
                'For more customization abilities, construct a <a href="struct.CertificateParams.html" title="struct rcgen::CertificateParams"><code>CertificateParams</code></a> and a key pair to call\n'
                '<a href="struct.CertificateParams.html#method.signed_by" title="method rcgen::CertificateParams::signed_by"><code>CertificateParams::signed_by()</code></a> or\n'
                '<a href="struct.CertificateParams.html#method.self_signed" title="method rcgen::CertificateParams::self_signed"><code>CertificateParams::self_signed()</code></a>.</p>'),
             '<p>使用本 crate 最简单的方式是调用 <a href="fn.generate_simple_self_signed.html" title="fn rcgen::generate_simple_self_signed"><code>generate_simple_self_signed</code></a> 函数。\n'
             '如果需要更强的定制能力，可以构造一个 <a href="struct.CertificateParams.html" title="struct rcgen::CertificateParams"><code>CertificateParams</code></a> 与一个密钥对，然后调用\n'
             '<a href="struct.CertificateParams.html#method.signed_by" title="method rcgen::CertificateParams::signed_by"><code>CertificateParams::signed_by()</code></a> 或\n'
             '<a href="struct.CertificateParams.html#method.self_signed" title="method rcgen::CertificateParams::self_signed"><code>CertificateParams::self_signed()</code></a>。</p>'),
        ],
    ),
    # ----- enum.BasicConstraints.html -----
    (
        'enum.BasicConstraints.html',
        [
            ('<p>No constraint</p>', '<p>不约束</p>'),
            (tr('<p>Constrain to the contained number of intermediate certificates</p>'),
             '<p>将中间证书的数量限制为所包含的数值</p>'),
        ],
    ),
    # ----- enum.CidrSubnet.html -----
    (
        'enum.CidrSubnet.html',
        [
            (tr('<p>CIDR subnet, as per <a href="https://tools.ietf.org/html/rfc4632">RFC 4632</a></p>'),
             '<p>CIDR 子网，遵循 <a href="https://tools.ietf.org/html/rfc4632">RFC 4632</a> 的规定</p>'),
            (tr('<p>You might know CIDR subnets better by their textual representation\n'
                'where they consist of an ip address followed by a slash and a prefix\n'
                'number, for example <code>192.168.99.0/24</code>.</p>'),
             '<p>你可能更熟悉 CIDR 子网的文本表示形式：由一个 IP 地址后接斜杠与一个前缀数字组成，\n'
             '例如 <code>192.168.99.0/24</code>。</p>'),
            (tr('<p>The first field in the enum is the address, the second is the mask.\n'
                'Both are specified in network byte order.</p>'),
             '<p>枚举的第一个字段是地址，第二个字段是掩码。两者均以网络字节序表示。</p>'),
            (tr('<p>Obtains the CidrSubnet from an ip address\n'
                'as well as the specified prefix number.</p>'),
             '<p>从一个 IP 地址与指定的前缀长度构造 <code>CidrSubnet</code>。</p>'),
            (tr('<p>Obtains the CidrSubnet from an IPv4 address in network byte order\n'
                'as well as the specified prefix.</p>'),
             '<p>从一个以网络字节序表示的 IPv4 地址与指定的前缀长度构造 <code>CidrSubnet</code>。</p>'),
            (tr('<p>Obtains the CidrSubnet from an IPv6 address in network byte order\n'
                'as well as the specified prefix.</p>'),
             '<p>从一个以网络字节序表示的 IPv6 地址与指定的前缀长度构造 <code>CidrSubnet</code>。</p>'),
            (tr('<p>Obtains the CidrSubnet from the well-known\n'
                'addr/prefix notation.</p>'),
             '<p>从常见的 addr/prefix 表示法构造 <code>CidrSubnet</code>。</p>'),
        ],
    ),
    # ----- enum.CrlScope.html -----
    (
        'enum.CrlScope.html',
        [
            (tr('<p>Describes the scope of a CRL for an issuing distribution point extension.</p>'),
             '<p>为 issuing distribution point 扩展描述一个 CRL 的覆盖范围。</p>'),
            (tr('<p>The CRL contains only end-entity user certificates.</p>'),
             '<p>该 CRL 仅包含终端用户证书。</p>'),
            (tr('<p>The CRL contains only CA certificates.</p>'),
             '<p>该 CRL 仅包含 CA 证书。</p>'),
        ],
    ),
    # ----- enum.DnType.html -----
    (
        'enum.DnType.html',
        [
            (tr('<p>The attribute type of a distinguished name entry</p>'),
             '<p>一个 distinguished name 条目的属性类型</p>'),
            ('<p>X520countryName</p>', '<p>X520countryName（国家名称）</p>'),
            ('<p>X520LocalityName</p>', '<p>X520LocalityName（所在地）</p>'),
            ('<p>X520StateOrProvinceName</p>', '<p>X520StateOrProvinceName（州/省）</p>'),
            ('<p>X520OrganizationName</p>', '<p>X520OrganizationName（组织名）</p>'),
            ('<p>X520OrganizationalUnitName</p>', '<p>X520OrganizationalUnitName（组织单位）</p>'),
            ('<p>X520CommonName</p>', '<p>X520CommonName（通用名）</p>'),
            (tr('<p>Custom distinguished name type</p>'),
             '<p>自定义的 distinguished name 类型</p>'),
            (tr('<p>Generate a DnType for the provided OID</p>'),
             '<p>为给定的 OID 构造一个 <code>DnType</code></p>'),
        ],
    ),
    # ----- enum.DnValue.html -----
    (
        'enum.DnValue.html',
        [
            (tr('<p>A distinguished name entry</p>'),
             '<p>一个 distinguished name 条目</p>'),
            (tr('<p>A string encoded using UCS-2</p>'),
             '<p>使用 UCS-2 编码的字符串</p>'),
            (tr('<p>An ASCII string.</p>'),
             '<p>一个 ASCII 字符串。</p>'),
            # 这里源文件中的 ’ 不能用 tr() 自动转换（tr() 改 ASCII 单引号），需要直接传 U+2019
            ('<p>An ASCII string containing only A-Z, a-z, 0-9, ’()+,-./:=? and <code>&lt;SPACE&gt;</code></p>',
             '<p>一个仅包含 A-Z、a-z、0-9、’()+,-./:=? 以及 <code>&lt;SPACE&gt;</code> 的 ASCII 字符串</p>'),
            (tr('<p>A string of characters from the T.61 character set</p>'),
             '<p>一个由 T.61 字符集字符组成的字符串</p>'),
            (tr('<p>A string encoded using UTF-32</p>'),
             '<p>使用 UTF-32 编码的字符串</p>'),
            (tr('<p>A string encoded using UTF-8</p>'),
             '<p>使用 UTF-8 编码的字符串</p>'),
        ],
    ),
    # ----- enum.Error.html -----
    (
        'enum.Error.html',
        [
            (tr('<p>The error type of the rcgen crate</p>'),
             '<p>rcgen crate 的错误类型</p>'),
            (tr('<p>The given certificate couldn’t be parsed</p>'),
             '<p>给定的证书无法被解析</p>'),
            (tr('<p>The given certificate signing request couldn’t be parsed</p>'),
             '<p>给定的证书签名请求无法被解析</p>'),
            (tr('<p>The given key pair couldn’t be parsed</p>'),
             '<p>给定的密钥对无法被解析</p>'),
            (tr('<p>Invalid ASN.1 string</p>'),
             '<p>非法的 ASN.1 字符串</p>'),
            (tr('<p>An IP address was provided as a byte array, but the byte array was an invalid length.</p>'),
             '<p>IP 地址以字节数组形式提供，但该字节数组长度不合法。</p>'),
            (tr('<p>There is no support for generating\n'
                'keys for the given algorithm</p>'),
             '<p>不支持为给定的算法生成密钥</p>'),
            (tr('<p>The requested signature algorithm is not supported</p>'),
             '<p>不支持所请求的签名算法</p>'),
            # Unspecified ring error / The ring library rejected the key upon loading 含有 <code>ring</code>
            (tr('<p>Unspecified <code>ring</code> error</p>'),
             '<p>未指明的 <code>ring</code> 错误</p>'),
            (tr('<p>The <code>ring</code> library rejected the key upon loading</p>'),
             '<p><code>ring</code> 库在加载时拒绝了该密钥</p>'),
            (tr('<p>Time conversion related errors</p>'),
             '<p>时间转换相关的错误</p>'),
            (tr('<p>Error from the pem crate</p>'),
             '<p>来自 pem crate 的错误</p>'),
            (tr('<p>Error generated by a remote key operation</p>'),
             '<p>由远程密钥操作产生的错误</p>'),
            (tr('<p>Unsupported field when generating a CSR</p>'),
             '<p>生成 CSR 时遇到了不支持的字段</p>'),
            (tr('<p>Invalid certificate revocation list (CRL) next update.</p>'),
             '<p>非法的证书吊销列表（CRL）下次更新。</p>'),
            (tr('<p>CRL issuer specifies Key Usages that don’t include cRLSign.</p>'),
             '<p>CRL 颁发者所指定的 Key Usages 不包含 cRLSign。</p>'),
        ],
    ),
    # ----- enum.ExtendedKeyUsagePurpose.html -----
    (
        'enum.ExtendedKeyUsagePurpose.html',
        [
            (tr('<p>One of the purposes contained in the extended key usage extension</p>'),
             '<p>extended key usage 扩展中包含的某个用途</p>'),
            ('<p>anyExtendedKeyUsage</p>', '<p>anyExtendedKeyUsage（任意扩展密钥用途）</p>'),
            ('<p>id-kp-serverAuth</p>', '<p>id-kp-serverAuth（服务器认证）</p>'),
            ('<p>id-kp-clientAuth</p>', '<p>id-kp-clientAuth（客户端认证）</p>'),
            ('<p>id-kp-codeSigning</p>', '<p>id-kp-codeSigning（代码签名）</p>'),
            ('<p>id-kp-emailProtection</p>', '<p>id-kp-emailProtection（电子邮件保护）</p>'),
            ('<p>id-kp-timeStamping</p>', '<p>id-kp-timeStamping（时间戳）</p>'),
            ('<p>id-kp-OCSPSigning</p>', '<p>id-kp-OCSPSigning（OCSP 签名）</p>'),
            (tr('<p>A custom purpose not from the pre-specified list of purposes</p>'),
             '<p>一个不在预定义用途列表中的自定义用途</p>'),
        ],
    ),
    # ----- enum.GeneralSubtree.html -----
    (
        'enum.GeneralSubtree.html',
        [
            (tr('<p>General Subtree type.</p>'),
             '<p>General Subtree（通用子树）类型。</p>'),
            (tr('<p>This type has similarities to the SanType enum but is not equal.\n'
                'For example, GeneralSubtree has CIDR subnets for ip addresses\n'
                'while SanType has IP addresses.</p>'),
             '<p>该类型与 <code>SanType</code> 枚举相似但并不相同。\n'
             '例如，<code>GeneralSubtree</code> 中的 IP 地址是 CIDR 子网形式，而 <code>SanType</code> 中则是纯 IP 地址形式。</p>'),
            (tr('<p>Also known as E-Mail address</p>'),
             '<p>也称为电子邮件地址</p>'),
        ],
    ),
    # ----- enum.InvalidAsn1String.html -----
    (
        'enum.InvalidAsn1String.html',
        [
            (tr('<p>Invalid ASN.1 string type</p>'),
             '<p>非法的 ASN.1 字符串类型</p>'),
            (tr('<p>Invalid PrintableString type</p>'),
             '<p>非法的 PrintableString 类型</p>'),
            (tr('<p>Invalid UniversalString type</p>'),
             '<p>非法的 UniversalString 类型</p>'),
            (tr('<p>Invalid Ia5String type</p>'),
             '<p>非法的 Ia5String 类型</p>'),
            (tr('<p>Invalid TeletexString type</p>'),
             '<p>非法的 TeletexString 类型</p>'),
            (tr('<p>Invalid BmpString type</p>'),
             '<p>非法的 BmpString 类型</p>'),
        ],
    ),
    # ----- enum.IsCa.html -----
    (
        'enum.IsCa.html',
        [
            (tr('<p>Whether the certificate is allowed to sign other certificates</p>'),
             '<p>该证书是否允许对其他证书进行签名</p>'),
            (tr('<p>The certificate can only sign itself</p>'),
             '<p>该证书只能用于对自身进行签名</p>'),
            (tr('<p>The certificate can only sign itself, adding the extension and CA:FALSE</p>'),
             '<p>该证书只能用于对自身进行签名，同时会添加相应扩展以及 CA:FALSE</p>'),
            (tr('<p>The certificate may be used to sign other certificates</p>'),
             '<p>该证书可用于对其他证书进行签名</p>'),
        ],
    ),
    # ----- enum.KeyIdMethod.html -----
    (
        'enum.KeyIdMethod.html',
        [
            (tr('<p>Method to generate key identifiers from public keys.</p>'),
             '<p>从公钥生成密钥标识符（Key Identifier）的方法。</p>'),
            (tr('<p>Key identifiers should be derived from the public key data. RFC 7093 defines\n'
                'three methods to do so using a choice of SHA256 (method 1), SHA384 (method 2), or SHA512\n'
                '(method 3). In each case the first 160 bits of the hash are used as the key identifier\n'
                'to match the output length that would be produced were SHA1 used (a legacy option defined in RFC 5280).\n'
                'In addition to the RFC 7093 mechanisms, rcgen supports using a pre-specified key identifier.\n'
                'This can be helpful when working with an existing <a href="struct.Certificate.html" title="struct rcgen::Certificate"><code>Certificate</code></a>.</p>'),
             '<p>密钥标识符应从公钥数据派生。RFC 7093 规定了三种实现方式：分别使用 SHA256（方法 1）、\n'
             'SHA384（方法 2）或 SHA512（方法 3）。在每种情况下，均取哈希值的前 160 位作为密钥标识符，\n'
             '以匹配使用 SHA1（RFC 5280 中定义的遗留选项）时所产生输出的长度。\n'
             '除 RFC 7093 规定的机制外，rcgen 还支持使用预先指定的密钥标识符，\n'
             '这在与现有的 <a href="struct.Certificate.html" title="struct rcgen::Certificate"><code>Certificate</code></a> 协作时尤为便利。</p>'),
            (tr('<p>RFC 7093 method 1 - a truncated SHA256 digest.</p>'),
             '<p>RFC 7093 方法 1 —— 截取的 SHA256 摘要。</p>'),
            (tr('<p>RFC 7093 method 2 - a truncated SHA384 digest.</p>'),
             '<p>RFC 7093 方法 2 —— 截取的 SHA384 摘要。</p>'),
            (tr('<p>RFC 7093 method 3 - a truncated SHA512 digest.</p>'),
             '<p>RFC 7093 方法 3 —— 截取的 SHA512 摘要。</p>'),
            (tr('<p>Pre-specified identifier. The exact given value is used as the key identifier.</p>'),
             '<p>预先指定的标识符。直接使用给定的值作为密钥标识符。</p>'),
        ],
    ),
    # ----- enum.KeyUsagePurpose.html -----
    (
        'enum.KeyUsagePurpose.html',
        [
            (tr('<p>One of the purposes contained in the key usage extension</p>'),
             '<p>key usage 扩展中包含的某个用途</p>'),
            ('<p>digitalSignature</p>', '<p>digitalSignature（数字签名）</p>'),
            ('<p>contentCommitment / nonRepudiation</p>', '<p>contentCommitment / nonRepudiation（内容承诺 / 不可否认）</p>'),
            ('<p>keyEncipherment</p>', '<p>keyEncipherment（密钥加密）</p>'),
            (tr('<p>dataEncipherment</p>'),
             '<p>dataEncipherment（数据加密）</p>'),
            ('<p>keyAgreement</p>', '<p>keyAgreement（密钥协商）</p>'),
            ('<p>keyCertSign</p>', '<p>keyCertSign（证书签名）</p>'),
            ('<p>cRLSign</p>', '<p>cRLSign（CRL 签名）</p>'),
            ('<p>encipherOnly</p>', '<p>encipherOnly（仅加密）</p>'),
            ('<p>decipherOnly</p>', '<p>decipherOnly（仅解密）</p>'),
        ],
    ),
    # ----- enum.OtherNameValue.html -----
    (
        'enum.OtherNameValue.html',
        [
            (tr('<p>An OtherName value, defined in RFC 5280§4.1.2.4.</p>'),
             '<p>一个 OtherName 值，定义见 RFC 5280 §4.1.2.4。</p>'),
            (tr('<p>While the standard specifies this could be any ASN.1 type rcgen limits\n'
                'the value to a UTF-8 encoded string as this will cover the most common\n'
                'use cases, for instance smart card user principal names (UPN).</p>'),
             '<p>尽管标准规定它可以是任意 ASN.1 类型，rcgen 将其值限定为 UTF-8 编码的字符串，\n'
             '因为这已能覆盖最常见的用例，例如智能卡用户主体名称（UPN）。</p>'),
        ],
    ),
    # ----- enum.RevocationReason.html -----
    (
        'enum.RevocationReason.html',
        [
            (tr('<p>Identifies the reason a certificate was revoked. See RFC 5280 §5.3.1</p>'),
             '<p>指明证书被吊销的原因。参见 RFC 5280 §5.3.1</p>'),
        ],
    ),
    # ----- enum.SanType.html -----
    (
        'enum.SanType.html',
        [
            (tr('<p>The type of subject alt name</p>'),
             '<p>主题备用名称（Subject Alternative Name）的类型</p>'),
        ],
    ),
    # ----- struct.Attribute.html -----
    (
        'struct.Attribute.html',
        [
            (tr('<p>A PKCS #10 CSR attribute, as defined in RFC 5280 and constrained by RFC 2986.</p>'),
             '<p>一个 PKCS #10 CSR 属性，定义见 RFC 5280，并由 RFC 2986 加以约束。</p>'),
            (tr('<p>AttributeType of the Attribute, defined as an OBJECT IDENTIFIER.</p>'),
             '<p>属性的 AttributeType，定义为 OBJECT IDENTIFIER。</p>'),
            (tr('<p>DER-encoded values of the Attribute, defined by RFC 2986 as:</p>'),
             '<p>属性的 DER 编码值，由 RFC 2986 定义如下：</p>'),
        ],
    ),
    # ----- struct.Certificate.html -----
    (
        'struct.Certificate.html',
        [
            (tr('<p>An issued certificate</p>'),
             '<p>一份已颁发的证书</p>'),
            (tr('<p>Get the certificate in DER encoded format.</p>'),
             '<p>获取该证书的 DER 编码形式。</p>'),
            # 链接路径是 ../rustls_pki_types/...（在子目录里的同结构）, 根目录下是 rustls_pki_types/...
            (tr('<p><a href="../rustls_pki_types/struct.CertificateDer.html" title="struct rustls_pki_types::CertificateDer"><code>CertificateDer</code></a> implements <code>Deref&lt;Target = [u8]&gt;</code> and <code>AsRef&lt;[u8]&gt;</code>, so you can easily\n'
                'extract the DER bytes from the return value.</p>'),
             '<p><a href="../rustls_pki_types/struct.CertificateDer.html" title="struct rustls_pki_types::CertificateDer"><code>CertificateDer</code></a> 实现了 <code>Deref&lt;Target = [u8]&gt;</code> 与 <code>AsRef&lt;[u8]&gt;</code>，\n'
             '因此你可以很方便地从返回值中提取出 DER 字节。</p>'),
            (tr('<p>Get the certificate in PEM encoded format.</p>'),
             '<p>获取该证书的 PEM 编码形式。</p>'),
        ],
    ),
    # ----- struct.CertificateParams.html -----
    (
        'struct.CertificateParams.html',
        [
            (tr('<p>Parameters used for certificate generation</p>'),
             '<p>用于生成证书的参数</p>'),
            (tr('<p>An optional list of certificate revocation list (CRL) distribution points as described\n'
                'in RFC 5280 Section 4.2.1.13<sup id="fnref1"><a href="#fn1">1</a></sup>. Each distribution point contains one or more URIs where\n'
                'an up-to-date CRL with scope including this certificate can be retrieved.</p>'),
             '<p>一个可选的证书吊销列表（CRL）分发点列表，参见 <a href="https://www.rfc-editor.org/rfc/rfc5280#section-4.2.1.13">RFC 5280 §4.2.1.13</a>。\n'
             '每个分发点包含一个或多个 URI，可从这些 URI 获取覆盖本证书范围的最新 CRL。</p>'),
            # 撇号是 U+2018/U+2019
            ('<p>If <code>true</code>, the ‘Authority Key Identifier’ extension will be added to the generated cert</p>',
             '<p>若 <code>true</code>，则会在生成的证书中加入 ‘Authority Key Identifier’（颁发者密钥标识符）扩展</p>'),
            (tr('<p>Method to generate key identifiers from public keys</p>'),
             '<p>从公钥生成密钥标识符的方法</p>'),
            (tr('<p>Defaults to a truncated SHA-256 digest. See <a href="enum.KeyIdMethod.html" title="enum rcgen::KeyIdMethod"><code>KeyIdMethod</code></a> for more information.</p>'),
             '<p>默认为截取的 SHA-256 摘要。详见 <a href="enum.KeyIdMethod.html" title="enum rcgen::KeyIdMethod"><code>KeyIdMethod</code></a>。</p>'),
            (tr('<p>Generate certificate parameters with reasonable defaults</p>'),
             '<p>使用合理的默认值生成证书参数</p>'),
            (tr('<p>Generate a new certificate from the given parameters, signed by the provided issuer.</p>'),
             '<p>根据给定参数生成一份新证书，由所提供的颁发者签名。</p>'),
            (tr('<p>The returned certificate will have its issuer field set to the subject of the\n'
                'provided <code>issuer</code>, and the authority key identifier extension will be populated using\n'
                'the subject public key of <code>issuer</code> (typically either a <a href="struct.CertificateParams.html" title="struct rcgen::CertificateParams"><code>CertificateParams</code></a> or\n'
                '<a href="struct.Certificate.html" title="struct rcgen::Certificate"><code>Certificate</code></a>). It will be signed by <code>issuer_key</code>.</p>'),
             '<p>返回的证书会将其 issuer 字段设置为所提供 <code>issuer</code> 的 subject，\n'
             '并使用 <code>issuer</code> 的 subject 公钥填充 authority key identifier 扩展\n'
             '（<code>issuer</code> 通常是一个 <a href="struct.CertificateParams.html" title="struct rcgen::CertificateParams"><code>CertificateParams</code></a> 或 <a href="struct.Certificate.html" title="struct rcgen::Certificate"><code>Certificate</code></a>）。\n'
             '该证书将由 <code>issuer_key</code> 进行签名。</p>'),
            (tr('<p>Note that no validation of the <code>issuer</code> certificate is performed. Rcgen will not require\n'
                'the certificate to be a CA certificate, or have key usage extensions that allow signing.</p>'),
             '<p>请注意，<code>issuer</code> 证书不会经过任何验证。rcgen 不会强制要求该证书是 CA 证书，\n'
             '也不会要求其具有允许签名的 key usage 扩展。</p>'),
            (tr('<p>The returned <a href="struct.Certificate.html" title="struct rcgen::Certificate"><code>Certificate</code></a> may be serialized using <a href="struct.Certificate.html#method.der" title="method rcgen::Certificate::der"><code>Certificate::der</code></a> and\n'
                '<a href="struct.Certificate.html#method.pem" title="method rcgen::Certificate::pem"><code>Certificate::pem</code></a>.</p>'),
             '<p>返回的 <a href="struct.Certificate.html" title="struct rcgen::Certificate"><code>Certificate</code></a> 可通过 <a href="struct.Certificate.html#method.der" title="method rcgen::Certificate::der"><code>Certificate::der</code></a> 与\n'
             '<a href="struct.Certificate.html#method.pem" title="method rcgen::Certificate::pem"><code>Certificate::pem</code></a> 进行序列化。</p>'),
            (tr('<p>Generates a new self-signed certificate from the given parameters.</p>'),
             '<p>根据给定参数生成一份新的自签名证书。</p>'),
            (tr('<p>Calculates a subject key identifier for the certificate subject’s public key.\n'
                'This key identifier is used in the SubjectKeyIdentifier X.509v3 extension.</p>'),
             '<p>为证书 subject 的公钥计算 subject key identifier。\n'
             '该密钥标识符用于 SubjectKeyIdentifier 这个 X.509v3 扩展。</p>'),
            (tr('<p>Generate and serialize a certificate signing request (CSR).</p>'),
             '<p>生成并将一个证书签名请求（CSR）序列化。</p>'),
            (tr('<p>The constructed CSR will contain attributes based on the certificate parameters,\n'
                'and include the subject public key information from <code>subject_key</code>. Additionally,\n'
                'the CSR will be signed using the subject key.</p>'),
             '<p>所构造的 CSR 将包含基于证书参数得到的属性，\n'
             '并携带来自 <code>subject_key</code> 的 subject 公钥信息。\n'
             '此外，CSR 将使用 subject 密钥进行签名。</p>'),
            (tr('<p>Note that subsequent invocations of <code>serialize_request()</code> will not produce the exact\n'
                'same output.</p>'),
             '<p>请注意，重复调用 <code>serialize_request()</code> 不会得到完全相同的输出。</p>'),
            (tr('<p>Generate and serialize a certificate signing request (CSR) with custom PKCS #10 attributes.\n'
                'as defined in <a href="https://datatracker.ietf.org/doc/html/rfc2986#section-4">RFC 2986</a>.</p>'),
             '<p>生成并将一个带有自定义 PKCS #10 属性的证书签名请求（CSR）序列化，\n'
             '属性定义见 <a href="https://datatracker.ietf.org/doc/html/rfc2986#section-4">RFC 2986</a>。</p>'),
            (tr('<p>The constructed CSR will contain attributes based on the certificate parameters,\n'
                'and include the subject public key information from <code>subject_key</code>. Additionally,\n'
                'the CSR will be self-signed using the subject key.</p>'),
             '<p>所构造的 CSR 将包含基于证书参数得到的属性，\n'
             '并携带来自 <code>subject_key</code> 的 subject 公钥信息。\n'
             '此外，CSR 将使用 subject 密钥进行自签名。</p>'),
            (tr('<p>Note that subsequent invocations of <code>serialize_request_with_attributes()</code> will not produce the exact\n'
                'same output.</p>'),
             '<p>请注意，重复调用 <code>serialize_request_with_attributes()</code> 不会得到完全相同的输出。</p>'),
            (tr('<p>Insert an extended key usage (EKU) into the parameters if it does not already exist</p>'),
             '<p>若参数中尚未存在指定的 extended key usage（EKU），则将其插入</p>'),
        ],
    ),
    # ----- struct.CertificateRevocationList.html -----
    (
        'struct.CertificateRevocationList.html',
        [
            (tr('<p>A certificate revocation list (CRL)</p>'),
             '<p>一个证书吊销列表（CRL）</p>'),
            (tr('<p>Get the CRL in PEM encoded format.</p>'),
             '<p>获取该 CRL 的 PEM 编码形式。</p>'),
            (tr('<p>Get the CRL in DER encoded format.</p>'),
             '<p>获取该 CRL 的 DER 编码形式。</p>'),
            (tr('<p><a href="../rustls_pki_types/struct.CertificateRevocationListDer.html" title="struct rustls_pki_types::CertificateRevocationListDer"><code>CertificateRevocationListDer</code></a> implements <code>Deref&lt;Target = [u8]&gt;</code> and <code>AsRef&lt;[u8]&gt;</code>,\n'
                'so you can easily extract the DER bytes from the return value.</p>'),
             '<p><a href="../rustls_pki_types/struct.CertificateRevocationListDer.html" title="struct rustls_pki_types::CertificateRevocationListDer"><code>CertificateRevocationListDer</code></a> 实现了 <code>Deref&lt;Target = [u8]&gt;</code> 与 <code>AsRef&lt;[u8]&gt;</code>，\n'
             '因此你可以很方便地从返回值中提取出 DER 字节。</p>'),
        ],
    ),
    # ----- struct.CertificateRevocationListParams.html -----
    (
        'struct.CertificateRevocationListParams.html',
        [
            (tr('<p>Parameters used for certificate revocation list (CRL) generation</p>'),
             '<p>用于生成证书吊销列表（CRL）的参数</p>'),
            (tr('<p>Issue date of the CRL.</p>'),
             '<p>该 CRL 的颁发日期。</p>'),
            (tr('<p>The date by which the next CRL will be issued.</p>'),
             '<p>下一份 CRL 将被颁发的日期。</p>'),
            (tr('<p>A monotonically increasing sequence number for a given CRL scope and issuer.</p>'),
             '<p>对于给定 CRL 范围与颁发者而言单调递增的序列号。</p>'),
            (tr('<p>An optional CRL extension identifying the CRL distribution point and scope for a\n'
                'particular CRL as described in RFC 5280 Section 5.2.5<sup id="fnref1"><a href="#fn1">1</a></sup>.</p>'),
             '<p>一个可选的 CRL 扩展，用于指明特定 CRL 的分发点与覆盖范围，\n'
             '参见 <a href="https://datatracker.ietf.org/doc/html/rfc5280#section-5.2.5">RFC 5280 §5.2.5</a>。</p>'),
            (tr('<p>A list of zero or more parameters describing revoked certificates included in the CRL.</p>'),
             '<p>包含在 CRL 中的、零个或多个已吊销证书的描述参数列表。</p>'),
            (tr('<p>Defaults to SHA-256.</p>'),
             '<p>默认为 SHA-256。</p>'),
            (tr('<p>Serializes the certificate revocation list (CRL).</p>'),
             '<p>将该证书吊销列表（CRL）序列化。</p>'),
            (tr('<p>Including a signature from the issuing certificate authority’s key.</p>'),
             '<p>其中包含由颁发该 CRL 的证书颁发机构密钥产生的签名。</p>'),
        ],
    ),
    # ----- struct.CertificateSigningRequest.html -----
    (
        'struct.CertificateSigningRequest.html',
        [
            (tr('<p>A certificate signing request (CSR) that can be encoded to PEM or DER.</p>'),
             '<p>一个可被编码为 PEM 或 DER 形式的证书签名请求（CSR）。</p>'),
            (tr('<p>Get the PEM-encoded bytes of the certificate signing request.</p>'),
             '<p>获取该证书签名请求的 PEM 编码字节。</p>'),
            (tr('<p>Get the DER-encoded bytes of the certificate signing request.</p>'),
             '<p>获取该证书签名请求的 DER 编码字节。</p>'),
            (tr('<p><a href="../rustls_pki_types/struct.CertificateSigningRequestDer.html" title="struct rustls_pki_types::CertificateSigningRequestDer"><code>CertificateSigningRequestDer</code></a> implements <code>Deref&lt;Target = [u8]&gt;</code> and <code>AsRef&lt;[u8]&gt;</code>,\n'
                'so you can easily extract the DER bytes from the return value.</p>'),
             '<p><a href="../rustls_pki_types/struct.CertificateSigningRequestDer.html" title="struct rustls_pki_types::CertificateSigningRequestDer"><code>CertificateSigningRequestDer</code></a> 实现了 <code>Deref&lt;Target = [u8]&gt;</code> 与 <code>AsRef&lt;[u8]&gt;</code>，\n'
             '因此你可以很方便地从返回值中提取出 DER 字节。</p>'),
        ],
    ),
    # ----- struct.CertificateSigningRequestParams.html -----
    (
        'struct.CertificateSigningRequestParams.html',
        [
            (tr('<p>Parameters for a certificate signing request</p>'),
             '<p>证书签名请求的参数</p>'),
            (tr('<p>Parameters for the certificate to be signed.</p>'),
             '<p>待签名证书的参数。</p>'),
            (tr('<p>Public key to include in the certificate signing request.</p>'),
             '<p>将包含在证书签名请求中的公钥。</p>'),
            (tr('<p>Generate a new certificate based on the requested parameters, signed by the provided\n'
                'issuer.</p>'),
             '<p>根据所请求的参数生成一份新证书，由所提供的颁发者签名。</p>'),
            (tr('<p>The returned certificate will have its issuer field set to the subject of the provided\n'
                'issuer, and the authority key identifier extension will be populated using the subject\n'
                'public key of issuer. It will be signed by issuer_key.</p>'),
             '<p>返回的证书会将其 issuer 字段设置为所提供颁发者的 subject，\n'
             '并使用颁发者的 subject 公钥填充 authority key identifier 扩展。该证书将由 <code>issuer_key</code> 进行签名。</p>'),
            (tr('<p>Note that no validation of the <code>issuer</code> certificate is performed. Rcgen will not require\n'
                'the certificate to be a CA certificate, or have key usage extensions that allow signing.</p>'),
             '<p>请注意，<code>issuer</code> 证书不会经过任何验证。rcgen 不会强制要求该证书是 CA 证书，\n'
             '也不会要求其具有允许签名的 key usage 扩展。</p>'),
            (tr('<p>The returned <a href="struct.Certificate.html" title="struct rcgen::Certificate"><code>Certificate</code></a> may be serialized using <a href="struct.Certificate.html#method.der" title="method rcgen::Certificate::der"><code>Certificate::der</code></a> and\n'
                '<a href="struct.Certificate.html#method.pem" title="method rcgen::Certificate::pem"><code>Certificate::pem</code></a>.</p>'),
             '<p>返回的 <a href="struct.Certificate.html" title="struct rcgen::Certificate"><code>Certificate</code></a> 可通过 <a href="struct.Certificate.html#method.der" title="method rcgen::Certificate::der"><code>Certificate::der</code></a> 与\n'
             '<a href="struct.Certificate.html#method.pem" title="method rcgen::Certificate::pem"><code>Certificate::pem</code></a> 进行序列化。</p>'),
        ],
    ),
    # ----- struct.CertifiedIssuer.html -----
    (
        'struct.CertifiedIssuer.html',
        [
            (tr('<p>An <a href="struct.Issuer.html" title="struct rcgen::Issuer"><code>Issuer</code></a> wrapper that also contains the issuer’s <a href="struct.Certificate.html" title="struct rcgen::Certificate"><code>Certificate</code></a>.</p>'),
             '<p>一个 <a href="struct.Issuer.html" title="struct rcgen::Issuer"><code>Issuer</code></a> 包装，同时包含颁发者的 <a href="struct.Certificate.html" title="struct rcgen::Certificate"><code>Certificate</code></a>。</p>'),
            (tr('<p>Create a new issuer from the given parameters and key, with a self-signed certificate.</p>'),
             '<p>使用给定参数与密钥创建一个新的颁发者，附带一份自签名证书。</p>'),
            # 注意：有 <code>issuer</code> 版本和无 <code>issuer</code> 版本
            (tr('<p>Create a new issuer from the given parameters and key, signed by the given <code>issuer</code>.</p>'),
             '<p>使用给定参数与密钥创建一个新的颁发者，并由指定的 <code>issuer</code> 签名。</p>'),
            (tr('<p>Get the certificate in PEM encoded format.</p>'),
             '<p>获取该证书的 PEM 编码形式。</p>'),
            (tr('<p>Get the certificate in DER encoded format.</p>'),
             '<p>获取该证书的 DER 编码形式。</p>'),
            (tr('<p>See also <a href="struct.Certificate.html#method.der" title="method rcgen::Certificate::der"><code>Certificate::der()</code></a></p>'),
             '<p>另请参见 <a href="struct.Certificate.html#method.der" title="method rcgen::Certificate::der"><code>Certificate::der()</code></a></p>'),
            (tr('<p>Allowed key usages for this issuer.</p>'),
             '<p>此颁发者所允许的 key usage。</p>'),
            (tr('<p>Yield a reference to the signing key.</p>'),
             '<p>返回签名密钥的引用。</p>'),
        ],
    ),
    # ----- struct.CertifiedKey.html -----
    (
        'struct.CertifiedKey.html',
        [
            (tr('<p>An issued certificate, together with the subject keypair.</p>'),
             '<p>一份已颁发的证书，连同其 subject 密钥对。</p>'),
            (tr('<p>An issued certificate.</p>'),
             '<p>一份已颁发的证书。</p>'),
            (tr('<p>The certificate’s subject signing key.</p>'),
             '<p>该证书的 subject 签名密钥。</p>'),
        ],
    ),
    # ----- struct.CrlDistributionPoint.html -----
    (
        'struct.CrlDistributionPoint.html',
        [
            (tr('<p>A certificate revocation list (CRL) distribution point, to be included in a certificate’s distribution points extension or a CRL’s issuing distribution point extension</p>'),
             '<p>一个证书吊销列表（CRL）分发点，可包含在证书的 distribution points 扩展或 CRL 的 issuing distribution point 扩展中</p>'),
            (tr('<p>One or more URI distribution point names, indicating a place the current CRL can\n'
                'be retrieved. When present, SHOULD include at least one LDAP or HTTP URI.</p>'),
             '<p>一个或多个 URI 形式的分发点名称，指明可获取当前 CRL 的位置。\n'
             '若提供，应至少包含一个 LDAP 或 HTTP URI。</p>'),
        ],
    ),
    # ----- struct.CrlIssuingDistributionPoint.html -----
    (
        'struct.CrlIssuingDistributionPoint.html',
        [
            (tr('<p>A certificate revocation list (CRL) issuing distribution point, to be included in a CRL’s issuing distribution point extension.</p>'),
             '<p>一个证书吊销列表（CRL）颁发分发点，包含在 CRL 的 issuing distribution point 扩展中。</p>'),
            (tr('<p>The CRL’s distribution point, containing a sequence of URIs the CRL can be retrieved from.</p>'),
             '<p>该 CRL 的分发点，包含一组可从中获取该 CRL 的 URI。</p>'),
            (tr('<p>An optional description of the CRL’s scope. If omitted, the CRL may contain\n'
                'both user certs and CA certs.</p>'),
             '<p>该 CRL 覆盖范围的可选描述。若省略，则该 CRL 可同时包含用户证书与 CA 证书。</p>'),
        ],
    ),
    # ----- struct.CustomExtension.html -----
    (
        'struct.CustomExtension.html',
        [
            (tr('<p>A custom extension of a certificate, as specified in RFC 5280</p>'),
             '<p>证书的一个自定义扩展，定义见 RFC 5280</p>'),
            (tr('<p>Creates a new acmeIdentifier extension for ACME TLS-ALPN-01\n'
                'as specified in <a href="https://datatracker.ietf.org/doc/html/rfc8737">RFC 8737</a></p>'),
             '<p>为 ACME TLS-ALPN-01 创建一个新的 acmeIdentifier 扩展，\n'
             '定义见 <a href="https://datatracker.ietf.org/doc/html/rfc8737">RFC 8737</a></p>'),
            (tr('<p>Panics if the passed <code>sha_digest</code> parameter doesn’t hold 32 bytes (256 bits).</p>'),
             '<p>若传入的 <code>sha_digest</code> 参数不包含 32 字节（256 位），则引发 panic。</p>'),
            (tr('<p>Create a new custom extension with the specified content</p>'),
             '<p>使用指定内容创建一个新的自定义扩展</p>'),
            (tr('<p>Sets the criticality flag of the extension.</p>'),
             '<p>设置该扩展的 criticality 标志。</p>'),
            (tr('<p>Obtains the criticality flag of the extension.</p>'),
             '<p>获取该扩展的 criticality 标志。</p>'),
            (tr('<p>Obtains the content of the extension.</p>'),
             '<p>获取该扩展的内容。</p>'),
            (tr('<p>Obtains the OID components of the extensions, as u64 pieces</p>'),
             '<p>获取该扩展的 OID 组成部分，以 <code>u64</code> 形式给出</p>'),
        ],
    ),
    # ----- struct.DistinguishedName.html -----
    (
        'struct.DistinguishedName.html',
        [
            (tr('<p>Distinguished name used e.g. for the issuer and subject fields of a certificate</p>'),
             '<p>用于（例如）证书 issuer 与 subject 字段的 distinguished name</p>'),
            (tr('<p>A distinguished name is a set of (attribute type, attribute value) tuples. This datastructure keeps them ordered by insertion order.\n'
                'See also the RFC 5280 sections on the issuer and subject fields.</p>'),
             '<p>distinguished name 是一组 (属性类型, 属性值) 元组。本数据结构按插入顺序保存这些元组。\n'
             '另请参阅 RFC 5280 中有关 issuer 与 subject 字段的小节。</p>'),
            (tr('<p>Creates a new, empty distinguished name</p>'),
             '<p>创建一个新的、空的 distinguished name</p>'),
            (tr('<p>Obtains the attribute value for the given attribute type</p>'),
             '<p>获取给定属性类型对应的属性值</p>'),
            (tr('<p>Removes the attribute with the specified DnType</p>'),
             '<p>移除具有指定 <code>DnType</code> 的属性</p>'),
            (tr('<p>Returns true when an actual removal happened, false\n'
                'when no attribute with the specified DnType was\n'
                'found.</p>'),
             '<p>若确实发生了移除则返回 true；若未找到具有指定 <code>DnType</code> 的属性则返回 false。</p>'),
            (tr('<p>Inserts or updates an attribute that consists of type and name</p>'),
             '<p>插入或更新一个由类型与名称组成的属性</p>'),
            (tr('<p>Iterate over the entries</p>'),
             '<p>遍历各个条目</p>'),
        ],
    ),
    # ----- struct.DistinguishedNameIterator.html -----
    (
        'struct.DistinguishedNameIterator.html',
        [
            (tr('<p>Iterator over <a href="struct.DistinguishedName.html" title="struct rcgen::DistinguishedName"><code>DistinguishedName</code></a> entries</p>'),
             '<p>对 <a href="struct.DistinguishedName.html" title="struct rcgen::DistinguishedName"><code>DistinguishedName</code></a> 条目的迭代器</p>'),
        ],
    ),
    # ----- struct.Issuer.html -----
    (
        'struct.Issuer.html',
        [
            (tr('<p>An issuer that can sign certificates. Encapsulates the distinguished name, key identifier method, key usages and signing key of the issuing certificate.</p>'),
             '<p>一个能够对证书进行签名的颁发者。它封装了颁发证书的 distinguished name、密钥标识符生成方法、key usage 与签名密钥。</p>'),
            (tr('<p>Create a new issuer from the given parameters and signing key.</p>'),
             '<p>使用给定参数与签名密钥创建一个新的颁发者。</p>'),
            (tr('<p>Create a new issuer from the given parameters and signing key references.</p>'),
             '<p>使用给定参数与签名密钥引用创建一个新的颁发者。</p>'),
            (tr('<p>Use <a href="struct.Issuer.html#method.new" title="associated function rcgen::Issuer::new"><code>Issuer::new</code></a> instead if you want to obtain an <a href="struct.Issuer.html" title="struct rcgen::Issuer"><code>Issuer</code></a> that owns\n'
                'its parameters.</p>'),
             '<p>若你希望获得一个拥有其参数所有权的 <a href="struct.Issuer.html" title="struct rcgen::Issuer"><code>Issuer</code></a>，请改用 <a href="struct.Issuer.html#method.new" title="associated function rcgen::Issuer::new"><code>Issuer::new</code></a>。</p>'),
            (tr('<p>Allowed key usages for this issuer.</p>'),
             '<p>此颁发者所允许的 key usage。</p>'),
            (tr('<p>Yield a reference to the signing key.</p>'),
             '<p>返回签名密钥的引用。</p>'),
            (tr('<p>Formats the issuer information without revealing the key pair.</p>'),
             '<p>格式化颁发者信息，但不泄露密钥对内容。</p>'),
        ],
    ),
    # ----- struct.KeyPair.html -----
    (
        'struct.KeyPair.html',
        [
            (tr('<p>A key pair used to sign certificates and CSRs</p>'),
             '<p>用于对证书和 CSR 进行签名的密钥对</p>'),
            (tr('<p>Generate a new random <a href="static.PKCS_ECDSA_P256_SHA256.html" title="static rcgen::PKCS_ECDSA_P256_SHA256"><code>PKCS_ECDSA_P256_SHA256</code></a> key pair</p>'),
             '<p>生成一个新的随机 <a href="static.PKCS_ECDSA_P256_SHA256.html" title="static rcgen::PKCS_ECDSA_P256_SHA256"><code>PKCS_ECDSA_P256_SHA256</code></a> 密钥对</p>'),
            (tr('<p>Generate a new random key pair for the specified signature algorithm</p>'),
             '<p>为指定的签名算法生成一个新的随机密钥对</p>'),
            (tr('<p>If you’re not sure which algorithm to use, <a href="static.PKCS_ECDSA_P256_SHA256.html" title="static rcgen::PKCS_ECDSA_P256_SHA256"><code>PKCS_ECDSA_P256_SHA256</code></a> is a good choice.\n'
                'If passed an RSA signature algorithm, it depends on the backend whether we return\n'
                'a generated key or an error for key generation being unavailable.\n'
                'Currently, only <code>aws-lc-rs</code> supports RSA key generation.</p>'),
             '<p>若你不确定该使用哪种算法，<a href="static.PKCS_ECDSA_P256_SHA256.html" title="static rcgen::PKCS_ECDSA_P256_SHA256"><code>PKCS_ECDSA_P256_SHA256</code></a> 是一个不错的选择。\n'
             '若传入的是一种 RSA 签名算法，则取决于后端实现：可能返回生成的密钥，\n'
             '也可能因不支持密钥生成而返回错误。目前只有 <code>aws-lc-rs</code> 支持 RSA 密钥生成。</p>'),
            (tr('<p>Returns the key pair’s signature algorithm</p>'),
             '<p>返回该密钥对的签名算法</p>'),
            (tr('<p>Parses the key pair from the ASCII PEM format</p>'),
             '<p>从 ASCII PEM 格式解析密钥对</p>'),
            # "..." (U+201C/U+201D)
            ('<p>If <code>aws_lc_rs</code> feature is used, then the key must be a DER-encoded plaintext private key; as specified in PKCS #8/RFC 5958, SEC1/RFC 5915, or PKCS#1/RFC 3447;\nAppears as “PRIVATE KEY”, “RSA PRIVATE KEY”, or “EC PRIVATE KEY” in PEM files.</p>',
             '<p>若使用了 <code>aws_lc_rs</code> feature，则该密钥必须是 DER 编码的明文私钥；\n规定见 PKCS #8 / RFC 5958、SEC1 / RFC 5915 或 PKCS#1 / RFC 3447；\n在 PEM 文件中以 “PRIVATE KEY”、“RSA PRIVATE KEY” 或 “EC PRIVATE KEY” 形式出现。</p>'),
            ('<p>Otherwise if the <code>ring</code> feature is used, then the key must be a DER-encoded plaintext private key; as specified in PKCS #8/RFC 5958;\nAppears as “PRIVATE KEY” in PEM files.</p>',
             '<p>若使用的是 <code>ring</code> feature，则该密钥必须是 DER 编码的明文私钥；\n规定见 PKCS #8 / RFC 5958；在 PEM 文件中以 “PRIVATE KEY” 形式出现。</p>'),
            (tr('<p>Obtains the key pair from a DER formatted key\n'
                'using the specified <a href="struct.SignatureAlgorithm.html" title="struct rcgen::SignatureAlgorithm"><code>SignatureAlgorithm</code></a></p>'),
             '<p>从 DER 格式的密钥解析出密钥对，并使用指定的 <a href="struct.SignatureAlgorithm.html" title="struct rcgen::SignatureAlgorithm"><code>SignatureAlgorithm</code></a></p>'),
            # "Same as ..." 形式有几种
            ('<p>Same as <a href="struct.KeyPair.html#method.from_pkcs8_pem_and_sign_algo" title="associated function rcgen::KeyPair::from_pkcs8_pem_and_sign_algo"><code>from_pkcs8_pem_and_sign_algo</code></a>.</p>',
             '<p>同 <a href="struct.KeyPair.html#method.from_pkcs8_pem_and_sign_algo" title="associated function rcgen::KeyPair::from_pkcs8_pem_and_sign_algo"><code>from_pkcs8_pem_and_sign_algo</code></a>。</p>'),
            # em-dash
            (tr('<p>If you have a <a href="../rustls_pki_types/struct.PrivatePkcs8KeyDer.html" title="struct rustls_pki_types::PrivatePkcs8KeyDer"><code>PrivatePkcs8KeyDer</code></a>, you can usually rely on the <a href="https://doc.rust-lang.org/1.95.0/core/convert/trait.TryFrom.html" title="trait core::convert::TryFrom"><code>TryFrom</code></a> implementation\n'
                'to obtain a <a href="struct.KeyPair.html" title="struct rcgen::KeyPair"><code>KeyPair</code></a> – it will determine the correct <a href="struct.SignatureAlgorithm.html" title="struct rcgen::SignatureAlgorithm"><code>SignatureAlgorithm</code></a> for you.\n'
                'However, sometimes multiple signature algorithms fit for the same DER key. In those instances,\n'
                'you can use this function to precisely specify the <a href="struct.SignatureAlgorithm.html" title="struct rcgen::SignatureAlgorithm"><code>SignatureAlgorithm</code></a>.</p>'),
             '<p>若你拥有一个 <a href="../rustls_pki_types/struct.PrivatePkcs8KeyDer.html" title="struct rustls_pki_types::PrivatePkcs8KeyDer"><code>PrivatePkcs8KeyDer</code></a>，通常可以依赖 <a href="https://doc.rust-lang.org/1.95.0/core/convert/trait.TryFrom.html" title="trait core::convert::TryFrom"><code>TryFrom</code></a> 实现来得到一个 <a href="struct.KeyPair.html" title="struct rcgen::KeyPair"><code>KeyPair</code></a>——\n'
             '它会为你确定正确的 <a href="struct.SignatureAlgorithm.html" title="struct rcgen::SignatureAlgorithm"><code>SignatureAlgorithm</code></a>。\n'
             '不过，有时同一段 DER 密钥可能匹配多种签名算法。这种情况下，你可以使用本函数精确地指定 <a href="struct.SignatureAlgorithm.html" title="struct rcgen::SignatureAlgorithm"><code>SignatureAlgorithm</code></a>。</p>'),
            (tr('<p><a href="https://docs.rs/rustls-pemfile/latest/rustls_pemfile/fn.private_key.html"><code>rustls_pemfile::private_key()</code></a> is often used to obtain a <a href="../rustls_pki_types/enum.PrivateKeyDer.html"><code>PrivateKeyDer</code></a> from PEM\n'
                'input. If the obtained <a href="../rustls_pki_types/enum.PrivateKeyDer.html"><code>PrivateKeyDer</code></a> is a <code>Pkcs8</code> variant, you can use its contents\n'
                'as input for this function. Alternatively, if you already have a byte slice containing DER,\n'
                'it can trivially be converted into <a href="../rustls_pki_types/struct.PrivatePkcs8KeyDer.html" title="struct rustls_pki_types::PrivatePkcs8KeyDer"><code>PrivatePkcs8KeyDer</code></a> using the <a href="https://doc.rust-lang.org/1.95.0/core/convert/trait.Into.html" title="trait core::convert::Into"><code>Into</code></a> trait.</p>'),
             '<p><a href="https://docs.rs/rustls-pemfile/latest/rustls_pemfile/fn.private_key.html"><code>rustls_pemfile::private_key()</code></a> 常用于从 PEM 输入得到 <a href="../rustls_pki_types/enum.PrivateKeyDer.html"><code>PrivateKeyDer</code></a>。\n'
             '若得到的 <a href="../rustls_pki_types/enum.PrivateKeyDer.html"><code>PrivateKeyDer</code></a> 是 <code>Pkcs8</code> 变体，你可以将它的内容作为本函数的输入。\n'
             '另外，若你已经有一段包含 DER 数据的字节切片，使用 <a href="https://doc.rust-lang.org/1.95.0/core/convert/trait.Into.html" title="trait core::convert::Into"><code>Into</code></a> trait 便可轻松地将其转换为 <a href="../rustls_pki_types/struct.PrivatePkcs8KeyDer.html" title="struct rustls_pki_types::PrivatePkcs8KeyDer"><code>PrivatePkcs8KeyDer</code></a>。</p>'),
            (tr('<p>Note that using the <code>ring</code> feature, this function only support <a href="../rustls_pki_types/enum.PrivateKeyDer.html#variant.Pkcs8" title="variant rustls_pki_types::PrivateKeyDer::Pkcs8"><code>PrivateKeyDer::Pkcs8</code></a> variant.\n'
                'Consider using the <code>aws_lc_rs</code> features to support <a href="../rustls_pki_types/enum.PrivateKeyDer.html" title="enum rustls_pki_types::PrivateKeyDer"><code>PrivateKeyDer</code></a> fully.</p>'),
             '<p>请注意，若使用 <code>ring</code> feature，本函数仅支持 <a href="../rustls_pki_types/enum.PrivateKeyDer.html#variant.Pkcs8" title="variant rustls_pki_types::PrivateKeyDer::Pkcs8"><code>PrivateKeyDer::Pkcs8</code></a> 变体。\n'
             '若需要完整支持 <a href="../rustls_pki_types/enum.PrivateKeyDer.html" title="enum rustls_pki_types::PrivateKeyDer"><code>PrivateKeyDer</code></a>，请考虑启用 <code>aws_lc_rs</code> feature。</p>'),
            (tr('<p>You can use <a href="https://docs.rs/rustls-pemfile/latest/rustls_pemfile/fn.private_key.html"><code>rustls_pemfile::private_key</code></a> to get the <code>key</code> input. If\n'
                'you have already a byte slice, just calling <code>try_into()</code> will convert it to a <a href="../rustls_pki_types/enum.PrivateKeyDer.html" title="enum rustls_pki_types::PrivateKeyDer"><code>PrivateKeyDer</code></a>.</p>'),
             '<p>你可以使用 <a href="https://docs.rs/rustls-pemfile/latest/rustls_pemfile/fn.private_key.html"><code>rustls_pemfile::private_key</code></a> 来获取密钥输入。\n'
             '若你已有字节切片，只需调用 <code>try_into()</code> 即可将其转换为 <a href="../rustls_pki_types/enum.PrivateKeyDer.html" title="enum rustls_pki_types::PrivateKeyDer"><code>PrivateKeyDer</code></a>。</p>'),
            (tr('<p>Get the raw public key of this key pair</p>'),
             '<p>获取此密钥对的原始公钥</p>'),
            (tr('<p>The key is in raw format, as how <a href="../ring/signature/trait.KeyPair.html#tymethod.public_key" title="method ring::signature::KeyPair::public_key"><code>KeyPair::public_key()</code></a>\n'
                'would output, and how <a href="../ring/signature/struct.UnparsedPublicKey.html#method.verify" title="method ring::signature::UnparsedPublicKey::verify"><code>UnparsedPublicKey::verify()</code></a>\n'
                'would accept.</p>'),
             '<p>密钥为原始格式，与 <a href="../ring/signature/trait.KeyPair.html#tymethod.public_key" title="method ring::signature::KeyPair::public_key"><code>KeyPair::public_key()</code></a> 的输出以及\n'
             '<a href="../ring/signature/struct.UnparsedPublicKey.html#method.verify" title="method ring::signature::UnparsedPublicKey::verify"><code>UnparsedPublicKey::verify()</code></a> 所接受的格式一致。</p>'),
            (tr('<p>Check if this key pair can be used with the given signature algorithm</p>'),
             '<p>检查此密钥对是否可用于给定的签名算法</p>'),
            # 撇号 ’s
            ('<p>Returns (possibly multiple) compatible <a href="struct.SignatureAlgorithm.html" title="struct rcgen::SignatureAlgorithm"><code>SignatureAlgorithm</code></a>’s\nthat the key can be used with</p>',
             '<p>返回（可能多个）此密钥可兼容使用的 <a href="struct.SignatureAlgorithm.html" title="struct rcgen::SignatureAlgorithm"><code>SignatureAlgorithm</code></a></p>'),
            (tr('<p>Return the key pair’s public key in PEM format</p>'),
             '<p>以 PEM 格式返回该密钥对的公钥</p>'),
            (tr('<p>The returned string can be interpreted with <code>openssl pkey --inform PEM -pubout -pubin -text</code></p>'),
             '<p>返回的字符串可通过 <code>openssl pkey --inform PEM -pubout -pubin -text</code> 进行解析</p>'),
            (tr('<p>Serializes the key pair (including the private key) in PKCS#8 format in DER</p>'),
             '<p>将该密钥对（包括私钥）以 PKCS#8 DER 格式序列化</p>'),
            (tr('<p>Returns a reference to the serialized key pair (including the private key)\n'
                'in PKCS#8 format in DER</p>'),
             '<p>返回该密钥对（包括私钥）以 PKCS#8 DER 格式序列化结果的引用</p>'),
            (tr('<p>Serializes the key pair (including the private key) in PKCS#8 format in PEM</p>'),
             '<p>将该密钥对（包括私钥）以 PKCS#8 PEM 格式序列化</p>'),
        ],
    ),
    # ----- struct.NameConstraints.html -----
    (
        'struct.NameConstraints.html',
        [
            (tr('<p>The NameConstraints extension (only relevant for CA certificates)</p>'),
             '<p>NameConstraints 扩展（仅对 CA 证书有意义）</p>'),
            (tr('<p>A list of subtrees that the domain has to match.</p>'),
             '<p>域名必须匹配的一组子树。</p>'),
            (tr('<p>A list of subtrees that the domain must not match.</p>'),
             '<p>域名不得匹配的一组子树。</p>'),
            (tr('<p>Any name matching an excluded subtree is invalid even if it also matches a permitted subtree.</p>'),
             '<p>任何匹配 excluded subtree 的名称都是非法的，即使它同时也匹配某个 permitted subtree。</p>'),
        ],
    ),
    # ----- struct.PublicKey.html -----
    (
        'struct.PublicKey.html',
        [
            (tr('<p>A public key, extracted from a CSR</p>'),
             '<p>从一份 CSR 中提取出的公钥</p>'),
            (tr('<p>The algorithm used to generate the public key and sign the CSR.</p>'),
             '<p>用于生成该公钥并对 CSR 进行签名的算法。</p>'),
        ],
    ),
    # ----- struct.RevokedCertParams.html -----
    (
        'struct.RevokedCertParams.html',
        [
            (tr('<p>Parameters used for describing a revoked certificate included in a <a href="struct.CertificateRevocationList.html" title="struct rcgen::CertificateRevocationList"><code>CertificateRevocationList</code></a>.</p>'),
             '<p>用于描述包含在 <a href="struct.CertificateRevocationList.html" title="struct rcgen::CertificateRevocationList"><code>CertificateRevocationList</code></a> 中的已吊销证书的参数。</p>'),
            (tr('<p>Serial number identifying the revoked certificate.</p>'),
             '<p>用于标识该已吊销证书的序列号。</p>'),
            (tr('<p>The date at which the CA processed the revocation.</p>'),
             '<p>CA 处理此次吊销的日期。</p>'),
            (tr('<p>An optional reason code identifying why the certificate was revoked.</p>'),
             '<p>一个可选的原因代码，用于指明该证书被吊销的原因。</p>'),
            (tr('<p>An optional field describing the date on which it was known or suspected that the\n'
                'private key was compromised or the certificate otherwise became invalid. This date\n'
                'may be earlier than the <a href="struct.RevokedCertParams.html#structfield.revocation_time" title="struct rcgen::RevokedCertParams::revocation_time"><code>RevokedCertParams::revocation_time</code></a>.</p>'),
             '<p>一个可选字段，描述已获知或怀疑私钥被泄露、或证书因其他原因失效的日期。\n'
             '该日期可能早于 <a href="struct.RevokedCertParams.html#structfield.revocation_time" title="struct rcgen::RevokedCertParams::revocation_time"><code>RevokedCertParams::revocation_time</code></a>。</p>'),
        ],
    ),
    # ----- struct.SerialNumber.html -----
    (
        'struct.SerialNumber.html',
        [
            (tr('<p>A certificate serial number.</p>'),
             '<p>证书的序列号。</p>'),
            (tr('<p>Create a serial number from the given byte slice.</p>'),
             '<p>从给定的字节切片构造一个序列号。</p>'),
            (tr('<p>Return the byte representation of the serial number.</p>'),
             '<p>返回该序列号的字节表示形式。</p>'),
            (tr('<p>Return the length of the serial number in bytes.</p>'),
             '<p>返回该序列号的字节长度。</p>'),
        ],
    ),
    # ----- struct.SignatureAlgorithm.html -----
    (
        'struct.SignatureAlgorithm.html',
        [
            (tr('<p>Signature algorithm type</p>'),
             '<p>签名算法类型</p>'),
            (tr('<p>Retrieve the <a href="struct.SignatureAlgorithm.html" title="struct rcgen::SignatureAlgorithm"><code>SignatureAlgorithm</code></a> for the provided OID</p>'),
             '<p>为给定的 OID 获取对应的 <a href="struct.SignatureAlgorithm.html" title="struct rcgen::SignatureAlgorithm"><code>SignatureAlgorithm</code></a></p>'),
            (tr('<p>The <code>Hash</code> trait is not derived, but implemented according to impl of the <code>PartialEq</code> trait</p>'),
             '<p>该类型并未派生 <code>Hash</code>，而是按 <code>PartialEq</code> 的实现方式手动实现</p>'),
        ],
    ),
    # ----- struct.SubjectPublicKeyInfo.html -----
    (
        'struct.SubjectPublicKeyInfo.html',
        [
            (tr('<p>A public key</p>'),
             '<p>一个公钥</p>'),
        ],
    ),
    # ----- trait.PublicKeyData.html -----
    (
        'trait.PublicKeyData.html',
        [
            (tr('<p>The public key data of a key pair</p>'),
             '<p>一个密钥对的公钥数据</p>'),
            (tr('<p>The public key in DER format</p>'),
             '<p>DER 格式的公钥</p>'),
            (tr('<p>The algorithm used by the key pair</p>'),
             '<p>该密钥对所使用的算法</p>'),
            (tr('<p>The public key data in DER format</p>'),
             '<p>DER 格式的公钥数据</p>'),
            (tr('<p>The key is formatted according to the X.509 SubjectPublicKeyInfo struct.\n'
                'See <a href="https://tools.ietf.org/html/rfc5280#section-4.1">RFC 5280 section 4.1</a>.</p>'),
             '<p>该密钥依据 X.509 SubjectPublicKeyInfo 结构进行格式化。\n'
             '参见 <a href="https://tools.ietf.org/html/rfc5280#section-4.1">RFC 5280 §4.1</a>。</p>'),
        ],
    ),
    # ----- trait.SigningKey.html -----
    (
        'trait.SigningKey.html',
        [
            (tr('<p>A key that can be used to sign messages</p>'),
             '<p>一个可用于对消息进行签名的密钥</p>'),
            (tr('<p>Signs <code>msg</code> using the selected algorithm</p>'),
             '<p>使用所选算法对 <code>msg</code> 进行签名</p>'),
        ],
    ),
    # ----- type.RcgenError.html -----
    (
        'type.RcgenError.html',
        [
            (tr('<p>Type-alias for the old name of <a href="enum.Error.html" title="enum rcgen::Error"><code>Error</code></a>.</p>'),
             '<p>旧名称 <a href="enum.Error.html" title="enum rcgen::Error"><code>Error</code></a> 的类型别名。</p>'),
            (tr('<p>The given certificate couldn’t be parsed</p>'),
             '<p>给定的证书无法被解析</p>'),
            (tr('<p>The given certificate signing request couldn’t be parsed</p>'),
             '<p>给定的证书签名请求无法被解析</p>'),
            (tr('<p>The given key pair couldn’t be parsed</p>'),
             '<p>给定的密钥对无法被解析</p>'),
            (tr('<p>Invalid ASN.1 string</p>'),
             '<p>非法的 ASN.1 字符串</p>'),
            (tr('<p>An IP address was provided as a byte array, but the byte array was an invalid length.</p>'),
             '<p>IP 地址以字节数组形式提供，但该字节数组长度不合法。</p>'),
            (tr('<p>There is no support for generating\n'
                'keys for the given algorithm</p>'),
             '<p>不支持为给定的算法生成密钥</p>'),
            (tr('<p>The requested signature algorithm is not supported</p>'),
             '<p>不支持所请求的签名算法</p>'),
            (tr('<p>Unspecified <code>ring</code> error</p>'),
             '<p>未指明的 <code>ring</code> 错误</p>'),
            (tr('<p>The <code>ring</code> library rejected the key upon loading</p>'),
             '<p><code>ring</code> 库在加载时拒绝了该密钥</p>'),
            (tr('<p>Time conversion related errors</p>'),
             '<p>时间转换相关的错误</p>'),
            (tr('<p>Error from the pem crate</p>'),
             '<p>来自 pem crate 的错误</p>'),
            (tr('<p>Error generated by a remote key operation</p>'),
             '<p>由远程密钥操作产生的错误</p>'),
            (tr('<p>Unsupported field when generating a CSR</p>'),
             '<p>生成 CSR 时遇到了不支持的字段</p>'),
            (tr('<p>Invalid certificate revocation list (CRL) next update.</p>'),
             '<p>非法的证书吊销列表（CRL）下次更新。</p>'),
            (tr('<p>CRL issuer specifies Key Usages that don’t include cRLSign.</p>'),
             '<p>CRL 颁发者所指定的 Key Usages 不包含 cRLSign。</p>'),
        ],
    ),
    # ----- string/index.html -----
    (
        'string/index.html',
        [
            (tr('<p>ASN.1 string types</p>'),
             '<p>ASN.1 字符串类型</p>'),
        ],
    ),
    # ----- string/struct.BmpString.html -----
    (
        'string/struct.BmpString.html',
        [
            (tr('<p>Returns a byte slice of this <code>BmpString</code>’s contents.</p>'),
             '<p>返回该 <code>BmpString</code> 内容对应的字节切片。</p>'),
            (tr('<p>The inverse of this method is <a href="struct.BmpString.html#method.from_utf16be" title="associated function rcgen::string::BmpString::from_utf16be"><code>from_utf16be</code></a>.</p>'),
             '<p>本方法的反操作是 <a href="struct.BmpString.html#method.from_utf16be" title="associated function rcgen::string::BmpString::from_utf16be"><code>from_utf16be</code></a>。</p>'),
            # en-dash
            ('<p>Decode a UTF-16BE–encoded vector <code>vec</code> into a <code>BmpString</code>, returning <a href="https://doc.rust-lang.org/1.95.0/core/result/enum.Result.html#variant.Err" title="variant core::result::Result::Err">Err</a> if <code>vec</code> contains any invalid data.</p>',
             '<p>将一个 UTF-16BE 编码的向量 <code>vec</code> 解码为 <code>BmpString</code>，若 <code>vec</code> 中含有任何非法数据则返回 <a href="https://doc.rust-lang.org/1.95.0/core/result/enum.Result.html#variant.Err" title="variant core::result::Result::Err"><code>Err</code></a>。</p>'),
            (tr('<p>Converts a <code>&amp;str</code> to a <a href="struct.BmpString.html" title="struct rcgen::string::BmpString"><code>BmpString</code></a>.</p>'),
             '<p>将一个 <code>&amp;str</code> 转换为 <a href="struct.BmpString.html" title="struct rcgen::string::BmpString"><code>BmpString</code></a>。</p>'),
            (tr('<p>Any character not in the <a href="struct.BmpString.html" title="struct rcgen::string::BmpString"><code>BmpString</code></a> charset will be rejected.\n'
                'See <a href="struct.BmpString.html" title="struct rcgen::string::BmpString"><code>BmpString</code></a> documentation for more information.</p>'),
             '<p>任何不属于 <a href="struct.BmpString.html" title="struct rcgen::string::BmpString"><code>BmpString</code></a> 字符集的字符都将被拒绝。\n'
             '更多信息请参见 <a href="struct.BmpString.html" title="struct rcgen::string::BmpString"><code>BmpString</code></a> 文档。</p>'),
            (tr('<p>The result is allocated on the heap.</p>'),
             '<p>结果将在堆上分配。</p>'),
            (tr('<p>Converts a <a href="https://doc.rust-lang.org/1.95.0/alloc/string/struct.String.html" title="struct alloc::string::String"><code>String</code></a> into a <a href="struct.BmpString.html" title="struct rcgen::string::BmpString"><code>BmpString</code></a></p>'),
             '<p>将一个 <a href="https://doc.rust-lang.org/1.95.0/alloc/string/struct.String.html" title="struct alloc::string::String"><code>String</code></a> 转换为 <a href="struct.BmpString.html" title="struct rcgen::string::BmpString"><code>BmpString</code></a></p>'),
            (tr('<p>Parsing a <a href="struct.BmpString.html" title="struct rcgen::string::BmpString"><code>BmpString</code></a> allocates memory since the UTF-8 to UTF-16 conversion requires a memory allocation.</p>'),
             '<p>解析 <a href="struct.BmpString.html" title="struct rcgen::string::BmpString"><code>BmpString</code></a> 时会进行内存分配，因为 UTF-8 到 UTF-16 的转换需要一次内存分配。</p>'),
        ],
    ),
    # ----- string/struct.Ia5String.html -----
    (
        'string/struct.Ia5String.html',
        [
            (tr('<p>Extracts a string slice containing the entire <a href="struct.Ia5String.html" title="struct rcgen::string::Ia5String"><code>Ia5String</code></a>.</p>'),
             '<p>提取包含整个 <a href="struct.Ia5String.html" title="struct rcgen::string::Ia5String"><code>Ia5String</code></a> 的字符串切片。</p>'),
            (tr('<p>Converts a <a href="https://doc.rust-lang.org/1.95.0/std/primitive.str.html" title="primitive str"><code>&amp;str</code></a> to a <a href="struct.Ia5String.html" title="struct rcgen::string::Ia5String"><code>Ia5String</code></a>.</p>'),
             '<p>将一个 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.str.html" title="primitive str"><code>&amp;str</code></a> 转换为 <a href="struct.Ia5String.html" title="struct rcgen::string::Ia5String"><code>Ia5String</code></a>。</p>'),
            (tr('<p>Any character not in the <a href="struct.Ia5String.html" title="struct rcgen::string::Ia5String"><code>Ia5String</code></a> charset will be rejected.\n'
                'See <a href="struct.Ia5String.html" title="struct rcgen::string::Ia5String"><code>Ia5String</code></a> documentation for more information.</p>'),
             '<p>任何不属于 <a href="struct.Ia5String.html" title="struct rcgen::string::Ia5String"><code>Ia5String</code></a> 字符集的字符都将被拒绝。\n'
             '更多信息请参见 <a href="struct.Ia5String.html" title="struct rcgen::string::Ia5String"><code>Ia5String</code></a> 文档。</p>'),
            (tr('<p>Converts a <a href="https://doc.rust-lang.org/1.95.0/alloc/string/struct.String.html" title="struct alloc::string::String"><code>String</code></a> into a <a href="struct.Ia5String.html" title="struct rcgen::string::Ia5String"><code>Ia5String</code></a></p>'),
             '<p>将一个 <a href="https://doc.rust-lang.org/1.95.0/alloc/string/struct.String.html" title="struct alloc::string::String"><code>String</code></a> 转换为 <a href="struct.Ia5String.html" title="struct rcgen::string::Ia5String"><code>Ia5String</code></a></p>'),
        ],
    ),
    # ----- string/struct.PrintableString.html -----
    (
        'string/struct.PrintableString.html',
        [
            (tr('<p>Extracts a string slice containing the entire <a href="struct.PrintableString.html" title="struct rcgen::string::PrintableString"><code>PrintableString</code></a>.</p>'),
             '<p>提取包含整个 <a href="struct.PrintableString.html" title="struct rcgen::string::PrintableString"><code>PrintableString</code></a> 的字符串切片。</p>'),
            (tr('<p>Converts a <a href="https://doc.rust-lang.org/1.95.0/std/primitive.str.html" title="primitive str"><code>&amp;str</code></a> to a <a href="struct.PrintableString.html" title="struct rcgen::string::PrintableString"><code>PrintableString</code></a>.</p>'),
             '<p>将一个 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.str.html" title="primitive str"><code>&amp;str</code></a> 转换为 <a href="struct.PrintableString.html" title="struct rcgen::string::PrintableString"><code>PrintableString</code></a>。</p>'),
            (tr('<p>Any character not in the <a href="struct.PrintableString.html" title="struct rcgen::string::PrintableString"><code>PrintableString</code></a> charset will be rejected.\n'
                'See <a href="struct.PrintableString.html" title="struct rcgen::string::PrintableString"><code>PrintableString</code></a> documentation for more information.</p>'),
             '<p>任何不属于 <a href="struct.PrintableString.html" title="struct rcgen::string::PrintableString"><code>PrintableString</code></a> 字符集的字符都将被拒绝。\n'
             '更多信息请参见 <a href="struct.PrintableString.html" title="struct rcgen::string::PrintableString"><code>PrintableString</code></a> 文档。</p>'),
            (tr('<p>Converts a <a href="https://doc.rust-lang.org/1.95.0/alloc/string/struct.String.html" title="struct alloc::string::String"><code>String</code></a> into a <a href="struct.PrintableString.html" title="struct rcgen::string::PrintableString"><code>PrintableString</code></a></p>'),
             '<p>将一个 <a href="https://doc.rust-lang.org/1.95.0/alloc/string/struct.String.html" title="struct alloc::string::String"><code>String</code></a> 转换为 <a href="struct.PrintableString.html" title="struct rcgen::string::PrintableString"><code>PrintableString</code></a></p>'),
            (tr('<p>This conversion does not allocate or copy memory.</p>'),
             '<p>本转换不会进行内存分配或复制。</p>'),
        ],
    ),
    # ----- string/struct.TeletexString.html -----
    (
        'string/struct.TeletexString.html',
        [
            (tr('<p>Extracts a string slice containing the entire <a href="struct.TeletexString.html" title="struct rcgen::string::TeletexString"><code>TeletexString</code></a>.</p>'),
             '<p>提取包含整个 <a href="struct.TeletexString.html" title="struct rcgen::string::TeletexString"><code>TeletexString</code></a> 的字符串切片。</p>'),
            (tr('<p>Returns a byte slice of this <code>TeletexString</code>’s contents.</p>'),
             '<p>返回该 <code>TeletexString</code> 内容对应的字节切片。</p>'),
            (tr('<p>Converts a <a href="https://doc.rust-lang.org/1.95.0/std/primitive.str.html" title="primitive str"><code>&amp;str</code></a> to a <a href="struct.TeletexString.html" title="struct rcgen::string::TeletexString"><code>TeletexString</code></a>.</p>'),
             '<p>将一个 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.str.html" title="primitive str"><code>&amp;str</code></a> 转换为 <a href="struct.TeletexString.html" title="struct rcgen::string::TeletexString"><code>TeletexString</code></a>。</p>'),
            (tr('<p>Any character not in the <a href="struct.TeletexString.html" title="struct rcgen::string::TeletexString"><code>TeletexString</code></a> charset will be rejected.\n'
                'See <a href="struct.TeletexString.html" title="struct rcgen::string::TeletexString"><code>TeletexString</code></a> documentation for more information.</p>'),
             '<p>任何不属于 <a href="struct.TeletexString.html" title="struct rcgen::string::TeletexString"><code>TeletexString</code></a> 字符集的字符都将被拒绝。\n'
             '更多信息请参见 <a href="struct.TeletexString.html" title="struct rcgen::string::TeletexString"><code>TeletexString</code></a> 文档。</p>'),
            (tr('<p>Converts a <a href="https://doc.rust-lang.org/1.95.0/alloc/string/struct.String.html" title="struct alloc::string::String"><code>String</code></a> into a <a href="struct.TeletexString.html" title="struct rcgen::string::TeletexString"><code>TeletexString</code></a></p>'),
             '<p>将一个 <a href="https://doc.rust-lang.org/1.95.0/alloc/string/struct.String.html" title="struct alloc::string::String"><code>String</code></a> 转换为 <a href="struct.TeletexString.html" title="struct rcgen::string::TeletexString"><code>TeletexString</code></a></p>'),
        ],
    ),
    # ----- string/struct.UniversalString.html -----
    (
        'string/struct.UniversalString.html',
        [
            (tr('<p>Returns a byte slice of this <code>UniversalString</code>’s contents.</p>'),
             '<p>返回该 <code>UniversalString</code> 内容对应的字节切片。</p>'),
            (tr('<p>The inverse of this method is <a href="struct.UniversalString.html#method.from_utf32be" title="associated function rcgen::string::UniversalString::from_utf32be"><code>from_utf32be</code></a>.</p>'),
             '<p>本方法的反操作是 <a href="struct.UniversalString.html#method.from_utf32be" title="associated function rcgen::string::UniversalString::from_utf32be"><code>from_utf32be</code></a>。</p>'),
            ('<p>Decode a UTF-32BE–encoded vector <code>vec</code> into a <code>UniversalString</code>, returning <a href="https://doc.rust-lang.org/1.95.0/core/result/enum.Result.html#variant.Err" title="variant core::result::Result::Err">Err</a> if <code>vec</code> contains any invalid data.</p>',
             '<p>将一个 UTF-32BE 编码的向量 <code>vec</code> 解码为 <code>UniversalString</code>，若 <code>vec</code> 中含有任何非法数据则返回 <a href="https://doc.rust-lang.org/1.95.0/core/result/enum.Result.html#variant.Err" title="variant core::result::Result::Err"><code>Err</code></a>。</p>'),
            (tr('<p>Converts a <a href="https://doc.rust-lang.org/1.95.0/std/primitive.str.html" title="primitive str"><code>&amp;str</code></a> to a <a href="struct.UniversalString.html" title="struct rcgen::string::UniversalString"><code>UniversalString</code></a>.</p>'),
             '<p>将一个 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.str.html" title="primitive str"><code>&amp;str</code></a> 转换为 <a href="struct.UniversalString.html" title="struct rcgen::string::UniversalString"><code>UniversalString</code></a>。</p>'),
            (tr('<p>Any character not in the <a href="struct.UniversalString.html" title="struct rcgen::string::UniversalString"><code>UniversalString</code></a> charset will be rejected.\n'
                'See <a href="struct.UniversalString.html" title="struct rcgen::string::UniversalString"><code>UniversalString</code></a> documentation for more information.</p>'),
             '<p>任何不属于 <a href="struct.UniversalString.html" title="struct rcgen::string::UniversalString"><code>UniversalString</code></a> 字符集的字符都将被拒绝。\n'
             '更多信息请参见 <a href="struct.UniversalString.html" title="struct rcgen::string::UniversalString"><code>UniversalString</code></a> 文档。</p>'),
            (tr('<p>Converts a <a href="https://doc.rust-lang.org/1.95.0/alloc/string/struct.String.html" title="struct alloc::string::String"><code>String</code></a> into a <a href="struct.UniversalString.html" title="struct rcgen::string::UniversalString"><code>UniversalString</code></a></p>'),
             '<p>将一个 <a href="https://doc.rust-lang.org/1.95.0/alloc/string/struct.String.html" title="struct alloc::string::String"><code>String</code></a> 转换为 <a href="struct.UniversalString.html" title="struct rcgen::string::UniversalString"><code>UniversalString</code></a></p>'),
            (tr('<p>Parsing a <a href="struct.UniversalString.html" title="struct rcgen::string::UniversalString"><code>UniversalString</code></a> allocates memory since the UTF-8 to UTF-32 conversion requires a memory allocation.</p>'),
             '<p>解析 <a href="struct.UniversalString.html" title="struct rcgen::string::UniversalString"><code>UniversalString</code></a> 时会进行内存分配，因为 UTF-8 到 UTF-32 的转换需要一次内存分配。</p>'),
        ],
    ),
    # ----- fn.date_time_ymd.html -----
    (
        'fn.date_time_ymd.html',
        [
            (tr('<p>Convenience function to build a <a href="https://doc.rust-lang.org/1.95.0/core/time/struct.UnixTime.html" title="struct core::time::UnixTime"><code>core::time::UnixTime</code></a> from a year, month, day tuple.</p>'),
             '<p>用于从年、月、日三元组构造 <a href="https://doc.rust-lang.org/1.95.0/core/time/struct.UnixTime.html" title="struct core::time::UnixTime"><code>core::time::UnixTime</code></a> 的便捷函数。</p>'),
        ],
    ),
    # ----- fn.generate_simple_self_signed.html -----
    (
        'fn.generate_simple_self_signed.html',
        [
            (tr('<p>Generates a self-signed certificate with the given subject alt names</p>'),
             '<p>使用给定的主题备用名称（Subject Alternative Name）生成一份自签名证书</p>'),
            (tr('<p>The certificate is generated with default parameters and a randomly generated key pair.\n'
                'It is signed with a self-signed <a href="https://en.wikipedia.org/wiki/X.509" title="X.509"><code>X.509</code></a> certificate using the default key pair.</p>'),
             '<p>该证书使用默认参数和随机生成的密钥对进行生成，\n'
             '并使用默认密钥对对一份自签名的 <a href="https://en.wikipedia.org/wiki/X.509" title="X.509"><code>X.509</code></a> 证书进行签名。</p>'),
        ],
    ),
    # ----- sign_algo/struct.SignatureAlgorithm.html -----
    (
        'sign_algo/struct.SignatureAlgorithm.html',
        [
            (tr('<p>Signature algorithm type</p>'),
             '<p>签名算法类型</p>'),
            (tr('<p>Retrieve the <a href="struct.SignatureAlgorithm.html" title="struct rcgen::SignatureAlgorithm"><code>SignatureAlgorithm</code></a> for the provided OID</p>'),
             '<p>为给定的 OID 获取对应的 <a href="struct.SignatureAlgorithm.html" title="struct rcgen::SignatureAlgorithm"><code>SignatureAlgorithm</code></a></p>'),
            (tr('<p>The <code>Hash</code> trait is not derived, but implemented according to impl of the <code>PartialEq</code> trait</p>'),
             '<p>该类型并未派生 <code>Hash</code>，而是按 <code>PartialEq</code> 的实现方式手动实现</p>'),
        ],
    ),
    # ----- certificate/enum.CidrSubnet.html, certificate/struct.Certificate.html, etc. (重导出页面)
    # 11 个子目录里的页可能与根页面内容相同或简略。
]


# PKCS static files (12 files) — bulk pattern
PKCS_FILES = [
    'static.PKCS_ECDSA_P256_SHA256.html',
    'static.PKCS_ECDSA_P384_SHA384.html',
    'static.PKCS_ED25519.html',
    'static.PKCS_RSA_SHA256.html',
    'static.PKCS_RSA_SHA384.html',
    'static.PKCS_RSA_SHA512.html',
    'sign_algo/algo/static.PKCS_ECDSA_P256_SHA256.html',
    'sign_algo/algo/static.PKCS_ECDSA_P384_SHA384.html',
    'sign_algo/algo/static.PKCS_ED25519.html',
    'sign_algo/algo/static.PKCS_RSA_SHA256.html',
    'sign_algo/algo/static.PKCS_RSA_SHA384.html',
    'sign_algo/algo/static.PKCS_RSA_SHA512.html',
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
    for rel in PKCS_FILES:
        path = os.path.join(BASE, rel)
        if not os.path.exists(path):
            print(f'  MISSING file: {rel}')
            continue
        with open(path, 'rb') as f:
            raw = f.read()
        orig = raw
        n_this = 0
        pairs = [
            ('<p>Signature algorithm for ECDSA</p>',
             '<p>ECDSA 签名算法</p>'),
            ('<p>Signature algorithm for Ed25519</p>',
             '<p>Ed25519 签名算法</p>'),
            ('<p>Signature algorithm for RSA</p>',
             '<p>RSA 签名算法</p>'),
        ]
        for old, new in pairs:
            old_b = old.encode('utf-8')
            new_b = new.encode('utf-8')
            if old_b in raw:
                raw = raw.replace(old_b, new_b)
                total_found += 1
                n_this += 1
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
