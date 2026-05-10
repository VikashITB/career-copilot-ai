"""
pages/job_match.py – FAISS-powered job matching page.
"""

import streamlit as st
import plotly.express as px
from src.resume_parser import parse_resume
from src.job_matcher import match_jobs, add_custom_job
from src.embeddings import build_index, index_exists
from src.utils import load_job_files, score_color, wrap_ai_output


def _build_if_needed():
    """Silently build the FAISS index if it doesn't exist yet."""
    if not index_exists():
        jobs = load_job_files()
        if jobs:
            build_index(list(jobs.values()), list(jobs.keys()))


def render():
    st.markdown("<div class='section-header'>🎯 Job Matcher</div>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#64748b;margin-top:-8px;'>Paste your resume to find the best-fit "
        "jobs using AI-powered semantic similarity search.</p>",
        unsafe_allow_html=True,
    )

    # ── Build index silently ────────────────────────────────────────────────────
    _build_if_needed()

    # ── Inputs ─────────────────────────────────────────────────────────────────
    left, right = st.columns([1, 1])

    with left:
        st.subheader("📁 Resume")
        uploaded = st.file_uploader(
            "Upload PDF / DOCX / TXT",
            type=["pdf", "docx", "txt"],
            key="jm_upload",
        )
        pasted = st.text_area(
            "Or paste resume text",
            height=180,
            placeholder="Paste your resume here…",
            key="jm_paste",
        )

    with right:
        st.subheader("⚙️ Options")
        top_k = st.slider("Number of job matches", 1, 10, 5, key="jm_topk")
        explain = st.toggle("Generate AI explanations per match", value=True, key="jm_explain")

        st.markdown("---")
        st.subheader("➕ Add Custom Job")
        custom_name = st.text_input("Job title", placeholder="e.g. ML Engineer at Startup X", key="jm_cname")
        custom_jd   = st.text_area("Job description", height=120, placeholder="Paste JD here…", key="jm_cjd")
        if st.button("Add to Index", key="jm_add"):
            if custom_name.strip() and custom_jd.strip():
                add_custom_job(custom_name.strip(), custom_jd.strip())
                st.success(f"✅ Added **{custom_name}** to the job index!")
            else:
                st.error("Please provide both a job title and description.")

    # ── Resolve resume ─────────────────────────────────────────────────────────
    resume_text = ""
    if uploaded:
        with st.spinner("Parsing resume…"):
            resume_text = parse_resume(uploaded) or ""
    elif pasted.strip():
        resume_text = pasted.strip()

    # ── Match button ────────────────────────────────────────────────────────────
    st.markdown("---")
    if st.button("🔍 Find Matching Jobs", use_container_width=True, type="primary"):
        if not resume_text:
            st.error("Please upload or paste your resume first.")
            return

        with st.spinner("Running semantic search…"):
            matches = match_jobs(resume_text, top_k=top_k, explain=explain)

        if not matches:
            st.warning("No jobs found in the index. Add job descriptions using the panel above.")
            return

        # ── Bar chart overview ─────────────────────────────────────────────────
        st.subheader("📊 Match Overview")
        names  = [m.job_name for m in matches]
        scores = [m.match_percent for m in matches]
        colors = [score_color(s) for s in scores]

        fig = px.bar(
            x=scores,
            y=names,
            orientation="h",
            text=[f"{s}%" for s in scores],
            color=scores,
            color_continuous_scale=["#fee2e2", "#fef9c3", "#dcfce7"],
            range_color=[0, 100],
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(
            height=max(200, 60 * len(matches)),
            margin=dict(l=0, r=30, t=10, b=10),
            xaxis=dict(range=[0, 110], title="Match %"),
            yaxis=dict(title=""),
            coloraxis_showscale=False,
            paper_bgcolor="white",
            plot_bgcolor="white",
            font_family="Inter",
        )
        st.plotly_chart(fig, use_container_width=True)

        # ── Individual match cards ─────────────────────────────────────────────
        st.subheader("🗂 Match Details")
        for i, match in enumerate(matches):
            color = score_color(match.match_percent)
            with st.expander(
                f"{'🥇' if i == 0 else '🔵'} {match.job_name} — {match.match_percent}% match",
                expanded=(i == 0),
            ):
                prog_col, desc_col = st.columns([1, 2])
                with prog_col:
                    st.metric("Match Score", f"{match.match_percent}%")
                    st.progress(match.match_percent / 100)

                with desc_col:
                    if match.explanation:
                        st.markdown("**🤖 AI Explanation:**")
                        st.markdown(
                            wrap_ai_output(match.explanation, "🤖 AI Job Match Explanation"),
                            unsafe_allow_html=True,
                        )

                with st.expander("View full job description"):
                    st.text(match.job_text[:1500] + ("…" if len(match.job_text) > 1500 else ""))
