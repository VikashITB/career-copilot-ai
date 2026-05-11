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

    /* Agent step cards */
    .agent-step {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(15, 23, 42, 0.9) 100%);
        border-radius: 10px;
        padding: 0.8rem 1.2rem;
        border-left: 4px solid #a5b4fc;
        margin: 0.5rem 0;
        color: #e2e8f0;
        font-size: 0.9rem;
    }

    /* Agent plan badge */
    .plan-badge {
        display: inline-block;
        background: rgba(99, 102, 241, 0.15);
        color: #a5b4fc;
        border: 1px solid #6366f1;
        border-radius: 6px;
        padding: 3px 10px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 2px;
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
    .stSubheader { color: #f1f5f9 !important; }

    /* Captions */
    .stCaption { color: #94a3b8 !important; }

    /* Hide Streamlit branding */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }

    /* Scrollbar styling */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: rgba(15, 23, 42, 0.5); border-radius: 4px; }
    ::-webkit-scrollbar-thumb { background: #475569; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #6366f1; }
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
            "🤖 AI Career Agent",       # ← NEW
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")

    # ── Agent mode indicator ───────────────────────────────
    if page == "🤖 AI Career Agent":
        st.markdown(
            """
            <div style='background:rgba(99,102,241,0.1);border:1px solid #6366f1;
                        border-radius:8px;padding:10px 12px;margin-bottom:12px;'>
                <p style='color:#a5b4fc;font-size:0.8rem;margin:0;font-weight:600;'>
                    🧠 Agentic Mode Active
                </p>
                <p style='color:#64748b;font-size:0.72rem;margin:4px 0 0;'>
                    Adaptive • Multi-step • Goal-directed
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        "<p style='color:#475569;font-size:0.75rem;'>Powered by LangChain + Groq<br/>© 2025 CareerCopilot AI</p>",
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


# ═════════════════════════════════════════════════════════════════════════════
# 🤖 AI CAREER AGENT PAGE — NEW
# ═════════════════════════════════════════════════════════════════════════════

elif page == "🤖 AI Career Agent":

    from src.agent.career_agent import run_career_agent
    from src.resume_parser import parse_resume

    # ── Page header ───────────────────────────────────────
    st.markdown(
        """
        <div style='margin-bottom:1.5rem;'>
            <h1 style='color:#a5b4fc;margin-bottom:4px;'>🤖 AI Career Agent</h1>
            <p style='color:#64748b;font-size:0.95rem;margin:0;'>
                Tell the agent your goal — it plans, adapts, and executes automatically.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── How it works banner ───────────────────────────────
    with st.expander("ℹ️ How the Agent Works", expanded=False):
        st.markdown(
            """
            The **Career Copilot Agent** is an adaptive AI system that:

            1. **Classifies your goal** — understands what you need (ATS fix, job match, career roadmap, etc.)
            2. **Creates an execution plan** — selects the right tools in the right order
            3. **Runs each tool** — ATS scorer → bullet improver → resume generator → career advisor
            4. **Adapts mid-execution** — if ATS score is low, it automatically adds more improvement steps
            5. **Returns all results** — with a full execution trace

            **Example goals you can enter:**
            - `"Help me become an ML Engineer"`
            - `"Optimize my resume for backend developer jobs"`
            - `"Quick ATS fix for this job description"`
            - `"Prepare me for data science internships"`
            - `"Full career analysis and roadmap"`
            """,
        )

    st.markdown("---")

    # ── Input section ─────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🎯 Your Goal")
        agent_goal = st.text_input(
            "What's your career goal?",
            placeholder="e.g. Help me become an AI Engineer",
            label_visibility="collapsed",
        )

        st.markdown("#### 🏷️ Target Role *(optional)*")
        target_role = st.text_input(
            "Target Role",
            placeholder="e.g. ML Engineer, Backend Developer, Data Analyst",
            label_visibility="collapsed",
        )

        st.markdown("#### 📄 Your Resume")
        agent_resume = st.file_uploader(
            "Upload Resume",
            type=["pdf", "txt", "docx"],
            key="agent_resume",
            label_visibility="collapsed",
        )

    with col2:
        st.markdown("#### 📋 Job Description")
        agent_jd = st.text_area(
            "Paste Job Description",
            placeholder="Paste the full job description here...",
            height=280,
            key="agent_jd",
            label_visibility="collapsed",
        )

    st.markdown("---")

    # ── Example goals quick-fill ──────────────────────────
    st.markdown("**⚡ Quick Goals:**")
    qcol1, qcol2, qcol3, qcol4 = st.columns(4)

    if qcol1.button("🤖 Become AI Engineer", use_container_width=True):
        st.session_state["quick_goal"] = "Help me become an AI Engineer"
    if qcol2.button("🔧 Fix ATS Score", use_container_width=True):
        st.session_state["quick_goal"] = "Optimize my ATS score for this job"
    if qcol3.button("🗺️ Career Roadmap", use_container_width=True):
        st.session_state["quick_goal"] = "Generate a career roadmap for my target role"
    if qcol4.button("⚡ Quick Improve", use_container_width=True):
        st.session_state["quick_goal"] = "Quick resume improvement"

    # Apply quick goal if selected
    if "quick_goal" in st.session_state and not agent_goal:
        agent_goal = st.session_state["quick_goal"]
        st.info(f"💡 Goal set to: **{agent_goal}**")

    st.markdown("")

    # ── Run button ────────────────────────────────────────
    run_clicked = st.button(
        "🚀 Run Agent",
        type="primary",
        use_container_width=True,
    )

    # ── Validation ────────────────────────────────────────
    if run_clicked:
        errors = []
        if not agent_goal.strip():
            errors.append("Please enter your career goal.")
        if not agent_resume:
            errors.append("Please upload your resume.")
        if not agent_jd.strip():
            errors.append("Please paste a job description.")

        for err in errors:
            st.markdown(
                f"<div class='error-box'>❌ {err}</div>",
                unsafe_allow_html=True,
            )

        if not errors:
            # ── Parse resume ──────────────────────────────
            try:
                resume_text = parse_resume(agent_resume)
            except Exception as e:
                st.markdown(
                    f"<div class='error-box'>❌ Failed to parse resume: {e}</div>",
                    unsafe_allow_html=True,
                )
                st.stop()

            if not resume_text or len(resume_text.strip()) < 50:
                st.markdown(
                    "<div class='error-box'>❌ Resume appears to be empty or unreadable. "
                    "Please try a different file.</div>",
                    unsafe_allow_html=True,
                )
                st.stop()

            # ── Agent execution ───────────────────────────
            st.markdown("---")
            st.markdown("### 🔄 Agent Execution")

            st.markdown(
                f"""
                <div class='info-box'>
                    🧠 <strong>Goal:</strong> {agent_goal}<br/>
                    🏷️ <strong>Target Role:</strong> {target_role or "Auto-detected from goal"}<br/>
                    📄 <strong>Resume:</strong> {agent_resume.name}
                </div>
                """,
                unsafe_allow_html=True,
            )

            try:
                memory = run_career_agent(
                    goal=agent_goal,
                    resume_text=resume_text,
                    job_description=agent_jd,
                    target_role=target_role,
                    use_streamlit=True,
                )
            except Exception as e:
                st.markdown(
                    f"<div class='error-box'>❌ Agent execution failed: {e}</div>",
                    unsafe_allow_html=True,
                )
                st.stop()

            # ── Results section ───────────────────────────
            st.markdown("---")
            st.markdown("### 📊 Agent Results")

            # Summary metrics row
            mc1, mc2, mc3, mc4 = st.columns(4)

            with mc1:
                score = memory.ats_score if memory.ats_score else 0
                badge_class = (
                    "score-high" if score >= 70
                    else "score-med" if score >= 50
                    else "score-low"
                )
                st.markdown(
                    f"""
                    <div class='metric-card' style='text-align:center;'>
                        <p style='color:#94a3b8;font-size:0.8rem;margin:0;'>ATS Score</p>
                        <span class='score-badge {badge_class}'>{score}/100</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with mc2:
                steps = len(memory.steps_executed)
                st.markdown(
                    f"""
                    <div class='metric-card' style='text-align:center;'>
                        <p style='color:#94a3b8;font-size:0.8rem;margin:0;'>Steps Completed</p>
                        <p style='color:#a5b4fc;font-size:1.8rem;font-weight:700;margin:0;'>{steps}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with mc3:
                gaps = len(memory.ats_result.get("missing_skills", [])) if memory.ats_result else 0
                st.markdown(
                    f"""
                    <div class='metric-card' style='text-align:center;'>
                        <p style='color:#94a3b8;font-size:0.8rem;margin:0;'>Skill Gaps Found</p>
                        <p style='color:#f87171;font-size:1.8rem;font-weight:700;margin:0;'>{gaps}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with mc4:
                adapted = "Yes" if memory.skill_gaps_detected or memory.role_mismatch_detected else "No"
                adapt_color = "#4ade80" if adapted == "Yes" else "#94a3b8"
                st.markdown(
                    f"""
                    <div class='metric-card' style='text-align:center;'>
                        <p style='color:#94a3b8;font-size:0.8rem;margin:0;'>Plan Adapted</p>
                        <p style='color:{adapt_color};font-size:1.8rem;font-weight:700;margin:0;'>{adapted}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown("")

            # ── Helper for intelligent skipped module messaging ───────────────────────
            def get_skipped_message(module_name: str, goal: str) -> str:
                """Generate context-aware message for skipped execution modules."""
                goal_lower = goal.lower()
                
                if module_name == "ats":
                    if any(kw in goal_lower for kw in ["career", "become", "roadmap", "transition", "path"]):
                        return "ℹ️ ATS analysis was skipped because the current goal focused on career guidance rather than resume optimization."
                    elif any(kw in goal_lower for kw in ["job", "match", "apply"]):
                        return "ℹ️ ATS analysis was skipped to prioritize job matching for your current goal."
                    else:
                        return "ℹ️ ATS analysis was not required for the current execution plan."
                
                elif module_name == "bullets":
                    if any(kw in goal_lower for kw in ["career", "become", "roadmap", "transition", "path"]):
                        return "ℹ️ Bullet improvement was skipped because the goal focused on career planning rather than resume refinement."
                    elif any(kw in goal_lower for kw in ["job", "match", "apply"]):
                        return "ℹ️ Bullet improvement was skipped to focus on job matching for your current goal."
                    else:
                        return "ℹ️ Bullet improvement was not needed for the current execution plan."
                
                elif module_name == "resume":
                    if any(kw in goal_lower for kw in ["career", "become", "roadmap", "transition", "path"]):
                        return "ℹ️ Resume generation was skipped because the agent determined it was unnecessary for career guidance goals."
                    elif any(kw in goal_lower for kw in ["ats", "score", "optimize"]):
                        return "ℹ️ Resume generation was skipped to focus on ATS optimization for your current goal."
                    else:
                        return "ℹ️ Resume generation was not required for the current execution plan."
                
                elif module_name == "career":
                    if any(kw in goal_lower for kw in ["ats", "score", "optimize", "improve", "bullets"]):
                        return "ℹ️ Career roadmap was skipped to focus on resume optimization for your current goal."
                    elif any(kw in goal_lower for kw in ["job", "match", "apply"]):
                        return "ℹ️ Career roadmap was skipped to prioritize job matching for your current goal."
                    else:
                        return "ℹ️ Career roadmap was not needed for the current execution plan."
                
                elif module_name == "job_match":
                    if any(kw in goal_lower for kw in ["career", "become", "roadmap", "transition", "path"]):
                        return "ℹ️ Job matching was skipped to focus on career planning for your current goal."
                    elif any(kw in goal_lower for kw in ["ats", "score", "optimize", "improve", "bullets"]):
                        return "ℹ️ Job matching was skipped to prioritize resume optimization for your current goal."
                    else:
                        return "ℹ️ Job matching was not required for the current execution plan."
                
                return f"ℹ️ {module_name.title()} was not part of the optimized execution plan for your goal."

            # ── Result tabs ───────────────────────────────
            r1, r2, r3, r4, r5 = st.tabs([
                "📊 ATS Analysis",
                "⚡ Improved Bullets",
                "📄 Generated Resume",
                "🗺️ Career Roadmap",
                "🔍 Job Match",
            ])

            # Tab 1 — ATS Analysis
            with r1:
                if memory.ats_result:
                    st.markdown("#### ATS Score Breakdown")

                    if memory.ats_result.get("missing_skills"):
                        st.markdown("**❌ Missing Skills / Keywords:**")
                        skill_cols = st.columns(3)
                        for i, skill in enumerate(memory.ats_result["missing_skills"]):
                            skill_cols[i % 3].markdown(
                                f"<span class='score-badge score-low'>{skill}</span>",
                                unsafe_allow_html=True,
                            )

                    if memory.ats_result.get("present_keywords"):
                        st.markdown("**✅ Keywords Found:**")
                        p_cols = st.columns(3)
                        for i, kw in enumerate(memory.ats_result["present_keywords"]):
                            p_cols[i % 3].markdown(
                                f"<span class='score-badge score-high'>{kw}</span>",
                                unsafe_allow_html=True,
                            )

                    if memory.ats_result.get("section_scores"):
                        st.markdown("**📋 Section Scores:**")
                        for section, score in memory.ats_result["section_scores"].items():
                            st.progress(score / 100, text=f"{section}: {score}/100")
                else:
                    st.markdown(
                        f"<div class='info-box'>{get_skipped_message('ats', memory.goal)}</div>",
                        unsafe_allow_html=True,
                    )

            # Tab 2 — Improved Bullets
            with r2:
                if memory.bullet_result:
                    st.markdown(
                        f"<div class='ai-output-box'>{memory.bullet_result}</div>",
                        unsafe_allow_html=True,
                    )
                    st.download_button(
                        "⬇️ Download Improved Bullets",
                        data=memory.bullet_result,
                        file_name="improved_bullets.txt",
                        mime="text/plain",
                    )
                else:
                    st.markdown(
                        f"<div class='info-box'>{get_skipped_message('bullets', memory.goal)}</div>",
                        unsafe_allow_html=True,
                    )

            # Tab 3 — Generated Resume
            with r3:
                if memory.generator_result:
                    st.markdown(
                        f"<div class='ai-output-box'>{memory.generator_result}</div>",
                        unsafe_allow_html=True,
                    )
                    st.download_button(
                        "⬇️ Download Tailored Resume",
                        data=memory.generator_result,
                        file_name="tailored_resume.txt",
                        mime="text/plain",
                    )
                else:
                    st.markdown(
                        f"<div class='info-box'>{get_skipped_message('resume', memory.goal)}</div>",
                        unsafe_allow_html=True,
                    )

            # Tab 4 — Career Roadmap
            with r4:
                if memory.advisor_result:
                    st.markdown(
                        f"<div class='ai-output-box'>{memory.advisor_result}</div>",
                        unsafe_allow_html=True,
                    )
                    st.download_button(
                        "⬇️ Download Career Roadmap",
                        data=memory.advisor_result,
                        file_name="career_roadmap.txt",
                        mime="text/plain",
                    )
                else:
                    st.markdown(
                        f"<div class='info-box'>{get_skipped_message('career', memory.goal)}</div>",
                        unsafe_allow_html=True,
                    )

            # Tab 5 — Job Match
            with r5:
                if memory.matcher_result:
                    match_score = memory.matcher_result.get("score", 0)
                    badge_class = (
                        "score-high" if match_score >= 70
                        else "score-med" if match_score >= 50
                        else "score-low"
                    )
                    st.markdown(
                        f"""
                        <div class='metric-card' style='display:inline-block;margin-bottom:1rem;'>
                            <span style='color:#94a3b8;font-size:0.85rem;'>Job Match Score: </span>
                            <span class='score-badge {badge_class}'>{match_score}/100</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    if memory.matcher_result.get("explanation"):
                        st.markdown(
                            f"<div class='ai-output-box'>{memory.matcher_result['explanation']}</div>",
                            unsafe_allow_html=True,
                        )
                else:
                    st.markdown(
                        f"<div class='info-box'>{get_skipped_message('job_match', memory.goal)}</div>",
                        unsafe_allow_html=True,
                    )

            # ── Execution trace ───────────────────────────
            st.markdown("---")
            with st.expander("🔍 Agent Execution Trace", expanded=False):
                st.markdown("**Steps Executed:**")
                for i, step in enumerate(memory.steps_executed):
                    st.markdown(
                        f"<div class='agent-step'>✅ Step {i+1}: <strong>{step}</strong></div>",
                        unsafe_allow_html=True,
                    )

                st.markdown("**Adaptive Flags:**")
                flag_col1, flag_col2 = st.columns(2)
                flag_col1.markdown(
                    f"<div class='{'success-box' if memory.skill_gaps_detected else 'info-box'}'>"
                    f"Skill Gaps Detected: <strong>{'Yes' if memory.skill_gaps_detected else 'No'}</strong>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
                flag_col2.markdown(
                    f"<div class='{'warning-box' if memory.role_mismatch_detected else 'info-box'}'>"
                    f"Role Mismatch: <strong>{'Yes' if memory.role_mismatch_detected else 'No'}</strong>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

                st.markdown("**Full Memory Snapshot:**")
                st.json({
                    "goal": memory.goal,
                    "target_role": memory.target_role,
                    "ats_score": memory.ats_score,
                    "steps_executed": memory.steps_executed,
                    "skill_gaps_detected": memory.skill_gaps_detected,
                    "role_mismatch_detected": memory.role_mismatch_detected,
                })