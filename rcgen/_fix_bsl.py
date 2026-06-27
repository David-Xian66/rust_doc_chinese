"""修复 DistinguishedNameIterator.html 的 Windows 反斜杠."""
import re

fp = 'rcgen/struct.DistinguishedNameIterator.html'
with open(fp, 'r', encoding='utf-8') as f:
    c = f.read()

# 仅修 href 和 src 属性里的反斜杠，避免动 script 块
def fix_attr(m):
    attr = m.group(1)
    val = m.group(2)
    if '\\' in val:
        val = val.replace('\\', '/')
        return f'{attr}="{val}"'
    return m.group(0)

# 匹配 href="..." 或 src="..." (贪婪匹配属性值, 但只在标签内部)
c2 = re.sub(r'(href|src)="([^"]*?)"', fix_attr, c)
if c2 != c:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(c2)
    print(f'fixed {fp}')
else:
    print('no change')
