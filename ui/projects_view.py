"""
AI Project Registry View for Odisha AI Nexus.
Enables ecosystem stakeholders to submit, discover, filter, update, and export AI initiatives.
Fully localized for English, Odia (ଓଡ଼ିଆ), and Hindi (हिन्दी) with voice accessibility.
"""

import streamlit as st
from typing import Dict, Any

from database import (
    get_all_projects,
    get_project_by_id,
    add_project,
    update_project_status
)
from reports import export_projects_to_csv
from config import SECTORS, PROJECT_STAGES, PROJECT_STATUSES, ODISHA_DISTRICTS
from i18n import t, t_sector, t_stage, t_status, get_current_language
from ui.voice_widget import render_voice_companion, render_voice_input_search


def render_projects_view(include_demo: bool):
    """Render the AI Project Registry interface."""
    lang = get_current_language()

    # Header
    st.markdown(f"""
    <div style="margin-bottom: 12px;">
        <h2 style="color: #FFFFFF; font-weight: 800; margin-bottom: 4px;">{t("projects_heading")}</h2>
        <div style="color: #94A3B8; font-size: 0.95rem;">
            {t("projects_subheading")}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Voice Accessibility Companion
    render_voice_companion(section_key="projects")

    tab_browse, tab_register = st.tabs([
        t("tab_browse_projects"),
        t("tab_register_project")
    ])

    # ==========================================================================
    # TAB 1: BROWSE PROJECTS
    # ==========================================================================
    with tab_browse:
        col_search, col_sector, col_status = st.columns([2, 1.5, 1.5])
        
        with col_search:
            search_query = st.text_input(
                "🔎 " + t("search_placeholder"),
                placeholder="e.g. PyTorch, pest, cyclone, Jajpur",
                key="projects_search_input"
            )
            # Voice search button
            render_voice_input_search()
        
        with col_sector:
            sector_display_map = {t("all_sectors"): "All Sectors"}
            for s in SECTORS:
                sector_display_map[t_sector(s)] = s
            selected_sector_label = st.selectbox(
                t("filter_sector"),
                list(sector_display_map.keys()),
                key="projects_sector_filter"
            )
            selected_sector = sector_display_map[selected_sector_label]
        
        with col_status:
            status_display_map = {t("all_statuses"): "All Statuses"}
            for st_val in PROJECT_STATUSES:
                status_display_map[t_status(st_val)] = st_val
            selected_status_label = st.selectbox(
                t("filter_status"),
                list(status_display_map.keys()),
                key="projects_status_filter"
            )
            selected_status = status_display_map[selected_status_label]

        # Retrieve filtered projects
        projects = get_all_projects(
            include_demo=include_demo,
            sector=selected_sector,
            status=selected_status,
            search=search_query
        )

        count_text = {
            "en": f"**Found {len(projects)} projects** matching your criteria.",
            "or": f"**{len(projects)} ଟି ପ୍ରକଳ୍ପ** ମିଳିଲା ।",
            "hi": f"आपके मानदंडों से मेल खाते **{len(projects)} प्रोजेक्ट्स** मिले।"
        }.get(lang, f"**Found {len(projects)} projects** matching your criteria.")

        st.markdown(count_text)

        # Quick CSV export button
        csv_data = export_projects_to_csv(projects)
        st.download_button(
            label="📥 " + t("export_csv"),
            data=csv_data,
            file_name="odisha_ai_projects.csv",
            mime="text/csv",
            help="Download these records in standard CSV format"
        )
        st.write("")

        if not projects:
            st.info(
                {"en": "No projects match the selected filters. Try broadening your search or register a new project!",
                 "or": "ଚୟନିତ ଫିଲ୍ଟର୍ ଅନୁଯାୟୀ କୌଣସି ପ୍ରକଳ୍ପ ମିଳିଲା ନାହିଁ । ଦୟାକରି ସନ୍ଧାନ ପରିସର ବଢ଼ାନ୍ତୁ କିମ୍ବା ନୂତନ ପ୍ରକଳ୍ପ ପଞ୍ଜୀକରଣ କରନ୍ତୁ !",
                 "hi": "चयनित फ़िल्टर से कोई प्रोजेक्ट मेल नहीं खाता। कृपया अपनी खोज का दायरा बढ़ाएं या नया प्रोजेक्ट जोड़ें!"}.get(lang, "No projects found.")
            )
        else:
            for p in projects:
                demo_badge = f'<span class="badge-demo">{t("badge_demo")}</span>' if p.get('is_demo') else f'<span class="badge-real">{t("badge_verified")}</span>'
                readiness = p.get('readiness_score', 0)
                stage_label = t_stage(p.get('stage', 'N/A'))
                status_label = t_status(p.get('status', 'Active'))
                sector_label = t_sector(p.get('sector', ''))
                
                with st.container():
                    st.markdown(f"""
                    <div class="nexus-card">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
                            <div style="flex: 1 1 260px;">
                                <span style="font-size: 1.2rem; font-weight: 700; color: #FFFFFF;">{p['title']}</span>
                                &nbsp; {demo_badge}
                                <div style="color: #00F0FF; font-size: 0.88rem; margin-top: 3px;">{p.get('tagline', '')}</div>
                            </div>
                            <div style="text-align: right; flex-shrink: 0;">
                                <span class="badge-stage">{stage_label}</span>
                                <div style="font-size: 0.88rem; font-weight: 700; color: #10B981; margin-top: 6px;">
                                    {readiness}% {t("kpi_readiness")}
                                </div>
                            </div>
                        </div>
                        <div style="margin: 10px 0; font-size: 0.88rem; color: #E2E8F0; line-height: 1.5;">
                            {p.get('description', '')}
                        </div>
                        <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px;">
                            <span class="badge-sector">📍 {p.get('district', '')}</span>
                            <span class="badge-sector">🏛️ {p.get('organization', 'Independent')}</span>
                            <span class="badge-sector">🏷️ {sector_label}</span>
                            <span class="badge-sector" style="border-color: #00F0FF; color: #00F0FF;">⚡ {status_label}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Expandable Project Actions & Deep-Dive
                    details_title = {
                        "en": f"⚙️ View Details & Manage: {p['title']}",
                        "or": f"⚙️ ବିବରଣୀ ଦେଖନ୍ତୁ ଓ ପରିଚାଳନା କରନ୍ତୁ: {p['title']}",
                        "hi": f"⚙️ विवरण देखें एवं प्रबंधित करें: {p['title']}"
                    }.get(lang, f"⚙️ View Details: {p['title']}")

                    with st.expander(details_title):
                        detail_col1, detail_col2 = st.columns(2)
                        
                        with detail_col1:
                            st.write(f"**{t('lead_innovator')}:** {p.get('lead_name', 'N/A')}")
                            st.write(f"**{t('target_beneficiaries_label')}:** {p.get('target_beneficiaries', 'N/A')}")
                            st.write(f"**{t('tech_stack_label')}:** `{p.get('tech_stack', 'Not specified')}`")
                            if p.get('github_or_demo_url'):
                                st.write(f"**{t('repo_url_label')}:** [{p['github_or_demo_url']}]({p['github_or_demo_url']})")
                        
                        with detail_col2:
                            st.write(f"**Record ID:** #{p['id']} &nbsp;|&nbsp; **Created:** {p.get('created_at', 'N/A')}")
                            # Status update form
                            status_choices = {t_status(s_opt): s_opt for s_opt in PROJECT_STATUSES}
                            cur_status_trans = t_status(p.get('status', 'Active'))
                            default_idx = list(status_choices.keys()).index(cur_status_trans) if cur_status_trans in status_choices else 0

                            new_status_trans = st.selectbox(
                                t("filter_status"),
                                list(status_choices.keys()),
                                index=default_idx,
                                key=f"status_select_{p['id']}"
                            )
                            chosen_status_val = status_choices[new_status_trans]

                            if st.button(t("save") + " Status", key=f"save_status_{p['id']}"):
                                if update_project_status(p['id'], chosen_status_val):
                                    st.success(f"Status updated successfully!")
                                    st.rerun()

    # ==========================================================================
    # TAB 2: REGISTER NEW PROJECT
    # ==========================================================================
    with tab_register:
        st.markdown(f"### 📝 {t('tab_register_project')}")
        st.caption(
            {"en": "All submissions are stored persistently in the local database as verified contributions.",
             "or": "ସମସ୍ତ ଦାଖଲ ସ୍ଥାନୀୟ ଡାଟାବେସ୍ରେ ଯାଞ୍ଚ ହୋଇଥିବା ପ୍ରକଳ୍ପ ଭାବରେ ସଂରକ୍ଷିତ ହୁଏ ।",
             "hi": "सभी प्रस्तुतियां स्थानीय डेटाबेस में सत्यापित योगदान के रूप में सुरक्षित की जाती हैं।"}.get(lang, "All submissions are stored persistently in the local database.")
        )

        from security import get_current_user
        current_user = get_current_user()
        if current_user:
            st.info(f"👤 {t('manage_profile')}: **{current_user['display_name']}** ({current_user['email']})")

        with st.form("new_project_form", clear_on_submit=True):
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                title = st.text_input(t("project_title_label"), placeholder="e.g. SmartBlast AI: Open-Cast Quarry Optimization")
                tagline = st.text_input(t("project_tagline_label"), placeholder="e.g. Physics-guided neural networks for haulage and pit safety")
                
                # Sector mapping
                sector_options_map = {t_sector(s): s for s in SECTORS}
                sel_sector_trans = st.selectbox(t("filter_sector") + " *", list(sector_options_map.keys()))
                sector = sector_options_map[sel_sector_trans]

                # Stage mapping
                stage_options_map = {t_stage(st_val): st_val for st_val in PROJECT_STAGES}
                sel_stage_trans = st.selectbox(t("stage_chart_title") + " *", list(stage_options_map.keys()))
                stage = stage_options_map[sel_stage_trans]
            
            with col_t2:
                default_lead = current_user["display_name"] if current_user else ""
                lead_name = st.text_input(t("lead_innovator") + " *", value=default_lead, placeholder="e.g. Debashis Tripathy")
                organization = st.text_input(t("organization"), placeholder="e.g. NIT Rourkela / GreenStone AI")
                district = st.selectbox(t("district") + " *", ODISHA_DISTRICTS)
                
                # Status mapping
                status_opts_map = {t_status(s_val): s_val for s_val in PROJECT_STATUSES}
                sel_status_trans = st.selectbox(t("filter_status"), list(status_opts_map.keys()))
                status = status_opts_map[sel_status_trans]

            description = st.text_area(
                t("problem_description_label"),
                placeholder="Describe what specific operational or societal problem this solution solves, who the end users are, and how the model operates...",
                height=130
            )

            col_b1, col_b2 = st.columns(2)
            with col_b1:
                target_beneficiaries = st.text_input(
                    t("target_beneficiaries_label"),
                    placeholder="e.g. Paddy farmers, sponge iron manufacturers, port operators"
                )
                tech_stack = st.text_input(
                    t("tech_stack_label"),
                    placeholder="e.g. PyTorch, YOLOv8, FastAPI, GeoPandas, Docker"
                )
            
            with col_b2:
                github_url = st.text_input(
                    t("repo_url_label"),
                    placeholder="https://github.com/your-username/your-ai-project"
                )
                initial_readiness = st.slider(f"{t('kpi_readiness')} (%)", 0, 100, 40)

            submitted = st.form_submit_button(t("btn_submit_project"), use_container_width=True)

            if submitted:
                # Validation
                if not title.strip():
                    st.error("Project Title is required / ପ୍ରକଳ୍ପ ଶୀର୍ଷକ ଆବଶ୍ୟକ ।")
                elif not description.strip():
                    st.error("Project Description is required / ବିବରଣୀ ଆବଶ୍ୟକ ।")
                elif not lead_name.strip():
                    st.error("Lead Innovator Name is required / ଉଦ୍ଭାବକଙ୍କ ନାମ ଆବଶ୍ୟକ ।")
                else:
                    new_proj_data = {
                        "title": title,
                        "tagline": tagline,
                        "description": description,
                        "sector": sector,
                        "stage": stage,
                        "lead_name": lead_name,
                        "organization": organization,
                        "district": district,
                        "target_beneficiaries": target_beneficiaries,
                        "tech_stack": tech_stack,
                        "github_or_demo_url": github_url,
                        "status": status,
                        "readiness_score": float(initial_readiness),
                        "is_demo": 0,  # Real user submission
                    }
                    new_id = add_project(new_proj_data)
                    st.success(f"🎉 Project '{title}' registered successfully with ID #{new_id}!")
                    st.balloons()
