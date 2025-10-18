"""LangChain agent for mentoring system with Azure OpenAI."""
from typing import Optional, Dict, Any, List
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnablePassthrough
from app.agent.mentoring_agent.tools import MENTORING_TOOLS
import os

from dotenv import load_dotenv
load_dotenv()
from langchain_openai import AzureChatOpenAI

# Load environment variables from .env
load_dotenv()
import getpass
import os

# System prompt for the mentoring agent
SYSTEM_PROMPT = """You are a helpful AI assistant for PSA's mentoring program.

Your role is to help employees find mentors, match mentor-mentee pairs, track mentorship progress, 
and provide insights about the mentoring program.

You have access to tools that can:
1. Search for available mentors by skill, department, or rating
2. Get detailed profiles for mentors and mentees
3. Recommend mentor-mentee matches using an intelligent algorithm
4. Analyze mentorship progress and engagement
5. Provide organization-wide mentorship statistics
6. Validate and improve mentorship goals
7. Identify skill gaps where more mentors are needed

When helping users:
- Be friendly, professional, and encouraging
- Ask clarifying questions if needed
- Explain your recommendations with clear reasoning
- Use the tools to provide data-driven insights
- Help employees set SMART (Specific, Measurable, Achievable, Relevant, Time-bound) goals

For mentor recommendations:
- Consider skill alignment, experience gap, and department fit
- Explain why each mentor is a good match
- Suggest specific focus areas for the mentorship

For employers/HR:
- Provide actionable insights about program health
- Highlight areas needing attention (e.g., skill gaps, underserved departments)
- Track engagement and progress metrics

Always ground your responses in the data from the tools. If you don't have enough information, 
ask for it or use the appropriate tool to retrieve it."""


def create_mentoring_agent() -> None:
    deployment = os.getenv("DEPLOYMENT")
    api_version = os.getenv("API_VERSION")

    llm = AzureChatOpenAI(
        azure_deployment=deployment,
        api_version=api_version,
        temperature=0.7,
        max_tokens=256,
    )

    # create_agent signature may vary by langchain version.
    # Expecting an agent that takes {"messages": List[BaseMessage]}.
    from langchain.agents import create_agent

    agent = create_agent(
        model=llm,
        tools=[],
        system_prompt=SYSTEM_PROMPT,
)
    return agent



def run_agent_query(
    query: str,
    chat_history: Optional[List] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Run a single query through the mentoring agent with manual tool execution.
    
    This function implements a tool execution loop because the standard LangChain
    AgentExecutor has import issues with the current package versions.
    
    Args:
        query: User's question or request
        chat_history: Optional conversation history
        **kwargs: Additional parameters for agent creation
    
    Returns:
        Dictionary with agent's response and intermediate steps
    
    Example:
        >>> result = run_agent_query("Find mentors who know Python")
        >>> print(result['output'])
        "I found 3 Python mentors: Dr. Sarah Chen (rating 4.9)..."
    """
    from langchain_core.messages import ToolMessage, SystemMessage, HumanMessage
    
    # Create the agent chain
    agent_chain = create_mentoring_agent(**kwargs)
    
    # Initialize LLM from the chain (it's the last element after the pipe)
    # The chain is: prompt | llm_with_tools
    llm_with_tools = agent_chain.steps[-1] if hasattr(agent_chain, 'steps') else agent_chain.last
    
    # Build initial messages
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=query)
    ]
    
    # Add chat history if provided
    if chat_history:
        # Insert chat history before the current query
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + chat_history + [HumanMessage(content=query)]
    
    # Tool execution loop (max 5 iterations to prevent infinite loops)
    intermediate_steps = []
    
    for iteration in range(5):
        try:
            # Get LLM response
            response = llm_with_tools.invoke(messages)
            
            # Check if LLM wants to call tools
            if not hasattr(response, 'tool_calls') or not response.tool_calls:
                # No tools to call - we have the final answer
                return {
                    "output": response.content if hasattr(response, 'content') else str(response),
                    "intermediate_steps": intermediate_steps
                }
            
            # Add AI message to history
            messages.append(response)
            
            # Execute each tool call
            for tool_call in response.tool_calls:
                tool_name = tool_call.get('name', '')
                tool_args = tool_call.get('args', {})
                tool_id = tool_call.get('id', f'call_{iteration}')
                
                # Record the tool call
                intermediate_steps.append({
                    'tool': tool_name,
                    'args': tool_args,
                    'iteration': iteration
                })
                
                # Find and execute the tool
                tool_function = next(
                    (t for t in MENTORING_TOOLS if t.name == tool_name),
                    None
                )
                
                if tool_function:
                    try:
                        # Execute the tool
                        tool_result = tool_function.invoke(tool_args)
                        
                        # Add tool result to messages
                        tool_message = ToolMessage(
                            content=str(tool_result),
                            tool_call_id=tool_id
                        )
                        messages.append(tool_message)
                        
                        # Record successful execution
                        intermediate_steps[-1]['result'] = 'success'
                        intermediate_steps[-1]['result_preview'] = str(tool_result)[:100]
                        
                    except Exception as e:
                        # Add error message
                        error_msg = f"Error executing {tool_name}: {str(e)}"
                        tool_message = ToolMessage(
                            content=error_msg,
                            tool_call_id=tool_id
                        )
                        messages.append(tool_message)
                        
                        # Record error
                        intermediate_steps[-1]['result'] = 'error'
                        intermediate_steps[-1]['error'] = str(e)
                else:
                    # Tool not found
                    error_msg = f"Tool '{tool_name}' not found in available tools"
                    tool_message = ToolMessage(
                        content=error_msg,
                        tool_call_id=tool_id
                    )
                    messages.append(tool_message)
                    
                    intermediate_steps[-1]['result'] = 'not_found'
        
        except Exception as e:
            # Catch any unexpected errors in the loop
            return {
                "output": f"Sorry, I encountered an error: {str(e)}",
                "intermediate_steps": intermediate_steps,
                "error": str(e)
            }
    
    # If we hit max iterations, return what we have
    return {
        "output": "I've processed your request but reached the maximum number of tool calls. Please try rephrasing your question.",
        "intermediate_steps": intermediate_steps
    }


# Convenience functions for common queries

def find_mentors(
    skill_area: Optional[str] = None,
    department: Optional[str] = None,
    min_rating: float = 0.0
) -> Dict[str, Any]:
    """Find available mentors matching criteria."""
    query_parts = ["Find available mentors"]
    
    if skill_area:
        query_parts.append(f"with expertise in {skill_area}")
    if department:
        query_parts.append(f"in department {department}")
    if min_rating > 0:
        query_parts.append(f"with rating at least {min_rating}")
    
    query = " ".join(query_parts)
    return run_agent_query(query)


def recommend_mentor_for_employee(
    employee_id: str,
    career_goals: list,
    desired_skills: list
) -> Dict[str, Any]:
    """Get personalized mentor recommendations."""
    query = (
        f"Recommend mentors for employee {employee_id}. "
        f"Their career goals are: {', '.join(career_goals)}. "
        f"They want to learn: {', '.join(desired_skills)}."
    )
    return run_agent_query(query)


def get_program_insights(department: Optional[str] = None) -> Dict[str, Any]:
    """Get mentorship program statistics and insights."""
    if department:
        query = f"Provide mentorship program statistics and insights for department {department}"
    else:
        query = "Provide organization-wide mentorship program statistics and identify any areas needing attention"
    
    return run_agent_query(query)
