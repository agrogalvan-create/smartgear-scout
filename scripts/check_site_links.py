#!/usr/bin/env python3
"""Check internal HTML links; external URLs are not fetched."""
from html.parser import HTMLParser
from pathlib import Path
from functools import lru_cache
from urllib.parse import unquote, urlsplit
import sys

ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.anchors = set()
    def handle_starttag(self, tag, attrs):
        props = dict(attrs)
        if props.get("id") is not None:
            self.anchors.add(props["id"])
        if tag == "a" and props.get("name") is not None:
            self.anchors.add(props["name"])
        if tag in ("a", "link", "script", "img"):
            value = props.get("href") if tag in ("a", "link") else props.get("src")
            if value:
                self.links.append(value)

@lru_cache(maxsize=512)
def anchors_in(path):
    parser = Links()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.anchors

def audit():
    errors = []
    pages = sorted(p for p in SITE_ROOT.rglob("*.html") if not (SITE_ROOT == ROOT and "dist" in p.relative_to(ROOT).parts))
    for page in pages:
        parser = Links()
        parser.feed(page.read_text(encoding="utf-8"))
        for href in parser.links:
            url = urlsplit(href)
            if url.scheme or url.netloc or href.startswith("//"):
                continue
            if url.path == "" and not url.fragment:
                continue
            target = (page if not url.path else ((SITE_ROOT / unquote(url.path).lstrip("/")) if url.path.startswith("/") else (page.parent / unquote(url.path)))).resolve()
            if not target.is_relative_to(SITE_ROOT):
                errors.append(f"{page.relative_to(SITE_ROOT)}: path escapes site: {href}")
                continue
            elif not target.exists():
                errors.append(f"{page.relative_to(SITE_ROOT)}: broken link: {href}")
                continue
            elif target.is_dir():
                index = target / "index.html"
                if not index.is_file():
                    errors.append(f"{page.relative_to(SITE_ROOT)}: directory without index: {href}")
                    continue
                target = index
            if url.fragment and target.suffix == ".html" and target.is_file():
                fragment = unquote(url.fragment)
                if fragment not in anchors_in(target):
                    errors.append(f"{page.relative_to(SITE_ROOT)}: missing anchor: {href}")
    return len(pages), errors

if __name__ == "__main__":
    count, errors = audit()
    for err in errors:
        print(err, file=sys.stderr)
    print(f"Audited {count} HTML files; {len(errors)} broken internal links")
    sys.exit(bool(errors))
