"""Core agent package for the TalkingTables ReAct agent."""

from .react_agent import create_talking_tables_agent
from .react_prompts import TALKING_TABLES_SYSTEM_PROMPT

__all__ = [
    "create_talking_tables_agent",
    "TALKING_TABLES_SYSTEM_PROMPT"
] 