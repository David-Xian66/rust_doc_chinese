"""Translate quinn's all.html (cross-crate items list) to Chinese.

Workflow per rust-doc-translation-pattern:
- Use Python open() directly (no Read tool).
- Translate only chrome (title, sidebar, headers); preserve all Rust identifiers.
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


def translate_all_html(content):
    # lang attribute
    content = content.replace('<html lang="en">', '<html lang="zh-CN">')

    # Meta description
    content = content.replace(
        '<meta name="description" content="List of all items in this crate">',
        '<meta name="description" content="本 crate 中所有项的列表">',
    )

    # Title
    content = content.replace(
        '<title>List of all items in this crate</title>',
        '<title>本 crate 中所有项的列表</title>',
    )

    pairs = [
        # Skip link
        ('>Skip to main content<', '>跳到主要内容<'),
        # IE warning
        ('This old browser is unsupported and will most likely display funky things.',
         '此旧版浏览器不受支持，很可能会显示异常内容。'),
        # Topbar label (different from sidebar "All Items")
        ('<a href="#">All</a>', '<a href="#">所有项</a>'),
        # Sidebar: Crate Items / toc labels
        ('>Crate Items<', '>crate 项<'),
        (' title="Structs"', ' title="结构体"'),
        (' title="Enums"', ' title="枚举"'),
        (' title="Traits"', ' title="trait"'),
        (' title="Functions"', ' title="函数"'),
        # Main H1
        ('<h1>List of all items</h1>', '<h1>所有项列表</h1>'),
        # Section headers (H3 in this file)
        ('<h3 id="structs">Structs</h3>', '<h3 id="structs">结构体</h3>'),
        ('<h3 id="enums">Enums</h3>', '<h3 id="enums">枚举</h3>'),
        ('<h3 id="traits">Traits</h3>', '<h3 id="traits">trait</h3>'),
        ('<h3 id="functions">Functions</h3>', '<h3 id="functions">函数</h3>'),
        # Sidebar visible toc labels
        ('>Structs<', '>结构体<'),
        ('>Enums<', '>枚举<'),
        ('>Traits<', '>trait<'),
        ('>Functions<', '>函数<'),
    ]
    for old, new in pairs:
        if old not in content:
            print(f'  [MISS] {old[:60]!r}')
        content = content.replace(old, new)
    return content


def main():
    path = os.path.join(QUINN_ROOT, 'all.html')
    print(f'--- {path} ---')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = translate_all_html(content)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    rel = os.path.relpath(path, QUINN_ROOT)
    verify(new_content, rel)
    # spot check: Rust identifiers preserved
    for ident in ['Accept', 'Connection', 'Endpoint', 'Bbr', 'CryptoError',
                  'struct.Accept.html', 'crypto/rustls/struct.HandshakeData.html',
                  'trait.AsyncTimer.html', 'fn.default_runtime.html']:
        if ident not in new_content:
            print(f'  [WARN] identifier missing: {ident!r}')
    # spot check: Chinese present
    for needle in ['所有项', '跳到主要内容', '结构体', '枚举', 'trait', '函数',
                   'crate 项', '本 crate 中所有项的列表', '所有项列表']:
        if needle not in new_content:
            print(f'  [WARN] translation missing: {needle!r}')
    print()


if __name__ == '__main__':
    main()
