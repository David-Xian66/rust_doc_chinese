#!/usr/bin/env python3
"""
Inject two navigation aids into every translated HTML file:

1. A sidebar toggle button (collapsible left sidebar)
   - Placed as the FIRST child of <rustdoc-topbar>
   - Uses class "sidebar-menu-toggle" so rustdoc's main.js auto-binds the mobile toggle
   - Adds desktop behavior via injected JS:
       * click to toggle
       * localStorage persistence (key: rustdoc-cn-sidebar-hidden)
       * keyboard shortcuts: `\\` or `[` to toggle, Esc to close
       * when hidden, hovering the left edge (8px) peeks the sidebar (VS Code style)
       * when hidden, a small floating "show sidebar" handle appears at the left edge
       * toggle button title/aria-label updates dynamically

2. A "back to home" button linking to the site root (/index.html)
   - Placed inside <div class="search-menu"> so it sits alongside the search button
   - Uses absolute path "/index.html" so it works regardless of file depth

Idempotent: skipped if marker `rustdoc-cn-sidebar-handle` is already present.

Pattern follows _common_tools/inject_github_link.py.
"""
import os
import re
import sys

# === Markers (NEW injection) ===
NEW_HANDLE_MARKER = b'<button class="rustdoc-cn-sidebar-handle"'
TOPBAR_OPEN = b'<rustdoc-topbar>'
TOPBAR_CLOSE = b'</rustdoc-topbar>'
SEARCH_MENU_OPEN = b'<div class="search-menu">'

# === Markers (OLD injection — to detect and roll back) ===
OLD_TOGGLE_RE = re.compile(
    rb'<button class="sidebar-menu-toggle"[^>]*></button>'
)
OLD_HOME_RE = re.compile(
    rb'<a class="rustdoc-cn-home"[^>]*>.*?</a>',
    re.DOTALL,
)
# The OLD JS block contained id="rustdoc-cn-nav-script"; the NEW block reuses that id
# but has different content. We detect the OLD content via its distinctive elements:
#   - function applyHidden uses classList toggle
#   - listens for keydown with `e.key !== "["` (only `[`, not `\`)
# To be safe we match by the unique substring that the NEW script does NOT have but the OLD does.
OLD_JS_RE = re.compile(
    rb'<script defer id="rustdoc-cn-nav-script">.*?</script>',
    re.DOTALL,
)
# OLD CSS block had `transition:margin-left .2s ease,opacity .2s ease` (no .18s)
# We match the full <style id="rustdoc-cn-nav-style"> + <style>...</style> pair
OLD_CSS_RE = re.compile(
    rb'<style id="rustdoc-cn-nav-style">[^<]*</style><style>[^<]*</style>'
)

# === Skip lists ===
SKIP_TOP_DIRS = {
    'static.files', 'search.index', 'src', '_common_tools',
    '__pycache__', '.git', 'node_modules',
}


def should_skip_dir(dirname: str) -> bool:
    if dirname.startswith('.'):
        return True
    if dirname in SKIP_TOP_DIRS:
        return True
    if dirname.endswith('_old'):
        return True
    return False


