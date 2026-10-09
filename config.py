"""
Configuration and constants for Odisha AI Nexus.
Brand: Odisha AI Nexus
Tagline: Local Innovation. Global Impact.
"""

from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
DB_PATH = DATA_DIR / "odisha_ai_nexus.db"
REPORTS_DIR = DATA_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

# Brand details
APP_NAME = "Odisha AI Nexus"
TAGLINE = "Local Innovation. Global Impact."
APP_VERSION = "1.0.0-MVP"
COMMUNITY_DISCLAIMER = (
    "Odisha AI Nexus is an independent, community-driven ecosystem initiative. "
    "It is not officially affiliated with or endorsed by the Government of Odisha, "
    "Odisha AI Mission, or Startup Odisha. It does not provide guaranteed funding, "
    "legal certification, or official regulatory endorsements."
)

# Sectors relevant to Odisha
SECTORS = [
    "Agriculture & Food Security",
    "Disaster Management & Climate Resilience",
    "Mining & Mineral Exploration",
    "Steel & Heavy Metallurgy",
    "Logistics, Ports & Marine Economy",
    "Healthcare & Rural MedTech",
    "Tourism, Temple Tech & Heritage Preservation",
    "Education & Skilling (EdTech)",
    "Urban Governance & Smart Municipalities",
    "Handlooms, Handicrafts & MSME Artisans",
    "Energy, Renewable & Grid AI",
]

# Development Stages
PROJECT_STAGES = [
    "Ideation / Concept",
    "Proof of Concept (PoC)",
    "Working Prototype",
    "Field-Tested / Pilot",
    "Commercial MVP / Scaled",
]

# Project Statuses
PROJECT_STATUSES = [
    "Active",
    "Seeking Collaborators",
    "Seeking Pilot Partners",
    "Seeking Mentorship",
    "Completed / Operational",
]

# Odisha Districts (All 30 administrative districts)
ODISHA_DISTRICTS = [
    "Angul", "Balangir", "Balasore (Baleswar)", "Bargarh", "Bhadrak", "Boudh",
    "Cuttack", "Deogarh", "Dhenkanal", "Gajapati", "Ganjam", "Jagatsinghpur",
    "Jajpur", "Jharsuguda", "Kalahandi", "Kandhamal", "Kendrapara", "Kendujhar (Keonjhar)",
    "Khordha (Bhubaneswar)", "Koraput", "Malkangiri", "Mayurbhanj", "Nabarangpur",
    "Nayagarh", "Nuapada", "Puri", "Rayagada", "Sambalpur", "Subarnapur (Sonepur)", "Sundargarh (Rourkela)"
]

# Experience Levels for Talent
EXPERIENCE_LEVELS = [
    "Student / Fresher",
    "Junior (1-2 years)",
    "Mid-Level (3-5 years)",
    "Senior (5+ years)",
    "Lead / Architect",
    "Academic / Researcher / Faculty",
]

# Challenge Urgencies
CHALLENGE_URGENCIES = [
    "Critical / Immediate (< 1 month)",
    "High (1 - 3 months)",
    "Medium (3 - 6 months)",
    "Strategic / Long-term (6+ months)",
]

# Budget Ranges
BUDGET_RANGES = [
    "Community / Academic (Unfunded)",
    "Micro-grant (Up to ₹2 Lakhs)",
    "Seed / Pilot (₹2 - ₹10 Lakhs)",
    "Industry Scale (₹10 - ₹25 Lakhs)",
    "Enterprise / Institutional (₹25 Lakhs+)",
]

# Default Opportunity Scoring Weights (Sum to 100)
DEFAULT_SCORING_WEIGHTS = {
    "technical_feasibility": 20,
    "local_relevance": 20,
    "socio_economic_impact": 20,
    "global_market_potential": 15,
    "budget_resource_realism": 15,
    "data_regulatory_viability": 10,
}

# Color Theme Palette (Dark Navy + Cyan + Teal)
THEME = {
    "bg_dark": "#070E1E",
    "card_bg": "#0D1B2E",
    "card_border": "#1E3A5F",
    "accent_cyan": "#00F0FF",
    "accent_teal": "#14B8A6",
    "accent_emerald": "#10B981",
    "accent_amber": "#F59E0B",
    "accent_rose": "#F43F5E",
    "text_main": "#F8FAFC",
    "text_muted": "#94A3B8",
    "text_highlight": "#38BDF8",
}

# Local Database & Security Configuration
# By default, uses local zero-configuration SQLite at data/odisha_ai_nexus.db
# Can also connect to local PostgreSQL if DATABASE_URL environment variable is provided
DATABASE_URL = None  # None uses local SQLite DB_PATH

# Security & RBAC Roles
ROLES = {
    "ADMIN": "Admin",
    "INNOVATOR": "Innovator / Researcher",
    "INDUSTRY": "Industry Partner",
    "TALENT": "AI Talent / Student",
    "VIEWER": "Guest / Observer"
}

ROLE_PERMISSIONS = {
    "Admin": [
        "view_dashboard", "browse_projects", "create_project", "edit_any_project",
        "browse_talent", "register_talent", "browse_challenges", "create_challenge",
        "edit_any_challenge", "assess_opportunity", "audit_readiness", "export_reports",
        "purge_demo_data", "view_audit_logs", "manage_user_roles"
    ],
    "Innovator / Researcher": [
        "view_dashboard", "browse_projects", "create_project", "edit_own_project",
        "browse_talent", "register_talent", "browse_challenges", "assess_opportunity",
        "audit_readiness", "export_reports"
    ],
    "Industry Partner": [
        "view_dashboard", "browse_projects", "browse_talent", "browse_challenges",
        "create_challenge", "edit_own_challenge", "assess_opportunity", "audit_readiness",
        "export_reports"
    ],
    "AI Talent / Student": [
        "view_dashboard", "browse_projects", "browse_talent", "register_talent",
        "edit_own_talent", "browse_challenges", "assess_opportunity", "audit_readiness",
        "export_reports"
    ],
    "Guest / Observer": [
        "view_dashboard", "browse_projects", "browse_talent", "browse_challenges",
        "assess_opportunity", "audit_readiness", "export_reports"
    ]
}

SESSION_EXPIRY_SECONDS = 7200  # 2-hour rolling session window
