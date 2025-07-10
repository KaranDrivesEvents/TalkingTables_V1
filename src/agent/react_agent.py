"""Standard LangGraph ReAct agent for TalkingTables."""

from typing import Dict, Any
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from ..agent.react_prompts import TALKING_TABLES_SYSTEM_PROMPT
from ..tools import get_dbml_tools
from ..config.settings import get_settings


def create_talking_tables_agent():
    """Create standard ReAct agent following LangGraph best practices."""
    
    # Get settings
    settings = get_settings()
    
    # Initialize the LLM
    llm = ChatOpenAI(
        model=settings.llm.model_name,
        temperature=settings.llm.temperature,
        max_tokens=settings.llm.max_tokens,
        api_key=settings.llm.api_key
    )
    
    # Get tools
    tools = get_dbml_tools()
    
    # Create system message
    system_message = SystemMessage(content=TALKING_TABLES_SYSTEM_PROMPT)
    
    # Create memory saver for conversation context
    memory = MemorySaver()
    
    # Create ReAct agent with memory checkpointing
    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=system_message,
        checkpointer=memory
    )
    
    return agent 