"""Configuration management for the Talking Tables agent."""

from typing import Optional
from pydantic import Field, BaseModel
from pydantic_settings import BaseSettings
import toml
from pathlib import Path


class LLMSettings(BaseModel):
    """LLM configuration settings."""
    model_name: str = Field(default="gpt-4")
    temperature: float = Field(default=0.1)
    max_tokens: int = Field(default=4000)
    api_key: Optional[str] = Field(default=None)


class ParserServiceSettings(BaseModel):
    """Parser service configuration."""
    base_url: str = Field(default="http://localhost:5001")
    timeout: int = Field(default=30)
    retry_attempts: int = Field(default=3)


class Settings(BaseSettings):
    """Main settings class that combines all configuration sections."""
    
    # API Keys
    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")
    langsmith_api_key: Optional[str] = Field(default=None, alias="LANGSMITH_API_KEY")
    langsmith_project: Optional[str] = Field(default="talking-tables-agent", alias="LANGSMITH_PROJECT")
    langgraph_cloud_api_key: Optional[str] = Field(default=None, alias="LANGGRAPH_CLOUD_API_KEY")
    
    # Parser service settings (flattened)
    parser_service_url: str = Field(default="http://localhost:5001", alias="PARSER_SERVICE_URL")
    
    # Environment settings
    environment: str = Field(default="development", alias="ENVIRONMENT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._load_config()
        
    @property
    def llm(self) -> LLMSettings:
        """Get LLM settings with API key injected."""
        return self._llm_settings
        
    @property 
    def parser_service(self) -> ParserServiceSettings:
        """Get parser service settings."""
        return self._parser_service_settings
    
    @property
    def deployment(self):
        """Get deployment settings (compatibility layer)."""
        class DeploymentCompat:
            def __init__(self, environment: str, log_level: str):
                self.environment = environment
                self.log_level = log_level
        
        return DeploymentCompat(self.environment, self.log_level)

    def _load_config(self):
        """Load configuration from config.toml file if it exists."""
        config_path = Path("config.toml")
        
        # Start with defaults
        llm_config = {
            "model_name": "gpt-4",
            "temperature": 0.1,
            "max_tokens": 4000,
            "api_key": self.openai_api_key
        }
        
        parser_config = {
            "base_url": self.parser_service_url,
            "timeout": 30,
            "retry_attempts": 3
        }
        
        # Override with TOML config if available
        if config_path.exists():
            try:
                config_data = toml.load(config_path)
                
                # Update LLM config (keeping backward compatibility with "agent" section)
                if "llm" in config_data:
                    llm_config.update(config_data["llm"])
                elif "agent" in config_data:
                    # Backward compatibility: map agent.model to llm.model_name
                    agent_data = config_data["agent"]
                    if "model" in agent_data:
                        llm_config["model_name"] = agent_data["model"]
                    if "temperature" in agent_data:
                        llm_config["temperature"] = agent_data["temperature"]
                    if "max_tokens" in agent_data:
                        llm_config["max_tokens"] = agent_data["max_tokens"]
                
                if "parser_service" in config_data:
                    parser_config.update(config_data["parser_service"])
                            
            except Exception as e:
                # Log warning but don't fail
                print(f"Warning: Could not load config.toml: {e}")
        
        # Create the nested settings objects
        self._llm_settings = LLMSettings(**llm_config)
        self._parser_service_settings = ParserServiceSettings(**parser_config)


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get the global settings instance, creating it if necessary."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reset_settings() -> None:
    """Reset the global settings instance (useful for testing)."""
    global _settings
    _settings = None 