#!/usr/bin/env python3
"""Check this static package without downloads or third-party Python packages."""
from __future__ import annotations

import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []


def check(ok: bool, message: str) -> None:
    print(('PASS' if ok else 'FAIL') + '  ' + message)
    if not ok:
        errors.append(message)


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.resources: list[str] = []
        self.scripts: list[str] = []
        self.in_script = False
        self.current: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str]]) -> None:
        a = dict(attrs)
        if tag == 'script':
            self.in_script = True
            self.current = []
        for key in ('src', 'poster'):
            if a.get(key):
                self.resources.append(a[key])
        if tag == 'link' and a.get('href'):
            self.resources.append(a['href'])

    def handle_data(self, data: str) -> None:
        if self.in_script:
            self.current.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == 'script' and self.in_script:
            self.scripts.append(''.join(self.current))
            self.in_script = False


def main() -> int:
    required = ['index.html', 'README.md', '.nojekyll', '.gitignore',
                '.gitattributes', 'package-info.json', 'data/world-v9.json',
                'docs/GITHUB_PAGES_SETUP.md', 'docs/GAME_GUIDE.md',
                'docs/PROJECT_NOTES.md', 'docs/PACKAGE_CHECKS.md']
    for name in required:
        check((ROOT / name).is_file(), 'Required file: ' + name)
    if errors:
        return 1

    html = (ROOT / 'index.html').read_text(encoding='utf-8')
    info = json.loads((ROOT / 'package-info.json').read_text(encoding='utf-8'))
    digest = hashlib.sha256((ROOT / 'index.html').read_bytes()).hexdigest()
    check(digest == info['entrySha256'], 'index.html matches package manifest SHA-256')
    if not info.get('gameplayModified'):
        check(digest == info['sourceSha256'], 'Original v9 game preserved byte-for-byte')
    check('<html lang="ko">' in html, 'Korean document language')
    check("version:'9.0.0'" in html, 'v9 runtime version declared')
    check('viewport-fit=cover' in html, 'Original responsive viewport preserved')

    page = PageParser()
    page.feed(html)
    external = [x for x in page.resources if x.startswith(('http:', 'https:', '//'))]
    absolute = [x for x in page.resources if x.startswith('/')]
    check(not external, 'No external runtime script, image or stylesheet tags')
    check(not absolute, 'No root-absolute runtime resource tags')
    for resource in page.resources:
        if resource.startswith(('data:', 'blob:', '#')):
            continue
        check((ROOT / unquote(urlsplit(resource).path)).is_file(), 'Runtime asset: ' + resource)

    # Reference links and normal Markdown links, excluding fenced command examples.
    for path in sorted(ROOT.rglob('*.md')):
        text = re.sub(r'```.*?```', '', path.read_text(encoding='utf-8'), flags=re.S)
        links = re.findall(r'!?\[[^\]\n]*\]\(([^)\n]+)\)', text)
        for link in links:
            target = link.split(' "', 1)[0].strip().strip('<>')
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith(('#', '//')):
                continue
            resolved = (path.parent / unquote(parsed.path)).resolve()
            check(resolved.is_file(), path.relative_to(ROOT).as_posix() + ' -> ' + target)

    for path in sorted(ROOT.rglob('*.json')):
        try:
            json.loads(path.read_text(encoding='utf-8-sig'))
            check(True, 'Valid JSON: ' + path.relative_to(ROOT).as_posix())
        except (ValueError, OSError) as exc:
            check(False, 'Invalid JSON: ' + str(exc))

    world = json.loads((ROOT / 'data/world-v9.json').read_text(encoding='utf-8-sig'))
    check(len(world['nodes']) == 51, 'Reference world data: 51 conquest nodes')
    check(len(world['units']) == 7, 'Reference world data: 7 troop classes')
    check(len(world['heroUnits']) == 99, 'Reference world data: 99 officer class assignments')
    ids = {n['id'] for n in world['nodes']}
    check(len(ids) == len(world['nodes']), 'Unique reference city IDs')
    fonts = [p for p in ROOT.rglob('*') if p.suffix.lower() in {'.ttf', '.otf', '.woff', '.woff2'}]
    check(not fonts, 'No font files included')

    node = shutil.which('node')
    if node:
        for i, script in enumerate(page.scripts, 1):
            with tempfile.TemporaryDirectory() as folder:
                js = Path(folder) / 'game.js'
                js.write_text(script, encoding='utf-8')
                try:
                    result = subprocess.run([node, '--check', str(js)], text=True,
                                            capture_output=True, timeout=30, check=False)
                    check(result.returncode == 0, 'JavaScript syntax: inline block ' + str(i))
                    if result.returncode:
                        print(result.stderr)
                except subprocess.TimeoutExpired:
                    check(False, 'JavaScript syntax check timed out')
    else:
        print('SKIP  Node.js not installed; JavaScript syntax check skipped.')

    print('\n' + ('Package checks failed.' if errors else 'Package checks passed.'))
    print('This check does not publish to GitHub or replace gameplay/browser testing.')
    return 1 if errors else 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError) as exc:
        print('ERROR  ' + str(exc), file=sys.stderr)
        sys.exit(1)
