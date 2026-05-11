"""
generator_tool.py
-----------------
Wraps resume_generator.py as an agent-compatible tool.
Uses improved bullets from memory if available.
"""

from src.agent.memory import AgentMemory


def run_generator_tool(memory: AgentMemory) -> str:
    """
    Generate tailored resume using best available data.
    Uses improved bullets if bullet_improver ran first.
    """
    from src.resume_generator import generate_resume, ResumeProfile

    try:
        # Use improved bullets if available, else original
        experience_text = memory.bullet_result or memory.resume_text

        # Create a basic profile from available data
        profile = ResumeProfile(
            name="Your Name",  # Could be extracted from resume
            role=memory.target_role or memory.goal or "Software Engineer",
            years_exp="3",  # Could be extracted from resume
            skills=", ".join(memory.ats_result.get("matched_keywords", [])) if memory.ats_result else "Python, JavaScript",
            experience=experience_text[:1000],  # First 1000 chars
            education="Bachelor's Degree",  # Could be extracted from resume
            projects="Various projects",  # Could be extracted from resume
        )

        result = generate_resume(profile)

        memory.generator_result = result
        memory.log_step("resume_generator", result)
        return result

    except Exception as e:
        memory.log_step("resume_generator", str(e))
        return f"Error generating resume: {e}"