# TalkingTables Agent

A sophisticated database schema assistant powered by LangGraph and LangChain that helps users design, modify, and analyze database schemas using DBML (Database Markup Language). With interactive schema in the UI-canvas.  

## 🤖 What is TalkingTables?

TalkingTables is an AI-powered database schema assistant that understands natural language requests and helps you create, modify, and analyze database schemas. It uses DBML (Database Markup Language) as its schema representation and provides intelligent recommendations, validation, and visualization capabilities.

### Key Features

- **Natural Language Processing**: Ask questions about your database design in plain English
- **DBML Schema Management**: Create and modify database schemas using DBML syntax
- **Intelligent Validation**: Automatic parsing and validation of schema changes
- **Visual Schema Analysis**: Get JSON representations for UI rendering
- **Change Tracking**: Compare current and updated schemas to see differences
- **Best Practices Guidance**: Receive recommendations for optimal database design

## 🏗️ Architecture

TalkingTables uses a custom **StateGraph** architecture built with LangGraph, providing:

### Core Components

1. **Agent Node** (`agent_node`): The "brain" that processes user input and decides actions
2. **Tool Node** (`tool_node`): The "hands" that execute specific operations
3. **State Management**: Pydantic-based state tracking with message history
4. **Routing Logic**: Conditional flow control between agent and tools

### State Management

The agent maintains conversation state using a Pydantic model (`TalkingTablesState`) that tracks:

- **Messages**: Complete conversation history
- **Current DBML**: The active database schema
- **Updated DBML**: Pending schema changes
- **Schema JSON**: Parsed schema for UI rendering
- **Diff JSON**: Changes between schema versions

## 🛠️ Available Tools

### 1. `read_current_dbml`
Retrieves the current database schema from state. Used to understand existing structure before making changes.

### 2. `read_updated_dbml`
Internal tool for accessing previously failed schema attempts for comparison and debugging.

### 3. `call_dbml_parser`
The core validation tool that:
- Parses DBML schemas for syntax validation
- Compares current vs updated schemas
- Generates JSON representations for UI rendering
- Tracks schema differences
- Updates the conversation state with results

## 🎯 Interaction Modes

### Analytical Mode
For exploratory questions and schema analysis:
1. Retrieves current schema
2. Analyzes structure and relationships
3. Provides detailed recommendations
4. Presents DBML code blocks when relevant
5. Offers numbered suggestions for clarity

### Directive Mode
For direct schema modification commands:
1. **Always** starts by reading current schema
2. Analyzes existing structure
3. Creates updated DBML with requested changes
4. **Immediately** validates changes via parser
5. Celebrates success or helps fix validation errors

## 🔧 Technical Implementation

### Technology Stack
- **LangGraph**: Custom StateGraph for workflow management
- **LangChain**: LLM integration and tool orchestration
- **OpenAI GPT-4**: Natural language understanding and generation
- **Pydantic**: Type-safe state management
- **DBML**: Database schema representation
- **HTTPX**: Async HTTP client for parser service integration

### Key Design Patterns

1. **StateGraph Architecture**: Modular, debuggable workflow with clear separation of concerns
2. **Tool-Based Execution**: LLM decides which tools to use based on user intent
3. **Conditional Routing**: Smart flow control between agent reasoning and tool execution
4. **Async Parser Integration**: External DBML parsing service for validation
5. **Streaming Responses**: Real-time interaction with streaming enabled

## 🎨 UI Integration

The agent provides structured outputs for UI rendering:

- **Schema JSON**: Parsed database structure for visualization
- **Diff JSON**: Change tracking for highlighting modifications
- **Validation Results**: Success/error messages with detailed feedback

## 🔄 Workflow Flow

1. **User Input**: Natural language request or command
2. **Agent Processing**: LLM analyzes intent and decides action
3. **Tool Execution**: Appropriate tools are called based on decision
4. **State Update**: Results update conversation state
5. **Response Generation**: Agent provides user-friendly response
6. **Loop**: Process continues until user request is satisfied

## 🌟 Key Benefits

- **Intelligent Schema Design**: AI-powered recommendations for optimal database structure
- **Natural Language Interface**: No need to learn complex syntax
- **Validation & Safety**: Automatic parsing and error detection
- **Version Control**: Track schema changes and differences
- **Extensible Architecture**: Easy to add new tools and capabilities
- **Production Ready**: Built for LangGraph Cloud deployment

TalkingTables transforms database schema design from a technical chore into an intelligent, conversational experience, making database design accessible to everyone while maintaining professional-grade quality and validation. 