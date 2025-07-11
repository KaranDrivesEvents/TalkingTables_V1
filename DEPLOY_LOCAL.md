# TalkingTables LangGraph Deployment & Test Guide

## 🚀 Quick Deploy

### Configuration

The agent is highly configurable through environment variables:

```bash
# Required
OPENAI_API_KEY=your_openai_api_key

# Optional
PARSER_SERVICE_URL=http://localhost:5001
LLM_MODEL=gpt-4
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=4000
```

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- OpenAI API key
- Optional: DBML parser service (for full validation)

### Quick Start
```bash
# 1. Set up environment
cp .env.example .env
# Edit .env and add your OpenAI API key

# 2. Start development server
./start_web_dev.sh

# 3. Access the agent via the provided Studio URL
```

## 💬 Example Interactions

### Creating a New Schema
```
User: "I need a database for an e-commerce store with users, products, and orders"

Agent: [Analyzes requirements and creates DBML schema]
- Creates users table with authentication fields
- Creates products table with inventory tracking
- Creates orders table with relationships
- Validates schema and provides JSON representation
```

### Modifying Existing Schema
```
User: "Add a reviews table to my existing schema"

Agent: [Reads current schema, adds reviews table, validates changes]
- Retrieves current DBML schema
- Adds reviews table with proper relationships
- Validates complete updated schema
- Shows differences and confirms success
```

### Schema Analysis
```
User: "What are the potential issues with my current database design?"

Agent: [Analyzes schema and provides recommendations]
- Reviews current structure
- Identifies normalization opportunities
- Suggests index improvements
- Recommends relationship optimizations
```

### Studio Connection Issues
If LangGraph Studio fails to connect:
1. Try the direct Studio URL provided by the script
2. Open in incognito/private browsing mode
3. Check browser console for CORS errors
4. Ensure no firewall is blocking port 8123

### Logs
- Check LangGraph Cloud logs in the dashboard
- Local logs: `*.log` files (ignored by git)

## 📚 Resources
- [LangGraph Cloud Documentation](https://langchain-ai.github.io/langgraph/)
- [Custom StateGraph Guide](https://langchain-ai.github.io/langgraph/tutorials/state_graph/)
- [Deployment Best Practices](https://langchain-ai.github.io/langgraph/how-tos/deploy/)
- [Studio Troubleshooting](https://aka.ms/vscode-troubleshoot-terminal-launch) 