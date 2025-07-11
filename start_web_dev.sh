#!/bin/bash

# TalkingTables Web Development Setup Script
# This script sets up everything needed for web-based testing

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
VENV_NAME="venv"
PORT="8123"
PYTHON_VERSION="3.11"
BASE_URL="http://127.0.0.1:$PORT"
STUDIO_URL="https://smith.langchain.com/studio/?baseUrl=$BASE_URL"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Python version
check_python_version() {
    if command_exists python3; then
        PYTHON_VERSION_ACTUAL=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
        if [[ "$PYTHON_VERSION_ACTUAL" == "$PYTHON_VERSION"* ]]; then
            print_success "Python $PYTHON_VERSION_ACTUAL found"
            return 0
        else
            print_warning "Python $PYTHON_VERSION_ACTUAL found, but $PYTHON_VERSION is recommended"
            return 0
        fi
    else
        print_error "Python3 not found. Please install Python $PYTHON_VERSION or later."
        exit 1
    fi
}

# Function to create and activate virtual environment
setup_venv() {
    if [ ! -d "$VENV_NAME" ]; then
        print_status "Creating virtual environment..."
        python3 -m venv "$VENV_NAME"
        print_success "Virtual environment created"
    else
        print_status "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    print_status "Activating virtual environment..."
    source "$VENV_NAME/bin/activate"
    print_success "Virtual environment activated"
}

# Function to install dependencies
install_dependencies() {
    print_status "Installing dependencies..."
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install requirements
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        print_success "Requirements installed from requirements.txt"
    else
        print_error "requirements.txt not found"
        exit 1
    fi
    
    # Install development dependencies
    if [ -f "setup.py" ]; then
        pip install -e ".[dev]"
        print_success "Development dependencies installed"
    fi
    
    # Install LangGraph CLI if not already installed
    if ! command_exists langgraph; then
        print_status "Installing LangGraph CLI..."
        pip install langgraph-cli[inmem]
        print_success "LangGraph CLI installed"
    else
        print_status "LangGraph CLI already installed"
    fi
}

# Function to check environment file
check_env_file() {
    if [ ! -f ".env" ]; then
        print_warning ".env file not found"
        echo ""
        echo "📝 Create a .env file with your API keys:"
        echo ""
        echo "# OpenAI API Configuration (REQUIRED)"
        echo "OPENAI_API_KEY=YOUR-API-KEY"
        echo ""
        echo "# Parser Service Configuration"
        echo "PARSER_SERVICE_URL=http://localhost:5001"
        echo ""
        echo "# Environment Configuration"
        echo "ENVIRONMENT=development"
        echo "LOG_LEVEL=INFO"
        echo ""
        echo "# Optional: LangSmith Configuration for monitoring"
        echo "# LANGSMITH_API_KEY=your_langsmith_api_key_here (REQUIRED)"
        echo "# LANGSMITH_PROJECT=talking-tables-agent"
        echo ""
        print_warning "Please create .env file with your OpenAI API key before continuing"
        exit 1
    else
        print_success ".env file found"
    fi
}

# Function to validate configuration
validate_config() {
    print_status "Validating configuration..."
    
    # Check if langgraph.json exists
    if [ ! -f "langgraph.json" ]; then
        print_error "langgraph.json not found"
        exit 1
    fi
    
    # Check if graph file exists
    if [ ! -f "src/agent/graph.py" ]; then
        print_error "src/agent/graph.py not found"
        exit 1
    fi
    
    # Test graph structure
    print_status "Testing graph structure..."
    if python3 test_graph_structure.py >/dev/null 2>&1; then
        print_success "Graph structure validation passed"
    else
        print_warning "Graph structure validation failed, but continuing..."
    fi
    
    print_success "Configuration validated"
}

# Function to start development server
start_dev_server() {
    print_status "Starting LangGraph development server..."
    print_status "Port: $PORT"
    print_status "No browser will be opened automatically"
    
    # Create a temporary script to run langgraph dev
    cat > temp_start.sh << EOF
#!/bin/bash
source $VENV_NAME/bin/activate
langgraph dev --port $PORT --no-browser
EOF
    
    chmod +x temp_start.sh
    
    # Start the server in background
    ./temp_start.sh &
    SERVER_PID=$!
    
    # Wait a moment for server to start
    sleep 3
    
    # Check if server is running
    if curl -s "$BASE_URL/ok" >/dev/null 2>&1; then
        print_success "Development server started successfully!"
        echo ""
        echo "🎨 ${GREEN}Access your TalkingTables agent at:${NC}"
        echo "   ${BLUE}$STUDIO_URL${NC}"
        echo ""
        echo "🛑 ${YELLOW}To stop the server, press Ctrl+C${NC}"
        echo ""
        
        # Clean up temp script
        rm -f temp_start.sh
        
        # Wait for user to stop the server
        wait $SERVER_PID
    else
        print_error "Failed to start development server"
        kill $SERVER_PID 2>/dev/null || true
        rm -f temp_start.sh
        exit 1
    fi
}

# Main execution
main() {
    echo "🚀 ${GREEN}TalkingTables Web Development Setup${NC}"
    echo "================================================"
    echo ""
    
    # Check if we're in the right directory
    if [ ! -f "src/agent/graph.py" ]; then
        print_error "Please run this script from the TalkingTables_V1 directory"
        exit 1
    fi
    
    # Step 1: Check Python version
    check_python_version
    
    # Step 2: Check environment file
    check_env_file
    
    # Step 3: Setup virtual environment
    setup_venv
    
    # Step 4: Install dependencies
    install_dependencies
    
    # Step 5: Validate configuration
    validate_config
    
    # Step 6: Start development server
    start_dev_server
}

# Handle script interruption
trap 'echo ""; print_warning "Shutting down..."; exit 0' INT TERM

# Run main function
main "$@" 