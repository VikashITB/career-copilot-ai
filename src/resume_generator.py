"""Resume generation using LLM."""

from dataclasses import dataclass
from src.rag_chain import resume_generator_chain
from src.utils import clean_text


@dataclass
class ResumeProfile:
    """User profile data for resume generation."""
    name: str
    role: str
    years_exp: str
    skills: str
    experience: str
    education: str
    projects: str


def generate_resume(profile: ResumeProfile) -> str:
    """Generate ATS-optimized resume from user profile."""
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
    """Convert resume text to bytes for download."""
    return resume_text.encode("utf-8")
