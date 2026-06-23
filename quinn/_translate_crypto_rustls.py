"""Translate quinn/crypto/rustls/ files to Chinese."""

import os
import re

QUINN_ROOT = 'D:/Administrator/Documents/Code/rust_doc_all/quinn'
RUSTLS_DIR = os.path.join(QUINN_ROOT, 'crypto', 'rustls')


def verify(content, label):
    line_artifacts = re.findall(r'^\d+\t', content, flags=re.MULTILINE)
    if line_artifacts:
        print(f'  [WARN] {label}: {len(line_artifacts)} lines with cat-n style line numbers')
    cjk = re.findall(r'[一-鿿]', content)
    print(f'  [INFO] {label}: {len(cjk)} CJK characters')
    tag_pairs = ['html', 'head', 'body', 'main', 'section', 'div', 'p',
                 'a', 'span', 'h1', 'h2', 'h3', 'h4', 'ul', 'li',
                 'code', 'pre', 'details', 'summary', 'dl', 'dt', 'dd']
    for t in tag_pairs:
        opens = len(re.findall(rf'<{t}[\s>]', content))
        closes = len(re.findall(rf'</{t}>', content))
        if opens != closes:
            print(f'  [WARN] {label}: <{t}> open={opens} close={closes} diff={opens-closes}')


CHROME = [
    ('<html lang="en">', '<html lang="zh-CN">'),
    ('>Skip to main content<', '>跳到主要内容<'),
    ('This old browser is unsupported and will most likely display funky things.',
     '此旧版浏览器不受支持，很可能会显示异常内容。'),
    (' title="Copy item path to clipboard"', ' title="复制项目路径到剪贴板"'),
    ('>Copy item path<', '>复制项目路径<'),
    ('>Source<', '>源代码<'),
    ('>Expand description<', '>展开描述<'),
    ('>In crate quinn<', '>在 crate quinn 中<'),
    ('>In crate quinn::crypto::rustls<', '>在 crate quinn::crypto::rustls 中<'),
    ('>Trait Implementations<', '>trait 实现<'),
    ('>Auto Trait Implementations<', '>自动 trait 实现<'),
    ('>Blanket Implementations<', '>blanket 实现<'),
]

# Chrome for module index page
INDEX_CHROME = CHROME + [
    ('>Module Items<', '>模块项<'),
    (' title="Enums"', ' title="枚举"'),
    (' title="Structs"', ' title="结构体"'),
    ('>Enums<', '>枚举<'),
    ('>Structs<', '>结构体<'),
    ('>Module rustls<', '>模块 rustls<'),
    ('>Module <span>rustls</span>', '>模块 <span>rustls</span>'),
]

H1_KIND = {'Struct': '结构体', 'Enum': '枚举', 'Trait': 'trait', 'Module': '模块'}


def build_h1(kind, class_name, type_name, wbr_pos=None):
    name_with_wbr = type_name
    if wbr_pos:
        chars = list(type_name)
        for pos in sorted(wbr_pos, reverse=True):
            chars.insert(pos, '<wbr>')
        name_with_wbr = ''.join(chars)
    if class_name:
        return f'<h1>{kind} <span class="{class_name}">{name_with_wbr}</span>'
    return f'<h1>{kind} <span>{name_with_wbr}</span>'


def translate_content(rel_path, *, type_kind, type_name, wbr_pos=None,
                      title_in_english, title_in_chinese,
                      description_old, description_new,
                      docblocks=None, is_module=False):
    path = os.path.join(RUSTLS_DIR, rel_path)
    print(f'--- {rel_path} ---')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    chrome = INDEX_CHROME if is_module else CHROME
    for old, new in chrome:
        content = content.replace(old, new)

    content = content.replace(
        f'<title>{title_in_english}</title>',
        f'<title>{title_in_chinese}</title>',
    )
    content = content.replace(
        f'<meta name="description" content="{description_old}">',
        f'<meta name="description" content="{description_new}">',
    )

    h1_old = build_h1(type_kind, '' if is_module else type_kind.lower(), type_name, wbr_pos)
    h1_new = build_h1(H1_KIND[type_kind], '' if is_module else type_kind.lower(), type_name, wbr_pos)
    content = content.replace(h1_old, h1_new)

    if docblocks:
        for old, new in docblocks:
            if old not in content:
                print(f'  [MISS] docblock: {old[:60]!r}')
            content = content.replace(old, new)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    verify(content, rel_path)


