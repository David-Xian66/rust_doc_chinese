#!/usr/bin/env python3
"""inject_seo_meta.py - 全站注入 SEO meta 标签

对仓库内所有 .html 文件，注入：
  - <link rel="canonical">
  - <meta property="og:..."> × 6
  - <meta name="twitter:..."> × 3
  - <meta name="keywords">
  - <script type="application/ld+json"> (仅根 index / crate 顶层 index)

注入锚点：
  - meta block → `<meta name="description" content="...">` 之后
  - JSON-LD   → `</head>` 之前

幂等：检测 `og:title` 存在即跳过。
bytes 模式保留 CRLF。

跳过目录：
  - static.files/、search.index/、trait.impl/、src/、__pycache__/、.git/、_common_tools/
  - 所有 *_old/ 备份目录

用法：
    python _common_tools/inject_seo_meta.py
"""

import os
import re
import json
import sys

ROOT = r'D:\Administrator\Documents\Code\rust_doc_all'
DOMAIN = 'https://rustdoc.p-cat.fun/'

SKIP_DIRS = {
    'static.files',
    'search.index',
    'trait.impl',
    'src',
    '__pycache__',
    '.git',
    '_common_tools',
}

# Crate 名 → 上游 GitHub 仓库
CRATE_REPO = {
    'coarsetime': 'https://github.com/jedisct1/rust-coarsetime',
    'enigo': 'https://github.com/enigo-rs/enigo',
    'ffmpeg_next': 'https://github.com/zmwangx/rust-ffmpeg',
    'ffmpeg_sys_next': 'https://github.com/zmwangx/rust-ffmpeg',
    'quinn': 'https://github.com/quinn-rs/quinn',
    'rcgen': 'https://github.com/est31/rcgen',
    'rdev': 'https://github.com/Narsil/rdev',
    'rustls_pki_types': 'https://github.com/rustls/pki-types',
    'scrap': 'https://github.com/quadrupleslap/scrap',
    'tokio': 'https://github.com/tokio-rs/tokio',
    'windows': 'https://github.com/microsoft/windows-rs',
    'windows_capture': 'https://github.com/zzhgithub/windows-capture',
    'windows_core': 'https://github.com/microsoft/windows-rs',
}

# Crate → 关键词补充（用于 keywords meta）
CRATE_KEYWORDS = {
    'coarsetime': 'Rust,时间,计时,coarsetime,Instant,Duration,性能',
    'enigo': 'Rust,键鼠,模拟,输入,enigo,跨平台,UI,自动化',
    'ffmpeg_next': 'Rust,FFmpeg,多媒体,音视频,编解码,绑定,ffmpeg_next',
    'ffmpeg_sys_next': 'Rust,FFmpeg,FFI,底层,bindings,ffmpeg_sys_next',
    'quinn': 'Rust,QUIC,传输协议,UDP,网络,quinn,Endpoint,Connection',
    'rdev': 'Rust,键鼠,监听,事件,跨平台,rdev,模拟',
    'rustls_pki_types': 'Rust,TLS,X.509,PEM,证书,密钥,rustls_pki_types',
    'tokio': 'Rust,异步,运行时,tokio,async,await,网络,定时器',
    'windows_capture': 'Rust,Windows,屏幕捕获,D3D11,DXGI,windows_capture',
    'windows_core': 'Rust,Windows,API,绑定,windows_core,COM',
    'windows': 'Rust,Windows,API,绑定,umbrella',
    'scrap': 'Rust,屏幕捕获,跨平台,scrap',
    'rcgen': 'Rust,证书,rcgen,X.509,生成器',
}

ROOT_KEYWORDS = (
    'Rust,中文文档,rustdoc,API,异步,网络,多媒体,'
    'tokio,quinn,enigo,rdev,rustls,ffmpeg,coarsetime,windows,'
    '翻译,中文,Rust 中文'
)


