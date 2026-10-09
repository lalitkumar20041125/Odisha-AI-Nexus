"""
Unit tests for Local Google Authentication, Security, and RBAC Cryptography in Odisha AI Nexus.
Verifies tamper-evident session signatures, role-based permissions, local DB persistence, and audit logging.
"""

import unittest
import time
from security import (
    create_user_session,
    validate_session,
    sanitize_text
)
from config import ROLES, ROLE_PERMISSIONS
from database import init_db, get_user_by_uid, get_recent_audit_logs
from auth_service import upsert_user_in_db, get_auth_system_status


class TestSecurityAndAuth(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()

    def test_session_creation_and_hmac_verification(self):
        """Verify that a newly created session passes cryptographic HMAC verification."""
        user_claims = {
            "uid": "google_test_12345",
            "email": "innovator@iitbbs.ac.in",
            "display_name": "Test Innovator",
            "photo_url": "https://example.com/avatar.jpg",
            "email_verified": True
        }
        session = create_user_session(user_claims, chosen_role=ROLES["INNOVATOR"])
        self.assertIsNotNone(session)
        self.assertEqual(session["uid"], "google_test_12345")
        self.assertEqual(session["role"], ROLES["INNOVATOR"])
        self.assertIn("signature", session)

        # Verify session is valid
        is_valid, err = validate_session(session)
        self.assertTrue(is_valid)
        self.assertIsNone(err)

    def test_session_tampering_detection(self):
        """Ensure cryptographic HMAC catches any client-side claim tampering."""
        user_claims = {
            "uid": "google_regular_user",
            "email": "user@gmail.com",
            "display_name": "Regular User",
            "role": ROLES["VIEWER"]
        }
        session = create_user_session(user_claims, chosen_role=ROLES["VIEWER"])
        
        # Attacker tries to elevate role to Admin
        tampered_session = dict(session)
        tampered_session["role"] = ROLES["ADMIN"]

        is_valid, err = validate_session(tampered_session)
        self.assertFalse(is_valid)
        self.assertIn("tamper check failed", err.lower())

    def test_session_expiration(self):
        """Ensure expired session tokens are rejected."""
        session = {
            "session_id": "test_sess_expired",
            "uid": "google_exp_user",
            "email": "exp@gmail.com",
            "role": ROLES["INNOVATOR"],
            "created_at": time.time() - 10000,
            "expires_at": time.time() - 10,  # Expired in past
            "signature": "dummy_sig"
        }
        is_valid, err = validate_session(session)
        self.assertFalse(is_valid)
        self.assertIn("expired", err.lower())

    def test_local_db_user_persistence(self):
        """Verify that Google user profile persists directly in local database without cloud dependencies."""
        user_data = {
            "uid": "google_local_999",
            "email": "local.researcher@nitr.ac.in",
            "display_name": "NIT Researcher",
            "photo_url": "",
            "role": ROLES["INNOVATOR"],
            "email_verified": 1,
            "status": "active"
        }
        success, msg = upsert_user_in_db(user_data)
        self.assertTrue(success)

        retrieved = get_user_by_uid("google_local_999")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["email"], "local.researcher@nitr.ac.in")
        self.assertEqual(retrieved["role"], ROLES["INNOVATOR"])

    def test_audit_log_tracking(self):
        """Verify that authentication and security events are logged locally."""
        user_claims = {
            "uid": "google_audit_user",
            "email": "audit.test@odisha.ai",
            "display_name": "Audit Tester"
        }
        create_user_session(user_claims, chosen_role=ROLES["TALENT"])
        
        recent_logs = get_recent_audit_logs(limit=10)
        self.assertGreater(len(recent_logs), 0)
        
        login_events = [log for log in recent_logs if log["event_type"] == "AUTH_LOGIN_SUCCESS"]
        self.assertGreater(len(login_events), 0)

    def test_input_sanitization(self):
        """Verify that malicious script tags are stripped safely."""
        malicious = "<script>alert('xss')</script>Hello <b>Odisha</b>"
        cleaned = sanitize_text(malicious)
        self.assertNotIn("<script>", cleaned)
        self.assertIn("Hello", cleaned)

    def test_auth_system_status(self):
        """Verify that system reports 100% local operation with zero cloud dependencies."""
        status = get_auth_system_status()
        self.assertFalse(status["cloud_dependent"])
        self.assertIn("Local", status["mode"])
        self.assertIn("database_engine", status)
        self.assertIn("SQLite", status["database_engine"])
        self.assertIn("total_registered_users", status)


if __name__ == "__main__":
    unittest.main()
