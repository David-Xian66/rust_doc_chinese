#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Translate remaining untranslated docblocks in tokio/process/.

Files in scope:
- process/struct.Command.html (15 untranslated <p>: 14 'Basic usage:' + 1 'usage would be:')
- process/index.html (4 untranslated <p> in Dropping/Cancellation section + chrome headers)

CRLF line endings: rustdoc on Windows uses \r\n.
NOTE: Use bytes literals (b'...') to avoid double-encoding of non-ASCII chars.
"""
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))


def E(s):
    """Encode string to bytes, but use bytes literals when pattern has non-ASCII.

    For non-ASCII chars, prefer using raw bytes literals (b'...') directly.
    This E() helper is for ASCII-only patterns.
    """
    return s.encode('utf-8')


PAIRS = {}

# === process/struct.Command.html ===
# 14 instances of <p>Basic usage:</p> + 1 instance of <p>usage would be:</p>
# These are short chrome-style example headings.
PAIRS['process/struct.Command.html'] = [
    (b'<p>Basic usage:</p>',
     b'<p>\xe5\x9f\xba\xe6\x9c\xac\xe7\x94\xa8\xe6\xb3\x95\xef\xbc\x9a</p>'),
    (b'<p>usage would be:</p>',
     b'<p>\xe7\x94\xa8\xe6\xb3\x95\xe7\xa4\xba\xe4\xbe\x8b\xef\xbc\x9a</p>'),
]


# === process/index.html ===
# Dropping/Cancellation section has 4 untranslated <p> + 3 section headers.
PAIRS['process/index.html'] = [
    # Section header: Caveats (h2 with anchor)
    # § in UTF-8 is c2 a7
    (b'<h2 id="caveats"><a class="doc-anchor" href="#caveats">\xc2\xa7</a>Caveats</h2>',
     b'<h2 id="caveats"><a class="doc-anchor" href="#caveats">\xc2\xa7</a>\xe6\xb3\xa8\xe6\x84\x8f\xe4\xba\x8b\xe9\xa1\xb9</h2>'),
    # Section header: Dropping/Cancellation (it's h3, not h2)
    (b'<h3 id="droppingcancellation"><a class="doc-anchor" href="#droppingcancellation">\xc2\xa7</a>Dropping/Cancellation</h3>',
     b'<h3 id="droppingcancellation"><a class="doc-anchor" href="#droppingcancellation">\xc2\xa7</a>\xe6\x96\xad\xe5\xbc\x80/\xe5\x8f\x96\xe6\xb6\x88</h3>'),
    # Section header: Unix Processes (h3, not h2)
    (b'<h3 id="unix-processes"><a class="doc-anchor" href="#unix-processes">\xc2\xa7</a>Unix Processes</h3>',
     b'<h3 id="unix-processes"><a class="doc-anchor" href="#unix-processes">\xc2\xa7</a>Unix \xe8\xbf\x9b\xe7\xa8\x8b</h3>'),

    # <p> in Dropping/Cancellation section
    (b'<p>Similar to the behavior to the standard library, and unlike the futures\r\nparadigm of dropping-implies-cancellation, a spawned process will, by\r\ndefault, continue to execute even after the <code>Child</code> handle has been dropped.</p>',
     b'<p>\xe4\xb8\x8e\xe6\xa0\x87\xe5\x87\x86\xe5\xba\x93\xe7\x9a\x84\xe8\xa1\x8c\xe4\xb8\xba\xe7\xb1\xbb\xe4\xbc\xbc\xef\xbc\x8c\xe4\xb8\x8d\xe5\x90\x8c\xe4\xba\x8e futures \xe8\x8c\x83\xe5\xbc\x8f\xe7\x9a\x84\xe2\x80\x9cdrop \xe5\x8d\xb3\xe5\x8f\x96\xe6\xb6\x88\xe2\x80\x9d\xef\xbc\x8c\r\n\xe9\xbb\x98\xe8\xae\xa4\xe6\x83\x85\xe5\x86\xb5\xe4\xb8\x8b\xef\xbc\x8c\xe6\xb4\xbe\xe7\x94\x9f\xe5\x87\xba\xe7\x9a\x84\xe8\xbf\x9b\xe7\xa8\x8b\xe5\x8d\xb3\xe4\xbd\xbf\xe5\x9c\xa8 <code>Child</code> \xe5\x8f\xa5\xe6\x9f\x84\xe8\xa2\xab drop \xe4\xb9\x8b\xe5\x90\x8e\r\n\xe4\xbb\x8d\xe4\xbc\x9a\xe7\xbb\xa7\xe7\xbb\xad\xe6\x89\xa7\xe8\xa1\x8c\xe3\x80\x82</p>'),
    (b'<p>The <a href="struct.Command.html#method.kill_on_drop" title="method tokio::process::Command::kill_on_drop"><code>Command::kill_on_drop</code></a> method can be used to modify this behavior\r\nand kill the child process if the <code>Child</code> wrapper is dropped before it\r\nhas exited.</p>',
     b'<p><a href="struct.Command.html#method.kill_on_drop" title="method tokio::process::Command::kill_on_drop"><code>Command::kill_on_drop</code></a> \xe6\x96\xb9\xe6\xb3\x95\xe5\x8f\xaf\xe7\x94\xa8\xe4\xba\x8e\xe4\xbf\xae\xe6\x94\xb9\xe6\xad\xa4\xe8\xa1\x8c\xe4\xb8\xba\xef\xbc\x8c\r\n\xe5\xbd\x93 <code>Child</code> \xe5\x8c\x85\xe8\xa3\x85\xe5\x99\xa8\xe5\x9c\xa8\xe5\xad\x90\xe8\xbf\x9b\xe7\xa8\x8b\xe9\x80\x80\xe5\x87\xba\xe5\x89\x8d\xe8\xa2\xab drop \xe6\x97\xb6\xe7\xbb\x88\xe6\xad\xa2\xe5\xad\x90\xe8\xbf\x9b\xe7\xa8\x8b\xe3\x80\x82</p>'),
    # On Unix platforms processes must be "reaped" by their parent...
    (b'<p>On Unix platforms processes must be \xe2\x80\x9creaped\xe2\x80\x9d by their parent process after\r\nthey have exited in order to release all OS resources. A child process which\r\nhas exited, but has not yet been reaped by its parent is considered a \xe2\x80\x9czombie\xe2\x80\x9d\r\nprocess. Such processes continue to count against limits imposed by the system,\r\nand having too many zombie processes present can prevent additional processes\r\nfrom being spawned.</p>',
     b'<p>\xe5\x9c\xa8 Unix \xe5\xb9\xb3\xe5\x8f\xb0\xe4\xb8\x8a\xef\xbc\x8c\xe8\xbf\x9b\xe7\xa8\x8b\xe5\x9c\xa8\xe9\x80\x80\xe5\x87\xba\xe4\xb9\x8b\xe5\x90\x8e\xe5\xbf\x85\xe9\xa1\xbb\xe8\xa2\xab\xe7\x88\xb6\xe8\xbf\x9b\xe7\xa8\x8b\xe2\x80\x9c\xe6\x94\xb6\xe8\x97\x8f\xe2\x80\x9d\xef\xbc\x88reap\xef\xbc\x89\xe4\xbb\xa5\xe9\x87\x8a\xe6\x94\xbe\xe6\x89\x80\xe6\x9c\x89\xe7\x9a\x84\r\nOS \xe8\xb5\x84\xe6\xba\x90\xe3\x80\x82\xe5\xb7\xb2\xe9\x80\x80\xe5\x87\xba\xe4\xbd\x86\xe8\xbf\x98\xe6\x9c\xaa\xe8\xa2\xab\xe7\x88\xb6\xe8\xbf\x9b\xe7\xa8\x8b\xe6\x94\xb6\xe8\x97\x8f\xe7\x9a\x84\xe5\xad\x90\xe8\xbf\x9b\xe7\xa8\x8b\xe8\xa2\xab\xe7\xa7\xb0\xe4\xb8\xba\xe2\x80\x9c\xe5\x83\xb5\xe5\xb0\xb8\xe2\x80\x9d\xe8\xbf\x9b\xe7\xa8\x8b\xe3\x80\x82\r\n\xe8\xbf\x99\xe7\xa7\x8d\xe8\xbf\x9b\xe7\xa8\x8b\xe4\xbc\x9a\xe7\xbb\xa7\xe7\xbb\xad\xe5\x8d\xa0\xe7\x94\xa8\xe7\xb3\xbb\xe7\xbb\x9f\xe5\xae\x9e\xe6\x96\xbd\xe7\x9a\x84\xe8\xb5\x84\xe6\xba\x90\xe9\x99\x90\xe5\x88\xb6\xef\xbc\x8c\r\n\xe5\x83\xb5\xe5\xb0\xb8\xe8\xbf\x9b\xe7\xa8\x8b\xe8\xbf\x87\xe5\xa4\x9a\xe4\xbc\x9a\xe9\x98\xbb\xe7\xa6\x81\xe5\x8f\xa6\xe5\xa4\x96\xe6\xb4\xbe\xe7\x94\x9f\xe6\x96\xb0\xe8\xbf\x9b\xe7\xa8\x8b\xe3\x80\x82</p>'),
    (b'<p>The tokio runtime will, on a best-effort basis, attempt to reap and clean up\r\nany process which it has spawned. No additional guarantees are made with regard to\r\nhow quickly or how often this procedure will take place.</p>',
     b'<p>tokio \xe8\xbf\x90\xe8\xa1\x8c\xe6\x97\xb6\xe5\xb0\x86\xe5\xb0\xbd\xe5\x8a\x9b\xe5\xb0\x9d\xe8\xaf\x95\xe5\x9b\x9e\xe6\x94\xb6\xe5\xb9\xb6\xe6\xb8\x85\xe7\x90\x86\xe5\xae\x83\xe6\xb4\xbe\xe7\x94\x9f\xe7\x9a\x84\xe4\xbb\xbb\xe4\xbd\x95\xe8\xbf\x9b\xe7\xa8\x8b\xe3\x80\x82\r\n\xe4\xbd\x86\xe5\xb0\x9d\xe8\xaf\x95\xe7\x9a\x84\xe9\xa2\x91\xe7\x8e\x87\xe5\x92\x8c\xe9\x80\x9f\xe5\xba\xa6\xe4\xb8\x8d\xe6\x8f\x90\xe4\xbe\x9b\xe4\xbb\xbb\xe4\xbd\x95\xe9\xa2\x9d\xe5\xa4\x96\xe4\xbf\x9d\xe8\xaf\x81\xe3\x80\x82</p>'),

    # <dd> blocks - module item descriptions
    (b'<dd>Representation of a child process spawned onto an event loop.</dd>',
     b'<dd>\xe4\xbb\xa3\xe8\xa1\xa8\xe5\x9c\xa8\xe4\xba\x8b\xe4\xbb\xb6\xe5\xbe\xaa\xe7\x8e\xaf\xe4\xb8\x8a\xe6\xb4\xbe\xe7\x94\x9f\xe7\x9a\x84\xe5\xad\x90\xe8\xbf\x9b\xe7\xa8\x8b\xe3\x80\x82</dd>'),
    (b'<dd>The standard error stream for spawned children.</dd>',
     b'<dd>\xe6\xb4\xbe\xe7\x94\x9f\xe5\xad\x90\xe8\xbf\x9b\xe7\xa8\x8b\xe7\x9a\x84\xe6\xa0\x87\xe5\x87\x86\xe9\x94\x99\xe8\xaf\xaf\xe6\xb5\x81\xe3\x80\x82</dd>'),
    (b'<dd>The standard input stream for spawned children.</dd>',
     b'<dd>\xe6\xb4\xbe\xe7\x94\x9f\xe5\xad\x90\xe8\xbf\x9b\xe7\xa8\x8b\xe7\x9a\x84\xe6\xa0\x87\xe5\x87\x86\xe8\xbe\x93\xe5\x85\xa5\xe6\xb5\x81\xe3\x80\x82</dd>'),
    (b'<dd>The standard output stream for spawned children.</dd>',
     b'<dd>\xe6\xb4\xbe\xe7\x94\x9f\xe5\xad\x90\xe8\xbf\x9b\xe7\xa8\x8b\xe7\x9a\x84\xe6\xa0\x87\xe5\x87\x86\xe8\xbe\x93\xe5\x87\xba\xe6\xb5\x81\xe3\x80\x82</dd>'),
    # Command with link to std
    (b'<dd>This structure mimics the API of <a href="https://doc.rust-lang.org/1.95.0/std/process/struct.Command.html" title="struct std::process::Command"><code>std::process::Command</code></a> found in the standard library, but\r\nreplaces functions that create a process with an asynchronous variant. The main provided\r\nasynchronous functions are <a href="struct.Command.html#method.spawn" title="method tokio::process::Command::spawn">spawn</a>, <a href="struct.Command.html#method.status" title="method tokio::process::Command::status">status</a>, and\r\n<a href="struct.Command.html#method.output" title="method tokio::process::Command::output">output</a>.</dd>',
     b'<dd>\xe6\xad\xa4\xe7\xbb\x93\xe6\x9e\x84\xe4\xbd\x93\xe6\xa8\xa1\xe4\xbb\xbf\xe4\xba\x86\xe6\xa0\x87\xe5\x87\x86\xe5\xba\x93\xe4\xb8\xad <a href="https://doc.rust-lang.org/1.95.0/std/process/struct.Command.html" title="struct std::process::Command"><code>std::process::Command</code></a> \xe7\x9a\x84 API\xef\xbc\x8c\r\n\xe4\xbd\x86\xe5\xb0\x86\xe5\x88\x9b\xe5\xbb\xba\xe8\xbf\x9b\xe7\xa8\x8b\xe7\x9a\x84\xe5\x87\xbd\xe6\x95\xb0\xe6\x9b\xbf\xe6\x8d\xa2\xe4\xb8\xba\xe5\xbc\x82\xe6\xad\xa5\xe7\x89\x88\xe6\x9c\xac\xe3\x80\x82\xe4\xb8\xbb\xe8\xa6\x81\xe6\x8f\x90\xe4\xbe\x9b\xe7\x9a\x84\r\n\xe5\xbc\x82\xe6\xad\xa5\xe5\x87\xbd\xe6\x95\xb0\xe6\x98\xaf <a href="struct.Command.html#method.spawn" title="method tokio::process::Command::spawn">spawn</a>\xe3\x80\x81<a href="struct.Command.html#method.status" title="method tokio::process::Command::status">status</a> \xe5\x92\x8c\r\n<a href="struct.Command.html#method.output" title="method tokio::process::Command::output">output</a>\xe3\x80\x82</dd>'),
]


def main():
    apply = '--apply' in sys.argv
    total = 0
    for rel, pairs in PAIRS.items():
        path = os.path.join(ROOT, rel)
        with open(path, 'rb') as f:
            content = f.read()
        original = content
        count = 0
        for en, zh in pairs:
            if en in content:
                n = content.count(en)
                content = content.replace(en, zh)
                count += n
            else:
                print(f'  [WARN] no match in {rel}: {en[:80]!r}')
        if content != original:
            if apply:
                with open(path, 'wb') as f:
                    f.write(content)
            print(f'{rel}: {count} replacements {"APPLIED" if apply else "(dry-run)"}')
            total += count
        else:
            print(f'{rel}: 0 replacements (no match)')
    print(f'\nTOTAL: {total} replacements')


if __name__ == '__main__':
    main()