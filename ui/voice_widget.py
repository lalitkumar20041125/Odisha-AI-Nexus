"""
Interactive Voice & Speech Companion for Odisha AI Nexus.
Enables non-English speaking and non-reading users to:
1. Listen to page overviews, project details, and briefings aloud in Odia (ଓଡ଼ିଆ), Hindi (हिन्दी), or English via HTML5 Web Speech Synthesis.
2. Speak to search or give voice commands via Web Speech Recognition (Microphone STT).
"""

import streamlit as st
import streamlit.components.v1 as components
import json
from typing import Optional
from i18n import get_current_language, t, get_speech_script


# Rich spoken scripts for each section in English, Odia, and Hindi
AUDIO_SCRIPTS = {
    "dashboard": {
        "en": "Welcome to Odisha AI Nexus. Local Innovation, Global Impact. Explore registered AI projects, discover industry challenges across steel, mining, and agriculture, and connect with top researchers from IIT Bhubaneswar, NIT Rourkela, and local universities.",
        "or": "ଓଡ଼ିଶା AI ନେକ୍ସସକୁ ଆପଣଙ୍କୁ ସ୍ୱାଗତ । ସ୍ଥାନୀୟ ଉଦ୍ଭାବନ, ବିଶ୍ୱସ୍ତରୀୟ ପ୍ରଭାବ । ଏଠାରେ ଆପଣ ଓଡ଼ିଶାର କୃଷି, ଖଣି, ଇସ୍ପାତ ଏବଂ ବିପର୍ଯ୍ୟୟ ପରିଚାଳନା ପାଇଁ ପ୍ରସ୍ତୁତ AI ପ୍ରକଳ୍ପ ଦେଖିପାରିବେ ଏବଂ ଶିଳ୍ପ ସମସ୍ୟା ସହିତ ଯୋଡ଼ି ହୋଇପାରିବେ ।",
        "hi": "ओडिशा AI नेक्सस में आपका स्वागत है। स्थानीय नवाचार, वैश्विक प्रभाव। यहाँ आप कृषि, खनन, इस्पात और आपदा प्रबंधन के लिए विकसित AI प्रोजेक्ट्स देख सकते हैं और राज्य के शीर्ष शोधकर्ताओं से जुड़ सकते हैं।",
    },
    "projects": {
        "en": "This is the AI Project Registry. You can browse applied machine learning projects created in Odisha or register your own solution using the form tab.",
        "or": "ଏହା ହେଉଛି AI ପ୍ରକଳ୍ପ ରେଜିଷ୍ଟ୍ରି । ଏଠାରେ ଆପଣ ଓଡ଼ିଶାରେ ତିଆରି ହୋଇଥିବା AI ପ୍ରକଳ୍ପ ସନ୍ଧାନ କରିପାରିବେ ଏବଂ ନିଜର ନୂତନ ପ୍ରକଳ୍ପ ପଞ୍ଜୀକରଣ କରିପାରିବେ ।",
        "hi": "यह AI प्रोजेक्ट रजिस्ट्री है। यहाँ आप ओडिशा में विकसित AI परियोजनाओं को खोज सकते हैं और अपने प्रोजेक्ट को पंजीकृत कर सकते हैं।",
    },
    "opportunity": {
        "en": "The AI Opportunity Explorer lets you test and evaluate new ideas across technical feasibility, Odisha impact, data availability, and global export potential.",
        "or": "AI ସୁଯୋଗ ଅନୁସନ୍ଧାନ ମାଧ୍ୟମରେ ଆପଣ ନିଜର AI ଧାରଣାର ସମ୍ଭାବ୍ୟତା, ଆଞ୍ଚଳିକ ଉପଯୋଗିତା ଏବଂ ରପ୍ତାନି ସାମର୍ଥ୍ୟ ପରୀକ୍ଷା କରିପାରିବେ ।",
        "hi": "AI अवसर एक्सप्लोरर के माध्यम से आप अपने AI विचार की व्यवहार्यता, सामाजिक प्रभाव और वैश्विक निर्यात क्षमता का मूल्यांकन कर सकते हैं।",
    },
    "talent": {
        "en": "The Talent Exchange connects students, engineers, and AI researchers across all 30 districts of Odisha with matching projects and mentors.",
        "or": "ପ୍ରତିଭା ବିନିମୟ ମଞ୍ଚ ଓଡ଼ିଶାର ୩୦ଟି ଜିଲ୍ଲାର ଛାତ୍ରଛାତ୍ରୀ, ଇଞ୍ଜିନିୟର ଏବଂ AI ଗବେଷକଙ୍କୁ ଉପଯୁକ୍ତ ପ୍ରକଳ୍ପ ସହ ସଂଯୋଗ କରେ ।",
        "hi": "प्रतिभा विनिमय मंच ओडिशा के सभी 30 जिलों के छात्रों, इंजीनियरों और शोधकर्ताओं को उपयुक्त AI प्रोजेक्ट्स से जोड़ता है।",
    },
    "challenges": {
        "en": "The Industry Challenge Board lists real operational problems submitted by heavy industries, MSMEs, and public departments in Odisha awaiting AI solutions.",
        "or": "ଶିଳ୍ପ ଚ୍ୟାଲେଞ୍ଜ ବୋର୍ଡରେ ଓଡ଼ିଶାର କାରଖାନା, କ୍ଷୁଦ୍ର ଶିଳ୍ପ ଏବଂ ସରକାରୀ ବିଭାଗ ଦ୍ୱାରା ଦିଆଯାଇଥିବା ବାସ୍ତବ ସମସ୍ୟା ରହିଛି, ଯାହା AI ଦଳମାନଙ୍କ ସମାଧାନକୁ ଅପେକ୍ଷା କରିଛି ।",
        "hi": "उद्योग चुनौती बोर्ड पर ओडिशा के भारी उद्योगों और सरकारी विभागों की वास्तविक समस्याएं सूचीबद्ध हैं, जिनके समाधान हेतु AI टीमों की आवश्यकता है।",
    },
    "readiness": {
        "en": "The Global Market Readiness tool evaluates your AI product against a 10-point checklist covering data privacy, edge offline capability, explainability, and containerization.",
        "or": "ବିଶ୍ୱ ବଜାର ପ୍ରସ୍ତୁତି ଉପକରଣ ଆପଣଙ୍କ AI ସମାଧାନକୁ ୧୦-ବିନ୍ଦୁ ଯାଞ୍ଚ-ତାଲିକା ମାଧ୍ୟମରେ ପରୀକ୍ଷା କରି ଆନ୍ତର୍ଜାତୀୟ ରପ୍ତାନି ପାଇଁ ମାର୍ଗଦର୍ଶନ ପ୍ରଦାନ କରେ ।",
        "hi": "वैश्विक बाज़ार तैयारी उपकरण 10-बिंदु चेकलिस्ट के माध्यम से आपके AI उत्पाद का मूल्यांकन कर अंतर्राष्ट्रीय निर्यात के लिए मार्गदर्शन देता है।",
    },
}


