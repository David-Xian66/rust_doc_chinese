"""为缺失的 trait.impl JS 路径生成空实现者的 stub。

策略：扫描所有 HTML，解析 trait.impl 引用，对于源 demo_sc/target/doc/trait.impl/
里没有的路径（因为对应 crate 没在 demo_sc 里构建），生成空 stub。

调用方式：
    python _common_tools/_gen_trait_impl_stubs.py
    # 或从 copy_doc_artifacts.py 里导入 generate()
"""
import os
import re
from collections import defaultdict


def generate():
    """主函数：扫描 + 生成 stub。返回生成的 stub 数量。"""
    cwd = os.getcwd()
    missing = defaultdict(set)
    for root, dirs, files in os.walk(cwd):
        if 'trait.impl' in root or '.git' in root or 'search.index' in root or 'static.files' in root:
            continue
        for f in files:
            if not f.endswith('.html'):
                continue
            path = os.path.join(root, f)
            try:
                with open(path, 'rb') as fh:
                    c = fh.read().decode('utf-8', errors='replace')
            except Exception:
                continue
            html_dir = os.path.dirname(os.path.abspath(path))
            rel = os.path.relpath(path, cwd).replace('\\', '/')
            parts = rel.split('/')
            src_crate = parts[0] if parts else 'unknown'
            if src_crate.endswith('_old'):
                continue
            for m in re.findall(r'(?:src|href)="((?:[^"/]+/)*trait\.impl/[^"]+\.js)"', c):
                target = os.path.normpath(os.path.join(html_dir, m))
                if not os.path.exists(target):
                    missing[target].add(src_crate)

    if not missing:
        print('  No missing trait.impl references')
        return 0

    generated = 0
    for target_path, src_crates in sorted(missing.items()):
        rel = os.path.relpath(target_path, cwd).replace('\\', '/')
        if not rel.startswith('trait.impl/'):
            continue
        parts = rel.split('/')
        if len(parts) < 3:
            continue

        src_list = sorted(src_crates)
        if len(src_list) == 1:
            key_entries = f'["{src_list[0]}",[]]'
        else:
            key_entries = ','.join(f'["{c}",[]]' for c in src_list)

        stub = (
            '(function() {\n'
            f'    const implementors = Object.fromEntries([{key_entries}]);\n'
            '    if (window.register_implementors) {\n'
            '        window.register_implementors(implementors);\n'
            '    } else {\n'
            '        window.pending_implementors = implementors;\n'
            '    }\n'
            '})()\n'
        )

        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with open(target_path, 'w', encoding='utf-8') as fh:
            fh.write(stub)
        generated += 1
        print(f'  + {rel}  (sources: {src_list})')

    return generated


if __name__ == '__main__':
    n = generate()
    print(f'\nGenerated {n} stub files')