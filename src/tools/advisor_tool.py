"""
advisor_tool.py
---------------
Wraps career_advisor.py as an agent-compatible tool.
Uses full memory context for personalized roadmap.
"""

from src.agent.memory import AgentMemory


def run_advisor_tool(memory: AgentMemory) -> str:
    """
    Generate career roadmap using all available context.
    Context-aware: uses ATS gaps, role, and goal.
    """
    from src.career_advisor import get_career_roadmap

    try:
        # Extract skills from resume or use missing skills from ATS
        current_skills = memory.resume_text[:500]  # First 500 chars as skill context
        if memory.ats_result and memory.ats_result.get("matched_keywords"):
            current_skills = ", ".join(memory.ats_result["matched_keywords"])

        # Use target role from memory
        target_role = memory.target_role or memory.goal or "Software Engineer"

        # Default current role if not specified
        current_role = "Software Developer"  # Could be extracted from resume

        # Default years of experience
        years_exp = "3"  # Could be extracted from resume

        result = get_career_roadmap(
            current_role=current_role,
            target_role=target_role,
            current_skills=current_skills,
            years_exp=years_exp,
        )

        memory.advisor_result = result
        memory.log_step("career_advisor", result)
        return result

    except Exception as e:
        memory.log_step("career_advisor", str(e))
        return f"Error generating roadmap: {e}"