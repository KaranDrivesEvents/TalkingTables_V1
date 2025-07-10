"""State management models for TalkingTables ReAct agent."""

from typing import Annotated, Sequence, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langgraph.managed import IsLastStep, RemainingSteps


class TalkingTablesState(BaseModel):
    """State model with LangGraph reducers for ReAct agent."""
    
    # Pydantic v2 configuration
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    # LangGraph message handling
    messages: Annotated[Sequence[BaseMessage], add_messages]
    
    # LangGraph ReAct agent requirements
    is_last_step: IsLastStep = Field(default=False, description="Whether this is the last step")
    remaining_steps: RemainingSteps = Field(default=10, description="Number of remaining steps")
    
    # Schema state management
    current_dbml: str = Field(
        default="",
        description="Current DBML schema (gets replaced on successful parsing)"
    )
    updated_dbml: Optional[str] = Field(
        default=None,
        description="Updated DBML with user changes (for parser input)"
    )
    
    # UI rendering data
    dbml_json: Optional[Dict[str, Any]] = Field(
        default=None,
        description="JSON schema for UI rendering"
    )
    diff_json: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Diff JSON for UI rendering"
    )


# Global state for tools to access
_global_state: Optional[TalkingTablesState] = None


def update_state(updates: Dict[str, Any]) -> None:
    """Update the global state with new values.
    
    Args:
        updates: Dictionary of state updates
    """
    global _global_state
    if _global_state is None:
        _global_state = TalkingTablesState(
            messages=[],
            current_dbml="",
            updated_dbml=None,
            dbml_json=None,
            diff_json=None
        )
    
    # Update the state
    for key, value in updates.items():
        if hasattr(_global_state, key):
            setattr(_global_state, key, value)
        else:
            raise ValueError(f"Invalid state field: {key}")


def get_state() -> TalkingTablesState:
    """Get the current global state.
    
    Returns:
        Current state instance
    """
    global _global_state
    if _global_state is None:
        _global_state = TalkingTablesState(
            messages=[],
            current_dbml="",
            updated_dbml=None,
            dbml_json=None,
            diff_json=None
        )
    return _global_state 