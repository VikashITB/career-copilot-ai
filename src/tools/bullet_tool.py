"""
bullet_tool.py
--------------
Wraps bullet_improver.py as an agent-compatible tool.
Uses ATS results from memory to improve bullets contextually.
"""

from src.agent.memory import AgentMemory


def run_bullet_tool(memory: AgentMemory) -> str:
    """
    Improve resume bullets using ATS gap context from memory.
    Context-aware: uses identified skill gaps if available.
    """
    from src.bullet_improver import improve_bullets

    try:
        # Use target role from memory, default to goal
        role = memory.target_role or memory.goal or "Software Engineer"

        # Add context about missing skills if available
        context_bullets = memory.resume_text
        if memory.ats_result and memory.ats_result.get("missing_skills"):
            gaps = memory.ats_result["missing_skills"]
            context_bullets += f"\n\nFocus on incorporating these skills: {', '.join(gaps)}"

        result = improve_bullets(
            weak_bullets=context_bullets,
            role=role,
        )

        memory.bullet_result = result
        memory.log_step("bullet_improver", result)
        return result

    except Exception as e:
        memory.log_step("bullet_improver", str(e))
        return f"Error improving bullets: {e}"