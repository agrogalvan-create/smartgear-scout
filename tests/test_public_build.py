"""End-to-end smoke tests for the public build, with no external packages."""
import os
import subprocess
import sys
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

class PublicBuildTests(unittest.TestCase):
    def test_public_output_and_sitemap(self):
        env = dict(os.environ, SITE_URL="https://example.com/smartgear-scout")
        subprocess.run([sys.executable, str(ROOT / "scripts/build_site.py")],
                       cwd=ROOT, env=env, check=True, capture_output=True, text=True)
        self.assertTrue((DIST / "index.html").is_file())
        self.assertTrue((DIST / "disclosure.html").is_file())
        self.assertFalse((DIST / "research").exists())
        self.assertFalse((DIST / "scripts").exists())
        self.assertFalse((DIST / ".github").exists())
        self.assertFalse((DIST / "data").exists())
        tree = ET.parse(DIST / "sitemap.xml")
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = [n.text for n in tree.findall("s:url/s:loc", ns)]
        self.assertIn("https://example.com/smartgear-scout/", urls)
        self.assertIn("https://example.com/smartgear-scout/about.html", urls)
        self.assertEqual(len(urls), len(list(DIST.rglob("*.html"))))
        robots = (DIST / "robots.txt").read_text()
        self.assertIn("Sitemap: https://example.com/smartgear-scout/sitemap.xml", robots)

if __name__ == "__main__":
    unittest.main()
