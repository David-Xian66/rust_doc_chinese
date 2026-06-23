"""Translate all quinn/crypto/ files to Chinese (index + 13 content pages)."""

import os
import re

QUINN_ROOT = 'D:/Administrator/Documents/Code/rust_doc_all/quinn'
CRYPTO_DIR = os.path.join(QUINN_ROOT, 'crypto')


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
    ('>In crate quinn::crypto<', '>在 crate quinn::crypto 中<'),
    ('>Trait Implementations<', '>trait 实现<'),
    ('>Auto Trait Implementations<', '>自动 trait 实现<'),
    ('>Blanket Implementations<', '>blanket 实现<'),
]

H1_KIND = {'Struct': '结构体', 'Enum': '枚举', 'Trait': 'trait'}


def build_h1(kind, class_name, type_name, wbr_pos=None):
    name_with_wbr = type_name
    if wbr_pos:
        chars = list(type_name)
        for pos in sorted(wbr_pos, reverse=True):
            chars.insert(pos, '<wbr>')
        name_with_wbr = ''.join(chars)
    return f'<h1>{kind} <span class="{class_name}">{name_with_wbr}</span>'


def translate_content(rel_path, *, type_kind, type_name, wbr_pos=None,
                      title_in_english, title_in_chinese,
                      description_old, description_new,
                      docblocks=None):
    path = os.path.join(CRYPTO_DIR, rel_path)
    print(f'--- {rel_path} ---')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    for old, new in CHROME:
        content = content.replace(old, new)

    content = content.replace(
        f'<title>{title_in_english}</title>',
        f'<title>{title_in_chinese}</title>',
    )
    content = content.replace(
        f'<meta name="description" content="{description_old}">',
        f'<meta name="description" content="{description_new}">',
    )

    h1_old = build_h1(type_kind, type_kind.lower(), type_name, wbr_pos)
    h1_new = build_h1(H1_KIND[type_kind], type_kind.lower(), type_name, wbr_pos)
    content = content.replace(h1_old, h1_new)

    if docblocks:
        for old, new in docblocks:
            if old not in content:
                print(f'  [MISS] docblock: {old[:60]!r}')
            content = content.replace(old, new)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    verify(content, rel_path)


# --- 5 structs ---
translate_content(
    'struct.CryptoError.html',
    type_kind='Struct', type_name='CryptoError', wbr_pos=[6],
    title_in_english='CryptoError in quinn::crypto - Rust',
    title_in_chinese='quinn::crypto 中的 CryptoError - Rust',
    description_old='Generic crypto errors',
    description_new='通用加密错误',
    docblocks=[(
        '<p>Generic crypto errors</p>',
        '<p>通用加密错误</p>',
    )],
)

translate_content(
    'struct.ExportKeyingMaterialError.html',
    type_kind='Struct', type_name='ExportKeyingMaterialError', wbr_pos=[6, 13, 20],
    title_in_english='ExportKeyingMaterialError in quinn::crypto - Rust',
    title_in_chinese='quinn::crypto 中的 ExportKeyingMaterialError - Rust',
    description_old='Error returned by Session::export_keying_material.',
    description_new='由 Session::export_keying_material 返回的错误。',
    docblocks=[(
        '<p>Error returned by <a href="trait.Session.html#tymethod.export_keying_material" title="method quinn::crypto::Session::export_keying_material">Session::export_keying_material</a>.</p>\n<p>This error occurs if the requested output length is too large.</p>',
        '<p>由 <a href="trait.Session.html#tymethod.export_keying_material" title="method quinn::crypto::Session::export_keying_material">Session::export_keying_material</a> 返回的错误。</p>\n<p>当请求的输出长度过大时会产生此错误。</p>',
    )],
)

translate_content(
    'struct.KeyPair.html',
    type_kind='Struct', type_name='KeyPair',
    title_in_english='KeyPair in quinn::crypto - Rust',
    title_in_chinese='quinn::crypto 中的 KeyPair - Rust',
    description_old='A pair of keys for bidirectional communication',
    description_new='用于双向通信的一对密钥',
    docblocks=[(
        '<p>A pair of keys for bidirectional communication</p>',
        '<p>用于双向通信的一对密钥</p>',
    )],
)

translate_content(
    'struct.Keys.html',
    type_kind='Struct', type_name='Keys',
    title_in_english='Keys in quinn::crypto - Rust',
    title_in_chinese='quinn::crypto 中的 Keys - Rust',
    description_old='A complete set of keys for a certain packet space',
    description_new='某个 packet space 下的完整密钥集合',
    docblocks=[(
        '<p>A complete set of keys for a certain packet space</p>',
        '<p>某个 packet space 下的完整密钥集合</p>',
    )],
)

