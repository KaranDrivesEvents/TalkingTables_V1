"""Integration tests for the agent graph."""

import pytest
from unittest.mock import patch, MagicMock
from src.agent.graph import create_graph
from src.agent.state import reset_agent_state


@pytest.fixture
def mock_openai():
    """Mock OpenAI API calls."""
    with patch('src.nodes.main_processor.ChatOpenAI') as mock:
        mock_instance = MagicMock()
        mock_instance.invoke.return_value = MagicMock(content="Test response")
        mock.return_value.bind_tools.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_parser_service():
    """Mock parser service calls."""
    with patch('src.services.parser_client.make_parser_request') as mock:
        mock.return_value = {
            "dbml_json": {"tables": []},
            "diff_json": {"changes": []},
            "errors": []
        }
        yield mock


class TestAgentGraph:
    """Test the complete agent graph workflow."""
    
    def setup_method(self):
        """Reset state before each test."""
        reset_agent_state()
    
    def test_graph_creation(self):
        """Test that the graph can be created successfully."""
        graph = create_graph()
        assert graph is not None
    
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
    def test_collaborative_mode_flow(self, mock_openai, mock_parser_service):
        """Test collaborative mode workflow."""
        graph = create_graph()
        
        # Test collaborative query
        result = graph.invoke({
            "user_message": "What's the best way to model user authentication?"
        })
        
        assert "agent_response" in result or "final_response" in result
    
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
    def test_directive_mode_flow(self, mock_openai, mock_parser_service):
        """Test directive mode workflow with successful schema change."""
        graph = create_graph()
        
        # Test directive command
        result = graph.invoke({
            "user_message": "Add a users table with email and name fields"
        })
        
        # Should complete successfully
        assert "final_response" in result or "agent_response" in result 