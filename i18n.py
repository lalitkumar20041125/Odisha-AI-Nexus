"""
Internationalization (i18n) and Multilingual Localization Engine for Odisha AI Nexus.
Supports English (en), Odia (or - ଓଡ଼ିଆ), and Hindi (hi - हिन्दी).
Provides comprehensive translation mappings for UI, forms, sectors, KPIs, alerts,
readiness checklist, and speech/audio accessibility guidance.
"""

from typing import Dict, Any, Optional, List
import streamlit as st

SUPPORTED_LANGUAGES = {
    "en": {"name": "English", "flag": "🇬🇧", "native": "English", "speech_code": "en-IN"},
    "or": {"name": "Odia", "flag": "🇮🇳", "native": "ଓଡ଼ିଆ", "speech_code": "or-IN"},
    "hi": {"name": "Hindi", "flag": "🇮🇳", "native": "हिन्दी", "speech_code": "hi-IN"},
}

DEFAULT_LANGUAGE = "en"

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    # Brand & Tagline
    "app_name": {
        "en": "Odisha AI Nexus",
        "or": "ଓଡ଼ିଶା AI ନେକ୍ସସ୍",
        "hi": "ओडिशा AI नेक्सस",
    },
    "tagline": {
        "en": "Local Innovation. Global Impact.",
        "or": "ସ୍ଥାନୀୟ ଉଦ୍ଭାବନ । ବିଶ୍ୱସ୍ତରୀୟ ପ୍ରଭାବ ।",
        "hi": "स्थानीय नवाचार । वैश्विक प्रभाव ।",
    },
    "community_disclaimer": {
        "en": "Odisha AI Nexus is an independent, community-driven ecosystem platform. It is not officially affiliated with the Government of Odisha or Startup Odisha.",
        "or": "ଓଡ଼ିଶା AI ନେକ୍ସସ୍ ଏକ ସ୍ୱତନ୍ତ୍ର, ସମ୍ପ୍ରଦାୟ-ଚାଳିତ ଇକୋସିଷ୍ଟମ୍ ପ୍ଲାଟଫର୍ମ ଅଟେ । ଏହା ଓଡ଼ିଶା ସରକାର କିମ୍ବା ଷ୍ଟାର୍ଟଅପ୍ ଓଡ଼ିଶା ସହିତ ସରକାରୀ ଭାବରେ ଜଡ଼ିତ ନୁହେଁ ।",
        "hi": "ओडिशा AI नेक्सस एक स्वतंत्र, समुदाय-संचालित इकोसिस्टम प्लेटफॉर्म है। यह ओडिशा सरकार या स्टार्टअप ओडिशा से आधिकारिक रूप से संबद्ध नहीं है।",
    },

    # Navigation
    "nav_menu": {
        "en": "Navigation Menu",
        "or": "ମୁଖ୍ୟ ମେନୁ (Navigation)",
        "hi": "मुख्य मेन्यू",
    },
    "nav_dashboard": {
        "en": "🌟 Executive Dashboard",
        "or": "🌟 କାର୍ଯ୍ୟନିର୍ବାହୀ ଡ୍ୟାସବୋର୍ଡ",
        "hi": "🌟 कार्यकारी डैशबोर्ड",
    },
    "nav_projects": {
        "en": "🚀 AI Project Registry",
        "or": "🚀 AI ପ୍ରକଳ୍ପ ରେଜିଷ୍ଟ୍ରି",
        "hi": "🚀 AI प्रोजेक्ट रजिस्ट्री",
    },
    "nav_opportunity": {
        "en": "💡 AI Opportunity Explorer",
        "or": "💡 AI ସୁଯୋଗ ଅନୁସନ୍ଧାନ",
        "hi": "💡 AI अवसर एक्सप्लोरर",
    },
    "nav_talent": {
        "en": "👥 Odisha AI Talent Exchange",
        "or": "👥 ଓଡ଼ିଶା AI ପ୍ରତିଭା ବିନିମୟ",
        "hi": "👥 ओडिशा AI प्रतिभा विनिमय",
    },
    "nav_challenges": {
        "en": "🏭 Industry Challenge Board",
        "or": "🏭 ଶିଳ୍ପ ଚ୍ୟାଲେଞ୍ଜ ବୋର୍ଡ",
        "hi": "🏭 उद्योग चुनौती बोर्ड",
    },
    "nav_readiness": {
        "en": "🌐 Global Market Readiness",
        "or": "🌐 ବିଶ୍ୱ ବଜାର ପ୍ରସ୍ତୁତି",
        "hi": "🌐 वैश्विक बाज़ार तैयारी",
    },
    "nav_reports": {
        "en": "📊 Reports & Data Export",
        "or": "📊 ରିପୋର୍ଟ ଏବଂ ଡାଟା ରପ୍ତାନି",
        "hi": "📊 रिपोर्ट एवं डेटा निर्यात",
    },
    "nav_about": {
        "en": "ℹ️ About & Roadmap",
        "or": "ℹ️ ପ୍ଲାଟଫର୍ମ ବିଷୟରେ ଏବଂ ରୋଡମ୍ୟାପ୍",
        "hi": "ℹ️ मंच के बारे में एवं रोडमैप",
    },

    # Language selection
    "select_language": {
        "en": "Language / ଭାଷା / भाषा",
        "or": "ଭାଷା ଚୟନ କରନ୍ତୁ",
        "hi": "भाषा चुनें",
    },

    # Data scope
    "data_controller": {
        "en": "Data Scope Controller",
        "or": "ଡାଟା ପରିସର ନିୟନ୍ତ୍ରଣ",
        "hi": "डेटा दायरा नियंत्रक",
    },
    "include_demo": {
        "en": "Include Demonstration Records",
        "or": "ପ୍ରଦର୍ଶନୀ / ଡେମୋ ରେକର୍ଡ ଦେଖାନ୍ତୁ",
        "hi": "प्रदर्शन / डेमो रिकॉर्ड शामिल करें",
    },
    "mode_all": {
        "en": "Mode: All Data (Demo + User Submissions)",
        "or": "ମୋଡ୍: ସମସ୍ତ ଡାଟା (ଡେମୋ + ବ୍ୟବହାରକାରୀ ଦାଖଲ)",
        "hi": "मोड: सभी डेटा (डेमो + उपयोगकर्ता प्रस्तुतियां)",
    },
    "mode_verified": {
        "en": "Mode: Verified Submissions Only",
        "or": "ମୋଡ୍: କେବଳ ଯାଞ୍ଚ ହୋଇଥିବା ପ୍ରକୃତ ଦାଖଲ",
        "hi": "मोड: केवल सत्यापित वास्तविक प्रस्तुतियां",
    },

    # KPIs
    "kpi_projects": {
        "en": "Registered AI Projects",
        "or": "ପଞ୍ଜୀକୃତ AI ପ୍ରକଳ୍ପ",
        "hi": "पंजीकृत AI प्रोजेक्ट्स",
    },
    "kpi_talent": {
        "en": "Registered AI Talent",
        "or": "ପଞ୍ଜୀକୃତ AI ପ୍ରତିଭା",
        "hi": "पंजीकृत AI प्रतिभा",
    },
    "kpi_challenges": {
        "en": "Industry Challenges",
        "or": "ଶିଳ୍ପ ସମସ୍ୟା / ଚ୍ୟାଲେଞ୍ଜ",
        "hi": "उद्योग चुनौतियां",
    },
    "kpi_readiness": {
        "en": "Avg. Global Readiness",
        "or": "ହାରାହାରି ବିଶ୍ୱ ପ୍ରସ୍ତୁତି",
        "hi": "औसत वैश्विक तैयारी",
    },
    "kpi_real": {
        "en": "Real",
        "or": "ପ୍ରକୃତ",
        "hi": "वास्तविक",
    },
    "kpi_demo": {
        "en": "Demo",
        "or": "ଡେମୋ",
        "hi": "डेमो",
    },

    # Authentication & User State
    "sign_in_google": {
        "en": "Sign in with Google",
        "or": "Google ଦ୍ୱାରା ଲଗଇନ୍ କରନ୍ତୁ",
        "hi": "Google से साइन इन करें",
    },
    "sign_out": {
        "en": "Sign Out",
        "or": "ଲଗଆଉଟ୍ କରନ୍ତୁ",
        "hi": "साइन आउट",
    },
    "manage_profile": {
        "en": "Manage Profile",
        "or": "ପ୍ରୋଫାଇଲ୍ ପରିଚାଳନା",
        "hi": "प्रोफ़ाइल प्रबंधित करें",
    },
    "badge_verified": {
        "en": "Verified Submission",
        "or": "ଯାଞ୍ଚ ହୋଇଥିବା ଦାଖଲ",
        "hi": "सत्यापित प्रस्तुति",
    },
    "badge_demo": {
        "en": "Demo",
        "or": "ପରୀକ୍ଷଣ ଡାଟା",
        "hi": "डेमो डेटा",
    },
    "badge_local_sync": {
        "en": "Local DB Synced",
        "or": "ସ୍ଥାନୀୟ ଡାଟାବେସ୍ ସଂରକ୍ଷିତ",
        "hi": "स्थानीय डेटाबेस सुरक्षित",
    },

    # Common Actions & Buttons
    "search_placeholder": {
        "en": "Search by keywords, tech, or title...",
        "or": "ଶବ୍ଦ, ପ୍ରଯୁକ୍ତି କିମ୍ବା ଶୀର୍ଷକ ଦ୍ୱାରା ସନ୍ଧାନ କରନ୍ତୁ...",
        "hi": "कीवर्ड, तकनीक या शीर्षक से खोजें...",
    },
    "filter_sector": {
        "en": "Filter by Sector",
        "or": "କ୍ଷେତ୍ର ଅନୁଯାୟୀ ଫିଲ୍ଟର୍",
        "hi": "क्षेत्र के अनुसार फ़िल्टर करें",
    },
    "filter_status": {
        "en": "Filter by Status",
        "or": "ସ୍ଥିତି ଅନୁଯାୟୀ ଫିଲ୍ଟର୍",
        "hi": "स्थिति के अनुसार फ़िल्टर करें",
    },
    "all_sectors": {
        "en": "All Sectors",
        "or": "ସମସ୍ତ କ୍ଷେତ୍ର",
        "hi": "सभी क्षेत्र",
    },
    "all_statuses": {
        "en": "All Statuses",
        "or": "ସମସ୍ତ ସ୍ଥିତି",
        "hi": "सभी स्थितियां",
    },
    "export_csv": {
        "en": "Export to CSV",
        "or": "CSV ଡାଉନଲୋଡ୍ କରନ୍ତୁ",
        "hi": "CSV डाउनलोड करें",
    },
    "download_pdf": {
        "en": "Download Executive Briefing (PDF)",
        "or": "କାର୍ଯ୍ୟନିର୍ବାହୀ ରିପୋର୍ଟ ଡାଉନଲୋଡ୍ (PDF)",
        "hi": "कार्यकारी रिपोर्ट डाउनलोड करें (PDF)",
    },
    "submit": {
        "en": "Submit",
        "or": "ଦାଖଲ କରନ୍ତୁ",
        "hi": "जमा करें",
    },
    "save": {
        "en": "Save",
        "or": "ସଂରକ୍ଷଣ କରନ୍ତୁ",
        "hi": "सुरक्षित करें",
    },
    "purge_demo": {
        "en": "Purge Demo",
        "or": "ଡେମୋ ହଟାନ୍ତୁ",
        "hi": "डेमो हटाएं",
    },
    "reseed_demo": {
        "en": "Re-Seed Demo",
        "or": "ଡେମୋ ପୁନଃସ୍ଥାପନ",
        "hi": "डेमो पुनर्स्थापित करें",
    },
    "database_tools": {
        "en": "Database Tools",
        "or": "ଡାଟାବେସ୍ ଉପକରଣ",
        "hi": "डेटाबेस उपकरण",
    },

    # Sectors translated
    "sec_agri": {
        "en": "Agriculture & Food Security",
        "or": "କୃଷି ଏବଂ ଖାଦ୍ୟ ସୁରକ୍ଷା",
        "hi": "कृषि एवं खाद्य सुरक्षा",
    },
    "sec_disaster": {
        "en": "Disaster Management & Climate Resilience",
        "or": "ବିପର୍ଯ୍ୟୟ ପରିଚାଳନା ଏବଂ ଜଳବାୟୁ ସହନଶୀଳତା",
        "hi": "आपदा प्रबंधन एवं जलवायु लचीलापन",
    },
    "sec_mining": {
        "en": "Mining & Mineral Exploration",
        "or": "ଖଣି ଏବଂ ଖଣିଜ ଅନୁସନ୍ଧାନ",
        "hi": "खनन एवं खनिज अन्वेषण",
    },
    "sec_steel": {
        "en": "Steel & Heavy Metallurgy",
        "or": "ଇସ୍ପାତ ଏବଂ ଭାରୀ ଧାତୁବିଜ୍ଞାନ",
        "hi": "इस्पात एवं भारी धातु विज्ञान",
    },
    "sec_ports": {
        "en": "Logistics, Ports & Marine Economy",
        "or": "ଲଜିଷ୍ଟିକ୍ସ, ବନ୍ଦର ଏବଂ ସାମୁଦ୍ରିକ ଅର୍ଥନୀତି",
        "hi": "लॉजिस्टिक्स, बंदरगाह एवं समुद्री अर्थव्यवस्था",
    },
    "sec_health": {
        "en": "Healthcare & Rural MedTech",
        "or": "ସ୍ୱାସ୍ଥ୍ୟସେବା ଏବଂ ଗ୍ରାମୀଣ ମେଡଟେକ୍",
        "hi": "स्वास्थ्य सेवा एवं ग्रामीण मेडटेक",
    },
    "sec_heritage": {
        "en": "Tourism, Temple Tech & Heritage Preservation",
        "or": "ପର୍ଯ୍ୟଟନ, ମନ୍ଦିର ପ୍ରଯୁକ୍ତି ଏବଂ ଐତିହ୍ୟ ସଂରକ୍ଷଣ",
        "hi": "पर्यटन, मंदिर प्रौद्योगिकी एवं विरासत संरक्षण",
    },
    "sec_handloom": {
        "en": "Handlooms, Handicrafts & MSME Artisans",
        "or": "ହସ୍ତତନ୍ତ, ହସ୍ତଶିଳ୍ପ ଏବଂ କାରିଗର ସଶକ୍ତୀକରଣ",
        "hi": "हथकरघा, हस्तशिल्प एवं कारीगर सशक्तिकरण",
    },

    # Section Headers
    "sector_chart_title": {
        "en": "Project Distribution by Sector",
        "or": "କ୍ଷେତ୍ର ଅନୁଯାୟୀ ପ୍ରକଳ୍ପ ବଣ୍ଟନ",
        "hi": "क्षेत्र के अनुसार प्रोजेक्ट वितरण",
    },
    "stage_chart_title": {
        "en": "Development Stage Maturity",
        "or": "ବିକାଶ ପର୍ଯ୍ୟାୟ ପରିପକ୍ୱତା",
        "hi": "विकास चरण परिपक्वता",
    },
    "top_projects_title": {
        "en": "Promising Registered AI Solutions (Ranked by Readiness)",
        "or": "ପ୍ରତିଶ୍ରୁତିବଦ୍ଧ AI ସମାଧାନ (ପ୍ରସ୍ତୁତି କ୍ରମାନୁସାରେ)",
        "hi": "होनहार AI समाधान (तैयारी के आधार पर)",
    },
    "urgent_challenges_title": {
        "en": "High-Priority Industry Challenges Awaiting AI Teams",
        "or": "AI ଦଳକୁ ଅପେକ୍ଷା କରିଥିବା ଜରୁରୀ ଶିଳ୍ପ ସମସ୍ୟା",
        "hi": "AI टीमों की प्रतीक्षा में उच्च प्राथमिकता वाली उद्योग चुनौतियां",
    },

    # Speech / Audio Accessibility
    "audio_helper": {
        "en": "🔊 Listen / ଶୁଣନ୍ତୁ / सुनें",
        "or": "🔊 ଭଏସ୍ ସହାୟକ (ଶୁଣନ୍ତୁ)",
        "hi": "🔊 आवाज में सुनें",
    },
    "voice_guide_title": {
        "en": "🎙️ Odisha AI Voice Companion",
        "or": "🎙️ ଓଡ଼ିଶା AI ବାକ୍ ସହାୟକ (ଭଏସ୍ ଗାଇଡ୍)",
        "hi": "🎙️ ओडिशा AI आवाज साथी (वॉइस गाइड)",
    },
    "voice_guide_desc": {
        "en": "Listen to spoken narration or search in your preferred language.",
        "or": "ନିଜ ମାତୃଭାଷାରେ ଶୁଣନ୍ତୁ କିମ୍ବା କହି ସନ୍ଧାନ କରନ୍ତୁ ।",
        "hi": "अपनी पसंदीदा भाषा में सुनें या बोलकर खोजें।",
    },
    "btn_listen_page": {
        "en": "🔊 Read Overview Aloud",
        "or": "🔊 ବିବରଣୀ ଶୁଣନ୍ତୁ",
        "hi": "🔊 विवरण सुनें",
    },
    "btn_pause_audio": {
        "en": "⏸️ Pause",
        "or": "⏸️ ରୋକନ୍ତୁ",
        "hi": "⏸️ रोकें",
    },
    "btn_stop_audio": {
        "en": "⏹️ Stop",
        "or": "⏹️ ବନ୍ଦ କରନ୍ତୁ",
        "hi": "⏹️ बंद करें",
    },
    "voice_search_btn": {
        "en": "🎙️ Speak to Search",
        "or": "🎙️ କହି ସନ୍ଧାନ କରନ୍ତୁ",
        "hi": "🎙️ बोलकर खोजें",
    },
    "voice_listening": {
        "en": "Listening... Please speak now",
        "or": "ଶୁଣୁଛି... ଦୟାକରି କୁହନ୍ତୁ",
        "hi": "सुन रहा हूँ... कृपया बोलिए",
    },
    "voice_not_supported": {
        "en": "Speech Recognition is supported in Chrome, Edge, and Android browsers.",
        "or": "ବାକ୍ ଚିହ୍ନଟ Chrome, Edge ଏବଂ Android ବ୍ରାଉଜର୍ରେ ଉପଲବ୍ଧ ଅଟେ ।",
        "hi": "वॉइस सर्च Chrome, Edge और Android ब्राउज़र में समर्थित है।",
    },

    # Projects View Specific
    "projects_heading": {
        "en": "🚀 AI Project Registry",
        "or": "🚀 AI ପ୍ରକଳ୍ପ ରେଜିଷ୍ଟ୍ରି",
        "hi": "🚀 AI प्रोजेक्ट रजिस्ट्री",
    },
    "projects_subheading": {
        "en": "Discover, track, and collaborate on applied AI solutions engineered across Odisha.",
        "or": "ଓଡ଼ିଶାରେ ବିକଶିତ ହେଉଥିବା ପ୍ରୟୋଗାତ୍ମକ AI ସମାଧାନଗୁଡ଼ିକ ଆବିଷ୍କାର କରନ୍ତୁ ଏବଂ ସହଯୋଗ କରନ୍ତୁ ।",
        "hi": "ओडिशा भर में विकसित अनुप्रयुक्त AI समाधानों की खोज करें और सहयोग करें।",
    },
    "tab_browse_projects": {
        "en": "🔍 Browse & Filter Projects",
        "or": "🔍 ପ୍ରକଳ୍ପ ଅନୁସନ୍ଧାନ ଓ ଫିଲ୍ଟର୍",
        "hi": "🔍 प्रोजेक्ट खोजें एवं फ़िल्टर करें",
    },
    "tab_register_project": {
        "en": "➕ Register New AI Project",
        "or": "➕ ନୂତନ AI ପ୍ରକଳ୍ପ ପଞ୍ଜୀକରଣ",
        "hi": "➕ नया AI प्रोजेक्ट पंजीकृत करें",
    },
    "lead_innovator": {
        "en": "Lead Innovator / Team",
        "or": "ମୁଖ୍ୟ ଉଦ୍ଭାବକ / ଦଳ",
        "hi": "प्रमुख नवाचारक / दल",
    },
    "organization": {
        "en": "Organization / Institution",
        "or": "ସଂସ୍ଥା / ଶିକ୍ଷାନୁଷ୍ଠାନ",
        "hi": "संस्था / संस्थान",
    },
    "district": {
        "en": "District in Odisha",
        "or": "ଓଡ଼ିଶାର ଜିଲ୍ଲା",
        "hi": "ओडिशा का जिला",
    },
    "project_title_label": {
        "en": "Project Title *",
        "or": "ପ୍ରକଳ୍ପ ଶୀର୍ଷକ *",
        "hi": "प्रोजेक्ट का नाम *",
    },
    "project_tagline_label": {
        "en": "One-Line Tagline",
        "or": "ଏକ ଧାଡ଼ିଆ ପରିଚୟ (ଟ୍ୟାଗଲାଇନ୍)",
        "hi": "एक पंक्ति का परिचय (टैगलाइन)",
    },
    "problem_description_label": {
        "en": "Detailed Description & Problem Solved *",
        "or": "ବିସ୍ତୃତ ବିବରଣୀ ଏବଂ ସମାଧାନ ହୋଇଥିବା ସମସ୍ୟା *",
        "hi": "विस्तृत विवरण एवं हल की गई समस्या *",
    },
    "target_beneficiaries_label": {
        "en": "Target Beneficiaries",
        "or": "ଲକ୍ଷିତ ହିତାଧିକାରୀ",
        "hi": "लक्षित लाभार्थी",
    },
    "tech_stack_label": {
        "en": "Key Technologies & Libraries",
        "or": "ମୁଖ୍ୟ ପ୍ରଯୁକ୍ତି ଏବଂ ଲାଇବ୍ରେରୀ",
        "hi": "प्रमुख तकनीकें एवं लाइब्रेरी",
    },
    "repo_url_label": {
        "en": "Repository, Paper, or Demo URL",
        "or": "ରେପୋଜିଟୋରୀ / ଡେମୋ ଲିଙ୍କ୍",
        "hi": "रिपोजिटरी / डेमो लिंक",
    },
    "btn_submit_project": {
        "en": "🚀 Submit Project to Registry",
        "or": "🚀 ରେଜିଷ୍ଟ୍ରିରେ ପ୍ରକଳ୍ପ ଦାଖଲ କରନ୍ତୁ",
        "hi": "🚀 रजिस्ट्री में प्रोजेक्ट जमा करें",
    },

    # Opportunity View Specific
    "opp_heading": {
        "en": "💡 AI Opportunity Explorer",
        "or": "💡 AI ସୁଯୋଗ ଅନୁସନ୍ଧାନ (Opportunity Explorer)",
        "hi": "💡 AI अवसर एक्सप्लोरर",
    },
    "opp_subheading": {
        "en": "Heuristic decision-support system to stress-test AI solutions across feasibility, regional relevance, and export potential.",
        "or": "ସମ୍ଭାବ୍ୟତା, ଆଞ୍ଚଳିକ ପ୍ରାସଙ୍ଗିକତା ଏବଂ ରପ୍ତାନି ସାମର୍ଥ୍ୟ ପରୀକ୍ଷା କରିବା ପାଇଁ ପାରଦର୍ଶୀ ମାର୍ଗଦର୍ଶକ ।",
        "hi": "व्यवहार्यता, क्षेत्रीय प्रासंगिकता और निर्यात क्षमता का परीक्षण करने हेतु पारदर्शी निर्णय-सहायक प्रणाली।",
    },
    "tab_eval_idea": {
        "en": "🧪 Evaluate an AI Idea",
        "or": "🧪 ନୂତନ AI ଧାରଣା ମୂଲ୍ୟାଙ୍କନ",
        "hi": "🧪 नए AI विचार का मूल्यांकन",
    },
    "tab_eval_history": {
        "en": "📜 Saved Assessments Archive",
        "or": "📜 ସଂରକ୍ଷିତ ମୂଲ୍ୟାଙ୍କନ ଇତିହାସ",
        "hi": "📜 सहेजे गए मूल्यांकन इतिहास",
    },
    "btn_run_opp_assessment": {
        "en": "⚡ Run Opportunity Assessment",
        "or": "⚡ ସୁଯୋଗ ମୂଲ୍ୟାଙ୍କନ ଚଲାନ୍ତୁ",
        "hi": "⚡ अवसर मूल्यांकन चलाएं",
    },

    # Talent Exchange Specific
    "talent_heading": {
        "en": "👥 Odisha AI Talent Exchange",
        "or": "👥 ଓଡ଼ିଶା AI ପ୍ରତିଭା ବିନିମୟ",
        "hi": "👥 ओडिशा AI प्रतिभा विनिमय",
    },
    "talent_subheading": {
        "en": "Connecting students, ML engineers, researchers, and domain experts across Odisha's 30 districts with high-impact AI projects.",
        "or": "ଓଡ଼ିଶାର ୩୦ଟି ଜିଲ୍ଲାର ଛାତ୍ରଛାତ୍ରୀ, ଇଞ୍ଜିନିୟର ଏବଂ ବିଶେଷଜ୍ଞଙ୍କୁ AI ପ୍ରକଳ୍ପ ସହ ଯୋଡ଼ିବା ।",
        "hi": "ओडिशा के 30 जिलों के छात्रों, इंजीनियरों और विशेषज्ञों को उच्च-प्रभावशाली AI प्रोजेक्ट्स से जोड़ना।",
    },
    "tab_explore_talent": {
        "en": "🔍 Explore Talent Directory",
        "or": "🔍 ପ୍ରତିଭା ତାଲିକା ଅନୁସନ୍ଧାନ",
        "hi": "🔍 प्रतिभा निर्देशिका देखें",
    },
    "tab_smart_matching": {
        "en": "🎯 AI Synergy Matcher (Project ⇄ Talent)",
        "or": "🎯 ସ୍ମାର୍ଟ ମେଳକ (ପ୍ରକଳ୍ପ ⇄ ପ୍ରତିଭା)",
        "hi": "🎯 स्मार्ट मिलान (प्रोजेक्ट ⇄ प्रतिभा)",
    },
    "tab_register_talent": {
        "en": "➕ Register Your Profile",
        "or": "➕ ନିଜର ପ୍ରୋଫାଇଲ୍ ପଞ୍ଜୀକରଣ କରନ୍ତୁ",
        "hi": "➕ अपनी प्रोफ़ाइल पंजीकृत करें",
    },

    # Challenges Specific
    "challenges_heading": {
        "en": "🏭 Industry Challenge Board",
        "or": "🏭 ଶିଳ୍ପ ଚ୍ୟାଲେଞ୍ଜ ବୋର୍ଡ",
        "hi": "🏭 उद्योग चुनौती बोर्ड",
    },
    "challenges_subheading": {
        "en": "Real-world operational bottlenecks submitted by industries, public departments, and MSMEs across Odisha.",
        "or": "ଓଡ଼ିଶାର ଶିଳ୍ପ, ସରକାରୀ ବିଭାଗ ଏବଂ MSME ଦ୍ୱାରା ଉପସ୍ଥାପିତ ବାସ୍ତବ ସମସ୍ୟା ।",
        "hi": "ओडिशा के उद्योगों, सरकारी विभागों और एमएसएमई द्वारा प्रस्तुत वास्तविक समस्याएं।",
    },
    "tab_active_challenges": {
        "en": "🔍 Active Industry Challenges",
        "or": "🔍 ସକ୍ରିୟ ଶିଳ୍ପ ସମସ୍ୟା",
        "hi": "🔍 सक्रिय उद्योग चुनौतियां",
    },
    "tab_submit_challenge": {
        "en": "📢 Submit a Problem Statement",
        "or": "📢 ନୂତନ ଶିଳ୍ପ ସମସ୍ୟା ଦାଖଲ କରନ୍ତୁ",
        "hi": "📢 नई उद्योग समस्या प्रस्तुत करें",
    },

    # Market Readiness Specific
    "readiness_heading": {
        "en": "🌐 Global Market Readiness Explorer",
        "or": "🌐 ବିଶ୍ୱ ବଜାର ପ୍ରସ୍ତୁତି ପରୀକ୍ଷକ",
        "hi": "🌐 वैश्विक बाज़ार तैयारी विश्लेषक",
    },
    "readiness_subheading": {
        "en": "Assess operational, security, and regulatory maturity for AI innovations expanding beyond domestic borders.",
        "or": "ଆନ୍ତର୍ଜାତୀୟ ବଜାରରେ ପ୍ରବେଶ ପାଇଁ କାର୍ଯ୍ୟକ୍ଷମତା, ସୁରକ୍ଷା ଏବଂ ନିୟାମକ ପ୍ରସ୍ତୁତି ଯାଞ୍ଚ କରନ୍ତୁ ।",
        "hi": "अंतर्राष्ट्रीय बाजारों में विस्तार हेतु परिचालन, सुरक्षा और नियामक तत्परता का आकलन करें।",
    },
    "checklist_title": {
        "en": "📋 10-Point Global Export Checklist",
        "or": "📋 ୧୦-ବିନ୍ଦୁ ବିଶ୍ୱ ରପ୍ତାନି ଯାଞ୍ଚ-ତାଲିକା",
        "hi": "📋 10-बिंदु वैश्विक निर्यात चेकलिस्ट",
    },

    # Reports Specific
    "reports_heading": {
        "en": "📊 Reports & Ecosystem Data Export",
        "or": "📊 ରିପୋର୍ଟ ଏବଂ ଡାଟା ରପ୍ତାନି କେନ୍ଦ୍ର",
        "hi": "📊 रिपोर्ट एवं इकोसिस्टम डेटा निर्यात",
    },
    "reports_subheading": {
        "en": "Generate publication-ready PDF intelligence briefs and export raw SQLite datasets in CSV format.",
        "or": "ପ୍ରକାଶନ ଯୋଗ୍ୟ PDF ରିପୋର୍ଟ ତିଆରି କରନ୍ତୁ ଏବଂ CSV ଡାଟା ଡାଉନଲୋଡ୍ କରନ୍ତୁ ।",
        "hi": "प्रकाशन-योग्य PDF रिपोर्ट बनाएं एवं CSV प्रारूप में डेटा डाउनलोड करें।",
    },

    # About Specific
    "about_heading": {
        "en": "About Odisha AI Nexus",
        "or": "ଓଡ଼ିଶା AI ନେକ୍ସସ୍ ବିଷୟରେ",
        "hi": "ओडिशा AI नेक्सस के बारे में",
    },
}

