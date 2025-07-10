"""Tool to read previously failed/updated DBML schema from state."""

from langchain_core.tools import tool
from ..models.state import get_state


@tool
def read_updated_dbml() -> str:
    """INTERNAL: Get previously failed schema for agent comparison."""
    try:
        state = get_state()
        return state.updated_dbml or ""
    except Exception as e:
        return f"Error reading updated schema: {str(e)}" 