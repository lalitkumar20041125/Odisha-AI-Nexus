"""
PowerPoint Presentation Generator for Odisha AI Nexus.
Creates a widescreen 16:9 slide deck with custom dark navy/cyan branding,
embedded UI screenshots, formatted cards, and speaker notes.
Output: d:/ODISHA AI NEXUS/presentation/Odisha_AI_Nexus_Pitch_Deck.pptx
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# 16:9 Widescreen dimensions
SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

# Color Palette
COLOR_BG = RGBColor(11, 25, 46)        # Deep Navy #0B192E
COLOR_CARD = RGBColor(15, 33, 58)      # Card Navy #0F213A
COLOR_CYAN = RGBColor(0, 240, 255)     # Electric Cyan #00F0FF
COLOR_WHITE = RGBColor(255, 255, 255)  # White #FFFFFF
COLOR_SLATE = RGBColor(148, 163, 184)  # Slate Grey #94A3B8
COLOR_EMERALD = RGBColor(16, 185, 129) # Emerald #10B981
COLOR_AMBER = RGBColor(245, 158, 11)   # Amber #F59E0B

IMG_DIR = os.path.join(os.path.dirname(__file__), "presentation", "images")
OUTPUT_PPTX = os.path.join(os.path.dirname(__file__), "presentation", "Odisha_AI_Nexus_Pitch_Deck.pptx")


def set_slide_background(slide):
    """Fill slide with deep dark navy background."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_BG


def add_header(slide, title_text, subtitle_text):
    """Add a branded modern header to a slide."""
    txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p_title = tf.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = "Calibri"
    p_title.font.size = Pt(28)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_WHITE

    p_sub = tf.add_paragraph()
    p_sub.text = subtitle_text
    p_sub.font.name = "Calibri"
    p_sub.font.size = Pt(13)
    p_sub.font.color.rgb = COLOR_CYAN
    p_sub.space_before = Pt(4)


def add_speaker_notes(slide, notes_text):
    """Add speaker notes to slide for presenter view."""
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = notes_text