# Sector Translations Mapping
SECTOR_MAP = {
    "Agriculture & Food Security": {
        "en": "Agriculture & Food Security",
        "or": "କୃଷି ଏବଂ ଖାଦ୍ୟ ସୁରକ୍ଷା",
        "hi": "कृषि एवं खाद्य सुरक्षा",
    },
    "Disaster Management & Climate Resilience": {
        "en": "Disaster Management & Climate Resilience",
        "or": "ବିପର୍ଯ୍ୟୟ ପରିଚାଳନା ଏବଂ ଜଳବାୟୁ ସହନଶୀଳତା",
        "hi": "आपदा प्रबंधन एवं जलवायु लचीलापन",
    },
    "Mining & Mineral Exploration": {
        "en": "Mining & Mineral Exploration",
        "or": "ଖଣି ଏବଂ ଖଣିଜ ଅନୁସନ୍ଧାନ",
        "hi": "खनन एवं खनिज अन्वेषण",
    },
    "Steel & Heavy Metallurgy": {
        "en": "Steel & Heavy Metallurgy",
        "or": "ଇସ୍ପାତ ଏବଂ ଭାରୀ ଧାତୁବିଜ୍ଞାନ",
        "hi": "इस्पात एवं भारी धातु विज्ञान",
    },
    "Logistics, Ports & Marine Economy": {
        "en": "Logistics, Ports & Marine Economy",
        "or": "ଲଜିଷ୍ଟିକ୍ସ, ବନ୍ଦର ଏବଂ ସାମୁଦ୍ରିକ ଅର୍ଥନୀତି",
        "hi": "लॉजिस्टिक्स, बंदरगाह एवं समुद्री अर्थव्यवस्था",
    },
    "Healthcare & Rural MedTech": {
        "en": "Healthcare & Rural MedTech",
        "or": "ସ୍ୱାସ୍ଥ୍ୟସେବା ଏବଂ ଗ୍ରାମୀଣ ମେଡଟେକ୍",
        "hi": "स्वास्थ्य सेवा एवं ग्रामीण मेडटेक",
    },
    "Tourism, Temple Tech & Heritage Preservation": {
        "en": "Tourism, Temple Tech & Heritage Preservation",
        "or": "ପର୍ଯ୍ୟଟନ, ମନ୍ଦିର ପ୍ରଯୁକ୍ତି ଏବଂ ଐତିହ୍ୟ ସଂରକ୍ଷଣ",
        "hi": "पर्यटन, मंदिर प्रौद्योगिकी एवं विरासत संरक्षण",
    },
    "Handlooms, Handicrafts & MSME Artisans": {
        "en": "Handlooms, Handicrafts & MSME Artisans",
        "or": "ହସ୍ତତନ୍ତ, ହସ୍ତଶିଳ୍ପ ଏବଂ କାରିଗର ସଶକ୍ତୀକରଣ",
        "hi": "हथकरघा, हस्तशिल्प एवं कारीगर सशक्तिकरण",
    },
}

