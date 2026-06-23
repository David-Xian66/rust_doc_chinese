"""Translate all OWN untranslated docblocks in rustls_pki_types.

Each translation is (rel, [(old, new), ...]).
"""

import os
import re

BASE = 'D:/Administrator/Documents/Code/rust_doc_all/rustls_pki_types'

JOBS = [
    # enum.FipsStatus.html
    (
        'enum.FipsStatus.html',
        [
            ('<p>FIPS validation status of an algorithm or implementation.</p>',
             '<p>某算法或实现的 FIPS 验证状态。</p>'),
            ('<p>Not FIPS tested, or unapproved algorithm.</p>',
             '<p>未经过 FIPS 测试，或为未批准的算法。</p>'),
            ('<p>In queue for FIPS validation.</p>',
             '<p>正在排队等待 FIPS 验证。</p>'),
            ('<p>FIPS certified, with named certificate.</p>',
             '<p>已通过 FIPS 认证，并附带具名证书。</p>'),
            ('<p>A name, number or URL referencing the FIPS certificate.</p>',
             '<p>引用该 FIPS 证书的名称、编号或 URL。</p>'),
        ],
    ),
    # enum.IpAddr.html
    (
        'enum.IpAddr.html',
        [
            ('<p><code>no_std</code> implementation of <code>std::net::IpAddr</code>.</p>',
             '<p><code>std::net::IpAddr</code> 的 <code>no_std</code> 实现。</p>'),
            ('<p>Note: because we intend to replace this type with <code>core::net::IpAddr</code> as soon as it is\nstabilized, the identity of this type should not be considered semver-stable. However, the\nattached interfaces are stable; they form a subset of those provided by <code>core::net::IpAddr</code>.</p>',
             '<p>注意：由于我们计划在该类型一旦稳定后用 <code>core::net::IpAddr</code> 替换它，因此该类型本身的标识不应被视为 semver 稳定。不过，其对外提供的接口是稳定的，它们是 <code>core::net::IpAddr</code> 所提供接口的一个子集。</p>'),
            ('<p>An Ipv4 address.</p>', '<p>一个 IPv4 地址。</p>'),
            ('<p>An Ipv6 address.</p>', '<p>一个 IPv6 地址。</p>'),
        ],
    ),
    # enum.PrivateKeyDer.html
    (
        'enum.PrivateKeyDer.html',
        [
            ('<p>A DER-encoded X.509 private key, in one of several formats</p>',
             '<p>一个 DER 编码的 X.509 私钥，可采用多种格式之一</p>'),
            ('<p>See variant inner types for more detailed information.</p>',
             '<p>更多信息请参见各变体的内部类型。</p>'),
            ('<p>This can load several types of PEM-encoded private key, and then reveal\nwhich types were found:</p>',
             '<p>它可以加载多种类型的 PEM 编码私钥，并报告实际发现了哪些类型：</p>'),
            ('<p>Clone the private key to a <code>\'static</code> value</p>',
             '<p>将该私钥克隆为一个 <code>\'static</code> 值</p>'),
            ('<p>Yield the DER-encoded bytes of the private key</p>',
             '<p>产出该私钥 DER 编码后的字节</p>'),
        ],
    ),
    # enum.ServerName.html
    (
        'enum.ServerName.html',
        [
            ('<p>Encodes ways a client can know the expected name of the server.</p>',
             '<p>表示客户端获知服务器预期名称的途径。</p>'),
            ('<p>This currently covers knowing the DNS name of the server, but\nwill be extended in the future to supporting privacy-preserving names\nfor the server (“ECH”).  For this reason this enum is <code>non_exhaustive</code>.</p>',
             '<p>当前它涵盖知晓服务器的 DNS 名称这一情形，未来将扩展到支持服务器的隐私保护名称（“ECH”）。\n因此该枚举被声明为 <code>non_exhaustive</code>。</p>'),
            ('<p>If you have a DNS name as a <code>&amp;str</code>, this type implements <code>TryFrom&lt;&amp;str&gt;</code>,\nso you can do:</p>',
             '<p>如果你拥有一个 <code>&amp;str</code> 形式的 DNS 名称，该类型实现了 <code>TryFrom&lt;&amp;str&gt;</code>，\n因此你可以这样使用：</p>'),
            ('<p>Produce an owned <code>ServerName</code> from this (potentially borrowed) <code>ServerName</code>.</p>',
             '<p>从一个（可能为借用的）<code>ServerName</code> 产生一个 owned 的 <code>ServerName</code>。</p>'),
            ('<p>Return the string representation of this <code>ServerName</code>.</p>',
             '<p>返回该 <code>ServerName</code> 的字符串表示形式。</p>'),
            ('<p>In the case of a <code>ServerName::DnsName</code> instance, this function returns a borrowed <code>str</code>.\nFor a <code>ServerName::IpAddress</code> instance it returns an allocated <code>String</code>.</p>',
             '<p>对于 <code>ServerName::DnsName</code> 实例，此函数返回一个借用的 <code>str</code>。\n对于 <code>ServerName::IpAddress</code> 实例，它返回一个分配而来的 <code>String</code>。</p>'),
            ('<p>Attempt to make a ServerName from a string by parsing as a DNS name or IP address.</p>',
             '<p>尝试将一个字符串解析为 DNS 名称或 IP 地址以构造 <code>ServerName</code>。</p>'),
        ],
    ),
    # struct.AddrParseError.html
    (
        'struct.AddrParseError.html',
        [
            ('<p>Failure to parse an IP address</p>',
             '<p>解析 IP 地址失败</p>'),
        ],
    ),
    # struct.CertificateDer.html
    (
        'struct.CertificateDer.html',
        [
            ('<p>A DER-encoded X.509 certificate; as specified in RFC 5280</p>',
             '<p>一份 DER 编码的 X.509 证书；遵循 RFC 5280 的规定</p>'),
            ('<p>Certificates are identified in PEM context as <code>CERTIFICATE</code> and when stored in a\nfile usually use a <code>.pem</code>, <code>.cer</code> or <code>.crt</code> extension. For more on PEM files, refer to the\ncrate documentation.</p>',
             '<p>在 PEM 语境中，证书的类型标识为 <code>CERTIFICATE</code>；存储到文件时通常使用 <code>.pem</code>、<code>.cer</code> 或 <code>.crt</code> 后缀。\n更多关于 PEM 文件的信息，请参见本 crate 的文档。</p>'),
            ('<p>A const constructor to create a <code>CertificateDer</code> from a slice of DER.</p>',
             '<p>一个 const 构造器，用于从一段 DER 字节切片创建一个 <code>CertificateDer</code>。</p>'),
            ('<p>Converts this certificate into its owned variant, unfreezing borrowed content (if any)</p>',
             '<p>将该证书转换为其 owned 变体，解除对借用内容（如果有）的冻结</p>'),
        ],
    ),
    # struct.CertificateRevocationListDer.html
    (
        'struct.CertificateRevocationListDer.html',
        [
            ('<p>A Certificate Revocation List; as specified in RFC 5280</p>',
             '<p>证书吊销列表（CRL）；遵循 RFC 5280 的规定</p>'),
            ('<p>Certificate revocation lists are identified in PEM context as <code>X509 CRL</code> and when stored in a\nfile usually use a <code>.crl</code> extension. For more on PEM files, refer to the crate documentation.</p>',
             '<p>在 PEM 语境中，证书吊销列表的类型标识为 <code>X509 CRL</code>；存储到文件时通常使用 <code>.crl</code> 后缀。\n更多关于 PEM 文件的信息，请参见本 crate 的文档。</p>'),
        ],
    ),
    # struct.CertificateSigningRequestDer.html
    (
        'struct.CertificateSigningRequestDer.html',
        [
            ('<p>A Certificate Signing Request; as specified in RFC 2986</p>',
             '<p>证书签名请求（CSR）；遵循 RFC 2986 的规定</p>'),
            ('<p>Certificate signing requests are identified in PEM context as <code>CERTIFICATE REQUEST</code> and when stored in a\nfile usually use a <code>.csr</code> extension. For more on PEM files, refer to the crate documentation.</p>',
             '<p>在 PEM 语境中，证书签名请求的类型标识为 <code>CERTIFICATE REQUEST</code>；存储到文件时通常使用 <code>.csr</code> 后缀。\n更多关于 PEM 文件的信息，请参见本 crate 的文档。</p>'),
        ],
    ),
    # struct.Der.html
    (
        'struct.Der.html',
        [
            ('<p>A const constructor to create a <code>Der</code> from a borrowed slice</p>',
             '<p>一个 const 构造器，用于从一个借用切片创建一个 <code>Der</code></p>'),
            ('<p>DER-encoded data, either owned or borrowed</p>',
             '<p>DER 编码的数据，可以是 owned 或借用的形式</p>'),
            ('<p>This wrapper type is used to represent DER-encoded data in a way that is agnostic to whether\nthe data is owned (by a <code>Vec&lt;u8&gt;</code>) or borrowed (by a <code>&amp;[u8]</code>). Support for the owned\nvariant is only available when the <code>alloc</code> feature is enabled.</p>',
             '<p>该包装类型用于以与底层数据是否 owned（由 <code>Vec&lt;u8&gt;</code> 拥有）还是借用（由 <code>&amp;[u8]</code> 借用）无关的方式来表示 DER 编码数据。\n对 owned 变体的支持仅在启用了 <code>alloc</code> feature 时可用。</p>'),
        ],
    ),
    # struct.DnsName.html
    (
        'struct.DnsName.html',
        [
            ('<p>A type which encapsulates a string (borrowed or owned) that is a syntactically valid DNS name.</p>',
             '<p>一种将字符串（借用或 owned）封装为语法上合法的 DNS 名称的类型。</p>'),
            ('<p>Produce a borrowed <code>DnsName</code> from this owned <code>DnsName</code>.</p>',
             '<p>从一个 owned 的 <code>DnsName</code> 产生一个借用的 <code>DnsName</code>。</p>'),
            ('<p>Copy this object to produce an owned <code>DnsName</code>, smashing the case to lowercase\nin one operation.</p>',
             '<p>复制本对象以产生一个 owned 的 <code>DnsName</code>，同时将大小写统一为小写——一步完成。</p>'),
            ('<p>Produce an owned <code>DnsName</code> from this (potentially borrowed) <code>DnsName</code>.</p>',
             '<p>从一个（可能借用的）<code>DnsName</code> 产生一个 owned 的 <code>DnsName</code>。</p>'),
            ('<p>Produces a borrowed <a href="struct.DnsName.html" title="struct rustls_pki_types::DnsName"><code>DnsName</code></a> from a borrowed [<code>str</code>].</p>',
             '<p>从一个借用的 <code>str</code> 产生一个借用的 <a href="struct.DnsName.html" title="struct rustls_pki_types::DnsName"><code>DnsName</code></a>。</p>'),
        ],
    ),
    # struct.EchConfigListBytes.html
    (
        'struct.EchConfigListBytes.html',
        [
            ('<p>A TLS-encoded Encrypted Client Hello (ECH) configuration list (<code>ECHConfigList</code>); as specified in\n<a href="https://datatracker.ietf.org/doc/html/rfc9849#section-4">RFC 9849 §4</a></p>',
             '<p>一段 TLS 编码的 Encrypted Client Hello（ECH）配置列表（<code>ECHConfigList</code>）；遵循 <a href="https://datatracker.ietf.org/doc/html/rfc9849#section-4">RFC 9849 §4</a> 的规定</p>'),
            ('<p>Converts this config into its owned variant, unfreezing borrowed content (if any)</p>',
             '<p>将该配置转换为其 owned 变体，解除对借用内容（如果有）的冻结</p>'),
            ('<p>Convert an iterator over PEM items into an <code>EchConfigListBytes</code> and private key.</p>',
             '<p>将一个 PEM 条目迭代器转换为一个 <code>EchConfigListBytes</code> 以及对应的私钥。</p>'),
            ('<p>This handles the “ECHConfig file” format specified in\n<a href="https://www.ietf.org/archive/id/draft-farrell-tls-pemesni-05.html#name-echconfig-file">https://www.ietf.org/archive/id/draft-farrell-tls-pemesni-05.html#name-echconfig-file</a></p>',
             '<p>它处理 <a href="https://www.ietf.org/archive/id/draft-farrell-tls-pemesni-05.html#name-echconfig-file">此处规定的 “ECHConfig file” 格式</a>。</p>'),
            ('<p>Use it like:</p>', '<p>用法如下：</p>'),
        ],
    ),
    # struct.InvalidDnsNameError.html
    (
        'struct.InvalidDnsNameError.html',
        [
            ('<p>The provided input could not be parsed because\nit is not a syntactically-valid DNS Name.</p>',
             '<p>提供的输入无法被解析，因为它不是一个语法上合法的 DNS 名称。</p>'),
        ],
    ),
    # struct.InvalidSignature.html
    (
        'struct.InvalidSignature.html',
        [
            ('<p>A detail-less error when a signature is not valid.</p>',
             '<p>签名无效时返回的不含细节的错误。</p>'),
        ],
    ),
    # struct.Ipv4Addr.html
    (
        'struct.Ipv4Addr.html',
        [
            ('<p><code>no_std</code> implementation of <code>std::net::Ipv4Addr</code>.</p>',
             '<p><code>std::net::Ipv4Addr</code> 的 <code>no_std</code> 实现。</p>'),
            ('<p>Note: because we intend to replace this type with <code>core::net::Ipv4Addr</code> as soon as it is\nstabilized, the identity of this type should not be considered semver-stable. However, the\nattached interfaces are stable; they form a subset of those provided by <code>core::net::Ipv4Addr</code>.</p>',
             '<p>注意：由于我们计划在该类型一旦稳定后用 <code>core::net::Ipv4Addr</code> 替换它，因此该类型本身的标识不应被视为 semver 稳定。不过，其对外提供的接口是稳定的，它们是 <code>core::net::Ipv4Addr</code> 所提供接口的一个子集。</p>'),
        ],
    ),
    # struct.Ipv6Addr.html
    (
        'struct.Ipv6Addr.html',
        [
            ('<p><code>no_std</code> implementation of <code>std::net::Ipv6Addr</code>.</p>',
             '<p><code>std::net::Ipv6Addr</code> 的 <code>no_std</code> 实现。</p>'),
            ('<p>Note: because we intend to replace this type with <code>core::net::Ipv6Addr</code> as soon as it is\nstabilized, the identity of this type should not be considered semver-stable. However, the\nattached interfaces are stable; they form a subset of those provided by <code>core::net::Ipv6Addr</code>.</p>',
             '<p>注意：由于我们计划在该类型一旦稳定后用 <code>core::net::Ipv6Addr</code> 替换它，因此该类型本身的标识不应被视为 semver 稳定。不过，其对外提供的接口是稳定的，它们是 <code>core::net::Ipv6Addr</code> 所提供接口的一个子集。</p>'),
        ],
    ),
    # struct.PrivatePkcs1KeyDer.html
    (
        'struct.PrivatePkcs1KeyDer.html',
        [
            ('<p>A DER-encoded plaintext RSA private key; as specified in PKCS#1/RFC 3447</p>',
             '<p>一份 DER 编码的明文 RSA 私钥；遵循 PKCS#1 / RFC 3447 的规定</p>'),
            ('<p>RSA private keys are identified in PEM context as <code>RSA PRIVATE KEY</code> and when stored in a\nfile usually use a <code>.pem</code> or <code>.key</code> extension.</p>',
             '<p>在 PEM 语境中，RSA 私钥的类型标识为 <code>RSA PRIVATE KEY</code>；存储到文件时通常使用 <code>.pem</code> 或 <code>.key</code> 后缀。</p>'),
            ('<p>Clone the private key to a <code>\'static</code> value</p>',
             '<p>将该私钥克隆为一个 <code>\'static</code> 值</p>'),
            ('<p>Yield the DER-encoded bytes of the private key</p>',
             '<p>产出该私钥 DER 编码后的字节</p>'),
        ],
    ),
    # struct.PrivatePkcs8KeyDer.html
    (
        'struct.PrivatePkcs8KeyDer.html',
        [
            ('<p>A DER-encoded plaintext private key; as specified in PKCS#8/RFC 5958</p>',
             '<p>一份 DER 编码的明文私钥；遵循 PKCS#8 / RFC 5958 的规定</p>'),
            ('<p>PKCS#8 private keys are identified in PEM context as <code>PRIVATE KEY</code> and when stored in a\nfile usually use a <code>.pem</code> or <code>.key</code> extension. For more on PEM files, refer to the crate\ndocumentation.</p>',
             '<p>在 PEM 语境中，PKCS#8 私钥的类型标识为 <code>PRIVATE KEY</code>；存储到文件时通常使用 <code>.pem</code> 或 <code>.key</code> 后缀。\n更多关于 PEM 文件的信息，请参见本 crate 的文档。</p>'),
            ('<p>Clone the private key to a <code>\'static</code> value</p>',
             '<p>将该私钥克隆为一个 <code>\'static</code> 值</p>'),
            ('<p>Yield the DER-encoded bytes of the private key</p>',
             '<p>产出该私钥 DER 编码后的字节</p>'),
        ],
    ),
    # struct.PrivateSec1KeyDer.html
    (
        'struct.PrivateSec1KeyDer.html',
        [
            ('<p>A Sec1-encoded plaintext private key; as specified in RFC 5915</p>',
             '<p>一份 Sec1 编码的明文私钥；遵循 RFC 5915 的规定</p>'),
            ('<p>Sec1 private keys are identified in PEM context as <code>EC PRIVATE KEY</code> and when stored in a\nfile usually use a <code>.pem</code> or <code>.key</code> extension. For more on PEM files, refer to the crate\ndocumentation.</p>',
             '<p>在 PEM 语境中，Sec1 私钥的类型标识为 <code>EC PRIVATE KEY</code>；存储到文件时通常使用 <code>.pem</code> 或 <code>.key</code> 后缀。\n更多关于 PEM 文件的信息，请参见本 crate 的文档。</p>'),
            ('<p>Clone the private key to a <code>\'static</code> value</p>',
             '<p>将该私钥克隆为一个 <code>\'static</code> 值</p>'),
            ('<p>Yield the DER-encoded bytes of the private key</p>',
             '<p>产出该私钥 DER 编码后的字节</p>'),
        ],
    ),
    # struct.SubjectPublicKeyInfoDer.html
    (
        'struct.SubjectPublicKeyInfoDer.html',
        [
            ('<p>A DER-encoded SubjectPublicKeyInfo (SPKI), as specified in RFC 5280.</p>',
             '<p>一个 DER 编码的 SubjectPublicKeyInfo（SPKI），遵循 RFC 5280 的规定。</p>'),
            ('<p>Public keys are identified in PEM context as a <code>PUBLIC KEY</code>.</p>',
             '<p>在 PEM 语境中，公钥的类型标识为 <code>PUBLIC KEY</code>。</p>'),
            ('<p>Converts this SubjectPublicKeyInfo into its owned variant, unfreezing borrowed content (if any)</p>',
             '<p>将该 SubjectPublicKeyInfo 转换为其 owned 变体，解除对借用内容（如果有）的冻结</p>'),
        ],
    ),
    # struct.TrustAnchor.html
    (
        'struct.TrustAnchor.html',
        [
            ('<p>A trust anchor (a.k.a. root CA)</p>',
             '<p>一个信任锚（也称为根 CA）</p>'),
            ('<p>Traditionally, certificate verification libraries have represented trust anchors as full X.509\nroot certificates. However, those certificates contain a lot more data than is needed for\nverifying certificates. The <a href="struct.TrustAnchor.html" title="struct rustls_pki_types::TrustAnchor"><code>TrustAnchor</code></a> representation allows an application to store\njust the essential elements of trust anchors.</p>',
             '<p>传统上，证书验证库将信任锚表示为完整的 X.509 根证书。\n然而，这些证书中包含了远超证书验证所必需的数据。\n<a href="struct.TrustAnchor.html" title="struct rustls_pki_types::TrustAnchor"><code>TrustAnchor</code></a> 这种表示形式允许应用程序仅存储信任锚的关键要素。</p>'),
            ('<p>The most common way to get one of these is to call <a href="https://docs.rs/rustls-webpki/latest/webpki/fn.anchor_from_trusted_cert.html"><code>rustls_webpki::anchor_from_trusted_cert()</code></a>.</p>',
             '<p>获取此类对象的最常见方式是调用 <a href="https://docs.rs/rustls-webpki/latest/webpki/fn.anchor_from_trusted_cert.html"><code>rustls_webpki::anchor_from_trusted_cert()</code></a>。</p>'),
            ('<p>Yield a <code>\'static</code> lifetime of the <code>TrustAnchor</code> by allocating owned <code>Der</code> variants</p>',
             '<p>通过分配 owned 的 <code>Der</code> 变体，产生一个具有 <code>\'static</code> 生命周期的 <code>TrustAnchor</code></p>'),
            ('<p>Value of the <code>subject</code> field of the trust anchor</p>',
             '<p>该信任锚的 <code>subject</code> 字段的值</p>'),
            ('<p>Value of the <code>subjectPublicKeyInfo</code> field of the trust anchor</p>',
             '<p>该信任锚的 <code>subjectPublicKeyInfo</code> 字段的值</p>'),
            ('<p>Value of DER-encoded <code>NameConstraints</code>, containing name constraints to the trust anchor, if any</p>',
             '<p>DER 编码的 <code>NameConstraints</code> 值，包含对该信任锚的名称约束（如果有）</p>'),
        ],
    ),
    # struct.UnixTime.html
    (
        'struct.UnixTime.html',
        [
            ('<p>A timestamp, tracking the number of non-leap seconds since the Unix epoch.</p>',
             '<p>一个时间戳，记录自 Unix 纪元以来的非闰秒数。</p>'),
            ('<p>The Unix epoch is defined January 1, 1970 00:00:00 UTC.</p>',
             '<p>Unix 纪元定义为 1970 年 1 月 1 日 00:00:00 UTC。</p>'),
            ('<p>The current time, as a <code>UnixTime</code></p>',
             '<p>当前时间，表示为一个 <code>UnixTime</code></p>'),
            ('<p>Convert a <code>Duration</code> since the start of 1970 to a <code>UnixTime</code></p>',
             '<p>将自 1970 年起经过的一个 <code>Duration</code> 转换为一个 <code>UnixTime</code></p>'),
            ('<p>The <code>duration</code> must be relative to the Unix epoch.</p>',
             '<p><code>duration</code> 必须是相对于 Unix 纪元而言的。</p>'),
            ('<p>Number of seconds since the Unix epoch</p>',
             '<p>自 Unix 纪元以来的秒数</p>'),
        ],
    ),
    # trait.SignatureVerificationAlgorithm.html
    (
        'trait.SignatureVerificationAlgorithm.html',
        [
            ('<p>An abstract signature verification algorithm.</p>',
             '<p>一种抽象的签名验证算法。</p>'),
            ('<p>One of these is needed per supported pair of public key type (identified\nwith <code>public_key_alg_id()</code>) and <code>signatureAlgorithm</code> (identified with\n<code>signature_alg_id()</code>).  Note that both of these <code>AlgorithmIdentifier</code>s include\nthe parameters encoding, so separate <code>SignatureVerificationAlgorithm</code>s are needed\nfor each possible public key or signature parameters.</p>',
             '<p>对于每对所支持的公钥类型（通过 <code>public_key_alg_id()</code> 标识）\n与 <code>signatureAlgorithm</code>（通过 <code>signature_alg_id()</code> 标识），都需要这样一个实现。\n注意，这两个 <code>AlgorithmIdentifier</code> 都包含参数编码，\n因此对于每一种可能的公钥或签名参数，都需要单独的 <code>SignatureVerificationAlgorithm</code>。</p>'),
            ('<p>Debug implementations should list the public key algorithm identifier and\nsignature algorithm identifier in human friendly form (i.e. not encoded bytes),\nalong with the name of the implementing library (to distinguish different\nimplementations of the same algorithms).</p>',
             '<p>Debug 实现应以人类可读的形式（即不要以编码字节形式）列出公钥算法标识符与\n签名算法标识符，并附上实现库的名称（以区分同一算法的不同实现）。</p>'),
            ('<p>Verify a signature.</p>', '<p>验证签名。</p>'),
            ('<p><code>public_key</code> is the <code>subjectPublicKey</code> value from a <code>SubjectPublicKeyInfo</code> encoding\nand is untrusted.  The key’s <code>subjectPublicKeyInfo</code> matches the <a href="alg_id/struct.AlgorithmIdentifier.html" title="struct rustls_pki_types::alg_id::AlgorithmIdentifier"><code>AlgorithmIdentifier</code></a>\nreturned by <code>public_key_alg_id()</code>.</p>',
             '<p><code>public_key</code> 是取自某个 <code>SubjectPublicKeyInfo</code> 编码的 <code>subjectPublicKey</code> 值，\n不可信。该密钥的 <code>subjectPublicKeyInfo</code> 与 <code>public_key_alg_id()</code> 所返回的 <a href="alg_id/struct.AlgorithmIdentifier.html" title="struct rustls_pki_types::alg_id::AlgorithmIdentifier"><code>AlgorithmIdentifier</code></a> 相匹配。</p>'),
            ('<p><code>message</code> is the data over which the signature was allegedly computed.\nIt is not hashed; implementations of this trait function must do hashing\nif that is required by the algorithm they implement.</p>',
             '<p><code>message</code> 是据称用于计算签名的数据。\n该数据尚未哈希；若所实现的算法要求哈希，trait 函数的实现方需自行完成哈希。</p>'),
            ('<p><code>signature</code> is the signature allegedly over <code>message</code>.</p>',
             '<p><code>signature</code> 是据称针对 <code>message</code> 计算出的签名。</p>'),
            ('<p>Return <code>Ok(())</code> only if <code>signature</code> is a valid signature on <code>message</code>.</p>',
             '<p>仅当 <code>signature</code> 是 <code>message</code> 的合法签名时，返回 <code>Ok(())</code>。</p>'),
            ('<p>Return <code>Err(InvalidSignature)</code> if the signature is invalid, including if the <code>public_key</code>\nencoding is invalid.  There is no need or opportunity to produce errors\nthat are more specific than this.</p>',
             '<p>若签名无效（包括 <code>public_key</code> 编码无效的情况），则返回 <code>Err(InvalidSignature)</code>。\n没有必要也无法产生比这更具体的错误。</p>'),
            ('<p>Return the <code>AlgorithmIdentifier</code> that must equal a public key’s\n<code>subjectPublicKeyInfo</code> value for this <code>SignatureVerificationAlgorithm</code>\nto be used for signature verification.</p>',
             '<p>返回一个 <code>AlgorithmIdentifier</code>：只有当某个公钥的 <code>subjectPublicKeyInfo</code> 值与之相等时，\n本 <code>SignatureVerificationAlgorithm</code> 才可用于该公钥的签名验证。</p>'),
            ('<p>Return the <code>AlgorithmIdentifier</code> that must equal the <code>signatureAlgorithm</code> value\non the data to be verified for this <code>SignatureVerificationAlgorithm</code> to be used\nfor signature verification.</p>',
             '<p>返回一个 <code>AlgorithmIdentifier</code>：只有当待验证数据上的 <code>signatureAlgorithm</code> 值与之相等时，\n本 <code>SignatureVerificationAlgorithm</code> 才可用于该数据的签名验证。</p>'),
            ('<p>Return the FIPS status of this algorithm or implementation.</p>',
             '<p>返回本算法或实现的 FIPS 状态。</p>'),
            ('<p>Return <code>true</code> if this is backed by a FIPS-approved implementation.</p>',
             '<p>若本实现由 FIPS 批准的实现支撑，则返回 <code>true</code>。</p>'),
        ],
    ),
    # type.SubjectPublicKeyInfo.html
    (
        'type.SubjectPublicKeyInfo.html',
        [
            ('<p>A DER-encoded SubjectPublicKeyInfo (SPKI), as specified in RFC 5280.</p>',
             '<p>一个 DER 编码的 SubjectPublicKeyInfo（SPKI），遵循 RFC 5280 的规定。</p>'),
        ],
    ),
    # alg_id/index.html
    (
        'alg_id/index.html',
        [
            ('<p>The PKIX <a href="struct.AlgorithmIdentifier.html" title="struct rustls_pki_types::alg_id::AlgorithmIdentifier"><code>AlgorithmIdentifier</code></a> type, and common values.</p>',
             '<p>PKIX <a href="struct.AlgorithmIdentifier.html" title="struct rustls_pki_types::alg_id::AlgorithmIdentifier"><code>AlgorithmIdentifier</code></a> 类型及常用取值。</p>'),
            ('<p>If you need to use an <a href="struct.AlgorithmIdentifier.html" title="struct rustls_pki_types::alg_id::AlgorithmIdentifier"><code>AlgorithmIdentifier</code></a> not defined here,\nyou can define it locally.</p>',
             '<p>如果你需要使用此处未定义的 <a href="struct.AlgorithmIdentifier.html" title="struct rustls_pki_types::alg_id::AlgorithmIdentifier"><code>AlgorithmIdentifier</code></a>，\n可以在本地自行定义。</p>'),
        ],
    ),
    # alg_id/struct.AlgorithmIdentifier.html
    (
        'alg_id/struct.AlgorithmIdentifier.html',
        [
            ('<p>A DER encoding of the PKIX AlgorithmIdentifier type:</p>',
             '<p>PKIX AlgorithmIdentifier 类型的 DER 编码：</p>'),
            ('<p>Makes a new <code>AlgorithmIdentifier</code> from a static octet slice.</p>',
             '<p>从一个静态八位字节切片构造一个 <code>AlgorithmIdentifier</code>。</p>'),
            ('<p>This does not validate the contents of the slice.</p>',
             '<p>该函数不会校验切片的内容。</p>'),
        ],
    ),
    # alg_id/constant.*.html — common pattern
    # pem/enum.Error.html
    (
        'pem/enum.Error.html',
        [
            ('<p>Errors that may arise when parsing the contents of a PEM file</p>',
             '<p>解析 PEM 文件内容时可能发生的错误</p>'),
        ],
    ),
    # pem/enum.SectionKind.html
    (
        'pem/enum.SectionKind.html',
        [
            ('<p>A single recognised section in a PEM file.</p>',
             '<p>PEM 文件中某个被识别的 section。</p>'),
        ],
    ),
    # pem/fn.from_buf.html
    (
        'pem/fn.from_buf.html',
        [
            ('<p>Extract and decode the next supported PEM section from <code>rd</code>.</p>',
             '<p>从 <code>rd</code> 中提取并解码下一个所支持的 PEM section。</p>'),
        ],
    ),
    # pem/index.html
    (
        'pem/index.html',
        [
            ('<p>Low-level PEM decoding APIs.</p>',
             '<p>底层 PEM 解码 API。</p>'),
            ('<p>These APIs allow decoding PEM format in an iterator, which means you\ncan load multiple different types of PEM section from a file in a single\npass.</p>',
             '<p>这些 API 允许以迭代器方式解码 PEM 格式，\n这意味着你可以单次扫描文件从中加载多种不同类型的 PEM section。</p>'),
        ],
    ),
    # pem/struct.ReadIter.html
    (
        'pem/struct.ReadIter.html',
        [
            ('<p>Extract and return all PEM sections by reading <code>rd</code>.</p>',
             '<p>通过读取 <code>rd</code> 来提取并返回所有 PEM section。</p>'),
            ('<p>Create a new iterator.</p>',
             '<p>创建一个新的迭代器。</p>'),
        ],
    ),
    # pem/struct.SliceIter.html
    (
        'pem/struct.SliceIter.html',
        [
            ('<p>Iterator over all PEM sections in a <code>&amp;[u8]</code> slice.</p>',
             '<p>对一段 <code>&amp;[u8]</code> 切片中所有 PEM section 的迭代器。</p>'),
            ('<p>Create a new iterator.</p>',
             '<p>创建一个新的迭代器。</p>'),
        ],
    ),
    # pem/trait.PemObject.html
    (
        'pem/trait.PemObject.html',
        [
            ('<p>Items that can be decoded from PEM data.</p>',
             '<p>可从 PEM 数据解码得到的项。</p>'),
            ('<p>Conversion from a PEM <a href="enum.SectionKind.html" title="enum rustls_pki_types::pem::SectionKind"><code>SectionKind</code></a> and body data.</p>',
             '<p>从一个 PEM <a href="enum.SectionKind.html" title="enum rustls_pki_types::pem::SectionKind"><code>SectionKind</code></a> 与相应的 body 数据进行转换。</p>'),
            ('<p>This inspects <code>kind</code>, and if it matches this type’s PEM section kind,\nconverts <code>der</code> into this type.</p>',
             '<p>该函数会检查 <code>kind</code>，若与本类型的 PEM section 类型匹配，\n则将 <code>der</code> 转换为本类型。</p>'),
            ('<p>Decode the first section of this type from PEM contained in\na byte slice.</p>',
             '<p>从一段字节切片中的 PEM 数据里，解码出本类型的第一个 section。</p>'),
            ('<p><a href="enum.Error.html#variant.NoItemsFound" title="variant rustls_pki_types::pem::Error::NoItemsFound"><code>Error::NoItemsFound</code></a> is returned if no such items are found.</p>',
             '<p>若未找到相应的项，则返回 <a href="enum.Error.html#variant.NoItemsFound" title="variant rustls_pki_types::pem::Error::NoItemsFound"><code>Error::NoItemsFound</code></a>。</p>'),
            ('<p>Iterate over all sections of this type from PEM contained in\na byte slice.</p>',
             '<p>从一段字节切片中的 PEM 数据里，迭代出本类型的所有 section。</p>'),
            ('<p>Decode the first section of this type from the PEM contents of the named file.</p>',
             '<p>从指定文件中的 PEM 内容里，解码出本类型的第一个 section。</p>'),
            ('<p>Iterate over all sections of this type from the PEM contents of the named file.</p>',
             '<p>从指定文件中的 PEM 内容里，迭代出本类型的所有 section。</p>'),
            ('<p>This reports errors in two phases:</p>',
             '<p>该方法分两阶段报告错误：</p>'),
            ('<p>Decode the first section of this type from PEM read from an <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.Read.html" title="trait std::io::Read"><code>io::Read</code></a>.</p>',
             '<p>从某个 <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.Read.html" title="trait std::io::Read"><code>io::Read</code></a> 读取的 PEM 中，解码出本类型的第一个 section。</p>'),
            ('<p>Iterate over all sections of this type from PEM present in an <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.Read.html" title="trait std::io::Read"><code>io::Read</code></a>.</p>',
             '<p>从某个 <a href="https://doc.rust-lang.org/1.95.0/std/io/trait.Read.html" title="trait std::io::Read"><code>io::Read</code></a> 中的 PEM 数据里，迭代出本类型的所有 section。</p>'),
        ],
    ),
]

