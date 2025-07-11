"""DBML parser service client."""

import httpx
from typing import Dict, Any, Optional
import asyncio
import logging
from src.config.settings import PARSER_SERVICE_URL, PARSER_TIMEOUT, PARSER_RETRY_ATTEMPTS

logger = logging.getLogger(__name__)


class DBMLParserClient:
    """Simple DBML parser service client for LangGraph Cloud SaaS."""
    
    def __init__(self, base_url: Optional[str] = None, timeout: Optional[int] = None):
        self.base_url = base_url or PARSER_SERVICE_URL
        self.timeout = timeout or PARSER_TIMEOUT
        self.retry_attempts = PARSER_RETRY_ATTEMPTS
    
    async def parse_dbml(self, current_dbml: str, updated_dbml: str) -> Dict[str, Any]:
        """Parse DBML schemas and return analysis result."""
        
        payload = {
            "old_dbml_string": current_dbml,
            "new_dbml_string": updated_dbml
        }
        
        for attempt in range(self.retry_attempts):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(
                        f"{self.base_url}/parse-dbml",
                        json=payload
                    )
                    response.raise_for_status()
                    
                    result = response.json()
                    logger.info(f"Successfully parsed DBML schemas (attempt {attempt + 1})")
                    return result
                    
            except httpx.HTTPError as e:
                logger.warning(f"HTTP error on attempt {attempt + 1}: {e}")
                if attempt == self.retry_attempts - 1:
                    raise
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
                
            except Exception as e:
                logger.error(f"Unexpected error on attempt {attempt + 1}: {e}")
                if attempt == self.retry_attempts - 1:
                    raise
                await asyncio.sleep(2 ** attempt)
        
        raise Exception("Failed to parse DBML after all retry attempts")


# Global client instance
_parser_client: Optional[DBMLParserClient] = None


def get_parser_client() -> DBMLParserClient:
    """Get the global parser client instance."""
    global _parser_client
    if _parser_client is None:
        _parser_client = DBMLParserClient()
    return _parser_client 