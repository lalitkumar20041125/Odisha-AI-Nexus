"""
Main Streamlit Application Entrypoint for Odisha AI Nexus.
Brand: Odisha AI Nexus
Tagline: Local Innovation. Global Impact.
Fully localized for English, Odia (ଓଡ଼ିଆ), and Hindi (हिन्दी) with voice audio companion.
"""

import streamlit as st

# Configure Streamlit page settings before any other Streamlit calls
st.set_page_config(
    page_title="Odisha AI Nexus | Local Innovation. Global Impact.",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

from config import APP_NAME, TAGLINE, APP_VERSION, COMMUNITY_DISCLAIMER
from database import (
    init_db,
    get_ecosystem_stats,
    has_demo_data,
    delete_all_demo_data
)
from seed_data import seed_database_if_empty
from ui.styles import get_custom_css

# Views
from ui.dashboard_view import render_dashboard_view
from ui.projects_view import render_projects_view
from ui.opportunity_view import render_opportunity_view
from ui.talent_view import render_talent_view
from ui.challenges_view import render_challenges_view
from ui.readiness_view import render_readiness_view
from ui.reports_view import render_reports_view
from ui.about_view import render_about_view
from ui.auth_view import render_sidebar_auth_widget, render_auth_dialog_if_active
from security import has_permission, get_current_user, log_security_event
from i18n import get_current_language, set_language, t, SUPPORTED_LANGUAGES


def main():
    # Initialize SQLite database and seed initial demo dataset idempotently
    init_db()
    seed_database_if_empty()

    # Inject styling
    st.markdown(get_custom_css(), unsafe_allow_html=True)

    # ==========================================================================
    # SIDEBAR CONFIGURATION & NAVIGATION
    # ==========================================================================
    with st.sidebar:
        st.markdown(f"""
        <div style="padding: 8px 0 12px 0; border-bottom: 1px solid #1E3A5F; margin-bottom: 12px;">
            <div style="font-size: 1.45rem; font-weight: 800; background: linear-gradient(90deg, #FFFFFF 0%, #00F0FF 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                ⚡ {t("app_name")}
            </div>
            <div style="font-size: 0.8rem; color: #14B8A6; font-weight: 600; margin-top: 2px;">
                {t("tagline")}
            </div>
            <div style="font-size: 0.7rem; color: #64748B; margin-top: 4px;">
                v{APP_VERSION} (English / ଓଡ଼ିଆ / हिन्दी)
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Language Selector (English / ଓଡ଼ିଆ / हिन्दी)
        lang_options = {
            "en": "🇬🇧 English",
            "or": "🇮🇳 ଓଡ଼ିଆ (Odia)",
            "hi": "🇮🇳 हिन्दी (Hindi)"
        }
        current_lang = get_current_language()
        selected_lang_label = st.selectbox(
            "🌐 " + t("select_language"),
            list(lang_options.values()),
            index=list(lang_options.keys()).index(current_lang) if current_lang in lang_options else 0,
            key="lang_selector"
        )
        for code, label in lang_options.items():
            if label == selected_lang_label and code != current_lang:
                set_language(code)
                st.rerun()

        st.write("")

        # Google Authentication Profile / Sign-in Widget
        render_sidebar_auth_widget()
        st.write("")

        # Multilingual Navigation
        nav_options = [
            t("nav_dashboard"),
            t("nav_projects"),
            t("nav_opportunity"),
            t("nav_talent"),
            t("nav_challenges"),
            t("nav_readiness"),
            t("nav_reports"),
            t("nav_about"),
        ]

        nav_selection = st.radio(
            t("nav_menu"),
            nav_options,
            index=0
        )

        st.write("")
        st.divider()

        # Data Scope Controller (Real vs Demo)
        st.markdown(f"##### 🎛️ {t('data_controller')}")
        include_demo = st.toggle(
            t("include_demo"),
            value=True,
            help="Toggle visibility of realistic demonstration records."
        )

        if include_demo:
            st.caption(f"🟡 {t('mode_all')}")
        else:
            st.caption(f"🟢 {t('mode_verified')}")

        # Quick stats snapshot in sidebar
        stats = get_ecosystem_stats(include_demo=include_demo)
        st.markdown(f"""
        <div style="background: rgba(13, 27, 46, 0.6); padding: 10px 12px; border-radius: 8px; border: 1px solid #1E3A5F; font-size: 0.78rem; margin: 10px 0;">
            <div>🚀 <b>{t('kpi_projects')}:</b> {stats['projects']} <span style="color:#94A3B8;">({stats['real_projects']} {t('kpi_real')})</span></div>
            <div>👥 <b>{t('kpi_talent')}:</b> {stats['talent']} <span style="color:#94A3B8;">({stats['real_talent']} {t('kpi_real')})</span></div>
            <div>🏭 <b>{t('kpi_challenges')}:</b> {stats['challenges']} <span style="color:#94A3B8;">({stats['real_challenges']} {t('kpi_real')})</span></div>
            <div>🌐 <b>{t('kpi_readiness')}:</b> {stats['avg_readiness']}%</div>
        </div>
        """, unsafe_allow_html=True)

        # Demo Data Management Utilities (Admin Protected)
        with st.expander("🛠️ " + t("database_tools")):
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                if st.button(t("purge_demo"), use_container_width=True, help="Remove all seed demo data (Admin only)"):
                    if not has_permission("purge_demo_data"):
                        st.error("🔒 Access Denied: Admin permission required / ଆଡମିନ୍ ଅନୁମତି ଆବଶ୍ୟକ ।")
                        log_security_event(
                            event_type="AUTH_PERMISSION_DENIED",
                            details="Non-admin attempted to purge demonstration data",
                            status="DENIED"
                        )
                    else:
                        delete_all_demo_data()
                        log_security_event(
                            event_type="ADMIN_PURGE_DEMO",
                            details="Admin successfully purged demonstration records",
                            status="SUCCESS"
                        )
                        st.success("Demo data purged!")
                        st.rerun()
            with col_d2:
                if st.button(t("reseed_demo"), use_container_width=True, help="Re-populate initial demo records"):
                    seed_database_if_empty()
                    st.success("Demo re-seeded!")
                    st.rerun()

        st.write("")
        st.markdown(f"""
        <div style="font-size: 0.68rem; color: #64748B; line-height: 1.3; padding-top: 10px; border-top: 1px solid #1E3A5F;">
            <b>Notice:</b> {t('community_disclaimer')}
        </div>
        """, unsafe_allow_html=True)

    # Render Google Sign-in / Security Center if modal is active
    render_auth_dialog_if_active()

    # ==========================================================================
    # MAIN VIEW ROUTER (Language-Agnostic Index Routing)
    # ==========================================================================
    nav_idx = nav_options.index(nav_selection) if nav_selection in nav_options else 0

    if nav_idx == 0:
        render_dashboard_view(include_demo=include_demo)
    elif nav_idx == 1:
        render_projects_view(include_demo=include_demo)
    elif nav_idx == 2:
        render_opportunity_view(include_demo=include_demo)
    elif nav_idx == 3:
        render_talent_view(include_demo=include_demo)
    elif nav_idx == 4:
        render_challenges_view(include_demo=include_demo)
    elif nav_idx == 5:
        render_readiness_view(include_demo=include_demo)
    elif nav_idx == 6:
        render_reports_view(include_demo=include_demo)
    elif nav_idx == 7:
        render_about_view()


if __name__ == "__main__":
    main()
