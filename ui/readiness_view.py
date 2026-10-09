"""
Global Market Readiness View for Odisha AI Nexus.
Interactive 10-point checklist, export maturity scoring, regulatory risk evaluation,
and international market corridor hypotheses.
Fully localized for English, Odia (ଓଡ଼ିଆ), and Hindi (हिन्दी) with voice audio companion.
"""

import streamlit as st
import plotly.express as px
import pandas as pd

from database import get_all_projects, update_project_readiness
from readiness import READINESS_CHECKLIST, evaluate_readiness
from config import SECTORS
from i18n import t, t_sector, t_checklist, get_current_language
from ui.voice_widget import render_voice_companion


def render_readiness_view(include_demo: bool):
    """Render the Global Market Readiness diagnostic interface."""
    lang = get_current_language()

    # Header
    st.markdown(f"""
    <div style="margin-bottom: 12px;">
        <h2 style="color: #FFFFFF; font-weight: 800; margin-bottom: 4px;">{t("readiness_heading")}</h2>
        <div style="color: #94A3B8; font-size: 0.95rem;">
            {t("readiness_subheading")}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Voice Accessibility Companion
    render_voice_companion(section_key="readiness")

    # Disclaimer
    disclaimer_html = {
        "en": """
        <div class="disclaimer-box">
            ⚖️ <b>Self-Assessment Diagnostic:</b> A high readiness score is a technical self-audit benchmark, 
            <b>not</b> legal certification (e.g. CE Mark, FDA 510(k), HIPAA BAA) or guaranteed international commercial success.
        </div>
        """,
        "or": """
        <div class="disclaimer-box">
            ⚖️ <b>ସ୍ୱୟଂ-ମୂଲ୍ୟାଙ୍କନ ନିର୍ଣ୍ଣୟ:</b> ଏହି ସ୍କୋର ଏକ ବୈଷୟିକ ସ୍ୱୟଂ-ଅଡିଟ୍ ମାନଦଣ୍ଡ ଅଟେ, କୌଣସି ଆଇନଗତ ପ୍ରମାଣପତ୍ର କିମ୍ବା ବାଣିଜ୍ୟିକ ସଫଳତାର ପ୍ରତିଶ୍ରୁତି ନୁହେଁ ।
        </div>
        """,
        "hi": """
        <div class="disclaimer-box">
            ⚖️ <b>स्व-मूल्यांकन नैदानिक उपकरण:</b> यह स्कोर एक तकनीकी स्व-ऑडिट बेंचमार्क है, कोई कानूनी प्रमाणन या व्यावसायिक सफलता की गारंटी नहीं है।
        </div>
        """
    }.get(lang, "")
    st.markdown(disclaimer_html, unsafe_allow_html=True)

    # Project selection or standalone audit
    projects = get_all_projects(include_demo=include_demo)
    
    col_p1, col_p2 = st.columns([2, 1.5])
    with col_p1:
        standalone_lbl = {"en": "-- Standalone Custom Diagnostic --", "or": "-- ସ୍ୱତନ୍ତ୍ର ପରୀକ୍ଷଣ (Standalone) --", "hi": "-- स्वतंत्र कस्टम मूल्यांकन --"}.get(lang, "Standalone Diagnostic")
        proj_options = [standalone_lbl] + [f"{p['title']} (#{p['id']})" for p in projects]
        selected_option = st.selectbox(
            {"en": "Select Project to Audit:", "or": "ଅଡିଟ୍ ପାଇଁ ପ୍ରକଳ୍ପ ଚୟନ କରନ୍ତୁ:", "hi": "ऑडिट हेतु प्रोजेक्ट चुनें:"}.get(lang, "Select Project:"),
            proj_options
        )

    selected_project = None
    if selected_option != standalone_lbl:
        selected_id = int(selected_option.split("(#")[-1].replace(")", ""))
        selected_project = next((p for p in projects if p["id"] == selected_id), None)

    with col_p2:
        default_sector = selected_project["sector"] if selected_project else SECTORS[0]
        sec_map = {t_sector(s): s for s in SECTORS}
        chosen_sec_label = st.selectbox(
            t("filter_sector"),
            list(sec_map.keys()),
            index=list(sec_map.values()).index(default_sector) if default_sector in sec_map.values() else 0
        )
        chosen_sector = sec_map[chosen_sec_label]

    st.write("")
    st.markdown(f"### {t('checklist_title')}")
    st.caption({"en": "Check each milestone that is currently documented, tested, and implemented in your product.",
                "or": "ଆପଣଙ୍କ ଉତ୍ପାଦରେ କାର୍ଯ୍ୟକାରୀ ହୋଇଥିବା ପ୍ରତ୍ୟେକ ବିନ୍ଦୁ ଉପରେ ଟିକ୍ ଚିହ୍ନ ଦିଅନ୍ତୁ ।",
                "hi": "अपने उत्पाद में कार्यान्वित प्रत्येक बिंदु की जांच करें और टिक करें।"}.get(lang, "Check milestones."))

    # Render checklist items with full Odia/Hindi translation
    completed_items = []
    categories = list(dict.fromkeys(item["category"] for item in READINESS_CHECKLIST))
    
    for cat in categories:
        st.markdown(f"##### 🏷️ {cat}")
        cat_items = [item for item in READINESS_CHECKLIST if item["category"] == cat]
        for item in cat_items:
            translated_desc = t_checklist(item["id"], f"{item['title']}: {item['description']}")
            checked = st.checkbox(
                f"{item['title']}: {translated_desc}",
                key=f"chk_{item['id']}"
            )
            if checked:
                completed_items.append(item["id"])

    st.write("")
    results = evaluate_readiness(completed_items, chosen_sector)
    readiness_score = results["score"]

    # Visual Score Banner
    st.divider()
    col_sc1, col_sc2 = st.columns([1, 2])

    with col_sc1:
        color = "#10B981" if readiness_score >= 80 else "#38BDF8" if readiness_score >= 50 else "#EF4444"
        score_title = {"en": "Export Readiness Score", "or": "ରପ୍ତାନି ପ୍ରସ୍ତୁତି ସ୍କୋର", "hi": "निर्यात तैयारी स्कोर"}.get(lang, "Readiness Score")
        st.markdown(f"""
        <div class="metric-card" style="text-align: center; border-color: {color};">
            <div class="metric-label">{score_title}</div>
            <div style="font-size: 3.2rem; font-weight: 800; color: {color};">{readiness_score}%</div>
            <div class="metric-sub">{results['completed_count']} of {results['total_count']} Milestones Met</div>
        </div>
        """, unsafe_allow_html=True)

        if selected_project:
            if st.button("💾 " + t("save") + " Score", use_container_width=True):
                update_project_readiness(selected_project["id"], readiness_score)
                st.success(f"Updated {selected_project['title']} with {readiness_score}% readiness score!")

    with col_sc2:
        cat_data = []
        for cat_name, data in results["category_summary"].items():
            pct = round((data["completed"] / data["total"]) * 100, 1)
            cat_data.append({"Category": cat_name, "Completion (%)": pct})
        
        df_cat = pd.DataFrame(cat_data)
        fig_cat = px.bar(
            df_cat,
            x="Completion (%)",
            y="Category",
            orientation="h",
            text="Completion (%)",
            color="Completion (%)",
            color_continuous_scale=["#EF4444", "#F59E0B", "#10B981"],
            range_x=[0, 100]
        )
        fig_cat.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F8FAFC", family="Plus Jakarta Sans"),
            showlegend=False,
            margin=dict(l=20, r=20, t=10, b=20),
            height=200,
            xaxis=dict(gridcolor="#1E3A5F")
        )
        fig_cat.update_traces(texttemplate='%{text:.0f}%', textposition='outside')
        st.plotly_chart(fig_cat, use_container_width=True, config={"responsive": True, "displayModeBar": False})

    # Gaps & Roadmap
    st.write("")
    gap_col1, gap_col2 = st.columns(2)

    with gap_col1:
        st.markdown("#### ⚠️ " + {"en": "Remaining Export Gaps", "or": "ବାକି ଥିବା ରପ୍ତାନି ସର୍ତ୍ତାବଳୀ", "hi": "शेष निर्यात कमियां"}.get(lang, "Gaps"))
        if not results["missing_items"]:
            st.success("🎉 Outstanding! All 10 baseline export criteria have been completed.")
        else:
            for item in results["missing_items"]:
                desc = t_checklist(item["id"], item['description'])
                st.markdown(f"- **{item['title']}**: <span style='color: #94A3B8; font-size: 0.85rem;'>{desc}</span>", unsafe_allow_html=True)

    with gap_col2:
        st.markdown("#### 🎯 " + {"en": "Prioritized Action Items", "or": "ପ୍ରାଥମିକ କାର୍ଯ୍ୟାନୁଷ୍ଠାନ", "hi": "प्राथमिकता वाले कदम"}.get(lang, "Action Items"))
        if not results["actionable_remedies"]:
            st.info("Focus on international customer discovery and cross-border commercial pilot structuring.")
        else:
            for act in results["actionable_remedies"]:
                st.info(f"👉 {act}")

    # International Corridors
    st.write("")
    st.markdown(f"### 🌍 International Market Corridors for *{t_sector(chosen_sector)}*")
    st.caption("Hypotheses generated based on regional climate vulnerabilities, industrial mineral corridors, and shared macroeconomic structures.")

    for corridor in results["target_corridors"]:
        st.markdown(f"""
        <div class="nexus-card">
            <div style="font-size: 1.1rem; font-weight: 700; color: #00F0FF;">
                🌏 {corridor['region']} — <span style="color: #FFFFFF;">{corridor['countries']}</span>
            </div>
            <div style="margin-top: 6px; font-size: 0.88rem; color: #CBD5E1; line-height: 1.4;">
                {corridor['rationale']}
            </div>
        </div>
        """, unsafe_allow_html=True)