# Project Stage Translations
STAGE_MAP = {
    "Concept / Ideation": {
        "en": "Concept / Ideation",
        "or": "ଧାରଣା / ଚିନ୍ତନ (Concept)",
        "hi": "विचार / अवधारणा (Concept)",
    },
    "Working Prototype (Lab Tested)": {
        "en": "Working Prototype (Lab Tested)",
        "or": "କାର୍ଯ୍ୟକ୍ଷମ ପ୍ରୋଟୋଟାଇପ୍ (Prototype)",
        "hi": "कार्यशील प्रोटोटाइप (Prototype)",
    },
    "Field Pilot / Live Deployment": {
        "en": "Field Pilot / Live Deployment",
        "or": "କ୍ଷେତ୍ରସ୍ତରୀୟ ପରୀକ୍ଷଣ (Field Pilot)",
        "hi": "फील्ड पायलट / जमीनी परीक्षण",
    },
    "Commercial Scale / Production": {
        "en": "Commercial Scale / Production",
        "or": "ବାଣିଜ୍ୟିକ ସ୍ତର / ଉତ୍ପାଦନ (Production)",
        "hi": "वाणिज्यिक स्तर / उत्पादन (Production)",
    },
}

# Project Status Translations
STATUS_MAP = {
    "Active Development": {
        "en": "Active Development",
        "or": "ସକ୍ରିୟ ବିକାଶ ଚାଲିଛି",
        "hi": "सक्रिय विकास जारी",
    },
    "Pilot in Progress": {
        "en": "Pilot in Progress",
        "or": "ପରୀକ୍ଷଣ କାର୍ଯ୍ୟ ଚାଲୁଅଛି",
        "hi": "पायलट परीक्षण जारी",
    },
    "Seeking Funding / Partners": {
        "en": "Seeking Funding / Partners",
        "or": "ଅନୁଦାନ / ସହଯୋଗୀ ଆବଶ୍ୟକ",
        "hi": "फंडिंग / साझेदार की तलाश",
    },
    "Completed / Archived": {
        "en": "Completed / Archived",
        "or": "ସମ୍ପୂର୍ଣ୍ଣ / ସଂରକ୍ଷିତ",
        "hi": "पूर्ण / संग्रहीत",
    },
}

