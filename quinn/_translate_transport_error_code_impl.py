"""Translate all impl-section docblocks in quinn/struct.TransportErrorCode.html."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/struct.TransportErrorCode.html'

TRANSLATIONS = [
    # 1. crypto (from_tls)
    ('<p>Create QUIC error code from TLS alert code</p>',
     '<p>从 TLS alert 码构造 QUIC 错误码</p>'),
    # 2. NO_ERROR
    ('<p>the connection is being closed abruptly in the absence of any error</p>',
     '<p>在没有任何错误的情况下连接被突然关闭</p>'),
    # 3. INTERNAL_ERROR
    ('<p>the endpoint encountered an internal error and cannot continue with the connection</p>',
     '<p>端点遇到内部错误，无法继续连接</p>'),
    # 4. CONNECTION_REFUSED
    ('<p>the server refused to accept a new connection</p>',
     '<p>服务器拒绝接受新连接</p>'),
    # 5. FLOW_CONTROL_ERROR
    ('<p>received more data than permitted in advertised data limits</p>',
     '<p>收到的数据量超过了所通告的数据限制</p>'),
    # 6. STREAM_LIMIT_ERROR
    ('<p>received a frame for a stream identifier that exceeded advertised the stream limit for the corresponding stream type</p>',
     '<p>收到针对某个流 ID 的帧，其超过了对相应类型流所通告的流数量限制</p>'),
    # 7. STREAM_STATE_ERROR
    ('<p>received a frame for a stream that was not in a state that permitted that frame</p>',
     '<p>收到的帧所对应的流不处于允许该帧的状态</p>'),
    # 8. FINAL_SIZE_ERROR
    ('<p>received a STREAM frame or a RESET_STREAM frame containing a different final size to the one already established</p>',
     '<p>收到的 STREAM 或 RESET_STREAM 帧中所携带的最终大小与已建立的不一致</p>'),
    # 9. FRAME_ENCODING_ERROR
    ('<p>received a frame that was badly formatted</p>',
     '<p>收到了格式错误的帧</p>'),
    # 10. TRANSPORT_PARAMETER_ERROR
    ('<p>received transport parameters that were badly formatted, included an invalid value, was absent even though it is mandatory, was present though it is forbidden, or is otherwise in error</p>',
     '<p>收到的传输参数格式错误、包含非法值、缺失必选项、出现了禁用项，或存在其他错误</p>'),
    # 11. CONNECTION_ID_LIMIT_ERROR
    ('<p>the number of connection IDs provided by the peer exceeds the advertised active_connection_id_limit</p>',
     '<p>对端提供的连接 ID 数量超过所通告的 active_connection_id_limit</p>'),
    # 12. PROTOCOL_VIOLATION
    ('<p>detected an error with protocol compliance that was not covered by more specific error codes</p>',
     '<p>检测到无法被更具体的错误码覆盖的协议违规错误</p>'),
    # 13. INVALID_TOKEN
    ('<p>received an invalid Retry Token in a client Initial</p>',
     '<p>在客户端 Initial 中收到了无效的 Retry Token</p>'),
    # 14. APPLICATION_ERROR
    ('<p>the application or application protocol caused the connection to be closed during the handshake</p>',
     '<p>应用程序或应用层协议导致连接在握手期间被关闭</p>'),
    # 15. CRYPTO_BUFFER_EXCEEDED
    ('<p>received more data in CRYPTO frames than can be buffered</p>',
     '<p>CRYPTO 帧中收到的数据量超过了可缓冲的大小</p>'),
    # 16. KEY_UPDATE_ERROR
    ('<p>key update error</p>',
     '<p>密钥更新错误</p>'),
    # 17. AEAD_LIMIT_REACHED
    ('<p>the endpoint has reached the confidentiality or integrity limit for the AEAD algorithm</p>',
     '<p>端点已达到所用 AEAD 算法的机密性或完整性上限</p>'),
    # 18. NO_VIABLE_PATH
    ('<p>no viable network path exists</p>',
     '<p>不存在可行的网络路径</p>'),
    # 19. From impl boilerplate
    ('<p>Returns the argument unchanged.</p>',
     '<p>原样返回该参数。</p>'),
    # 20. From impl
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
