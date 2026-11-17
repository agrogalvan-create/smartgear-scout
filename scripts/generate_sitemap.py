#!/usr/bin/env python3
"""Generate sitemap for a confirmed production origin; no external dependencies."""
import os
from pathlib import Path
from urllib.parse import urlparse
from xml.etree.ElementTree import Element, SubElement, ElementTree

root = Path(__file__).resolve().parents[1]
out = root / "dist"
origin = os.environ.get("SITE_URL", "").strip().rstrip("/")
parsed = urlparse(origin)
if parsed.scheme != "https" or not parsed.netloc or parsed.query or parsed.fragment:
    raise SystemExit("SITE_URL must be an explicitly confirmed HTTPS site origin/path")
if not out.joinpath("index.html").exists():
    raise SystemExit("Build dist/ first with scripts/build_site.py")
sitemap = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
for page in sorted(out.rglob("*.html")):
    relative = page.relative_to(out).as_posix()
    loc = origin + ("/" if relative == "index.html" else "/" + relative)
    entry = SubElement(sitemap, "url")
    SubElement(entry, "loc").text = loc
ElementTree(sitemap).write(out / "sitemap.xml", encoding="utf-8", xml_declaration=True)
with (out / "robots.txt").open("a", encoding="utf-8") as f:
    f.write(f"\nSitemap: {origin}/sitemap.xml\n")
print(f"Created sitemap for {origin}")
