import logging
from typing import Optional
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from app.config import settings

logger = logging.getLogger(__name__)

class MongoDBManager:
    """MongoDB Connection Manager - Read-Only Access"""
    
    _instance: Optional[MongoClient] = None
    
    @classmethod
    def get_client(cls) -> MongoClient:
        """Get MongoDB client instance (singleton pattern)"""
        if cls._instance is None:
            cls._instance = cls._create_client()
        return cls._instance
    
    @classmethod
    def _create_client(cls) -> MongoClient:
        """Create MongoDB connection"""
        try:
            logger.info("Connecting to MongoDB...")
            client = MongoClient(
                settings.get_mongo_uri(),
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000,
                socketTimeoutMS=5000,
                retryWrites=False,  # Read-only mode
                readPreference="secondaryPreferred"  # Prefer reading from secondaries
            )
            
            # Verify connection
            client.admin.command('ping')
            logger.info("✓ MongoDB connected successfully")
            return client
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"✗ Failed to connect to MongoDB: {str(e)}")
            raise
    
    @classmethod
    def get_database(cls):
        """Get database instance"""
        client = cls.get_client()
        return client[settings.MONGO_DB_NAME]
    
    @classmethod
    def get_active_members_collection(cls):
        """Get active members collection"""
        db = cls.get_database()
        return db[settings.MONGO_ACTIVE_MEMBERS_COLLECTION]
    
    @classmethod
    def get_user_data_collection(cls):
        """Get user data collection"""
        db = cls.get_database()
        return db[settings.MONGO_USER_DATA_COLLECTION]
    
    @classmethod
    def close_connection(cls) -> None:
        """Close MongoDB connection"""
        if cls._instance:
            cls._instance.close()
            cls._instance = None
            logger.info("MongoDB connection closed")
    
    @classmethod
    def health_check(cls) -> bool:
        """Check MongoDB connection health"""
        try:
            client = cls.get_client()
            client.admin.command('ping')
            return True
        except Exception as e:
            logger.error(f"MongoDB health check failed: {str(e)}")
            return False

# Singleton instance
mongodb_manager = MongoDBManager()
