"""Translate quinn/struct.Accept.html to Chinese.

struct.Accept is a Future type produced by Endpoint::accept. Its page is
mostly auto-generated trait/blanket impls from stdlib.
"""

import os
import re

QUINN_ROOT = 'D:/Administrator/Documents/Code/rust_doc_all/quinn'


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


COMMON = [
    ('>Skip to main content<', '>跳到主要内容<'),
    ('This old browser is unsupported and will most likely display funky things.',
     '此旧版浏览器不受支持，很可能会显示异常内容。'),
    (' title="Copy item path to clipboard"', ' title="复制项目路径到剪贴板"'),
    ('>Copy item path<', '>复制项目路径<'),
    ('>Source<', '>源代码<'),
    ('>Expand description<', '>展开描述<'),
    ('>In crate quinn<', '>在 crate quinn 中<'),
    # Sidebar H3 / body H2 (same English text used in two places)
    ('>Trait Implementations<', '>trait 实现<'),
    ('>Auto Trait Implementations<', '>自动 trait 实现<'),
    ('>Blanket Implementations<', '>blanket 实现<'),
]


def translate_struct_accept(content):
    for old, new in COMMON:
        if old not in content:
            print(f'  [MISS] common: {old[:60]!r}')
        content = content.replace(old, new)

    # lang attribute
    content = content.replace('<html lang="en">', '<html lang="zh-CN">')

    # Title: "Accept in quinn - Rust"
    content = content.replace(
        '<title>Accept in quinn - Rust</title>',
        '<title>quinn 中的 Accept - Rust</title>',
    )

    # Meta description
    content = content.replace(
        '<meta name="description" content="Future produced by `Endpoint::accept`">',
        '<meta name="description" content="由 `Endpoint::accept` 产生的 Future">',
    )

    # H1: "Struct <span class=\"struct\">Accept</span>"
    content = content.replace(
        '<h1>Struct <span class="struct">Accept</span>',
        '<h1>结构体 <span class="struct">Accept</span>',
    )

    # Docblock: "Future produced by `Endpoint::accept`"
    content = content.replace(
        '<p>Future produced by <a href="struct.Endpoint.html#method.accept" title="method quinn::Endpoint::accept"><code>Endpoint::accept</code></a></p>',
        '<p>由 <a href="struct.Endpoint.html#method.accept" title="method quinn::Endpoint::accept"><code>Endpoint::accept</code></a> 产生的 Future</p>',
    )

    return content


def main():
    path = os.path.join(QUINN_ROOT, 'struct.Accept.html')
    print(f'--- {path} ---')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = translate_struct_accept(content)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    rel = os.path.relpath(path, QUINN_ROOT)
    verify(new_content, rel)
    # spot check identifiers
    for ident in ['Accept', 'Endpoint', 'Future', 'Unpin', 'Incoming',
                  'doc.rust-lang.org', 'quinn::Endpoint::accept',
                  '<span class="struct">Accept</span>',
                  'struct.Endpoint.html#method.accept']:
        if ident not in new_content:
            print(f'  [WARN] identifier missing: {ident!r}')
    for needle in ['quinn 中的 Accept', '由 `Endpoint::accept` 产生的 Future',
                   '结构体 <span class="struct">Accept</span>',
                   'trait 实现', '自动 trait 实现', 'blanket 实现',
                   '在 crate quinn 中', '跳到主要内容',
                   '复制项目路径', '源代码', '展开描述']:
        if needle not in new_content:
            print(f'  [WARN] translation missing: {needle!r}')
    print()


if __name__ == '__main__':
    main()
