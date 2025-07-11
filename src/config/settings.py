"""Simple configuration for LangGraph Cloud SaaS deployment."""

import os
from typing import Optional


# Simple environment variable configuration
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
PARSER_SERVICE_URL: str = os.getenv("PARSER_SERVICE_URL", "http://localhost:5001")

# Optional LangSmith configuration
LANGSMITH_API_KEY: Optional[str] = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_PROJECT: str = os.getenv("LANGSMITH_PROJECT", "talking-tables-agent")

# LLM Configuration (with sensible defaults)
LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4")
LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.1"))
LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "4000"))

# Parser service configuration
PARSER_TIMEOUT: int = int(os.getenv("PARSER_TIMEOUT", "30"))
PARSER_RETRY_ATTEMPTS: int = int(os.getenv("PARSER_RETRY_ATTEMPTS", "3")) 