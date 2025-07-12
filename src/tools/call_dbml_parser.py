"""Tool to call DBML parser service."""

import asyncio
from typing import Annotated, Dict, Any
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool, InjectedToolCallId
from langgraph.prebuilt import InjectedState
from langgraph.types import Command
from pydantic import BaseModel, Field
from src.models.state import TalkingTablesState
from src.services.parser_client import get_parser_client


class DBMLParseResult(BaseModel):
    """Result from DBML parser service."""
    success: bool = Field(description="Whether parsing was successful")
    message: str = Field(description="Success/error message")
    parsed_schema: dict = Field(default_factory=dict, description="Parsed schema JSON")
    diff_json: dict = Field(default_factory=dict, description="Schema differences")


@tool
def call_dbml_parser(
    updated_dbml: str,
    state: Annotated[TalkingTablesState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId]
) -> Dict[str, Any]:
    """Call the DBML parser service to analyze current vs updated schemas.
    
    Args:
        updated_dbml: The new/updated DBML schema to parse
        state: The current conversation state (contains current_dbml)
        tool_call_id: The ID of the tool call (injected by LangGraph)
    
    Compares the current DBML schema with the updated DBML schema and returns
    validation results, differences, and parsed schema information.
    Empty current DBML is fine - it means we're creating a schema from scratch.
    
    Returns:
        Dict[str, Any]: State updates dictionary with parser results
    """
    current_dbml = state.current_dbml or ""  # Empty string is fine for new schemas
    
    if not updated_dbml:
        return {"messages": [ToolMessage("Error: No updated DBML schema provided. Please provide the new DBML schema to validate.", tool_call_id=tool_call_id)]}
    
    try:
        parser_client = get_parser_client()
        
        # Run the async operation (current_dbml can be empty string)
        result = asyncio.run(parser_client.parse_dbml(current_dbml, updated_dbml))
        
        # Parse the result
        if result.get("success", False):
            parsed_schema = result.get("schema_json", {})
            diff_json = result.get("diff_json", {})

            state_updates = {
                "current_dbml": updated_dbml,
                "dbml_json": parsed_schema,
                "diff_json": diff_json,
                "updated_dbml": ""  # Clear the updated schema
            }

            # Create a ToolMessage with the tool_call_id for proper state persistence
            success_message = "✅ DBML parsing successful!"
            state_updates["messages"] = [ToolMessage(content=success_message, tool_call_id=tool_call_id)]

            # Return the dictionary inside a Command object
            # This now correctly signals a state update with proper ToolMessage
            return Command(update=state_updates)
        else:
            # Handle parser service errors (when success=False but no exception)
            error_msg = result.get("error", "Unknown parsing error")
            if isinstance(error_msg, list):
                error_msg = "; ".join(error_msg)
            return {"messages": [ToolMessage(f"DBML parsing failed: {error_msg}", tool_call_id=tool_call_id)]}
            
    except Exception as e:
        error_message = str(e)
        
        # Provide more helpful error messages for common issues
        if "Parser service error:" in error_message:
            # This is a parsed error from the parser service - pass it through
            return {"messages": [ToolMessage(f"❌ {error_message}", tool_call_id=tool_call_id)]}
        elif "Connection" in error_message or "timeout" in error_message.lower():
            return {"messages": [ToolMessage(f"❌ Connection error: Unable to reach the DBML parser service. Please check if the service is running at {parser_client.base_url}", tool_call_id=tool_call_id)]}
        elif "500" in error_message or "Internal Server Error" in error_message:
            return {"messages": [ToolMessage(f"❌ Server error: The DBML parser service encountered an internal error. Please try again or contact support.", tool_call_id=tool_call_id)]}
        else:
            return {"messages": [ToolMessage(f"❌ Error calling DBML parser service: {error_message}", tool_call_id=tool_call_id)]} 