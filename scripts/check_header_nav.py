#!/usr/bin/env python3
"""Verify every HTML page uses the same Adrian Marikar blog header nav."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSET_VERSION = '20260816-mobile-nav1'
EXPECTED_HEADER = '''<header class="site-header">
      <a class="brand" href="/" aria-label="Adrian Marikar home">
        <span class="brand-mark">AM</span>
        <span>Adrian Marikar</span>
      </a>
      <details class="nav-menu" open>
        <summary>
          <span>Menu</span>
          <span class="nav-icon" aria-hidden="true"></span>
        </summary>
        <nav id="primary-navigation" aria-label="Primary navigation">
          <a href="/#writing">Writing</a>
          <a href="/categories/ai-agents.html">AI agents</a>
          <a href="/categories/newbizfeed.html">NewBizFeed</a>
          <a href="/categories/dryhomeadvice.html">Dry Home Advice</a>
          <a href="/categories/horse-racing-tips-research.html">RailSideRatings Research</a>
          <a href="/#about">About</a>
          <a href="mailto:hello@adrianmarikar.com">Contact</a>
        </nav>
      </details>
    </header>'''

HEADER_RE = re.compile(r'<header class="site-header">.*?</header>', re.S)


def main() -> int:
    failures: list[str] = []
    html_files = sorted(ROOT.glob('**/*.html'))
    for path in html_files:
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding='utf-8')
        match = HEADER_RE.search(text)
        if not match:
            failures.append(f'{rel}: missing site-header')
            continue
        if match.group(0) != EXPECTED_HEADER:
            failures.append(f'{rel}: header nav differs from canonical menu')
        if f'/styles.css?v={ASSET_VERSION}' not in text:
            failures.append(f'{rel}: missing current mobile-nav stylesheet version')
        if f'/script.js?v={ASSET_VERSION}' not in text:
            failures.append(f'{rel}: missing current mobile-nav script version')

    css = (ROOT / 'styles.css').read_text(encoding='utf-8')
    javascript = (ROOT / 'script.js').read_text(encoding='utf-8')
    for marker in (
        '.nav-menu > summary',
        '.nav-menu[open] .nav-icon',
        '@media (max-width: 1050px)',
        'max-height: calc(100svh - 5rem)',
    ):
        if marker not in css:
            failures.append(f'styles.css: missing compact-nav rule {marker!r}')
    if '.site-header { align-items: flex-start; flex-direction: column; }' in css:
        failures.append('styles.css: legacy vertical sticky-header rule remains')
    for marker in (
        "const navMenu = document.querySelector('.nav-menu')",
        "const mobileNavQuery = window.matchMedia('(max-width: 1050px)')",
        "navMenu.removeAttribute('open')",
        "mobileNavQuery.addEventListener('change'",
    ):
        if marker not in javascript:
            failures.append(f'script.js: missing compact-nav behavior {marker!r}')

    if failures:
        print('Header nav audit failed:')
        for failure in failures:
            print(f'- {failure}')
        return 1
    print(f'Header nav audit passed for {len(html_files)} HTML files')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
