"""
resume_generator.py – LLM-powered resume generation.

Takes user profile information and generates a full, ATS-optimised
plain-text resume via the LangChain chain defined in rag_chain.py.
"""

from dataclasses import dataclass
from src.rag_chain import resume_generator_chain
from src.utils import clean_text


@dataclass
class ResumeProfile:
    """Stores the user inputs required to generate a resume."""
    name: str
    role: str
    years_exp: str
    skills: str
    experience: str
    education: str
    projects: str


def generate_resume(profile: ResumeProfile) -> str:
    """
    Generate a full resume for *profile* using the LLM chain.

    Returns plain text resume content.
    Raises RuntimeError if the LLM call fails.
    """
    chain = resume_generator_chain()
    try:
        result = chain.invoke(
            {
                "name": profile.name,
                "role": profile.role,
                "years_exp": profile.years_exp,
                "skills": profile.skills,
                "experience": profile.experience,
                "education": profile.education,
                "projects": profile.projects,
            }
        )
        return clean_text(result)
    except Exception as exc:
        raise RuntimeError(f"Resume generation failed: {exc}") from exc


def resume_to_download_bytes(resume_text: str) -> bytes:
    """Convert resume text to UTF-8 bytes for Streamlit download button."""
    return resume_text.encode("utf-8")
