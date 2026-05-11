"""
tool_registry.py
----------------
Central registry of all available agent tools.
Each tool is a callable with a standard interface:
    tool(memory: AgentMemory) -> Any

The agent dynamically selects tools based on the goal
and results of previous steps.
"""

from dataclasses import dataclass
from typing import Callable, List
from src.agent.memory import AgentMemory


@dataclass
class Tool:
    """Represents a single agent tool."""
    name: str
    description: str
    fn: Callable
    requires: List[str] = None  # prerequisite tool names

    def can_run(self, memory: AgentMemory) -> bool:
        """Check if prerequisites are satisfied."""
        if not self.requires:
            return True
        return all(memory.has_run(req) for req in self.requires)


class ToolRegistry:
    """
    Holds all registered tools.
    Agent queries this registry to select next steps.
    """

    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool):
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        return self._tools.get(name)

    def all_tools(self) -> list[Tool]:
        return list(self._tools.values())

    def available_tools(self, memory: AgentMemory) -> list[Tool]:
        """Return tools whose prerequisites are met and haven't run yet."""
        return [
            t for t in self._tools.values()
            if t.can_run(memory) and not memory.has_run(t.name)
        ]

    def names(self) -> list[str]:
        return list(self._tools.keys())

    def values(self) -> list[Tool]:
        return list(self._tools.values())