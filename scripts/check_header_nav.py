#!/usr/bin/env python3
"""Verify every HTML page uses the same Adrian Marikar blog header nav."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_HEADER = '''<header class="site-header">
      <a class="brand" href="/" aria-label="Adrian Marikar home">
        <span class="brand-mark">AM</span>
        <span>Adrian Marikar</span>
      </a>
      <nav aria-label="Primary navigation">
        <a href="/#writing">Writing</a>
        <a href="/categories/ai-agents.html">AI agents</a>
        <a href="/categories/newbizfeed.html">NewBizFeed</a>
        <a href="/categories/dryhomeadvice.html">Dry Home Advice</a>
        <a href="/categories/horse-racing-tips-research.html">RailSideRatings Research</a>
        <a href="/#about">About</a>
        <a href="mailto:hello@adrianmarikar.com">Contact</a>
      </nav>
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
    if failures:
        print('Header nav audit failed:')
        for failure in failures:
            print(f'- {failure}')
        return 1
    print(f'Header nav audit passed for {len(html_files)} HTML files')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
