"""
Reporting and Data Export Module for Odisha AI Nexus.
Generates structured CSV exports and executive-grade PDF reports via ReportLab.
"""

import io
import csv
from datetime import datetime
from typing import List, Dict, Any, Optional

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
    HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

from config import APP_NAME, TAGLINE, COMMUNITY_DISCLAIMER


# ==============================================================================
# CSV EXPORT UTILITIES
# ==============================================================================

def export_projects_to_csv(projects: List[Dict[str, Any]]) -> str:
    """Generate CSV string of project registry."""
    output = io.StringIO()
    if not projects:
        return "No projects available to export."
    
    fieldnames = [
        "id", "title", "tagline", "sector", "stage", "lead_name",
        "organization", "district", "tech_stack", "status",
        "readiness_score", "is_demo", "created_at"
    ]
    writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    for p in projects:
        writer.writerow(p)
    return output.getvalue()


def export_talent_to_csv(talents: List[Dict[str, Any]]) -> str:
    """Generate CSV string of talent directory (with contact details masked)."""
    output = io.StringIO()
    if not talents:
        return "No talent profiles available to export."
    
    fieldnames = [
        "id", "full_name", "institution", "district", "role_title",
        "experience_level", "technical_skills", "areas_of_interest",
        "portfolio_url", "is_available", "is_demo", "created_at"
    ]
    writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    for t in talents:
        writer.writerow(t)
    return output.getvalue()


def export_challenges_to_csv(challenges: List[Dict[str, Any]]) -> str:
    """Generate CSV string of industry challenges."""
    output = io.StringIO()
    if not challenges:
        return "No industry challenges available to export."
    
    fieldnames = [
        "id", "title", "organization_name", "org_type", "sector",
        "district", "budget_range", "urgency", "status", "is_demo", "created_at"
    ]
    writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    for c in challenges:
        writer.writerow(c)
    return output.getvalue()


# ==============================================================================
# PDF GENERATION (ReportLab)
# ==============================================================================

def _get_custom_styles():
    """Create a cohesive, executive-styled palette for PDF reports."""
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0A192F"),
        alignment=TA_LEFT,
    )
    
    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#0D9488"),
        alignment=TA_LEFT,
    )
    
    heading2_style = ParagraphStyle(
        "ReportH2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#0A192F"),
        spaceBefore=10,
        spaceAfter=6,
    )
    
    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155"),
    )
    
    disclaimer_style = ParagraphStyle(
        "ReportDisclaimer",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#64748B"),
        alignment=TA_CENTER,
    )
    
    return {
        "title": title_style,
        "subtitle": subtitle_style,
        "h2": heading2_style,
        "body": body_style,
        "disclaimer": disclaimer_style,
    }


