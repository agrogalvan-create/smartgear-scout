#!/usr/bin/env python3
"""Regression tests for product catalog publication gates."""
import csv
import tempfile
import unittest
from pathlib import Path
from scripts.validate_products import FIELDS, validate

class CatalogTests(unittest.TestCase):
    def check_rows(self, rows):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "products.csv"
            with path.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(stream, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(rows)
            return validate(path)

    def row(self, **changes):
        base = dict.fromkeys(FIELDS, "")
        base.update(category="smart-irrigation", brand="Test", model="Model A", review_status="pending")
        base.update(changes)
        return base

    def test_pending_without_sources_allowed(self):
        self.assertEqual(self.check_rows([self.row()]), [])

    def test_reviewed_without_sources_rejected(self):
        errors = self.check_rows([self.row(review_status="reviewed")])
        self.assertTrue(any("official_spec_url" in error for error in errors))
        self.assertTrue(any("verified_at" in error for error in errors))

    def test_duplicate_rejected(self):
        errors = self.check_rows([self.row(), self.row()])
        self.assertTrue(any("duplicate" in error for error in errors))

    def test_affiliate_without_eligibility_rejected(self):
        errors = self.check_rows([self.row(
            review_status="published", official_spec_url="https://example.com/specs",
            verified_at="2026-11-17", affiliate_program="Test Program",
            merchant_url="https://example.com/buy",
            commission_source_url="https://example.com/terms",
            eligibility_from_argentina="unknown")])
        self.assertTrue(any("eligibility" in error for error in errors))

if __name__ == "__main__":
    unittest.main()
