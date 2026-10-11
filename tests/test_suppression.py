"""Offline regressions for deletion and permanent opt-out checks."""
import csv
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("suppression", Path(__file__).resolve().parents[1] / "tools/suppression.py")
suppression = importlib.util.module_from_spec(spec)
spec.loader.exec_module(suppression)


class SuppressionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "sales/pitches/html").mkdir(parents=True)
        self.lead = {"id": "999", "business": "Fixture Bakehouse", "site_found": "",
                     "contact_verified": "Owner@fixture.example (their own footer)"}
        other = {"id": "1000", "business": "Other Bakery", "site_found": "other.example",
                 "contact_verified": "hello@other.example"}
        self.write_csv("prospects-2026.csv", list(self.lead), [self.lead, other])
        self.write_csv("OUTREACH-LOG.csv", ["id", "business", "contact_used", "status"], [
            {"id": "999", "business": "Fixture Bakehouse", "contact_used": "owner@fixture.example", "status": "sent"},
            {"id": "1000", "business": "Other Bakery", "contact_used": "hello@other.example", "status": "sent"},
        ])
        self.write_csv("SENT-RECORD.csv", ["to", "kind"], [
            {"to": "OWNER@fixture.example", "kind": "cold pitch"},
            {"to": "hello@other.example", "kind": "cold pitch"},
        ])
        (self.root / "sales/prospects-2026.json").write_text(json.dumps([self.lead, other]))
        (self.root / suppression.REGISTRY).write_text(json.dumps({"version": 1, "entries": []}))
        (self.root / "sales/pitches/999-fixture-bakehouse.md").write_text("old board")
        (self.root / "sales/pitches/html/999-fixture-bakehouse.html").write_text("old board")

    def write_csv(self, name, fields, rows):
        with (self.root / "sales" / name).open("w", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    def remove(self):
        return suppression.remove_lead("999", "2026-10-11", "https://www.fixture-shop.example/contact", self.root)

    def test_purge_removes_records_and_boards_without_storing_identity(self):
        counts = self.remove()
        self.assertEqual(set(counts.values()), {1})
        self.assertFalse((self.root / "sales/pitches/999-fixture-bakehouse.md").exists())
        self.assertFalse((self.root / "sales/pitches/html/999-fixture-bakehouse.html").exists())
        registry_text = (self.root / suppression.REGISTRY).read_text()
        for value in ("Fixture Bakehouse", "fixture.example", "fixture-shop.example", "owner@"):
            self.assertNotIn(value, registry_text)
        self.assertEqual(suppression.check_sources(self.root), 1)
        self.assertEqual(suppression.read_csv(self.root / "sales/prospects-2026.csv")[1][0]["id"], "1000")

    def test_same_email_alias_domain_site_name_and_id_are_blocked(self):
        self.remove()
        registry = suppression.load_registry(self.root)
        for candidate in ({"email": " OWNER@FIXTURE.EXAMPLE "}, {"email": "new@fixture.example"},
                          {"site": "https://www.fixture-shop.example/orders"},
                          {"business": "Fixture   Bakehouse"}, {"id": "999"}):
            with self.subTest(candidate=candidate):
                self.assertTrue(suppression.is_blocked(candidate, registry))
        self.assertFalse(suppression.is_blocked({"email": "hello@other.example"}, registry))
        self.assertFalse(suppression.is_blocked({}, registry))

    def test_source_check_rejects_reimport(self):
        self.remove()
        path = self.root / "sales/prospects-2026.json"
        path.write_text(json.dumps([self.lead]))
        with self.assertRaisesRegex(ValueError, "Suppressed contact"):
            suppression.check_sources(self.root)

    def test_invalid_or_missing_registry_fails_closed(self):
        (self.root / suppression.REGISTRY).unlink()
        with self.assertRaises(OSError):
            suppression.check_sources(self.root)
        (self.root / suppression.REGISTRY).write_text('{"version": 99, "entries": []}')
        with self.assertRaises(ValueError):
            suppression.check_sources(self.root)

    def test_empty_suppression_entry_fails_closed(self):
        (self.root / suppression.REGISTRY).write_text(json.dumps({"version": 1, "entries": [
            {"removed_on": "2026-10-11", "reason": "opt-out", "fingerprints": {}}
        ]}))
        with self.assertRaisesRegex(ValueError, "Empty suppression entry"):
            suppression.check_sources(self.root)

    def test_shared_mail_provider_is_not_a_business_domain(self):
        fields, rows = suppression.read_csv(self.root / "sales/prospects-2026.csv")
        rows[0]["contact_verified"] = "owner@gmail.com"
        suppression.write_csv(self.root / "sales/prospects-2026.csv", fields, rows)
        self.remove()
        registry = suppression.load_registry(self.root)
        self.assertTrue(suppression.is_blocked({"email": "owner@gmail.com"}, registry))
        self.assertFalse(suppression.is_blocked({"email": "unrelated@gmail.com"}, registry))
        self.assertNotIn(suppression.fingerprint("domain", "gmail.com"), registry["entries"][0]["fingerprints"]["domain"])

    def test_country_exclusion_is_permanent_and_distinct_from_opt_out(self):
        fields, rows = suppression.read_csv(self.root / "sales/prospects-2026.csv")
        for row in rows:
            row["country"] = "US" if row["id"] == "999" else "GB"
        suppression.write_csv(self.root / "sales/prospects-2026.csv", fields + ["country"], rows)
        suppression.exclude_countries(["US", "CA"], "2026-10-11", self.root)
        registry = suppression.load_registry(self.root)
        self.assertEqual(registry["entries"][0]["reason"], "user-exclusion")
        self.assertTrue(suppression.is_blocked({"country": "US", "email": "new@new.example"}, registry))
        self.assertTrue(suppression.is_blocked({"country": "CA"}, registry))
        self.assertFalse(suppression.is_blocked({"country": "GB", "email": "hello@other.example"}, registry))
        self.assertEqual(suppression.check_sources(self.root), 1)

    def test_unknown_id_does_not_change_data(self):
        before = (self.root / suppression.REGISTRY).read_bytes()
        with self.assertRaises(ValueError):
            suppression.remove_lead("no-such-id", "2026-10-11", root=self.root)
        self.assertEqual((self.root / suppression.REGISTRY).read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
