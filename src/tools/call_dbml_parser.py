"""Tool to call the DBML parser service."""

from langchain_core.tools import tool
from ..models.state import get_state, update_state
from ..services.parser_client import make_parser_request


@tool
def call_dbml_parser(updated_dbml: str) -> str:
    """Convert updated_dbml to JSON schema for UI rendering and update state if successful.
    
    Args:
        updated_dbml: Updated DBML schema to validate
    """
    try:
        # Auto-fetch current schema from state
        current_dbml = get_state().current_dbml
        
        # HTTP request to parser service with current_dbml and updated_dbml
        response = make_parser_request(current_dbml, updated_dbml)
        
        # Check if the response indicates success
        if response.get("errors"):
            # FAILURE: Return error details for user
            errors = response.get("errors", [])
            error_messages = []
            for error in errors:
                error_type = error.get("error_type", "Unknown")
                message = error.get("message", "Unknown error")
                error_messages.append(f"{error_type}: {message}")
            
            # Store updated_dbml for potential user review
            update_state({"updated_dbml": updated_dbml})
            
            return f"❌ Schema parsing failed: {'; '.join(error_messages)}"
        
        else:
            # SUCCESS: Update state with new schema data
            # Use schema_json instead of dbml_json to match actual parser service response
            update_state({
                'current_dbml': updated_dbml,  # Replace current with updated
                'dbml_json': response.get('schema_json'),  # JSON schema from parser (schema_json -> dbml_json for internal state)
                'diff_json': response.get('diff_json'),  # Diff for UI rendering
                'updated_dbml': None  # Clear the updated_dbml since it's now current
            })
            
            return "✅ Schema validation successful! Changes applied and state updated."
            
    except Exception as e:
        return f"❌ Parser service error: {str(e)}" 