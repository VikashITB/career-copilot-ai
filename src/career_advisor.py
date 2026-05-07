"""Career roadmap generation using LLM."""

import re
from src.rag_chain import career_advisor_chain
from src.utils import clean_text


def get_career_roadmap(
    current_role: str,
    target_role: str,
    current_skills: str,
    years_exp: str,
) -> str:
    """Generate personalized career development plan."""
    chain = career_advisor_chain()
    try:
        result = chain.invoke(
            {
                "current_role": current_role,
                "target_role": target_role,
                "current_skills": current_skills,
                "years_exp": years_exp,
            }
        )
        return clean_text(result)
    except Exception as exc:
        raise RuntimeError(f"Career advice generation failed: {exc}") from exc


def parse_roadmap_weeks(roadmap_text: str) -> list[dict]:
    """Extract week-by-week tasks from roadmap text."""
    weeks: list[dict] = []
    pattern = re.compile(r"week\s*(\d+)[:\-–]?\s*(.+)", re.IGNORECASE)
    for line in roadmap_text.splitlines():
        m = pattern.search(line)
        if m:
            weeks.append({"week": int(m.group(1)), "task": m.group(2).strip()})
    return weeks
