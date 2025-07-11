"""Tool to read updated DBML schema from state."""

from typing import Annotated
from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState
from src.models.state import TalkingTablesState


@tool
def read_updated_dbml(state: Annotated[TalkingTablesState, InjectedState]) -> str:
    """Read the updated DBML schema from the conversation state.
    
    Returns:
        str: The updated DBML schema string
    """
    updated_dbml = state.updated_dbml or ""
    
    if not updated_dbml:
        return "No updated DBML schema found in state. Please provide the updated DBML schema first."
    
    return f"Updated DBML schema retrieved successfully:\n\n{updated_dbml}" 