# alg_id/constant.*.html — bulk simple pattern
ALG_CONST = [
    'ECDSA_P256', 'ECDSA_P256K1', 'ECDSA_P384', 'ECDSA_P521',
    'ECDSA_SHA256', 'ECDSA_SHA384', 'ECDSA_SHA512',
    'ED25519', 'ED448',
    'ML_DSA_44', 'ML_DSA_65', 'ML_DSA_87',
    'RSA_ENCRYPTION',
    'RSA_PKCS1_SHA256', 'RSA_PKCS1_SHA384', 'RSA_PKCS1_SHA512',
    'RSA_PSS_SHA256', 'RSA_PSS_SHA384', 'RSA_PSS_SHA512',
]

# Curve names mapping
ALG_NAMES = {
    'ECDSA_P256': ('id-ecPublicKey', 'secp256r1'),
    'ECDSA_P256K1': ('id-ecPublicKey', 'secp256k1'),
    'ECDSA_P384': ('id-ecPublicKey', 'secp384r1'),
    'ECDSA_P521': ('id-ecPublicKey', 'secp521r1'),
    'ECDSA_SHA256': ('ecdsa-with-SHA256', None),
    'ECDSA_SHA384': ('ecdsa-with-SHA384', None),
    'ECDSA_SHA512': ('ecdsa-with-SHA512', None),
    'ED25519': ('ED25519', None),
    'ED448': ('ED448', None),
    'ML_DSA_44': ('id-ml-dsa-44', None),
    'ML_DSA_65': ('id-ml-dsa-65', None),
    'ML_DSA_87': ('id-ml-dsa-87', None),
    'RSA_ENCRYPTION': ('rsaEncryption', None),
    'RSA_PKCS1_SHA256': ('sha256WithRSAEncryption', None),
    'RSA_PKCS1_SHA384': ('sha384WithRSAEncryption', None),
    'RSA_PKCS1_SHA512': ('sha512WithRSAEncryption', None),
    'RSA_PSS_SHA256': ('rsassaPss', None),
    'RSA_PSS_SHA384': ('rsassaPss', None),
    'RSA_PSS_SHA512': ('rsassaPss', None),
}


