"""
Unit tests for CSV export utilities and ReportLab PDF document compilation.
"""

import unittest
from reports import (
    export_projects_to_csv,
    export_talent_to_csv,
    export_challenges_to_csv,
    generate_ecosystem_summary_pdf,
    generate_opportunity_pdf
)


class TestReports(unittest.TestCase):
    def setUp(self):
        self.sample_projects = [
            {
                "id": 1,
                "title": "CycloneEye Inundation AI",
                "tagline": "Coastal flood prediction",
                "sector": "Disaster Management & Climate Resilience",
                "stage": "Field-Tested / Pilot",
                "lead_name": "Dr. S. Nayak",
                "organization": "IIT Bhubaneswar",
                "district": "Khordha (Bhubaneswar)",
                "tech_stack": "PyTorch, SAR",
                "status": "Active",
                "readiness_score": 78.5,
                "is_demo": 1,
                "created_at": "2026-01-01 10:00:00"
            }
        ]
        self.sample_challenges = [
            {
                "id": 1,
                "title": "Slag Detection",
                "organization_name": "Kalinga Heavy Metallurgy",
                "org_type": "PSU / Large Enterprise",
                "sector": "Steel & Heavy Metallurgy",
                "district": "Jajpur",
                "budget_range": "₹10 - ₹25 Lakhs",
                "urgency": "High",
                "status": "Open for Proposals",
                "is_demo": 1,
                "created_at": "2026-01-01 10:00:00"
            }
        ]
        self.sample_talent = [
            {
                "id": 1,
                "full_name": "Aman Biswal",
                "institution": "IIT Bhubaneswar",
                "district": "Khordha (Bhubaneswar)",
                "role_title": "CV Engineer",
                "experience_level": "Student / Fresher",
                "technical_skills": "PyTorch, OpenCV",
                "areas_of_interest": "Disaster AI",
                "portfolio_url": "https://github.com/aman",
                "is_available": 1,
                "is_demo": 1,
                "created_at": "2026-01-01 10:00:00"
            }
        ]

    def test_csv_exports(self):
        """Verify that CSV generators return valid header and row contents."""
        csv_p = export_projects_to_csv(self.sample_projects)
        self.assertIn("CycloneEye Inundation AI", csv_p)
        self.assertIn("IIT Bhubaneswar", csv_p)

        csv_t = export_talent_to_csv(self.sample_talent)
        self.assertIn("Aman Biswal", csv_t)
        self.assertIn("PyTorch", csv_t)

        csv_c = export_challenges_to_csv(self.sample_challenges)
        self.assertIn("Slag Detection", csv_c)

    def test_empty_csv_handling(self):
        """Ensure empty lists do not cause exceptions."""
        self.assertEqual(export_projects_to_csv([]), "No projects available to export.")
        self.assertEqual(export_talent_to_csv([]), "No talent profiles available to export.")
        self.assertEqual(export_challenges_to_csv([]), "No industry challenges available to export.")

    def test_ecosystem_pdf_generation(self):
        """Verify ReportLab PDF generation generates non-empty valid PDF byte array."""
        stats = {
            "projects": 8, "real_projects": 0, "demo_projects": 8,
            "talent": 6, "real_talent": 0, "demo_talent": 6,
            "challenges": 5, "real_challenges": 0, "demo_challenges": 5,
            "avg_readiness": 65.4,
            "sector_distribution": [{"sector": "Disaster Management & Climate Resilience", "cnt": 2}],
            "stage_distribution": [{"stage": "Working Prototype", "cnt": 3}],
        }
        pdf_bytes = generate_ecosystem_summary_pdf(
            stats=stats,
            top_projects=self.sample_projects,
            top_challenges=self.sample_challenges,
            include_demo=True
        )
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertGreater(len(pdf_bytes), 1000)
        # Check standard PDF file header (%PDF-)
        self.assertTrue(pdf_bytes.startswith(b"%PDF-"))

    def test_opportunity_assessment_pdf_generation(self):
        """Verify Opportunity Assessment PDF generation."""
        assessment_data = {
            "title": "Coastal Carbon Sequestration AI",
            "sector": "Disaster Management & Climate Resilience",
            "problem_statement": "Measuring mangrove carbon sequestration using SAR satellite imagery in Bhitarkanika.",
            "overall_score": 82.5,
            "factors": {
                "technical_feasibility": 80.0,
                "local_relevance": 90.0,
                "socio_economic_impact": 85.0,
                "global_market_potential": 85.0,
                "budget_resource_realism": 75.0,
                "data_regulatory_viability": 75.0,
            },
            "contributions": {
                "technical_feasibility": 16.0,
                "local_relevance": 18.0,
                "socio_economic_impact": 17.0,
                "global_market_potential": 12.75,
                "budget_resource_realism": 11.25,
                "data_regulatory_viability": 7.5,
            },
            "weights": {
                "technical_feasibility": 20,
                "local_relevance": 20,
                "socio_economic_impact": 20,
                "global_market_potential": 15,
                "budget_resource_realism": 15,
                "data_regulatory_viability": 10,
            },
            "strengths": ["High regional alignment with coastal mangroves", "Strong global blue carbon market demand"],
            "weaknesses": ["Requires SAR radar access during monsoon"],
            "recommendations": ["Establish pilot with local forestry authorities"],
            "disclaimer": "Prototype Decision-Support Tool"
        }
        pdf_bytes = generate_opportunity_pdf(assessment_data)
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertTrue(pdf_bytes.startswith(b"%PDF-"))


if __name__ == "__main__":
    unittest.main()
