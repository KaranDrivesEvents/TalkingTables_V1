"""Node definitions for the TalkingTables StateGraph."""

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from src.models.state import TalkingTablesState
from src.tools import call_dbml_parser, read_current_dbml
from src.config.settings import OPENAI_API_KEY, LLM_MODEL, LLM_TEMPERATURE
from src.agent.react_prompts import TALKING_TABLES_PROMPT

# 1. Define the list of executable tool functions
tools = [call_dbml_parser, read_current_dbml]

# 2. Instantiate the ToolNode with our list of tools. This is the "Hands".
#    It will automatically execute the correct tool based on the LLM's decision.
tool_node = ToolNode(tools)

# 3. Define the Agent Node. This is the "Brain".
def agent_node(state: TalkingTablesState):
    """
    Invokes the LLM to decide the next action or respond to the user.
    """
    # Create the LLM instance and bind the tools to it.
    # This tells the LLM what tools it has available.
    llm = ChatOpenAI(model=LLM_MODEL, temperature=LLM_TEMPERATURE, api_key=OPENAI_API_KEY)
    llm_with_tools = llm.bind_tools(tools)
    
    # Use the prompt template with the current messages
    # Fix: Use dot notation for Pydantic object instead of dictionary access
    prompt = TALKING_TABLES_PROMPT.format(messages=state.messages)
    response = llm_with_tools.invoke(prompt)
    return {"messages": [response]} 