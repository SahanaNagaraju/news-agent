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
    
    # Newdata.io Configuration
    newdata_api_key: Optional[str] = None
    newdata_api_url: str = "https://api.newdata.io/v1"
    
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
        errors = []
        
        if not self.newdata_api_key:
            errors.append("NEWDATA_API_KEY is required")
        
        if errors:
            print("Configuration validation failed:")
            for error in errors:
                print(f"  - {error}")
            print("Warning: Application may not function correctly without proper configuration")
            return False
        
        return True


# Global settings instance
settings = Settings()