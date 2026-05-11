"""
planner.py
----------
Goal-based planner that determines which tools to run
and in what order, based on:
  1. The user's stated goal
  2. Adaptive rules triggered by prior tool outputs

This is the brain of the agentic system.
"""

from src.agent.memory import AgentMemory


# ── Goal → Initial Tool Plan ──────────────────────────────

GOAL_PLANS = {
    "ats_optimize": [
        "ats_scorer",
        "bullet_improver",
        "resume_generator",
    ],
    "career_roadmap": [
        "ats_scorer",
        "job_matcher",
        "career_advisor",
    ],
    "full_pipeline": [
        "ats_scorer",
        "job_matcher",
        "bullet_improver",
        "resume_generator",
        "career_advisor",
    ],
    "job_match": [
        "job_matcher",
        "ats_scorer",
        "career_advisor",
    ],
    "quick_improve": [
        "ats_scorer",
        "bullet_improver",
    ],
}


# ── Adaptive Rules ────────────────────────────────────────

def apply_adaptive_rules(memory: AgentMemory, plan: list[str]) -> list[str]:
    """
    Dynamically modify the execution plan based on
    results from already-completed steps.
    """
    updated_plan = list(plan)

    # Check if this is a career roadmap goal (should be minimal)
    is_career_goal = any(keyword in memory.goal.lower() for keyword in ["become", "career", "roadmap", "transition", "path"])
    
    # Rule 1: ATS score below 60 → force bullet improvement (but not for career goals)
    if memory.ats_result and memory.ats_score < 60 and not is_career_goal:
        if "bullet_improver" not in updated_plan:
            updated_plan.insert(1, "bullet_improver")
        if "resume_generator" not in updated_plan:
            updated_plan.append("resume_generator")

    # Rule 2: Skill gaps detected → add career advisor (only if not already in plan)
    if memory.skill_gaps_detected and "career_advisor" not in updated_plan:
        updated_plan.append("career_advisor")

    # Rule 3: Role mismatch detected → add job matcher (only if not already in plan)
    if memory.role_mismatch_detected and "job_matcher" not in updated_plan:
        updated_plan.insert(1, "job_matcher")

    # Remove already executed steps
    updated_plan = [s for s in updated_plan if not memory.has_run(s)]

    return updated_plan


# ── Goal Classifier ───────────────────────────────────────

def classify_goal(goal: str) -> str:
    """
    Map a natural language goal to a plan key.
    Uses keyword matching — simple and internship-appropriate.
    """
    goal_lower = goal.lower()

    if any(k in goal_lower for k in ["ats", "score", "optimize resume", "pass ats"]):
        return "ats_optimize"

    if any(k in goal_lower for k in ["roadmap", "career", "become", "transition", "path"]):
        return "career_roadmap"

    if any(k in goal_lower for k in ["job", "match", "apply", "find role"]):
        return "job_match"

    if any(k in goal_lower for k in ["improve", "bullets", "quick", "fast"]):
        return "quick_improve"

    # Default: run full pipeline
    return "full_pipeline"


class Planner:
    """
    Creates and adapts execution plans for the agent.
    """

    def create_plan(self, goal: str, memory: AgentMemory) -> list[str]:
        """Generate initial tool execution plan from goal."""
        plan_key = classify_goal(goal)
        plan = GOAL_PLANS.get(plan_key, GOAL_PLANS["full_pipeline"])
        memory.goal = goal
        return plan

    def adapt_plan(self, current_plan: list[str], memory: AgentMemory) -> list[str]:
        """Re-evaluate plan after each tool runs."""
        return apply_adaptive_rules(memory, current_plan)