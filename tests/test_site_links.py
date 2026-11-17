"""Regression tests for the static internal-link checker."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "check_site_links.py"

class LinkAuditTests(unittest.TestCase):
    def run_audit(self, files):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name, html in files.items():
                page = root / name
                page.parent.mkdir(parents=True, exist_ok=True)
                page.write_text(html, encoding="utf-8")
            return subprocess.run([sys.executable, str(CHECKER), str(root)],
                                  capture_output=True, text=True)

    def test_valid_cross_page_and_same_page_fragments(self):
        result = self.run_audit({
            "index.html": '<a href="#intro">Intro</a><h2 id="intro">Start</h2><a href="guides/a.html#detail">Guide</a>',
            "guides/a.html": '<h2 id="detail">Detail</h2><a href="../index.html">Home</a>',
        })
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_missing_fragment_fails(self):
        result = self.run_audit({
            "index.html": '<a href="guide.html#missing">Broken</a>',
            "guide.html": '<h2 id="other">Other</h2>',
        })
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing anchor", result.stderr)

    def test_directory_index_fragment_is_checked(self):
        result = self.run_audit({
            "index.html": '<a href="guides/#missing">Guide section</a>',
            "guides/index.html": '<h2 id="present">Present</h2>',
        })
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing anchor", result.stderr)

    def test_directory_index_fragment_can_pass(self):
        result = self.run_audit({
            "index.html": '<a href="guides/#present">Guide section</a>',
            "guides/index.html": '<h2 id="present">Present</h2>',
        })
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_missing_file_fails(self):
        result = self.run_audit({"index.html": '<a href="missing.html">Missing</a>'})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("broken link", result.stderr)

if __name__ == "__main__":
    unittest.main()