# === Inject CSS into <head> ===
# Idempotency is via the unique id="rustdoc-cn-nav-style".
CSS_BLOCK = (
    b'<style id="rustdoc-cn-nav-style">.rustdoc-cn-nav-check{}</style>'
    b'<style>'
    # --- Toggle button (matches rustdoc's hamburger style) ---
    b'.sidebar-menu-toggle{width:41px;min-width:41px;border:none;line-height:0;background:transparent;cursor:pointer;padding:0;margin:0;border-radius:4px;flex-shrink:0;transition:background-color .15s ease}'
    b'.sidebar-menu-toggle::before{content:var(--hamburger-image);opacity:.75;filter:var(--mobile-sidebar-menu-filter);display:block;width:22px;height:22px;margin:0 auto}'
    b'.sidebar-menu-toggle:hover,.sidebar-menu-toggle:focus{background:rgba(0,0,0,.06);outline:none}'
    b'.sidebar-menu-toggle:hover::before,.sidebar-menu-toggle:focus::before{opacity:1}'
    # --- Home button ---
    b'.rustdoc-cn-home{display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;margin-left:6px;padding:0;border-radius:4px;color:inherit;text-decoration:none;font-size:18px;line-height:1;flex-shrink:0;transition:background-color .15s ease;cursor:pointer;user-select:none}'
    b'.rustdoc-cn-home:hover,.rustdoc-cn-home:focus{background:rgba(0,0,0,.06);outline:none}'
    b'.rustdoc-cn-home svg{display:block;width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}'
    # --- Sidebar transitions ---
    b'.rustdoc .sidebar,.rustdoc .sidebar-resizer{transition:margin-left .18s ease,opacity .18s ease}'
    # --- Desktop: hidden state ---
    b'@media (min-width:701px){'
    b'html.hide-sidebar .sidebar-menu-toggle{display:flex !important;align-items:center;justify-content:center}'
    b'html.hide-sidebar .sidebar{opacity:0;pointer-events:none;margin-left:-100%}'
    b'html.hide-sidebar .sidebar-resizer{display:none !important}'
    b'html.hide-sidebar main{padding-left:0 !important}'
    # Floating handle to bring sidebar back, on the left edge
    b'html.hide-sidebar .rustdoc-cn-sidebar-handle{opacity:.85}'
    b'.rustdoc-cn-sidebar-handle{position:fixed;left:0;top:50%;transform:translateY(-50%);z-index:99;width:18px;height:64px;background:rgba(0,0,0,.08);border:1px solid rgba(0,0,0,.12);border-left:none;border-radius:0 6px 6px 0;cursor:pointer;display:flex;align-items:center;justify-content:center;opacity:0;transition:opacity .2s ease,background-color .15s ease}'
    b'.rustdoc-cn-sidebar-handle:hover,.rustdoc-cn-sidebar-handle:focus{background:rgba(0,0,0,.18);opacity:1;outline:none}'
    b'.rustdoc-cn-sidebar-handle::before{content:"\\2039";font-size:18px;color:#333;line-height:1;font-weight:600}'
    b'html.hide-sidebar:not(.sidebar-peek) .rustdoc-cn-sidebar-handle{opacity:0;pointer-events:none}'
    # Peek: when user hovers the very left edge (8px), show the sidebar temporarily
    b'html.hide-sidebar .rustdoc-cn-sidebar-peek-zone{display:block}'
    b'.rustdoc-cn-sidebar-peek-zone{position:fixed;left:0;top:0;bottom:0;width:8px;z-index:98;display:none}'
    b'html.hide-sidebar.sidebar-peek .sidebar{opacity:1;pointer-events:auto;margin-left:0;box-shadow:4px 0 12px rgba(0,0,0,.15)}'
    b'html.hide-sidebar.sidebar-peek .rustdoc-cn-sidebar-handle{opacity:0}'
    b'}'
    # --- Mobile: hide the floating handle (mobile already has its own hamburger) ---
    b'@media (max-width:700px){.rustdoc-cn-sidebar-handle,.rustdoc-cn-sidebar-peek-zone{display:none !important}}'
    b'</style>'
)

# Marker for idempotency (unique id we control)
CSS_MARKER = b'id="rustdoc-cn-nav-style"'

# === Toggle button HTML ===
# Placed as first child of <rustdoc-topbar>
TOGGLE_BUTTON = (
    b'<button class="sidebar-menu-toggle" type="button" '
    b'aria-label="\xe6\x8a\x98\xe5\x8f\xa0/\xe5\xb1\x95\xe5\xbc\x80\xe4\xbe\xa7\xe8\xbe\xb9\xe6\xa0\x8f" '
    b'title="\xe6\x8a\x98\xe5\x8f\xa0/\xe5\xb1\x95\xe5\xbc\x80\xe4\xbe\xa7\xe8\xbe\xb9\xe6\xa0\x8f (\\ \xe9\x94\xae)" '
    b'data-show-title="\xe5\xb1\x95\xe5\xbc\x80\xe4\xbe\xa7\xe8\xbe\xb9\xe6\xa0\x8f (\\ \xe9\x94\xae)" '
    b'data-hide-title="\xe6\x8a\x98\xe5\x8f\xa0\xe4\xbe\xa7\xe8\xbe\xb9\xe6\xa0\x8f (\\ \xe9\x94\xae)"></button>'
)

# === Floating "show sidebar" handle + hover peek zone ===
# Both go inside <body> right after </rustdoc-topbar>.
SIDEBAR_HANDLE = (
    b'<div class="rustdoc-cn-sidebar-peek-zone" aria-hidden="true"></div>'
    b'<button class="rustdoc-cn-sidebar-handle" type="button" '
    b'aria-label="\xe5\xb1\x95\xe5\xbc\x80\xe4\xbe\xa7\xe8\xbe\xb9\xe6\xa0\x8f" '
    b'title="\xe5\xb1\x95\xe5\xbc\x80\xe4\xbe\xa7\xe8\xbe\xb9\xe6\xa0\x8f (\\ \xe9\x94\xae)"></button>'
)

