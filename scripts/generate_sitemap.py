#!/usr/bin/env python3
"""Generate sitemap for a confirmed production origin; no external dependencies."""
import os
from pathlib import Path
from html import escape
import re
from urllib.parse import urlparse
from xml.etree.ElementTree import Element, SubElement, ElementTree

root = Path(__file__).resolve().parents[1]
out = root / "dist"
origin = os.environ.get("SITE_URL", "").strip().rstrip("/")
parsed = urlparse(origin)
if (parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password
        or parsed.query or parsed.fragment or parsed.path.endswith("/") and parsed.path != "/"
        or ".." in parsed.path.split("/")):
    raise SystemExit("SITE_URL must be an explicitly confirmed HTTPS site origin/path")
if not out.joinpath("index.html").exists():
    raise SystemExit("Build dist/ first with scripts/build_site.py")
sitemap = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
for page in sorted(out.rglob("*.html")):
    relative = page.relative_to(out).as_posix()
    # Google ownership tokens are verification files, not editorial pages.
    if page.name.startswith("google") and page.parent == out:
        continue
    loc = origin + ("/" if relative == "index.html" else "/" + relative)
    # Set a canonical URL in each deployed editorial page, not the source files.
    html = page.read_text(encoding="utf-8")
    html = re.sub(r'<link\s+rel="canonical"\s+href="[^"]*"\s*/?>', "", html, flags=re.I)
    if "</head>" not in html:
        raise SystemExit(f"Missing closing head tag in {relative}")
    canonical = '<link rel="canonical" href="' + escape(loc, quote=True) + '">'
    page.write_text(html.replace("</head>", canonical + "</head>", 1), encoding="utf-8")
    entry = SubElement(sitemap, "url")
    SubElement(entry, "loc").text = loc
ElementTree(sitemap).write(out / "sitemap.xml", encoding="utf-8", xml_declaration=True)
robots_path = out / "robots.txt"
robots = robots_path.read_text(encoding="utf-8")
robots = re.sub(r"(?m)^Sitemap: .*\n?", "", robots).rstrip() + f"\nSitemap: {origin}/sitemap.xml\n"
robots_path.write_text(robots, encoding="utf-8")
print(f"Created sitemap for {origin}")
