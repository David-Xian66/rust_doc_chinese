#!/usr/bin/env python3
"""Restore <code> tags lost during v2 translation.

For each translated <p> in sync files, find the equivalent <p> in the OLD file
and re-insert <code> tags around matching tokens.
"""
import re
import os

TOKIO_DIR = r"D:/Administrator/Documents/Code/rust_doc_all/tokio"
SYNC_DIR = os.path.join(TOKIO_DIR, 'sync')
OLD_DIR = os.path.join(TOKIO_DIR.rstrip('/').replace('D:/', 'D:/').replace('/Code', '/Code'), 'tokio_old', 'sync')
# Use the explicit path
OLD_DIR = r"D:/Administrator/Documents/Code/rust_doc_all/tokio_old/sync"


def find_docblocks(text):
    """Find docblocks with depth tracking."""
    blocks = []
    pos = 0
    while True:
        m = re.search(r"<div class=['\"]docblock['\"]>", text[pos:])
        if not m:
            break
        start = pos + m.start()
        depth = 1
        i = pos + m.end()
        while i < len(text) and depth > 0:
            next_open = text.find("<div", i)
            next_close = text.find("</div>", i)
            if next_close == -1:
                return blocks
            if next_open != -1 and next_open < next_close:
                depth += 1
                i = next_open + 4
            else:
                depth -= 1
                i = next_close + 6
        end = i - 6
        blocks.append((start, end, text[start:end]))
        pos = end
    return blocks


def extract_inline_codes(html):
    """Get set of words/identifiers wrapped in <code> tags from a docblock."""
    codes = set()
    for m in re.finditer(r'<code>([^<]+)</code>', html):
        codes.add(m.group(1))
    return codes


def strip_p(text):
    """Strip <p> tags and HTML, get plain text for matching."""
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def restore_code_in_p(p_html, inline_codes):
    """Re-insert <code> tags around identifiers that match the original.

    Sort codes by length (longest first) to avoid partial matches.
    Only wrap if the exact text appears as a word boundary.
    """
    if not inline_codes:
        return p_html

    # We need to walk through the p text and re-insert <code>
    # First, extract the content between <p ...> and </p>
    m = re.match(r'(<p(?:\s[^>]*)?>)(.*?)(</p>)$', p_html, re.DOTALL)
    if not m:
        return p_html
    p_open, p_inner, p_close = m.group(1), m.group(2), m.group(3)

    # Process p_inner character by character to find text nodes and re-insert <code>
    # We work on a tokenized version
    # Strategy: split p_inner into segments of (text, tag, text, tag, ...)
    # For each text segment, find code identifiers and wrap them

    # Tokenize: keep tags as separate tokens
    tokens = re.split(r'(<[^>]+>)', p_inner)
    out = []
    for tok in tokens:
        if not tok:
            continue
        if tok.startswith('<'):
            out.append(tok)
        else:
            # text node - find code identifiers
            out.append(wrap_codes_in_text(tok, inline_codes))
    return p_open + ''.join(out) + p_close


def wrap_codes_in_text(text, inline_codes):
    """Wrap each occurrence of any code identifier in <code> tags.

    Sort codes by length (longest first) to avoid partial matches.
    Use word boundaries to avoid mid-word matches.
    """
    if not text or not inline_codes:
        return text
    # Sort by length desc
    sorted_codes = sorted(inline_codes, key=len, reverse=True)
    # Track what's been wrapped to avoid double-wrapping
    result = text
    for code in sorted_codes:
        # Escape regex special chars
        esc = re.escape(code)
        # Use word boundaries; only match if not already inside <code>
        # Use negative lookbehind/ahead for >
        pattern = rf'(?<![<])(?<![A-Za-z0-9_]){esc}(?![A-Za-z0-9_])(?![^<>]*</code>)'
        result = re.sub(pattern, f'<code>{code}</code>', result)
    return result


def main():
    total_fixed = 0
    files_fixed = 0
    for f in sorted(os.listdir(SYNC_DIR)):
        if not f.endswith('.html'):
            continue
        new_full = os.path.join(SYNC_DIR, f)
        old_full = os.path.join(OLD_DIR, f)
        if not os.path.exists(old_full):
            continue

        with open(new_full, 'r', encoding='utf-8') as fp:
            new_content = fp.read()
        with open(old_full, 'r', encoding='utf-8') as fp:
            old_content = fp.read()

        # Find all docblocks in OLD, extract inline codes
        old_docblocks = find_docblocks(old_content)
        old_db_codes = []
        for start, end, db in old_docblocks:
            codes = extract_inline_codes(db)
            old_db_codes.append(codes)

        # For each docblock in NEW, restore code tags based on old codes
        new_docblocks = find_docblocks(new_content)
        # Build new content by walking docblocks
        new_out = []
        last_pos = 0
        file_modified = False
        for (start, end, db), codes in zip(new_docblocks, old_db_codes):
            new_out.append(new_content[last_pos:start])
            # In new docblock, find all <p> and re-insert <code> tags
            new_db = db
            # Find all <p>...</p> within this docblock
            p_iter = list(re.finditer(r'<p(?:\s[^>]*)?>.*?</p>', new_db, re.DOTALL))
            if p_iter and codes:
                # Build replacement
                new_db_parts = []
                last_p_end = 0
                for p_match in p_iter:
                    new_db_parts.append(new_db[last_p_end:p_match.start()])
                    fixed_p = restore_code_in_p(p_match.group(0), codes)
                    if fixed_p != p_match.group(0):
                        file_modified = True
                    new_db_parts.append(fixed_p)
                    last_p_end = p_match.end()
                new_db_parts.append(new_db[last_p_end:])
                new_db = ''.join(new_db_parts)
            new_out.append(new_db)
            last_pos = end
        new_out.append(new_content[last_pos:])

        new_content_new = ''.join(new_out)

        if file_modified:
            # Preserve line endings
            with open(new_full, 'rb') as fp:
                raw_orig = fp.read()
            if b'\r\n' in raw_orig:
                new_content_new = new_content_new.replace('\n', '\r\n')
            with open(new_full, 'wb') as fp:
                fp.write(new_content_new.encode('utf-8'))
            files_fixed += 1
            # Count <code> tags recovered
            old_count = len(re.findall(r'<code>', new_content))
            new_count = len(re.findall(r'<code>', new_content_new))
            total_fixed += new_count - old_count
            print(f"  Fixed: {f} (+{new_count - old_count} <code> tags)")

    print(f"\nTotal: +{total_fixed} <code> tags in {files_fixed} files")


if __name__ == '__main__':
    main()
