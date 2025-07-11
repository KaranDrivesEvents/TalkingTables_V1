"""Setup script for TalkingTables LangGraph application."""

from setuptools import setup, find_packages

setup(
    name="talking-tables-agent",
    version="1.0.0",
    description="TalkingTables DBML Schema Agent",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "langgraph>=0.5.0",
        "langchain-openai>=0.3.0",
        "langchain-core>=0.3.0",
        "httpx>=0.25.0",
        "pydantic>=2.6.0",
        "pydantic-settings>=2.10.1",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "langgraph-cli[inmem]",
        ]
    },
) 