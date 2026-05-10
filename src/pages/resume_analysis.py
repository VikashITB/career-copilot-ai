"""
pages/resume_analysis.py – ATS scoring and resume analysis page.
"""

import streamlit as st
import plotly.graph_objects as go
from src.resume_parser import parse_resume
from src.ats_scorer import score_resume
from src.rag_chain import ats_analysis_chain
from src.utils import score_color, score_label, load_job_files, truncate, wrap_ai_output


def _gauge(score: int) -> go.Figure:
    """Return a Plotly gauge figure for the given ATS score."""
    color = score_color(score)
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "ATS Score", "font": {"size": 18}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1},
                "bar": {"color": color},
                "steps": [
                    {"range": [0, 40], "color": "#fee2e2"},
                    {"range": [40, 70], "color": "#fef9c3"},
                    {"range": [70, 100], "color": "#dcfce7"},
                ],
                "threshold": {
                    "line": {"color": color, "width": 4},
                    "thickness": 0.75,
                    "value": score,
                },
            },
        )
    )
    fig.update_layout(height=260, margin=dict(l=20, r=20, t=30, b=10), paper_bgcolor="white")
    return fig


def render():
    st.markdown("<div class='section-header'>📄 Resume Analysis</div>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#64748b;margin-top:-8px;'>Upload your resume and paste a job description "
        "to get an instant ATS compatibility score.</p>",
        unsafe_allow_html=True,
    )

    # ── Inputs ─────────────────────────────────────────────────────────────────
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("📁 Upload Resume")
        uploaded = st.file_uploader(
            "Supports PDF, DOCX, TXT",
            type=["pdf", "docx", "txt"],
            key="ats_upload",
        )
        if uploaded:
            st.success(f"✅ Loaded: **{uploaded.name}**")

        st.subheader("✏️ Or Paste Resume Text")
        pasted = st.text_area(
            "Resume Text",
            height=200,
            placeholder="Paste your resume content here…",
            key="ats_pasted",
            label_visibility="collapsed",
        )

    with col_right:
        st.subheader("📋 Job Description")
        sample_jobs = load_job_files()
        job_choice = st.selectbox(
            "Load a sample job or write your own",
            ["— Custom —"] + list(sample_jobs.keys()),
            key="ats_job_select",
        )
        default_jd = sample_jobs.get(job_choice, "") if job_choice != "— Custom —" else ""
        jd_text = st.text_area(
            "Job Description",
            value=default_jd,
            height=250,
            placeholder="Paste the job description here…",
            key="ats_jd",
            label_visibility="collapsed",
        )

    # ── Resolve resume text ────────────────────────────────────────────────────
    resume_text = ""
    if uploaded:
        with st.spinner("Parsing resume…"):
            resume_text = parse_resume(uploaded) or ""
    elif pasted.strip():
        resume_text = pasted.strip()

    # ── Analyse button ─────────────────────────────────────────────────────────
    st.markdown("---")
    if st.button("🔍 Analyse Resume", use_container_width=True, type="primary"):
        if not resume_text:
            st.error("Please upload a resume or paste resume text.")
            return
        if not jd_text.strip():
            st.error("Please provide a job description.")
            return

        with st.spinner("Running ATS analysis…"):
            result = score_resume(resume_text, jd_text)

        # ── Results layout ─────────────────────────────────────────────────────
        g_col, info_col = st.columns([1, 1.6])

        with g_col:
            st.plotly_chart(_gauge(result.score), use_container_width=True)
            label = score_label(result.score)
            color = score_color(result.score)
            st.markdown(
                f"<p style='text-align:center;font-weight:700;color:{color};font-size:1.1rem;'>{label}</p>",
                unsafe_allow_html=True,
            )

        with info_col:
            st.subheader("📊 Score Breakdown")
            breakdown = {
                "Keyword Match (50 pts)": int((len(result.matched_keywords) / max(len(result.matched_keywords) + len(result.missing_keywords), 1)) * 50),
                "Section Completeness (20 pts)": sum(result.section_scores.values()),
                "Action Verbs (15 pts)": min(15, result.action_verb_count * 2),
                "Resume Length (15 pts)": min(15, max(2, result.word_count // 30)),
            }
            for label_text, pts in breakdown.items():
                max_pts = int(label_text.split("(")[1].replace(" pts)", ""))
                pct = min(100, int((pts / max_pts) * 100))
                st.markdown(f"**{label_text}** — {pts}/{max_pts}")
                st.progress(pct / 100)

        # ── Keywords ───────────────────────────────────────────────────────────
        kw_col1, kw_col2 = st.columns(2)
        with kw_col1:
            st.markdown("#### ✅ Matched Keywords")
            if result.matched_keywords:
                tags = " ".join(
                    f"<span style='background:rgba(22, 163, 74, 0.2);color:#4ade80;padding:2px 10px;"
                    f"border:1px solid #22c55e;border-radius:99px;font-size:.8rem;margin:2px;display:inline-block;'>{kw}</span>"
                    for kw in result.matched_keywords[:20]
                )
                st.markdown(tags, unsafe_allow_html=True)
            else:
                st.info("No keyword matches found.")

        with kw_col2:
            st.markdown("#### ❌ Missing Keywords")
            if result.missing_keywords:
                tags = " ".join(
                    f"<span style='background:rgba(220, 38, 38, 0.2);color:#f87171;padding:2px 10px;"
                    f"border:1px solid #ef4444;border-radius:99px;font-size:.8rem;margin:2px;display:inline-block;'>{kw}</span>"
                    for kw in result.missing_keywords
                )
                st.markdown(tags, unsafe_allow_html=True)
            else:
                st.success("No critical keywords missing!")

        # ── Feedback ───────────────────────────────────────────────────────────
        st.markdown("#### 💡 Improvement Suggestions")
        for tip in result.feedback:
            st.markdown(
                f"<div style='background:linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);"
                f"border-radius:10px;padding:1rem 1.2rem;"
                f"border-left:4px solid #6366f1;margin:0.8rem 0;"
                f"font-size:0.93rem;color:#e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.2);'>{tip}</div>",
                unsafe_allow_html=True,
            )

        # ── AI narrative analysis ───────────────────────────────────────────────
        st.markdown("#### 🤖 AI Recruiter Analysis")
        with st.spinner("Generating AI analysis…"):
            try:
                chain = ats_analysis_chain()
                narrative = chain.invoke(
                    {
                        "resume": truncate(resume_text, 1500),
                        "job_description": truncate(jd_text, 1500),
                        "score": result.score,
                        "missing_keywords": ", ".join(result.missing_keywords[:10]),
                    }
                )
                st.markdown(
                    wrap_ai_output(narrative, "🤖 AI Recruiter Analysis"),
                    unsafe_allow_html=True,
                )
            except Exception as exc:
                st.warning(f"AI analysis unavailable: {exc}")
