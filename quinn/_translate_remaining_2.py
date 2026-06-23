"""Batch translate the 2 common boilerplate untranslated docblocks across remaining files."""

import os
import re

REMAINING = [
    'struct.Accept.html',
    'struct.AcceptBi.html',
    'struct.AcceptUni.html',
    'struct.ClosedStream.html',
    'struct.Connection.html',
    'struct.Endpoint.html',
    'struct.FrameType.html',
    'struct.IdleTimeout.html',
    'struct.IncomingFuture.html',
    'struct.NoneTokenLog.html',
    'struct.NoneTokenStore.html',
    'struct.OpenBi.html',
    'struct.OpenUni.html',
    'struct.ReadDatagram.html',
    'struct.RetryError.html',
    'struct.SendDatagram.html',
    'struct.StdSystemTime.html',
    'struct.TokenReuseError.html',
    'struct.TokioRuntime.html',
    'struct.VarIntBoundsExceeded.html',
    'struct.ZeroRttAccepted.html',
    'trait.AsyncTimer.html',
    'trait.TokenStore.html',
    'crypto/struct.CryptoError.html',
    'crypto/struct.ExportKeyingMaterialError.html',
    'crypto/struct.UnsupportedVersion.html',
    'crypto/trait.AeadKey.html',
    'crypto/rustls/struct.NoInitialCipherSuite.html',
]

BASE = 'D:/Administrator/Documents/Code/rust_doc_all/quinn'

T1_OLD = '</h4></section></summary><div class="docblock"><p>Returns the argument unchanged.</p>'
T1_NEW = '</h4></section></summary><div class="docblock"><p>原样返回该参数。</p>'

T2_OLD = ('<p>Calls <code>U::from(self)</code>.</p>\n<p>That is, this conversion is whatever the implementation of\n'
          '<code><a href="https://doc.rust-lang.org/1.95.0/core/convert/trait.From.html" title="trait core::convert::From">From</a>&lt;T&gt; for U</code> chooses to do.</p>')
T2_NEW = ('<p>调用 <code>U::from(self)</code>。</p>\n<p>也就是说，此转换行为完全由\n'
          '<code><a href="https://doc.rust-lang.org/1.95.0/core/convert/trait.From.html" title="trait core::convert::From">From</a>&lt;T&gt; for U</code> 的实现决定。</p>')


def main():
    total_files = 0
    total_found = 0
    for rel in REMAINING:
        path = os.path.join(BASE, rel)
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        orig = c
        n1 = c.count(T1_OLD)
        n2 = c.count(T2_OLD)
        if n1:
            c = c.replace(T1_OLD, T1_NEW)
        if n2:
            c = c.replace(T2_OLD, T2_NEW)
        if c != orig:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(c)
            total_files += 1
            total_found += n1 + n2
            cjk = re.findall(r'[一-鿿]', c)
            print(f'  {rel}: t1={n1} t2={n2} CJK={len(cjk)}')
    print(f'Updated {total_files} files; total replacements: {total_found}')


if __name__ == '__main__':
    main()