"""Tests for the LangChain mentoring agent."""
import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from app.agent.mentoring_agent.agent import (
    create_mentoring_agent,
    run_agent_query,
    find_mentors,
    recommend_mentor_for_employee,
    get_program_insights,
    SYSTEM_PROMPT
)


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Set up mock environment variables for Azure OpenAI."""
    monkeypatch.setenv("AZURE_OPENAI_API_KEY", "test-key-12345")
    monkeypatch.setenv("AZURE_OPENAI_ENDPOINT", "https://test.openai.azure.com")
    monkeypatch.setenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    monkeypatch.setenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4")


def test_system_prompt_contains_key_info():
    """Test that system prompt has essential instructions."""
    assert "mentoring program" in SYSTEM_PROMPT.lower()
    assert "tools" in SYSTEM_PROMPT.lower()
    assert "mentor" in SYSTEM_PROMPT.lower()
    assert len(SYSTEM_PROMPT) > 100  # Should be substantial


def test_create_agent_missing_env_vars():
    """Test agent creation fails gracefully with missing env vars."""
    # Clear all Azure env vars
    env_backup = {k: os.environ.get(k) for k in [
        'AZURE_OPENAI_API_KEY', 
        'AZURE_OPENAI_ENDPOINT', 
        'AZURE_OPENAI_API_VERSION',
        'AZURE_OPENAI_DEPLOYMENT'
    ]}
    
    for key in env_backup.keys():
        os.environ.pop(key, None)
    
    # Should raise ValueError for missing vars
    with pytest.raises(ValueError) as exc_info:
        create_mentoring_agent()
    
    assert "Missing required environment variables" in str(exc_info.value)
    
    # Restore env vars
    for key, value in env_backup.items():
        if value is not None:
            os.environ[key] = value


def test_create_agent_missing_deployment(mock_env_vars, monkeypatch):
    """Test agent creation fails without deployment name."""
    monkeypatch.delenv("AZURE_OPENAI_DEPLOYMENT", raising=False)
    
    with pytest.raises(ValueError) as exc_info:
        create_mentoring_agent()
    
    assert "deployment name" in str(exc_info.value).lower()


@patch('app.agent.mentoring_agent.agent.AzureChatOpenAI')
def test_create_agent_with_defaults(mock_llm, mock_env_vars):
    """Test agent creation with default parameters."""
    # Mock the LLM and bind_tools method
    mock_llm_instance = Mock()
    mock_llm_instance.bind_tools.return_value = mock_llm_instance
    mock_llm.return_value = mock_llm_instance
    
    agent_executor = create_mentoring_agent()
    
    # Verify LLM was initialized with correct params
    mock_llm.assert_called_once()
    call_kwargs = mock_llm.call_args.kwargs
    assert call_kwargs['azure_deployment'] == 'gpt-4'
    assert call_kwargs['temperature'] == 0.7
    assert call_kwargs['streaming'] == False
    
    # Verify bind_tools was called
    mock_llm_instance.bind_tools.assert_called_once()
    
    # Verify agent executor is returned
    assert agent_executor is not None


@patch('app.agent.mentoring_agent.agent.AzureChatOpenAI')
def test_create_agent_with_custom_params(mock_llm, mock_env_vars):
    """Test agent creation with custom parameters."""
    mock_llm_instance = Mock()
    mock_llm_instance.bind_tools.return_value = mock_llm_instance
    mock_llm.return_value = mock_llm_instance
    
    create_mentoring_agent(
        model="gpt-4-turbo",
        temperature=0.3,
        streaming=True
    )
    
    call_kwargs = mock_llm.call_args.kwargs
    assert call_kwargs['azure_deployment'] == 'gpt-4-turbo'
    assert call_kwargs['temperature'] == 0.3
    assert call_kwargs['streaming'] == True


@patch('app.agent.mentoring_agent.agent.create_mentoring_agent')
def test_run_agent_query_basic(mock_create_agent, mock_env_vars):
    """Test running a basic query through the agent."""
    # Mock agent chain
    mock_chain = Mock()
    mock_response = Mock()
    mock_response.content = 'Here are the mentors...'
    mock_chain.invoke.return_value = mock_response
    mock_create_agent.return_value = mock_chain
    
    result = run_agent_query("Find mentors for Python")
    
    assert 'output' in result
    assert result['output'] == 'Here are the mentors...'
    mock_chain.invoke.assert_called_once()


@patch('app.agent.mentoring_agent.agent.create_mentoring_agent')
def test_run_agent_query_with_history(mock_create_agent, mock_env_vars):
    """Test running query with chat history."""
    mock_executor = Mock()
    mock_executor.invoke.return_value = {'output': 'Response', 'intermediate_steps': []}
    mock_create_agent.return_value = mock_executor
    
    chat_history = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi!"}
    ]
    
    result = run_agent_query("Continue", chat_history=chat_history)
    
    call_args = mock_executor.invoke.call_args[0][0]
    assert 'chat_history' in call_args
    assert call_args['chat_history'] == chat_history


@patch('app.agent.mentoring_agent.agent.run_agent_query')
def test_find_mentors_convenience_function(mock_run_query, mock_env_vars):
    """Test find_mentors convenience function builds correct query."""
    mock_run_query.return_value = {'output': 'Results', 'intermediate_steps': []}
    
    find_mentors(skill_area="Python", department="DEPT001", min_rating=4.5)
    
    # Check the query string contains all criteria
    call_args = mock_run_query.call_args[0][0]
    assert "python" in call_args.lower()
    assert "DEPT001" in call_args
    assert "4.5" in call_args


@patch('app.agent.mentoring_agent.agent.run_agent_query')
def test_recommend_mentor_for_employee(mock_run_query, mock_env_vars):
    """Test recommend_mentor_for_employee convenience function."""
    mock_run_query.return_value = {'output': 'Recommendations', 'intermediate_steps': []}
    
    recommend_mentor_for_employee(
        employee_id="EMP001",
        career_goals=["Technical Leadership"],
        desired_skills=["Cloud Architecture", "Team Management"]
    )
    
    call_args = mock_run_query.call_args[0][0]
    assert "EMP001" in call_args
    assert "Technical Leadership" in call_args
    assert "Cloud Architecture" in call_args


@patch('app.agent.mentoring_agent.agent.run_agent_query')
def test_get_program_insights_organization_wide(mock_run_query, mock_env_vars):
    """Test get_program_insights for organization-wide stats."""
    mock_run_query.return_value = {'output': 'Insights', 'intermediate_steps': []}
    
    get_program_insights()
    
    call_args = mock_run_query.call_args[0][0]
    assert "organization-wide" in call_args.lower()
    assert "statistics" in call_args.lower()


@patch('app.agent.mentoring_agent.agent.run_agent_query')
def test_get_program_insights_by_department(mock_run_query, mock_env_vars):
    """Test get_program_insights filtered by department."""
    mock_run_query.return_value = {'output': 'Insights', 'intermediate_steps': []}
    
    get_program_insights(department="DEPT001")
    
    call_args = mock_run_query.call_args[0][0]
    assert "DEPT001" in call_args
    assert "statistics" in call_args.lower()


def test_agent_has_all_tools(mock_env_vars):
    """Verify agent is configured with all 8 mentoring tools."""
    from app.agent.mentoring_agent.tools import MENTORING_TOOLS
    
    with patch('app.agent.mentoring_agent.agent.AzureChatOpenAI') as mock_llm:
        mock_llm_instance = Mock()
        mock_llm_instance.bind_tools.return_value = mock_llm_instance
        mock_llm.return_value = mock_llm_instance
        
        create_mentoring_agent()
        
        # Verify bind_tools was called with all 8 tools
        mock_llm_instance.bind_tools.assert_called_once_with(MENTORING_TOOLS)
        assert len(MENTORING_TOOLS) == 8
