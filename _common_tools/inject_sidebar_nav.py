#!/usr/bin/env python3
"""
Inject navigation UI + JS into every translated HTML file.

1. Sidebar toggle button (chevron icon, follows the sidebar's right border).
   Lives as a `position:fixed` element after </rustdoc-topbar> because rustdoc
   sets the topbar to `display:none` on desktop, which would hide anything inside.
   The toggle button's `left` is driven by a custom CSS variable --cn-sidebar-w
   mirrored from the sidebar's actual rendered width via ResizeObserver.

2. Home button (house icon, links to /index.html — the crate list page).
   Placed INSIDE the sidebar nav, directly below the GitHub repo link block,
   so the two appear as a unified navigation header at the top of the sidebar.
   The home button is part of the sidebar flow, so it scrolls with the sidebar
   and is hidden when the sidebar is hidden (the toggle button on the top-left
   remains visible to bring the sidebar back).

Behavior (added via injected JS):
  * click to toggle sidebar
  * localStorage persistence (key: rustdoc-cn-sidebar-hidden)
  * keyboard shortcuts: `\\` or `[` to toggle, Esc to close
  * ResizeObserver on .sidebar updates --cn-sidebar-w so the toggle button
    follows the sidebar's right border as the user resizes it
  * during collapse, --cn-sidebar-w is frozen at its last visible value
    so the button doesn't drift toward the viewport's left edge

Idempotent: skipped if BOTH new markers (`<button class="rustdoc-cn-toggle"` and
`class="sidebar-home-link"`) are already present.

Pattern follows _common_tools/inject_github_link.py.
"""
import os
import re
import sys

# === Markers (NEW injection) ===
NEW_HANDLE_MARKER = b'<button class="rustdoc-cn-toggle"'
# The home button marker checks for the opening tag (with angle brackets) so we
# don't false-match the .sidebar-home-link CSS class definition in the injected
# <style> block. The CSS contains bare `sidebar-home-link` substrings, while
# the HTML element has `<div class="sidebar-home-link">`.
NEW_HOME_MARKER = b'<div class="sidebar-home-link">'
TOPBAR_OPEN = b'<rustdoc-topbar>'
TOPBAR_CLOSE = b'</rustdoc-topbar>'
NAV_SIDEBAR = b'<nav class="sidebar">'
GITHUB_LINK_CLASS = b'<div class="sidebar-github-link"'

