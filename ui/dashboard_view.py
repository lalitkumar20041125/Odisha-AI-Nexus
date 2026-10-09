"""
Executive Dashboard View for Odisha AI Nexus.
Presents high-level metrics, sector charts, stage breakdowns, and ranked AI solutions.
Explicitly distinguishes user submissions from demonstration baseline data.
Fully localized for English, Odia (ଓଡ଼ିଆ), and Hindi (हिन्दी) with voice audio companion.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from database import get_ecosystem_stats, get_all_projects, get_all_challenges
from config import APP_NAME, TAGLINE, THEME
from i18n import t, t_sector, t_stage, get_current_language
from ui.voice_widget import render_voice_companion


def render_dashboard_view(include_demo: bool):
    """Render the central Executive Dashboard."""
    lang = get_current_language()

    # Header Banner
    st.markdown(f"""
    <div class="nexus-header">
        <h1 class="nexus-title">{t("app_name")}</h1>
        <div class="nexus-tagline">{t("tagline")}</div>
    </div>
    """, unsafe_allow_html=True)

    # Voice Accessibility Companion
    render_voice_companion(section_key="dashboard")

    # Data filter notification
    if include_demo:
        st.info(f"ℹ️ {t('mode_all')}")
    else:
        st.success(f"✅ {t('mode_verified')}")

    # Fetch stats
    stats = get_ecosystem_stats(include_demo=include_demo)
    
    # 4 Key Metrics Cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{t("kpi_projects")}</div>
            <div class="metric-value">{stats['projects']}</div>
            <div class="metric-sub">👤 {stats['real_projects']} {t("kpi_real")} &nbsp;|&nbsp; 🧪 {stats['demo_projects']} {t("kpi_demo")}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{t("kpi_talent")}</div>
            <div class="metric-value">{stats['talent']}</div>
            <div class="metric-sub">👤 {stats['real_talent']} {t("kpi_real")} &nbsp;|&nbsp; 🧪 {stats['demo_talent']} {t("kpi_demo")}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{t("kpi_challenges")}</div>
            <div class="metric-value">{stats['challenges']}</div>
            <div class="metric-sub">👤 {stats['real_challenges']} {t("kpi_real")} &nbsp;|&nbsp; 🧪 {stats['demo_challenges']} {t("kpi_demo")}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        readiness_sub = {"en": "Across benchmarked projects", "or": "ପରୀକ୍ଷିତ ପ୍ରକଳ୍ପ ସମୂହ", "hi": "परीक्षित प्रोजेक्ट्स में"}.get(lang, "Across benchmarked projects")
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{t("kpi_readiness")}</div>
            <div class="metric-value">{stats['avg_readiness']}%</div>
            <div class="metric-sub">{readiness_sub}</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # Visual Analytics Row
    chart_col1, chart_col2 = st.columns([1.1, 1])

    with chart_col1:
        header_c1, header_c2 = st.columns([1.8, 1.2])
        with header_c1:
            st.markdown(f"### 🌐 {t('sector_chart_title')}")
        
        sector_data = stats.get("sector_distribution", [])
        if sector_data:
            df_sector = pd.DataFrame(sector_data)
            df_sector["sector_display"] = df_sector["sector"].apply(lambda s: t_sector(s))
            total_projs = df_sector["cnt"].sum()

            # Chart representation toggle to eliminate visual clustering
            view_labels = {
                "en": ("📊 Ranked Bar View", "🍩 Clean Donut View"),
                "or": ("📊 ବାର୍ ଚାର୍ଟ (ସ୍ପଷ୍ଟ)", "🍩 ଡୋନଟ୍ ଚାର୍ଟ"),
                "hi": ("📊 रैंक बार चार्ट", "🍩 स्वच्छ डोनट चार्ट")
            }.get(lang, ("📊 Ranked Bar View", "🍩 Clean Donut View"))

            with header_c2:
                selected_chart_view = st.radio(
                    "Chart Type",
                    [view_labels[0], view_labels[1]],
                    index=0,  # Default to clean un-clustered Bar View
                    horizontal=True,
                    label_visibility="collapsed",
                    key="sector_view_format"
                )

            if selected_chart_view == view_labels[0]:
                # Option A: Ranked Horizontal Bar Chart (Completely uncluttered, sorted descending)
                df_sector_sorted = df_sector.sort_values(by="cnt", ascending=True)
                
                fig_sector = px.bar(
                    df_sector_sorted,
                    x="cnt",
                    y="sector_display",
                    orientation="h",
                    text="cnt",
                    color="cnt",
                    color_continuous_scale=[
                        [0.0, "#00F0FF"],
                        [0.5, "#14B8A6"],
                        [1.0, "#38BDF8"]
                    ]
                )
                fig_sector.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#F8FAFC", family="Plus Jakarta Sans, Noto Sans Oriya, Noto Sans Devanagari", size=11),
                    coloraxis_showscale=False,
                    xaxis=dict(title=dict(text="Projects", font=dict(color="#94A3B8", size=10)), gridcolor="#1E3A5F", dtick=1),
                    yaxis=dict(title="", showgrid=False, tickfont=dict(size=11)),
                    margin=dict(l=10, r=25, t=10, b=30),
                    height=350
                )
                fig_sector.update_traces(
                    textposition="outside",
                    texttemplate="<b>%{text}</b>",
                    hovertemplate="<b>%{y}</b><br>📁 Projects: <b>%{x}</b><extra></extra>",
                    marker=dict(line=dict(color="#00F0FF", width=1))
                )
                st.plotly_chart(fig_sector, use_container_width=True, config={"responsive": True, "displayModeBar": False})

            else:
                # Option B: Clean Donut View (De-clustered with hole KPI and no in-slice text overlapping)
                df_sector_donut = df_sector.sort_values(by="cnt", reverse=True if hasattr(df_sector, 'reverse') else False)
                fig_sector = px.pie(
                    df_sector,
                    names="sector_display",
                    values="cnt",
                    hole=0.62,
                    color_discrete_sequence=[
                        "#00F0FF", "#14B8A6", "#38BDF8", "#6366F1", "#A855F7",
                        "#EC4899", "#F59E0B", "#10B981", "#64748B", "#F43F5E"
                    ]
                )
                fig_sector.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#F8FAFC", family="Plus Jakarta Sans, Noto Sans Oriya, Noto Sans Devanagari"),
                    legend=dict(
                        orientation="h",
                        yanchor="top",
                        y=-0.12,
                        xanchor="center",
                        x=0.5,
                        font=dict(size=10)
                    ),
                    margin=dict(l=10, r=10, t=10, b=60),
                    height=350,
                    annotations=[dict(
                        text=f"<span style='font-size:24px;font-weight:800;color:#00F0FF;'>{total_projs}</span><br><span style='font-size:11px;color:#94A3B8;'>{t('kpi_projects')}</span>",
                        x=0.5,
                        y=0.5,
                        showarrow=False,
                        align="center"
                    )]
                )
                fig_sector.update_traces(
                    textposition='none',  # Eliminates text crowding inside slices!
                    hovertemplate="<b>%{label}</b><br>📁 Projects: <b>%{value}</b> (%{percent})<extra></extra>",
                    marker=dict(line=dict(color='#060D1A', width=2))
                )
                st.plotly_chart(fig_sector, use_container_width=True, config={"responsive": True, "displayModeBar": False})
        else:
            st.info("No sector data available to plot.")

    with chart_col2:
        st.markdown(f"### 📈 {t('stage_chart_title')}")
        stage_data = stats.get("stage_distribution", [])
        if stage_data:
            df_stage = pd.DataFrame(stage_data)
            df_stage["stage_display"] = df_stage["stage"].apply(lambda stg: t_stage(stg))
            
            # Sort logically by maturity order if possible
            stage_order = [
                t_stage("Concept / Ideation"),
                t_stage("Working Prototype (Lab Tested)"),
                t_stage("Field Pilot / Live Deployment"),
                t_stage("Commercial Scale / Production")
            ]
            df_stage["sort_key"] = df_stage["stage_display"].apply(lambda s: stage_order.index(s) if s in stage_order else 99)
            df_stage = df_stage.sort_values(by="sort_key", ascending=False)

            fig_stage = px.bar(
                df_stage,
                x="cnt",
                y="stage_display",
                orientation="h",
                text="cnt",
                color="stage_display",
                color_discrete_sequence=["#00F0FF", "#14B8A6", "#38BDF8", "#10B981", "#818CF8"]
            )
            fig_stage.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#F8FAFC", family="Plus Jakarta Sans, Noto Sans Oriya, Noto Sans Devanagari", size=11),
                showlegend=False,
                xaxis=dict(title=dict(text="Projects", font=dict(color="#94A3B8", size=10)), gridcolor="#1E3A5F", dtick=1),
                yaxis=dict(title="", showgrid=False, tickfont=dict(size=11)),
                margin=dict(l=10, r=25, t=10, b=30),
                height=350
            )
            fig_stage.update_traces(
                textposition="outside",
                texttemplate="<b>%{text}</b>",
                hovertemplate="<b>%{y}</b><br>📁 Projects: <b>%{x}</b><extra></extra>",
                marker=dict(line=dict(color="#00F0FF", width=1))
            )
            st.plotly_chart(fig_stage, use_container_width=True, config={"responsive": True, "displayModeBar": False})
        else:
            st.info("No stage distribution data available.")

    st.write("")
    st.divider()

    # Promising AI Projects Table / Ranked List
    st.markdown(f"### 🏆 {t('top_projects_title')}")
    projects = get_all_projects(include_demo=include_demo)
    
    if projects:
        # Sort by readiness score descending
        ranked_projects = sorted(projects, key=lambda x: x.get("readiness_score", 0), reverse=True)
        
        for idx, p in enumerate(ranked_projects[:5], 1):
            demo_badge = f'<span class="badge-demo">{t("badge_demo")}</span>' if p.get('is_demo') else f'<span class="badge-real">{t("badge_verified")}</span>'
            readiness = p.get('readiness_score', 0)
            
            with st.container():
                st.markdown(f"""
                <div class="nexus-card">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
                        <div style="flex: 1 1 260px;">
                            <span style="font-size: 1.15rem; font-weight: 700; color: #FFFFFF;">#{idx} {p['title']}</span>
                            &nbsp; {demo_badge}
                            <div style="color: #00F0FF; font-size: 0.85rem; margin-top: 4px;">{p.get('tagline', '')}</div>
                        </div>
                        <div style="text-align: right; flex-shrink: 0;">
                            <span class="badge-stage">{t_stage(p.get('stage', 'N/A'))}</span>
                            <div style="font-size: 0.95rem; font-weight: 700; color: #10B981; margin-top: 6px;">{readiness}% {t("kpi_readiness")}</div>
                        </div>
                    </div>
                    <div style="margin-top: 10px; font-size: 0.86rem; color: #CBD5E1; line-height: 1.5;">
                        {p.get('description', '')[:200]}...
                    </div>
                    <div style="margin-top: 12px; display: flex; flex-wrap: wrap; gap: 8px; align-items: center;">
                        <span class="badge-sector">📍 {p.get('district', 'Odisha')}</span>
                        <span class="badge-sector">🏛️ {p.get('organization', 'Independent')}</span>
                        <span class="badge-sector">🏷️ {t_sector(p.get('sector', ''))}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("No projects currently found in the selected data view.")

    # High-Priority Industry Challenges
    st.write("")
    st.markdown(f"### ⚡ {t('urgent_challenges_title')}")
    challenges = get_all_challenges(include_demo=include_demo)
    
    if challenges:
        crit_challenges = [c for c in challenges if "Critical" in c.get("urgency", "") or "High" in c.get("urgency", "")]
        display_challenges = crit_challenges[:3] if crit_challenges else challenges[:3]

        col_c1, col_c2, col_c3 = st.columns(len(display_challenges))
        for col, c in zip([col_c1, col_c2, col_c3], display_challenges):
            with col:
                demo_badge = f'<span class="badge-demo">{t("badge_demo")}</span>' if c.get('is_demo') else f'<span class="badge-real">{t("badge_verified")}</span>'
                st.markdown(f"""
                <div class="nexus-card" style="min-height: 220px;">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="font-size: 0.8rem; color: #F59E0B; font-weight: 700;">{c.get('urgency', '')}</span>
                        {demo_badge}
                    </div>
                    <div style="font-weight: 700; font-size: 1rem; color: #FFFFFF; margin: 8px 0 4px 0;">
                        {c.get('title', '')[:50]}...
                    </div>
                    <div style="font-size: 0.8rem; color: #94A3B8;">By {c.get('organization_name', '')} ({c.get('district', '')})</div>
                    <div style="font-size: 0.82rem; color: #CBD5E1; margin: 8px 0; line-height: 1.4;">
                        {c.get('problem_statement', '')[:120]}...
                    </div>
                    <div style="font-size: 0.78rem; color: #00F0FF; font-weight: 600;">
                        Budget: {c.get('budget_range', 'Unspecified')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No industry challenges recorded.")
