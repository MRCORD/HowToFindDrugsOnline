from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Drug Finder API"
    PROJECT_VERSION: str = "1.0.0"
    MONGODB_CONNECTION_STRING: str = os.getenv("MONGODB_CONNECTION_STRING", "mongodb://localhost:27017")
    ALLOWED_ORIGINS: List[str] = os.getenv("CORS_ORIGINS", "http://localhost:3000,https://buscatupepa.com,http://frontend_react_service:3000").split(",")

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = True

settings = Settings()

# Print configuration for debugging (remove in production)
print("Current configuration:")
print(f"PROJECT_NAME: {settings.PROJECT_NAME}")
print(f"PROJECT_VERSION: {settings.PROJECT_VERSION}")
print(f"MONGODB_CONNECTION_STRING: {settings.MONGODB_CONNECTION_STRING}")
print(f"ALLOWED_ORIGINS: {settings.ALLOWED_ORIGINS}")