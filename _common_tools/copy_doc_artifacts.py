"""复制 cargo doc 产物：search.index/, src/, help.html 到本仓库，更新 crates.js。

用法：
    python _common_tools/copy_doc_artifacts.py

源目录: D:\\Administrator\\Documents\\Code\\demo_sc\\target\\doc\\
目标目录: 当前仓库根（脚本运行时的 cwd 必须是 rust_doc_all 根）

可重复运行：目标已存在则覆盖 src/* 和 search.index/*；
crates.js 仅在内容变化时写入；help.html 同样。
"""
import os
import shutil
import sys

SRC = r'D:\Administrator\Documents\Code\demo_sc\target\doc'
DST = '.'  # 仓库根

# 我们翻译过的 crate（用于 crates.js）
OUR_CRATES = [
    "coarsetime",
    "enigo",
    "ffmpeg_next",
    "ffmpeg_sys_next",
    "quinn",
    "rdev",
    "rustls_pki_types",
    "scrap",
    "tokio",
    "windows",
    "windows_capture",
    "windows_core",
]


def copy_dir_tree(src_subdir, dst_subdir):
    """递归复制整个目录。已存在的目标被覆盖。"""
    src = os.path.join(SRC, src_subdir)
    dst = os.path.join(DST, dst_subdir)
    if not os.path.isdir(src):
        print(f'  SKIP: source not found: {src}')
        return False

    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    return True


def copy_file(filename):
    src = os.path.join(SRC, filename)
    dst = os.path.join(DST, filename)
    if not os.path.isfile(src):
        print(f'  SKIP: source not found: {src}')
        return False
    shutil.copy2(src, dst)
    return True


def write_crates_js():
    """写 crates.js：保留我们翻译过的 11 个 crate，按字典序。"""
    cr = sorted(OUR_CRATES)
    # rustdoc 原版的 crates.js 末尾有 //{"start":N,"fragment_lengths":[...]} 注释
    # main.js 不依赖它但保留格式一致：start=1 + fragment_lengths 长度 = len(ALL_CRATES)
    fl = [len(c) for c in cr]
    content = 'window.ALL_CRATES = ["' + '","'.join(cr) + '"];\n'
    content += '//{"start":1,"fragment_lengths":[' + ','.join(str(x) for x in fl) + ']}\n'
    dst = os.path.join(DST, 'crates.js')
    if os.path.exists(dst):
        with open(dst, 'r', encoding='utf-8') as f:
            if f.read() == content:
                print(f'  crates.js: unchanged, skipping write')
                return False
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(content)
    return True


def main():
    print(f'Source: {SRC}')
    print(f'Destination: {os.path.abspath(DST)}')
    print()

    # 1. search.index/
    print('[1/3] Copying search.index/...')
    if copy_dir_tree('search.index', 'search.index'):
        # 统计文件数
        n = 0
        for _, _, fs in os.walk(os.path.join(DST, 'search.index')):
            n += len(fs)
        print(f'  OK: copied, {n} shard files')

    # 2. src/
    print('[2/3] Copying src/...')
    if copy_dir_tree('src', 'src'):
        n = 0
        for _, _, fs in os.walk(os.path.join(DST, 'src')):
            n += len(fs)
        print(f'  OK: copied, {n} source HTML files')

    # 3. help.html
    print('[3/3] Copying help.html + writing crates.js...')
    if copy_file('help.html'):
        print('  OK: help.html copied')
    if write_crates_js():
        print(f'  OK: crates.js written ({len(OUR_CRATES)} crates)')

    print('\nDone. Run: python -m http.server 8080')
    print('Then open http://localhost:8080/quinn/index.html')


if __name__ == '__main__':
    main()