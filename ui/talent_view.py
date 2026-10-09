"""
Odisha AI Talent Exchange View for Odisha AI Nexus.
Facilitates talent registration, privacy-first profiles, and bidirectional skill matching with projects.
Fully localized for English, Odia (ଓଡ଼ିଆ), and Hindi (हिन्दी) with voice audio companion.
"""

import streamlit as st
from database import get_all_talent, get_all_projects, add_talent
from matching import mask_email, find_top_projects_for_talent, find_top_talent_for_project
from reports import export_talent_to_csv
from config import EXPERIENCE_LEVELS, ODISHA_DISTRICTS, SECTORS
from i18n import t, t_exp, t_sector, t_stage, get_current_language
from ui.voice_widget import render_voice_companion, render_voice_input_search


def render_talent_view(include_demo: bool):
    """Render the AI Talent Exchange interface."""
    lang = get_current_language()

    # Header
    st.markdown(f"""
    <div style="margin-bottom: 12px;">
        <h2 style="color: #FFFFFF; font-weight: 800; margin-bottom: 4px;">{t("talent_heading")}</h2>
        <div style="color: #94A3B8; font-size: 0.95rem;">
            {t("talent_subheading")}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Voice Accessibility Companion
    render_voice_companion(section_key="talent")

    tab_dir, tab_match, tab_reg = st.tabs([
        t("tab_explore_talent"),
        t("tab_smart_matching"),
        t("tab_register_talent")
    ])

    # ==========================================================================
    # TAB 1: TALENT DIRECTORY
    # ==========================================================================
    with tab_dir:
        f_col1, f_col2 = st.columns([2, 1.5])
        with f_col1:
            search_query = st.text_input(
                "🔎 " + t("search_placeholder"),
                placeholder="e.g. PyTorch, IIT, NLP, VSSUT, GIS",
                key="talent_search_input"
            )
            render_voice_input_search()

        with f_col2:
            all_exp_lbl = {"en": "All Experience Levels", "or": "ସମସ୍ତ ଅଭିଜ୍ଞତା ସ୍ତର", "hi": "सभी अनुभव स्तर"}.get(lang, "All Levels")
            exp_display_map = {all_exp_lbl: "All Experience Levels"}
            for exp_v in EXPERIENCE_LEVELS:
                exp_display_map[t_exp(exp_v)] = exp_v

            selected_exp_label = st.selectbox(
                {"en": "Experience Level", "or": "ଅଭିଜ୍ଞତା ସ୍ତର", "hi": "अनुभव स्तर"}.get(lang, "Experience Level"),
                list(exp_display_map.keys()),
                key="talent_exp_filter"
            )
            exp_filter = exp_display_map[selected_exp_label]

        talents = get_all_talent(include_demo=include_demo, experience=exp_filter, search=search_query)

        count_msg = {
            "en": f"**Found {len(talents)} talent profiles** in the network.",
            "or": f"ନେଟୱର୍କରେ **{len(talents)} ଜଣ ପ୍ରତିଭା ପ୍ରୋଫାଇଲ୍** ମିଳିଲା ।",
            "hi": f"नेटवर्क में **{len(talents)} प्रतिभा प्रोफाइल** मिले।"
        }.get(lang, f"**Found {len(talents)} talent profiles**.")

        st.markdown(count_msg)
        
        # Privacy notice
        privacy_html = {
            "en": """
            <div class="disclaimer-box" style="margin-top: 6px;">
                🔒 <b>Privacy Safeguard:</b> Direct contact emails are masked by default to protect students and professionals from scraping and unsolicited spam. Portfolios and public GitHub links remain accessible.
            </div>
            """,
            "or": """
            <div class="disclaimer-box" style="margin-top: 6px;">
                🔒 <b>ଗୋପନୀୟତା ସୁରକ୍ଷା:</b> ଛାତ୍ରଛାତ୍ରୀ ଏବଂ ପେଶାଦାରମାନଙ୍କୁ ସ୍ପାମ୍‌ରୁ ରକ୍ଷା କରିବା ପାଇଁ ସିଧାସଳଖ ଇମେଲ୍ ମାସ୍କ (ଲୁକ୍କାୟିତ) କରାଯାଇଛି । ପୋର୍ଟଫୋଲିଓ ଏବଂ GitHub ଲିଙ୍କ୍ ଉପଲବ୍ଧ ରହିଛି ।
            </div>
            """,
            "hi": """
            <div class="disclaimer-box" style="margin-top: 6px;">
                🔒 <b>गोपनीयता सुरक्षा:</b> स्पैम से छात्रों और पेशेवरों की सुरक्षा हेतु संपर्क ईमेल डिफ़ॉल्ट रूप से मास्क किए गए हैं। पोर्टफोलियो और GitHub लिंक सुलभ हैं।
            </div>
            """
        }.get(lang, "")
        st.markdown(privacy_html, unsafe_allow_html=True)

        # CSV Export
        csv_talent = export_talent_to_csv(talents)
        st.download_button(
            label="📥 " + t("export_csv"),
            data=csv_talent,
            file_name="odisha_ai_talent_directory.csv",
            mime="text/csv"
        )
        st.write("")

        if not talents:
            st.info({"en": "No talent profiles found matching the current search parameters.",
                     "or": "ଚୟନିତ ସନ୍ଧାନ ଅନୁଯାୟୀ କୌଣସି ପ୍ରୋଫାଇଲ୍ ମିଳିଲା ନାହିଁ ।",
                     "hi": "वर्तमान खोज मापदंडों से मेल खाती कोई प्रोफ़ाइल नहीं मिली।"}.get(lang, "No profiles found."))
        else:
            for t_item in talents:
                demo_badge = f'<span class="badge-demo">{t("badge_demo")}</span>' if t_item.get('is_demo') else f'<span class="badge-real">{t("badge_verified")}</span>'
                masked_contact = mask_email(t_item.get('contact_email', ''))
                skills = [s.strip() for s in t_item.get('technical_skills', '').split(',') if s.strip()]
                skills_html = "".join([f'<span class="skill-pill">{s}</span>' for s in skills])

                with st.container():
                    st.markdown(f"""
                    <div class="nexus-card">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
                            <div style="flex: 1 1 240px;">
                                <span style="font-size: 1.15rem; font-weight: 700; color: #FFFFFF;">{t_item['full_name']}</span>
                                &nbsp; {demo_badge}
                                <div style="color: #00F0FF; font-size: 0.88rem; margin-top: 3px;">
                                    {t_item.get('role_title', 'AI Researcher')} &nbsp;•&nbsp; <span style="color: #CBD5E1;">{t_item.get('institution', '')}</span>
                                </div>
                            </div>
                            <div style="text-align: right; flex-shrink: 0;">
                                <span class="badge-stage">{t_exp(t_item.get('experience_level', 'N/A'))}</span>
                                <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 4px;">📍 {t_item.get('district', '')}</div>
                            </div>
                        </div>
                        <div style="margin: 10px 0 6px 0; font-size: 0.86rem; color: #E2E8F0; line-height: 1.4;">
                            {t_item.get('bio', '')}
                        </div>
                        <div style="margin: 8px 0;">
                            <span style="font-size: 0.78rem; color: #94A3B8; font-weight: 600;">SKILLS:</span>&nbsp;
                            {skills_html}
                        </div>
                        <div style="margin-top: 10px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; font-size: 0.8rem; color: #94A3B8;">
                            <div><b>Interests:</b> {t_item.get('areas_of_interest', '')}</div>
                            <div>
                                {'🔗 <a href="' + t_item['portfolio_url'] + '" target="_blank" style="color: #00F0FF;">Portfolio</a> &nbsp;|&nbsp; ' if t_item.get('portfolio_url') else ''}
                                <span>📧 {masked_contact}</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    # ==========================================================================
    # TAB 2: AI SYNERGY MATCHER
    # ==========================================================================
    with tab_match:
        st.markdown(f"### 🎯 {t('tab_smart_matching')}")
        mode_opt1 = {"en": "Find Talent for a Project", "or": "ପ୍ରକଳ୍ପ ପାଇଁ ପ୍ରତିଭା ଖୋଜନ୍ତୁ", "hi": "प्रोजेक्ट हेतु प्रतिभा खोजें"}.get(lang, "Find Talent for a Project")
        mode_opt2 = {"en": "Find Projects for a Talent Profile", "or": "ପ୍ରତିଭା ପାଇଁ ଉପଯୁକ୍ତ ପ୍ରକଳ୍ପ ଖୋଜନ୍ତୁ", "hi": "प्रतिभा हेतु उपयुक्त प्रोजेक्ट्स खोजें"}.get(lang, "Find Projects for Talent")
        
        mode = st.radio("Perspective / ଦୃଷ୍ଟିକୋଣ:", [mode_opt1, mode_opt2], horizontal=True)

        projects_all = get_all_projects(include_demo=include_demo)
        talents_all = get_all_talent(include_demo=include_demo)

        if not projects_all or not talents_all:
            st.warning("Both projects and talent profiles must be present to compute matches.")
        else:
            if mode == mode_opt1:
                proj_options = {f"{p['title']} (#{p['id']})": p for p in projects_all}
                selected_proj_key = st.selectbox("Choose Project:", list(proj_options.keys()))
                target_project = proj_options[selected_proj_key]

                st.markdown(f"**Tech Stack:** `{target_project.get('tech_stack', 'Not specified')}` &nbsp;|&nbsp; **Sector:** {t_sector(target_project.get('sector', ''))}")
                
                matches = find_top_talent_for_project(target_project, talents_all, top_n=4)
                
                st.write("")
                st.markdown(f"#### Top Matched Candidates for *{target_project['title']}*")
                for candidate, info in matches:
                    score = info["score"]
                    color = "#10B981" if score >= 70 else "#38BDF8" if score >= 50 else "#94A3B8"
                    
                    with st.container():
                        st.markdown(f"""
                        <div class="nexus-card">
                            <div style="display: flex; justify-content: space-between;">
                                <div>
                                    <span style="font-weight: 700; font-size: 1.1rem; color: #FFFFFF;">{candidate['full_name']}</span>
                                    <span style="color: #94A3B8; font-size: 0.85rem;"> — {candidate.get('institution')} ({candidate.get('district')})</span>
                                </div>
                                <div style="font-size: 1.25rem; font-weight: 800; color: {color};">
                                    {score}% Match
                                </div>
                            </div>
                            <div style="margin: 8px 0; font-size: 0.85rem; color: #CBD5E1;">
                                <b>Why this match?</b>
                                <ul style="margin: 4px 0 0 16px; padding: 0;">
                                    {"".join([f"<li>{r}</li>" for r in info['reasons']])}
                                </ul>
                            </div>
                            <div style="font-size: 0.8rem; color: #94A3B8;">
                                Skills: <code>{candidate.get('technical_skills')}</code>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

            else:
                talent_options = {f"{t_one['full_name']} — {t_one.get('role_title')} (#{t_one['id']})": t_one for t_one in talents_all}
                selected_talent_key = st.selectbox("Choose Profile:", list(talent_options.keys()))
                target_talent = talent_options[selected_talent_key]

                st.markdown(f"**Skills:** `{target_talent.get('technical_skills')}` &nbsp;|&nbsp; **Interests:** {target_talent.get('areas_of_interest')}")
                
                proj_matches = find_top_projects_for_talent(target_talent, projects_all, top_n=4)
                
                st.write("")
                st.markdown(f"#### Recommended Projects for *{target_talent['full_name']}*")
                for proj, info in proj_matches:
                    score = info["score"]
                    color = "#10B981" if score >= 70 else "#38BDF8" if score >= 50 else "#94A3B8"
                    
                    with st.container():
                        st.markdown(f"""
                        <div class="nexus-card">
                            <div style="display: flex; justify-content: space-between;">
                                <div>
                                    <span style="font-weight: 700; font-size: 1.1rem; color: #FFFFFF;">{proj['title']}</span>
                                    <span style="color: #94A3B8; font-size: 0.85rem;"> — {proj.get('organization')}</span>
                                </div>
                                <div style="font-size: 1.25rem; font-weight: 800; color: {color};">
                                    {score}% Match
                                </div>
                            </div>
                            <div style="margin: 8px 0; font-size: 0.85rem; color: #CBD5E1;">
                                <b>Why this match?</b>
                                <ul style="margin: 4px 0 0 16px; padding: 0;">
                                    {"".join([f"<li>{r}</li>" for r in info['reasons']])}
                                </ul>
                            </div>
                            <div style="font-size: 0.8rem; color: #94A3B8;">
                                Sector: <b>{t_sector(proj.get('sector', ''))}</b> &nbsp;|&nbsp; Stage: <b>{t_stage(proj.get('stage', ''))}</b>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

    # ==========================================================================
    # TAB 3: REGISTER TALENT PROFILE
    # ==========================================================================
    with tab_reg:
        st.markdown(f"### 📝 {t('tab_register_talent')}")
        from security import get_current_user
        current_user = get_current_user()
        if current_user:
            st.info(f"👤 {t('manage_profile')}: **{current_user['display_name']}** ({current_user['email']})")

        with st.form("talent_reg_form", clear_on_submit=True):
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                default_name = current_user["display_name"] if current_user else ""
                name = st.text_input("Full Name / ପୂର୍ଣ୍ଣ ନାମ *", value=default_name, placeholder="e.g. Lipika Mohapatra")
                institution = st.text_input(t("organization") + " *", placeholder="e.g. IIT Bhubaneswar, VSSUT, Infosys")
                district = st.selectbox(t("district") + " *", ODISHA_DISTRICTS)
                role_title = st.text_input("Role / ବିଶେଷଜ୍ଞତା *", placeholder="e.g. Computer Vision Researcher, ML Engineer")

            with col_r2:
                exp_trans_map = {t_exp(ev): ev for ev in EXPERIENCE_LEVELS}
                sel_exp_t = st.selectbox("Experience Level / ଅଭିଜ୍ଞତା *", list(exp_trans_map.keys()))
                experience = exp_trans_map[sel_exp_t]

                skills_input = st.text_input(t("tech_stack_label") + " *", placeholder="PyTorch, OpenCV, ROS2, FastAPI, Transformers")
                interests_input = st.text_input("Areas of Interest / ଆଗ୍ରହ କ୍ଷେତ୍ର *", placeholder="Disaster Management, Agritech, Healthcare")
                portfolio_url = st.text_input("Portfolio / GitHub URL", placeholder="https://github.com/your-handle")

            default_email = current_user["email"] if current_user else ""
            contact_email = st.text_input("Contact Email / ଇମେଲ୍ *", value=default_email, placeholder="your.email@domain.com")
            bio = st.text_area("Bio / ପରିଚୟ", placeholder="Describe your background and skills...", height=100)

            t_submitted = st.form_submit_button("🚀 " + t("submit"), use_container_width=True)

            if t_submitted:
                if not name.strip() or not institution.strip() or not skills_input.strip() or not contact_email.strip():
                    st.error("Please fill in all required fields (Name, Institution, Skills, Email).")
                else:
                    new_talent_data = {
                        "full_name": name,
                        "institution": institution,
                        "district": district,
                        "role_title": role_title,
                        "experience_level": experience,
                        "technical_skills": skills_input,
                        "areas_of_interest": interests_input,
                        "portfolio_url": portfolio_url,
                        "bio": bio,
                        "contact_email": contact_email,
                        "is_available": 1,
                        "is_demo": 0,
                    }
                    new_id = add_talent(new_talent_data)
                    st.success(f"🎉 Profile #{new_id} registered successfully for {name}!")
                    st.balloons()
