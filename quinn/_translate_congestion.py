"""Translate all quinn/congestion/ files to Chinese (index + 9 content pages)."""

import os
import re

QUINN_ROOT = 'D:/Administrator/Documents/Code/rust_doc_all/quinn'
CONGESTION_DIR = os.path.join(QUINN_ROOT, 'congestion')


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


# Chrome for content pages (struct/trait/enum/fn)
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
    ('>In crate quinn::congestion<', '>在 crate quinn::congestion 中<'),
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
    path = os.path.join(CONGESTION_DIR, rel_path)
    print(f'--- {rel_path} ---')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    for old, new in CHROME:
        if old not in content:
            # In crate quinn::congestion may not appear on every page
            if 'quinn::congestion' not in old:
                pass  # silently skip
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


# Bbr (multi-paragraph)
translate_content(
    'struct.Bbr.html',
    type_kind='Struct', type_name='Bbr',
    title_in_english='Bbr in quinn::congestion - Rust',
    title_in_chinese='quinn::congestion 中的 Bbr - Rust',
    description_old='Experimental! Use at your own risk.',
    description_new='实验性！使用风险自负。',
    docblocks=[(
        '<p>Experimental! Use at your own risk.</p>\n<p>Aims for reduced buffer bloat and improved performance over high bandwidth-delay product networks.\nBased on google’s quiche implementation <a href="https://source.chromium.org/chromium/chromium/src/+/master:net/third_party/quiche/src/quic/core/congestion_control/bbr_sender.cc">https://source.chromium.org/chromium/chromium/src/+/master:net/third_party/quiche/src/quic/core/congestion_control/bbr_sender.cc</a>\nof BBR <a href="https://datatracker.ietf.org/doc/html/draft-cardwell-iccrg-bbr-congestion-control">https://datatracker.ietf.org/doc/html/draft-cardwell-iccrg-bbr-congestion-control</a>.\nMore discussion and links at <a href="https://groups.google.com/g/bbr-dev">https://groups.google.com/g/bbr-dev</a>.</p>',
        '<p>实验性！使用风险自负。</p>\n<p>目标是减少 buffer bloat，并在高带宽时延积（BDP）的网络上提升性能。基于 Google 的 quiche 实现 <a href="https://source.chromium.org/chromium/chromium/src/+/master:net/third_party/quiche/src/quic/core/congestion_control/bbr_sender.cc">https://source.chromium.org/chromium/chromium/src/+/master:net/third_party/quiche/src/quic/core/congestion_control/bbr_sender.cc</a>，\n对应的 BBR 规范见 <a href="https://datatracker.ietf.org/doc/html/draft-cardwell-iccrg-bbr-congestion-control">https://datatracker.ietf.org/doc/html/draft-cardwell-iccrg-bbr-congestion-control</a>。\n更多讨论与链接见 <a href="https://groups.google.com/g/bbr-dev">https://groups.google.com/g/bbr-dev</a>。</p>',
    )],
)

# BbrConfig
translate_content(
    'struct.BbrConfig.html',
    type_kind='Struct', type_name='BbrConfig',
    title_in_english='BbrConfig in quinn::congestion - Rust',
    title_in_chinese='quinn::congestion 中的 BbrConfig - Rust',
    description_old='Configuration for the `Bbr` congestion controller',
    description_new='`Bbr` 拥塞控制器的配置',
    docblocks=[(
        '<p>Configuration for the <a href="struct.Bbr.html" title="struct quinn::congestion::Bbr"><code>Bbr</code></a> congestion controller</p>',
        '<p><a href="struct.Bbr.html" title="struct quinn::congestion::Bbr"><code>Bbr</code></a> 拥塞控制器的配置</p>',
    )],
)

# ControllerMetrics
translate_content(
    'struct.ControllerMetrics.html',
    type_kind='Struct', type_name='ControllerMetrics', wbr_pos=[10],
    title_in_english='ControllerMetrics in quinn::congestion - Rust',
    title_in_chinese='quinn::congestion 中的 ControllerMetrics - Rust',
    description_old='Common congestion controller metrics',
    description_new='拥塞控制器的通用指标',
    docblocks=[(
        '<p>Common congestion controller metrics</p>',
        '<p>拥塞控制器的通用指标</p>',
    )],
)

# Cubic
translate_content(
    'struct.Cubic.html',
    type_kind='Struct', type_name='Cubic',
    title_in_english='Cubic in quinn::congestion - Rust',
    title_in_chinese='quinn::congestion 中的 Cubic - Rust',
    description_old='The RFC8312 congestion controller, as widely used for TCP',
    description_new='RFC 8312 拥塞控制器，与 TCP 中广泛使用的实现一致',
    docblocks=[(
        '<p>The RFC8312 congestion controller, as widely used for TCP</p>',
        '<p>RFC 8312 拥塞控制器，与 TCP 中广泛使用的实现一致</p>',
    )],
)

# CubicConfig
translate_content(
    'struct.CubicConfig.html',
    type_kind='Struct', type_name='CubicConfig', wbr_pos=[5],
    title_in_english='CubicConfig in quinn::congestion - Rust',
    title_in_chinese='quinn::congestion 中的 CubicConfig - Rust',
    description_old='Configuration for the `Cubic` congestion controller',
    description_new='`Cubic` 拥塞控制器的配置',
    docblocks=[(
        '<p>Configuration for the <code>Cubic</code> congestion controller</p>',
        '<p><code>Cubic</code> 拥塞控制器的配置</p>',
    )],
)

# NewReno
translate_content(
    'struct.NewReno.html',
    type_kind='Struct', type_name='NewReno',
    title_in_english='NewReno in quinn::congestion - Rust',
    title_in_chinese='quinn::congestion 中的 NewReno - Rust',
    description_old='A simple, standard congestion controller',
    description_new='一种简单、标准的拥塞控制器',
    docblocks=[(
        '<p>A simple, standard congestion controller</p>',
        '<p>一种简单、标准的拥塞控制器</p>',
    )],
)

# NewRenoConfig
translate_content(
    'struct.NewRenoConfig.html',
    type_kind='Struct', type_name='NewRenoConfig', wbr_pos=[7],
    title_in_english='NewRenoConfig in quinn::congestion - Rust',
    title_in_chinese='quinn::congestion 中的 NewRenoConfig - Rust',
    description_old='Configuration for the `NewReno` congestion controller',
    description_new='`NewReno` 拥塞控制器的配置',
    docblocks=[(
        '<p>Configuration for the <code>NewReno</code> congestion controller</p>',
        '<p><code>NewReno</code> 拥塞控制器的配置</p>',
    )],
)

# Controller trait
translate_content(
    'trait.Controller.html',
    type_kind='Trait', type_name='Controller',
    title_in_english='Controller in quinn::congestion - Rust',
    title_in_chinese='quinn::congestion 中的 Controller - Rust',
    description_old='Common interface for different congestion controllers',
    description_new='不同拥塞控制器的公共接口',
    docblocks=[(
        '<p>Common interface for different congestion controllers</p>',
        '<p>不同拥塞控制器的公共接口</p>',
    )],
)

# ControllerFactory trait
translate_content(
    'trait.ControllerFactory.html',
    type_kind='Trait', type_name='ControllerFactory', wbr_pos=[10],
    title_in_english='ControllerFactory in quinn::congestion - Rust',
    title_in_chinese='quinn::congestion 中的 ControllerFactory - Rust',
    description_old='Constructs controllers on demand',
    description_new='按需构造控制器',
    docblocks=[(
        '<p>Constructs controllers on demand</p>',
        '<p>按需构造控制器</p>',
    )],
)
