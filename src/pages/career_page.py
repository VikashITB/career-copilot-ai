"""
pages/career_page.py – AI career advisor and roadmap generator page.
"""

import streamlit as st
import plotly.graph_objects as go
from src.career_advisor import get_career_roadmap, parse_roadmap_weeks
from src.utils import truncate_output


def _roadmap_chart(weeks: list[dict]) -> go.Figure:
    """Create a simple Gantt-style timeline from parsed week entries."""
    if not weeks:
        return None
    fig = go.Figure()
    for entry in weeks:
        fig.add_trace(
            go.Bar(
                x=[1],
                y=[f"Week {entry['week']}"],
                orientation="h",
                text=entry["task"][:60] + ("…" if len(entry["task"]) > 60 else ""),
                textposition="inside",
                marker_color=f"rgba(99,102,241,{0.4 + entry['week'] * 0.06:.2f})",
                showlegend=False,
            )
        )
    fig.update_layout(
        height=max(250, 40 * len(weeks)),
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(visible=False),
        yaxis=dict(autorange="reversed"),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font_family="Inter",
        barmode="stack",
    )
    return fig


def render():
    st.markdown("<div class='section-header'>🧭 Career Advisor</div>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#64748b;margin-top:-8px;'>Get a personalised skills roadmap, project "
        "recommendations, and 8-week learning plan to reach your target role.</p>",
        unsafe_allow_html=True,
    )

    # ── Inputs ─────────────────────────────────────────────────────────────────
    with st.form("career_form"):
        col1, col2 = st.columns(2)
        with col1:
            current_role = st.text_input(
                "Current Role / Background *",
                placeholder="e.g. Junior Backend Developer",
            )
            years_exp = st.selectbox(
                "Years of Experience *",
                ["0–1 (Entry)", "1–3 (Junior)", "3–6 (Mid)", "6–10 (Senior)", "10+ (Lead)"],
            )
        with col2:
            target_role = st.text_input(
                "Target Role *",
                placeholder="e.g. Machine Learning Engineer",
            )
            current_skills = st.text_input(
                "Current Skills (comma-separated) *",
                placeholder="Python, SQL, REST APIs, Git…",
            )
        submitted = st.form_submit_button(
            "🧭 Generate My Career Roadmap",
            use_container_width=True,
            type="primary",
        )

    # ── Generation ─────────────────────────────────────────────────────────────
    if submitted:
        if not all([current_role.strip(), target_role.strip(), current_skills.strip()]):
            st.error("Please fill in all required fields (*).")
            return

        with st.spinner("Building your personalised career roadmap…"):
            try:
                roadmap = get_career_roadmap(
                    current_role=current_role.strip(),
                    target_role=target_role.strip(),
                    current_skills=current_skills.strip(),
                    years_exp=years_exp,
                )
                roadmap = truncate_output(roadmap, max_chars=3000)
                st.session_state["career_roadmap"] = roadmap
                st.session_state["career_target"] = target_role.strip()
                st.success(f"✅ Roadmap generated for **{target_role.strip()}**!")
            except RuntimeError as exc:
                st.error(str(exc))
                return

    # ── Display roadmap ────────────────────────────────────────────────────────
    if "career_roadmap" in st.session_state:
        roadmap = st.session_state["career_roadmap"]
        target = st.session_state.get("career_target", "Your Goal")

        st.markdown("---")
        st.subheader(f"🗺 Career Roadmap → **{target}**")

        # ── Week timeline chart ────────────────────────────────────────────────
        weeks = parse_roadmap_weeks(roadmap)
        if weeks:
            st.subheader("📅 8-Week Learning Timeline")
            fig = _roadmap_chart(weeks)
            if fig:
                st.plotly_chart(fig, use_container_width=True)

        # ── Full roadmap text ──────────────────────────────────────────────────
        st.subheader("📋 Full Roadmap Details")
        # Parse the roadmap into sections for nicer display
        import re
        sections = re.split(r"\n(?=\d+\.|[A-Z]{2,})", roadmap)
        for section in sections:
            if not section.strip():
                continue
            # Detect if it's a section header
            first_line = section.strip().splitlines()[0]
            if first_line.isupper() or re.match(r"^\d+\.", first_line):
                rest = "\n".join(section.strip().splitlines()[1:])
                st.markdown(
                    f"<div style='background:#f8fafc;border-radius:10px;padding:1rem 1.2rem;"
                    f"margin-bottom:.8rem;border:1px solid #e2e8f0;'>"
                    f"<p style='font-weight:700;color:#4f46e5;margin:0 0 6px;'>{first_line}</p>"
                    f"<p style='color:#334155;font-size:.88rem;margin:0;white-space:pre-wrap;'>{rest}</p>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"<div style='background:white;border-radius:10px;padding:1rem 1.2rem;"
                    f"margin-bottom:.8rem;box-shadow:0 1px 3px rgba(0,0,0,.06);'>"
                    f"<p style='color:#1e293b;font-size:.88rem;margin:0;white-space:pre-wrap;'>{section.strip()}</p>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

        # ── Download ───────────────────────────────────────────────────────────
        st.download_button(
            label="⬇️  Download Roadmap (.txt)",
            data=roadmap.encode("utf-8"),
            file_name=f"career_roadmap_{target.replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True,
        )

        if st.button("🗑 Clear Roadmap"):
            del st.session_state["career_roadmap"]
            st.rerun()
