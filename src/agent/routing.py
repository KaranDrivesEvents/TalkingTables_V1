"""Routing logic for the TalkingTables StateGraph."""

from typing import Literal
from src.models.state import TalkingTablesState


def should_continue(state: TalkingTablesState) -> Literal["tools", "__end__"]:
    """
    Router function to decide the next step.

    If the last message in the state is a tool call, route to the 'tools' node.
    Otherwise, end the execution.
    """
    # Fix: Use dot notation for Pydantic object instead of dictionary access
    last_message = state.messages[-1]
    if last_message.tool_calls:
        return "tools"
    return "__end__" 