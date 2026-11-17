#!/usr/bin/env python3
"""Build a public-only static directory for hosting. No dependencies."""
from pathlib import Path
import shutil

root = Path(__file__).resolve().parents[1]
out = root / "dist"
if out.exists():
    shutil.rmtree(out)
out.mkdir()
for name in ("index.html", "about.html", "disclosure.html", "robots.txt"):
    src = root / name
    if src.is_file():
        shutil.copy2(src, out / name)
for verification in root.glob("google*.html"):
    shutil.copy2(verification, out / verification.name)
for folder in ("guides",):
    src = root / folder
    if src.is_dir():
        shutil.copytree(src, out / folder)
assert (out / "index.html").exists(), "Missing home page"
for verification in root.glob("google*.html"):
    assert (out / verification.name).exists(), "Missing Google verification file"
assert (out / "disclosure.html").exists(), "Missing disclosure"
assert (out / "about.html").exists(), "Missing about page"
import os
import subprocess
import sys
if os.environ.get("SITE_URL"):
    subprocess.run([sys.executable, str(root / "scripts" / "generate_sitemap.py")], check=True)
print("Public-only site assembled in dist/; internal research and source scripts excluded.")
