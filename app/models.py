from pydantic import BaseModel, Field
from typing import Optional, Any, Dict, List
from datetime import datetime


class NewsQueryParams(BaseModel):
    """Query parameters for news fetching."""
    query: Optional[str] = Field(None, description="Search query term")
    category: Optional[str] = Field(None, description="News category (e.g., business, technology, sports)")
    country: Optional[str] = Field(None, description="Country code (e.g., us, uk, in)")
    language: Optional[str] = Field("en", description="Language code (e.g., en, es, fr)")
    limit: int = Field(10, ge=1, le=100, description="Number of results to return")


class HeadlineParams(BaseModel):
    """Query parameters for headlines fetching."""
    category: Optional[str] = Field(None, description="News category")
    country: Optional[str] = Field("us", description="Country code")
    limit: int = Field(10, ge=1, le=100, description="Number of results to return")


class SearchParams(BaseModel):
    """Query parameters for topic search."""
    country: Optional[str] = Field(None, description="Country code")
    language: Optional[str] = Field("en", description="Language code")
    limit: int = Field(10, ge=1, le=100, description="Number of results to return")


class NewsResponse(BaseModel):
    """Standard response model for news data."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    timestamp: str
    service: str
    environment: str
    newdata_service: Dict[str, Any]


class ServiceInfoResponse(BaseModel):
    """Service information response model."""
    service: str
    version: str
    description: str
    endpoints: Dict[str, str]
    documentation: str