# === Markers (OLD injection — to detect and roll back) ===
OLD_TOGGLE_RE = re.compile(
    rb'<button class="sidebar-menu-toggle"[^>]*></button>'
)
OLD_RUSTDOC_CN_TOGGLE_RE = re.compile(
    rb'<button class="rustdoc-cn-toggle"[^>]*>.*?</button>',
    re.DOTALL,
)
OLD_KBD_HINT_RE = re.compile(
    rb'<span class="rustdoc-cn-kbd-hint"[^>]*>.*?</span>',
    re.DOTALL,
)
OLD_HANDLE_RE = re.compile(
    rb'<button class="rustdoc-cn-sidebar-handle"[^>]*></button>'
)
OLD_PEEK_ZONE_RE = re.compile(
    rb'<div class="rustdoc-cn-sidebar-peek-zone"[^>]*></div>'
)
OLD_HOME_RE = re.compile(
    rb'<a class="rustdoc-cn-home"[^>]*>.*?</a>',
    re.DOTALL,
)
# The OLD JS block contained id="rustdoc-cn-nav-script"; the NEW block reuses that id
# but has different content. We detect the OLD content via the unique substring that
# the NEW script does NOT have but the OLD does.
OLD_JS_RE = re.compile(
    rb'<script defer id="rustdoc-cn-nav-script">.*?</script>',
    re.DOTALL,
)
# OLD CSS block: we match by the unique id="rustdoc-cn-nav-style" anchor.
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
    # --- Toggle button: small, fixed top-left corner ---
    # Pinned at top:8px left:8px — does NOT move with the resizer, so the user
    # can drag the sidebar resizer without the button getting in the way.
    # 28x28px is small enough to be unobtrusive.
    # --- Toggle button: positioned just outside the sidebar's right edge ---
    # Pinned at top:8px, left = --cn-sidebar-w + 14px. The 14px gap puts the
    # button clear of the 9px-wide .sidebar-resizer (which sits at left:
    # var(--desktop-sidebar-width) .. +9px), so the user can still drag the
    # resizer to resize the sidebar.
    #
    # We use a custom CSS variable --cn-sidebar-w (mirrored from the sidebar's
    # actual rendered width via ResizeObserver) instead of rustdoc's own
    # --desktop-sidebar-width, because rustdoc sets that variable on the
    # .sidebar element only — CSS variables don't inherit upward, so our
    # fixed-position button on <body> can't see it.
    #
    # When the sidebar is collapsed, we do NOT update --cn-sidebar-w, so the
    # button stays at its last position (i.e., where the sidebar's right
    # border used to be) instead of jumping to the viewport's left edge.
    b'.rustdoc-cn-toggle{position:fixed;top:8px;left:calc(var(--cn-sidebar-w, 200px) + 14px);z-index:calc(var(--desktop-sidebar-z-index) + 1);width:28px;height:28px;display:flex;align-items:center;justify-content:center;background-color:var(--main-background-color);border:1px solid var(--border-color);border-radius:4px;cursor:pointer;color:var(--main-color);text-decoration:none;line-height:0;padding:0;transition:left .18s ease,background-color .15s ease,border-color .15s ease}'
    b'.rustdoc-cn-toggle:hover,.rustdoc-cn-toggle:focus{background-color:var(--sidebar-background-color);border-color:var(--settings-button-border-focus);outline:none}'
    b'.rustdoc-cn-toggle svg{display:block;width:16px;height:16px;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}'
    # Icon swaps based on sidebar state
    b'.rustdoc-cn-toggle .icon-collapse{display:block}'
    b'.rustdoc-cn-toggle .icon-expand{display:none}'
    b'html.hide-sidebar .rustdoc-cn-toggle .icon-collapse{display:none}'
    b'html.hide-sidebar .rustdoc-cn-toggle .icon-expand{display:block}'
    # When sidebar is hidden, slide the button back to the viewport's top-left
    # corner (with the same 8px inset the page chrome uses elsewhere). The
    # transition on `left` gives a smooth slide.
    b'html.hide-sidebar .rustdoc-cn-toggle{left:8px}'
    # Hide on mobile (rustdoc's mobile hamburger in topbar takes over)
    b'@media (max-width:700px){.rustdoc-cn-toggle{display:none}}'
    # --- Home button: inside the sidebar, below the GitHub link ---
    # Placed inside <nav class="sidebar"> as a sibling block to the GitHub
    # repo link. Matches the github link's visual style (inline-flex icon +
    # label) so the two appear as a unified navigation header at the top of
    # the sidebar. Hidden whenever the sidebar is hidden (via the parent
    # sidebar's own opacity:0 / pointer-events:none transition).
    b'.sidebar-home-link{padding:6px 16px;margin-bottom:8px}'
    b'.sidebar-home-link a{display:inline-flex;align-items:center;gap:6px;color:#333;text-decoration:none;font-size:14px;line-height:1}'
    b'.sidebar-home-link a:hover{text-decoration:underline}'
    b'.sidebar-home-link svg{flex-shrink:0}'
    # --- Sidebar transitions ---
    # When the sidebar is hidden, we collapse its flex-basis to 0 so main
    # actually takes the full viewport (instead of leaving an empty 200px
    # gap on the left where the sidebar used to be). The width transition
    # gives a smooth slide-out animation.
    b'.rustdoc .sidebar{transition:flex-basis .18s ease,width .18s ease,opacity .18s ease}'
    b'.rustdoc .sidebar-resizer{transition:margin-left .18s ease,opacity .18s ease}'
    # --- Desktop: hidden state ---
    b'@media (min-width:701px){'
    # Collapse the sidebar to 0 flex-basis so main fills the full viewport.
    # Previously we used margin-left:-100%, but that left the sidebar occupying
    # 200px in the flex layout — causing asymmetric left/right padding on main.
    b'html.hide-sidebar .sidebar{flex:0 0 0 !important;width:0;overflow:hidden;opacity:0;pointer-events:none}'
    b'html.hide-sidebar .sidebar-resizer{display:none !important}'
    # Symmetric left/right padding so the content sits centered in the viewport.
    b'html.hide-sidebar main{padding-left:24px !important;padding-right:24px !important}'
    b'html.hide-sidebar .width-limiter{margin-left:0 !important;margin-right:auto !important}'
    b'}'
    # --- Hide rustdoc's built-in duplicate expand button ---
    # rustdoc's main.js dynamically creates <div id="sidebar-button"> inside
    # <div class="main-heading">. It is hidden by default, but its CSS
    # (#sidebar-button{display:none}, .hide-sidebar #sidebar-button{display:flex})
    # makes it appear at left:6px top:25px when html.hide-sidebar is set —
    # which duplicates our own toggle button. Hide it permanently; our toggle
    # is the single source of truth for showing/hiding the sidebar.
    b'#sidebar-button{display:none !important}'
    b'</style>'
)

