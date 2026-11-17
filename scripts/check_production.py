#!/usr/bin/env python3
"""Read-only production smoke check. Uses only Python standard library."""
from urllib.request import Request, urlopen
from urllib.parse import urljoin, urlsplit
from xml.etree import ElementTree as ET
import sys

BASE = "https://smartgear-scout.pages.dev"
NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}

def fetch(path):
    request = Request(urljoin(BASE + "/", path.lstrip("/")), headers={"User-Agent": "SmartGearScout-Healthcheck/1.0"})
    with urlopen(request, timeout=20) as response:
        body = response.read()
        if response.status != 200:
            raise RuntimeError(f"{path}: HTTP {response.status}")
        return body.decode("utf-8")

def main():
    robots = fetch("/robots.txt")
    assert f"Sitemap: {BASE}/sitemap.xml" in robots, "Wrong sitemap directive"
    sitemap = ET.fromstring(fetch("/sitemap.xml"))
    urls = [node.text for node in sitemap.findall("s:url/s:loc", NS)]
    assert len(urls) >= 10, f"Unexpected sitemap size: {len(urls)}"
    assert len(urls) == len(set(urls)), "Duplicate URLs"
    assert all(urlsplit(u).scheme == "https" and urlsplit(u).netloc == urlsplit(BASE).netloc and urlsplit(u).path.startswith("/") for u in urls), "Unexpected sitemap origin"
    assert all("/google" not in u for u in urls), "Verification token leaked into sitemap"
    assert BASE + "/" in urls, "Homepage absent from sitemap"
    assert all(not urlsplit(u).query and not urlsplit(u).fragment for u in urls), "Unexpected query or fragment in sitemap"
    for url in urls:
        relative = url[len(BASE):]
        html = fetch(relative)
        expected = '<link rel="canonical" href="' + url + '">'
        assert expected in html, f"Canonical missing or incorrect: {url}"
        assert "<title>" in html, f"Missing page title: {url}"
        assert 'name="description"' in html, f"Missing meta description: {url}"
    print(f"OK: robots, sitemap and {len(urls)} canonical pages are accessible")

if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Production smoke check FAILED: {error}", file=sys.stderr)
        raise SystemExit(1)