# === Home button HTML ===
# Placed right after <div class="search-menu"> opening tag
HOME_BUTTON = (
    b'<a class="rustdoc-cn-home" href="/index.html" '
    b'title="\xe8\xbf\x94\xe5\x9b\x9e\xe9\xa6\x96\xe9\xa1\xb5" '
    b'aria-label="\xe8\xbf\x94\xe5\x9b\x9e\xe9\xa6\x96\xe9\xa1\xb5">'
    b'<svg viewBox="0 0 24 24" aria-hidden="true">'
    b'<path d="M3 11l9-8 9 8"/>'
    b'<path d="M5 10v10h14V10"/>'
    b'</svg></a>'
)

# === JS to inject before </body> ===
# - Click handler for sidebar toggle (desktop + mobile)
# - Keyboard shortcuts: `\` or `[` to toggle, Esc to close
# - localStorage persistence
# - Hover-edge peek when sidebar is hidden
# - Floating handle click + dynamic title
JS_BLOCK = (
    b'<script defer id="rustdoc-cn-nav-script">(function(){'
    b'var BTN=".sidebar-menu-toggle",STORAGE="rustdoc-cn-sidebar-hidden";'
    b'var SHOW_TITLE="\xe5\xb1\x95\xe5\xbc\x80\xe4\xbe\xa7\xe8\xbe\xb9\xe6\xa0\x8f (\\ \xe9\x94\xae)";'
    b'var HIDE_TITLE="\xe6\x8a\x98\xe5\x8f\xa0\xe4\xbe\xa7\xe8\xbe\xb9\xe6\xa0\x8f (\\ \xe9\x94\xae)";'
    b'function isDesktop(){return window.matchMedia&&window.matchMedia("(min-width: 701px)").matches;}'
    b'function applyHidden(hidden){'
    b'document.documentElement.classList[hidden?"add":"remove"]("hide-sidebar");'
    b'var btn=document.querySelector(BTN);'
    b'if(btn){btn.setAttribute("title",hidden?SHOW_TITLE:HIDE_TITLE);btn.setAttribute("aria-label",hidden?SHOW_TITLE:HIDE_TITLE);}'
    b'try{localStorage.setItem(STORAGE,hidden?"true":"false");}catch(e){}'
    b'}'
    b'function toggle(){'
    b'if(isDesktop()){'
    b'var hidden=!document.documentElement.classList.contains("hide-sidebar");'
    b'applyHidden(hidden);'
    b'}else{'
    b'var s=document.getElementsByClassName("sidebar")[0];'
    b'if(s){if(s.classList.contains("shown")){s.classList.remove("shown");}else{s.classList.add("shown");}}'
    b'}'
    b'}'
    b'function showSidebar(){if(isDesktop()){applyHidden(false);}}'
    b'document.addEventListener("DOMContentLoaded",function(){'
    b'var btn=document.querySelector(BTN);'
    b'if(!btn){return;}'
    # Initial state from localStorage
    b'var initialHidden=false;'
    b'try{initialHidden=localStorage.getItem(STORAGE)==="true";}catch(e){}'
    b'if(isDesktop()&&initialHidden){applyHidden(true);}else{applyHidden(false);}'
    # Click toggle
    b'btn.addEventListener("click",function(e){e.preventDefault();e.stopPropagation();toggle();});'
    # Handle button -> show sidebar
    b'var handle=document.querySelector(".rustdoc-cn-sidebar-handle");'
    b'if(handle){handle.addEventListener("click",function(e){e.preventDefault();e.stopPropagation();showSidebar();});}'
    # Peek zone: hover left edge -> temporary show
    b'var peek=document.querySelector(".rustdoc-cn-sidebar-peek-zone");'
    b'if(peek){'
    b'peek.addEventListener("mouseenter",function(){document.documentElement.classList.add("sidebar-peek");});'
    b'peek.addEventListener("mouseleave",function(){document.documentElement.classList.remove("sidebar-peek");});'
    b'}'
    # Keyboard shortcuts
    b'document.addEventListener("keydown",function(e){'
    b'var t=e.target.tagName;'
    b'if(t==="INPUT"||t==="TEXTAREA"||t==="SELECT"||e.target.isContentEditable){return;}'
    # Esc -> close sidebar (desktop only, only when currently shown)
    b'if(e.key==="Escape"&&isDesktop()&&!document.documentElement.classList.contains("hide-sidebar")){'
    b'e.preventDefault();applyHidden(true);return;}'
    # `\` or `[` -> toggle (no modifier keys)
    b'if((e.key==="\\\\"||e.key==="[")&&!e.ctrlKey&&!e.metaKey&&!e.altKey&&!e.shiftKey){'
    b'e.preventDefault();toggle();return;}'
    b'});'
    b'});'
    b'})();</script>'
)


