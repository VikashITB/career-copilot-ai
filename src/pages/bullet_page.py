"""
pages/bullet_page.py – AI-powered bullet point improver page.
"""

import streamlit as st
from src.bullet_improver import improve_bullets, parse_bullets
from src.utils import truncate_output

EXAMPLES = {
    "Software Engineer": (
        "- Worked on backend systems\n"
        "- Fixed bugs in the API\n"
        "- Helped with deployments\n"
        "- Wrote some unit tests"
    ),
    "Data Scientist": (
        "- Did machine learning projects\n"
        "- Worked with large datasets\n"
        "- Built models for prediction\n"
        "- Presented findings to stakeholders"
    ),
    "Product Manager": (
        "- Managed product roadmap\n"
        "- Worked with different teams\n"
        "- Helped improve user experience\n"
        "- Wrote product requirements"
    ),
    "AI Engineer": (
        "- Built AI models\n"
        "- Worked with LLMs\n"
        "- Optimized inference\n"
        "- Deployed ML systems"
    ),
    "DevOps Engineer": (
        "- Managed cloud infrastructure\n"
        "- Set up CI/CD pipelines\n"
        "- Monitored systems\n"
        "- Automated deployments"
    ),
    "ML Engineer": (
        "- Trained machine learning models\n"
        "- Built data pipelines\n"
        "- Optimized model performance\n"
        "- Deployed models to production"
    ),
}


