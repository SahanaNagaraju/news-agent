import httpx
from typing import Dict, Any, Optional, List
from datetime import datetime
from app.config import settings


class SerpAPIService:
    """Service for interacting with SerpAPI."""
    
    def __init__(self):
        self.api_url = settings.serpapi_api_url
        self.api_key = settings.serpapi_api_key
        self.timeout = 30.0
        
    def _get_headers(self) -> Dict[str, str]:
        """Get HTTP headers for API requests."""
        return {
            "Content-Type": "application/json"
        }
    
    def _combine_results(self, results: List[Dict[str, Any]]) -> str:
        """
        Combine questions and snippets from search results into a comprehensive response.
        
        Args:
            results: List of search results containing 'question' and 'snippet'
            
        Returns:
            Combined comprehensive response string
        """
        if not results:
            return "No results found for your query."
        
        combined_text = []
        
        for idx, result in enumerate(results, 1):
            question = result.get('question', '')
            snippet = result.get('snippet', '')
            
            if question or snippet:
                section = f"**Result {idx}:**\n"
                if question:
                    section += f"Question: {question}\n"
                if snippet:
                    section += f"Answer: {snippet}\n"
                combined_text.append(section)
        
        if not combined_text:
            return "No relevant information found in the search results."
        
        # Join all sections with a separator
        comprehensive_response = "\n---\n\n".join(combined_text)
        
        # Add a summary header
        summary = f"**Comprehensive Search Results ({len(results)} results found)**\n\n"
        
        return summary + comprehensive_response
    
    async def search(self, query: str, limit: int = 5) -> Dict[str, Any]:
        """
        Search using SerpAPI and return combined results.
        
        Args:
            query: Search query string
            limit: Number of results to return (default: 5)
            
        Returns:
            Dictionary containing success status and comprehensive response
        """
        try:
            query_params = {
                "q": query,
                "api_key": self.api_key,
                "num": limit  # SerpAPI uses 'num' parameter for result count
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    self.api_url,
                    params=query_params,
                    headers=self._get_headers()
                )
                response.raise_for_status()
                
                data = response.json()
                
                # Extract results (SerpAPI may return results in different formats)
                # Check for 'organic_results', 'related_questions', or direct results
                results = []
                
                # Try to get related_questions which often have question/snippet format
                if 'related_questions' in data:
                    results = data['related_questions'][:limit]
                # Try organic_results as fallback
                elif 'organic_results' in data:
                    organic = data['organic_results'][:limit]
                    # Transform organic results to question/snippet format
                    results = [
                        {
                            'question': item.get('title', ''),
                            'snippet': item.get('snippet', '')
                        }
                        for item in organic
                    ]
                # Use the raw data if it already has the expected format
                else:
                    # Assume the data might be in the format you described
                    results = data if isinstance(data, list) else []
                
                # Generate comprehensive response
                comprehensive_response = self._combine_results(results)
                
                return {
                    "success": True,
                    "data": {
                        "query": query,
                        "results_count": len(results),
                        "comprehensive_response": comprehensive_response,
                        "raw_results": results,
                        "full_data": data  # Include full API response for debugging
                    },
                    "timestamp": datetime.utcnow().isoformat()
                }
                
        except httpx.HTTPStatusError as e:
            return self._handle_error(e, "HTTP error")
        except httpx.RequestError as e:
            return self._handle_error(e, "Request error")
        except Exception as e:
            return self._handle_error(e, "Unexpected error")
    
    async def fetch_news(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fetch news using search query.
        Maintained for backward compatibility with existing endpoints.
        
        Args:
            params: Query parameters including query, limit
            
        Returns:
            Dictionary containing success status and comprehensive response
        """
        query = params.get("query", "")
        limit = params.get("limit", 5)
        
        # Build a more specific query if additional filters are provided
        if params.get("category"):
            query = f"{query} {params['category']}" if query else params['category']
        if params.get("country"):
            query = f"{query} {params['country']}" if query else params['country']
        
        return await self.search(query, limit)
    
    async def fetch_headlines(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fetch top headlines using search.
        
        Args:
            params: Query parameters including category, country, limit
            
        Returns:
            Dictionary containing success status and comprehensive response
        """
        query = "latest news"
        if params.get("category"):
            query = f"latest {params['category']} news"
        if params.get("country"):
            query = f"{query} {params['country']}"
            
        limit = params.get("limit", 5)
        return await self.search(query, limit)
    
    async def search_by_topic(self, topic: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """
        Search news by topic.
        
        Args:
            topic: Topic to search for
            options: Additional query options
            
        Returns:
            Dictionary containing success status and comprehensive response
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
        Check health of SerpAPI service.
        
        Returns:
            Dictionary containing health status
        """
        try:
            # Simple test search
            result = await self.search("test", limit=1)
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
                    "message": "No response from SerpAPI",
                    "details": "The request was made but no response was received"
                }
            }
        else:
            return {
                "success": False,
                "error": {
                    "message": f"Failed to fetch data: {error_type}",
                    "details": str(error)
                }
            }


# Global service instance
serpapi_service = SerpAPIService()