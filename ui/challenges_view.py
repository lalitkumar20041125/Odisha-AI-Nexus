"""
Industry Challenge Board View for Odisha AI Nexus.
Allows public sector units, MSMEs, municipal bodies, and startups to post operational AI problem statements.
Fully localized for English, Odia (ଓଡ଼ିଆ), and Hindi (हिन्दी) with voice audio companion.
"""

import streamlit as st
from database import get_all_challenges, add_challenge, update_challenge_status
from reports import export_challenges_to_csv
from config import SECTORS, CHALLENGE_URGENCIES, BUDGET_RANGES, ODISHA_DISTRICTS
from i18n import t, t_sector, get_current_language
from ui.voice_widget import render_voice_companion, render_voice_input_search

ORG_TYPES = [
    "PSU / Large Enterprise",
    "MSME / Local Industry",
    "Government Dept / Urban Local Body",
    "Non-Profit / Cooperative",
    "Startup / Emerging Venture",
]


def render_challenges_view(include_demo: bool):
    """Render the Industry Challenge Board interface."""
    lang = get_current_language()

    # Header
    st.markdown(f"""
    <div style="margin-bottom: 12px;">
        <h2 style="color: #FFFFFF; font-weight: 800; margin-bottom: 4px;">{t("challenges_heading")}</h2>
        <div style="color: #94A3B8; font-size: 0.95rem;">
            {t("challenges_subheading")}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Voice Accessibility Companion
    render_voice_companion(section_key="challenges")

    tab_browse, tab_submit = st.tabs([
        t("tab_active_challenges"),
        t("tab_submit_challenge")
    ])

    # ==========================================================================
    # TAB 1: BROWSE CHALLENGES
    # ==========================================================================
    with tab_browse:
        f_col1, f_col2, f_col3 = st.columns([2, 1.5, 1.5])
        with f_col1:
            search_query = st.text_input(
                "🔎 " + t("search_placeholder"),
                placeholder="e.g. Slag, flood, cashew, cold chain",
                key="chal_search_input"
            )
            render_voice_input_search()

        with f_col2:
            sec_opts_map = {t("all_sectors"): "All Sectors"}
            for s in SECTORS:
                sec_opts_map[t_sector(s)] = s
            sel_sec_label = st.selectbox(t("filter_sector"), list(sec_opts_map.keys()), key="chal_sec_filter")
            sec_filter = sec_opts_map[sel_sec_label]

        with f_col3:
            urg_opts_map = {{"en": "All Urgencies", "or": "ସମସ୍ତ ଜରୁରୀ ସ୍ତର", "hi": "सभी प्राथमिकताएं"}.get(lang, "All Urgencies"): "All Urgencies"}
            for u in CHALLENGE_URGENCIES:
                urg_opts_map[u] = u
            sel_urg_label = st.selectbox(
                {"en": "Urgency", "or": "ଜରୁରୀ ସ୍ଥିତି", "hi": "प्राथमिकता"}.get(lang, "Urgency"),
                list(urg_opts_map.keys()),
                key="chal_urg_filter"
            )
            urg_filter = urg_opts_map[sel_urg_label]

        challenges = get_all_challenges(
            include_demo=include_demo,
            sector=sec_filter,
            urgency=urg_filter,
            search=search_query
        )

        count_msg = {
            "en": f"**Found {len(challenges)} open industry challenges.**",
            "or": f"**{len(challenges)} ଟି ସକ୍ରିୟ ଶିଳ୍ପ ସମସ୍ୟା** ମିଳିଲା ।",
            "hi": f"**{len(challenges)} सक्रिय उद्योग चुनौतियां** मिलीं।"
        }.get(lang, f"**Found {len(challenges)} challenges.**")

        st.markdown(count_msg)

        # CSV Export
        csv_chal = export_challenges_to_csv(challenges)
        st.download_button(
            label="📥 " + t("export_csv"),
            data=csv_chal,
            file_name="odisha_ai_industry_challenges.csv",
            mime="text/csv"
        )
        st.write("")

        if not challenges:
            st.info({"en": "No industry challenges match your criteria. Consider posting a challenge!",
                     "or": "ଚୟନିତ ସନ୍ଧାନ ଅନୁଯାୟୀ କୌଣସି ସମସ୍ୟା ମିଳିଲା ନାହିଁ ।",
                     "hi": "मापदंडों से मेल खाती कोई चुनौती नहीं मिली।"}.get(lang, "No challenges match."))
        else:
            for c in challenges:
                demo_badge = f'<span class="badge-demo">{t("badge_demo")}</span>' if c.get('is_demo') else f'<span class="badge-real">{t("badge_verified")}</span>'
                urgency = c.get('urgency', 'Medium')
                urg_color = "#EF4444" if "Critical" in urgency else "#F59E0B" if "High" in urgency else "#38BDF8"

                with st.container():
                    st.markdown(f"""
                    <div class="nexus-card">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
                            <div style="flex: 1 1 240px;">
                                <span style="font-size: 1.2rem; font-weight: 700; color: #FFFFFF;">{c['title']}</span>
                                &nbsp; {demo_badge}
                                <div style="color: #00F0FF; font-size: 0.88rem; margin-top: 3px;">
                                    {c.get('organization_name')} ({c.get('org_type')}) &nbsp;•&nbsp; 📍 {c.get('district')}
                                </div>
                            </div>
                            <div style="text-align: right; flex-shrink: 0;">
                                <span style="display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 700; color: {urg_color}; border: 1px solid {urg_color};">
                                    {urgency}
                                </span>
                                <div style="font-size: 0.78rem; color: #94A3B8; margin-top: 5px;">Status: <b>{c.get('status', 'Open')}</b></div>
                            </div>
                        </div>
                        <div style="margin: 12px 0 6px 0; font-size: 0.88rem; color: #CBD5E1; line-height: 1.5;">
                            <b>Problem Statement:</b><br/>{c.get('problem_statement')}
                        </div>
                        <div style="margin: 8px 0; font-size: 0.86rem; color: #34D399; line-height: 1.4;">
                            <b>Expected Solution Outcome:</b><br/>{c.get('expected_outcome')}
                        </div>
                        <div style="margin-top: 10px; display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; font-size: 0.8rem; color: #94A3B8;">
                            <div>
                                <span class="badge-sector">🏷️ {t_sector(c.get('sector', ''))}</span>
                                <span class="badge-sector" style="border-color: #00F0FF; color: #00F0FF;">💰 Budget: {c.get('budget_range')}</span>
                            </div>
                            <div>Point of Contact: <i>{c.get('contact_person', 'Organization Desk')}</i></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    with st.expander(f"⚙️ Manage Status: #{c['id']} {c['title'][:30]}"):
                        new_stat = st.selectbox(
                            "Lifecycle",
                            ["Open for Proposals", "In Evaluation", "Pilot Team Assigned", "Completed / Resolved"],
                            index=0,
                            key=f"chal_stat_{c['id']}"
                        )
                        if st.button("Update Status", key=f"btn_c_{c['id']}"):
                            update_challenge_status(c['id'], new_stat)
                            st.success("Challenge status updated!")
                            st.rerun()

    # ==========================================================================
    # TAB 2: SUBMIT A CHALLENGE
    # ==========================================================================
    with tab_submit:
        st.markdown(f"### 📢 {t('tab_submit_challenge')}")
        from security import get_current_user
        current_user = get_current_user()
        if current_user:
            st.info(f"👤 {t('manage_profile')}: **{current_user['display_name']}** ({current_user['email']})")

        with st.form("new_challenge_form", clear_on_submit=True):
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                org_name = st.text_input(t("organization") + " *", placeholder="e.g. Baitarani Basin Irrigation Board")
                org_type = st.selectbox("Category / ପ୍ରକାର *", ORG_TYPES)
                
                sec_map = {t_sector(s): s for s in SECTORS}
                sel_sec_t = st.selectbox(t("filter_sector") + " *", list(sec_map.keys()), key="new_c_sec")
                sector = sec_map[sel_sec_t]

                district = st.selectbox(t("district") + " *", ODISHA_DISTRICTS, key="new_c_dist")

            with col_s2:
                chal_title = st.text_input("Title / ଶୀର୍ଷକ *", placeholder="e.g. Automated Optical Sorting for Cashew Kernel Defects")
                urgency = st.selectbox("Urgency / ଜରୁରୀ ସ୍ଥିତି *", CHALLENGE_URGENCIES)
                budget_range = st.selectbox("Budget / ଅନୁଦାନ *", BUDGET_RANGES)
                default_contact = current_user["display_name"] if current_user else ""
                contact_person = st.text_input("Contact Person / ଯୋଗାଯୋଗ ବ୍ୟକ୍ତି *", value=default_contact, placeholder="e.g. Technology Cell")

            problem_statement = st.text_area(
                "Problem Bottleneck / ସମସ୍ୟା ବିବରଣୀ *",
                placeholder="Explain the physical or operational challenge...",
                height=130
            )

            expected_outcome = st.text_area(
                "Desired Deliverable & Metric / ପ୍ରତ୍ୟାଶିତ ଫଳାଫଳ *",
                placeholder="e.g. A lightweight mobile vision app achieving 92%+ classification accuracy...",
                height=100
            )

            c_submitted = st.form_submit_button("🚀 " + t("submit"), use_container_width=True)

            if c_submitted:
                if not org_name.strip() or not chal_title.strip() or not problem_statement.strip() or not expected_outcome.strip():
                    st.error("Please fill in all mandatory fields (Organization, Title, Problem, Outcome).")
                else:
                    new_chal = {
                        "title": chal_title,
                        "organization_name": org_name,
                        "org_type": org_type,
                        "sector": sector,
                        "district": district,
                        "problem_statement": problem_statement,
                        "expected_outcome": expected_outcome,
                        "budget_range": budget_range,
                        "urgency": urgency,
                        "contact_person": contact_person,
                        "is_demo": 0,
                    }
                    new_cid = add_challenge(new_chal)
                    st.success(f"🎉 Challenge #{new_cid} successfully published!")
                    st.balloons()
