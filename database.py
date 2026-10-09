"""
Database management module for Odisha AI Nexus.
Uses SQLite for persistent, zero-configuration local storage.
Implements parameterized queries, error handling, and demo-data tagging.
"""

import sqlite3
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from config import DB_PATH

logger = logging.getLogger(__name__)


def get_connection() -> sqlite3.Connection:
    """Return a thread-safe connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create all required tables if they do not exist."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Projects Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                tagline TEXT,
                description TEXT NOT NULL,
                sector TEXT NOT NULL,
                stage TEXT NOT NULL,
                lead_name TEXT NOT NULL,
                organization TEXT,
                district TEXT NOT NULL,
                target_beneficiaries TEXT,
                tech_stack TEXT,
                github_or_demo_url TEXT,
                status TEXT NOT NULL DEFAULT 'Active',
                readiness_score REAL DEFAULT 0.0,
                is_demo INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Talent Profiles Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS talent_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                institution TEXT NOT NULL,
                district TEXT NOT NULL,
                role_title TEXT NOT NULL,
                experience_level TEXT NOT NULL,
                technical_skills TEXT NOT NULL,
                areas_of_interest TEXT NOT NULL,
                portfolio_url TEXT,
                bio TEXT,
                contact_email TEXT,
                is_available INTEGER DEFAULT 1,
                is_demo INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Industry Challenges Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS industry_challenges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                organization_name TEXT NOT NULL,
                org_type TEXT NOT NULL,
                sector TEXT NOT NULL,
                district TEXT NOT NULL,
                problem_statement TEXT NOT NULL,
                expected_outcome TEXT NOT NULL,
                budget_range TEXT NOT NULL,
                urgency TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Open for Proposals',
                contact_person TEXT,
                is_demo INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Opportunity Assessments Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS opportunity_assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idea_title TEXT NOT NULL,
                sector TEXT NOT NULL,
                problem_statement TEXT NOT NULL,
                overall_score REAL NOT NULL,
                factor_breakdown_json TEXT NOT NULL,
                strengths_json TEXT,
                weaknesses_json TEXT,
                recommendations_json TEXT,
                risks_json TEXT,
                target_markets_json TEXT,
                is_demo INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Users Table (Mirrors Firebase Firestore users collection locally)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                uid TEXT PRIMARY KEY,
                email TEXT NOT NULL UNIQUE,
                display_name TEXT,
                photo_url TEXT,
                role TEXT NOT NULL DEFAULT 'Innovator / Researcher',
                email_verified INTEGER DEFAULT 1,
                status TEXT NOT NULL DEFAULT 'active',
                last_login_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Security Audit Logs Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS auth_audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                user_id TEXT,
                email TEXT,
                ip_address TEXT,
                details TEXT,
                status TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()


# ==============================================================================
# PROJECT CRUD
# ==============================================================================

def add_project(data: Dict[str, Any]) -> int:
    """Insert a new project into the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO projects (
                title, tagline, description, sector, stage, lead_name,
                organization, district, target_beneficiaries, tech_stack,
                github_or_demo_url, status, readiness_score, is_demo, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """, (
            data.get("title", "").strip(),
            data.get("tagline", "").strip(),
            data.get("description", "").strip(),
            data.get("sector", ""),
            data.get("stage", ""),
            data.get("lead_name", "").strip(),
            data.get("organization", "").strip(),
            data.get("district", ""),
            data.get("target_beneficiaries", "").strip(),
            data.get("tech_stack", "").strip(),
            data.get("github_or_demo_url", "").strip(),
            data.get("status", "Active"),
            float(data.get("readiness_score", 0.0)),
            1 if data.get("is_demo") else 0,
        ))
        conn.commit()
        return cursor.lastrowid


def get_all_projects(
    include_demo: bool = True,
    sector: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Retrieve projects with optional filters."""
    query = "SELECT * FROM projects WHERE 1=1"
    params: List[Any] = []

    if not include_demo:
        query += " AND is_demo = 0"

    if sector and sector != "All Sectors":
        query += " AND sector = ?"
        params.append(sector)

    if status and status != "All Statuses":
        query += " AND status = ?"
        params.append(status)

    if search:
        query += " AND (title LIKE ? OR description LIKE ? OR tech_stack LIKE ? OR organization LIKE ?)"
        wildcard = f"%{search}%"
        params.extend([wildcard, wildcard, wildcard, wildcard])

    query += " ORDER BY id DESC"

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def get_project_by_id(project_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve a single project by ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def update_project_status(project_id: int, new_status: str) -> bool:
    """Update the status of a project."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE projects
            SET status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (new_status, project_id))
        conn.commit()
        return cursor.rowcount > 0


def update_project_readiness(project_id: int, readiness_score: float) -> bool:
    """Update the global readiness score for a project."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE projects
            SET readiness_score = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (readiness_score, project_id))
        conn.commit()
        return cursor.rowcount > 0


def delete_project(project_id: int) -> bool:
    """Delete a project by ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        conn.commit()
        return cursor.rowcount > 0


# ==============================================================================
# TALENT PROFILES CRUD
# ==============================================================================

def add_talent(data: Dict[str, Any]) -> int:
    """Insert a new talent profile."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO talent_profiles (
                full_name, institution, district, role_title, experience_level,
                technical_skills, areas_of_interest, portfolio_url, bio,
                contact_email, is_available, is_demo, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (
            data.get("full_name", "").strip(),
            data.get("institution", "").strip(),
            data.get("district", ""),
            data.get("role_title", "").strip(),
            data.get("experience_level", ""),
            data.get("technical_skills", "").strip(),
            data.get("areas_of_interest", "").strip(),
            data.get("portfolio_url", "").strip(),
            data.get("bio", "").strip(),
            data.get("contact_email", "").strip(),
            1 if data.get("is_available", True) else 0,
            1 if data.get("is_demo") else 0,
        ))
        conn.commit()
        return cursor.lastrowid


