"""Stage 2: translate index.html crate-level description (10 paragraphs)."""

import re

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/rustls_pki_types/index.html'

TRANSLATIONS = [
    ('<p>This crate provides types for representing X.509 certificates, keys and other types as\ncommonly used in the rustls ecosystem. It is intended to be used by crates that need to work\nwith such X.509 types, such as <a href="https://crates.io/crates/rustls">rustls</a>,\n<a href="https://crates.io/crates/rustls-webpki">rustls-webpki</a>, and others.</p>',
     '<p>本 crate 提供用于表示 X.509 证书、密钥及其他在 rustls 生态中常用的类型。它面向那些需要处理这些 X.509 类型的 crate，\n例如 <a href="https://crates.io/crates/rustls">rustls</a>、<a href="https://crates.io/crates/rustls-webpki">rustls-webpki</a> 等。</p>'),
    ('<p>Some of these crates used to define their own trivial wrappers around DER-encoded bytes.\nHowever, in order to avoid inconvenient dependency edges, these were all disconnected. By\nusing a common low-level crate of types with long-term stable API, we hope to avoid the\ndownsides of unnecessary dependency edges while providing good interoperability between crates.</p>',
     '<p>这些 crate 中有一些原本围绕 DER 编码字节定义了自己的简单包装类型。\n然而，为了避免产生不便的依赖关系，所有这些包装类型都已被解耦。\n通过使用一个长期 API 稳定的公共底层 crate，我们希望在避免不必要依赖关系弊病的同时，为各 crate 之间提供良好的互操作性。</p>'),
    ('<p>Many of the types defined in this crate represent DER-encoded data. DER is a binary encoding of\nthe ASN.1 format commonly used in web PKI specifications. It is a binary encoding, so it is\nrelatively compact when stored in memory. However, as a binary format, it is not very easy to\nwork with for humans and in contexts where binary data is inconvenient. For this reason,\nmany tools and protocols use a ASCII-based encoding of DER, called PEM. In addition to the\nbase64-encoded DER, PEM objects are delimited by header and footer lines which indicate the type\nof object contained in the PEM blob.</p>',
     '<p>本 crate 中定义的许多类型都表示 DER 编码数据。DER 是 ASN.1 格式的二进制编码，在 Web PKI 规范中被广泛使用。\n作为一种二进制格式，它在内存中存储时相当紧凑。\n但由于是二进制格式，对人类阅读以及在不便处理二进制的场景中使用并不友好。\n因此，许多工具和协议采用一种称为 PEM 的基于 ASCII 的 DER 编码方式。\n除了 base64 编码的 DER 之外，PEM 对象还通过头部和尾部行定界，标明该 PEM 数据块中所包含对象的类型。</p>'),
    ('<p>Types here can be created from:</p>',
     '<p>这些类型可通过以下方式创建：</p>'),
    ('<p>The <a href="pem/trait.PemObject.html" title="trait rustls_pki_types::pem::PemObject"><code>pem::PemObject</code></a> trait contains the full selection of ways to construct\nthese types from PEM encodings.  That includes ways to open and read from a file,\nfrom a slice, or from an <code>std::io</code> stream.</p>',
     '<p><a href="pem/trait.PemObject.html" title="trait rustls_pki_types::pem::PemObject"><code>pem::PemObject</code></a> 特性提供了从 PEM 编码构造这些类型的完整方式。\n包括从文件、字节切片，或从 <code>std::io</code> 流中读取并构造。</p>'),
    ('<p>There is also a lower-level API that allows a given PEM file to be fully consumed\nin one pass, even if it contains different data types: see the implementation of\nthe <a href="pem/trait.PemObject.html" title="trait rustls_pki_types::pem::PemObject"><code>pem::PemObject</code></a> trait on the <code>(pem::SectionKind, Vec&lt;u8&gt;)</code> tuple.</p>',
     '<p>还提供了一个更底层的 API，可一次性完整消费给定的 PEM 文件，\n即使其中包含不同的数据类型：见 <a href="pem/trait.PemObject.html" title="trait rustls_pki_types::pem::PemObject"><code>pem::PemObject</code></a> 特性在 <code>(pem::SectionKind, Vec&lt;u8&gt;)</code> 元组上的实现。</p>'),
    ('<p>This crate does not provide any functionality for creating new certificates or keys. However,\nthe <a href="https://docs.rs/rcgen">rcgen</a> crate can be used to create new certificates and keys.</p>',
     '<p>本 crate 不提供创建新证书或密钥的功能。不过，可以使用 <a href="https://docs.rs/rcgen">rcgen</a> crate 来创建新的证书和密钥。</p>'),
    ('<p>This crate intentionally <strong>does not</strong> implement <code>Clone</code> on private key types in\norder to minimize the exposure of private key data in memory.</p>',
     '<p>本 crate 故意<strong>不</strong>为私钥类型实现 <code>Clone</code>，\n以最大程度地减少私钥数据在内存中的暴露。</p>'),
    ('<p>If you want to extend the lifetime of a <code>PrivateKeyDer&lt;&gt;&gt;</code>, consider <a href="https://docs.rs/rustls-pki-types/latest/rustls_pki_types/enum.PrivateKeyDer.html#method.clone_key"><code>PrivateKeyDer::clone_key()</code></a>.\nAlternatively  since these types are immutable, consider wrapping the <code>PrivateKeyDer&lt;&gt;&gt;</code> in a <a href="https://doc.rust-lang.org/std/rc/struct.Rc.html"><code>Rc</code></a>\nor an <a href="https://doc.rust-lang.org/std/sync/struct.Arc.html"><code>Arc</code></a>.</p>',
     '<p>若希望延长 <code>PrivateKeyDer&lt;&gt;&gt;</code> 的生命周期，可考虑使用 <a href="https://docs.rs/rustls-pki-types/latest/rustls_pki_types/enum.PrivateKeyDer.html#method.clone_key"><code>PrivateKeyDer::clone_key()</code></a>。\n另外，由于这些类型是不可变的，也可以考虑将 <code>PrivateKeyDer&lt;&gt;&gt;</code> 包装在 <a href="https://doc.rust-lang.org/std/rc/struct.Rc.html"><code>Rc</code></a> 或 <a href="https://doc.rust-lang.org/std/sync/struct.Arc.html"><code>Arc</code></a> 中。</p>'),
    ('<p><a href="https://doc.rust-lang.org/std/time/struct.SystemTime.html"><code>std::time::SystemTime</code></a>\nis unavailable in <code>wasm32-unknown-unknown</code> targets, so calls to\n<a href="https://docs.rs/rustls-pki-types/latest/rustls_pki_types/struct.UnixTime.html#method.now"><code>UnixTime::now()</code></a>,\notherwise enabled by the <a href="https://docs.rs/crate/rustls-pki-types/latest/features#std"><code>std</code></a> feature,\nrequire building instead with the <a href="https://docs.rs/crate/rustls-pki-types/latest/features#web"><code>web</code></a>\nfeature. It gets time by calling <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/now"><code>Date.now()</code></a>\nin the browser.</p>',
     '<p><a href="https://doc.rust-lang.org/std/time/struct.SystemTime.html"><code>std::time::SystemTime</code></a> 在 <code>wasm32-unknown-unknown</code> 目标中不可用，\n因此对 <a href="https://docs.rs/rustls-pki-types/latest/rustls_pki_types/struct.UnixTime.html#method.now"><code>UnixTime::now()</code></a> 的调用——通常由 <a href="https://docs.rs/crate/rustls-pki-types/latest/features#std"><code>std</code></a> feature 启用——\n需要改为启用 <a href="https://docs.rs/crate/rustls-pki-types/latest/features#web"><code>web</code></a> feature 后再编译。\n该实现通过在浏览器中调用 <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/now"><code>Date.now()</code></a> 来获取时间。</p>'),
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
    print(f'Found: {found}/{len(TRANSLATIONS)}')
    print(f'CJK: {len(cjk)}')
    for m in missed:
        print(f'  MISSED: {m!r}')


if __name__ == '__main__':
    main()