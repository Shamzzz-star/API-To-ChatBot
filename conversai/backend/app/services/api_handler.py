"""
API Request Handler - Sends requests to external APIs with caching and error handling
"""
import httpx
from typing import Dict, Any, Optional
from cachetools import TTLCache
import hashlib
import json
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


class APIRequestHandler:
    """Handle API requests with retry logic, caching, and error handling"""
    
    def __init__(self):
        # In-memory cache (alternative to Redis for simplicity)
        # Format: {cache_key: response_data}
        self.cache = TTLCache(maxsize=1000, ttl=300)  # 1000 items, 5 min default TTL
        
        # Cache TTL by category
        self.cache_ttls = {
            "weather": settings.CACHE_TTL_WEATHER,
            "cryptocurrency": settings.CACHE_TTL_CRYPTO,
            "news": settings.CACHE_TTL_NEWS,
            "default": settings.CACHE_TTL_DEFAULT
        }
    
    async def send_request(
        self, 
        request_config: Dict[str, Any],
        category: str = "default",
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Send an HTTP request to an API
        
        Args:
            request_config: Request configuration (url, method, headers, params)
            category: API category for cache TTL
            use_cache: Whether to use caching
        
        Returns:
            API response data or error dict
        """
        # Generate cache key
        cache_key = self._generate_cache_key(request_config)
        
        # Check cache
        if use_cache and cache_key in self.cache:
            logger.info(f"Cache hit for: {cache_key[:20]}...")
            cached_data = self.cache[cache_key]
            cached_data["_cached"] = True
            return cached_data
        
        # Send request
        try:
            response_data = await self._make_request(request_config)
            
            # Wrap list responses in a dictionary for consistency
            if isinstance(response_data, list):
                response_data = {"data": response_data, "_cached": False}
            else:
                response_data["_cached"] = False
            
            # Cache successful response
            if use_cache and "error" not in response_data:
                ttl = self.cache_ttls.get(category, self.cache_ttls["default"])
                # Create a new cache with specific TTL for this entry
                self.cache[cache_key] = response_data
            
            return response_data
            
        except Exception as e:
            logger.error(f"API request error: {e}", exc_info=True)
            return {
                "error": str(e),
                "status": "failed",
                "_cached": False
            }
    
    async def _make_request(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Make the actual HTTP request"""
        url = config.get("url")
        method = config.get("method", "GET").upper()
        headers = config.get("headers", {})
        params = config.get("params", {})
        data = config.get("data", {})
        
        # Set timeout
        timeout = httpx.Timeout(10.0, connect=5.0)
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                if method == "GET":
                    response = await client.get(url, headers=headers, params=params)
                elif method == "POST":
                    response = await client.post(url, headers=headers, params=params, json=data)
                elif method == "PUT":
                    response = await client.put(url, headers=headers, params=params, json=data)
                elif method == "DELETE":
                    response = await client.delete(url, headers=headers, params=params)
                else:
                    return {"error": f"Unsupported HTTP method: {method}"}
                
                # Handle response
                if response.status_code == 200:
                    try:
                        json_data = response.json()
                        logger.info(f"API response received (status 200): {type(json_data)}")
                        logger.debug(f"API response data: {json.dumps(json_data, indent=2, default=str)[:500]}")
                        return json_data
                    except json.JSONDecodeError:
                        logger.warning(f"JSON decode error, returning text response")
                        return {"data": response.text}
                else:
                    error_msg = self._get_error_message(response.status_code)
                    return {
                        "error": error_msg,
                        "status_code": response.status_code,
                        "detail": response.text[:200]
                    }
                    
            except httpx.TimeoutException:
                return {"error": "Request timed out", "status": "timeout"}
            except httpx.ConnectError:
                return {"error": "Could not connect to API", "status": "connection_error"}
            except Exception as e:
                return {"error": f"Request failed: {str(e)}", "status": "error"}
    
    def _generate_cache_key(self, config: Dict[str, Any]) -> str:
        """Generate a unique cache key for a request"""
        # Create a string representation of the request
        key_parts = [
            config.get("url", ""),
            config.get("method", "GET"),
            json.dumps(config.get("params", {}), sort_keys=True),
            json.dumps(config.get("data", {}), sort_keys=True)
        ]
        
        key_string = "|".join(key_parts)
        
        # Hash it for shorter key
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _get_error_message(self, status_code: int) -> str:
        """Get user-friendly error message for HTTP status code"""
        error_messages = {
            400: "Invalid parameters sent to API",
            401: "API authentication failed. Please check your API key.",
            403: "Access forbidden. You may not have permission to access this resource.",
            404: "Resource not found. Please check your input.",
            429: "Rate limit exceeded. Please try again in a few moments.",
            500: "API server error. Please try again later.",
            502: "Bad gateway. The API server is having issues.",
            503: "API temporarily unavailable. Please try again later.",
            504: "Gateway timeout. The API took too long to respond."
        }
        
        return error_messages.get(status_code, f"API returned status code: {status_code}")
    
    def clear_cache(self):
        """Clear all cached data"""
        self.cache.clear()
        logger.info("Cache cleared")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            "size": len(self.cache),
            "max_size": self.cache.maxsize,
            "ttl": self.cache.ttl
        }


# Global request handler instance
request_handler = APIRequestHandler()
