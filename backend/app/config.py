import os
import logging
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application Configuration"""
    
    # API Configuration
    API_TITLE: str = "ADYAANANT GURUKUL - Live Leaderboard API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Read-only API for live leaderboard display"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # MongoDB Configuration
    MONGO_URI: str = os.getenv("MONGO_URI", "")
    MONGO_DB_NAME: str = "adyaanant_gurukul"
    MONGO_ACTIVE_MEMBERS_COLLECTION: str = "active_members"
    MONGO_USER_DATA_COLLECTION: str = "user_data"
    
    # CORS Configuration
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5000",
        "http://localhost:8000",
        "http://localhost:8001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5000",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8001",
        "https://*.github.io",
        "https://your-domain.com",
    ]
    
    # Logging Configuration
    LOG_LEVEL: str = logging.DEBUG if DEBUG else logging.INFO
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @classmethod
    def validate(cls) -> None:
        """Validate critical configuration"""
        if not cls.MONGO_URI:
            raise ValueError("MONGO_URI environment variable is not set")
    
    @classmethod
    def get_mongo_uri(cls) -> str:
        """Get MongoDB URI (never expose in logs)"""
        if not cls.MONGO_URI:
            raise ValueError("MongoDB URI not configured")
        return cls.MONGO_URI

settings = Settings()
settings.validate()