# Module index
translate_content(
    'index.html',
    type_kind='Module', type_name='rustls',
    title_in_english='quinn::crypto::rustls - Rust',
    title_in_chinese='quinn::crypto::rustls - Rust',  # path-based, keep
    description_old='TLS interface based on rustls',
    description_new='基于 rustls 的 TLS 接口',
    docblocks=[(
        '<p>TLS interface based on rustls</p>',
        '<p>基于 rustls 的 TLS 接口</p>',
    )],
    is_module=True,
)

# enum.Error
translate_content(
    'enum.Error.html',
    type_kind='Enum', type_name='Error',
    title_in_english='Error in quinn::crypto::rustls - Rust',
    title_in_chinese='quinn::crypto::rustls 中的 Error - Rust',
    description_old='rustls reports protocol errors using this type.',
    description_new='rustls 通过该类型上报协议错误。',
    docblocks=[(
        '<p>rustls reports protocol errors using this type.</p>',
        '<p>rustls 通过该类型上报协议错误。</p>',
    )],
)

# struct.HandshakeData
translate_content(
    'struct.HandshakeData.html',
    type_kind='Struct', type_name='HandshakeData', wbr_pos=[9],
    title_in_english='HandshakeData in quinn::crypto::rustls - Rust',
    title_in_chinese='quinn::crypto::rustls 中的 HandshakeData - Rust',
    description_old='Authentication data for (rustls) TLS session',
    description_new='（基于 rustls 的）TLS 会话的身份认证数据',
    docblocks=[(
        '<p>Authentication data for (rustls) TLS session</p>',
        '<p>（基于 rustls 的）TLS 会话的身份认证数据</p>',
    )],
)

# struct.NoInitialCipherSuite (2 paragraphs)
translate_content(
    'struct.NoInitialCipherSuite.html',
    type_kind='Struct', type_name='NoInitialCipherSuite', wbr_pos=[10, 16],
    title_in_english='NoInitialCipherSuite in quinn::crypto::rustls - Rust',
    title_in_chinese='quinn::crypto::rustls 中的 NoInitialCipherSuite - Rust',
    description_old='The initial cipher suite (AES-128-GCM-SHA256) is not available',
    description_new='初始密码套件（AES-128-GCM-SHA256）不可用',
    docblocks=[(
        '<p>The initial cipher suite (AES-128-GCM-SHA256) is not available</p>\n<p>When the cipher suite is supplied <code>with_initial()</code>, it must be\n<a href="../../../rustls/enums/enum.CipherSuite.html#variant.TLS13_AES_128_GCM_SHA256" title="variant rustls::enums::CipherSuite::TLS13_AES_128_GCM_SHA256"><code>CipherSuite::TLS13_AES_128_GCM_SHA256</code></a>. When the cipher suite is derived from a config’s\n<a href="../../../rustls/crypto/struct.CryptoProvider.html" title="struct rustls::crypto::CryptoProvider"><code>CryptoProvider</code></a>, that provider must reference a cipher suite with the same ID.</p>',
        '<p>初始密码套件（AES-128-GCM-SHA256）不可用</p>\n<p>当通过 <code>with_initial()</code> 显式提供密码套件时，必须是\n<a href="../../../rustls/enums/enum.CipherSuite.html#variant.TLS13_AES_128_GCM_SHA256" title="variant rustls::enums::CipherSuite::TLS13_AES_128_GCM_SHA256"><code>CipherSuite::TLS13_AES_128_GCM_SHA256</code></a>。当密码套件是从某个 config 的\n<a href="../../../rustls/crypto/struct.CryptoProvider.html" title="struct rustls::crypto::CryptoProvider"><code>CryptoProvider</code></a> 派生而来时，该 provider 必须引用一个 ID 相同的密码套件。</p>',
    )],
)