def should_skip_dir(d):
    if d in SKIP_DIRS:
        return True
    if d.endswith('_old') or d.startswith('_'):
        return True
    return False


def parse_meta(content):
    """提取 <title> 与 <meta name="description" content="..."> 的内容（bytes 模式）"""
    title_m = re.search(rb'<title>(.*?)</title>', content, re.DOTALL)
    desc_m = re.search(rb'<meta name="description" content="(.*?)"', content)
    title = title_m.group(1).decode('utf-8', 'replace').strip() if title_m else ''
    desc = desc_m.group(1).decode('utf-8', 'replace').strip() if desc_m else ''
    return title, desc


def escape_attr(s):
    """转义 meta attribute 内的 & 和双引号"""
    return s.replace('&', '&amp;').replace('"', '&quot;')


def build_seo_block(url, title, desc, is_root, keywords):
    """构造 meta 块（HTML 字符串，bytes 编码留给上层）"""
    og_type = 'website' if is_root else 'article'
    et = escape_attr(title)
    ed = escape_attr(desc)
    eu = escape_attr(url)
    parts = [
        f'<link rel="canonical" href="{eu}">',
        f'<meta property="og:type" content="{og_type}">',
        f'<meta property="og:title" content="{et}">',
        f'<meta property="og:description" content="{ed}">',
        f'<meta property="og:url" content="{eu}">',
        '<meta property="og:site_name" content="Rust 文档中文翻译">',
        '<meta property="og:locale" content="zh_CN">',
        '<meta property="og:locale:alternate" content="en_US">',
    ]
    if is_root:
        parts.append(
            f'<meta property="og:image" content="{DOMAIN}static.files/rust-logo-9a9549ea.svg">'
        )
    parts.extend([
        '<meta name="twitter:card" content="summary">',
        f'<meta name="twitter:title" content="{et}">',
        f'<meta name="twitter:description" content="{ed}">',
        f'<meta name="keywords" content="{escape_attr(keywords)}">',
    ])
    return ''.join(parts)


def build_jsonld_root(url):
    """根 index.html 的 WebSite + SearchAction JSON-LD"""
    obj = {
        '@context': 'https://schema.org',
        '@type': 'WebSite',
        'name': 'Rust 文档中文翻译',
        'description': '常用 Rust crate 的官方 rustdoc 文档的中文翻译版，覆盖异步、网络、TLS、多媒体、键鼠、FFI 等领域。',
        'url': url,
        'inLanguage': 'zh-CN',
        'potentialAction': {
            '@type': 'SearchAction',
            'target': {
                '@type': 'EntryPoint',
                'urlTemplate': 'https://rustdoc.p-cat.fun/{crate}/index.html?search={search_term}',
            },
            'query-input': 'required name=search_term',
        },
    }
    return f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False)}</script>'


def build_jsonld_crate(url, crate_name, desc, title):
    """crate 顶层 index.html 的 SoftwareSourceCode JSON-LD"""
    obj = {
        '@context': 'https://schema.org',
        '@type': 'SoftwareSourceCode',
        'name': crate_name,
        'description': desc,
        'programmingLanguage': 'Rust',
        'url': url,
        'inLanguage': 'zh-CN',
    }
    repo = CRATE_REPO.get(crate_name)
    if repo:
        obj['codeRepository'] = repo
        obj['author'] = {'@type': 'Organization', 'url': repo}
    return f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False)}</script>'


def keywords_for(crate_name, is_root):
    if is_root:
        return ROOT_KEYWORDS
    base = CRATE_KEYWORDS.get(
        crate_name,
        f'Rust,{crate_name},中文文档,rustdoc',
    )
    return base


def is_redirection_page(title, raw):
    """检测是否是 rustdoc 生成的"重定向"占位页（无 SEO 价值）"""
    if title in ('Redirection', '重定向'):
        return True
    # 也检测正文是否含 "Redirecting to" 标识
    if b'Redirecting to' in raw or '正在重定向到'.encode('utf-8') in raw:
        return True
    return False


