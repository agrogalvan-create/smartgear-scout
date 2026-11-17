#!/usr/bin/env python3
"""Validate editorial product evidence before publishing. Python stdlib only."""
import csv
import datetime
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "products.csv"
FIELDS = ("category","brand","model","official_spec_url","verified_at","merchant",
          "merchant_url","affiliate_program","commission_source_url",
          "eligibility_from_argentina","review_status")
ALLOWED = {"pending", "reviewed", "published"}

def validate(path=PATH):
    errors = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if tuple(reader.fieldnames or ()) != FIELDS:
            return ["CSV columns do not match expected schema"]
        seen = set()
        for line, row in enumerate(reader, start=2):
            key = (row["brand"].strip().lower(), row["model"].strip().lower())
            if not all(key):
                errors.append(f"line {line}: brand and model required")
            if key in seen:
                errors.append(f"line {line}: duplicate brand/model")
            seen.add(key)
            status = row["review_status"].strip().lower()
            if status not in ALLOWED:
                errors.append(f"line {line}: invalid review_status")
            if status in {"reviewed", "published"}:
                for field in ("official_spec_url", "verified_at"):
                    if not row[field].strip():
                        errors.append(f"line {line}: {field} required for {status}")
                url = row["official_spec_url"].strip()
                if url and not url.startswith("https://"):
                    errors.append(f"line {line}: official_spec_url must be HTTPS")
                try:
                    datetime.date.fromisoformat(row["verified_at"].strip())
                except ValueError:
                    errors.append(f"line {line}: verified_at must be YYYY-MM-DD")
            if status == "published" and row["affiliate_program"].strip():
                for field in ("merchant_url", "commission_source_url"):
                    if not row[field].strip().startswith("https://"):
                        errors.append(f"line {line}: {field} HTTPS URL required")
                if row["eligibility_from_argentina"].strip().lower() != "yes":
                    errors.append(f"line {line}: affiliate eligibility not confirmed")
    return errors

if __name__ == "__main__":
    problems = validate()
    if problems:
        print("\n".join(problems), file=sys.stderr)
        sys.exit(1)
    print("Catalog schema and publication gates: PASS")
