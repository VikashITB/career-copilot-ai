"""Shared utilities for CareerCopilot AI."""

import os
import re
import streamlit as st


def get_env(key: str, default: str = "") -> str:
    """Get environment variable with Streamlit secrets fallback."""
    value = os.environ.get(key, "")
    if not value:
        try:
            value = st.secrets.get(key, default)
        except Exception:
            value = default
    return value


def check_api_key() -> bool:
    """Check if any LLM API key is configured."""
    return bool(get_env("GROQ_API_KEY") or get_env("OPENAI_API_KEY"))


def clean_text(text: str) -> str:
    """Clean text by normalizing whitespace."""
    text = re.sub(r"\r\n|\r", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def truncate(text: str, max_chars: int = 4000) -> str:
    """Truncate text to max characters."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(" ", 1)[0] + "…"


def truncate_output(text: str, max_chars: int = 3000) -> str:
    """Truncate LLM output preserving sentence structure."""
    if len(text) <= max_chars:
        return text
    truncated = text[:max_chars]
    last_period = truncated.rfind(".")
    last_newline = truncated.rfind("\n")
    cutoff = max(last_period, last_newline)
    if cutoff > max_chars * 0.8:
        return truncated[:cutoff + 1] + "\n\n… (output truncated for display)"
    return truncated + "…"


def extract_sections(resume_text: str) -> dict:
    """Extract resume sections by headings."""
    section_patterns = [
        "SUMMARY", "OBJECTIVE", "EXPERIENCE", "WORK EXPERIENCE",
        "EDUCATION", "SKILLS", "PROJECTS", "CERTIFICATIONS",
        "ACHIEVEMENTS", "AWARDS", "PUBLICATIONS",
    ]
    pattern = r"(?i)(?:^|\n)(" + "|".join(section_patterns) + r")[\s:]*\n"
    parts = re.split(pattern, resume_text, flags=re.IGNORECASE)
    sections: dict = {}
    if len(parts) > 1:
        for i in range(1, len(parts) - 1, 2):
            name = parts[i].strip().upper()
            content = parts[i + 1].strip() if i + 1 < len(parts) else ""
            sections[name] = content
    if not sections:
        sections["FULL TEXT"] = resume_text.strip()
    return sections


def word_count(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def score_color(score: int) -> str:
    """Get color for score display."""
    if score >= 75:
        return "#16a34a"
    if score >= 50:
        return "#ca8a04"
    return "#dc2626"


def score_label(score: int) -> str:
    """Get human-readable score label."""
    if score >= 80:
        return "Excellent ✅"
    if score >= 60:
        return "Good 👍"
    if score >= 40:
        return "Average ⚠️"
    return "Needs Work ❌"


def bullet_list_html(items: list[str]) -> str:
    """Convert list to HTML unordered list."""
    lis = "".join(f"<li>{item}</li>" for item in items)
    return f"<ul style='margin:0;padding-left:1.2rem;'>{lis}</ul>"


def wrap_metric_card(title: str, value: str, subtitle: str = "", color: str = "#6366f1") -> str:
    """Create HTML metric card."""
    return f"""
    <div style='background:white;border-radius:12px;padding:1.1rem 1.4rem;
                box-shadow:0 1px 3px rgba(0,0,0,.08);border-left:4px solid {color};
                margin-bottom:.8rem;'>
        <p style='margin:0;font-size:.78rem;color:#64748b;font-weight:600;
                  text-transform:uppercase;letter-spacing:.05em;'>{title}</p>
        <p style='margin:4px 0 0;font-size:1.6rem;font-weight:700;color:#0f172a;'>{value}</p>
        {f"<p style='margin:2px 0 0;font-size:.8rem;color:#94a3b8;'>{subtitle}</p>" if subtitle else ""}
    </div>
    """


def jobs_directory() -> str:
    """Get path to jobs data directory."""
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, "data", "jobs")


def load_job_files() -> dict[str, str]:
    """Load all job description files."""
    directory = jobs_directory()
    jobs: dict[str, str] = {}
    if not os.path.isdir(directory):
        return jobs
    for fname in os.listdir(directory):
        if fname.endswith(".txt"):
            fpath = os.path.join(directory, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                key = fname.replace(".txt", "").replace("_", " ").title()
                jobs[key] = f.read()
    return jobs
