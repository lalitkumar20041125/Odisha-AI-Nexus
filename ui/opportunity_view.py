"""
AI Opportunity Explorer View for Odisha AI Nexus.
Provides a transparent, explainable decision-support algorithm to evaluate AI product concepts.
Fully localized for English, Odia (ଓଡ଼ିଆ), and Hindi (हिन्दी) with voice audio companion.
"""

import streamlit as st
import plotly.graph_objects as go
import json

from config import SECTORS, DEFAULT_SCORING_WEIGHTS
from scoring import calculate_opportunity_score
from database import add_assessment, get_all_assessments
from reports import generate_opportunity_pdf
from i18n import t, t_sector, get_current_language
from ui.voice_widget import render_voice_companion


def render_opportunity_view(include_demo: bool):
    """Render the AI Opportunity Explorer interface."""
    lang = get_current_language()

    # Header
    st.markdown(f"""
    <div style="margin-bottom: 12px;">
        <h2 style="color: #FFFFFF; font-weight: 800; margin-bottom: 4px;">{t("opp_heading")}</h2>
        <div style="color: #94A3B8; font-size: 0.95rem;">
            {t("opp_subheading")}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Voice audio companion
    render_voice_companion(section_key="opportunity")

    tab_eval, tab_history = st.tabs([
        t("tab_eval_idea"),
        t("tab_eval_history")
    ])

    # ==========================================================================
    # TAB 1: EVALUATE IDEA
    # ==========================================================================
    with tab_eval:
        disclaimer_html = {
            "en": """
            <div class="disclaimer-box">
                ⚖️ <b>Prototype Decision-Support Tool:</b> This scoring engine generates a structured 
                heuristic evaluation (0–100) based on weighted multi-criteria decision analysis. 
                It is designed to highlight operational blindspots, data gaps, and export corridors. 
                It is <b>not</b> a scientifically guaranteed prediction of commercial or financial success.
            </div>
            """,
            "or": """
            <div class="disclaimer-box">
                ⚖️ <b>ପ୍ରୋଟୋଟାଇପ୍ ନିଷ୍ପତ୍ତି-ସହାୟକ ଉପକରଣ:</b> ଏହି ସ୍କୋରିଂ ଇଞ୍ଜିନ୍ ବହୁ-ମାନଦଣ୍ଡ ବିଶ୍ଳେଷଣ ଉପରେ ଆଧାରିତ ଏକ ଗଠନମୂଳକ ଆକଳନ (୦-୧୦୦) ପ୍ରଦାନ କରେ । 
                ଏହା କାର୍ଯ୍ୟକ୍ଷମ ଦୁର୍ବଳତା ଏବଂ ରପ୍ତାନି ସୁଯୋଗ ଦର୍ଶାଇବା ପାଇଁ ଉଦ୍ଦିଷ୍ଟ । ଏହା କୌଣସି ବାଣିଜ୍ୟିକ ସଫଳତାର ଗ୍ୟାରେଣ୍ଟି ନୁହେଁ ।
            </div>
            """,
            "hi": """
            <div class="disclaimer-box">
                ⚖️ <b>प्रोटोटाइप निर्णय-सहायक प्रणाली:</b> यह स्कोरिंग इंजन बहु-मानदंडीय विश्लेषण पर आधारित एक संरचनात्मक मूल्यांकन (0-100) तैयार करता है। 
                इसका उद्देश्य परिचालन संबंधी कमियों और निर्यात अवसरों को उजागर करना है। यह व्यावसायिक सफलता की गारंटी नहीं है।
            </div>
            """
        }.get(lang, "")

        st.markdown(disclaimer_html, unsafe_allow_html=True)

        with st.form("opportunity_form"):
            col_left, col_right = st.columns([1.2, 1])

            with col_left:
                title_label = {"en": "AI Solution / Idea Title *", "or": "AI ସମାଧାନ / ଧାରଣା ଶୀର୍ଷକ *", "hi": "AI समाधान / विचार का शीर्षक *"}.get(lang, "Idea Title")
                title = st.text_input(title_label, placeholder="e.g. DroneSAR Flood Inundation Mapper")
                
                sector_opts_map = {t_sector(s): s for s in SECTORS}
                sel_sec_trans = st.selectbox(t("filter_sector") + " *", list(sector_opts_map.keys()))
                sector = sector_opts_map[sel_sec_trans]

                prob_label = {
                    "en": "Problem Statement & Proposed Solution *",
                    "or": "ସମସ୍ୟା ବିବରଣୀ ଏବଂ ପ୍ରସ୍ତାବିତ ସମାଧାନ *",
                    "hi": "समस्या विवरण एवं प्रस्तावित समाधान *"
                }.get(lang, "Problem Statement")

                problem_statement = st.text_area(
                    prob_label,
                    placeholder="Describe the operational challenge in Odisha (or globally), the intended user, and how your proposed machine learning pipeline addresses it...",
                    height=180
                )

            with col_right:
                slider_header = {
                    "en": "**Multi-Criteria Parameter Sliders (1 = Low, 10 = High)**",
                    "or": "**ବହୁ-ମାନଦଣ୍ଡ ପାରାମିଟର ସ୍ଲାଇଡର୍ (୧ = କମ୍, ୧୦ = ଅଧିକ)**",
                    "hi": "**बहु-मानदंडीय पैरामीटर स्लाइडर्स (1 = कम, 10 = अधिक)**"
                }.get(lang, "Parameter Sliders")
                st.markdown(slider_header)

                lbl_tech = {"en": "Technical Feasibility & Architecture Clarity", "or": "ପ୍ରଯୁକ୍ତିଗତ ସମ୍ଭାବ୍ୟତା ଏବଂ ସ୍ପଷ୍ଟତା", "hi": "तकनीकी व्यवहार्यता एवं आर्किटेक्चर स्पष्टता"}.get(lang, "Tech Feasibility")
                lbl_impact = {"en": "Expected Socio-Economic Impact", "or": "ସାମାଜିକ-ଅର୍ଥନୈତିକ ପ୍ରଭାବ", "hi": "अपेक्षित सामाजिक-आर्थिक प्रभाव"}.get(lang, "Impact")
                lbl_budget = {"en": "Budget & Resource Realism", "or": "ବଜେଟ୍ ଏବଂ ସମ୍ବଳ ବାସ୍ତବତା", "hi": "बजट एवं संसाधन यथार्थता"}.get(lang, "Budget")
                lbl_data = {"en": "Data Availability & Regulatory Fit", "or": "ଡାଟା ଉପଲବ୍ଧତା ଏବଂ ନିୟାମକ ଅନୁପାଳନ", "hi": "डेटा उपलब्धता एवं विनियामक अनुपालन"}.get(lang, "Data Viability")
                lbl_global = {"en": "Global Market & Export Potential", "or": "ବିଶ୍ୱ ବଜାର ଏବଂ ରପ୍ତାନି ସାମର୍ଥ୍ୟ", "hi": "वैश्विक बाज़ार एवं निर्यात क्षमता"}.get(lang, "Global Potential")

                tech_feas = st.slider(lbl_tech, 1, 10, 7)
                impact = st.slider(lbl_impact, 1, 10, 8)
                budget = st.slider(lbl_budget, 1, 10, 6)
                data_ready = st.slider(lbl_data, 1, 10, 6)
                global_pot = st.slider(lbl_global, 1, 10, 7)

            with st.expander("⚙️ Advanced: Configure Dimension Weights"):
                st.caption("Customize the relative importance of each dimension.")
                w_col1, w_col2, w_col3 = st.columns(3)
                with w_col1:
                    w_tech = st.number_input("Tech Feasibility Weight", 5, 50, DEFAULT_SCORING_WEIGHTS["technical_feasibility"])
                    w_loc = st.number_input("Local Relevance Weight", 5, 50, DEFAULT_SCORING_WEIGHTS["local_relevance"])
                with w_col2:
                    w_imp = st.number_input("Impact Weight", 5, 50, DEFAULT_SCORING_WEIGHTS["socio_economic_impact"])
                    w_glob = st.number_input("Global Potential Weight", 5, 50, DEFAULT_SCORING_WEIGHTS["global_market_potential"])
                with w_col3:
                    w_bud = st.number_input("Budget Realism Weight", 5, 50, DEFAULT_SCORING_WEIGHTS["budget_resource_realism"])
                    w_dat = st.number_input("Data/Reg Viability Weight", 5, 50, DEFAULT_SCORING_WEIGHTS["data_regulatory_viability"])

            eval_submitted = st.form_submit_button(t("btn_run_opp_assessment"), use_container_width=True)

        if eval_submitted:
            if not title.strip() or not problem_statement.strip():
                st.error("Please provide both an Idea Title and a Problem Statement / ଦୟାକରି ଶୀର୍ଷକ ଏବଂ ବିବରଣୀ ପ୍ରଦାନ କରନ୍ତୁ ।")
            else:
                custom_w = {
                    "technical_feasibility": w_tech,
                    "local_relevance": w_loc,
                    "socio_economic_impact": w_imp,
                    "global_market_potential": w_glob,
                    "budget_resource_realism": w_bud,
                    "data_regulatory_viability": w_dat,
                }
                
                result = calculate_opportunity_score(
                    title=title,
                    sector=sector,
                    problem_statement=problem_statement,
                    tech_feasibility_input=tech_feas,
                    impact_input=impact,
                    budget_input=budget,
                    data_readiness_input=data_ready,
                    global_potential_input=global_pot,
                    custom_weights=custom_w
                )
                
                st.session_state["latest_assessment"] = result

        # Display results if available
        if "latest_assessment" in st.session_state:
            res = st.session_state["latest_assessment"]
            st.write("")
            st.divider()
            
            score_col1, score_col2 = st.columns([1, 2])
            
            with score_col1:
                score = res["overall_score"]
                color = "#10B981" if score >= 75 else "#F59E0B" if score >= 55 else "#EF4444"
                
                verdict_text = {
                    "en": "🟢 High Viability & Alignment" if score >= 75 else "🟡 Moderate / Address Gaps" if score >= 55 else "🔴 High Risk / Requires Re-scoping",
                    "or": "🟢 ଉଚ୍ଚ ସମ୍ଭାବ୍ୟତା ଓ ପ୍ରାସଙ୍ଗିକତା" if score >= 75 else "🟡 ମଧ୍ୟମ ସ୍ତର / ଦୁର୍ବଳତା ସୁଧାରନ୍ତୁ" if score >= 55 else "🔴 ଉଚ୍ଚ ବିପଦ / ପୁନର୍ବିଚାର ଆବଶ୍ୟକ",
                    "hi": "🟢 उच्च व्यवहार्यता एवं प्रासंगिकता" if score >= 75 else "🟡 मध्यम स्तर / कमियां सुधारें" if score >= 55 else "🔴 उच्च जोखिम / पुनर्मूल्यांकन आवश्यक"
                }.get(lang, "Composite Score")

                score_lbl = {"en": "Composite Opportunity Score", "or": "ମିଳିତ ସୁଯୋଗ ସ୍କୋର", "hi": "समग्र अवसर स्कोर"}.get(lang, "Composite Score")

                st.markdown(f"""
                <div class="metric-card" style="text-align: center; border-color: {color};">
                    <div class="metric-label">{score_lbl}</div>
                    <div style="font-size: 3.2rem; font-weight: 800; color: {color};">{score}<span style="font-size: 1.5rem; color: #94A3B8;">/100</span></div>
                    <div class="metric-sub">
                        {verdict_text}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with score_col2:
                categories = [
                    "Tech Feasibility", "Local Relevance", "Socio-Econ Impact",
                    "Global Potential", "Budget Realism", "Data Viability"
                ]
                values = [
                    res["factors"]["technical_feasibility"],
                    res["factors"]["local_relevance"],
                    res["factors"]["socio_economic_impact"],
                    res["factors"]["global_market_potential"],
                    res["factors"]["budget_resource_realism"],
                    res["factors"]["data_regulatory_viability"],
                ]
                categories_closed = categories + [categories[0]]
                values_closed = values + [values[0]]

                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=values_closed,
                    theta=categories_closed,
                    fill='toself',
                    fillcolor='rgba(0, 240, 255, 0.2)',
                    line=dict(color='#00F0FF', width=2),
                    name='Factor Rating'
                ))
                fig.update_layout(
                    polar=dict(
                        bgcolor="rgba(13, 27, 46, 0.4)",
                        radialaxis=dict(visible=True, range=[0, 100], gridcolor="#1E3A5F", tickfont=dict(color="#94A3B8", size=8)),
                        angularaxis=dict(gridcolor="#1E3A5F", tickfont=dict(color="#F8FAFC", size=9))
                    ),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=40, r=40, t=20, b=20),
                    height=240,
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True, config={"responsive": True, "displayModeBar": False})

            # Strengths & Weaknesses
            str_col, weak_col = st.columns(2)
            with str_col:
                st.markdown("#### ✅ " + {"en": "Identified Strengths", "or": "ଚିହ୍ନଟ ହୋଇଥିବା ଶକ୍ତି", "hi": "पहचानी गई ताकत"}.get(lang, "Strengths"))
                for s in res["strengths"]:
                    st.success(s)

            with weak_col:
                st.markdown("#### ⚠️ " + {"en": "Operational Blindspots & Gaps", "or": "କାର୍ଯ୍ୟକ୍ଷମ ଦୁର୍ବଳତା ଓ ଅଭାବ", "hi": "परिचालन संबंधी कमियां"}.get(lang, "Gaps"))
                for w in res["weaknesses"]:
                    st.warning(w)

            # Recommendations
            st.markdown("#### 🎯 " + {"en": "Practical Next Steps for Validation", "or": "ପ୍ରମାଣୀକରଣ ପାଇଁ ପରବର୍ତ୍ତୀ ପଦକ୍ଷେପ", "hi": "सत्यापन हेतु व्यावहारिक अगले कदम"}.get(lang, "Next Steps"))
            for idx, r in enumerate(res["recommendations"], 1):
                st.info(r)

            # Risk Matrix
            st.markdown("#### 🛡️ " + {"en": "Multidimensional Risk Assessment", "or": "ବହୁମୁଖୀ ବିପଦ ମୂଲ୍ୟାଙ୍କନ", "hi": "बहुआयामी जोखिम मूल्यांकन"}.get(lang, "Risk Assessment"))
            r_col1, r_col2 = st.columns(2)
            with r_col1:
                st.markdown(f"**Technical Risk:** {res['risks']['technical']}")
                st.markdown(f"**Financial Risk:** {res['risks']['financial']}")
            with r_col2:
                st.markdown(f"**Operational Risk:** {res['risks']['operational']}")
                st.markdown(f"**Adoption Risk:** {res['risks']['adoption']}")

            # Actions
            st.write("")
            act_col1, act_col2 = st.columns(2)
            
            with act_col1:
                btn_save_lbl = {"en": "💾 Save Assessment to Database", "or": "💾 ଡାଟାବେସ୍ରେ ମୂଲ୍ୟାଙ୍କନ ସଂରକ୍ଷଣ କରନ୍ତୁ", "hi": "💾 डेटाबेस में मूल्यांकन सुरक्षित करें"}.get(lang, "Save Assessment")
                if st.button(btn_save_lbl, use_container_width=True):
                    db_entry = {
                        "idea_title": res["title"],
                        "sector": res["sector"],
                        "problem_statement": res["problem_statement"],
                        "overall_score": res["overall_score"],
                        "factor_breakdown": res["factors"],
                        "strengths": res["strengths"],
                        "weaknesses": res["weaknesses"],
                        "recommendations": res["recommendations"],
                        "risks": res["risks"],
                        "target_markets": res["target_markets"],
                        "is_demo": 0,
                    }
                    add_assessment(db_entry)
                    st.success("Assessment archived permanently to local SQLite database!")

            with act_col2:
                pdf_bytes = generate_opportunity_pdf(res)
                btn_pdf_lbl = {"en": "📄 Download Assessment Report (PDF)", "or": "📄 ମୂଲ୍ୟାଙ୍କନ ରିପୋର୍ଟ ଡାଉନଲୋଡ୍ (PDF)", "hi": "📄 मूल्यांकन रिपोर्ट डाउनलोड करें (PDF)"}.get(lang, "Download PDF")
                st.download_button(
                    label=btn_pdf_lbl,
                    data=pdf_bytes,
                    file_name=f"assessment_{res['title'][:15].lower().replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

    # ==========================================================================
    # TAB 2: SAVED ASSESSMENTS
    # ==========================================================================
    with tab_history:
        assessments = get_all_assessments(include_demo=include_demo)
        st.markdown(f"**{t('tab_eval_history')} ({len(assessments)} records)**")
        
        if not assessments:
            st.info("No saved assessments available in the current view.")
        else:
            for a in assessments:
                demo_badge = f'<span class="badge-demo">{t("badge_demo")}</span>' if a.get('is_demo') else f'<span class="badge-real">{t("badge_verified")}</span>'
                with st.expander(f"📊 {a['idea_title']} ({t_sector(a.get('sector', ''))}) — Score: {a.get('overall_score')}/100"):
                    st.markdown(f"{demo_badge} &nbsp; **Date:** {a.get('created_at', 'N/A')}", unsafe_allow_html=True)
                    st.write(f"**Problem Statement:** {a.get('problem_statement', '')}")
                    
                    st.markdown("**Strengths:**")
                    for s in a.get("strengths", []):
                        st.write(f"- {s}")
                    
                    st.markdown("**Gaps:**")
                    for w in a.get("weaknesses", []):
                        st.write(f"- {w}")
                    
                    pdf_data = generate_opportunity_pdf({
                        "title": a["idea_title"],
                        "sector": a["sector"],
                        "problem_statement": a["problem_statement"],
                        "overall_score": a["overall_score"],
                        "factors": a.get("factor_breakdown", {}),
                        "contributions": {},
                        "strengths": a.get("strengths", []),
                        "weaknesses": a.get("weaknesses", []),
                        "recommendations": a.get("recommendations", []),
                        "disclaimer": "Educational Prototype Score",
                    })
                    st.download_button(
                        label="📥 " + t("download_pdf"),
                        data=pdf_data,
                        file_name=f"assessment_{a['id']}.pdf",
                        mime="application/pdf",
                        key=f"dl_pdf_saved_{a['id']}"
                    )
