"""Custom StateGraph definition for TalkingTables agent."""

from langgraph.graph import StateGraph
from src.models.state import TalkingTablesState
import os
# Import our modular components using absolute imports
from src.agent.nodes import agent_node, tool_node
from src.agent.routing import should_continue


def create_graph():
    """
    Assembles the custom StateGraph for our agent.
    """
    workflow = StateGraph(TalkingTablesState)

    # 1. Add the nodes to the graph
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)

    # 2. Define the entry point of the graph
    workflow.set_entry_point("agent")

    # 3. Add the conditional router edge
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "__end__": "__end__",
        },
    )

    # 4. Add the edge to loop back from the tools to the agent
    workflow.add_edge("tools", "agent")

    # 5. Compile the graph and return it
    
    # Create memory saver for conversation context
    graph = workflow.compile()
    return graph 