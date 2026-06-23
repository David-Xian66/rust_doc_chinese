"""Translate quinn/struct.ZeroRttAccepted.html to Chinese.

struct.ZeroRttAccepted is a Future that completes when a connection is fully
established. H1 contains <wbr> between Zero and RttAccepted.
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
    ('>Trait Implementations<', '>trait 实现<'),
    ('>Auto Trait Implementations<', '>自动 trait 实现<'),
    ('>Blanket Implementations<', '>blanket 实现<'),
]


def translate_struct_zerorttaccepted(content):
    for old, new in COMMON:
        if old not in content:
            print(f'  [MISS] common: {old[:60]!r}')
        content = content.replace(old, new)

    content = content.replace('<html lang="en">', '<html lang="zh-CN">')
    content = content.replace(
        '<title>ZeroRttAccepted in quinn - Rust</title>',
        '<title>quinn 中的 ZeroRttAccepted - Rust</title>',
    )
    content = content.replace(
        '<meta name="description" content="Future that completes when a connection is fully established">',
        '<meta name="description" content="在连接完全建立时完成的 Future">',
    )
    content = content.replace(
        '<h1>Struct <span class="struct">Zero<wbr>RttAccepted</span>',
        '<h1>结构体 <span class="struct">Zero<wbr>RttAccepted</span>',
    )
    content = content.replace(
        '<p>Future that completes when a connection is fully established</p>',
        '<p>在连接完全建立时完成的 Future</p>',
    )
    return content


def main():
    path = os.path.join(QUINN_ROOT, 'struct.ZeroRttAccepted.html')
    print(f'--- {path} ---')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = translate_struct_zerorttaccepted(content)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    rel = os.path.relpath(path, QUINN_ROOT)
    verify(new_content, rel)
    for ident in ['ZeroRttAccepted', 'Future',
                  '<span class="struct">Zero<wbr>RttAccepted</span>',
                  '<wbr>']:
        if ident not in new_content:
            print(f'  [WARN] identifier missing: {ident!r}')
    for needle in ['quinn 中的 ZeroRttAccepted', '在连接完全建立时完成的 Future',
                   '结构体 <span class="struct">Zero<wbr>RttAccepted</span>']:
        if needle not in new_content:
            print(f'  [WARN] translation missing: {needle!r}')
    print()


if __name__ == '__main__':
    main()