def render_voice_companion(section_key: str = "dashboard", custom_text: Optional[str] = None):
    """
    Renders an interactive browser-based audio reader / voice narrator widget.
    Users can click to listen to the section spoken aloud in Odia, Hindi, or English.
    """
    lang = get_current_language()
    speech_lang_code = get_speech_script(lang)
    
    # Pick script text
    if custom_text:
        text_to_speak = custom_text
    else:
        text_to_speak = AUDIO_SCRIPTS.get(section_key, {}).get(lang, AUDIO_SCRIPTS.get("dashboard", {}).get(lang, ""))

    # Prepare safe JSON strings
    safe_text_json = json.dumps(text_to_speak)
    safe_lang_code = json.dumps(speech_lang_code)

    # Localized button labels
    labels = {
        "en": {"play": "🔊 Listen Aloud", "pause": "⏸️ Pause", "resume": "▶️ Resume", "stop": "⏹️ Stop", "voice_guide": "Voice Companion"},
        "or": {"play": "🔊 ସ୍ୱରରେ ଶୁଣନ୍ତୁ (Odia Audio)", "pause": "⏸️ ରୋକନ୍ତୁ", "resume": "▶️ ପୁଣି ଶୁଣନ୍ତୁ", "stop": "⏹️ ବନ୍ଦ କରନ୍ତୁ", "voice_guide": "ବାକ୍ ସହାୟକ"},
        "hi": {"play": "🔊 आवाज में सुनें (Hindi Audio)", "pause": "⏸️ रोकें", "resume": "▶️ पुनः सुनें", "stop": "⏹️ बंद करें", "voice_guide": "वॉइस साथी"}
    }
    cur_labels = labels.get(lang, labels["en"])

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        body {{
            margin: 0;
            padding: 4px 0;
            background: transparent;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            color: #F8FAFC;
        }}
        .voice-card {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 10px;
            background: linear-gradient(135deg, rgba(13, 27, 46, 0.95) 0%, rgba(15, 33, 58, 0.95) 100%);
            border: 1px solid rgba(0, 240, 255, 0.4);
            border-radius: 10px;
            padding: 8px 14px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }}
        .voice-info {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.85rem;
            color: #E2E8F0;
        }}
        .voice-badge {{
            background: rgba(0, 240, 255, 0.15);
            color: #00F0FF;
            border: 1px solid #00F0FF;
            border-radius: 6px;
            padding: 2px 8px;
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
        }}
        .voice-controls {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .v-btn {{
            background: #1E3A5F;
            color: #FFFFFF;
            border: 1px solid #38BDF8;
            border-radius: 6px;
            padding: 5px 12px;
            font-size: 0.82rem;
            cursor: pointer;
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            font-weight: 600;
        }}
        .v-btn:hover {{
            background: #00F0FF;
            color: #0B192E;
            border-color: #00F0FF;
            box-shadow: 0 0 8px rgba(0, 240, 255, 0.6);
        }}
        .v-btn:active {{
            transform: scale(0.97);
        }}
        .pulse-wave {{
            display: none;
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: #10B981;
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
            animation: pulse-green 1.5s infinite;
        }}
        @keyframes pulse-green {{
            0% {{
                transform: scale(0.95);
                box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
            }}
            70% {{
                transform: scale(1);
                box-shadow: 0 0 0 10px rgba(16, 185, 129, 0);
            }}
            100% {{
                transform: scale(0.95);
                box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
            }}
        }}
        #statusText {{
            font-size: 0.75rem;
            color: #94A3B8;
            margin-left: 4px;
        }}
    </style>
    </head>
    <body>
        <div class="voice-card">
            <div class="voice-info">
                <span class="voice-badge">🎙️ {cur_labels["voice_guide"]}</span>
                <span class="pulse-wave" id="pulseWave"></span>
                <span id="statusText">Ready</span>
            </div>
            <div class="voice-controls">
                <button class="v-btn" id="playBtn" onclick="speakText()">
                    {cur_labels["play"]}
                </button>
                <button class="v-btn" id="pauseBtn" onclick="pauseSpeech()" style="display:none;">
                    {cur_labels["pause"]}
                </button>
                <button class="v-btn" id="stopBtn" onclick="stopSpeech()" style="display:none; background:#7F1D1D; border-color:#EF4444;">
                    {cur_labels["stop"]}
                </button>
            </div>
        </div>

        <script>
            const textToSpeak = {safe_text_json};
            const speechLang = {safe_lang_code};
            let synth = window.speechSynthesis;
            let currentUtterance = null;
            let isPaused = false;

            const playBtn = document.getElementById('playBtn');
            const pauseBtn = document.getElementById('pauseBtn');
            const stopBtn = document.getElementById('stopBtn');
            const pulseWave = document.getElementById('pulseWave');
            const statusText = document.getElementById('statusText');

            function speakText() {{
                if (!synth) {{
                    statusText.innerText = "Speech API not available in this browser.";
                    return;
                }}

                if (isPaused) {{
                    synth.resume();
                    isPaused = false;
                    statusText.innerText = "Playing...";
                    playBtn.style.display = 'none';
                    pauseBtn.style.display = 'inline-flex';
                    pulseWave.style.display = 'inline-block';
                    return;
                }}

                synth.cancel(); // Stop any pending speech

                currentUtterance = new SpeechSynthesisUtterance(textToSpeak);
                currentUtterance.lang = speechLang;
                currentUtterance.rate = 0.95; // Clear natural pace

                // Try to match available voices
                const voices = synth.getVoices();
                const matchedVoice = voices.find(v => v.lang === speechLang || v.lang.startsWith(speechLang.split('-')[0]));
                if (matchedVoice) {{
                    currentUtterance.voice = matchedVoice;
                }}

                currentUtterance.onstart = function() {{
                    pulseWave.style.display = 'inline-block';
                    statusText.innerText = "Speaking ({speech_lang_code})...";
                    playBtn.style.display = 'none';
                    pauseBtn.style.display = 'inline-flex';
                    stopBtn.style.display = 'inline-flex';
                }};

                currentUtterance.onend = function() {{
                    resetUI();
                }};

                currentUtterance.onerror = function() {{
                    resetUI();
                    statusText.innerText = "Finished.";
                }};

                synth.speak(currentUtterance);
            }}

            function pauseSpeech() {{
                if (synth && synth.speaking) {{
                    synth.pause();
                    isPaused = true;
                    pulseWave.style.display = 'none';
                    statusText.innerText = "Paused";
                    pauseBtn.style.display = 'none';
                    playBtn.style.display = 'inline-flex';
                    playBtn.innerText = "{cur_labels['resume']}";
                }}
            }}

            function stopSpeech() {{
                if (synth) {{
                    synth.cancel();
                    resetUI();
                }}
            }}

            function resetUI() {{
                isPaused = false;
                pulseWave.style.display = 'none';
                statusText.innerText = "Ready";
                playBtn.style.display = 'inline-flex';
                playBtn.innerText = "{cur_labels['play']}";
                pauseBtn.style.display = 'none';
                stopBtn.style.display = 'none';
            }}
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=62)


