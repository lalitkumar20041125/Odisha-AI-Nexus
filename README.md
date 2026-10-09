# Odisha AI Nexus (ଓଡ଼ିଶା AI ନେକ୍ସସ୍)
> **Tagline:** *Local Innovation. Global Impact.*  
> **Mission:** A practical, unified open ecosystem platform connecting students, researchers, startups, and industries across Odisha's 30 districts to build, validate, and export artificial intelligence solutions.

---

## ⚖️ Transparency & Independent Community Disclaimer
**Odisha AI Nexus** is an independent, community-driven digital ecosystem initiative. It is **not** officially affiliated with, endorsed by, or operated by the Government of Odisha, the Odisha AI Mission, or Startup Odisha. It does not provide official government grants, guaranteed institutional funding, or statutory compliance certifications. It operates as an open discovery, benchmarking, and collaboration sandbox designed to complement state and academic efforts.

---

## 🌟 Key Application Features

1. **Executive Dashboard (`ui/dashboard_view.py`)**
   - High-level ecosystem health metrics: Total projects, registered talent, open industry challenges, and average export readiness score.
   - Interactive Plotly visualizations: Sectoral project distribution donut chart and development stage maturity bar chart.
   - Promising AI solutions ranked by global readiness.
   - High-priority industry challenges awaiting engineering teams.
   - Transparent separation of verified user submissions from seed demonstration data.

2. **AI Project Registry (`ui/projects_view.py`)**
   - Browse, search (by keyword, title, or tech stack), and filter (by sector, status, and stage) active AI projects across Odisha.
   - Submit new AI solutions with full validation and persistent SQLite storage.
   - Inline status updates (e.g., transition from *Seeking Collaborators* to *Seeking Pilot Partners*).
   - Instant CSV data export of filtered project records.

3. **AI Opportunity Explorer (`ui/opportunity_view.py`)**
   - Heuristic multi-criteria decision-support algorithm evaluating concepts on a **0–100 scale**.
   - Assesses 6 dimensions: Technical Feasibility, Regional Relevance to Odisha, Socio-Economic Leverage, Global Export Potential, Budget Realism, and Data Availability/Regulatory Fit.
   - Interactive radar/polar chart showing factor balance.
   - Generates strengths, operational blindspots, multidimensional risk matrix (Technical, Financial, Operational, Adoption), and prospective target international markets.
   - Permanent local database persistence and one-click downloadable ReportLab PDF briefing.

4. **Odisha AI Talent Exchange (`ui/talent_view.py`)**
   - Community directory of ML researchers, students, and engineers from IIT Bhubaneswar, NIT Rourkela, IIIT, VSSUT, KIIT, SOA, Utkal University, and industry firms.
   - **Privacy Safeguard:** Direct contact emails are masked (`a***l@domain.com`) to prevent scraping.
   - **Bidirectional AI Synergy Matcher:** Matches talent skills with project tech stacks (or projects to talent profiles) using normalized token overlap and domain affinity, providing human-readable explanations (*"Why this match?"*).

5. **Industry Challenge Board (`ui/challenges_view.py`)**
   - Structured board for PSUs, steel manufacturers, MSMEs, municipal bodies, and cooperatives to publish real operational bottlenecks (e.g., blast furnace slag carry-over, river basin flash floods, raw cashew defect sorting).
   - Browse by urgency, budget range, and sector.
   - Interactive submission form for new enterprise challenges.

6. **Global Market Readiness (`ui/readiness_view.py`)**
   - 10-point comprehensive export checklist covering working prototypes, ROI metrics, SLA testing, data privacy (DPDP/GDPR), API documentation, localization, international pricing, and EU AI Act / regulatory risk.
   - Interactive export readiness score (0–100%) with category breakdown.
   - Persistence back to project records in local database.
   - International Market Corridor hypotheses tailored by sector (e.g., ASEAN rice belts, Bay of Bengal coastal nations, GCC maritime ports, Western European ethical fashion).

7. **Reports & Data Export Center (`ui/reports_view.py`)**
   - One-click executive PDF report compilation via **ReportLab**, featuring headers, KPI tables, sector breakdowns, project spotlights, and compliance notices.
   - RFC 4180 CSV exports for projects, talent directories, and industry challenges.
   - Saved opportunity assessment dossier re-downloads.