# Experience Level Translations
EXPERIENCE_MAP = {
    "Student / Researcher": {
        "en": "Student / Researcher",
        "or": "ଛାତ୍ର / ଗବେଷକ",
        "hi": "छात्र / शोधकर्ता",
    },
    "Junior Engineer (1-3 yrs)": {
        "en": "Junior Engineer (1-3 yrs)",
        "or": "କନିଷ୍ଠ ଇଞ୍ଜିନିୟର (୧-୩ ବର୍ଷ)",
        "hi": "कनिष्ठ इंजीनियर (1-3 वर्ष)",
    },
    "Senior Engineer (4-7 yrs)": {
        "en": "Senior Engineer (4-7 yrs)",
        "or": "ବରିଷ୍ଠ ଇଞ୍ଜିନିୟର (୪-୭ ବର୍ଷ)",
        "hi": "वरिष्ठ इंजीनियर (4-7 वर्ष)",
    },
    "Lead / Principal / Domain Expert": {
        "en": "Lead / Principal / Domain Expert",
        "or": "ମୁଖ୍ୟ / ପ୍ରିନ୍ସିପାଲ୍ / ବିଶେଷଜ୍ଞ",
        "hi": "प्रधान / विषय विशेषज्ञ",
    },
}

# Checklist Item Translations for Global Readiness
CHECKLIST_MAP = {
    "data_privacy": {
        "en": "Data Privacy & Localization (DPDP Act 2023 & GDPR aligned)",
        "or": "ଡାଟା ଗୋପନୀୟତା ଓ ଆଇନସଙ୍ଗତ ନିୟମାବଳୀ (DPDP ୨୦୨୩ ଏବଂ GDPR)",
        "hi": "डेटा गोपनीयता एवं कानून अनुपालन (DPDP 2023 एवं GDPR)",
    },
    "model_explainability": {
        "en": "Model Explainability & Auditing (SHAP/LIME or feature attribution)",
        "or": "ମଡେଲ ସ୍ପଷ୍ଟତା ଏବଂ ଅଡିଟ୍ ସାମର୍ଥ୍ୟ (SHAP/LIME ତଥ୍ୟ)",
        "hi": "मॉडल व्याख्यात्मकता एवं ऑडिट क्षमता (SHAP/LIME)",
    },
    "api_standards": {
        "en": "Open API & Interoperability (REST/gRPC with OpenAPI/Swagger docs)",
        "or": "ମୁକ୍ତ API ଏବଂ ମାନକ ଡକ୍ୟୁମେଣ୍ଟେସନ୍ (OpenAPI/Swagger)",
        "hi": "ओपन API एवं मानक प्रलेखन (OpenAPI/Swagger)",
    },
    "edge_readiness": {
        "en": "Edge / Offline Capability (Low latency or intermittent network fit)",
        "or": "ଅଫଲାଇନ୍ ଏବଂ ନିମ୍ନ ନେଟୱର୍କରେ କାର୍ଯ୍ୟକ୍ଷମତା (Edge Fit)",
        "hi": "ऑफ़लाइन एवं कम कनेक्टिविटी में कार्यक्षमता (Edge Ready)",
    },
    "multilingual_support": {
        "en": "Multilingual UI / Native Language Support (Odia, Hindi, English)",
        "or": "ବହୁଭାଷୀ ଇଣ୍ଟରଫେସ୍ ସମର୍ଥନ (ଓଡ଼ିଆ, ହିନ୍ଦୀ, ଇଂରାଜୀ)",
        "hi": "बहुभाषी इंटरफ़ेस समर्थन (ओडिया, हिन्दी, अंग्रेज़ी)",
    },
    "bias_testing": {
        "en": "Demographic & Demographic Bias Testing documented",
        "or": "ପାତରଅନ୍ତର ବିହୀନ ପରୀକ୍ଷଣ ଏବଂ ନ୍ୟାୟସଙ୍ଗତ ଡାଟା ଯାଞ୍ଚ",
        "hi": "निष्पक्षता एवं जनसांख्यिकीय पूर्वाग्रह परीक्षण",
    },
    "benchmarking": {
        "en": "Rigorous Evaluation against Standard Benchmark Datasets",
        "or": "ମାନକ ବେଞ୍ଚମାର୍କ ଡାଟାସେଟ୍ ଉପରେ ପରୀକ୍ଷିତ ଫଳାଫଳ",
        "hi": "मानक बेंचमार्क डेटासेट पर परीक्षित परिणाम",
    },
    "security_audit": {
        "en": "Security Audit & Vulnerability Testing (OWASP LLM Top 10)",
        "or": "ସାଇବର ସୁରକ୍ଷା ଅଡିଟ୍ ଏବଂ ଦୁର୍ବଳତା ପରୀକ୍ଷଣ",
        "hi": "साइबर सुरक्षा ऑडिट एवं संवेदनशीलता परीक्षण",
    },
    "license_compliance": {
        "en": "Open Source & Intellectual Property Licensing Clearances",
        "or": "ଓପନ୍ ସୋର୍ସ ଏବଂ ବୌଦ୍ଧିକ ସମ୍ପତ୍ତି (IP) ଲାଇସେନ୍ସ ସ୍ୱଚ୍ଛତା",
        "hi": "ओपन सोर्स एवं बौद्धिक संपदा (IP) लाइसेंस स्पष्टता",
    },
    "export_packaging": {
        "en": "Containerized Deployment & CI/CD Pipelines (Docker/Helm)",
        "or": "କଣ୍ଟେନରାଇଜଡ୍ ଡିପ୍ଲୟମେଣ୍ଟ (Docker/CI/CD ସୁବିଧା)",
        "hi": "कंटेनरीकृत परिनियोजन (Docker/CI/CD क्षमता)",
    },
}


