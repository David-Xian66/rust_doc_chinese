"""Apply the translated <dd> descriptions back into ffmpeg_sys_next/index.html.

Workflow:
- Read all 9 batch JSON files (D:/ffmpeg_batch_00.json .. D:/ffmpeg_batch_08.json)
- Build a dict mapping raw -> translation
- Read ffmpeg_sys_next/index.html
- For each <dd>...</dd>, replace inner content with the translation (keeping the <dd> tag)
- Write back
"""

import os
import re
import json

HTML_PATH = r'D:/Administrator/Documents/Code/rust_doc_all/ffmpeg_sys_next/index.html'


def load_translations():
    """Build {raw_text: chinese_translation} dict from all batch files."""
    translations = {}
    for i in range(9):
        path = f'D:/ffmpeg_batch_{i:02d}.json'
        if not os.path.exists(path):
            print(f'  [WARN] {path} missing')
            continue
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for item in data:
            if 'translation' in item and item['translation']:
                translations[item['raw']] = item['translation']
                # Also try key variations for matching
                # (raw may have different whitespace)
                translations[item['raw'].strip()] = item['translation']
    return translations


def apply_translations(html, translations):
    """For each <dd>...</dd> in html, replace its content with the translation."""
    counter = {'total': 0, 'translated': 0, 'untranslated': 0}

    def repl(m):
        counter['total'] += 1
        inner = m.group(1)
        # inner is the raw content of <dd>
        # check both exact match and stripped match
        if inner in translations:
            counter['translated'] += 1
            return f'<dd>{translations[inner]}</dd>'
        # try stripped
        stripped = inner.strip()
        if stripped in translations:
            counter['translated'] += 1
            return f'<dd>{translations[stripped]}</dd>'
        # try without leading/trailing whitespace
        # The key in translations was created with key = d.strip()
        # d is from re.findall so it's exactly the inner content (no leading/trailing ws from regex)
        # but might have \n etc. so try normalized
        normalized = re.sub(r'\s+', ' ', stripped)
        if normalized in translations:
            counter['translated'] += 1
            return f'<dd>{translations[normalized]}</dd>'
        counter['untranslated'] += 1
        return m.group(0)  # leave as-is

    new_html = re.sub(r'<dd[^>]*>(.*?)</dd>', repl, html, flags=re.DOTALL)
    return new_html, counter


def main():
    print('Loading translations...')
    translations = load_translations()
    print(f'  Loaded {len(translations)} translations')

    print(f'\nReading {HTML_PATH}...')
    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        html = f.read()
    print(f'  Size: {len(html)} bytes')

    print('\nApplying translations...')
    new_html, counter = apply_translations(html, translations)
    print(f'  Total <dd> blocks: {counter["total"]}')
    print(f'  Translated: {counter["translated"]}')
    print(f'  Untranslated (no match): {counter["untranslated"]}')

    print(f'\nWriting back to {HTML_PATH}...')
    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(new_html)

    # Verify
    cjk = len(re.findall(r'[一-鿿]', new_html))
    print(f'\nVerification:')
    print(f'  CJK characters: {cjk}')
    # Check no line artifacts
    line_artifacts = re.findall(r'^\d+\t', new_html, flags=re.MULTILINE)
    print(f'  Line artifacts: {len(line_artifacts)}')


if __name__ == '__main__':
    main()