8. **Google Login & Tight Local Security (`auth_service.py`, `security.py`, `ui/auth_view.py`)**
   - **100% Local Execution:** No secondary external cloud services or Firebase required.
   - **Google Identity Integration:** Sign in with Google with token cryptographic verification and local verified identities.
   - **Tamper-Evident HMAC-SHA256 Sessions:** Cryptographically signed session tokens prevent client-side privilege escalation.
   - **Role-Based Access Control (RBAC):** Admin, Innovator / Researcher, Industry Partner, AI Talent / Student, and Guest Viewer permissions.
   - **Security Audit Trail:** Persistent `auth_audit_logs` tracking all logins, logouts, permission denials, and data mutations.

9. **About & Strategic Roadmap (`ui/about_view.py`)**
   - Detailed rationale, 5-phase strategic execution roadmap (Foundation -> Ecosystem Growth -> Data Integration -> Global Expansion -> Responsible AI), and privacy/governance disclosures.

---

## 💻 Tech Stack & Architecture

- **Language:** Python 3.11+ (Tested on Python 3.12)
- **Web Interface:** Streamlit (Custom Dark Navy + Cyber Cyan aesthetic)
- **Data Persistence:** 100% Local Database (Embedded SQLite3 at `data/odisha_ai_nexus.db` with zero configuration; optional local PostgreSQL support via `psycopg2-binary`)
- **Security & Auth:** HMAC-SHA256 cryptographic session engine + Google OAuth verification + RBAC permission system
- **Data Manipulation:** Pandas & NumPy
- **Interactive Visualizations:** Plotly Express & Plotly Graph Objects
- **Document Generation:** ReportLab 5.x (Platypus flowables, custom styled tables, PDF export)
- **Zero Cloud Dependencies:** Operates completely offline/locally without secondary cloud accounts or API subscriptions.

---

## 📁 Repository Structure

```
d:/ODISHA AI NEXUS/
├── app.py                      # Main Streamlit application entrypoint & router
├── config.py                   # App configuration, theme tokens, sectors, districts, scoring weights
├── database.py                 # Local database schema, queries, CRUD functions, demo data tagging
├── auth_service.py             # Local Google OAuth token verification & identity service
├── security.py                 # Cryptographic HMAC session tokens, RBAC, and audit logging
├── seed_data.py                # Realistic seed demonstration dataset for Odisha
├── scoring.py                  # Opportunity Explorer scoring engine & risk analyzer
├── matching.py                 # Talent-to-project matching engine & privacy masking
├── readiness.py                # Global Market Readiness evaluator & market corridor mapper
├── reports.py                  # ReportLab PDF compiler & CSV export utilities
├── ui/
│   ├── __init__.py
│   ├── styles.py               # Custom Dark Navy (#0B192E) + Cyan (#00F0FF) CSS
│   ├── auth_view.py            # Google Sign-In widget & local security center
│   ├── dashboard_view.py       # Executive Dashboard
│   ├── projects_view.py        # Project Registry
│   ├── opportunity_view.py     # AI Opportunity Explorer
│   ├── talent_view.py          # Talent Exchange & Matcher
│   ├── challenges_view.py      # Industry Challenge Board
│   ├── readiness_view.py       # Global Market Readiness
│   ├── reports_view.py         # Reports & Data Export Center
│   └── about_view.py           # Mission, Roadmap & Governance
├── tests/
│   ├── __init__.py
│   ├── test_database.py        # Database CRUD, filtering, demo separation tests
│   ├── test_security.py        # Cryptographic HMAC sessions, RBAC, and audit tests
│   ├── test_scoring.py         # Opportunity scoring bounds & weight consistency tests
│   ├── test_matching.py        # Talent matching & privacy masking tests
│   ├── test_readiness.py       # Checklist & market corridor evaluation tests
│   └── test_reports.py         # CSV & PDF generation verification tests
├── data/
│   └── odisha_ai_nexus.db      # SQLite database (auto-generated locally on first run)
├── requirements.txt            # Python dependencies
└── README.md                   # Complete documentation
```

---

## 🚀 Installation & Local Launch

### 1. Prerequisites
- Python 3.11 or later installed.
- Git (optional, for cloning).

### 2. Clone or Navigate to Directory
```bash
cd "d:/ODISHA AI NEXUS"
```

### 3. Create a Virtual Environment (Recommended)
```bash
python -m venv venv

# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# On macOS/Linux:
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Launch the Streamlit Application
```bash
streamlit run app.py
```
The application will launch automatically in your default browser at `http://localhost:8501`.

---

## 🧪 Automated Testing

Odisha AI Nexus includes an automated test suite covering database transactions, heuristic scoring engines, talent matching algorithms, and PDF compiling.

Run all tests via Python's built-in `unittest`:
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

