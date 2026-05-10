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

    /* Dark theme base */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }

    /* Main container */
    .main .block-container {
        background: rgba(15, 23, 42, 0.95);
        border-radius: 16px;
        padding: 2rem;
        margin-top: 1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        border-right: 1px solid #334155;
    }
    section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
    section[data-testid="stSidebar"] .stRadio label { 
        font-size: 0.95rem; 
        padding: 8px 12px; 
        border-radius: 8px;
        margin: 4px 0;
        transition: background 0.2s;
    }
    section[data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(99, 102, 241, 0.1);
    }

    /* Text colors - high contrast */
    h1, h2, h3, h4, h5, h6 { color: #f1f5f9 !important; }
    p, span, div { color: #cbd5e1; }
    .stMarkdown { color: #e2e8f0; }

    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        border-left: 4px solid #6366f1;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.8rem;
        font-weight: 600;
        transition: all 0.2s;
        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.5);
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
    }

    /* Score badge */
    .score-badge {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 99px;
        font-weight: 700;
        font-size: 0.9rem;
    }
    .score-high  { background: rgba(22, 163, 74, 0.2); color: #4ade80; border: 1px solid #22c55e; }
    .score-med   { background: rgba(202, 138, 4, 0.2); color: #facc15; border: 1px solid #eab308; }
    .score-low   { background: rgba(220, 38, 38, 0.2); color: #f87171; border: 1px solid #ef4444; }

    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #334155;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }

    /* AI output boxes */
    .ai-output-box {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #334155;
        border-left: 4px solid #06b6d4;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        color: #e2e8f0;
        line-height: 1.6;
    }

    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        border-radius: 10px;
        padding: 1rem 1.2rem;
        border-left: 4px solid #6366f1;
        margin: 0.8rem 0;
        font-size: 0.93rem;
        color: #e2e8f0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }

    /* Success boxes */
    .success-box {
        background: linear-gradient(135deg, rgba(22, 163, 74, 0.15) 0%, rgba(15, 23, 42, 0.9) 100%);
        border-radius: 10px;
        padding: 1rem 1.2rem;
        border-left: 4px solid #22c55e;
        margin: 0.8rem 0;
        color: #4ade80;
    }

    /* Warning boxes */
    .warning-box {
        background: linear-gradient(135deg, rgba(202, 138, 4, 0.15) 0%, rgba(15, 23, 42, 0.9) 100%);
        border-radius: 10px;
        padding: 1rem 1.2rem;
        border-left: 4px solid #eab308;
        margin: 0.8rem 0;
        color: #facc15;
    }

    /* Error boxes */
    .error-box {
        background: linear-gradient(135deg, rgba(220, 38, 38, 0.15) 0%, rgba(15, 23, 42, 0.9) 100%);
        border-radius: 10px;
        padding: 1rem 1.2rem;
        border-left: 4px solid #ef4444;
        margin: 0.8rem 0;
        color: #f87171;
    }

    /* Card containers */
    .card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #334155;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        margin: 1rem 0;
    }

    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid #475569;
        color: #e2e8f0;
        border-radius: 8px;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
    }

    /* File uploader */
    .stFileUploader {
        background: rgba(30, 41, 59, 0.8);
        border: 2px dashed #475569;
        border-radius: 12px;
        padding: 2rem;
    }
    .stFileUploader:hover {
        border-color: #6366f1;
    }

    /* Progress bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(30, 41, 59, 0.8);
        border-radius: 8px;
        color: #e2e8f0;
    }

    /* Tables */
    .stDataFrame {
        background: rgba(30, 41, 59, 0.8);
        border-radius: 8px;
    }

    /* Plotly charts */
    .js-plotly-plot {
        background: rgba(15, 23, 42, 0.8);
        border-radius: 12px;
    }

    /* Subheaders */
    .stSubheader {
        color: #f1f5f9 !important;
    }

    /* Captions */
    .stCaption {
        color: #94a3b8 !important;
    }

    /* Hide Streamlit branding */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(15, 23, 42, 0.5);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb {
        background: #475569;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #6366f1;
    }
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
