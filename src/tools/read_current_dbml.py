"""Tool to read current DBML schema from state."""

from langchain_core.tools import tool
from ..models.state import get_state


@tool
def read_current_dbml() -> str:
    """INTERNAL: Get current DBML schema for agent context and decision-making."""
    try:
        state = get_state()
        return state.current_dbml
    except Exception as e:
        return f"Error reading schema: {str(e)}" 