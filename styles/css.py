"""Global CSS injection."""
import streamlit as st
from styles.theme import TEXT, BG, MUTED, LINE, ACCENT, ACCENT_2, ACCENT_3, PURPLE


def inject_global_css() -> None:
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    :root {{
        color-scheme: light !important;
    }}

    html, body, [class*="css"], .stApp, p, span, div, h1, h2, h3, h4, h5, h6, label {{
        font-family: 'Inter', sans-serif;
        color: {TEXT} !important;
        box-sizing: border-box;
    }}

    .stApp > header {{ display: none !important; }}
    #root > div:first-child {{ padding-top: 0 !important; }}
    .stApp {{ background: {BG} !important; }}

    .main .block-container {{
        padding: 0.5rem 1.8rem 2rem 1.8rem !important;
        max-width: 1600px;
        margin-top: 0 !important;
    }}

    [data-testid="stAppViewContainer"] > .main {{ padding-top: 0 !important; }}
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] {{
        display: none !important;
    }}

    h1 {{
        color: {TEXT} !important;
        letter-spacing: -0.03em;
        font-size: 1.75rem !important;
        font-weight: 900 !important;
        margin-bottom: 0.15rem !important;
    }}

    .page-subtitle {{
        color: {MUTED} !important;
        font-size: 0.88rem;
        line-height: 1.5;
        margin-bottom: 1.1rem;
    }}

    .divider {{
        height: 1px;
        background: linear-gradient(to right, {ACCENT}, {PURPLE}, transparent);
        margin: 0.75rem 0 0.85rem 0;
        opacity: 0.35;
        pointer-events: none;
        user-select: none;
    }}

    /* SIDEBAR — sempre visible, boto de plegar amagat */
    section[data-testid="stSidebar"] {{
        background: #0F172A !important;
        border-right: 1px solid rgba(255,255,255,0.05);
        min-width: 240px !important;
        max-width: 300px !important;
        transform: none !important;
        visibility: visible !important;
        display: block !important;
    }}
    section[data-testid="stSidebar"] * {{ color: #e2e8f0 !important; }}

    [data-testid="collapsedControl"],
    button[kind="header"] {{
        display: none !important;
    }}

    [data-testid="stSidebarUserContent"] {{
        padding-top: 0.5rem !important;
        display: flex;
        flex-direction: column;
        height: 100%;
    }}

    section[data-testid="stSidebar"] .stRadio > div > label > div:first-child {{
        display: none !important;
    }}
    section[data-testid="stSidebar"] .stRadio > div > label {{
        display: flex !important;
        width: 100% !important;
        min-height: 50px !important;
        align-items: center !important;
        justify-content: flex-start !important;
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.07) !important;
        border-radius: 12px !important;
        margin-bottom: 0.6rem !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.2s ease;
    }}
    section[data-testid="stSidebar"] .stRadio > div > label:hover {{
        background: rgba(6,182,212,0.08) !important;
        border-color: rgba(6,182,212,0.25) !important;
    }}
    section[data-testid="stSidebar"] .stRadio > div > label:has(input:checked) {{
        background: linear-gradient(135deg, rgba(6,182,212,0.22), rgba(139,92,246,0.22)) !important;
        border: 1px solid rgba(6,182,212,0.40) !important;
        box-shadow: 0 0 18px rgba(6,182,212,0.16) !important;
    }}

    .sb-section-label {{
        font-size: 0.62rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: rgba(255,255,255,0.28) !important;
        margin-bottom: 0.4rem;
        display: block;
    }}

    .sb-footer {{
        margin-top: auto;
        padding: 1.25rem 0 0.5rem 0;
        border-top: 1px solid rgba(255,255,255,0.08);
        font-size: 0.74rem;
        color: rgba(226,232,240,0.55) !important;
        line-height: 2;
    }}

    /* KPI */
    [data-testid="stMetric"] {{
        position: relative;
        background: #FFFFFF !important;
        border: 1px solid {LINE} !important;
        border-radius: 20px !important;
        padding: 1.1rem 1.15rem 0.9rem 1.15rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        min-height: 115px;
        overflow: hidden !important;
    }}

    [data-testid="stHorizontalBlock"] > div:first-child [data-testid="stMetric"] {{
        background: linear-gradient(135deg, #0891b2 0%, #0e7490 100%) !important;
        border-color: transparent !important;
    }}
    [data-testid="stHorizontalBlock"] > div:first-child [data-testid="stMetricLabel"] p {{
        color: rgba(255,255,255,0.7) !important;
    }}
    [data-testid="stHorizontalBlock"] > div:first-child [data-testid="stMetricValue"] div {{
        color: #ffffff !important;
    }}
    [data-testid="stHorizontalBlock"] > div:first-child [data-testid="stMetricDelta"] {{
        color: rgba(255,255,255,0.85) !important;
    }}

    [data-testid="stMetric"]::before {{
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 4px;
        background: linear-gradient(90deg, {ACCENT} 0%, {PURPLE} 100%);
    }}

    [data-testid="stMetricLabel"] p {{
        font-size: 0.68rem !important;
        font-weight: 700 !important;
        color: #64748b !important;
        text-transform: uppercase;
        letter-spacing: 0.07em;
    }}
    [data-testid="stMetricValue"] div {{
        font-size: 1.55rem !important;
        font-weight: 800 !important;
        color: {ACCENT_3} !important;
    }}
    [data-testid="stMetricDelta"] {{
        color: {ACCENT} !important;
        font-weight: 600 !important;
    }}
    [data-testid="stMetricDelta"] svg {{ display: none !important; }}

    /* CHARTS */
    [data-testid="stPlotlyChart"] {{
        background: #FFFFFF !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05) !important;
        border: 1px solid #E2E8F0 !important;
        padding: 0 !important;
        margin-top: 0.5rem !important;
        margin-bottom: 1rem !important;
        overflow: hidden !important;
        color-scheme: light !important;
    }}
    [data-testid="stPlotlyChart"] > div {{
        border: none !important;
        box-shadow: none !important;
        background: #FFFFFF !important;
        width: 100% !important;
        color-scheme: light !important;
    }}

    /* SLIDER */
    [data-testid="stSlider"] span,
    [data-testid="stSlider"] p,
    [data-testid="stSlider"] div {{
        color: {TEXT} !important;
        font-weight: 500 !important;
    }}
    [data-testid="stSlider"] label {{
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        color: {TEXT} !important;
    }}
    [data-testid="stSlider"] [data-baseweb="slider"] > div > div {{
        background: #E2E8F0 !important;
    }}
    [data-testid="stSlider"] [data-baseweb="slider"] > div > div > div {{
        background: linear-gradient(90deg, {ACCENT_2}, {ACCENT}) !important;
    }}
    [role="slider"] {{
        background-color: {ACCENT} !important;
        border: 3px solid #fff !important;
        box-shadow: 0 0 8px rgba(6,182,212,0.45) !important;
    }}
    [data-testid="stTickBarMin"],
    [data-testid="stTickBarMax"],
    [data-testid="stThumbValue"] {{
        color: {MUTED} !important;
        font-weight: 600 !important;
        font-size: 0.78rem !important;
    }}

    /* INFO BOX */
    .info-box {{
        background: rgba(6,182,212,0.05);
        border-left: 4px solid {ACCENT};
        border-radius: 12px;
        padding: 0.85rem 1.1rem;
        color: {TEXT};
        font-size: 0.85rem;
        line-height: 1.6;
        margin-bottom: 0.8rem;
        overflow: hidden;
    }}

    /* DARK MODE */
    @media (prefers-color-scheme: dark) {{
        :root {{ color-scheme: light !important; }}
        html, body, .stApp {{ background: {BG} !important; }}
        html, body, [class*="css"], .stApp, p, span, div,
        h1, h2, h3, h4, h5, h6, label {{
            color: {TEXT} !important;
        }}
        [data-testid="stPlotlyChart"],
        [data-testid="stPlotlyChart"] > div {{
            background: #FFFFFF !important;
            color-scheme: light !important;
        }}
        [data-testid="stMetric"] {{
            background: #FFFFFF !important;
        }}
    }}
    </style>

    <script>
        const keepSidebarOpen = () => {
            const sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
            if (sidebar && sidebar.getAttribute('aria-expanded') === 'false') {
                const btn = window.parent.document.querySelector('[data-testid="collapsedControl"] button');
                if (btn) btn.click();
            }
        };
        setInterval(keepSidebarOpen, 300);
    </script>
    """, unsafe_allow_html=True)
