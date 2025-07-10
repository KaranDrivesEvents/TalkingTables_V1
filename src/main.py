"""Main entry point for the Talking Tables ReAct agent."""

import logging
import sys
from typing import Dict, Any
from dotenv import load_dotenv

from .agent.react_agent import create_talking_tables_agent
from .config.settings import get_settings
from .services.parser_client import health_check


def setup_logging() -> None:
    """Setup logging configuration."""
    settings = get_settings()
    
    logging.basicConfig(
        level=getattr(logging, settings.deployment.log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )


def main() -> None:
    """Main function for running the ReAct agent locally."""
    # Load environment variables
    load_dotenv()
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Get settings and validate configuration
        settings = get_settings()
        logger.info(f"Starting Talking Tables ReAct agent in {settings.deployment.environment} mode")
        
        # Check parser service health
        if not health_check():
            logger.warning("Parser service health check failed - some functionality may be limited")
        else:
            logger.info("Parser service is healthy")
        
        # Create the ReAct agent
        agent = create_talking_tables_agent()
        logger.info("ReAct agent created successfully")
        
        # Configuration for memory persistence - use consistent thread ID
        config = {"configurable": {"thread_id": "talking-tables-session"}}
        
        # Interactive mode for local testing
        print("\n🗣️ Talking Tables ReAct Agent - Interactive Mode")
        print("Type 'quit' or 'exit' to stop")
        print("Type 'help' for available commands\n")
        
        while True:
            try:
                user_input = input("> ").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() in ['quit', 'exit']:
                    print("Goodbye! 👋")
                    break
                    
                if user_input.lower() == 'help':
                    print_help()
                    continue
                
                # Process the user message through the ReAct agent with memory
                # Only pass the new message - the agent will maintain full conversation history
                result = agent.invoke(
                    {"messages": [("user", user_input)]}, 
                    config
                )
                
                # Display the result - LangGraph returns AddableValuesDict with messages key
                if "messages" in result and result["messages"]:
                    last_message = result["messages"][-1]
                    print(f"\n💬 {last_message.content}")
                else:
                    print(f"\n📄 {result}")
                
                print()  # Add spacing
                    
            except KeyboardInterrupt:
                print("\n\nGoodbye! 👋")
                break
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                print(f"\n❌ Error: {e}\n")
                
    except Exception as e:
        logger.error(f"Failed to start ReAct agent: {e}")
        sys.exit(1)


def print_help() -> None:
    """Print help information."""
    help_text = """
Available Commands:
- help: Show this help message
- quit/exit: Exit the agent

Example Interactions:

Schema Modification:
> Add a users table with email and name fields
> Remove the email field from users table
> Add a posts table that references users

Schema Analysis:
> What's the best way to model user authentication?
> How should I structure tables for a blog system?
> What relationships should I consider between users and posts?

The ReAct agent will automatically determine the appropriate actions based on your input.
    """
    print(help_text)


if __name__ == "__main__":
    main() 