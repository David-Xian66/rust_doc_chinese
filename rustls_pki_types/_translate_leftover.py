"""rustls_pki_types 第 N 阶段：补译 _strict_p_audit 漏网的多段 <p>"""
import os
import re

# 注意：模式串里必须保留原始 \r\n 和 “/”（UTF-8 编码）
PAIRS = [
    # ===== enum.ServerName.html =====
    # variant.DnsName
    ('The server is identified by a DNS name.  The name\r\nis sent in the TLS Server Name Indication (SNI)\r\nextension.',
     '服务器通过 DNS 名称标识。该名称通过 TLS 的 Server Name Indication (SNI)\r\nextension（服务器名称指示扩展）发送。'),
    ('The server is identified by a DNS name.  The name\nis sent in the TLS Server Name Indication (SNI)\nextension.',
     '服务器通过 DNS 名称标识。该名称通过 TLS 的 Server Name Indication (SNI)\nextension（服务器名称指示扩展）发送。'),
    # variant.IpAddress
    ('The server is identified by an IP address. SNI is not\r\ndone.',
     '服务器通过 IP 地址标识，不发送 SNI。'),
    ('The server is identified by an IP address. SNI is not\ndone.',
     '服务器通过 IP 地址标识，不发送 SNI。'),
    # method.from-7 (TryFrom<i32> etc.)
    ('Returns the argument unchanged.',
     '原样返回参数。'),
    # method.into (TryFrom::try_from -> Into::into)
    ('That is, this conversion is whatever the implementation of\r\nFrom&lt;T&gt; for U chooses to do.',
     '即此转换的实际行为取决于 From&lt;T&gt; for U 的实现。'),
    ('That is, this conversion is whatever the implementation of\nFrom&lt;T&gt; for U chooses to do.',
     '即此转换的实际行为取决于 From&lt;T&gt; for U 的实现。'),

    # ===== pem/enum.Error.html =====
    # variant.MissingSectionEnd
    ('a section is missing its “END marker” line',
     '某个 section 缺少 "END marker" 行'),
    # variant.MissingSectionEnd.field.end_marker
    ('the expected “END marker” line that was not found',
     '未能找到的 "END marker" 行'),
    # variant.IllegalSectionStart
    ('syntax error found in the line that starts a new section',
     '在开始新 section 的行中发现语法错误'),
    # variant.IllegalSectionStart.field.line
    ('line that contains the syntax error',
     '包含语法错误的行'),
    # variant.Io
    ('I/O errors, from APIs that accept std::io types.',
     'I/O 错误，来自接受 std::io 类型的 API。'),
    # variant.NoItemsFound
    ('No items found of desired type',
     '未找到期望类型的条目'),
    # variant.SectionTooLarge
    ('PEM section exceeds maximum allowed size of 256 MB',
     'PEM section 超过最大允许大小 256 MB'),

    # ===== pem/enum.SectionKind.html =====
    # variant.Certificate
    ('A DER-encoded x509 certificate.',
     '一个 DER 编码的 x509 证书。'),
    # variant.Certificate "Appears as"
    ('Appears as “CERTIFICATE” in PEM files.',
     '在 PEM 文件中显示为 "CERTIFICATE"。'),
    # variant.PublicKey
    ('A DER-encoded Subject Public Key Info; as specified in RFC 7468.',
     '一个 DER 编码的 Subject Public Key Info（主体公钥信息），如 RFC 7468 所规定。'),
    ('Appears as “PUBLIC KEY” in PEM files.',
     '在 PEM 文件中显示为 "PUBLIC KEY"。'),
    # variant.RsaPrivateKey
    ('A DER-encoded plaintext RSA private key; as specified in PKCS #1/RFC 3447',
     '一个 DER 编码的明文 RSA 私钥，如 PKCS #1 / RFC 3447 所规定'),
    ('Appears as “RSA PRIVATE KEY” in PEM files.',
     '在 PEM 文件中显示为 "RSA PRIVATE KEY"。'),
    # variant.PrivateKey
    ('A DER-encoded plaintext private key; as specified in PKCS #8/RFC 5958',
     '一个 DER 编码的明文私钥，如 PKCS #8 / RFC 5958 所规定'),
    ('Appears as “PRIVATE KEY” in PEM files.',
     '在 PEM 文件中显示为 "PRIVATE KEY"。'),
    # variant.EcPrivateKey
    ('A Sec1-encoded plaintext private key; as specified in RFC 5915',
     '一个 Sec1 编码的明文私钥，如 RFC 5915 所规定'),
    ('Appears as “EC PRIVATE KEY” in PEM files.',
     '在 PEM 文件中显示为 "EC PRIVATE KEY"。'),
    # variant.Crl
    ('A Certificate Revocation List; as specified in RFC 5280',
     '一个证书吊销列表（CRL），如 RFC 5280 所规定'),
    ('Appears as “X509 CRL” in PEM files.',
     '在 PEM 文件中显示为 "X509 CRL"。'),
    # variant.Csr
    ('A Certificate Signing Request; as specified in RFC 2986',
     '一个证书签名请求（CSR），如 RFC 2986 所规定'),
    ('Appears as “CERTIFICATE REQUEST” in PEM files.',
     '在 PEM 文件中显示为 "CERTIFICATE REQUEST"。'),
    # variant.EchConfigList
    ('An EchConfigList structure, as specified in\r\nhttps://www.ietf.org/archive/id/draft-farrell-tls-pemesni-05.html.',
     '一个 EchConfigList 结构，如\r\nhttps://www.ietf.org/archive/id/draft-farrell-tls-pemesni-05.html 所规定。'),
    ('An EchConfigList structure, as specified in\nhttps://www.ietf.org/archive/id/draft-farrell-tls-pemesni-05.html.',
     '一个 EchConfigList 结构，如\nhttps://www.ietf.org/archive/id/draft-farrell-tls-pemesni-05.html 所规定。'),
    ('Appears as “ECHCONFIG” in PEM files.',
     '在 PEM 文件中显示为 "ECHCONFIG"。'),
]

# Read more → 更多信息
READ_MORE = ('>Read more</a>', '>更多信息</a>')


def apply(text):
    applied = []
    for en, zh in PAIRS:
        if en in text:
            text = text.replace(en, zh)
            applied.append(en[:60])
    if READ_MORE[0] in text:
        c = text.count(READ_MORE[0])
        text = text.replace(READ_MORE[0], READ_MORE[1])
        applied.append(f'Read more x {c}')
    return text, applied


total = 0
mod = 0
per_file = {}
for root, dirs, fs in os.walk('rustls_pki_types'):
    for fn in fs:
        if not fn.endswith('.html'):
            continue
        path = os.path.join(root, fn)
        with open(path, 'rb') as f:
            before = f.read().decode('utf-8')
        after, applied = apply(before)
        if after != before:
            with open(path, 'wb') as f:
                f.write(after.encode('utf-8'))
            mod += 1
            total += len(applied)
            per_file[os.path.relpath(path, 'rustls_pki_types')] = applied

print(f'Modified {mod} files, {total} replacements')
for f in sorted(per_file):
    print(f'\n{f}:')
    for a in per_file[f]:
        print(f'  - {a}')