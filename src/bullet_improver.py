"""Resume bullet point improvement using LLM."""

import re
from src.rag_chain import bullet_improver_chain
from src.utils import clean_text


def improve_bullets(weak_bullets: str, role: str = "Software Engineer") -> str:
    """Improve weak resume bullet points into strong achievements."""
    chain = bullet_improver_chain()
    try:
        result = chain.invoke({"bullets": weak_bullets, "role": role})
        return clean_text(result)
    except Exception as exc:
        raise RuntimeError(f"Bullet improvement failed: {exc}") from exc


def parse_bullets(text: str) -> list[str]:
    """Parse bullet text into list, handling various bullet formats."""
    lines = text.strip().splitlines()
    bullets: list[str] = []
    for line in lines:
        line = line.strip().lstrip("-•*·").strip()
        line = re.sub(r"^\d+[\.\)]\s*", "", line)
        if line:
            bullets.append(line)
    return bullets
