from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import logging

from app.config import settings
from app.routes.news import router as news_router
from app.services.serpapi_service import serpapi_service
from app.models import ServiceInfoResponse, HealthResponse

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Standalone news agent with SerpAPI integration for BTP deployment",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Validate configuration on startup
@app.on_event("startup")
async def startup_event():
    """Run validation and setup on application startup."""
    logger.info("=" * 50)
    logger.info(f"{settings.app_name} starting up...")
    logger.info(f"Environment: {settings.env}")
    logger.info(f"Version: {settings.app_version}")
    
    # Validate configuration
    settings.validate_config()
    
    logger.info("Application started successfully")
    logger.info("=" * 50)


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    logger.info("Application shutting down...")


# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "message": "Internal server error",
                "details": str(exc) if settings.env == "development" else "An error occurred"
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    )


# Root endpoint
@app.get("/", response_model=ServiceInfoResponse)
async def root():
    """
    Root endpoint providing service information.
    """
    return ServiceInfoResponse(
        service=settings.app_name,
        version=settings.app_version,
        description="Standalone news agent with SerpAPI integration",
        endpoints={
            "health": "/health",
            "docs": "/docs",
            "news": "/api/news",
            "headlines": "/api/headlines",
            "search": "/api/search/{topic}",
            "query": "/api/news/query (POST)"
        },
        documentation="See /docs for interactive API documentation"
    )


# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify service status.
    """
    serpapi_health = await serpapi_service.health_check()
    
    return HealthResponse(
        status="ok",
        timestamp=datetime.utcnow().isoformat(),
        service=settings.app_name,
        environment=settings.env,
        newdata_service=serpapi_health
    )


# Include routers
app.include_router(news_router)


# 404 handler
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Handle 404 errors."""
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "error": {
                "message": "Route not found",
                "path": str(request.url)
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    )