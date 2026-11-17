"""Reproducible positive and negative cases with synthetic inputs."""

import unittest
from demo import triage_request, process_requests


class TriageTests(unittest.TestCase):
    def test_complete_request_requires_human_review(self):
        result = triage_request({"request_id": "R1", "message": "250 kg steel to buyer@example.org"})
        self.assertEqual(result["status"], "ready_for_human_review")
        self.assertEqual(result["quantity_kg"], 250)
        self.assertTrue(result["human_approval_required"])

    def test_missing_contact_requires_clarification(self):
        result = triage_request({"request_id": "R2", "message": "100 kg copper"})
        self.assertIn("email contact", result["missing"])

    def test_conflicting_materials(self):
        result = triage_request({"request_id": "R3",
                                 "message": "steel or aluminium 50 kg to buyer@example.org"})
        self.assertIsNone(result["material"])
        self.assertIn("one clear material", result["missing"])

    def test_missing_quantity(self):
        result = triage_request({"request_id": "R4",
                                 "message": "steel to buyer@example.org"})
        self.assertIn("quantity in kg", result["missing"])

    def test_empty_id_rejected(self):
        with self.assertRaises(ValueError):
            triage_request({"request_id": "", "message": "steel 50 kg to a@b.org"})

    def test_duplicate_id_rejected(self):
        with self.assertRaises(ValueError):
            process_requests([{"request_id": "A", "message": "steel"},
                              {"request_id": "A", "message": "copper"}])

    def test_non_text_rejected(self):
        with self.assertRaises(ValueError):
            triage_request({"request_id": "A", "message": 77})

    def test_no_autonomous_quote_or_send(self):
        result = triage_request({"request_id": "R8", "message": "25 kg copper, x@example.com"})
        self.assertEqual(result["next_action"], "human_validate_and_prepare_quote")
        self.assertTrue(result["human_approval_required"])


if __name__ == "__main__":
    unittest.main()
