"""A sent offer must not acquire a duplicate discovery row's licence price."""
import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("outreach_data", Path(__file__).resolve().parents[1] / "tools/outreach_data.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ContactIndexTests(unittest.TestCase):
    def test_sent_log_wins_over_uncontacted_row_in_either_order(self):
        active = {"id": "1", "contact_verified": "sales@fixture.example (own page)", "quote_eur": "2900"}
        duplicate = {"id": "2", "contact_verified": "sales@fixture.example (same business)", "quote_eur": "149"}
        log = {"1": {"status": "sent"}, "2": {"status": "no-pitch"}}
        for rows in ([active, duplicate], [duplicate, active]):
            self.assertEqual(module.contact_index(rows, log)["sales@fixture.example"], active)

    def test_two_sent_rows_are_ambiguous_and_not_silently_priced(self):
        rows = [{"id": "1", "contact_verified": "sales@fixture.example"},
                {"id": "2", "contact_verified": "sales@fixture.example"}]
        with self.assertRaisesRegex(ValueError, "Ambiguous"):
            module.contact_index(rows, {"1": {"status": "sent"}, "2": {"status": "sent"}})


if __name__ == "__main__":
    unittest.main()