def render():
    st.markdown("<div class='section-header'>⚡ Bullet Point Improver</div>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#64748b;margin-top:-8px;'>Turn vague, weak bullet points into "
        "powerful, quantified achievement statements using AI.</p>",
        unsafe_allow_html=True,
    )

    # ── Inputs ─────────────────────────────────────────────────────────────────
    col_in, col_out = st.columns([1, 1])

    with col_in:
        st.subheader("📝 Input")
        
        # Predefined example role dropdown
        st.markdown(
            "<p style='color:#94a3b8;font-size:0.85rem;margin-bottom:0.5rem;'>"
            "📋 Choose an example role (for demo templates)</p>",
            unsafe_allow_html=True,
        )
        example_role = st.selectbox("Example Role", list(EXAMPLES.keys()), key="bullet_example_role")
        
        # Custom role input
        st.markdown(
            "<p style='color:#94a3b8;font-size:0.85rem;margin:0.5rem 0;'>"
            "✏️ Or enter a custom target role</p>",
            unsafe_allow_html=True,
        )
        custom_role = st.text_input(
            "Custom Target Role",
            placeholder="e.g. AI Engineer, DevOps Engineer, ML Engineer, Cybersecurity Analyst",
            key="bullet_custom_role",
        )
        
        # Determine which role to use (custom overrides example)
        role = custom_role.strip() if custom_role.strip() else example_role
        
        # Show which role is being used
        if custom_role.strip():
            st.markdown(
                f"<div style='background:rgba(6, 182, 212, 0.1);border:1px solid #06b6d4;"
                f"border-radius:6px;padding:0.5rem 0.8rem;margin:0.5rem 0;'>"
                f"<p style='margin:0;color:#06b6d4;font-size:0.8rem;font-weight:600;'>"
                f"Using custom role: {role}</p></div>",
                unsafe_allow_html=True,
            )
        
        # Load example button (only works for predefined roles)
        if not custom_role.strip():
            if st.button("Load Example", key="load_example"):
                st.session_state["bullet_input"] = EXAMPLES[example_role]
                st.rerun()

        bullets_input = st.text_area(
            "Your weak bullet points",
            height=200,
            placeholder="Enter your bullet points, one per line…",
            value=st.session_state.get("bullet_input", ""),
            key="bullet_input",
        )

    with col_out:
        st.subheader("✅ Improved Bullets")
        result_placeholder = st.empty()
        result_placeholder.info("Improved bullets will appear here after you click **Improve** ⬇️")

    # ── Improve button ─────────────────────────────────────────────────────────
    st.markdown("---")
    if st.button("⚡ Improve My Bullets", use_container_width=True, type="primary"):
        raw = bullets_input.strip()
        if not raw:
            st.error("Please enter at least one bullet point.")
            return
        
        if not role:
            st.error("Please either select an example role or enter a custom target role.")
            return

        with st.spinner("Transforming your bullets with AI…"):
            try:
                improved_text = improve_bullets(raw, role=role)
                improved_text = truncate_output(improved_text, max_chars=2000)
                improved_list = parse_bullets(improved_text)
                st.session_state["improved_bullets"] = improved_list
                st.session_state["original_bullets"] = parse_bullets(raw)
                st.session_state["used_role"] = role  # Store the role for reference
            except RuntimeError as exc:
                st.error(str(exc))
                return

    # ── Display results ────────────────────────────────────────────────────────
    if "improved_bullets" in st.session_state:
        improved = st.session_state["improved_bullets"]
        original = st.session_state.get("original_bullets", [])
        used_role = st.session_state.get("used_role", "Unknown Role")
        
        # Show which role was used for improvement
        st.markdown(
            f"<div style='background:linear-gradient(135deg, rgba(6, 182, 212, 0.15) 0%, rgba(15, 23, 42, 0.9) 100%);"
            f"border-radius:10px;padding:1rem 1.2rem;border:1px solid #06b6d4;border-left:4px solid #06b6d4;"
            f"margin:1rem 0;box-shadow:0 2px 8px rgba(0,0,0,0.2);'>"
            f"<p style='margin:0;color:#06b6d4;font-weight:700;font-size:0.9rem;'>"
            f"🎯 Target Role: {used_role}</p></div>",
            unsafe_allow_html=True,
        )

        # Fill the right-column placeholder
        with col_out:
            result_placeholder.empty()
            for bullet in improved:
                st.markdown(
                    f"<div style='background:linear-gradient(135deg, rgba(22, 163, 74, 0.15) 0%, rgba(15, 23, 42, 0.9) 100%);"
                    f"border-left:3px solid #22c55e;"
                    f"padding:.6rem 1rem;border-radius:6px;margin-bottom:.5rem;"
                    f"font-size:.9rem;color:#4ade80;'>✅ {bullet}</div>",
                    unsafe_allow_html=True,
                )

        # ── Side-by-side comparison table ────────────────────────────────────
        st.markdown("---")
        st.subheader("📊 Before vs After")
        max_rows = max(len(original), len(improved))
        for i in range(max_rows):
            b_col, a_col = st.columns(2)
            with b_col:
                if i < len(original):
                    st.markdown(
                        f"<div style='background:linear-gradient(135deg, rgba(220, 38, 38, 0.15) 0%, rgba(15, 23, 42, 0.9) 100%);"
                        f"border-left:3px solid #ef4444;"
                        f"padding:.5rem .9rem;border-radius:6px;font-size:.85rem;color:#f87171;'>"
                        f"❌ {original[i]}</div>",
                        unsafe_allow_html=True,
                    )
            with a_col:
                if i < len(improved):
                    st.markdown(
                        f"<div style='background:linear-gradient(135deg, rgba(22, 163, 74, 0.15) 0%, rgba(15, 23, 42, 0.9) 100%);"
                        f"border-left:3px solid #22c55e;"
                        f"padding:.5rem .9rem;border-radius:6px;font-size:.85rem;color:#4ade80;'>"
                        f"✅ {improved[i]}</div>",
                        unsafe_allow_html=True,
                    )

        # ── Copy/download ─────────────────────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        dl_col, clear_col = st.columns([2, 1])
        with dl_col:
            st.download_button(
                label="⬇️  Download Improved Bullets (.txt)",
                data="\n".join(f"• {b}" for b in improved).encode("utf-8"),
                file_name="improved_bullets.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with clear_col:
            if st.button("🗑 Clear", use_container_width=True):
                for key in ["improved_bullets", "original_bullets", "used_role", "bullet_input"]:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
