"""
matcher_tool.py
---------------
Wraps job_matcher.py as an agent-compatible tool.
Sets role mismatch flag for adaptive planning.
"""

from src.agent.memory import AgentMemory


def run_matcher_tool(memory: AgentMemory) -> dict:
    """
    Run semantic job matching using FAISS.
    Sets role_mismatch flag if score is low.
    """
    from src.job_matcher import match_jobs

    try:
        matches = match_jobs(memory.resume_text, top_k=3, explain=True)

        # Convert JobMatch objects to dict for memory storage
        if matches:
            best_match = matches[0]
            result_dict = {
                "score": best_match.match_percent,
                "similarity": best_match.similarity,
                "job_name": best_match.job_name,
                "explanation": best_match.explanation,
                "all_matches": [
                    {
                        "job_name": m.job_name,
                        "score": m.match_percent,
                        "explanation": m.explanation,
                    }
                    for m in matches
                ],
            }
        else:
            result_dict = {"score": 0, "explanation": "No matches found"}

        memory.matcher_result = result_dict
        match_score = result_dict.get("score", 0)

        # Set adaptive flag if poor match
        if match_score < 50:
            memory.role_mismatch_detected = True

        memory.log_step("job_matcher", result_dict)
        return result_dict

    except Exception as e:
        memory.log_step("job_matcher", str(e))
        return {"error": str(e), "score": 0}