def get_all_talent(
    include_demo: bool = True,
    experience: Optional[str] = None,
    search: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Retrieve talent profiles with optional filters."""
    query = "SELECT * FROM talent_profiles WHERE 1=1"
    params: List[Any] = []

    if not include_demo:
        query += " AND is_demo = 0"

    if experience and experience != "All Experience Levels":
        query += " AND experience_level = ?"
        params.append(experience)

    if search:
        query += " AND (full_name LIKE ? OR technical_skills LIKE ? OR institution LIKE ? OR areas_of_interest LIKE ?)"
        wildcard = f"%{search}%"
        params.extend([wildcard, wildcard, wildcard, wildcard])

    query += " ORDER BY id DESC"

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def delete_talent(talent_id: int) -> bool:
    """Delete a talent profile by ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM talent_profiles WHERE id = ?", (talent_id,))
        conn.commit()
        return cursor.rowcount > 0


# ==============================================================================
# INDUSTRY CHALLENGES CRUD
# ==============================================================================

def add_challenge(data: Dict[str, Any]) -> int:
    """Insert a new industry challenge."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO industry_challenges (
                title, organization_name, org_type, sector, district,
                problem_statement, expected_outcome, budget_range,
                urgency, status, contact_person, is_demo, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (
            data.get("title", "").strip(),
            data.get("organization_name", "").strip(),
            data.get("org_type", ""),
            data.get("sector", ""),
            data.get("district", ""),
            data.get("problem_statement", "").strip(),
            data.get("expected_outcome", "").strip(),
            data.get("budget_range", ""),
            data.get("urgency", ""),
            data.get("status", "Open for Proposals"),
            data.get("contact_person", "").strip(),
            1 if data.get("is_demo") else 0,
        ))
        conn.commit()
        return cursor.lastrowid


def get_all_challenges(
    include_demo: bool = True,
    sector: Optional[str] = None,
    urgency: Optional[str] = None,
    search: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Retrieve industry challenges with optional filters."""
    query = "SELECT * FROM industry_challenges WHERE 1=1"
    params: List[Any] = []

    if not include_demo:
        query += " AND is_demo = 0"

    if sector and sector != "All Sectors":
        query += " AND sector = ?"
        params.append(sector)

    if urgency and urgency != "All Urgencies":
        query += " AND urgency = ?"
        params.append(urgency)

    if search:
        query += " AND (title LIKE ? OR problem_statement LIKE ? OR organization_name LIKE ?)"
        wildcard = f"%{search}%"
        params.extend([wildcard, wildcard, wildcard])

    query += " ORDER BY id DESC"

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def update_challenge_status(challenge_id: int, new_status: str) -> bool:
    """Update challenge status."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE industry_challenges SET status = ? WHERE id = ?", (new_status, challenge_id))
        conn.commit()
        return cursor.rowcount > 0


# ==============================================================================
# OPPORTUNITY ASSESSMENTS CRUD
# ==============================================================================

def add_assessment(data: Dict[str, Any]) -> int:
    """Save an opportunity assessment."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO opportunity_assessments (
                idea_title, sector, problem_statement, overall_score,
                factor_breakdown_json, strengths_json, weaknesses_json,
                recommendations_json, risks_json, target_markets_json,
                is_demo, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (
            data.get("idea_title", "").strip(),
            data.get("sector", ""),
            data.get("problem_statement", "").strip(),
            float(data.get("overall_score", 0.0)),
            json.dumps(data.get("factor_breakdown", {})),
            json.dumps(data.get("strengths", [])),
            json.dumps(data.get("weaknesses", [])),
            json.dumps(data.get("recommendations", [])),
            json.dumps(data.get("risks", {})),
            json.dumps(data.get("target_markets", [])),
            1 if data.get("is_demo") else 0,
        ))
        conn.commit()
        return cursor.lastrowid


