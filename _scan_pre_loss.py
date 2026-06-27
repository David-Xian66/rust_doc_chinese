"""扫描所有 crate 中 <pre class="rust rust-example-rendered"> 数量下降的文件。"""
import os
import re


def main():
    crates = [('quinn', 'quinn_old'), ('tokio', 'tokio_old'), ('rcgen', 'rcgen_old'),
              ('coarsetime', 'coarsetime_old'), ('bytes', 'bytes_old'),
              ('rustls_pki_types', 'rustls_pki_types_old')]
    issues_per_crate = {}
    for cur_root, old_root in crates:
        issues = []
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
                old_pre = len(re.findall(r'<pre[^>]*class="rust rust-example-rendered"', old))
                cur_pre = len(re.findall(r'<pre[^>]*class="rust rust-example-rendered"', cur))
                if old_pre > 5 and cur_pre < old_pre * 0.5:
                    issues.append((rel, old_pre, cur_pre))
        issues_per_crate[cur_root] = issues
        if issues:
            print(f'{cur_root}: {len(issues)} files with significant pre loss')
            for rel, o, c in issues[:20]:
                print(f'  {rel}: {o}->{c}')
        else:
            print(f'{cur_root}: clean')


if __name__ == '__main__':
    main()