"""
Unit tests for Talent Matcher engine and privacy safeguarding.
"""

import unittest
from matching import (
    calculate_talent_project_match,
    mask_email,
    find_top_talent_for_project,
    find_top_projects_for_talent
)


class TestMatching(unittest.TestCase):
    def setUp(self):
        self.sample_project = {
            "id": 1,
            "title": "CycloneEye Inundation AI",
            "sector": "Disaster Management & Climate Resilience",
            "tech_stack": "PyTorch, Sentinel-1 SAR, UNet, OpenCV, Python",
            "description": "Satellite flood segmentation and hydrological routing in Ganjam.",
            "district": "Khordha (Bhubaneswar)",
        }
        self.matching_talent = {
            "id": 10,
            "full_name": "Aman Biswal",
            "technical_skills": "PyTorch, OpenCV, Computer Vision, Python",
            "areas_of_interest": "Disaster Management & Climate Resilience, Edge AI",
            "district": "Khordha (Bhubaneswar)",
            "contact_email": "aman.biswal@iitbbs.demo",
        }
        self.non_matching_talent = {
            "id": 11,
            "full_name": "Suresh Mohanty",
            "technical_skills": "Java, Spring Boot, MySQL",
            "areas_of_interest": "Fintech, Banking",
            "district": "Cuttack",
            "contact_email": "suresh@fintech.demo",
        }

    def test_high_skill_and_domain_match(self):
        """Verify high score and reasons when skills, domain, and district align."""
        match = calculate_talent_project_match(self.matching_talent, self.sample_project)
        self.assertGreaterEqual(match["score"], 60.0)
        self.assertTrue(match["has_domain_overlap"])
        self.assertTrue(match["has_district_proximity"])
        self.assertGreater(len(match["matched_skills"]), 0)
        self.assertGreater(len(match["reasons"]), 0)

    def test_low_match_for_unrelated_profile(self):
        """Verify lower score when neither skills nor domain overlap."""
        match_high = calculate_talent_project_match(self.matching_talent, self.sample_project)
        match_low = calculate_talent_project_match(self.non_matching_talent, self.sample_project)
        self.assertLess(match_low["score"], match_high["score"])

    def test_email_masking_privacy(self):
        """Ensure emails are safely masked for privacy protection."""
        masked = mask_email("soumya.nayak@iitbbs.ac.in")
        self.assertIn("@iitbbs.ac.in", masked)
        self.assertIn("*", masked)
        self.assertNotIn("soumya.nayak", masked)

        # Short email
        short_masked = mask_email("ab@cd.com")
        self.assertTrue("*" in short_masked or "@" in short_masked)

        # Empty / None
        self.assertEqual(mask_email(""), "Private / Confidential")
        self.assertEqual(mask_email(None), "Private / Confidential")

    def test_ranking_functions(self):
        """Verify top candidate ranking for a project."""
        talents = [self.non_matching_talent, self.matching_talent]
        top = find_top_talent_for_project(self.sample_project, talents, top_n=2)
        self.assertEqual(len(top), 2)
        # Aman should be ranked #1
        self.assertEqual(top[0][0]["full_name"], "Aman Biswal")


if __name__ == "__main__":
    unittest.main()
