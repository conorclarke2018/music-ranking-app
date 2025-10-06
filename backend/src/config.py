"""
Configuration settings for the Music Ranking App.
"""

import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import validator


class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    database_url: str = "postgresql://user:password@localhost:5432/musicrankingdb"
    
    # Application
    secret_key: str = "dev-secret-key-change-in-production"
    debug: bool = False
    node_env: str = "development"
    
    # Spotify API
    spotify_client_id: str = ""
    spotify_client_secret: str = ""
    
    # OpenAI API
    openai_api_key: str = ""
    
    # JWT
    jwt_secret_key: str = "jwt-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    allowed_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    
    # Database Pool
    db_pool_size: int = 20
    db_max_overflow: int = 0
    db_pool_recycle: int = 300
    db_pool_pre_ping: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @validator("allowed_origins")
    def parse_origins(cls, v: str) -> List[str]:
        """Parse comma-separated origins into a list."""
        return [origin.strip() for origin in v.split(",") if origin.strip()]
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.node_env.lower() in ("development", "dev")
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.node_env.lower() in ("production", "prod")


# Create global settings instance
settings = Settings()