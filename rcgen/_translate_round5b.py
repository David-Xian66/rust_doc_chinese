"""Round 5b: Fix the 4 remaining patterns with NBSP and exact whitespace."""
import os
import re

BASE = 'D:/Administrator/Documents/Code/rust_doc_all/rcgen'

# Use partial patterns (sliced around the unique English phrase) for robustness.
JOBS = [
    # ----- enum.KeyIdMethod.html (2nd paragraph with line break) -----
    (
        'enum.KeyIdMethod.html',
        [
            ('<p>Key identifiers should be derived from the public key data. <a href="https://www.rfc-editor.org/rfc/rfc7093">RFC 7093</a> defines\r\n'
             'three methods to do so using a choice of SHA256 (method 1), SHA384 (method 2), or SHA512\r\n'
             '(method 3). In each case the first 160 bits of the hash are used as the key identifier\r\n'
             'to match the output length that would be produced were SHA1 used (a legacy option defined\r\n'
             'in RFC 5280).</p>',
             '<p>密钥标识符应从公钥数据派生。<a href="https://www.rfc-editor.org/rfc/rfc7093">RFC 7093</a> 规定了三种实现方式：\n'
             '分别使用 SHA256（方法 1）、SHA384（方法 2）或 SHA512（方法 3）。\n'
             '在每种情况下，均取哈希值的前 160 位作为密钥标识符，\n'
             '以匹配使用 SHA1（RFC 5280 中定义的遗留选项）时所产生输出的长度。</p>'),
        ],
    ),
    # ----- enum.OtherNameValue.html (NBSP not section sign) -----
    (
        'enum.OtherNameValue.html',
        [
            ('<p>An <code>OtherName</code> value, defined in <a href="https://datatracker.ietf.org/doc/html/rfc5280#section-4.1.2.4">RFC 5280 §4.1.2.4</a>.</p>',
             '<p>一个 <code>OtherName</code> 值，定义见 <a href="https://datatracker.ietf.org/doc/html/rfc5280#section-4.1.2.4">RFC 5280 §4.1.2.4</a>。</p>'),
        ],
    ),
    # ----- enum.RevocationReason.html (NBSP not section sign) -----
    (
        'enum.RevocationReason.html',
        [
            ('<p>Identifies the reason a certificate was revoked.\r\n'
             'See <a href="https://www.rfc-editor.org/rfc/rfc5280#section-5.3.1">RFC 5280 §5.3.1</a></p>',
             '<p>指明证书被吊销的原因。\n'
             '参见 <a href="https://www.rfc-editor.org/rfc/rfc5280#section-5.3.1">RFC 5280 §5.3.1</a></p>'),
        ],
    ),
    # ----- index.html (no line break before final <a>) -----
    (
        'index.html',
        [
            ('<p>The most simple way of using this crate is by calling the\r\n'
             '<a href="fn.generate_simple_self_signed.html" title="fn rcgen::generate_simple_self_signed"><code>generate_simple_self_signed</code></a> function.\r\n'
             'For more customization abilities, construct a <a href="struct.CertificateParams.html" title="struct rcgen::CertificateParams"><code>CertificateParams</code></a> and\r\n'
             'a key pair to call <a href="struct.CertificateParams.html#method.signed_by" title="method rcgen::CertificateParams::signed_by"><code>CertificateParams::signed_by()</code></a> or <a href="struct.CertificateParams.html#method.self_signed" title="method rcgen::CertificateParams::self_signed"><code>CertificateParams::self_signed()</code></a>.</p>',
             '<p>使用本 crate 最简单的方式是调用 <a href="fn.generate_simple_self_signed.html" title="fn rcgen::generate_simple_self_signed"><code>generate_simple_self_signed</code></a> 函数。\n'
             '如果需要更强的定制能力，可以构造一个 <a href="struct.CertificateParams.html" title="struct rcgen::CertificateParams"><code>CertificateParams</code></a> 与一个密钥对，\n'
             '然后调用 <a href="struct.CertificateParams.html#method.signed_by" title="method rcgen::CertificateParams::signed_by"><code>CertificateParams::signed_by()</code></a> 或\n'
             '<a href="struct.CertificateParams.html#method.self_signed" title="method rcgen::CertificateParams::self_signed"><code>CertificateParams::self_signed()</code></a>。</p>'),
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
