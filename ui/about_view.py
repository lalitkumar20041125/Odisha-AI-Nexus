"""
About and Development Roadmap View for Odisha AI Nexus.
Presents mission, complementary ecosystem position, 5-phase strategic roadmap,
and transparency & governance declarations.
Fully localized for English, Odia (ଓଡ଼ିଆ), and Hindi (हिन्दी) with voice audio companion.
"""

import streamlit as st
from config import APP_NAME, TAGLINE, COMMUNITY_DISCLAIMER
from i18n import t, get_current_language
from ui.voice_widget import render_voice_companion


def render_about_view():
    """Render the About, Strategic Roadmap, and Governance view."""
    lang = get_current_language()

    # Header
    st.markdown(f"""
    <div class="nexus-header">
        <h1 class="nexus-title">{t("about_heading")}</h1>
        <div class="nexus-tagline">{t("tagline")}</div>
    </div>
    """, unsafe_allow_html=True)

    # Voice audio companion
    render_voice_companion(
        section_key="about",
        custom_text={
            "en": "About Odisha AI Nexus. Our mission is to bridge students, researchers, startups, and heavy industries across all 30 districts of Odisha with national and global artificial intelligence markets.",
            "or": "ଓଡ଼ିଶା AI ନେକ୍ସସ୍ ବିଷୟରେ । ଆମର ଲକ୍ଷ୍ୟ ହେଉଛି ଓଡ଼ିଶାର ୩୦ଟି ଜିଲ୍ଲାର ଛାତ୍ରଛାତ୍ରୀ, ଗବେଷକ, ଷ୍ଟାର୍ଟଅପ୍ ଏବଂ ଶିଳ୍ପସଂସ୍ଥାମାନଙ୍କୁ ବିଶ୍ୱସ୍ତରୀୟ AI ବଜାର ସହିତ ସଂଯୋଗ କରିବା ।",
            "hi": "ओडिशा AI नेक्सस के बारे में। हमारा उद्देश्य ओडिशा के 30 जिलों के छात्रों, शोधकर्ताओं, स्टार्टअप्स और उद्योगों को वैश्विक आर्टिफिशियल इंटेलिजेंस बाज़ारों से जोड़ना है।"
        }.get(lang)
    )

    # Community Disclaimer Box
    st.markdown(f"""
    <div class="disclaimer-box" style="border-left-color: #F59E0B;">
        ⚠️ <b>{t("community_disclaimer")}</b>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1])

    with col1:
        mission_text = {
            "en": """
            ### 🎯 The Purpose & Vision
            Odisha possesses tremendous foundational strengths: premier technical institutes 
            (IIT Bhubaneswar, NIT Rourkela, IIIT, VSSUT, KIIT, SOA, Silicon), massive industrial 
            corridors in steel, mining, and ports, rich biodiversity in Chilika and Similipal, 
            and world-renowned disaster management operational leadership.

            However, students, researchers, early-stage founders, heavy industries, and overseas buyers 
            have traditionally operated in silos. **Odisha AI Nexus** is designed as a practical, open digital 
            bridge to:
            1. **Give Visibility to Grassroots Innovation:** Enable student researchers and startup builders to showcase working code, models, and prototypes to enterprise adopters.
            2. **Ground AI in Real Regional Problems:** Channel talent toward critical challenges in flash floods, blast furnace safety, agricultural pest mitigation, and handloom preservation.
            3. **Bridge Local to Global:** Guide innovators through the technical, documentation, and compliance steps needed to export software internationally.
            """,
            "or": """
            ### 🎯 ଲକ୍ଷ୍ୟ ଏବଂ ଦୂରଦୃଷ୍ଟି
            ଓଡ଼ିଶାର ପ୍ରଚୁର ସମ୍ଭାବନା ରହିଛି: ଶ୍ରେଷ୍ଠ ବୈଷୟିକ ଶିକ୍ଷାନୁଷ୍ଠାନ (IIT ଭୁବନେଶ୍ୱର, NIT ରାଉରକେଲା, IIIT, VSSUT, KIIT, SOA, ସିଲିକନ୍), 
            ଇସ୍ପାତ, ଖଣି ଓ ବନ୍ଦର ଶିଳ୍ପ, ଚିଲିକା ଓ ଶିମିଳିପାଳର ଜୈବ-ବିବିଧତା, ଏବଂ ବିଶ୍ୱପ୍ରସିଦ୍ଧ ବିପର୍ଯ୍ୟୟ ପରିଚାଳନା ଦକ୍ଷତା ।

            **ଓଡ଼ିଶା AI ନେକ୍ସସ୍** ଏକ ମୁକ୍ତ ଡିଜିଟାଲ୍ ସେତୁ ଯାହା:
            1. **ସ୍ଥାନୀୟ ଉଦ୍ଭାବନକୁ ଦୃଶ୍ୟମାନ କରେ:** ଛାତ୍ରଛାତ୍ରୀ ଓ ଷ୍ଟାର୍ଟଅପ୍‌ମାନଙ୍କୁ ସେମାନଙ୍କର AI ପ୍ରକଳ୍ପ ପ୍ରଦର୍ଶନ କରିବାକୁ ସୁଯୋଗ ଦିଏ ।
            2. **ଆଞ୍ଚଳିକ ସମସ୍ୟାର ସମାଧାନ କରେ:** ବନ୍ୟା, ବାତ୍ୟା, କୃଷି ରୋଗ ଏବଂ ସମ୍ବଲପୁରୀ ହସ୍ତତନ୍ତ ସଂରକ୍ଷଣରେ AI ପ୍ରୟୋଗ କରେ ।
            3. **ସ୍ଥାନୀୟରୁ ବିଶ୍ୱସ୍ତରୀୟ:** ଓଡ଼ିଶାର ପ୍ରତିଭାଙ୍କୁ ବିଶ୍ୱ ବଜାର ସହିତ ସଂଯୋଗ କରେ ।
            """,
            "hi": """
            ### 🎯 उद्देश्य एवं दृष्टिकोण
            ओडिशा में अपार क्षमताएं हैं: प्रमुख तकनीकी संस्थान (IIT भुवनेश्वर, NIT राउरकेला, IIIT, VSSUT, KIIT, SOA), 
            इस्पात, खनन और बंदरगाह के औद्योगिक गलियारे, और आपदा प्रबंधन में विश्वस्तरीय नेतृत्व।

            **ओडिशा AI नेक्सस** एक खुला डिजिटल सेतु है जो:
            1. **जमीनी नवाचार को दृश्यता प्रदान करता है:** छात्रों और स्टार्टअप्स को अपने AI प्रोजेक्ट्स प्रदर्शित करने का अवसर देता है।
            2. **क्षेत्रीय समस्याओं का समाधान करता है:** बाढ़, कृषि कीटों और हथकरघा संरक्षण में AI का अनुप्रयोग करता है।
            3. **स्थानीय से वैश्विक:** ओडिशा की प्रतिभा को अंतरराष्ट्रीय बाज़ारों से जोड़ता है।
            """
        }.get(lang, "")
        st.markdown(mission_text)

    with col2:
        roles_text = {
            "en": """
            ### 🤝 Complementary Ecosystem Role
            Odisha AI Nexus does not replace or compete with institutional entities. Instead, it serves as an agile, bottom-up discovery layer that complements:
            - **Odisha AI Mission:** Supporting state talent discovery and grassroots community engagement.
            - **Startup Odisha & O-Hub:** Providing an early sandbox where university ideas can be stress-tested before formal incubation.
            - **Academic Cohorts:** Allowing cross-institutional collaboration between universities across all 30 districts.
            """,
            "or": """
            ### 🤝 ପରିପୂରକ ଇକୋସିଷ୍ଟମ୍ ଭୂମିକା
            ଓଡ଼ିଶା AI ନେକ୍ସସ୍ କୌଣସି ସରକାରୀ ସଂସ୍ଥା ସହିତ ପ୍ରତିଦ୍ୱନ୍ଦ୍ୱିତା କରେ ନାହିଁ । ଏହା ଏକ ପରିପୂରକ ସହଯୋଗୀ ପ୍ଲାଟଫର୍ମ:
            - **Odisha AI Mission:** ରାଜ୍ୟସ୍ତରୀୟ ପ୍ରତିଭା ଚିହ୍ନଟ ଏବଂ ସମ୍ପ୍ରଦାୟ ସହଭାଗିତା ।
            - **Startup Odisha & O-Hub:** ବିଶ୍ୱବିଦ୍ୟାଳୟ ସ୍ତରର AI ଧାରଣାଗୁଡ଼ିକର ପ୍ରାଥମିକ ପରୀକ୍ଷଣ ।
            - **ଶିକ୍ଷାନୁଷ୍ଠାନ ସହଯୋଗ:** ୩୦ଟି ଜିଲ୍ଲାର କଲେଜ ମଧ୍ୟରେ ମିଳିତ ଗବେଷଣା ।
            """,
            "hi": """
            ### 🤝 पूरक इकोसिस्टम भूमिका
            ओडिशा AI नेक्सस किसी संस्था का विकल्प नहीं है, बल्कि एक पूरक सहयोगी मंच है:
            - **Odisha AI Mission:** प्रतिभा खोज और सामुदायिक सहभागिता को सशक्त बनाना।
            - **Startup Odisha & O-Hub:** औपचारिक इनक्यूबेशन से पूर्व शुरुआती विचारों का परीक्षण।
            - **शैक्षणिक सहयोग:** 30 जिलों के संस्थानों के बीच परस्पर अनुसंधान को बढ़ावा देना।
            """
        }.get(lang, "")
        st.markdown(roles_text)

    st.write("")
    st.divider()

    # Phased Strategic Roadmap
    st.markdown("### 🗺️ " + {"en": "Strategic Roadmap", "or": "ରୋଡମ୍ୟାପ୍ (କାର୍ଯ୍ୟ ଯୋଜନା)", "hi": "रणनीतिक रोडमैप"}.get(lang, "Strategic Roadmap"))

    roadmap_steps = [
        {
            "phase": "Phase 1: Foundation (Current Release)",
            "status": "COMPLETED & OPERATIONAL",
            "color": "#10B981",
            "desc": "Built core 100% local platform: persistent SQLite architecture, Project Registry, Talent Exchange, Industry Challenge Board, transparent Opportunity Explorer scoring, Global Readiness checklist, and ReportLab PDF reporting."
        },
        {
            "phase": "Phase 2: Multilingual Odia & Hindi UI + Voice Accessibility",
            "status": "COMPLETED & OPERATIONAL (Active)",
            "color": "#00F0FF",
            "desc": "Full tri-lingual localization across English, Odia (ଓଡ଼ିଆ), and Hindi (हिन्दी). Embedded Web Speech API text-to-speech audio reader and voice microphone search for inclusive accessibility."
        },
        {
            "phase": "Phase 3: Community Hackathons & Industry Pilots",
            "status": "PLANNED (H2 2026)",
            "color": "#38BDF8",
            "desc": "Facilitate direct university hackathons, student mentor circles, and structured pilot submissions with local MSMEs and cooperatives."
        },
        {
            "phase": "Phase 4: Open Geospatial & Public Hydrology Telemetry",
            "status": "PLANNED (2027)",
            "color": "#818CF8",
            "desc": "Investigate integration with open public datasets (e.g. data.gov.in, ISRO Bhuvan satellite feeds, open telemetry) for real-time model benchmarking."
        },
        {
            "phase": "Phase 5: Responsible AI Governance & Credentialing",
            "status": "PLANNED (2028)",
            "color": "#A855F7",
            "desc": "Automated bias audits, carbon footprint estimation for local model training, and cryptographically verified badges for student contributors."
        }
    ]

    for step in roadmap_steps:
        st.markdown(f"""
        <div class="nexus-card">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                <span style="font-weight: 700; font-size: 1.05rem; color: #FFFFFF;">{step['phase']}</span>
                <span style="font-size: 0.75rem; font-weight: 700; color: {step['color']}; border: 1px solid {step['color']}; padding: 2px 8px; border-radius: 4px;">
                    {step['status']}
                </span>
            </div>
            <div style="margin-top: 6px; font-size: 0.88rem; color: #CBD5E1; line-height: 1.4;">
                {step['desc']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.divider()

    # Security & Privacy Declarations
    st.markdown("### 🔒 " + {"en": "Architectural Transparency & Privacy", "or": "ସ୍ଥାପତ୍ୟ ସ୍ୱଚ୍ଛତା ଏବଂ ଗୋପନୀୟତା", "hi": "आर्किटेक्चरल पारदर्शिता एवं गोपनीयता"}.get(lang, "Security"))
    sec_col1, sec_col2 = st.columns(2)

    with sec_col1:
        st.markdown("""
        **Data Persistence & Privacy:**
        - All application records persist in an embedded local SQLite database.
        - Direct contact emails in the Talent Directory are masked to prevent automated scraping.
        - Cryptographic HMAC-SHA256 session management with persistent security audit logs.
        """)

    with sec_col2:
        st.markdown("""
        **Algorithmic Transparency:**
        - The Opportunity Explorer and Talent Matcher use deterministic, inspectable algorithms.
        - No paid cloud dependencies or third-party tracking services.
        - Complete tri-lingual voice and visual accessibility.
        """)
