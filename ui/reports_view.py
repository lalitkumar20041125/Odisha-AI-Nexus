"""
Reports and Data Export View for Odisha AI Nexus.
Enables instant generation and download of CSV datasets and executive PDF briefings.
Fully localized for English, Odia (ଓଡ଼ିଆ), and Hindi (हिन्दी) with voice audio companion.
"""

import streamlit as st
from database import (
    get_ecosystem_stats,
    get_all_projects,
    get_all_challenges,
    get_all_talent,
    get_all_assessments
)
from reports import (
    export_projects_to_csv,
    export_talent_to_csv,
    export_challenges_to_csv,
    generate_ecosystem_summary_pdf
)
from i18n import t, get_current_language
from ui.voice_widget import render_voice_companion


def render_reports_view(include_demo: bool):
    """Render the Reports and Data Export center."""
    lang = get_current_language()

    # Header
    st.markdown(f"""
    <div style="margin-bottom: 12px;">
        <h2 style="color: #FFFFFF; font-weight: 800; margin-bottom: 4px;">{t("reports_heading")}</h2>
        <div style="color: #94A3B8; font-size: 0.95rem;">
            {t("reports_subheading")}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Voice Accessibility Companion
    render_voice_companion(
        section_key="reports",
        custom_text={
            "en": "This is the Reports and Data Export center. You can generate publication-ready PDF briefings and download complete CSV datasets for research and analytical reporting.",
            "or": "ଏହା ହେଉଛି ରିପୋର୍ଟ ଏବଂ ଡାଟା ରପ୍ତାନି କେନ୍ଦ୍ର । ଏଠାରେ ଆପଣ କାର୍ଯ୍ୟନିର୍ବାହୀ PDF ରିପୋର୍ଟ ଏବଂ ସମ୍ପୂର୍ଣ୍ଣ CSV ଡାଟା ଡାଉନଲୋଡ୍ କରିପାରିବେ ।",
            "hi": "यह रिपोर्ट एवं डेटा निर्यात केंद्र है। यहाँ आप प्रकाशन-योग्य PDF ब्रीफिंग और पूर्ण CSV डेटा डाउनलोड कर सकते हैं।"
        }.get(lang)
    )

    # Executive PDF Dossier Card
    dossier_title = {
        "en": "📑 Executive Ecosystem Summary Briefing (PDF)",
        "or": "📑 କାର୍ଯ୍ୟନିର୍ବାହୀ ଇକୋସିଷ୍ଟମ୍ ସାରାଂଶ ରିପୋର୍ଟ (PDF)",
        "hi": "📑 कार्यकारी इकोसिस्टम सारांश रिपोर्ट (PDF)"
    }.get(lang, "Executive Summary Briefing (PDF)")

    dossier_desc = {
        "en": "Comprehensive report compiling ecosystem KPIs, sector distributions, top-ranked AI solutions, active industry challenges, and governance disclaimers.",
        "or": "ଇକୋସିଷ୍ଟମ୍ ସୂଚକାଙ୍କ, କ୍ଷେତ୍ର ବଣ୍ଟନ, ଶ୍ରେଷ୍ଠ AI ସମାଧାନ ଏବଂ ସକ୍ରିୟ ଶିଳ୍ପ ସମସ୍ୟା ଧାରଣ କରିଥିବା ସମ୍ପୂର୍ଣ୍ଣ ରିପୋର୍ଟ ।",
        "hi": "इकोसिस्टम संकेतक, क्षेत्र वितरण, शीर्ष AI समाधान और सक्रिय उद्योग चुनौतियों को संकलित करने वाली व्यापक रिपोर्ट।"
    }.get(lang, "Comprehensive report compiling ecosystem KPIs.")

    st.markdown(f"""
    <div class="nexus-card" style="border-color: rgba(0, 240, 255, 0.4); background: linear-gradient(135deg, rgba(13, 27, 46, 0.9) 0%, rgba(10, 35, 60, 0.9) 100%);">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="font-size: 1.3rem; font-weight: 800; color: #FFFFFF;">{dossier_title}</span>
                <div style="color: #00F0FF; font-size: 0.88rem; margin-top: 4px;">
                    {dossier_desc}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Fetch fresh data
    stats = get_ecosystem_stats(include_demo=include_demo)
    projects = get_all_projects(include_demo=include_demo)
    challenges = get_all_challenges(include_demo=include_demo)
    talents = get_all_talent(include_demo=include_demo)

    try:
        pdf_bytes = generate_ecosystem_summary_pdf(
            stats=stats,
            top_projects=projects[:6],
            top_challenges=challenges[:4],
            include_demo=include_demo
        )

        scope_label = "all_data" if include_demo else "verified_user_only"
        st.download_button(
            label="📥 " + t("download_pdf"),
            data=pdf_bytes,
            file_name=f"odisha_ai_nexus_ecosystem_brief_{scope_label}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Error compiling PDF report: {e}")

    st.write("")
    st.divider()

    # Raw CSV Exports Grid
    csv_header = {
        "en": "### 💾 Raw Tabular Data Exports (CSV)",
        "or": "### 💾 ସିଧାସଳଖ ଟେବୁଲାର୍ ଡାଟା ରପ୍ତାନି (CSV)",
        "hi": "### 💾 प्रत्यक्ष सारणीबद्ध डेटा निर्यात (CSV)"
    }.get(lang, "CSV Exports")
    st.markdown(csv_header)

    c1, c2, c3 = st.columns(3)

    with c1:
        csv_p = export_projects_to_csv(projects)
        st.markdown(f"""
        <div class="nexus-card">
            <div style="font-weight: 700; color: #FFFFFF; font-size: 1rem;">🚀 {t('kpi_projects')}</div>
            <div style="font-size: 0.82rem; color: #94A3B8; margin: 4px 0 10px 0;">{len(projects)} records</div>
        </div>
        """, unsafe_allow_html=True)
        st.download_button(
            label="📥 " + t("export_csv") + f" ({t('kpi_projects')})",
            data=csv_p,
            file_name="odisha_ai_projects_registry.csv",
            mime="text/csv",
            use_container_width=True
        )

    with c2:
        csv_t = export_talent_to_csv(talents)
        st.markdown(f"""
        <div class="nexus-card">
            <div style="font-weight: 700; color: #FFFFFF; font-size: 1rem;">👥 {t('kpi_talent')}</div>
            <div style="font-size: 0.82rem; color: #94A3B8; margin: 4px 0 10px 0;">{len(talents)} records (emails masked)</div>
        </div>
        """, unsafe_allow_html=True)
        st.download_button(
            label="📥 " + t("export_csv") + f" ({t('kpi_talent')})",
            data=csv_t,
            file_name="odisha_ai_talent_directory.csv",
            mime="text/csv",
            use_container_width=True
        )

    with c3:
        csv_c = export_challenges_to_csv(challenges)
        st.markdown(f"""
        <div class="nexus-card">
            <div style="font-weight: 700; color: #FFFFFF; font-size: 1rem;">🏭 {t('kpi_challenges')}</div>
            <div style="font-size: 0.82rem; color: #94A3B8; margin: 4px 0 10px 0;">{len(challenges)} records</div>
        </div>
        """, unsafe_allow_html=True)
        st.download_button(
            label="📥 " + t("export_csv") + f" ({t('kpi_challenges')})",
            data=csv_c,
            file_name="odisha_ai_industry_challenges.csv",
            mime="text/csv",
            use_container_width=True
        )

    st.write("")
    st.divider()

    # Ecosystem Audit Summary Table
    table_header = {
        "en": "### 📋 Ecosystem Snapshot Table",
        "or": "### 📋 ଇକୋସିଷ୍ଟମ୍ ସ୍ଥିତି ସାରଣୀ",
        "hi": "### 📋 इकोसिस्टम स्थिति सारणी"
    }.get(lang, "Snapshot Table")
    st.markdown(table_header)

    snapshot_data = [
        {"Category": t("kpi_projects"), "Active Count": stats['projects'], "User Submissions": stats['real_projects'], "Demo Records": stats['demo_projects']},
        {"Category": t("kpi_talent"), "Active Count": stats['talent'], "User Submissions": stats['real_talent'], "Demo Records": stats['demo_talent']},
        {"Category": t("kpi_challenges"), "Active Count": stats['challenges'], "User Submissions": stats['real_challenges'], "Demo Records": stats['demo_challenges']},
        {"Category": t("nav_opportunity"), "Active Count": stats['assessments'], "User Submissions": stats['real_assessments'], "Demo Records": stats['demo_assessments']},
    ]
    st.dataframe(snapshot_data, use_container_width=True)
