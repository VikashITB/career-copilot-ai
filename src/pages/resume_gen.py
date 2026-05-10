"""
pages/resume_gen.py – AI resume generator page.
"""

import streamlit as st
from src.resume_generator import generate_resume, resume_to_download_bytes, ResumeProfile
from src.utils import truncate_output


def render():
    st.markdown("<div class='section-header'>✍️ Resume Generator</div>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#64748b;margin-top:-8px;'>Fill in your profile and let the AI craft "
        "an ATS-optimised resume tailored to your target role.</p>",
        unsafe_allow_html=True,
    )

    # ── Form ───────────────────────────────────────────────────────────────────
    with st.form("resume_gen_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Full Name *", placeholder="e.g. Priya Sharma")
            role = st.text_input("Target Role *", placeholder="e.g. Senior Data Scientist")
            years_exp = st.selectbox(
                "Years of Experience *",
                ["0–1 (Entry)", "1–3 (Junior)", "3–6 (Mid)", "6–10 (Senior)", "10+ (Lead/Principal)"],
            )
            education = st.text_area(
                "Education *",
                height=100,
                placeholder="B.Tech Computer Science, IIT Delhi, 2020\nCoursera ML Certificate, 2022",
            )

        with col2:
            skills = st.text_area(
                "Skills (comma-separated) *",
                height=100,
                placeholder="Python, TensorFlow, SQL, AWS, Docker, LangChain…",
            )
            experience = st.text_area(
                "Work Experience *",
                height=150,
                placeholder="Software Engineer at Infosys (2020–2022):\n- Built REST APIs serving 10K RPS\n- Reduced latency by 40% via caching",
            )
            projects = st.text_area(
                "Key Projects",
                height=100,
                placeholder="1. AI Chatbot – LangChain + FastAPI – 500 GitHub stars\n2. Real-time fraud detector – 98% accuracy",
            )

        submitted = st.form_submit_button("✨ Generate Resume", use_container_width=True, type="primary")

    # ── Generation ─────────────────────────────────────────────────────────────
    if submitted:
        if not all([name.strip(), role.strip(), skills.strip(), experience.strip(), education.strip()]):
            st.error("Please fill in all required fields (*) before generating.")
            return

        profile = ResumeProfile(
            name=name.strip(),
            role=role.strip(),
            years_exp=years_exp,
            skills=skills.strip(),
            experience=experience.strip(),
            education=education.strip(),
            projects=projects.strip(),
        )

        with st.spinner("✨ Generating your resume with AI…"):
            try:
                resume_text = generate_resume(profile)
                resume_text = truncate_output(resume_text, max_chars=4000)
                st.session_state["generated_resume"] = resume_text
                st.success("✅ Resume generated successfully!")
            except RuntimeError as exc:
                st.error(str(exc))
                return

    # ── Display result if available ────────────────────────────────────────────
    if "generated_resume" in st.session_state:
        resume_text = st.session_state["generated_resume"]

        st.markdown("---")
        st.subheader("📄 Your Generated Resume")

        # Preview box
        st.markdown(
            f"<div style='background:linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);"
            f"border-radius:12px;padding:1.5rem;"
            f"box-shadow:0 4px 12px rgba(0,0,0,0.3);white-space:pre-wrap;"
            f"font-family:monospace;font-size:.85rem;color:#e2e8f0;"
            f"border:1px solid #334155;max-height:500px;overflow-y:auto;'>"
            f"{resume_text}</div>",
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Download button
        dl_col, clear_col = st.columns([2, 1])
        with dl_col:
            st.download_button(
                label="⬇️  Download Resume (.txt)",
                data=resume_to_download_bytes(resume_text),
                file_name=f"resume_{st.session_state.get('gen_name', 'generated')}.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with clear_col:
            if st.button("🗑 Clear", use_container_width=True):
                del st.session_state["generated_resume"]
                st.rerun()

        # Word count info
        wc = len(resume_text.split())
        st.caption(f"📊 Word count: **{wc}** words | Character count: **{len(resume_text)}**")