def roll_back_old(html_bytes: bytes) -> bytes:
    """Remove any partial old injections so the new injection can apply cleanly."""
    out = html_bytes
    out = OLD_CSS_RE.sub(b'', out)
    out = OLD_TOGGLE_RE.sub(b'', out)
    out = OLD_HOME_RE.sub(b'', out)
    out = OLD_JS_RE.sub(b'', out)
    return out


def inject_into_file(html_bytes: bytes) -> tuple[bytes, bool, str]:
    """
    Returns (new_bytes, modified, reason).
    reason ∈ {'injected', 'upgraded', 'already-injected', 'no-topbar', 'no-search-menu', 'no-body', 'no-head'}.
    """
    # Idempotency check on the NEW injection
    if NEW_HANDLE_MARKER in html_bytes:
        return html_bytes, False, 'already-injected'

    upgraded = False
    if b'sidebar-menu-toggle' in html_bytes or b'rustdoc-cn-nav-script' in html_bytes:
        upgraded = True
        html_bytes = roll_back_old(html_bytes)

    # 1. Inject CSS into <head>
    head_end = html_bytes.find(b'</head>')
    if head_end < 0:
        return html_bytes, False, 'no-head'

    if CSS_MARKER not in html_bytes:
        new_bytes = html_bytes[:head_end] + CSS_BLOCK + html_bytes[head_end:]
    else:
        new_bytes = html_bytes

    # 2. Inject toggle button at start of <rustdoc-topbar>
    tb_open = new_bytes.find(TOPBAR_OPEN)
    if tb_open < 0:
        return html_bytes, False, 'no-topbar'
    insert_pos = tb_open + len(TOPBAR_OPEN)
    new_bytes = new_bytes[:insert_pos] + TOGGLE_BUTTON + new_bytes[insert_pos:]

    # 3. Inject floating handle + peek zone right after </rustdoc-topbar>
    tb_close = new_bytes.find(TOPBAR_CLOSE)
    if tb_close < 0:
        return html_bytes, False, 'no-topbar'
    insert_pos = tb_close + len(TOPBAR_CLOSE)
    new_bytes = new_bytes[:insert_pos] + SIDEBAR_HANDLE + new_bytes[insert_pos:]

    # 4. Inject home button inside <div class="search-menu">
    sm_open = new_bytes.find(SEARCH_MENU_OPEN)
    if sm_open < 0:
        return html_bytes, False, 'no-search-menu'
    insert_pos = sm_open + len(SEARCH_MENU_OPEN)
    new_bytes = new_bytes[:insert_pos] + HOME_BUTTON + new_bytes[insert_pos:]

    # 5. Inject JS before </body>
    body_end = new_bytes.rfind(b'</body>')
    if body_end < 0:
        return html_bytes, False, 'no-body'
    new_bytes = new_bytes[:body_end] + JS_BLOCK + new_bytes[body_end:]

    return new_bytes, True, 'upgraded' if upgraded else 'injected'


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ('-h', '--help'):
        print(__doc__)
        return
    report_only = '--report' in sys.argv

    root = '.'
    total = 0
    modified = 0
    upgraded = 0
    injected = 0
    skipped_already = 0
    skipped_no_topbar = 0
    skipped_no_search_menu = 0
    skipped_no_head = 0
    skipped_no_body = 0

    for top, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if not should_skip_dir(d)]
        for fn in files:
            if not fn.endswith('.html'):
                continue
            path = os.path.join(top, fn)
            total += 1
            with open(path, 'rb') as f:
                before = f.read()
            after, was_modified, reason = inject_into_file(before)
            if not was_modified:
                if reason == 'already-injected':
                    skipped_already += 1
                elif reason == 'no-topbar':
                    skipped_no_topbar += 1
                elif reason == 'no-search-menu':
                    skipped_no_search_menu += 1
                elif reason == 'no-head':
                    skipped_no_head += 1
                elif reason == 'no-body':
                    skipped_no_body += 1
                continue
            if not report_only:
                with open(path, 'wb') as f:
                    f.write(after)
            modified += 1
            if reason == 'upgraded':
                upgraded += 1
            else:
                injected += 1

    print(f'Total HTML files scanned: {total}')
    if report_only:
        print('(REPORT ONLY - no files modified)')
    print(f'Modified: {modified}  (upgraded old: {upgraded}, fresh inject: {injected})')
    print(f'Already injected: {skipped_already}')
    if skipped_no_topbar:
        print(f'No <rustdoc-topbar> (likely redirect/stub): {skipped_no_topbar}')
    if skipped_no_search_menu:
        print(f'No <div class="search-menu">: {skipped_no_search_menu}')
    if skipped_no_head:
        print(f'No </head>: {skipped_no_head}')
    if skipped_no_body:
        print(f'No </body>: {skipped_no_body}')


if __name__ == '__main__':
    main()