# Marker for idempotency (unique id we control)
CSS_MARKER = b'id="rustdoc-cn-nav-style"'

# === Toggle button ===
# Single button: positioned at the resizer when sidebar is visible,
# or at the left viewport edge when hidden. Two SVG icons inside, only one shown
# at a time via CSS depending on .hide-sidebar state.
TOGGLE_BUTTON = (
    b'<button class="rustdoc-cn-toggle" type="button" '
    b'aria-label="\xe6\x8a\x98\xe5\x8f\xa0/\xe5\xb1\x95\xe5\xbc\x80\xe4\xbe\xa7\xe8\xbe\xb9\xe6\xa0\x8f" '
    b'title="\xe6\x8a\x98\xe5\x8f\xa0/\xe5\xb1\x95\xe5\xbc\x80\xe4\xbe\xa7\xe8\xbe\xb9\xe6\xa0\x8f (\\ \xe9\x94\xae)" '
    b'data-show-title="\xe5\xb1\x95\xe5\xbc\x80\xe4\xbe\xa7\xe8\xbe\xb9\xe6\xa0\x8f (\\ \xe9\x94\xae)" '
    b'data-hide-title="\xe6\x8a\x98\xe5\x8f\xa0\xe4\xbe\xa7\xe8\xbe\xb9\xe6\xa0\x8f (\\ \xe9\x94\xae)">'
    # Icon shown when sidebar is VISIBLE: left chevron (click to collapse)
    b'<svg class="icon-collapse" viewBox="0 0 24 24" aria-hidden="true">'
    b'<polyline points="15 6 9 12 15 18"/>'
    b'</svg>'
    # Icon shown when sidebar is HIDDEN: right chevron (click to expand)
    b'<svg class="icon-expand" viewBox="0 0 24 24" aria-hidden="true">'
    b'<polyline points="9 6 15 12 9 18"/>'
    b'</svg>'
    b'</button>'
)

# (Removed: floating handle + peek zone — now using a single toggle button)

# === Home button HTML ===
# In-sidebar navigation block (placed below the GitHub link). Mirrors the
# structure of the github-link block: a wrapping <div> for layout + a single
# inline-flex <a> with an icon + text label.
HOME_BUTTON = (
    b'<div class="sidebar-home-link">'
    b'<a href="/index.html" '
    b'title="\xe8\xbf\x94\xe5\x9b\x9e crate \xe5\x88\x97\xe8\xa1\xa8" '
    b'aria-label="\xe8\xbf\x94\xe5\x9b\x9e crate \xe5\x88\x97\xe8\xa1\xa8">'
    # House icon: roof + walls (stroke, matches the link label color)
    b'<svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    b'<path d="M3 11l9-8 9 8"/>'
    b'<path d="M5 10v10h14V10"/>'
    b'</svg>'
    b'<span>crate \xe5\x88\x97\xe8\xa1\xa8</span>'
    b'</a>'
    b'</div>'
)

