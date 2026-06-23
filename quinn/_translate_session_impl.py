"""Translate 12 untranslated docblocks in quinn/crypto/trait.Session.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/crypto/trait.Session.html'

TRANSLATIONS = [
    ('<p>Create the initial set of keys given the client’s initial destination ConnectionId</p>',
     '<p>根据客户端的初始目标 ConnectionId 创建初始的密钥集合</p>'),
    ('<p>Get data negotiated during the handshake, if available</p>\n<p>Returns <code>None</code> until the connection emits <code>HandshakeDataReady</code>.</p>',
     '<p>获取握手期间协商的数据（若有）</p>\n<p>在连接发出 <code>HandshakeDataReady</code> 之前返回 <code>None</code>。</p>'),
    ('<p>Get the peer’s identity, if available</p>',
     '<p>获取对端的身份（若有）</p>'),
    ('<p>Get the 0-RTT keys if available (clients only)</p>\n<p>On the client side, this method can be used to see if 0-RTT key material is available\nto start sending data before the protocol handshake has completed.</p>\n<p>Returns <code>None</code> if the key material is not available. This might happen if you have\nnot connected to this server before.</p>',
     '<p>若 0-RTT 密钥可用则返回（仅客户端）</p>\n<p>在客户端，该方法可用于判断在协议握手完成之前是否有可用的 0-RTT 密钥材料，从而开始发送数据。</p>\n<p>若密钥材料不可用则返回 <code>None</code>。例如之前未曾连接过该服务器时就可能出现这种情况。</p>'),
    ('<p>If the 0-RTT-encrypted data has been accepted by the peer</p>',
     '<p>对端是否已接受 0-RTT 加密数据</p>'),
    ('<p>Returns <code>true</code> until the connection is fully established.</p>',
     '<p>在连接完全建立之前返回 <code>true</code>。</p>'),
    ('<p>Read bytes of handshake data</p>\n<p>This should be called with the contents of <code>CRYPTO</code> frames. If it returns <code>Ok</code>, the\ncaller should call <code>write_handshake()</code> to check if the crypto protocol has anything\nto send to the peer. This method will only return <code>true</code> the first time that\nhandshake data is available. Future calls will always return false.</p>\n<p>On success, returns <code>true</code> iff <code>self.handshake_data()</code> has been populated.</p>',
     '<p>读取握手数据的字节</p>\n<p>应当使用 <code>CRYPTO</code> 帧的内容调用本方法。若返回 <code>Ok</code>，调用方应调用 <code>write_handshake()</code> 检查加密协议是否有内容要发给对端。该方法仅在首次握手数据就绪时返回 <code>true</code>，后续调用将始终返回 false。</p>\n<p>成功时，当且仅当 <code>self.handshake_data()</code> 已被填充时返回 <code>true</code>。</p>'),
    ('<p>The peer’s QUIC transport parameters</p>\n<p>These are only available after the first flight from the peer has been received.</p>',
     '<p>对端的 QUIC 传输参数</p>\n<p>仅在收到对端的第一批数据之后才可用。</p>'),
    ('<p>Writes handshake bytes into the given buffer and optionally returns the negotiated keys</p>\n<p>When the handshake proceeds to the next phase, this method will return a new set of\nkeys to encrypt data with.</p>',
     '<p>将握手字节写入给定缓冲区，并可选择性地返回协商出的密钥</p>\n<p>当握手进入下一阶段时，此方法会返回一组用于加密数据的新密钥。</p>'),
    ('<p>Compute keys for the next key update</p>',
     '<p>为下一次密钥更新计算密钥</p>'),
    ('<p>Verify the integrity of a retry packet</p>',
     '<p>校验 retry 包的完整性</p>'),
    ('<p>Fill <code>output</code> with <code>output.len()</code> bytes of keying material derived\nfrom the <a href="trait.Session.html" title="trait quinn::crypto::Session">Session</a>’s secrets, using <code>label</code> and <code>context</code> for domain\nseparation.</p>\n<p>This function will fail, returning <a href="struct.ExportKeyingMaterialError.html" title="struct quinn::crypto::ExportKeyingMaterialError">ExportKeyingMaterialError</a>,\nif the requested output length is too large.</p>',
     '<p>从 <a href="trait.Session.html" title="trait quinn::crypto::Session">Session</a> 的密钥派生 <code>output.len()</code> 个字节的密钥材料并写入 <code>output</code>，使用 <code>label</code> 与 <code>context</code> 进行域分离。</p>\n<p>若请求的输出长度过大，此函数将失败并返回 <a href="struct.ExportKeyingMaterialError.html" title="struct quinn::crypto::ExportKeyingMaterialError">ExportKeyingMaterialError</a>。</p>'),
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