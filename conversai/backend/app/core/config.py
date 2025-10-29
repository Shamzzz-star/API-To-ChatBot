"""
Configuration management for ConversAI
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    APP_NAME: str = "ConversAI"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "sqlite:///./conversai.db"
    
    # Security
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ENCRYPTION_KEY: str = "your-encryption-key-here-32chars"
    
    # LLM Configuration (Groq Free Tier)
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.1-8b-instant"
    
    # Free API Keys
    OPENWEATHER_API_KEY: Optional[str] = None
    NEWSAPI_KEY: Optional[str] = None
    WEATHERAPI_KEY: Optional[str] = None
    GNEWS_API_KEY: Optional[str] = None
    API_NINJAS_KEY: Optional[str] = None
    COINGECKO_API_KEY: Optional[str] = None
    GITHUB_TOKEN: Optional[str] = None
    
    # Rate Limiting
    MAX_REQUESTS_PER_MINUTE: int = 60
    MAX_REQUESTS_PER_DAY: int = 1000
    
    # Cache TTL (seconds)
    CACHE_TTL_WEATHER: int = 600
    CACHE_TTL_CRYPTO: int = 60
    CACHE_TTL_NEWS: int = 1800
    CACHE_TTL_DEFAULT: int = 300
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra fields in .env that aren't defined in Settings
    
    @property
    def cors_origins_list(self) -> list[str]:
        """Convert CORS_ORIGINS string to list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


# Global settings instance
settings = Settings()