# === JS to inject before </body> ===
# - Click handler for sidebar toggle (desktop + mobile)
# - Keyboard shortcuts: `\` or `[` to toggle, Esc to close
# - localStorage persistence
# - Hover-edge peek when sidebar is hidden
# - Floating handle click + dynamic title
JS_BLOCK = (
    b'<script defer id="rustdoc-cn-nav-script">(function(){'
    b'var BTN=".rustdoc-cn-toggle",STORAGE="rustdoc-cn-sidebar-hidden";'
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
    b'document.addEventListener("DOMContentLoaded",function(){'
    b'var btn=document.querySelector(BTN);'
    b'if(!btn){return;}'
    # Mirror the sidebar's rendered width into --cn-sidebar-w on documentElement.
    # rustdoc only sets --desktop-sidebar-width on the .sidebar element itself,
    # which CSS variables can't propagate up to <body>. Our fixed-position
    # button on body needs its own global copy.
    #
    # Two guards prevent the button from drifting during collapse:
    #   1. Skip updates when html.hide-sidebar is set — once the user clicks
    #      to collapse, the variable freezes at its last visible value, so the
    #      button stays at the original position even as the sidebar shrinks.
    #   2. Skip updates when width < 50 — defensive guard against any stray
    #      resize events at near-zero width.
    b'var sidebar=document.querySelector(".sidebar");'
    b'var cnW=200;'
    b'try{var s=localStorage.getItem("desktop-sidebar-width");if(s)cnW=parseInt(s,10);}catch(e){}'
    b'document.documentElement.style.setProperty("--cn-sidebar-w",cnW+"px");'
    b'if(sidebar&&window.ResizeObserver){'
    b'var updateW=function(){if(document.documentElement.classList.contains("hide-sidebar"))return;var w=sidebar.getBoundingClientRect().width;if(w>=50){document.documentElement.style.setProperty("--cn-sidebar-w",w+"px");}};'
    b'var ro=new ResizeObserver(updateW);ro.observe(sidebar);updateW();'
    b'}'
    # Initial state from localStorage
    b'var initialHidden=false;'
    b'try{initialHidden=localStorage.getItem(STORAGE)==="true";}catch(e){}'
    b'if(isDesktop()&&initialHidden){applyHidden(true);}else{applyHidden(false);}'
    # Click toggle
    b'btn.addEventListener("click",function(e){e.preventDefault();e.stopPropagation();toggle();});'
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
    out = OLD_RUSTDOC_CN_TOGGLE_RE.sub(b'', out)
    out = OLD_KBD_HINT_RE.sub(b'', out)
    out = OLD_HANDLE_RE.sub(b'', out)
    out = OLD_PEEK_ZONE_RE.sub(b'', out)
    out = OLD_HOME_RE.sub(b'', out)
    out = OLD_JS_RE.sub(b'', out)
    return out


def inject_into_file(html_bytes: bytes) -> tuple[bytes, bool, str]:
    """
    Returns (new_bytes, modified, reason).
    reason ∈ {'injected', 'upgraded', 'site-root-home-removed', 'already-injected',
              'no-topbar', 'no-sidebar', 'no-body', 'no-head',
              'malformed-nav', 'malformed-github-link'}.
    """
    # Idempotency check on the NEW injection.
    # We first roll back any partial/duplicate old injections so the count check is reliable.
    #
    # Only check substrings that appear in OLD content but NOT in NEW content —
    # otherwise we'd falsely match NEW files (e.g. the JS id
    # `rustdoc-cn-nav-script` is reused by the NEW block). The OLD_RUSTDOC_CN_TOGGLE_RE
    # regex below also matches the NEW toggle button format, so we can't use
    # `rustdoc-cn-toggle` as a "presence of OLD" signal either.
    has_any_old = (
        b'sidebar-menu-toggle' in html_bytes               # old toggle class
        or b'rustdoc-cn-sidebar-handle' in html_bytes        # old floating handle
        or b'rustdoc-cn-sidebar-peek-zone' in html_bytes     # old hover peek zone
        or b'rustdoc-cn-kbd-hint' in html_bytes              # old kbd-shortcut hint
        # Old-format home button (the previous fixed-position variant)
        or b'<a class="rustdoc-cn-home"' in html_bytes
    )
    if has_any_old:
        html_bytes = roll_back_old(html_bytes)

    # Detect site root: the repo-root index.html (crate list page). rustdoc sets
    # `data-current-crate=""` (empty string) in the rustdoc-vars meta tag for
    # this page, meaning no specific crate is being viewed. The home button
    # would just link back to itself here, so we skip its injection on this page
    # and strip any pre-existing instance.
    is_site_root = bool(re.search(rb'data-current-crate=""', html_bytes))

    # Check current state of each NEW piece after rollback
    has_toggle = NEW_HANDLE_MARKER in html_bytes
    has_home = NEW_HOME_MARKER in html_bytes
    has_css = CSS_MARKER in html_bytes
    has_js = b'rustdoc-cn-nav-script' in html_bytes

    # Strip the home button from site-root files that already have it.
    # Idempotent cleanup: removing it from files that never had it is a no-op.
    site_root_home_removed = False
    if is_site_root and has_home:
        home_re = re.compile(rb'<div class="sidebar-home-link">.*?</div>', re.DOTALL)
        html_bytes = home_re.sub(b'', html_bytes)
        has_home = False
        site_root_home_removed = True

    # Decide whether the file's current state matches what we want:
    # - non-site-root: toggle + home + css + js all present
    # - site-root:     toggle + (no home) + css + js all present
    home_should_be_present = not is_site_root
    fully_injected = (
        has_toggle
        and has_css
        and has_js
        and (has_home == home_should_be_present)
    )
    if fully_injected and not site_root_home_removed:
        return html_bytes, False, 'already-injected'

    upgraded = has_any_old or has_toggle or has_home or site_root_home_removed

    new_bytes = html_bytes

    # 1. Inject CSS into <head> (only if missing)
    if not has_css:
        head_end = new_bytes.find(b'</head>')
        if head_end < 0:
            return html_bytes, False, 'no-head'
        new_bytes = new_bytes[:head_end] + CSS_BLOCK + new_bytes[head_end:]

    # 2. Inject toggle button immediately AFTER </rustdoc-topbar>.
    #    It's position:fixed so it doesn't depend on the topbar being visible.
    if not has_toggle:
        tb_close = new_bytes.find(TOPBAR_CLOSE)
        if tb_close < 0:
            return html_bytes, False, 'no-topbar'
        insert_pos = tb_close + len(TOPBAR_CLOSE)
        new_bytes = new_bytes[:insert_pos] + TOGGLE_BUTTON + new_bytes[insert_pos:]

    # 3. Inject home button AFTER the github-link div, OR after <nav class="sidebar">
    #    if no github link is present yet. The github link is injected by
    #    _common_tools/inject_github_link.py — that script should normally run
    #    before this one. We also fall back to plain <nav class="sidebar"> for
    #    files where the github link has not been injected.
    #
    #    SKIP on site-root files (crate list page) — the home button would just
    #    link back to itself there.
    if not has_home and not is_site_root:
        github_idx = new_bytes.find(GITHUB_LINK_CLASS)
        if github_idx >= 0:
            # Find the end of the github-link div (the first </div> after the class attr).
            # The github-link div has no nested divs, so the first </div> after the class
            # attribute is the closing tag of that block.
            div_end = new_bytes.find(b'</div>', github_idx)
            if div_end < 0:
                return html_bytes, False, 'malformed-github-link'
            insert_pos = div_end + len(b'</div>')
        else:
            # Fallback: insert immediately after <nav class="sidebar">
            nav_idx = new_bytes.find(NAV_SIDEBAR)
            if nav_idx < 0:
                # No sidebar at all (redirect stub) — skip
                return html_bytes, False, 'no-sidebar'
            nav_end = new_bytes.find(b'>', nav_idx)
            if nav_end < 0:
                return html_bytes, False, 'malformed-nav'
            insert_pos = nav_end + 1
        new_bytes = new_bytes[:insert_pos] + HOME_BUTTON + new_bytes[insert_pos:]

    # 4. Inject JS before </body>
    if not has_js:
        body_end = new_bytes.rfind(b'</body>')
        if body_end < 0:
            return html_bytes, False, 'no-body'
        new_bytes = new_bytes[:body_end] + JS_BLOCK + new_bytes[body_end:]

    if site_root_home_removed:
        # Only the home-button cleanup ran; everything else was already in place.
        return new_bytes, True, 'site-root-home-removed'
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
    site_root_cleaned = 0
    skipped_already = 0
    skipped_no_topbar = 0
    skipped_no_sidebar = 0
    skipped_no_head = 0
    skipped_no_body = 0
    skipped_malformed = 0

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
                elif reason == 'no-sidebar':
                    skipped_no_sidebar += 1
                elif reason == 'no-head':
                    skipped_no_head += 1
                elif reason == 'no-body':
                    skipped_no_body += 1
                elif reason.startswith('malformed'):
                    skipped_malformed += 1
                continue
            if not report_only:
                with open(path, 'wb') as f:
                    f.write(after)
            modified += 1
            if reason == 'upgraded':
                upgraded += 1
            elif reason == 'site-root-home-removed':
                site_root_cleaned += 1
            else:
                injected += 1

    print(f'Total HTML files scanned: {total}')
    if report_only:
        print('(REPORT ONLY - no files modified)')
    print(f'Modified: {modified}  (upgraded old: {upgraded}, fresh inject: {injected}, site-root cleaned: {site_root_cleaned})')
    print(f'Already injected: {skipped_already}')
    if skipped_no_topbar:
        print(f'No </rustdoc-topbar> (likely redirect/stub): {skipped_no_topbar}')
    if skipped_no_sidebar:
        print(f'No <nav class="sidebar"> (redirect stub): {skipped_no_sidebar}')
    if skipped_no_head:
        print(f'No </head>: {skipped_no_head}')
    if skipped_no_body:
        print(f'No </body>: {skipped_no_body}')
    if skipped_malformed:
        print(f'Malformed markup: {skipped_malformed}')


if __name__ == '__main__':
    main()