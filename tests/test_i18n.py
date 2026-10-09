"""
Unit tests for the Internationalization (i18n) Engine of Odisha AI Nexus.
Validates multi-language dictionary integrity, language switching, fallbacks,
and localized domain helpers for Odia (ଓଡ଼ିଆ) and Hindi (हिन्दी).
"""

import unittest
from unittest.mock import patch

from i18n import (
    SUPPORTED_LANGUAGES,
    DEFAULT_LANGUAGE,
    get_current_language,
    set_language,
    t,
    t_sector,
    t_stage,
    t_status,
    t_exp,
    t_checklist,
    get_speech_script
)


class TestI18nLocalization(unittest.TestCase):
    def setUp(self):
        # Reset session state for language before each test
        import streamlit as st
        if "language" in st.session_state:
            del st.session_state["language"]

    def test_supported_languages_configuration(self):
        """Verify that English, Odia, and Hindi are configured with valid speech locales."""
        self.assertIn("en", SUPPORTED_LANGUAGES)
        self.assertIn("or", SUPPORTED_LANGUAGES)
        self.assertIn("hi", SUPPORTED_LANGUAGES)
        
        self.assertEqual(SUPPORTED_LANGUAGES["or"]["native"], "ଓଡ଼ିଆ")
        self.assertEqual(SUPPORTED_LANGUAGES["hi"]["native"], "हिन्दी")
        self.assertEqual(SUPPORTED_LANGUAGES["or"]["speech_code"], "or-IN")
        self.assertEqual(SUPPORTED_LANGUAGES["hi"]["speech_code"], "hi-IN")

    def test_default_language_and_switching(self):
        """Test default language fallback and explicit language switching."""
        self.assertEqual(get_current_language(), DEFAULT_LANGUAGE)
        
        set_language("or")
        self.assertEqual(get_current_language(), "or")
        
        set_language("hi")
        self.assertEqual(get_current_language(), "hi")
        
        # Invalid language code should be ignored
        set_language("fr_invalid")
        self.assertEqual(get_current_language(), "hi")

    def test_basic_translation_lookups(self):
        """Verify core UI keys return authentic English, Odia, and Hindi strings."""
        # English
        self.assertEqual(t("app_name", lang="en"), "Odisha AI Nexus")
        self.assertIn("Global Impact", t("tagline", lang="en"))
        
        # Odia
        self.assertEqual(t("app_name", lang="or"), "ଓଡ଼ିଶା AI ନେକ୍ସସ୍")
        self.assertIn("ସ୍ଥାନୀୟ ଉଦ୍ଭାବନ", t("tagline", lang="or"))
        self.assertIn("ପ୍ରକଳ୍ପ", t("nav_projects", lang="or"))
        
        # Hindi
        self.assertEqual(t("app_name", lang="hi"), "ओडिशा AI नेक्सस")
        self.assertIn("स्थानीय नवाचार", t("tagline", lang="hi"))
        self.assertIn("प्रोजेक्ट", t("nav_projects", lang="hi"))

    def test_fallback_on_missing_key(self):
        """Verify fallback behavior for missing translation keys."""
        missing_key = "non_existent_key_xyz_123"
        self.assertEqual(t(missing_key, lang="or"), missing_key)
        self.assertEqual(t(missing_key, lang="hi"), missing_key)

    def test_sector_translations(self):
        """Verify that sector names are accurately translated into Odia and Hindi."""
        sector_en = "Agriculture & Food Security"
        sector_or = t_sector(sector_en, lang="or")
        sector_hi = t_sector(sector_en, lang="hi")
        
        self.assertIn("କୃଷି", sector_or)
        self.assertIn("कृषि", sector_hi)
        
        mining_en = "Mining & Mineral Exploration"
        self.assertIn("ଖଣି", t_sector(mining_en, lang="or"))
        self.assertIn("खनन", t_sector(mining_en, lang="hi"))

    def test_stage_and_status_translations(self):
        """Verify project development stage and status translations."""
        stage_en = "Working Prototype (Lab Tested)"
        self.assertIn("ପ୍ରୋଟୋଟାଇପ୍", t_stage(stage_en, lang="or"))
        self.assertIn("प्रोटोटाइप", t_stage(stage_en, lang="hi"))
        
        status_en = "Active Development"
        self.assertIn("ସକ୍ରିୟ", t_status(status_en, lang="or"))
        self.assertIn("सक्रिय", t_status(status_en, lang="hi"))

    def test_experience_and_checklist_translations(self):
        """Verify experience levels and 10-point readiness checklist translations."""
        exp_en = "Student / Researcher"
        self.assertIn("ଛାତ୍ର", t_exp(exp_en, lang="or"))
        self.assertIn("छात्र", t_exp(exp_en, lang="hi"))
        
        chk_item = "data_privacy"
        chk_or = t_checklist(chk_item, "Default text", lang="or")
        chk_hi = t_checklist(chk_item, "Default text", lang="hi")
        
        self.assertIn("ଗୋପନୀୟତା", chk_or)
        self.assertIn("गोपनीयता", chk_hi)

    def test_speech_script_codes(self):
        """Verify that speech recognition and synthesis locale codes match language selection."""
        self.assertEqual(get_speech_script("en"), "en-IN")
        self.assertEqual(get_speech_script("or"), "or-IN")
        self.assertEqual(get_speech_script("hi"), "hi-IN")


if __name__ == "__main__":
    unittest.main()
