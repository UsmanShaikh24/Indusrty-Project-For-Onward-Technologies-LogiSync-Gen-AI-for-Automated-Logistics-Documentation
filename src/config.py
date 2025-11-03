from pydantic import BaseModel
from typing import Optional

class Settings(BaseModel):
    PROJECT_NAME: str = "LogiSync"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api/v1"
    
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "logisync"
    POSTGRES_DB: str = "logisync"
    
    # JWT settings
    JWT_SECRET_KEY: str = "your-secret-key-here"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OpenAI settings for document generation
    OPENAI_API_KEY: Optional[str] = None
    
    # Google Maps API for route optimization
    GOOGLE_MAPS_API_KEY: Optional[str] = None

settings = Settings()