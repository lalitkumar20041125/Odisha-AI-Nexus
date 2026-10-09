"""
Unit tests for Opportunity Explorer scoring algorithm.
Verifies score boundaries (0-100), weight consistency, factor contributions, and reproducibility.
"""

import unittest
from scoring import calculate_opportunity_score
from config import DEFAULT_SCORING_WEIGHTS


class TestOpportunityScoring(unittest.TestCase):
    def test_score_range_and_boundaries(self):
        """Ensure scores remain strictly within 0 to 100 for any extreme input."""
        # Low inputs
        res_min = calculate_opportunity_score(
            title="Basic Idea",
            sector="Agriculture & Food Security",
            problem_statement="Basic test",
            tech_feasibility_input=1,
            impact_input=1,
            budget_input=1,
            data_readiness_input=1,
            global_potential_input=1
        )
        self.assertGreaterEqual(res_min["overall_score"], 0.0)
        self.assertLessEqual(res_min["overall_score"], 100.0)

        # High inputs
        res_max = calculate_opportunity_score(
            title="Advanced Rice Paddy Cyclone Inundation AI",
            sector="Disaster Management & Climate Resilience",
            problem_statement="A comprehensive physics-informed satellite radar model for cyclone storm surge routing in Ganjam and Puri coastal villages.",
            tech_feasibility_input=10,
            impact_input=10,
            budget_input=10,
            data_readiness_input=10,
            global_potential_input=10
        )
        self.assertGreaterEqual(res_max["overall_score"], 80.0)
        self.assertLessEqual(res_max["overall_score"], 100.0)

    def test_deterministic_reproducibility(self):
        """Ensure identical inputs always produce identical scores and contributions."""
        args = {
            "title": "Sambalpuri Handloom Motif Verifier",
            "sector": "Handlooms, Handicrafts & MSME Artisans",
            "problem_statement": "Detecting counterfeit powerloom imitations using microscopic weave density cameras in Bargarh.",
            "tech_feasibility_input": 7,
            "impact_input": 8,
            "budget_input": 6,
            "data_readiness_input": 5,
            "global_potential_input": 8
        }
        res1 = calculate_opportunity_score(**args)
        res2 = calculate_opportunity_score(**args)
        self.assertEqual(res1["overall_score"], res2["overall_score"])
        self.assertEqual(res1["factors"], res2["factors"])
        self.assertEqual(res1["contributions"], res2["contributions"])

    def test_factor_contribution_consistency(self):
        """Verify that the sum of factor contributions approximately matches the overall score."""
        res = calculate_opportunity_score(
            title="Iron Ore Impurity Sorter",
            sector="Steel & Heavy Metallurgy",
            problem_statement="Near-infrared optical classification of silica impurities in Jajpur.",
            tech_feasibility_input=8,
            impact_input=7,
            budget_input=7,
            data_readiness_input=6,
            global_potential_input=8
        )
        contrib_sum = sum(res["contributions"].values())
        # Should be within 0.2 due to rounding of individual contributions
        self.assertAlmostEqual(res["overall_score"], contrib_sum, delta=0.2)

    def test_custom_weights_application(self):
        """Verify that custom weights alter the final score appropriately."""
        args = {
            "title": "Cashew Quality AI",
            "sector": "Agriculture & Food Security",
            "problem_statement": "Cashew grading",
            "tech_feasibility_input": 10,
            "impact_input": 2,
            "budget_input": 2,
            "data_readiness_input": 2,
            "global_potential_input": 2
        }
        # Standard weights
        res_std = calculate_opportunity_score(**args)

        # Heavily overweight technical feasibility (50%)
        heavy_tech_weights = {
            "technical_feasibility": 50,
            "local_relevance": 10,
            "socio_economic_impact": 10,
            "global_market_potential": 10,
            "budget_resource_realism": 10,
            "data_regulatory_viability": 10,
        }
        res_custom = calculate_opportunity_score(**args, custom_weights=heavy_tech_weights)
        
        # Since tech feasibility is 10/10 (100) and other factors are low, custom score must be higher
        self.assertGreater(res_custom["overall_score"], res_std["overall_score"])

    def test_risk_and_market_coverage(self):
        """Ensure risk matrix contains all 4 dimensions and target markets are populated."""
        res = calculate_opportunity_score(
            title="Mine Dumper Dispatch AI",
            sector="Mining & Mineral Exploration",
            problem_statement="Haulage scheduling in Talcher coalfield.",
            tech_feasibility_input=6,
            impact_input=7,
            budget_input=6,
            data_readiness_input=6,
            global_potential_input=8
        )
        self.assertIn("technical", res["risks"])
        self.assertIn("financial", res["risks"])
        self.assertIn("operational", res["risks"])
        self.assertIn("adoption", res["risks"])
        self.assertGreater(len(res["target_markets"]), 0)


if __name__ == "__main__":
    unittest.main()