def get_all_assessments(include_demo: bool = True) -> List[Dict[str, Any]]:
    """Retrieve saved opportunity assessments."""
    query = "SELECT * FROM opportunity_assessments WHERE 1=1"
    params: List[Any] = []

    if not include_demo:
        query += " AND is_demo = 0"

    query += " ORDER BY id DESC"

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        result = []
        for r in rows:
            d = dict(r)
            d["factor_breakdown"] = json.loads(d.get("factor_breakdown_json") or "{}")
            d["strengths"] = json.loads(d.get("strengths_json") or "[]")
            d["weaknesses"] = json.loads(d.get("weaknesses_json") or "[]")
            d["recommendations"] = json.loads(d.get("recommendations_json") or "[]")
            d["risks"] = json.loads(d.get("risks_json") or "{}")
            d["target_markets"] = json.loads(d.get("target_markets_json") or "[]")
            result.append(d)
        return result


# ==============================================================================
# ECOSYSTEM STATS & MANAGEMENT
# ==============================================================================

def get_ecosystem_stats(include_demo: bool = True) -> Dict[str, Any]:
    """Calculate aggregated ecosystem metrics, distinguishing demo from real submissions."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Project counts (total, real, demo)
        cursor.execute("SELECT COUNT(*), SUM(CASE WHEN is_demo=1 THEN 1 ELSE 0 END), SUM(CASE WHEN is_demo=0 THEN 1 ELSE 0 END) FROM projects")
        p_row = cursor.fetchone()
        total_p = p_row[0] or 0
        demo_p = p_row[1] or 0
        real_p = p_row[2] or 0

        # Talent counts
        cursor.execute("SELECT COUNT(*), SUM(CASE WHEN is_demo=1 THEN 1 ELSE 0 END), SUM(CASE WHEN is_demo=0 THEN 1 ELSE 0 END) FROM talent_profiles")
        t_row = cursor.fetchone()
        total_t = t_row[0] or 0
        demo_t = t_row[1] or 0
        real_t = t_row[2] or 0

        # Challenge counts
        cursor.execute("SELECT COUNT(*), SUM(CASE WHEN is_demo=1 THEN 1 ELSE 0 END), SUM(CASE WHEN is_demo=0 THEN 1 ELSE 0 END) FROM industry_challenges")
        c_row = cursor.fetchone()
        total_c = c_row[0] or 0
        demo_c = c_row[1] or 0
        real_c = c_row[2] or 0

        # Assessment counts
        cursor.execute("SELECT COUNT(*), SUM(CASE WHEN is_demo=1 THEN 1 ELSE 0 END), SUM(CASE WHEN is_demo=0 THEN 1 ELSE 0 END) FROM opportunity_assessments")
        a_row = cursor.fetchone()
        total_a = a_row[0] or 0
        demo_a = a_row[1] or 0
        real_a = a_row[2] or 0

        # Filtered counts based on current setting
        active_projects = total_p if include_demo else real_p
        active_talent = total_t if include_demo else real_t
        active_challenges = total_c if include_demo else real_c
        active_assessments = total_a if include_demo else real_a

        # Average readiness score for active projects with score > 0
        filter_clause = "" if include_demo else "WHERE is_demo = 0"
        cursor.execute(f"SELECT AVG(readiness_score) FROM projects {filter_clause} {'AND' if filter_clause else 'WHERE'} readiness_score > 0")
        avg_readiness = cursor.fetchone()[0] or 0.0

        # Top sectors
        cursor.execute(f"SELECT sector, COUNT(*) as cnt FROM projects {filter_clause} GROUP BY sector ORDER BY cnt DESC")
        sector_dist = [dict(row) for row in cursor.fetchall()]

        # Stage distribution
        cursor.execute(f"SELECT stage, COUNT(*) as cnt FROM projects {filter_clause} GROUP BY stage ORDER BY cnt DESC")
        stage_dist = [dict(row) for row in cursor.fetchall()]

        return {
            "projects": active_projects,
            "real_projects": real_p,
            "demo_projects": demo_p,
            "talent": active_talent,
            "real_talent": real_t,
            "demo_talent": demo_t,
            "challenges": active_challenges,
            "real_challenges": real_c,
            "demo_challenges": demo_c,
            "assessments": active_assessments,
            "real_assessments": real_a,
            "demo_assessments": demo_a,
            "avg_readiness": round(float(avg_readiness), 1),
            "sector_distribution": sector_dist,
            "stage_distribution": stage_dist,
        }


def has_demo_data() -> bool:
    """Check if demo data is already seeded."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM projects WHERE is_demo = 1")
        count = cursor.fetchone()[0]
        return count > 0