def build_noindex_block():
    """仅含 robots noindex 的最小 meta 块（用于重定向占位页）"""
    return '<meta name="robots" content="noindex,follow">'


def main():
    updated = 0
    skipped_already = 0
    skipped_help = 0
    noindex_added = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if not should_skip_dir(d)]
        for f in filenames:
            if not f.endswith('.html'):
                continue
            path = os.path.join(dirpath, f)
            base = os.path.basename(path)
            # 跳过 rustdoc 标准帮助页（无 SEO 价值）
            if base == 'help.html':
                skipped_help += 1
                continue

            with open(path, 'rb') as fp:
                raw = fp.read()
            # 幂等检测
            if b'og:title' in raw or b'name="robots" content="noindex' in raw:
                skipped_already += 1
                continue

            title, desc = parse_meta(raw)
            if not title:
                # 没有 title — 跳过
                skipped_help += 1
                continue

            rel = os.path.relpath(path, ROOT).replace(os.sep, '/')
            url = DOMAIN + rel
            is_root = (rel == 'index.html')
            parts = rel.split('/')
            is_crate_index = (len(parts) == 2 and parts[1] == 'index.html')
            crate_name = parts[0] if is_crate_index or len(parts) >= 2 else ''

            # === 重定向占位页处理：仅加 noindex，跳过 OG/Twitter/JSON-LD ===
            if is_redirection_page(title, raw):
                anchor = b'<title>'
                idx = raw.find(anchor)
                if idx > 0:
                    noindex_bytes = build_noindex_block().encode('utf-8')
                    # 注入到 <title> 之后
                    end = raw.find(b'</title>', idx)
                    if end > 0:
                        insert_at = end + len(b'</title>')
                        new_raw = raw[:insert_at] + noindex_bytes + raw[insert_at:]
                        with open(path, 'wb') as fp:
                            fp.write(new_raw)
                        noindex_added += 1
                continue

            # === 常规页面：注入完整 SEO meta + 可选 JSON-LD ===
            # 优先用 <meta description>，否则用 title 退化
            if not desc:
                desc = title

            keywords = keywords_for(crate_name, is_root)
            seo_html = build_seo_block(url, title, desc, is_root, keywords)
            seo_bytes = seo_html.encode('utf-8')

            # 注入到 <meta name="description" content="..."> 之后；若不存在，注入到 <title> 之后
            anchor = b'<meta name="description" content="'
            idx = raw.find(anchor)
            if idx > 0:
                end = raw.find(b'>', idx)
                if end < 0:
                    continue
                new_raw = raw[:end + 1] + seo_bytes + raw[end + 1:]
            else:
                # 没有 meta description（但有 title）— 注入到 title 之后
                title_idx = raw.find(b'<title>')
                if title_idx < 0:
                    continue
                title_end = raw.find(b'</title>', title_idx)
                if title_end < 0:
                    continue
                insert_at = title_end + len(b'</title>')
                new_raw = raw[:insert_at] + seo_bytes + raw[insert_at:]

            # JSON-LD 注入到 </head> 之前（仅根 / crate index）
            if is_root or is_crate_index:
                if is_root:
                    jsonld = build_jsonld_root(url)
                else:
                    jsonld = build_jsonld_crate(url, crate_name, desc, title)
                jsonld_bytes = jsonld.encode('utf-8')
                head_end = new_raw.find(b'</head>')
                if head_end > 0:
                    new_raw = new_raw[:head_end] + jsonld_bytes + new_raw[head_end:]

            with open(path, 'wb') as fp:
                fp.write(new_raw)
            updated += 1

    print(
        f'Updated: {updated}  '
        f'Noindex added: {noindex_added}  '
        f'Skipped (already): {skipped_already}  '
        f'Skipped (help/no title): {skipped_help}'
    )


if __name__ == '__main__':
    main()
