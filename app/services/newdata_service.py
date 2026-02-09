import httpx
from typing import Dict, Any, Optional
from datetime import datetime
from app.config import settings


class NewdataService:
    """Service for interacting with newdata.io API."""
    
    def __init__(self):
        self.api_url = settings.newdata_api_url
        self.api_key = settings.newdata_api_key
        self.timeout = 30.0
        
    def _get_headers(self) -> Dict[str, str]:
        """Get HTTP headers for API requests."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def fetch_news(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fetch news articles from newdata.io.
        
        Args:
            params: Query parameters including query, category, country, language, limit
            
        Returns:
            Dictionary containing success status and data or error
        """
        try:
            query_params = {
                "q": params.get("query", ""),
                "category": params.get("category", ""),
                "country": params.get("country", ""),
                "language": params.get("language", "en"),
                "limit": params.get("limit", 10)
            }
            
            # Remove empty parameters
            query_params = {k: v for k, v in query_params.items() if v}
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.api_url}/news",
                    params=query_params,
                    headers=self._get_headers()
                )
                response.raise_for_status()
                
                return {
                    "success": True,
                    "data": response.json(),
                    "timestamp": datetime.utcnow().isoformat()
                }
                
        except httpx.HTTPStatusError as e:
            return self._handle_error(e, "HTTP error")
        except httpx.RequestError as e:
            return self._handle_error(e, "Request error")
        except Exception as e:
            return self._handle_error(e, "Unexpected error")
    
    async def fetch_headlines(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fetch top headlines from newdata.io.
        
        Args:
            params: Query parameters including category, country, limit
            
        Returns:
            Dictionary containing success status and data or error
        """
        try:
            query_params = {
                "category": params.get("category", ""),
                "country": params.get("country", "us"),
                "limit": params.get("limit", 10)
            }
            
            # Remove empty parameters
            query_params = {k: v for k, v in query_params.items() if v}
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.api_url}/headlines",
                    params=query_params,
                    headers=self._get_headers()
                )
                response.raise_for_status()
                
                return {
                    "success": True,
                    "data": response.json(),
                    "timestamp": datetime.utcnow().isoformat()
                }
                
        except httpx.HTTPStatusError as e:
            return self._handle_error(e, "HTTP error")
        except httpx.RequestError as e:
            return self._handle_error(e, "Request error")
        except Exception as e:
            return self._handle_error(e, "Unexpected error")
    
    async def search_by_topic(self, topic: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """
        Search news by topic.
        
        Args:
            topic: Topic to search for
            options: Additional query options
            
        Returns:
            Dictionary containing success status and data or error
        """
        try:
            params = {
                "query": topic,
                **options
            }
            return await self.fetch_news(params)
            
        except Exception as e:
            return self._handle_error(e, "Search error")
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Check health of newdata.io service.
        
        Returns:
            Dictionary containing health status
        """
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(
                    f"{self.api_url}/health",
                    headers=self._get_headers()
                )
                return {
                    "success": True,
                    "status": "healthy",
                    "timestamp": datetime.utcnow().isoformat()
                }
        except Exception as e:
            return {
                "success": False,
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _handle_error(self, error: Exception, error_type: str) -> Dict[str, Any]:
        """
        Handle and format errors.
        
        Args:
            error: Exception that occurred
            error_type: Type of error
            
        Returns:
            Dictionary containing error information
        """
        if isinstance(error, httpx.HTTPStatusError):
            return {
                "success": False,
                "error": {
                    "message": f"API request failed: {error_type}",
                    "status": error.response.status_code,
                    "details": str(error)
                }
            }
        elif isinstance(error, httpx.RequestError):
            return {
                "success": False,
                "error": {
                    "message": "No response from newdata.io API",
                    "details": "The request was made but no response was received"
                }
            }
        else:
            return {
                "success": False,
                "error": {
                    "message": f"Failed to fetch news data: {error_type}",
                    "details": str(error)
                }
            }


# Global service instance
newdata_service = NewdataService()