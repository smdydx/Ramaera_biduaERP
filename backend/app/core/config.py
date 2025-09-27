from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database configuration
    database_url: str = os.getenv("DATABASE_URL", "postgresql://localhost:5432/crm_hrms_db")
    database_name: str = "crm_hrms_db"
    
    # Security configuration  
    secret_key: str = "development-key-only-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Application configuration
    app_name: str = "CRM + HRMS API"
    version: str = "1.0.0"
    debug: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        
    def validate_production_settings(self):
        """Validate settings for production environment."""
        if not self.debug and self.secret_key == "development-key-only-change-in-production":
            raise ValueError("SECRET_KEY must be set in production environment")
        if not self.debug and "localhost" in self.mongodb_url:
            raise ValueError("MONGODB_URL must be set to actual database in production")

# Global settings instance
settings = Settings()