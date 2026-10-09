"""
Unit tests for Global Market Readiness assessment logic.
"""

import unittest
from readiness import evaluate_readiness, READINESS_CHECKLIST


class TestReadiness(unittest.TestCase):
    def test_zero_completion(self):
        """Verify score is 0 when no checklist items are selected."""
        res = evaluate_readiness([], "Agriculture & Food Security")
        self.assertEqual(res["score"], 0.0)
        self.assertEqual(res["completed_count"], 0)
        self.assertEqual(len(res["missing_items"]), len(READINESS_CHECKLIST))
        self.assertGreater(len(res["actionable_remedies"]), 0)

    def test_full_completion(self):
        """Verify score is 100 when all checklist items are selected."""
        all_ids = [item["id"] for item in READINESS_CHECKLIST]
        res = evaluate_readiness(all_ids, "Steel & Heavy Metallurgy")
        self.assertEqual(res["score"], 100.0)
        self.assertEqual(res["completed_count"], len(READINESS_CHECKLIST))
        self.assertEqual(len(res["missing_items"]), 0)

    def test_partial_completion(self):
        """Verify proportional scoring and category summaries."""
        some_ids = ["prototype", "measurable_roi", "documentation"]
        res = evaluate_readiness(some_ids, "Disaster Management & Climate Resilience")
        self.assertEqual(res["score"], 30.0)
        self.assertEqual(res["completed_count"], 3)
        self.assertIn("target_corridors", res)
        self.assertGreater(len(res["target_corridors"]), 0)


if __name__ == "__main__":
    unittest.main()
