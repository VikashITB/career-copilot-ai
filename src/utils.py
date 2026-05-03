"""
utils.py – Shared helper utilities for CareerCopilot AI
"""

import os
import re
import textwrap
from typing import Optional
import streamlit as st


# ── Environment helpers ────────────────────────────────────────────────────────

def get_env(key: str, default: str = "") -> str:
    """Return environment variable, falling back to Streamlit secrets if available."""
    value = os.environ.get(key, "")
    if not value:
        try:
            value = st.secrets.get(key, default)
        except Exception:
            value = default
    return value


def check_api_key() -> bool:
    """Return True if at least one LLM API key is configured."""
    return bool(get_env("GROQ_API_KEY") or get_env("OPENAI_API_KEY"))


# ── Text helpers ───────────────────────────────────────────────────────────────

def clean_text(text: str) -> str:
    """Remove excessive whitespace and control characters from text."""
    text = re.sub(r"\r\n|\r", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def truncate(text: str, max_chars: int = 4000) -> str:
    """Truncate text to *max_chars*, appending ellipsis if needed."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(" ", 1)[0] + "…"


def truncate_output(text: str, max_chars: int = 3000) -> str:
    """Truncate LLM output to prevent UI breakage, preserving structure."""
    if len(text) <= max_chars:
        return text
    truncated = text[:max_chars]
    # Try to end at a complete sentence
    last_period = truncated.rfind(".")
    last_newline = truncated.rfind("\n")
    cutoff = max(last_period, last_newline)
    if cutoff > max_chars * 0.8:  # Only use if we have at least 80% of content
        return truncated[:cutoff + 1] + "\n\n… (output truncated for display)"
    return truncated + "…"


def extract_sections(resume_text: str) -> dict:
    """
    Naively extract common resume sections by looking for uppercase headings.
    Returns a dict of {section_name: content}.
    """
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
    """Return the word count of *text*."""
    return len(text.split())


# ── Formatting helpers ─────────────────────────────────────────────────────────

def score_color(score: int) -> str:
    """Return a hex colour string based on a 0–100 score."""
    if score >= 75:
        return "#16a34a"
    if score >= 50:
        return "#ca8a04"
    return "#dc2626"


def score_label(score: int) -> str:
    """Return a human-readable label for a score."""
    if score >= 80:
        return "Excellent ✅"
    if score >= 60:
        return "Good 👍"
    if score >= 40:
        return "Average ⚠️"
    return "Needs Work ❌"


def bullet_list_html(items: list[str]) -> str:
    """Convert a Python list into an HTML unordered list string."""
    lis = "".join(f"<li>{item}</li>" for item in items)
    return f"<ul style='margin:0;padding-left:1.2rem;'>{lis}</ul>"


def wrap_metric_card(title: str, value: str, subtitle: str = "", color: str = "#6366f1") -> str:
    """Return an HTML metric card."""
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


# ── File helpers ───────────────────────────────────────────────────────────────

def jobs_directory() -> str:
    """Return the absolute path to the data/jobs directory."""
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, "data", "jobs")


def load_job_files() -> dict[str, str]:
    """
    Load all .txt job description files from data/jobs/.
    Returns {filename_without_ext: content}.
    """
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