def build_presentation():
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: TITLE & VISION
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Accent decorative box
    accent_box = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.733), Inches(4.3))
    accent_box.fill.solid()
    accent_box.fill.fore_color.rgb = COLOR_CARD
    accent_box.line.color.rgb = COLOR_CYAN
    accent_box.line.width = Pt(1.5)

    tx1 = s1.shapes.add_textbox(Inches(1.2), Inches(2.1), Inches(11), Inches(3.6))
    tf1 = tx1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "⚡ ODISHA AI NEXUS"
    p.font.name = "Calibri"
    p.font.size = Pt(42)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    p = tf1.add_paragraph()
    p.text = "Local Innovation. Global Impact."
    p.font.name = "Calibri"
    p.font.size = Pt(24)
    p.font.color.rgb = COLOR_WHITE
    p.space_before = Pt(8)

    p = tf1.add_paragraph()
    p.text = "Unifying Odisha's 30 districts, premier academic institutes, heavy industries, and overseas markets on a 100% local, multilingual AI ecosystem platform."
    p.font.name = "Calibri"
    p.font.size = Pt(15)
    p.font.color.rgb = COLOR_SLATE
    p.space_before = Pt(18)

    # Badge indicators
    p = tf1.add_paragraph()
    p.text = "🌐 Tri-Lingual (English | ଓଡ଼ିଆ | हिन्दी)   •   🔒 100% Local SQLite / Zero Cloud   •   🎙️ Web Speech Voice AI"
    p.font.name = "Calibri"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD
    p.space_before = Pt(24)

    add_speaker_notes(s1, "Good morning, respected judges. Odisha is an industrial powerhouse with world-class technical institutes like IIT Bhubaneswar, NIT Rourkela, and VSSUT, alongside legendary disaster management leadership. Yet, its AI talent, university research, and heavy industries operate in disconnected silos. Today, we introduce Odisha AI Nexus — a fully functional, multilingual, and 100% local platform that bridges grassroots innovators across Odisha's 30 districts with regional challenges and global markets.")

    # =========================================================================
    # SLIDE 2: THE PROBLEM (REGIONAL PARADOX)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "The Regional Paradox: High Capability, Disconnected Silos", "Why Odisha's brightest tech innovations struggle to reach adoption and global scale")

    cards_data = [
        ("🎓 Academic Silos", "Student models at IIT, NIT, and VSSUT remain confined to college labs and GitHub repos, lacking exposure to local enterprise buyers.", COLOR_CYAN),
        ("🏭 Heavy Industry Bottlenecks", "Steel plants in Kalinganagar, mines in Keonjhar, and ports in Paradip face critical bottlenecks but lack access to local AI solvers.", COLOR_AMBER),
        ("🗣️ Linguistic Exclusion", "Standard AI platforms are 100% English-only, cutting off local artisans, farmers, and grassroots entrepreneurs who speak Odia or Hindi.", COLOR_EMERALD),
        ("🌐 The Export Vacuum", "Early-stage prototypes lack structured compliance frameworks (DPDP Act 2023, GDPR, Edge latency) to reach international buyers.", COLOR_CYAN),
    ]

    for idx, (head, desc, color) in enumerate(cards_data):
        col_left = Inches(0.8 + idx * 2.98)
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, col_left, Inches(1.8), Inches(2.8), Inches(4.8))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_CARD
        card.line.color.rgb = color
        card.line.width = Pt(1.5)

        tx = card.text_frame
        tx.word_wrap = True
        p = tx.paragraphs[0]
        p.text = head
        p.font.name = "Calibri"
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = color

        p = tx.add_paragraph()
        p.text = desc
        p.font.name = "Calibri"
        p.font.size = Pt(14)
        p.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(14)

    add_speaker_notes(s2, "Why do great student projects stay as college assignments while local industries look outside the state for solutions? Because there is no discovery bridge. Furthermore, language barriers keep non-English speakers out of the AI conversation. We set out to solve this fundamental gap.")

    # =========================================================================
    # SLIDE 3: EXECUTIVE PLATFORM OVERVIEW (WITH SCREENSHOT 1)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Executive Command Center & Responsive Analytics", "One unified discovery and decision-support layer for regional applied intelligence")

    # Image Left (16:9)
    img_path1 = os.path.join(IMG_DIR, "1_dashboard_overview.jpg")
    if os.path.exists(img_path1):
        s3.shapes.add_picture(img_path1, Inches(0.8), Inches(1.8), width=Inches(7.2))

    # Text Right
    tx3 = s3.shapes.add_textbox(Inches(8.3), Inches(1.8), Inches(4.3), Inches(5.0))
    tf3 = tx3.text_frame
    tf3.word_wrap = True

    p = tf3.paragraphs[0]
    p.text = "🎯 Core Capabilities"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    bullets3 = [
        "**Real-Time Ecosystem KPIs:** Instant counts of registered projects, verified talent, industry challenges, and global readiness.",
        "**De-Clustered Analytics:** Ranked horizontal bar chart eliminating label crowding across all 8 strategic economic sectors.",
        "**Verified vs. Demo Modes:** Clear toggle to isolate genuine verified submissions from seed baseline datasets.",
        "**Multi-Device Fluid Layout:** Responsive design tested on mobile phones, tablets, and desktop workstations."
    ]
    for b in bullets3:
        p = tf3.add_paragraph()
        p.text = "• " + b.replace("**", "")
        p.font.size = Pt(13)
        p.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(10)

    add_speaker_notes(s3, "As you can see on the screen, this is our live Executive Dashboard. It gives instant visibility into the state's AI assets. Notice the de-clustered sector analytics and verified project badges — all engineered to adapt smoothly across mobile, tablet, and PC screens.")

    # =========================================================================
    # SLIDE 4: GROUNDED REGIONAL USE CASES
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Culturally Grounded in Odisha's Strategic Sectors", "Solving genuine high-impact problems across the state's economic backbone")

    use_cases = [
        ("🌾 PaddyShield AI", "Bargarh / Western Odisha", "Edge-quantized CNN for early blast and planthopper detection in paddy fields, running offline on low-cost smartphones.", COLOR_EMERALD),
        ("🌊 CycloneEye Odisha", "Puri & Coastal Zone", "Physics-guided neural networks for storm surge height and inundation modeling using Doppler weather radar telemetry.", COLOR_CYAN),
        ("🏭 Kalinganagar Slag AI", "Jajpur Industrial Corridor", "Computer vision for high-temperature blast furnace slag foaming detection with sub-50ms latency for worker safety.", COLOR_AMBER),
        ("🧵 Sambalpuri Heritage AI", "Bargarh & Sonepur", "Authenticates traditional handloom weave geometry and provides immutable digital IP protection for weaver cooperatives.", COLOR_WHITE),
    ]

    for idx, (title, loc, desc, color) in enumerate(use_cases):
        row = idx // 2
        col = idx % 2
        box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + col * 5.9), Inches(1.8 + row * 2.5), Inches(5.6), Inches(2.2))
        box.fill.solid()
        box.fill.fore_color.rgb = COLOR_CARD
        box.line.color.rgb = color
        box.line.width = Pt(1.5)

        tx = box.text_frame
        tx.word_wrap = True
        p = tx.paragraphs[0]
        p.text = f"{title}  ({loc})"
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = color

        p = tx.add_paragraph()
        p.text = desc
        p.font.size = Pt(13)
        p.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(8)

    add_speaker_notes(s4, "Every demonstration project in our platform is culturally and economically grounded in Odisha's real challenges — from paddy pest mitigation in Bargarh to blast furnace safety in Kalinganagar and Sambalpuri handloom protection.")

    # =========================================================================
    # SLIDE 5: MULTILINGUAL & VOICE ACCESSIBILITY (WITH SCREENSHOT 2)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Inclusive Accessibility: Odia, Hindi & Web Speech Audio", "Breaking the digital divide for rural entrepreneurs, artisans, and non-English speakers")

    img_path2 = os.path.join(IMG_DIR, "2_multilingual_voice.jpg")
    if os.path.exists(img_path2):
        s5.shapes.add_picture(img_path2, Inches(0.8), Inches(1.8), width=Inches(7.2))

    tx5 = s5.shapes.add_textbox(Inches(8.3), Inches(1.8), Inches(4.3), Inches(5.0))
    tf5 = tx5.text_frame
    tf5.word_wrap = True

    p = tf5.paragraphs[0]
    p.text = "🗣️ Voice & Native Language"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    bullets5 = [
        "**Tri-Lingual Localization:** Full native script translation for English, Odia (ଓଡ଼ିଆ), and Hindi (हिन्दी) with authentic fonts (Noto Sans Oriya/Devanagari).",
        "**Web Speech Audio Reader (TTS):** Embedded browser narrator speaking page briefings aloud in Odia or Hindi with play/pause wave animation.",
        "**Voice Microphone Search (STT):** Tap the mic to speak search queries in Odia (or-IN) or Hindi (hi-IN) without typing English keywords.",
        "**Inclusive Grassroots Adoption:** Enables rural artisans and farmers to discover and utilize applied AI."
    ]
    for b in bullets5:
        p = tf5.add_paragraph()
        p.text = "• " + b.replace("**", "")
        p.font.size = Pt(13)
        p.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(10)

    add_speaker_notes(s5, "Not every innovator or beneficiary in Odisha communicates in English. We built native tri-lingual support and an interactive Web Speech companion. Users can listen to page briefings aloud in Odia or speak their search queries directly into the microphone.")

    # =========================================================================
    # SLIDE 6: OPPORTUNITY EXPLORER (WITH SCREENSHOT 3)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "AI Opportunity Explorer & 6-Factor Decision Support", "Transparent, explainable heuristic scoring to stress-test regional AI product viability")

    img_path3 = os.path.join(IMG_DIR, "3_opportunity_explorer.jpg")
    if os.path.exists(img_path3):
        s6.shapes.add_picture(img_path3, Inches(0.8), Inches(1.8), width=Inches(7.2))

    tx6 = s6.shapes.add_textbox(Inches(8.3), Inches(1.8), Inches(4.3), Inches(5.0))
    tf6 = tx6.text_frame
    tf6.word_wrap = True

    p = tf6.paragraphs[0]
    p.text = "📊 Transparent Intelligence"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    bullets6 = [
        "**Composite 0–100 Score Gauge:** Weighted multi-criteria decision analysis across technical, economic, and operational dimensions.",
        "**6-Factor Radar Polygon Chart:** Evaluates Feasibility, Relevance, Socio-Economic Impact, Global Potential, Budget, and Data Viability.",
        "**Actionable Diagnoses:** Automatically highlights identified strengths, operational blindspots, and missing telemetry.",
        "**Export Corridor Hypotheses:** Automatically links solutions to international target regions (e.g. ASEAN, Coastal Europe)."
    ]
    for b in bullets6:
        p = tf6.add_paragraph()
        p.text = "• " + b.replace("**", "")
        p.font.size = Pt(13)
        p.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(10)

    add_speaker_notes(s6, "We deliberately avoid black-box proprietary APIs that cost money and hallucinate. Our Opportunity Explorer uses transparent, weighted multi-criteria decision analysis. Innovators get a concrete 0-to-100 score, a 6-factor radar breakdown, identified blindspots, and target export corridors.")

    # =========================================================================
    # SLIDE 7: TALENT EXCHANGE & SYNERGY MATCHER (WITH SCREENSHOT 4)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Talent Exchange & Bidirectional Synergy Matcher", "Connecting 30 districts of students, ML engineers, and researchers with real projects")

    img_path4 = os.path.join(IMG_DIR, "4_talent_matcher.jpg")
    if os.path.exists(img_path4):
        s7.shapes.add_picture(img_path4, Inches(0.8), Inches(1.8), width=Inches(7.2))

    tx7 = s7.shapes.add_textbox(Inches(8.3), Inches(1.8), Inches(4.3), Inches(5.0))
    tf7 = tx7.text_frame
    tf7.word_wrap = True

    p = tf7.paragraphs[0]
    p.text = "👥 Privacy-First Matchmaking"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    bullets7 = [
        "**Privacy Safeguards:** Direct contact emails masked by default (s***@iitbbs.ac.in) to stop scraping while keeping portfolios accessible.",
        "**Mathematical Synergy Scoring:** Matches skills, domain affinity, and district proximity with explainable match reasons.",
        "**Bidirectional Perspective:** Pair projects with top researchers OR pair researchers with live industry challenges.",
        "**Cross-District Cohorts:** Connecting IIT Bhubaneswar, NIT Rourkela, and VSSUT with MSMEs in remote districts."
    ]
    for b in bullets7:
        p = tf7.add_paragraph()
        p.text = "• " + b.replace("**", "")
        p.font.size = Pt(13)
        p.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(10)

    add_speaker_notes(s7, "On the left, verified researcher profiles with masked emails for privacy protection. On the right, our automated AI Synergy Matcher pairing candidate skills with project requirements, complete with explainable matching reasons.")

    # =========================================================================
    # SLIDE 8: 100% LOCAL ARCHITECTURE & SECURITY
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "100% Local Autonomous Architecture & Tight Security", "Zero secondary cloud or Firebase lock-in; robust local cryptography and RBAC")

    sec_cards = [
        ("🔒 Zero Cloud Dependency", "100% local SQLite database running offline on personal hardware. Zero Firebase, zero external subscriptions. PostgreSQL-ready via psycopg2-binary.", COLOR_CYAN),
        ("🛡️ Tamper-Proof Sessions", "Sessions signed with internal HMAC-SHA256 tokens and sliding expiration. Modifying client claims triggers immediate cryptographic rejection.", COLOR_EMERALD),
        ("👥 Role-Based Access (RBAC)", "Strict authorization hierarchy: Guest, Talent, Innovator, Industry, and Admin with enforced granular permissions.", COLOR_AMBER),
        ("📋 Immutable Audit Trails", "Every sign-in, permission denial, and data update is recorded persistently in local SQLite auth_audit_logs for forensics.", COLOR_WHITE),
    ]

    for idx, (title, desc, color) in enumerate(sec_cards):
        col_left = Inches(0.8 + idx * 2.98)
        card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, col_left, Inches(1.8), Inches(2.8), Inches(4.8))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_CARD
        card.line.color.rgb = color
        card.line.width = Pt(1.5)

        tx = card.text_frame
        tx.word_wrap = True
        p = tx.paragraphs[0]
        p.text = title
        p.font.size = Pt(17)
        p.font.bold = True
        p.font.color.rgb = color

        p = tx.add_paragraph()
        p.text = desc
        p.font.size = Pt(13)
        p.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(14)

    add_speaker_notes(s8, "We engineered this system to run 100% on a laptop without requiring expensive cloud subscriptions or Firebase credentials. Even Google Sign-In is verified locally, backed by HMAC-SHA256 session signatures and persistent immutable audit logs.")

    # =========================================================================
    # SLIDE 9: GLOBAL EXPORT READINESS & REPORTING
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "10-Point Global Export Readiness & PDF Dossiers", "Guiding local innovations to international commercial readiness and compliance")

    box_left = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    box_left.fill.solid()
    box_left.fill.fore_color.rgb = COLOR_CARD
    box_left.line.color.rgb = COLOR_CYAN
    tx_l = box_left.text_frame
    tx_l.word_wrap = True
    p = tx_l.paragraphs[0]
    p.text = "📋 10-Point Global Readiness Framework"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    items_9 = [
        "Data Privacy: DPDP Act 2023 & GDPR compliance",
        "Explainability: SHAP/LIME feature attribution",
        "Edge / Offline Fit: Low latency under dust/intermittent network",
        "Multilingual UI: Odia, Hindi, English accessibility",
        "Security & Bias: OWASP LLM Top 10 + benchmark tests",
        "Export Packaging: Docker containers & CI/CD readiness"
    ]
    for it in items_9:
        p = tx_l.add_paragraph()
        p.text = "✓ " + it
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(8)

    box_right = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8))
    box_right.fill.solid()
    box_right.fill.fore_color.rgb = COLOR_CARD
    box_right.line.color.rgb = COLOR_EMERALD
    tx_r = box_right.text_frame
    tx_r.word_wrap = True
    p = tx_r.paragraphs[0]
    p.text = "📑 Executive Dossiers & Data Exports"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD

    items_r = [
        "One-Click PDF Dossiers: Multi-page executive intelligence briefings compiled via ReportLab with ecosystem stats.",
        "RFC 4180 CSV Exports: Download full datasets for projects, talent, challenges, and evaluations.",
        "Audit Snapshot Table: Complete breakdown of verified real user submissions vs demonstration data.",
        "Cross-Border Hypotheses: Mapping disaster tech to ASEAN and metallurgy AI to global industrial corridors."
    ]
    for it in items_r:
        p = tx_r.add_paragraph()
        p.text = "• " + it
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(8)

    add_speaker_notes(s9, "For investors and government leaders, the platform compiles publication-ready executive PDF dossiers in one click, diagnosing compliance gaps and mapping solutions directly to international markets like the Indo-Pacific and Southeast Asia.")

    # =========================================================================
    # SLIDE 10: ROADMAP & CONCLUSION
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Strategic Execution Roadmap & Pitch Conclusion", "Odisha AI Nexus: Empowering local talent to solve regional problems and create global impact")

    roadmap_items = [
        ("Phase 1: Core Platform Foundation", "COMPLETED", "Persistent SQLite architecture, Project Registry, Challenge Board, Opportunity Explorer, ReportLab PDF generation.", COLOR_EMERALD),
        ("Phase 2: Multilingual Odia & Hindi UI", "COMPLETED", "Native Odia and Hindi scripts, Web Speech audio narration companion, and voice microphone search.", COLOR_EMERALD),
        ("Phase 3: University Hackathons & MSME Pilots", "PLANNED (H2 2026)", "Onboarding engineering cohorts from IIT, NIT, VSSUT, and pairing them with local MSME challenges.", COLOR_CYAN),
        ("Phase 4: Open Public Hydrology & Satellite Telemetry", "PLANNED (2027)", "Integration with open data (ISRO Bhuvan satellite feeds, OSDMA sensors) for live model benchmarking.", COLOR_SLATE),
    ]

    for idx, (p_title, status, desc, color) in enumerate(roadmap_items):
        box = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8 + idx * 1.25), Inches(11.733), Inches(1.1))
        box.fill.solid()
        box.fill.fore_color.rgb = COLOR_CARD
        box.line.color.rgb = color
        box.line.width = Pt(1.5)

        tx = box.text_frame
        tx.word_wrap = True
        p = tx.paragraphs[0]
        p.text = f"{p_title}  —  [{status}]"
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = color

        p = tx.add_paragraph()
        p.text = desc
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(4)

    add_speaker_notes(s10, "Odisha AI Nexus is not just an idea — it is a production-tested, fully operational MVP with 37 passing unit tests, responsive UI across all devices, and genuine multilingual voice capabilities. We invite you to join us in powering Odisha's AI future. Thank you!")

    # Save presentation
    prs.save(OUTPUT_PPTX)
    print(f"Presentation generated successfully at: {OUTPUT_PPTX}")


if __name__ == "__main__":
    build_presentation()