translate_content(
    'struct.UnsupportedVersion.html',
    type_kind='Struct', type_name='UnsupportedVersion', wbr_pos=[11],
    title_in_english='UnsupportedVersion in quinn::crypto - Rust',
    title_in_chinese='quinn::crypto 中的 UnsupportedVersion - Rust',
    description_old='Error indicating that the specified QUIC version is not supported',
    description_new='表示指定的 QUIC 版本不受支持的错误',
    docblocks=[(
        '<p>Error indicating that the specified QUIC version is not supported</p>',
        '<p>表示指定的 QUIC 版本不受支持的错误</p>',
    )],
)

# --- 8 traits ---
translate_content(
    'trait.AeadKey.html',
    type_kind='Trait', type_name='AeadKey',
    title_in_english='AeadKey in quinn::crypto - Rust',
    title_in_chinese='quinn::crypto 中的 AeadKey - Rust',
    description_old='A key for sealing data with AEAD-based algorithms',
    description_new='使用基于 AEAD 的算法封装数据所用的密钥',
    docblocks=[(
        '<p>A key for sealing data with AEAD-based algorithms</p>',
        '<p>使用基于 AEAD 的算法封装数据所用的密钥</p>',
    )],
)

translate_content(
    'trait.ClientConfig.html',
    type_kind='Trait', type_name='ClientConfig', wbr_pos=[6],
    title_in_english='ClientConfig in quinn::crypto - Rust',
    title_in_chinese='quinn::crypto 中的 ClientConfig - Rust',
    description_old='Client-side configuration for the crypto protocol',
    description_new='加密协议的客户端配置',
    docblocks=[(
        '<p>Client-side configuration for the crypto protocol</p>',
        '<p>加密协议的客户端配置</p>',
    )],
)

translate_content(
    'trait.HandshakeTokenKey.html',
    type_kind='Trait', type_name='HandshakeTokenKey', wbr_pos=[9, 14],
    title_in_english='HandshakeTokenKey in quinn::crypto - Rust',
    title_in_chinese='quinn::crypto 中的 HandshakeTokenKey - Rust',
    description_old='A pseudo random key for HKDF',
    description_new='用于 HKDF 的伪随机密钥',
    docblocks=[(
        '<p>A pseudo random key for HKDF</p>',
        '<p>用于 HKDF 的伪随机密钥</p>',
    )],
)

translate_content(
    'trait.HeaderKey.html',
    type_kind='Trait', type_name='HeaderKey', wbr_pos=[6],
    title_in_english='HeaderKey in quinn::crypto - Rust',
    title_in_chinese='quinn::crypto 中的 HeaderKey - Rust',
    description_old='Keys used to protect packet headers',
    description_new='用于保护 packet header 的密钥',
    docblocks=[(
        '<p>Keys used to protect packet headers</p>',
        '<p>用于保护 packet header 的密钥</p>',
    )],
)

translate_content(
    'trait.HmacKey.html',
    type_kind='Trait', type_name='HmacKey',
    title_in_english='HmacKey in quinn::crypto - Rust',
    title_in_chinese='quinn::crypto 中的 HmacKey - Rust',
    description_old='A key for signing with HMAC-based algorithms',
    description_new='使用基于 HMAC 的算法进行签名所用的密钥',
    docblocks=[(
        '<p>A key for signing with HMAC-based algorithms</p>',
        '<p>使用基于 HMAC 的算法进行签名所用的密钥</p>',
    )],
)

translate_content(
    'trait.PacketKey.html',
    type_kind='Trait', type_name='PacketKey', wbr_pos=[6],
    title_in_english='PacketKey in quinn::crypto - Rust',
    title_in_chinese='quinn::crypto 中的 PacketKey - Rust',
    description_old='Keys used to protect packet payloads',
    description_new='用于保护 packet payload 的密钥',
    docblocks=[(
        '<p>Keys used to protect packet payloads</p>',
        '<p>用于保护 packet payload 的密钥</p>',
    )],
)

translate_content(
    'trait.ServerConfig.html',
    type_kind='Trait', type_name='ServerConfig', wbr_pos=[6],
    title_in_english='ServerConfig in quinn::crypto - Rust',
    title_in_chinese='quinn::crypto 中的 ServerConfig - Rust',
    description_old='Server-side configuration for the crypto protocol',
    description_new='加密协议的服务器端配置',
    docblocks=[(
        '<p>Server-side configuration for the crypto protocol</p>',
        '<p>加密协议的服务器端配置</p>',
    )],
)

translate_content(
    'trait.Session.html',
    type_kind='Trait', type_name='Session',
    title_in_english='Session in quinn::crypto - Rust',
    title_in_chinese='quinn::crypto 中的 Session - Rust',
    description_old='A cryptographic session (commonly TLS)',
    description_new='一个加密会话（通常是 TLS）',
    docblocks=[(
        '<p>A cryptographic session (commonly TLS)</p>',
        '<p>一个加密会话（通常是 TLS）</p>',
    )],
)
