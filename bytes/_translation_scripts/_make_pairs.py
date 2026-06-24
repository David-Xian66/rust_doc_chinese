"""Generate (old, new) pairs from translation table + untranslated data.

Approach:
- For each untranslated <p>, the stripped text maps to a Chinese translation
- We need to keep the original HTML wrapping (e.g. <code>...</code>, <a>...</a>)
- Build pairs: full_p -> full_p_with_chinese_text
"""
import json
import re
import os


def normalize_p_text(text):
    """Normalize text for matching: collapse multiple whitespace, normalize line endings."""
    return re.sub(r'\s+', ' ', text.strip())


def html_aware_translate(p_html, translation):
    """Take HTML <p>...</p> and a Chinese translation.
    The translation may already include <code>...</code> wrappers.
    We just rebuild <p>{translation}</p>.
    """
    # Extract inner content
    inner_match = re.match(r'<p[^>]*>(.*?)</p>', p_html, re.DOTALL)
    if not inner_match:
        return p_html
    # If translation is plain (no HTML tags), wrap as <p>{translation}</p>
    # If translation has <code> tags, wrap as <p>{translation}</p>
    return '<p>' + translation + '</p>'


def main():
    with open('bytes/_buf_translations.json', 'r', encoding='utf-8') as f:
        translations = json.load(f)
    with open('bytes/_untranslated_own_p.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    pairs = []
    seen = set()
    matched = 0
    unmatched = []

    for path, entries in data.items():
        for entry in entries:
            full_p = entry['full_p']
            stripped = entry['text'].strip()
            # Strip additional whitespace variations for lookup
            stripped_norm = normalize_p_text(stripped)

            # Try direct match first
            trans = None
            for key, val in translations.items():
                if normalize_p_text(key) == stripped_norm:
                    trans = val
                    break

            if trans is None:
                unmatched.append((path, entry['id'], stripped[:120]))
                continue

            if full_p in seen:
                continue
            seen.add(full_p)
            new_p = html_aware_translate(full_p, trans)
            pairs.append([full_p, new_p])
            matched += 1

    print(f'Matched: {matched}')
    print(f'Unmatched: {len(unmatched)}')

    # Save
    with open('bytes/_pairs_v2.json', 'w', encoding='utf-8') as f:
        json.dump(pairs, f, ensure_ascii=False, indent=2)
    print(f'Saved {len(pairs)} pairs to bytes/_pairs_v2.json')

    # Show unmatched
    if unmatched:
        print(f'\nFirst 30 unmatched:')
        for path, id_, t in unmatched[:30]:
            print(f'  [{path}] [{id_}]: {t}')


if __name__ == '__main__':
    main()