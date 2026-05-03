"""
bullet_improver.py – Convert weak resume bullet points into strong,
                     quantified achievement statements using LLM.
"""

from src.rag_chain import bullet_improver_chain
from src.utils import clean_text


def improve_bullets(weak_bullets: str, role: str = "Software Engineer") -> str:
    """
    Improve a block of weak resume bullet points.

    Parameters
    ----------
    weak_bullets : str
        Newline-separated bullet points as typed by the user.
    role : str
        The target job role context (helps the LLM tailor language).

    Returns
    -------
    str
        Improved bullet points, one per line.
    """
    chain = bullet_improver_chain()
    try:
        result = chain.invoke({"bullets": weak_bullets, "role": role})
        return clean_text(result)
    except Exception as exc:
        raise RuntimeError(f"Bullet improvement failed: {exc}") from exc


def parse_bullets(text: str) -> list[str]:
    """
    Parse a block of bullet text into a list of individual bullet strings.
    Handles lines starting with -, •, *, numbers, or plain text.
    """
    lines = text.strip().splitlines()
    bullets: list[str] = []
    for line in lines:
        line = line.strip().lstrip("-•*·").strip()
        # Strip leading number + dot (e.g. "1. " or "1) ")
        import re
        line = re.sub(r"^\d+[\.\)]\s*", "", line)
        if line:
            bullets.append(line)
    return bullets
