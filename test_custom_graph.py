#!/usr/bin/env python3
"""Test script for the custom StateGraph migration."""

import os
import sys
from langchain_core.messages import HumanMessage
from src.agent.graph import create_graph
from src.models.state import TalkingTablesState

def test_custom_graph():
    """Test the custom StateGraph implementation."""
    
    # Set up environment
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY environment variable not set")
        print("💡 Set OPENAI_API_KEY to test full LLM execution")
        return False
    
    try:
        # Create the graph
        print("🔧 Creating custom StateGraph...")
        graph = create_graph()
        print("✅ Graph created successfully")
        
        # Create initial state
        initial_state = TalkingTablesState(
            messages=[HumanMessage(content="Hello! Can you help me create a simple user management database schema?")]
        )
        
        print("🧪 Testing graph execution...")
        
        # Execute the graph
        result = graph.invoke(initial_state)
        
        print("✅ Graph execution completed successfully")
        print(f"📊 Final state keys: {list(result.keys())}")
        print(f"💬 Number of messages: {len(result['messages'])}")
        
        # Check if we have the expected state fields
        expected_fields = ['messages', 'current_dbml', 'updated_dbml', 'dbml_json', 'diff_json']
        for field in expected_fields:
            if field in result:
                print(f"✅ {field}: {type(result[field])}")
            else:
                print(f"❌ Missing field: {field}")
        
        # Test state defaults
        print("🔧 Testing state defaults...")
        if result['updated_dbml'] == "":  # Should be empty string, not None
            print("✅ updated_dbml defaults to empty string")
        else:
            print(f"⚠️  updated_dbml is: {result['updated_dbml']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing custom graph: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Testing TalkingTables Custom StateGraph Migration")
    print("=" * 50)
    
    success = test_custom_graph()
    
    if success:
        print("\n🎉 Migration test completed successfully!")
        print("✅ Custom StateGraph is working correctly")
        print("💡 For structure-only testing, run: python3 test_graph_structure.py")
    else:
        print("\n💥 Migration test failed!")
        print("💡 Make sure OPENAI_API_KEY is set for full testing")
        sys.exit(1) 