# struct.QuicClientConfig (3 paragraphs + list)
translate_content(
    'struct.QuicClientConfig.html',
    type_kind='Struct', type_name='QuicClientConfig', wbr_pos=[4, 10],
    title_in_english='QuicClientConfig in quinn::crypto::rustls - Rust',
    title_in_chinese='quinn::crypto::rustls 中的 QuicClientConfig - Rust',
    description_old='A QUIC-compatible TLS client configuration',
    description_new='一个兼容 QUIC 的 TLS 客户端配置',
    docblocks=[(
        '<p>A QUIC-compatible TLS client configuration</p>\n<p>Quinn implicitly constructs a <code>QuicClientConfig</code> with reasonable defaults within\n<a href="../../struct.ClientConfig.html#method.with_root_certificates" title="associated function quinn::ClientConfig::with_root_certificates"><code>ClientConfig::with_root_certificates()</code></a> and <a href="../../struct.ClientConfig.html#method.with_platform_verifier" title="associated function quinn::ClientConfig::with_platform_verifier"><code>ClientConfig::with_platform_verifier()</code></a>.\nAlternatively, <code>QuicClientConfig</code>’s <a href="https://doc.rust-lang.org/1.95.0/core/convert/trait.TryFrom.html" title="trait core::convert::TryFrom"><code>TryFrom</code></a> implementation can be used to wrap around a\ncustom <a href="../../../rustls/client/client_conn/struct.ClientConfig.html" title="struct rustls::client::client_conn::ClientConfig"><code>rustls::ClientConfig</code></a>, in which case care should be taken around certain points:</p>\n<ul>\n<li>If <code>enable_early_data</code> is not set to true, then sending 0-RTT data will not be possible on\noutgoing connections.</li>\n<li>The <a href="../../../rustls/client/client_conn/struct.ClientConfig.html" title="struct rustls::client::client_conn::ClientConfig"><code>rustls::ClientConfig</code></a> must have TLS 1.3 support enabled for conversion to succeed.</li>\n</ul>\n<p>The object in the <code>resumption</code> field of the inner <a href="../../../rustls/client/client_conn/struct.ClientConfig.html" title="struct rustls::client::client_conn::ClientConfig"><code>rustls::ClientConfig</code></a> determines whether\ncalling <code>into_0rtt</code> on outgoing connections returns <code>Ok</code> or <code>Err</code>. It typically allows\n<code>into_0rtt</code> to proceed if it recognizes the server name, and defaults to an in-memory cache of\n256 server names.</p>',
        '<p>一个兼容 QUIC 的 TLS 客户端配置</p>\n<p>Quinn 会在 <a href="../../struct.ClientConfig.html#method.with_root_certificates" title="associated function quinn::ClientConfig::with_root_certificates"><code>ClientConfig::with_root_certificates()</code></a> 和 <a href="../../struct.ClientConfig.html#method.with_platform_verifier" title="associated function quinn::ClientConfig::with_platform_verifier"><code>ClientConfig::with_platform_verifier()</code></a> 内部以合理的默认值隐式构造一个 <code>QuicClientConfig</code>。\n另外，也可以利用 <code>QuicClientConfig</code> 的 <a href="https://doc.rust-lang.org/1.95.0/core/convert/trait.TryFrom.html" title="trait core::convert::TryFrom"><code>TryFrom</code></a> 实现来包装一个自定义的 <a href="../../../rustls/client/client_conn/struct.ClientConfig.html" title="struct rustls::client::client_conn::ClientConfig"><code>rustls::ClientConfig</code></a>，但需要留意以下几点：</p>\n<ul>\n<li>如果没有将 <code>enable_early_data</code> 设为 true，则在出站连接上将无法发送 0-RTT 数据。</li>\n<li><a href="../../../rustls/client/client_conn/struct.ClientConfig.html" title="struct rustls::client::client_conn::ClientConfig"><code>rustls::ClientConfig</code></a> 必须启用 TLS 1.3 支持，转换才能成功。</li>\n</ul>\n<p>内部 <a href="../../../rustls/client/client_conn/struct.ClientConfig.html" title="struct rustls::client::client_conn::ClientConfig"><code>rustls::ClientConfig</code></a> 的 <code>resumption</code> 字段中的对象决定了在出站连接上调用 <code>into_0rtt</code> 时会返回 <code>Ok</code> 还是 <code>Err</code>。通常而言，当它识别到对应的服务器名时就会允许 <code>into_0rtt</code> 继续进行，其默认实现是缓存最多 256 个服务器名的内存缓存。</p>',
    )],
)

