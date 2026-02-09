from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from app.models import NewsQueryParams, NewsResponse
from app.services.newdata_service import newdata_service

router = APIRouter(prefix="/api", tags=["news"])


@router.get("/news", response_model=NewsResponse)
async def get_news(
    query: Optional[str] = Query(None, description="Search query term"),
    category: Optional[str] = Query(None, description="News category"),
    country: Optional[str] = Query(None, description="Country code"),
    language: Optional[str] = Query("en", description="Language code"),
    limit: int = Query(10, ge=1, le=100, description="Number of results")
):
    """
    Fetch news articles with optional filters.
    
    - **query**: Search term for news articles
    - **category**: Filter by category (e.g., business, technology, sports)
    - **country**: Filter by country code (e.g., us, uk, in)
    - **language**: Language code (default: en)
    - **limit**: Maximum number of results to return (1-100)
    """
    params = {
        "query": query,
        "category": category,
        "country": country,
        "language": language,
        "limit": limit
    }
    
    result = await newdata_service.fetch_news(params)
    
    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error"))
    
    return result


@router.get("/headlines", response_model=NewsResponse)
async def get_headlines(
    category: Optional[str] = Query(None, description="News category"),
    country: Optional[str] = Query("us", description="Country code"),
    limit: int = Query(10, ge=1, le=100, description="Number of results")
):
    """
    Fetch top headlines.
    
    - **category**: Filter by category
    - **country**: Country code (default: us)
    - **limit**: Maximum number of results to return (1-100)
    """
    params = {
        "category": category,
        "country": country,
        "limit": limit
    }
    
    result = await newdata_service.fetch_headlines(params)
    
    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error"))
    
    return result


@router.get("/search/{topic}", response_model=NewsResponse)
async def search_by_topic(
    topic: str,
    country: Optional[str] = Query(None, description="Country code"),
    language: Optional[str] = Query("en", description="Language code"),
    limit: int = Query(10, ge=1, le=100, description="Number of results")
):
    """
    Search news by topic.
    
    - **topic**: Topic to search for (path parameter)
    - **country**: Filter by country code
    - **language**: Language code (default: en)
    - **limit**: Maximum number of results to return (1-100)
    """
    options = {
        "country": country,
        "language": language,
        "limit": limit
    }
    
    result = await newdata_service.search_by_topic(topic, options)
    
    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error"))
    
    return result


@router.post("/news/query", response_model=NewsResponse)
async def query_news(params: NewsQueryParams):
    """
    Fetch news with complex query in request body.
    
    Accepts a JSON body with the following fields:
    - **query**: Search term
    - **category**: News category
    - **country**: Country code
    - **language**: Language code
    - **limit**: Number of results
    """
    params_dict = params.model_dump()
    
    result = await newdata_service.fetch_news(params_dict)
    
    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error"))
    
    return result