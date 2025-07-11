"""Tool to read current DBML schema from state."""

from typing import Annotated
from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState
from src.models.state import TalkingTablesState


@tool
def read_current_dbml(state: Annotated[TalkingTablesState, InjectedState]) -> str:
    """Read the current DBML schema from the conversation state.
    
    Returns:
        str: The current DBML schema string or indication that we're starting fresh
    """
    current_dbml = state.current_dbml or ""
    
    if not current_dbml:
        return "Current DBML schema is empty. Ready to create a new database schema from scratch!"
    
    return f"Current DBML schema retrieved successfully:\n\n{current_dbml}" 