# struct.QuicServerConfig (2 paragraphs + list)
translate_content(
    'struct.QuicServerConfig.html',
    type_kind='Struct', type_name='QuicServerConfig', wbr_pos=[4, 10],
    title_in_english='QuicServerConfig in quinn::crypto::rustls - Rust',
    title_in_chinese='quinn::crypto::rustls 中的 QuicServerConfig - Rust',
    description_old='A QUIC-compatible TLS server configuration',
    description_new='一个兼容 QUIC 的 TLS 服务器配置',
    docblocks=[(
        '<p>A QUIC-compatible TLS server configuration</p>\n<p>Quinn implicitly constructs a <code>QuicServerConfig</code> with reasonable defaults within\n<a href="../../struct.ServerConfig.html#method.with_single_cert" title="associated function quinn::ServerConfig::with_single_cert"><code>ServerConfig::with_single_cert()</code></a>. Alternatively, <code>QuicServerConfig</code>’s <a href="https://doc.rust-lang.org/1.95.0/core/convert/trait.TryFrom.html" title="trait core::convert::TryFrom"><code>TryFrom</code></a>\nimplementation or <code>with_initial</code> method can be used to wrap around a custom\n<a href="../../../rustls/server/server_conn/struct.ServerConfig.html" title="struct rustls::server::server_conn::ServerConfig"><code>rustls::ServerConfig</code></a>, in which case care should be taken around certain points:</p>\n<ul>\n<li>If <code>max_early_data_size</code> is not set to <code>u32::MAX</code>, the server will not be able to accept\nincoming 0-RTT data. QUIC prohibits <code>max_early_data_size</code> values other than 0 or <code>u32::MAX</code>.</li>\n<li>The <code>rustls::ServerConfig</code> must have TLS 1.3 support enabled for conversion to succeed.</li>\n</ul>',
        '<p>一个兼容 QUIC 的 TLS 服务器配置</p>\n<p>Quinn 会在 <a href="../../struct.ServerConfig.html#method.with_single_cert" title="associated function quinn::ServerConfig::with_single_cert"><code>ServerConfig::with_single_cert()</code></a> 内部以合理的默认值隐式构造一个 <code>QuicServerConfig</code>。另外，也可以利用 <code>QuicServerConfig</code> 的 <a href="https://doc.rust-lang.org/1.95.0/core/convert/trait.TryFrom.html" title="trait core::convert::TryFrom"><code>TryFrom</code></a> 实现或 <code>with_initial</code> 方法来包装一个自定义的 <a href="../../../rustls/server/server_conn/struct.ServerConfig.html" title="struct rustls::server::server_conn::ServerConfig"><code>rustls::ServerConfig</code></a>，但需要留意以下几点：</p>\n<ul>\n<li>如果没有将 <code>max_early_data_size</code> 设为 <code>u32::MAX</code>，则服务器将无法接受入站 0-RTT 数据。QUIC 协议禁止把 <code>max_early_data_size</code> 设为 0 或 <code>u32::MAX</code> 以外的值。</li>\n<li><code>rustls::ServerConfig</code> 必须启用 TLS 1.3 支持，转换才能成功。</li>\n</ul>',
    )],
)

# struct.TlsSession
translate_content(
    'struct.TlsSession.html',
    type_kind='Struct', type_name='TlsSession',
    title_in_english='TlsSession in quinn::crypto::rustls - Rust',
    title_in_chinese='quinn::crypto::rustls 中的 TlsSession - Rust',
    description_old='A rustls TLS session',
    description_new='一个基于 rustls 的 TLS 会话',
    docblocks=[(
        '<p>A rustls TLS session</p>',
        '<p>一个基于 rustls 的 TLS 会话</p>',
    )],
)
