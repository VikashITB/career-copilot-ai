"""
career_agent.py
---------------
Central orchestrator for the Career Copilot AI Agent.

Flow:
  1. Receive goal + resume + JD
  2. Planner creates initial tool plan
  3. Execute tools step by step
  4. After each step, re-evaluate plan adaptively
  5. Return complete results with execution trace
"""

import streamlit as st
from src.agent.memory import AgentMemory
from src.agent.planner import Planner
from src.agent.tool_registry import Tool, ToolRegistry

# Import all tool functions
from src.tools.ats_tool import run_ats_tool
from src.tools.bullet_tool import run_bullet_tool
from src.tools.advisor_tool import run_advisor_tool
from src.tools.generator_tool import run_generator_tool
from src.tools.matcher_tool import run_matcher_tool


# ── Build Tool Registry ───────────────────────────────────

def build_registry() -> ToolRegistry:
    """Register all available tools."""
    registry = ToolRegistry()

    registry.register(Tool(
        name="ats_scorer",
        description="Score resume against job description for ATS compatibility",
        fn=run_ats_tool,
        requires=[],
    ))

    registry.register(Tool(
        name="job_matcher",
        description="Semantic job matching using FAISS vector search",
        fn=run_matcher_tool,
        requires=[],
    ))

    registry.register(Tool(
        name="bullet_improver",
        description="Improve resume bullet points for impact and ATS keywords",
        fn=run_bullet_tool,
        requires=["ats_scorer"],
    ))

    registry.register(Tool(
        name="resume_generator",
        description="Generate a tailored resume for the target role",
        fn=run_generator_tool,
        requires=["bullet_improver"],
    ))

    registry.register(Tool(
        name="career_advisor",
        description="Generate personalized career roadmap and project recommendations",
        fn=run_advisor_tool,
        requires=[],
    ))

    return registry


# ── Career Agent ─────────────────────────────────────────

class CareerAgent:
    """
    Lightweight agentic orchestrator.
    Dynamically plans, executes, and adapts tool selection
    based on the user's goal and intermediate results.
    """

    def __init__(self):
        self.registry = build_registry()
        self.planner = Planner()

    def run(
        self,
        goal: str,
        resume_text: str,
        job_description: str,
        target_role: str = "",
        use_streamlit: bool = True,
    ) -> AgentMemory:
        """
        Execute the full agentic pipeline.

        Args:
            goal: User's natural language goal
            resume_text: Raw resume text
            job_description: Target job description
            target_role: Explicit role name if provided
            use_streamlit: Whether to show live progress in Streamlit

        Returns:
            Populated AgentMemory with all results
        """

        # ── Initialize memory ─────────────────────────
        memory = AgentMemory(
            goal=goal,
            resume_text=resume_text,
            job_description=job_description,
            target_role=target_role or goal,
        )

        # ── Create initial plan ───────────────────────
        plan = self.planner.create_plan(goal, memory)

        if use_streamlit:
            st.info(f"🧠 **Agent Goal:** {goal}")
            st.info(f"📋 **Initial Plan:** {' → '.join(plan)}")

        # ── Execute steps adaptively ──────────────────
        max_steps = 8  # Safety limit
        step_count = 0

        while plan and step_count < max_steps:
            step_count += 1
            tool_name = plan[0]
            tool = self.registry.get(tool_name)

            if not tool:
                plan.pop(0)
                continue

            # Check prerequisites
            if not tool.can_run(memory):
                plan.pop(0)
                continue

            # Execute tool
            if use_streamlit:
                with st.spinner(f"⚙️ Running: **{tool_name}**..."):
                    result = tool.fn(memory)
                st.success(f"✅ Completed: **{tool_name}**")
            else:
                result = tool.fn(memory)

            # Remove completed step
            plan.pop(0)

            # ── Adaptive re-planning ──────────────────
            plan = self.planner.adapt_plan(plan, memory)

            if use_streamlit and plan:
                st.caption(f"🔄 Adapted plan: {' → '.join(plan)}")

        if use_streamlit:
            st.success(f"🎯 Agent completed {len(memory.steps_executed)} steps!")

        return memory


# ── Convenience runner ────────────────────────────────────

def run_career_agent(
    goal: str,
    resume_text: str,
    job_description: str,
    target_role: str = "",
    use_streamlit: bool = True,
) -> AgentMemory:
    """Simple entry point for the agent."""
    agent = CareerAgent()
    return agent.run(goal, resume_text, job_description, target_role, use_streamlit)