def delete_all_demo_data() -> None:
    """Purge all demonstration entries from the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM projects WHERE is_demo = 1")
        cursor.execute("DELETE FROM talent_profiles WHERE is_demo = 1")
        cursor.execute("DELETE FROM industry_challenges WHERE is_demo = 1")
        cursor.execute("DELETE FROM opportunity_assessments WHERE is_demo = 1")
        conn.commit()


def reset_database() -> None:
    """Drop and recreate all tables."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS projects")
        cursor.execute("DROP TABLE IF EXISTS talent_profiles")
        cursor.execute("DROP TABLE IF EXISTS industry_challenges")
        cursor.execute("DROP TABLE IF EXISTS opportunity_assessments")
        cursor.execute("DROP TABLE IF EXISTS users")
        cursor.execute("DROP TABLE IF EXISTS auth_audit_logs")
        conn.commit()
    init_db()


# ==============================================================================
# USER & SECURITY AUDIT LOGGING
# ==============================================================================

def upsert_user(user_data: Dict[str, Any]) -> None:
    """Insert or update user record in local database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (
                uid, email, display_name, photo_url, role,
                email_verified, status, last_login_at, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            ON CONFLICT(uid) DO UPDATE SET
                email = excluded.email,
                display_name = excluded.display_name,
                photo_url = excluded.photo_url,
                role = excluded.role,
                last_login_at = CURRENT_TIMESTAMP
        """, (
            user_data.get("uid"),
            user_data.get("email", "").lower().strip(),
            user_data.get("display_name", "").strip(),
            user_data.get("photo_url", ""),
            user_data.get("role", "Innovator / Researcher"),
            1 if user_data.get("email_verified", True) else 0,
            user_data.get("status", "active"),
        ))
        conn.commit()


def get_user_by_uid(uid: str) -> Optional[Dict[str, Any]]:
    """Retrieve user record by Firebase UID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE uid = ?", (uid,))
        row = cursor.fetchone()
        return dict(row) if row else None


def update_user_role(uid: str, new_role: str) -> bool:
    """Update role for an existing user."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET role = ? WHERE uid = ?", (new_role, uid))
        conn.commit()
        return cursor.rowcount > 0


def log_audit_event(
    event_type: str,
    user_id: Optional[str] = None,
    email: Optional[str] = None,
    details: Optional[str] = None,
    status: str = "SUCCESS",
    ip_address: Optional[str] = None
) -> int:
    """Record a security audit log entry."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO auth_audit_logs (
                event_type, user_id, email, ip_address, details, status, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (
            event_type,
            user_id or "anonymous",
            email or "N/A",
            ip_address or "127.0.0.1",
            details or "",
            status
        ))
        conn.commit()
        return cursor.lastrowid


def get_recent_audit_logs(limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieve recent security audit logs."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM auth_audit_logs ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