def generate_ecosystem_summary_pdf(
    stats: Dict[str, Any],
    top_projects: List[Dict[str, Any]],
    top_challenges: List[Dict[str, Any]],
    include_demo: bool = True
) -> bytes:
    """Generate an Executive Ecosystem Summary PDF document."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = _get_custom_styles()
    story = []
    
    # 1. Header Banner
    story.append(Paragraph(f"<b>{APP_NAME}</b>", styles["title"]))
    story.append(Paragraph(f"{TAGLINE} | Executive Ecosystem Briefing", styles["subtitle"]))
    story.append(Spacer(1, 4))
    
    meta_text = (
        f"<b>Generated:</b> {datetime.now().strftime('%d %B %Y, %H:%M')} | "
        f"<b>Data Filter:</b> {'All Records (Real + Demonstration Data)' if include_demo else 'Verified User Submissions Only'}"
    )
    story.append(Paragraph(meta_text, styles["body"]))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0D9488"), spaceAfter=12))

    # 2. Key Metrics Table
    story.append(Paragraph("<b>1. Key Ecosystem Metrics</b>", styles["h2"]))
    
    metrics_data = [
        [
            "Total AI Projects", f"{stats.get('projects', 0)} ({stats.get('real_projects', 0)} User / {stats.get('demo_projects', 0)} Demo)",
            "Registered AI Talent", f"{stats.get('talent', 0)} ({stats.get('real_talent', 0)} User / {stats.get('demo_talent', 0)} Demo)"
        ],
        [
            "Industry Challenges", f"{stats.get('challenges', 0)} ({stats.get('real_challenges', 0)} User / {stats.get('demo_challenges', 0)} Demo)",
            "Avg Export Readiness", f"{stats.get('avg_readiness', 0.0)}%"
        ],
    ]
    
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTNAME', (3, 0), (3, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor("#0F172A")),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
    ])
    
    t_metrics = Table(metrics_data, colWidths=[130, 130, 130, 130], style=table_style)
    story.append(t_metrics)
    story.append(Spacer(1, 10))

    # 3. Sector Distribution Table
    story.append(Paragraph("<b>2. Sectoral Project Distribution</b>", styles["h2"]))
    sector_dist = stats.get("sector_distribution", [])
    if sector_dist:
        s_table_data = [["Sector", "Project Count", "Share (%)"]]
        total_p = max(stats.get("projects", 1), 1)
        for s in sector_dist[:6]:
            share = round((s["cnt"] / total_p) * 100, 1)
            s_table_data.append([s["sector"], str(s["cnt"]), f"{share}%"])
        
        t_sec = Table(s_table_data, colWidths=[300, 110, 110])
        t_sec.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0A192F")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(t_sec)
    else:
        story.append(Paragraph("<i>No project records currently registered.</i>", styles["body"]))
    story.append(Spacer(1, 10))

    # 4. Highlighted AI Projects
    story.append(Paragraph("<b>3. Prominent Registered AI Solutions</b>", styles["h2"]))
    if top_projects:
        proj_data = [["Title & Organization", "Sector", "Stage", "Readiness", "Type"]]
        for p in top_projects[:5]:
            title_cell = f"<b>{p['title'][:32]}</b><br/>{p.get('organization', 'Independent')[:30]}"
            demo_badge = "DEMO" if p.get("is_demo") else "REAL"
            proj_data.append([
                Paragraph(title_cell, styles["body"]),
                Paragraph(p.get("sector", "")[:28], styles["body"]),
                p.get("stage", "")[:15],
                f"{p.get('readiness_score', 0)}%",
                demo_badge
            ])
        t_proj = Table(proj_data, colWidths=[200, 150, 90, 50, 40])
        t_proj.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0D9488")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(t_proj)
    else:
        story.append(Paragraph("<i>No projects available.</i>", styles["body"]))
    story.append(Spacer(1, 10))

    # 5. Open Industry Challenges
    story.append(Paragraph("<b>4. Active Industry Challenges Seeking AI Solutions</b>", styles["h2"]))
    if top_challenges:
        chal_data = [["Challenge & Organization", "Sector", "Urgency", "Budget"]]
        for c in top_challenges[:4]:
            c_title = f"<b>{c['title'][:35]}</b><br/>{c.get('organization_name', '')[:30]}"
            chal_data.append([
                Paragraph(c_title, styles["body"]),
                Paragraph(c.get("sector", "")[:26], styles["body"]),
                c.get("urgency", "")[:20],
                c.get("budget_range", "")[:18]
            ])
        t_chal = Table(chal_data, colWidths=[220, 140, 90, 80])
        t_chal.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E293B")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(t_chal)
    story.append(Spacer(1, 14))

    # 6. Disclaimer Footer
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#94A3B8"), spaceAfter=8))
    story.append(Paragraph(COMMUNITY_DISCLAIMER, styles["disclaimer"]))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def generate_opportunity_pdf(assessment: Dict[str, Any]) -> bytes:
    """Generate a formal Opportunity Assessment Briefing PDF."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    styles = _get_custom_styles()
    story = []

    # Title
    story.append(Paragraph(f"<b>AI Opportunity Assessment: {assessment.get('title', 'Untitled')}</b>", styles["title"]))
    story.append(Paragraph(f"Sector: {assessment.get('sector', 'N/A')} | Overall Feasibility & Impact Score: <b>{assessment.get('overall_score', 0)}/100</b>", styles["subtitle"]))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0D9488"), spaceAfter=10))

    # Problem Statement
    story.append(Paragraph("<b>Problem Statement & Regional Scope:</b>", styles["h2"]))
    story.append(Paragraph(assessment.get("problem_statement", "N/A"), styles["body"]))
    story.append(Spacer(1, 10))

    # Factor Breakdown Table
    story.append(Paragraph("<b>Heuristic Factor Breakdown:</b>", styles["h2"]))
    factors = assessment.get("factors", {})
    contributions = assessment.get("contributions", {})
    
    f_data = [["Evaluation Factor", "Factor Score (/100)", "Effective Weight", "Contribution Points"]]
    factor_labels = {
        "technical_feasibility": "Technical Feasibility & Architecture",
        "local_relevance": "Regional Relevance (Odisha Context)",
        "socio_economic_impact": "Socio-Economic Leverage & Impact",
        "global_market_potential": "Global Market & Export Potential",
        "budget_resource_realism": "Budget & Resource Feasibility",
        "data_regulatory_viability": "Data Readiness & Regulatory Fit",
    }
    for k, label in factor_labels.items():
        score_val = factors.get(k, 0)
        contrib_val = contributions.get(k, 0)
        weight_val = f"{assessment.get('weights', {}).get(k, 0)}%"
        f_data.append([label, f"{score_val}", weight_val, f"{contrib_val} pts"])
    
    t_f = Table(f_data, colWidths=[240, 100, 90, 100])
    t_f.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0A192F")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_f)
    story.append(Spacer(1, 10))

    # Strengths & Weaknesses
    story.append(Paragraph("<b>Identified Strengths & Structural Advantages:</b>", styles["h2"]))
    for s in assessment.get("strengths", []):
        story.append(Paragraph(f"• {s}", styles["body"]))
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Identified Gaps, Risks & Missing Elements:</b>", styles["h2"]))
    for w in assessment.get("weaknesses", []):
        story.append(Paragraph(f"• {w}", styles["body"]))
    story.append(Spacer(1, 10))

    # Actionable Next Steps
    story.append(Paragraph("<b>Recommended Next Milestones:</b>", styles["h2"]))
    for r in assessment.get("recommendations", []):
        story.append(Paragraph(f"• {r}", styles["body"]))
    story.append(Spacer(1, 12))

    # Disclaimer
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#94A3B8"), spaceAfter=6))
    story.append(Paragraph(assessment.get("disclaimer", COMMUNITY_DISCLAIMER), styles["disclaimer"]))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
