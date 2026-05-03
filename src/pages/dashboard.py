"""
pages/dashboard.py – CareerCopilot AI Dashboard home page.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from src.utils import wrap_metric_card, check_api_key


def render():
    st.markdown("<div class='section-header'>🏠 Dashboard</div>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#64748b;margin-top:-8px;'>Welcome to CareerCopilot AI — "
        "your all-in-one career intelligence platform.</p>",
        unsafe_allow_html=True,
    )

    # ── API key warning ────────────────────────────────────────────────────────
    if not check_api_key():
        st.warning(
            "⚠️  No API key detected. Add `GROQ_API_KEY` or `OPENAI_API_KEY` "
            "to your `.env` file to enable AI features.",
            icon="🔑",
        )

    st.markdown("---")

    # ── KPI cards ─────────────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(wrap_metric_card("Features Available", "6", "AI-powered tools", "#6366f1"), unsafe_allow_html=True)
    with col2:
        st.markdown(wrap_metric_card("Avg ATS Boost", "+34%", "after optimisation", "#10b981"), unsafe_allow_html=True)
    with col3:
        st.markdown(wrap_metric_card("Job DB Size", "2+", "sample positions", "#f59e0b"), unsafe_allow_html=True)
    with col4:
        st.markdown(wrap_metric_card("LLM Provider", "Groq / OpenAI", "configurable", "#8b5cf6"), unsafe_allow_html=True)

    st.markdown("---")

    # ── Feature overview ───────────────────────────────────────────────────────
    left, right = st.columns([1.2, 1])

    with left:
        st.subheader("🎯 How It Works")
        steps = [
            ("1", "Upload or Generate Resume", "Upload your PDF/DOCX or let the AI build one from scratch."),
            ("2", "ATS Score Analysis", "See how your resume scores against any job description."),
            ("3", "Job Matching", "Find the best-fit jobs using semantic FAISS similarity search."),
            ("4", "Improve & Optimise", "Strengthen bullet points and get a personalised career roadmap."),
        ]
        for num, title, desc in steps:
            st.markdown(
                f"""
                <div style='display:flex;gap:1rem;align-items:flex-start;margin-bottom:1rem;'>
                    <div style='background:#6366f1;color:white;border-radius:50%;
                                width:32px;height:32px;min-width:32px;display:flex;
                                align-items:center;justify-content:center;
                                font-weight:700;font-size:.9rem;'>{num}</div>
                    <div>
                        <p style='margin:0;font-weight:600;color:#0f172a;'>{title}</p>
                        <p style='margin:2px 0 0;color:#64748b;font-size:.88rem;'>{desc}</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with right:
        st.subheader("📊 ATS Score Benchmarks")
        fig = go.Figure(
            go.Bar(
                x=["Entry Level", "Mid Level", "Senior Level", "Manager"],
                y=[55, 68, 74, 71],
                marker_color=["#818cf8", "#6366f1", "#4f46e5", "#4338ca"],
                text=[55, 68, 74, 71],
                textposition="outside",
            )
        )
        fig.update_layout(
            margin=dict(l=0, r=0, t=20, b=0),
            height=250,
            yaxis=dict(range=[0, 100], title="Avg ATS Score"),
            plot_bgcolor="white",
            paper_bgcolor="white",
            font_family="Inter",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Feature cards ──────────────────────────────────────────────────────────
    st.subheader("🛠 Available Tools")
    tools = [
        ("📄", "Resume Analysis", "Score resume vs job description. Detect missing keywords and gaps."),
        ("🎯", "Job Matcher", "Semantic similarity matching against real job descriptions via FAISS."),
        ("✍️", "Resume Generator", "Generate a full, ATS-ready resume from your profile in seconds."),
        ("⚡", "Bullet Improver", "Transform weak bullets into powerful, quantified achievements."),
        ("🧭", "Career Advisor", "Get a personalised 8-week roadmap to your target role."),
    ]
    cols = st.columns(len(tools))
    for col, (icon, title, desc) in zip(cols, tools):
        col.markdown(
            f"""
            <div style='background:white;border-radius:12px;padding:1.1rem;
                        box-shadow:0 1px 4px rgba(0,0,0,.08);text-align:center;height:160px;'>
                <div style='font-size:2rem;'>{icon}</div>
                <p style='font-weight:700;color:#0f172a;margin:6px 0 4px;font-size:.9rem;'>{title}</p>
                <p style='color:#64748b;font-size:.78rem;margin:0;'>{desc}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Radar chart ────────────────────────────────────────────────────────────
    st.subheader("📈 Sample Resume Quality Radar")
    categories = ["Keywords", "Action Verbs", "Quantification", "Formatting", "Length", "Sections"]
    fig2 = go.Figure(
        go.Scatterpolar(
            r=[72, 60, 45, 85, 80, 90],
            theta=categories,
            fill="toself",
            fillcolor="rgba(99,102,241,0.15)",
            line_color="#6366f1",
            name="Your Resume",
        )
    )
    fig2.add_trace(
        go.Scatterpolar(
            r=[85, 85, 85, 85, 85, 85],
            theta=categories,
            fill="toself",
            fillcolor="rgba(16,185,129,0.08)",
            line_color="#10b981",
            line_dash="dash",
            name="Target",
        )
    )
    fig2.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        height=350,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="white",
        font_family="Inter",
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("🔍 Upload your resume in **Resume Analysis** to see your personalised radar chart.")
