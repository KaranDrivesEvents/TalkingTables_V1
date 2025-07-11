#!/usr/bin/env python3
"""Test script for the custom StateGraph structure (no API key required)."""

import sys
from src.agent.graph import create_graph
from src.models.state import TalkingTablesState

def test_graph_structure():
    """Test the custom StateGraph structure without execution."""
    
    try:
        # Test imports
        print("🔧 Testing imports...")
        from src.agent.nodes import agent_node, tool_node, tools
        from src.agent.routing import should_continue
        print("✅ All imports successful")
        
        # Test tool list
        print(f"🔧 Tools available: {len(tools)}")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
        
        # Test state model
        print("🔧 Testing state model...")
        state = TalkingTablesState(
            messages=[],
            current_dbml="",
            updated_dbml=None,
            dbml_json=None,
            diff_json=None
        )
        print("✅ State model works correctly")
        
        # Test graph creation (without execution)
        print("🔧 Testing graph creation...")
        graph = create_graph()
        print("✅ Graph created successfully")
        
        # Test graph structure
        print("🔧 Testing graph structure...")
        nodes = list(graph.nodes.keys())
        print(f"  - Nodes: {nodes}")
        
        if "agent" in nodes and "tools" in nodes:
            print("✅ Graph has required nodes")
        else:
            print("❌ Graph missing required nodes")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing graph structure: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Testing TalkingTables Custom StateGraph Structure")
    print("=" * 50)
    
    success = test_graph_structure()
    
    if success:
        print("\n🎉 Structure test completed successfully!")
        print("✅ Custom StateGraph structure is correct")
    else:
        print("\n💥 Structure test failed!")
        sys.exit(1) 