def get_current_language() -> str:
    """Return the currently selected language code ('en', 'or', 'hi')."""
    if "language" not in st.session_state:
        st.session_state["language"] = DEFAULT_LANGUAGE
    return st.session_state["language"]


def set_language(lang_code: str) -> None:
    """Set the active application language."""
    if lang_code in SUPPORTED_LANGUAGES:
        st.session_state["language"] = lang_code


def t(key: str, lang: Optional[str] = None) -> str:
    """
    Retrieve translated text for the specified key.
    Falls back to English if the translation or key is missing.
    """
    target_lang = lang or get_current_language()
    if key in TRANSLATIONS:
        return TRANSLATIONS[key].get(target_lang, TRANSLATIONS[key].get("en", key))
    return key


def t_sector(sector: str, lang: Optional[str] = None) -> str:
    """Translate sector name."""
    target_lang = lang or get_current_language()
    if sector in SECTOR_MAP:
        return SECTOR_MAP[sector].get(target_lang, sector)
    return sector


def t_stage(stage: str, lang: Optional[str] = None) -> str:
    """Translate development stage."""
    target_lang = lang or get_current_language()
    if stage in STAGE_MAP:
        return STAGE_MAP[stage].get(target_lang, stage)
    return stage


def t_status(status: str, lang: Optional[str] = None) -> str:
    """Translate project status."""
    target_lang = lang or get_current_language()
    if status in STATUS_MAP:
        return STATUS_MAP[status].get(target_lang, status)
    return status


def t_exp(experience: str, lang: Optional[str] = None) -> str:
    """Translate experience level."""
    target_lang = lang or get_current_language()
    if experience in EXPERIENCE_MAP:
        return EXPERIENCE_MAP[experience].get(target_lang, experience)
    return experience


def t_checklist(item_id: str, default_text: str, lang: Optional[str] = None) -> str:
    """Translate readiness checklist item description."""
    target_lang = lang or get_current_language()
    if item_id in CHECKLIST_MAP:
        return CHECKLIST_MAP[item_id].get(target_lang, default_text)
    return default_text


def get_speech_script(lang: Optional[str] = None) -> str:
    """Return speech synthesis and recognition locale code (e.g. 'or-IN', 'hi-IN', 'en-IN')."""
    target_lang = lang or get_current_language()
    return SUPPORTED_LANGUAGES.get(target_lang, {}).get("speech_code", "en-IN")
