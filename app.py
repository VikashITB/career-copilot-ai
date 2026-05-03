"""
CareerCopilot AI – Resume Builder & Job Matcher
Main Streamlit Application Entry Point
"""

import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

# ── Page config must be FIRST Streamlit call ──────────────────────────────────
st.set_page_config(
    page_title="CareerCopilot AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        border-right: 1px solid #334155;
    }
    section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
    section[data-testid="stSidebar"] .stRadio label { font-size: 0.95rem; padding: 6px 0; }

    /* Main background */
    .main { background-color: #f8fafc; }

    /* Metric cards */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 4px 12px rgba(0,0,0,0.04);
        border-left: 4px solid #6366f1;
        margin-bottom: 1rem;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(99,102,241,0.4);
    }

    /* Score badge */
    .score-badge {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 99px;
        font-weight: 700;
        font-size: 0.85rem;
    }
    .score-high  { background:#dcfce7; color:#16a34a; }
    .score-med   { background:#fef9c3; color:#ca8a04; }
    .score-low   { background:#fee2e2; color:#dc2626; }

    /* Section headers */
    .section-header {
        font-size: 1.4rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
    }

    /* Info boxes */
    .info-box {
        background: #f0f4ff;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        border-left: 4px solid #6366f1;
        margin: 0.8rem 0;
        font-size: 0.92rem;
        color: #1e293b;
    }

    /* Hide Streamlit branding */
    #MainMenu { visibility: hidden; }
    footer    { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Sidebar navigation ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<h2 style='color:#a5b4fc;margin-bottom:0;'>🚀 CareerCopilot</h2>"
        "<p style='color:#64748b;font-size:0.8rem;margin-top:2px;'>AI-Powered Career Suite</p>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    page = st.radio(
        "Navigate",
        [
            "🏠 Dashboard",
            "📄 Resume Analysis",
            "🎯 Job Matcher",
            "✍️ Resume Generator",
            "⚡ Bullet Improver",
            "🧭 Career Advisor",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown(
        "<p style='color:#475569;font-size:0.75rem;'>Powered by LangChain + Groq<br/>© 2024 CareerCopilot AI</p>",
        unsafe_allow_html=True,
    )

# ── Route pages ────────────────────────────────────────────────────────────────
if page == "🏠 Dashboard":
    from src.pages.dashboard import render
    render()

elif page == "📄 Resume Analysis":
    from src.pages.resume_analysis import render
    render()

elif page == "🎯 Job Matcher":
    from src.pages.job_match import render
    render()

elif page == "✍️ Resume Generator":
    from src.pages.resume_gen import render
    render()

elif page == "⚡ Bullet Improver":
    from src.pages.bullet_page import render
    render()

elif page == "🧭 Career Advisor":
    from src.pages.career_page import render
    render()
