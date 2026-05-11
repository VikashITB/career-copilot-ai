"""
ats_tool.py
-----------
Wraps ats_scorer.py as an agent-compatible tool.
Updates memory with ATS score and triggers adaptive flags.
"""

from src.agent.memory import AgentMemory


def run_ats_tool(memory: AgentMemory) -> dict:
    """
    Run ATS scoring on resume vs job description.
    Updates memory with score and skill gap flags.
    """
    from src.ats_scorer import score_resume

    try:
        result = score_resume(
            resume_text=memory.resume_text,
            job_description=memory.job_description,
        )

        # Convert ATSResult to dict for memory storage
        result_dict = {
            "score": result.score,
            "matched_keywords": result.matched_keywords,
            "missing_keywords": result.missing_keywords,
            "missing_skills": result.missing_keywords,  # Alias for adaptive rules
            "section_scores": result.section_scores,
            "action_verb_count": result.action_verb_count,
            "word_count": result.word_count,
            "feedback": result.feedback,
        }

        # Update memory with results
        memory.ats_result = result_dict
        memory.ats_score = result_dict.get("score", 0)

        # Set adaptive flags
        if memory.ats_score < 60:
            memory.skill_gaps_detected = True

        if result_dict.get("missing_skills"):
            memory.skill_gaps_detected = True

        memory.log_step("ats_scorer", result_dict)
        return result_dict

    except Exception as e:
        error = {"error": str(e), "score": 0}
        memory.log_step("ats_scorer", error)
        return error