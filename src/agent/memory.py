"""
memory.py
---------
Lightweight session-scoped context memory.
Stores results from each tool execution so the agent
can make adaptive decisions based on prior outputs.
"""

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class AgentMemory:
    """
    Holds context across multi-step agent execution.
    Resets per session — no persistence needed for internship scope.
    """
    goal: str = ""
    resume_text: str = ""
    job_description: str = ""
    target_role: str = ""

    # Results from each tool (populated as agent runs)
    ats_result: Optional[dict] = None
    bullet_result: Optional[str] = None
    advisor_result: Optional[str] = None
    generator_result: Optional[str] = None
    matcher_result: Optional[dict] = None

    # Adaptive flags (set by planner based on results)
    ats_score: int = 0
    skill_gaps_detected: bool = False
    role_mismatch_detected: bool = False

    # Execution log for transparency
    steps_executed: list = field(default_factory=list)
    step_outputs: dict = field(default_factory=dict)

    def log_step(self, tool_name: str, output: Any):
        """Record a completed tool execution."""
        self.steps_executed.append(tool_name)
        self.step_outputs[tool_name] = output

    def has_run(self, tool_name: str) -> bool:
        """Check if a tool has already been executed."""
        return tool_name in self.steps_executed

    def summary(self) -> str:
        """Return a human-readable execution summary."""
        lines = [f"Goal: {self.goal}", f"Steps completed: {len(self.steps_executed)}"]
        for step in self.steps_executed:
            lines.append(f"  {step}")
        return "\n".join(lines)