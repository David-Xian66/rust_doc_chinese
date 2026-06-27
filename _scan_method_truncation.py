"""扫描所有 crate 中每个 method 的 docblock 大小，看是否有方法被截断。

策略：对每个 section id="method.X"，提取其后的 docblock 可见文本。
如果某个 method 的 docblock 文本长度 < 5，可能是截断为只剩 1 句简介。
"""
import os
import re


def main():
    crates = [('quinn', 'quinn_old'), ('tokio', 'tokio_old'), ('rcgen', 'rcgen_old'),
              ('coarsetime', 'coarsetime_old'), ('bytes', 'bytes_old'),
              ('rustls_pki_types', 'rustls_pki_types_old')]
    for cur_root, old_root in crates:
        truncation_candidates = []
        for dirpath, dirs, files in os.walk(cur_root):
            dirs[:] = [d for d in dirs if d != 'static.files']
            for f in files:
                if not f.endswith('.html'):
                    continue
                cur_path = os.path.join(dirpath, f)
                rel = os.path.relpath(cur_path, cur_root).replace('\\', '/')
                old_path = os.path.join(old_root, rel)
                if not os.path.exists(old_path):
                    continue
                with open(old_path, 'rb') as fh:
                    old = fh.read().decode('utf-8', errors='replace')
                with open(cur_path, 'rb') as fh:
                    cur = fh.read().decode('utf-8', errors='replace')
                # Per-method analysis: for each method.X section, compare docblock size
                old_methods = {}
                for m in re.finditer(r'<section[^>]*id="(method\.[^"]+)"[\s\S]*?(?=<section[^>]*id=|<h2)', old):
                    method = m.group(1)
                    start = m.end()
                    end_m = re.search(r'<section[^>]*id=|<h2', old[start:start + 10000])
                    block = old[start:start + (end_m.start() if end_m else 10000)]
                    db_m = re.search(r'<div class="docblock"[^>]*>([\s\S]*?)</div>', block)
                    if db_m:
                        text = re.sub(r'<[^>]+>', ' ', db_m.group(1))
                        text = re.sub(r'\s+', ' ', text).strip()
                        old_methods[method] = text
                cur_methods = {}
                for m in re.finditer(r'<section[^>]*id="(method\.[^"]+)"[\s\S]*?(?=<section[^>]*id=|<h2)', cur):
                    method = m.group(1)
                    start = m.end()
                    end_m = re.search(r'<section[^>]*id=|<h2', cur[start:start + 10000])
                    block = cur[start:start + (end_m.start() if end_m else 10000)]
                    db_m = re.search(r'<div class="docblock"[^>]*>([\s\S]*?)</div>', block)
                    if db_m:
                        text = re.sub(r'<[^>]+>', ' ', db_m.group(1))
                        text = re.sub(r'\s+', ' ', text).strip()
                        cur_methods[method] = text
                # Compare: find methods where cur is significantly shorter
                for m, old_text in old_methods.items():
                    if m not in cur_methods:
                        continue
                    cur_text = cur_methods[m]
                    if len(old_text) > 30 and len(cur_text) < 5:
                        truncation_candidates.append((rel, m, old_text, cur_text))
        if truncation_candidates:
            print(f'\n{cur_root}: {len(truncation_candidates)} truncated methods')
            for rel, m, o, c in truncation_candidates[:20]:
                print(f'  {rel} {m}')
                print(f'    OLD: {o[:80]}')
                print(f'    CUR: {c[:80]}')
        else:
            print(f'{cur_root}: no truncated methods')


if __name__ == '__main__':
    main()