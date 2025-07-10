"""Unit tests for state management."""

import pytest
from src.agent.state import AgentState, get_agent_state, reset_agent_state, update_agent_state


def test_agent_state_creation():
    """Test that AgentState can be created with default values."""
    state = AgentState()
    assert state.current_dbml == ""
    assert state.dbml_json is None
    assert state.last_operation_status == "idle"
    assert state.self_correction_attempts == 0
    assert not state.is_in_self_correction


def test_agent_state_validation():
    """Test Pydantic validation works correctly."""
    state = AgentState(current_dbml="test schema")
    assert state.current_dbml == "test schema"
    
    # Test validation error for invalid correction attempts
    with pytest.raises(ValueError):
        AgentState(self_correction_attempts=15)


def test_global_state_management():
    """Test global state management functions."""
    # Reset to ensure clean state
    reset_agent_state()
    
    # Get initial state
    state = get_agent_state()
    assert state.current_dbml == ""
    
    # Update state
    update_agent_state(current_dbml="new schema")
    updated_state = get_agent_state()
    assert updated_state.current_dbml == "new schema"
    
    # Test invalid field update
    with pytest.raises(ValueError):
        update_agent_state(invalid_field="value") 