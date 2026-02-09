from pydantic_settings import BaseSettings
from typing import Optional, List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Server Configuration
    app_name: str = "news-agent"
    app_version: str = "1.0.0"
    port: int = 8080
    host: str = "0.0.0.0"
    env: str = "production"
    log_level: str = "info"
    
    # SerpAPI Configuration
    serpapi_api_key: str = "742a92b18e3dc1a4f2205c40ec85633e8f0b1dc77caefe43a2be328036666633"
    serpapi_api_url: str = "https://serpapi.com/search.json"
    
    # CORS Configuration
    allowed_origins: str = "*"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        
    @property
    def cors_origins(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        if self.allowed_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    def validate_config(self) -> bool:
        """Validate required configuration."""
        # API key is hardcoded, no validation needed
        return True


# Global settings instance
settings = Settings()