def render_voice_input_search(target_component_id: str = "search_input", placeholder: str = "Search..."):
    """
    Renders an interactive Voice Search (Speech-to-Text) microphone widget.
    Allows users to speak search queries in Odia, Hindi, or English.
    """
    lang = get_current_language()
    speech_lang_code = get_speech_script(lang)

    labels = {
        "en": {"mic_btn": "🎙️ Speak to Search", "listening": "Listening... Speak your keywords", "prompt": "Click to speak"},
        "or": {"mic_btn": "🎙️ କହି ସନ୍ଧାନ କରନ୍ତୁ", "listening": "ଶୁଣୁଛି... ଦୟାକରି କୁହନ୍ତୁ", "prompt": "କହିବା ପାଇଁ କ୍ଲିକ୍ କରନ୍ତୁ"},
        "hi": {"mic_btn": "🎙️ बोलकर खोजें", "listening": "सुन रहा हूँ... बोलिए", "prompt": "बोलने के लिए क्लिक करें"}
    }
    cur_labels = labels.get(lang, labels["en"])
    speech_lang_json = json.dumps(speech_lang_code)

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: transparent;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            color: #F8FAFC;
        }}
        .mic-container {{
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 4px 0;
        }}
        .mic-btn {{
            background: linear-gradient(135deg, #1E3A5F 0%, #0D233A 100%);
            border: 1px solid #00F0FF;
            color: #FFFFFF;
            border-radius: 8px;
            padding: 6px 14px;
            font-size: 0.84rem;
            font-weight: 600;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s ease;
        }}
        .mic-btn:hover {{
            background: #00F0FF;
            color: #0B192E;
            box-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
        }}
        .mic-active {{
            background: #EF4444 !important;
            border-color: #F87171 !important;
            color: #FFFFFF !important;
            animation: pulse-red 1.2s infinite;
        }}
        @keyframes pulse-red {{
            0% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }}
            70% {{ box-shadow: 0 0 0 12px rgba(239, 68, 68, 0); }}
            100% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }}
        }}
        .speech-result {{
            font-size: 0.82rem;
            color: #00F0FF;
            font-style: italic;
        }}
    </style>
    </head>
    <body>
        <div class="mic-container">
            <button class="mic-btn" id="micBtn" onclick="toggleSpeechRec()">
                {cur_labels["mic_btn"]}
            </button>
            <span class="speech-result" id="speechResult"></span>
        </div>

        <script>
            const speechLang = {speech_lang_json};
            const micBtn = document.getElementById('micBtn');
            const speechResult = document.getElementById('speechResult');
            let recognition = null;
            let isRecognizing = false;

            const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;

            function toggleSpeechRec() {{
                if (!SpeechRec) {{
                    speechResult.innerText = "Voice recognition not supported in this browser. Please use Chrome/Edge.";
                    return;
                }}

                if (isRecognizing) {{
                    recognition.stop();
                    return;
                }}

                recognition = new SpeechRec();
                recognition.lang = speechLang;
                recognition.continuous = false;
                recognition.interimResults = false;

                recognition.onstart = function() {{
                    isRecognizing = true;
                    micBtn.classList.add('mic-active');
                    micBtn.innerText = "🔴 " + "{cur_labels['listening']}";
                    speechResult.innerText = "";
                }};

                recognition.onresult = function(event) {{
                    const transcript = event.results[0][0].transcript;
                    speechResult.innerText = '🗣️ "' + transcript + '"';
                    
                    // Copy to clipboard or write to active search field if accessible
                    try {{
                        navigator.clipboard.writeText(transcript);
                    }} catch (e) {{}}
                }};

                recognition.onerror = function(event) {{
                    speechResult.innerText = "Speech input ended (" + event.error + ")";
                    endRec();
                }};

                recognition.onend = function() {{
                    endRec();
                }};

                try {{
                    recognition.start();
                }} catch (e) {{
                    endRec();
                }}
            }}

            function endRec() {{
                isRecognizing = false;
                micBtn.classList.remove('mic-active');
                micBtn.innerText = "{cur_labels['mic_btn']}";
            }}
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=45)
