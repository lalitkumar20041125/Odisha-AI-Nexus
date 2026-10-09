"""
Unit and integration tests for database operations in Odisha AI Nexus.
"""

import unittest
import os
import sqlite3
from database import (
    init_db,
    add_project,
    get_all_projects,
    get_project_by_id,
    update_project_status,
    update_project_readiness,
    delete_project,
    add_talent,
    get_all_talent,
    delete_talent,
    add_challenge,
    get_all_challenges,
    update_challenge_status,
    add_assessment,
    get_all_assessments,
    get_ecosystem_stats,
    delete_all_demo_data,
    has_demo_data,
    reset_database
)
from seed_data import seed_database_if_empty


class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        seed_database_if_empty()

    def test_database_initialization_and_seeding(self):
        """Verify that tables exist and demo data is seeded."""
        self.assertTrue(has_demo_data())
        stats = get_ecosystem_stats(include_demo=True)
        self.assertGreater(stats["projects"], 0)
        self.assertGreater(stats["talent"], 0)
        self.assertGreater(stats["challenges"], 0)

    def test_demo_vs_real_metrics_separation(self):
        """Verify that metrics accurately distinguish demo from user records."""
        stats_all = get_ecosystem_stats(include_demo=True)
        stats_real = get_ecosystem_stats(include_demo=False)
        
        # Real-only view should have fewer or equal projects than all view
        self.assertLessEqual(stats_real["projects"], stats_all["projects"])
        self.assertEqual(stats_real["demo_projects"], stats_all["demo_projects"])

    def test_add_and_retrieve_user_project(self):
        """Verify inserting a verified user project with is_demo = 0."""
        project_data = {
            "title": "Test AI Crop Rover",
            "tagline": "Autonomous soil moisture analyzer",
            "description": "A field test unit measuring electrical conductivity in Bargarh farmlands.",
            "sector": "Agriculture & Food Security",
            "stage": "Working Prototype",
            "lead_name": "Test Innovator",
            "organization": "Test University",
            "district": "Bargarh",
            "target_beneficiaries": "Paddy farmers",
            "tech_stack": "PyTorch, Raspberry Pi, LoRa",
            "github_or_demo_url": "https://github.com/test/crop-rover",
            "status": "Active",
            "readiness_score": 65.0,
            "is_demo": 0,
        }
        proj_id = add_project(project_data)
        self.assertIsInstance(proj_id, int)
        
        # Retrieve by ID
        retrieved = get_project_by_id(proj_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["title"], "Test AI Crop Rover")
        self.assertEqual(retrieved["is_demo"], 0)

        # Update status
        updated = update_project_status(proj_id, "Seeking Pilot Partners")
        self.assertTrue(updated)
        self.assertEqual(get_project_by_id(proj_id)["status"], "Seeking Pilot Partners")

        # Update readiness
        updated_r = update_project_readiness(proj_id, 75.0)
        self.assertTrue(updated_r)
        self.assertEqual(get_project_by_id(proj_id)["readiness_score"], 75.0)

        # Clean up
        delete_project(proj_id)
        self.assertIsNone(get_project_by_id(proj_id))

    def test_project_search_and_filtering(self):
        """Verify sector filtering and keyword searching."""
        # Search by sector
        agri_projects = get_all_projects(include_demo=True, sector="Agriculture & Food Security")
        for p in agri_projects:
            self.assertEqual(p["sector"], "Agriculture & Food Security")

        # Keyword search
        paddy_results = get_all_projects(include_demo=True, search="paddy")
        self.assertGreater(len(paddy_results), 0)

    def test_add_and_retrieve_talent(self):
        """Verify inserting and filtering talent profiles."""
        talent_data = {
            "full_name": "Test ML Researcher",
            "institution": "IIIT Bhubaneswar",
            "district": "Khordha (Bhubaneswar)",
            "role_title": "NLP Engineer",
            "experience_level": "Junior (1-2 years)",
            "technical_skills": "PyTorch, Transformers, Python",
            "areas_of_interest": "EdTech, Indic Languages",
            "portfolio_url": "https://github.com/test-nlp",
            "bio": "Working on Odia speech recognition.",
            "contact_email": "test@domain.com",
            "is_available": 1,
            "is_demo": 0,
        }
        t_id = add_talent(talent_data)
        self.assertIsInstance(t_id, int)

        talents = get_all_talent(include_demo=True, search="Test ML Researcher")
        self.assertGreaterEqual(len(talents), 1)
        self.assertEqual(talents[0]["institution"], "IIIT Bhubaneswar")

        # Clean up
        delete_talent(t_id)

    def test_add_and_retrieve_challenge(self):
        """Verify industry challenge insertion and status update."""
        chal_data = {
            "title": "Predictive Sinter Plant Bearing Failure",
            "organization_name": "Test Sponge Iron Ltd",
            "org_type": "MSME / Local Industry",
            "sector": "Steel & Heavy Metallurgy",
            "district": "Jajpur",
            "problem_statement": "High vibration on secondary exhaust fan motor causing unexpected shutdowns.",
            "expected_outcome": "3-hour early warning alert from vibration telemetry.",
            "budget_range": "Seed / Pilot (₹2 - ₹10 Lakhs)",
            "urgency": "High (1 - 3 months)",
            "contact_person": "Plant Engineer",
            "is_demo": 0,
        }
        c_id = add_challenge(chal_data)
        self.assertIsInstance(c_id, int)

        # Update status
        self.assertTrue(update_challenge_status(c_id, "In Evaluation"))


if __name__ == "__main__":
    unittest.main()
