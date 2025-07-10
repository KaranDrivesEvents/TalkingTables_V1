"""HTTP client for the DBML parser service."""

import httpx
from typing import Dict, Any, Optional
import logging
from ..config.settings import get_settings

logger = logging.getLogger(__name__)


class ParserServiceError(Exception):
    """Exception raised when parser service encounters an error."""
    pass


def make_parser_request(current_dbml: str, updated_dbml: str) -> Dict[str, Any]:
    """Make HTTP request to parser service with current_dbml and updated_dbml.
    
    Args:
        current_dbml (str): The existing DBML schema string
        updated_dbml (str): The proposed DBML schema string to validate
        
    Returns:
        Dict[str, Any]: Parser response containing validation results, errors, or schema_json/diff_json
        
    Raises:
        ParserServiceError: If the parser service is unreachable or returns an error
    """
    settings = get_settings()
    
    # Use the correct request format for the actual parser service
    payload = {
        "old_dbml_string": current_dbml,
        "new_dbml_string": updated_dbml
    }
    
    # Retry logic with exponential backoff
    for attempt in range(settings.parser_service.retry_attempts):
        try:
            with httpx.Client(timeout=settings.parser_service.timeout) as client:
                # Use the correct endpoint /parse-dbml
                response = client.post(
                    f"{settings.parser_service.base_url}/parse-dbml",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"Parser service request successful on attempt {attempt + 1}")
                    return result
                
                elif response.status_code == 400:
                    # Bad request - likely a validation error, return as-is
                    result = response.json()
                    logger.warning(f"Parser service validation error: {result}")
                    return result
                
                else:
                    logger.warning(f"Parser service returned status {response.status_code} on attempt {attempt + 1}")
                    if attempt == settings.parser_service.retry_attempts - 1:
                        raise ParserServiceError(
                            f"Parser service returned status {response.status_code}: {response.text}"
                        )
                    
        except httpx.TimeoutException:
            logger.warning(f"Parser service timeout on attempt {attempt + 1}")
            if attempt == settings.parser_service.retry_attempts - 1:
                raise ParserServiceError("Parser service timeout after multiple attempts")
                
        except httpx.ConnectError:
            logger.warning(f"Failed to connect to parser service on attempt {attempt + 1}")
            if attempt == settings.parser_service.retry_attempts - 1:
                raise ParserServiceError("Unable to connect to parser service")
                
        except Exception as e:
            logger.error(f"Unexpected error calling parser service on attempt {attempt + 1}: {e}")
            if attempt == settings.parser_service.retry_attempts - 1:
                raise ParserServiceError(f"Unexpected error: {e}")
    
    # This should never be reached due to the raise statements above, but just in case
    raise ParserServiceError("All parser service attempts failed")


def health_check() -> bool:
    """Check if the parser service is healthy and reachable.
    
    Returns:
        bool: True if the service is healthy, False otherwise
    """
    settings = get_settings()
    
    try:
        with httpx.Client(timeout=5.0) as client:
            # Use the root endpoint since /health doesn't exist
            response = client.get(f"{settings.parser_service.base_url}/")
            if response.status_code == 200:
                result = response.json()
                # Check if response contains expected status
                return result.get("status") == "ok"
            return False
    except Exception as e:
        logger.warning(f"Parser service health check failed: {e}")
        return False 