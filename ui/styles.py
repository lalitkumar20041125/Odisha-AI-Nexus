"""
Custom Responsive Dark Navy + Cyan Theme CSS for Odisha AI Nexus.
Provides fully adaptive, fluid layouts across PCs, laptops, tablets, and mobile phones.
"""

def get_custom_css() -> str:
    return """
    <style>
    /* Global Base & Typography (Multilingual: English, Odia, Hindi) */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Noto+Sans+Oriya:wght@400;600;700;800&family=Noto+Sans+Devanagari:wght@400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    *, *::before, *::after {
        box-sizing: border-box;
    }

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Noto Sans Oriya', 'Noto Sans Devanagari', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        -webkit-font-smoothing: antialiased;
        text-rendering: optimizeLegibility;
    }

    /* Main background */
    .stApp {
        background: radial-gradient(circle at 15% 15%, #0B192E 0%, #060D1A 100%);
        color: #F8FAFC;
        overflow-x: hidden;
    }

    /* Fluid App Container */
    .block-container {
        max-width: 1400px;
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
    }

    /* Responsive Header styling */
    .nexus-header {
        background: linear-gradient(135deg, rgba(13, 27, 46, 0.85) 0%, rgba(15, 33, 58, 0.95) 100%);
        border: 1px solid rgba(0, 240, 255, 0.25);
        border-radius: 14px;
        padding: clamp(16px, 3vw, 28px);
        margin-bottom: clamp(16px, 2.5vw, 24px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(8px);
        width: 100%;
        overflow: hidden;
    }
    
    .nexus-title {
        font-size: clamp(1.4rem, 4vw, 2.3rem);
        font-weight: 800;
        letter-spacing: -0.5px;
        background: linear-gradient(90deg, #FFFFFF 0%, #00F0FF 60%, #14B8A6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        padding: 0;
        line-height: 1.2;
        word-break: break-word;
    }

    .nexus-tagline {
        color: #94A3B8;
        font-size: clamp(0.85rem, 1.8vw, 1.05rem);
        font-weight: 500;
        margin-top: 6px;
        letter-spacing: 0.3px;
        line-height: 1.4;
    }

    /* Responsive KPI Metric Cards */
    .metric-card {
        background: linear-gradient(145deg, #0D1E36 0%, #0A1627 100%);
        border: 1px solid rgba(30, 58, 95, 0.8);
        border-radius: 12px;
        padding: clamp(14px, 2.5vw, 20px);
        margin-bottom: 12px;
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(0, 240, 255, 0.4);
        box-shadow: 0 6px 20px rgba(0, 240, 255, 0.08);
    }
    .metric-label {
        font-size: clamp(0.72rem, 1.5vw, 0.82rem);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #94A3B8;
        margin-bottom: 4px;
    }
    .metric-value {
        font-size: clamp(1.5rem, 3.8vw, 2.2rem);
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.15;
    }
    .metric-sub {
        font-size: clamp(0.72rem, 1.4vw, 0.8rem);
        color: #38BDF8;
        margin-top: 6px;
        word-break: break-word;
    }

    /* Responsive Content Cards */
    .nexus-card {
        background: rgba(13, 27, 46, 0.7);
        border: 1px solid #1E3A5F;
        border-radius: 12px;
        padding: clamp(14px, 2.5vw, 22px);
        margin-bottom: 14px;
        backdrop-filter: blur(6px);
        width: 100%;
        word-break: break-word;
    }
    .nexus-card-title {
        font-size: clamp(1.05rem, 2.2vw, 1.25rem);
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 4px;
        line-height: 1.3;
    }
    .nexus-card-subtitle {
        font-size: clamp(0.8rem, 1.6vw, 0.9rem);
        color: #00F0FF;
        margin-bottom: 10px;
        line-height: 1.4;
    }

    /* Responsive Badges */
    .badge-real {
        display: inline-block;
        background-color: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.35);
        padding: 3px 8px;
        border-radius: 9999px;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.4px;
        white-space: nowrap;
    }
    .badge-demo {
        display: inline-block;
        background-color: rgba(245, 158, 11, 0.15);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.35);
        padding: 3px 8px;
        border-radius: 9999px;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.4px;
        white-space: nowrap;
    }
    .badge-stage {
        display: inline-block;
        background-color: rgba(0, 240, 255, 0.12);
        color: #38BDF8;
        border: 1px solid rgba(0, 240, 255, 0.25);
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        white-space: nowrap;
    }
    .badge-sector {
        display: inline-block;
        background-color: rgba(148, 163, 184, 0.1);
        color: #CBD5E1;
        border: 1px solid rgba(148, 163, 184, 0.2);
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        margin: 2px 2px 2px 0;
    }

    /* Disclaimer box */
    .disclaimer-box {
        background: rgba(15, 23, 42, 0.65);
        border-left: 3px solid #00F0FF;
        border-radius: 4px 8px 8px 4px;
        padding: clamp(10px, 2vw, 14px) clamp(12px, 2.5vw, 18px);
        font-size: clamp(0.78rem, 1.5vw, 0.85rem);
        color: #94A3B8;
        margin: 14px 0;
        line-height: 1.5;
        word-break: break-word;
    }

    /* Skills pill */
    .skill-pill {
        display: inline-block;
        background: #112240;
        color: #64FFDA;
        padding: 2px 8px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        margin: 2px 3px 2px 0;
        border: 1px solid rgba(100, 255, 218, 0.2);
    }

    /* Streamlit overrides for polished aesthetics */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: rgba(13, 27, 46, 0.5);
        padding: 6px;
        border-radius: 10px;
        border: 1px solid #1E3A5F;
        flex-wrap: wrap;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        color: #94A3B8;
        font-weight: 600;
        padding: 8px 14px;
        font-size: clamp(0.8rem, 1.8vw, 0.95rem);
        min-height: 40px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00F0FF !important;
        color: #060D1A !important;
        font-weight: 700;
    }

    /* Responsive Buttons & Form Elements */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        min-height: 42px;
        padding: 8px 16px;
        font-size: clamp(0.85rem, 1.8vw, 0.95rem);
        transition: all 0.2s ease;
        touch-action: manipulation;
    }
    .stButton>button:hover {
        border-color: #00F0FF;
        box-shadow: 0 0 12px rgba(0, 240, 255, 0.3);
    }

    /* Sidebar aesthetics & mobile collapse */
    [data-testid="stSidebar"] {
        background-color: #060D1A;
        border-right: 1px solid #1E3A5F;
    }

    /* ========================================================================= */
    /* RESPONSIVE MEDIA QUERIES (PC, LAPTOP, TABLET, MOBILE)                     */
    /* ========================================================================= */

    /* Large Desktops (>= 1200px) */
    @media (min-width: 1200px) {
        .block-container {
            padding-left: 3rem !important;
            padding-right: 3rem !important;
        }
    }

    /* Laptops & Desktops (992px to 1199px) */
    @media (max-width: 1199px) and (min-width: 992px) {
        .block-container {
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
    }

    /* Tablets & Small Laptops (768px to 991px) */
    @media (max-width: 991px) and (min-width: 768px) {
        .block-container {
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
        }
        /* Allow 4-column KPI rows to wrap into 2x2 cleanly */
        [data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
            gap: 10px !important;
        }
        [data-testid="stHorizontalBlock"] > div {
            flex: 1 1 calc(50% - 10px) !important;
            min-width: 220px !important;
        }
    }

    /* Mobile Phones & Phablets (< 768px) */
    @media (max-width: 767px) {
        .block-container {
            padding-left: 0.85rem !important;
            padding-right: 0.85rem !important;
            padding-top: 1.2rem !important;
        }

        /* Stack multi-column blocks cleanly on mobile */
        [data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
            gap: 12px !important;
        }
        [data-testid="stHorizontalBlock"] > div {
            width: 100% !important;
            min-width: 100% !important;
            flex: 1 1 100% !important;
        }

        /* Full-width buttons on mobile */
        .stButton>button {
            width: 100% !important;
        }

        /* Card header flex adjustments */
        .nexus-card > div:first-child {
            flex-direction: column !important;
            align-items: flex-start !important;
            gap: 8px !important;
        }

        /* Tables & Dataframes horizontal scroll */
        [data-testid="stDataFrame"], .stTable {
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch !important;
            width: 100% !important;
        }

        /* Tab bar styling for mobile */
        .stTabs [data-baseweb="tab-list"] {
            overflow-x: auto !important;
            display: flex !important;
            white-space: nowrap !important;
            -webkit-overflow-scrolling: touch !important;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 6px 10px !important;
            font-size: 0.8rem !important;
        }
    }

    /* Ultra-compact screens (< 420px) */
    @media (max-width: 419px) {
        .nexus-header {
            padding: 12px 14px;
        }
        .metric-card {
            padding: 12px;
        }
        .metric-value {
            font-size: 1.6rem;
        }
    }
    </style>
    """
