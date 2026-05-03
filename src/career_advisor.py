"""
career_advisor.py – AI-powered career roadmap and skill recommendation engine.
"""

from src.rag_chain import career_advisor_chain
from src.utils import clean_text


def get_career_roadmap(
    current_role: str,
    target_role: str,
    current_skills: str,
    years_exp: str,
) -> str:
    """
    Generate a detailed career development plan using the LLM.

    Parameters
    ----------
    current_role : str
        The user's current job title or background.
    target_role : str
        The role the user wants to reach.
    current_skills : str
        Comma-separated list of the user's current skills.
    years_exp : str
        Years of professional experience.

    Returns
    -------
    str
        Formatted career roadmap text with sections:
        SKILLS TO LEARN, PROJECTS TO BUILD, 8-WEEK ROADMAP, JOB TIPS.
    """
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
    """
    Extract week-by-week entries from a roadmap text.
    Looks for lines containing 'Week N' patterns.
    Returns a list of {"week": int, "task": str} dicts.
    """
    import re
    weeks: list[dict] = []
    pattern = re.compile(r"week\s*(\d+)[:\-–]?\s*(.+)", re.IGNORECASE)
    for line in roadmap_text.splitlines():
        m = pattern.search(line)
        if m:
            weeks.append({"week": int(m.group(1)), "task": m.group(2).strip()})
    return weeks
