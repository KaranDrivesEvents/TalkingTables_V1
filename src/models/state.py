"""State management models for TalkingTables StateGraph agent."""

from typing import Annotated, Sequence, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class TalkingTablesState(BaseModel):
    """State model for custom StateGraph agent."""
    
    # Pydantic v2 configuration
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    # LangGraph message handling
    messages: Annotated[Sequence[BaseMessage], add_messages]
    
    # Schema state management
    current_dbml: str = Field(
        default="",
        description="Current DBML schema (gets replaced on successful parsing)"
    )
    updated_dbml: Optional[str] = Field(
        default="",
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