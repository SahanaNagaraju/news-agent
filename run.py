#!/usr/bin/env python3
"""
Main entry point for the News Agent application.
This script starts the Uvicorn server with the FastAPI application.
"""
import uvicorn
from app.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=(settings.env == "development"),
        log_level=settings.log_level.lower()
    )