"""Pydantic models for structured LLM outputs."""

from pydantic import BaseModel, Field
from typing import List, Optional


class DBMLParserInput(BaseModel):
    """Input schema for DBML parser tool."""
    
    current_dbml: str = Field(
        description="Current DBML schema content"
    )
    updated_dbml: str = Field(
        description="Updated DBML schema to validate"
    ) 