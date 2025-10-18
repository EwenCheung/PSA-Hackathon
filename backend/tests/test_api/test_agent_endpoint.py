"""Tests for the AI agent chat API endpoint."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from app.main import app

client = TestClient(app)


def test_agent_chat_missing_env_vars():
    """Test that endpoint returns 503 when Azure OpenAI not configured."""
    # Clear all Azure env vars to simulate missing configuration
    with patch.dict('os.environ', {}, clear=True):
        response = client.post(
            "/api/v1/mentoring/agent/chat",
            json={"message": "Find me a mentor"}
        )
        
        assert response.status_code == 503
        data = response.json()
        assert "detail" in data
        assert "AI agent not configured" in str(data["detail"])
        assert "missing_variables" in data["detail"]


def test_agent_chat_empty_message():
    """Test that endpoint returns 422 for empty message (Pydantic validation)."""
    with patch.dict('os.environ', {
        'AZURE_OPENAI_API_KEY': 'test-key',
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com',
        'AZURE_OPENAI_API_VERSION': '2024-02-15-preview',
        'AZURE_OPENAI_DEPLOYMENT': 'gpt-4'
    }):
        response = client.post(
            "/api/v1/mentoring/agent/chat",
            json={"message": ""}
        )
        
        assert response.status_code == 422  # Pydantic validation error
        data = response.json()
        assert "detail" in data


def test_agent_chat_whitespace_message():
    """Test that endpoint returns 422 for whitespace-only message."""
    with patch.dict('os.environ', {
        'AZURE_OPENAI_API_KEY': 'test-key',
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com',
        'AZURE_OPENAI_API_VERSION': '2024-02-15-preview',
        'AZURE_OPENAI_DEPLOYMENT': 'gpt-4'
    }):
        response = client.post(
            "/api/v1/mentoring/agent/chat",
            json={"message": "   "}
        )
        
        assert response.status_code == 422  # Pydantic validation error


@patch('app.agent.mentoring_agent.agent.run_agent_query')
def test_agent_chat_success(mock_run_agent):
    """Test successful agent chat response."""
    # Mock the agent response
    mock_run_agent.return_value = {
        'output': 'I found 3 mentors with cloud architecture expertise.',
        'intermediate_steps': []
    }
    
    with patch.dict('os.environ', {
        'AZURE_OPENAI_API_KEY': 'test-key',
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com',
        'AZURE_OPENAI_API_VERSION': '2024-02-15-preview',
        'AZURE_OPENAI_DEPLOYMENT': 'gpt-4'
    }):
        response = client.post(
            "/api/v1/mentoring/agent/chat",
            json={
                "message": "Find me a mentor for cloud architecture",
                "employee_id": "EMP005"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert data["response"] == 'I found 3 mentors with cloud architecture expertise.'
        assert data["error"] is None
        assert "tools_used" in data


@patch('app.agent.mentoring_agent.agent.run_agent_query')
def test_agent_chat_with_history(mock_run_agent):
    """Test agent chat with conversation history."""
    mock_run_agent.return_value = {
        'output': 'Based on our previous conversation, here are more details...'
    }
    
    with patch.dict('os.environ', {
        'AZURE_OPENAI_API_KEY': 'test-key',
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com',
        'AZURE_OPENAI_API_VERSION': '2024-02-15-preview',
        'AZURE_OPENAI_DEPLOYMENT': 'gpt-4'
    }):
        response = client.post(
            "/api/v1/mentoring/agent/chat",
            json={
                "message": "Tell me more about the first mentor",
                "employee_id": "EMP005",
                "chat_history": [
                    {"role": "user", "content": "Find mentors"},
                    {"role": "assistant", "content": "Here are 3 mentors..."}
                ]
            }
        )
        
        assert response.status_code == 200
        
        # Verify chat history was passed to agent
        mock_run_agent.assert_called_once()
        call_kwargs = mock_run_agent.call_args.kwargs
        assert 'chat_history' in call_kwargs
        assert len(call_kwargs['chat_history']) == 2


@patch('app.agent.mentoring_agent.agent.run_agent_query')
def test_agent_chat_import_error(mock_run_agent):
    """Test handling of missing dependencies."""
    mock_run_agent.side_effect = ImportError("No module named 'langchain'")
    
    with patch.dict('os.environ', {
        'AZURE_OPENAI_API_KEY': 'test-key',
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com',
        'AZURE_OPENAI_API_VERSION': '2024-02-15-preview',
        'AZURE_OPENAI_DEPLOYMENT': 'gpt-4'
    }):
        response = client.post(
            "/api/v1/mentoring/agent/chat",
            json={"message": "Find me a mentor"}
        )
        
        assert response.status_code == 503
        data = response.json()
        assert "AI dependencies not installed" in str(data["detail"])


@patch('app.agent.mentoring_agent.agent.run_agent_query')
def test_agent_chat_value_error(mock_run_agent):
    """Test handling of configuration errors."""
    mock_run_agent.side_effect = ValueError("Missing required environment variables: AZURE_OPENAI_API_KEY")
    
    with patch.dict('os.environ', {
        'AZURE_OPENAI_API_KEY': 'test-key',
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com',
        'AZURE_OPENAI_API_VERSION': '2024-02-15-preview',
        'AZURE_OPENAI_DEPLOYMENT': 'gpt-4'
    }):
        response = client.post(
            "/api/v1/mentoring/agent/chat",
            json={"message": "Find me a mentor"}
        )
        
        assert response.status_code == 503
        data = response.json()
        assert "configuration error" in str(data["detail"]).lower()


@patch('app.agent.mentoring_agent.agent.run_agent_query')
def test_agent_chat_unexpected_error(mock_run_agent):
    """Test handling of unexpected errors."""
    mock_run_agent.side_effect = RuntimeError("Unexpected error occurred")
    
    with patch.dict('os.environ', {
        'AZURE_OPENAI_API_KEY': 'test-key',
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com',
        'AZURE_OPENAI_API_VERSION': '2024-02-15-preview',
        'AZURE_OPENAI_DEPLOYMENT': 'gpt-4'
    }):
        response = client.post(
            "/api/v1/mentoring/agent/chat",
            json={"message": "Find me a mentor"}
        )
        
        assert response.status_code == 500
        data = response.json()
        assert "Agent execution failed" in str(data["detail"])
        assert "type" in data["detail"]


@patch('app.agent.mentoring_agent.agent.run_agent_query')
def test_agent_chat_response_schema(mock_run_agent):
    """Test that response matches expected schema."""
    mock_run_agent.return_value = {
        'output': 'Test response',
        'intermediate_steps': []
    }
    
    with patch.dict('os.environ', {
        'AZURE_OPENAI_API_KEY': 'test-key',
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com',
        'AZURE_OPENAI_API_VERSION': '2024-02-15-preview',
        'AZURE_OPENAI_DEPLOYMENT': 'gpt-4'
    }):
        response = client.post(
            "/api/v1/mentoring/agent/chat",
            json={"message": "Test"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Check all required fields
        assert "response" in data
        assert "success" in data
        assert "error" in data
        assert "tools_used" in data
        
        # Check types
        assert isinstance(data["response"], str)
        assert isinstance(data["success"], bool)
        assert data["tools_used"] is None or isinstance(data["tools_used"], list)


def test_agent_chat_endpoint_in_openapi():
    """Test that endpoint is documented in OpenAPI spec."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    
    openapi = response.json()
    paths = openapi["paths"]
    
    assert "/api/v1/mentoring/agent/chat" in paths
    assert "post" in paths["/api/v1/mentoring/agent/chat"]
    
    # Check documentation
    endpoint_spec = paths["/api/v1/mentoring/agent/chat"]["post"]
    assert "summary" in endpoint_spec or "description" in endpoint_spec
    assert "requestBody" in endpoint_spec
    assert "responses" in endpoint_spec
