from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    app_name: str = "Polymer Tracker API"
    database_url: str = "sqlite:///./polymers.db"
    secret_key: str = "your-super-secret-key-change-in-production"
    api_keys: List[str] = ["test-key-123", "dev-key-456"]
    
    class Config:
        env_file = ".env"
        extra = "allow"  # This allows extra fields in the .env file

settings = Settings()