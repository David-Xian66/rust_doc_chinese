"""Fix backslashes in href/src attributes."""
import os
import re

fixed = 0
total_changes = 0
for root, _, fs in os.walk('bytes'):
    for f in fs:
        if not f.endswith('.html'):
            continue
        p = os.path.join(root, f)
        with open(p, 'r', encoding='utf-8') as fh:
            c = fh.read()

        # Replace backslashes in href="..." and src="..." attributes only
        def replace_in_attr(m):
            attr_name = m.group(1)
            value = m.group(2)
            if '\\' in value:
                new_value = value.replace('\\', '/')
                return f'{attr_name}="{new_value}"'
            return m.group(0)

        new_c = re.sub(r'(href|src)="([^"]*)"', replace_in_attr, c)
        if new_c != c:
            # Count changes
            changes = sum(1 for m in re.finditer(r'href="[^"]*\\\\[^"]*"|src="[^"]*\\\\[^"]*"', c))
            total_changes += changes
            with open(p, 'w', encoding='utf-8') as fh:
                fh.write(new_c)
            fixed += 1

print(f'Fixed: {fixed} files, {total_changes} attribute changes')