All 22 test suites verify:
- Database initialization, foreign table constraints, and idempotent seeding.
- User record insertion vs demo record isolation.
- Opportunity scoring boundaries (0–100) and weighted sum consistency.
- Talent matching explanations and email privacy masking.
- Readiness checklist calculations and gap detection.
- CSV serialization and ReportLab PDF document compilation.

---

## 🎛️ Demonstration Data vs User Submissions

The platform includes seed records representing real-world Odisha scenarios (e.g. Cyclone evacuation routing in Ganjam, Brown Plant Hopper vision detection in Sambalpur, Kalinganagar slag detection, Sambalpuri Ikat pattern authentication).

- **Data Scope Controller:** Toggle between **All Records (Demo + Real)** and **Verified Submissions Only** in the left sidebar at any time.
- **Visual Badges:** Every record displays an amber `[DEMO]` badge or an emerald `[VERIFIED SUBMISSION]` badge.
- **Database Tools:** The sidebar expander allows one-click **Purge Demo** (to test empty or real-only workflows) and **Re-Seed Demo** (to restore demonstration data).

---

## 📝 Example Submissions

### 1. Registering an AI Project
- **Title:** `SmartBlast AI: Open-Cast Vibration & Haulage Optimizer`
- **Tagline:** `Reinforcement learning minimizing diesel burn and blasting vibrations in Talcher coalfields`
- **Sector:** `Mining & Mineral Exploration`
- **Stage:** `Proof of Concept (PoC)`
- **Lead Innovator:** `Siddharth Patnaik`
- **Organization:** `NIT Rourkela / Mining Tech Labs`
- **District:** `Angul`
- **Tech Stack:** `PyTorch, Ray RLlib, GeoPandas, MQTT, Docker`
- **Target Beneficiaries:** `Mining leaseholders and heavy fleet operators`

### 2. Submitting an Industry Challenge
- **Organization:** `Ganjam Agro-Processors & Exporters Association`
- **Org Type:** `MSME / Local Industry`
- **Sector:** `Agriculture & Food Security`
- **District:** `Ganjam`
- **Challenge Title:** `Automated Optical Sorting for Raw Cashew Kernel Defects`
- **Problem Statement:** `Manual grading across 80+ micro-processing units leads to inconsistent kernel outturn ratio (KOR) estimation. Dust and high ambient heat cause human fatigue.`
- **Expected Outcome:** `A smartphone app or optical conveyor unit classifying defect probability with 90%+ accuracy under sunlight.`
- **Budget Range:** `Micro-grant (Up to ₹2 Lakhs)`
- **Urgency:** `High (1 - 3 months)`

---

## 🌐 Deployment to Streamlit Community Cloud

To deploy Odisha AI Nexus publicly for community evaluation:
1. Push this repository to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit of Odisha AI Nexus MVP"
   git branch -M main
   git remote add origin https://github.com/your-username/odisha-ai-nexus.git
   git push -u origin main
   ```
2. Visit [share.streamlit.io](https://share.streamlit.io/) and log in with GitHub.
3. Click **New app**, select your repository, set the branch to `main`, and main file path to `app.py`.
4. Click **Deploy**. The application requires no external secrets or environment variables to run in its baseline MVP form.

---

## 🔒 Security, Privacy & Known Limitations

1. **Authentication:** The current MVP does not implement multi-tenant user authentication or passwords. It is designed for transparent community discovery. Avoid submitting classified industrial intellectual property or commercially sensitive confidential data.
2. **Contact Privacy:** Direct email addresses in the Talent Directory are masked on the client view.
3. **Algorithm Scope:** The Opportunity Explorer and Global Readiness scores are structured heuristic decision-support benchmarks. They are not legal opinions or scientifically validated venture outcomes.
4. **Environment Variables:** For future LLM integrations, place API keys into `.env` or Streamlit secrets (`secrets.toml`), never in source control.

---

## 🗺️ Future Integration Roadmap

- **Phase 1 (Completed):** Core SQLite MVP, Project Registry, Talent Directory, Challenge Board, Opportunity Explorer, Readiness Checklist, and PDF/CSV Export.
- **Phase 2 (H2 2026):** University student hackathon pilots and direct collaboration with incubation hubs.
- **Phase 3 (2027):** Automated integration with open government datasets (e.g. data.gov.in, ISRO Bhuvan satellite radar data, OSDMA flood telemetry).
- **Phase 4 (2027):** Multilingual Odia language interface, localized voice interaction for rural farmers, and overseas pilot matching with Indo-Pacific buyers.
- **Phase 5 (2028):** Responsible AI bias benchmarking, green AI carbon accounting, and verified contributor credentialing.