def main():
    total_files = 0
    total_found = 0
    total_missed = 0
    for rel, pairs in JOBS:
        path = os.path.join(BASE, rel)
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        orig = c
        for old, new in pairs:
            if old in c:
                c = c.replace(old, new)
                total_found += 1
            else:
                total_missed += 1
                print(f'  MISSED {rel}: {old[:80]!r}')
        if c != orig:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(c)
            total_files += 1
            cjk = re.findall(r'[一-鿿]', c)
            print(f'  {rel}: OK CJK={len(cjk)}')
    # alg_id constant files
    for name in ALG_CONST:
        rel = f'alg_id/constant.{name}.html'
        path = os.path.join(BASE, rel)
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        orig = c
        alg_id_name, curve = ALG_NAMES[name]
        if curve:
            p1 = f'<p>AlgorithmIdentifier for <code>id-ecPublicKey</code> with named curve <code>{curve}</code>.</p>'
            p1_zh = f'<p><code>id-ecPublicKey</code> 配合命名曲线 <code>{curve}</code> 的 AlgorithmIdentifier。</p>'
        elif name.startswith('RSA_PSS_'):
            p1 = f'<p>AlgorithmIdentifier for <code>rsassaPss</code> with:</p>'
            p1_zh = '<p>带有如下参数的 <code>rsassaPss</code> AlgorithmIdentifier：</p>'
        else:
            p1 = f'<p>AlgorithmIdentifier for <code>{alg_id_name}</code>.</p>'
            p1_zh = f'<p><code>{alg_id_name}</code> 的 AlgorithmIdentifier。</p>'
        p2 = '<p>This is:</p>'
        p2_zh = '<p>其内容为：</p>'
        for old, new in [(p1, p1_zh), (p2, p2_zh)]:
            if old in c:
                c = c.replace(old, new)
                total_found += 1
            else:
                total_missed += 1
                print(f'  MISSED {rel}: {old[:80]!r}')
        if c != orig:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(c)
            total_files += 1
            cjk = re.findall(r'[一-鿿]', c)
            print(f'  {rel}: OK CJK={len(cjk)}')

    print(f'Updated {total_files} files; {total_found} found, {total_missed} missed')


if __name__ == '__main__':
    main()