from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional
import logging
from .config import settings

logger = logging.getLogger(__name__)

class Database:
    client: Optional[AsyncIOMotorClient] = None
    database: Optional[AsyncIOMotorDatabase] = None

db = Database()

async def connect_to_mongo():
    """Connect to MongoDB."""
    try:
        # Configure options for MongoDB Atlas
        connection_options = {
            'tls': True,
            'tlsAllowInvalidCertificates': True,  # Allow invalid certificates for development
            'tlsAllowInvalidHostnames': True,    # Allow invalid hostnames for development
            'authSource': 'admin',
            'maxPoolSize': 10,
            'minPoolSize': 1,
            'retryWrites': True,
            'w': 'majority'
        }

        db.client = AsyncIOMotorClient(
            settings.mongodb_url,
            serverSelectionTimeoutMS=5000,  # 5 second timeout
            connectTimeoutMS=5000,
            socketTimeoutMS=5000,
            **connection_options
        )
        db.database = db.client[settings.database_name]

        # Test the connection
        await db.client.admin.command('ping')
        logger.info(f"Successfully connected to MongoDB: {settings.database_name}")

        # Create indexes
        await create_indexes()

    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        if settings.debug:
            # For development, continue without database connection
            logger.warning("Running in development mode without database connection")
            db.client = None
            db.database = None
        else:
            # In production, fail fast
            raise

async def close_mongo_connection():
    """Close MongoDB connection."""
    if db.client is not None:
        db.client.close()
        logger.info("Disconnected from MongoDB")

async def get_database():
    """Get database instance for dependency injection."""
    if db.database is None:
        logger.warning("Database not connected")
        return None
    return db.database

async def create_indexes():
    """Create database indexes for optimal performance."""
    if db.database is None:
        logger.warning("Database not connected, skipping index creation")
        return

    from ..models.models import DATABASE_INDEXES

    try:
        for collection_name, indexes in DATABASE_INDEXES.items():
            collection = db.database[collection_name]
            for index_spec in indexes:
                await collection.create_index(**index_spec)
        logger.info("Database indexes created successfully")
    except Exception as e:
        logger.error(f"Failed to create database indexes: {e}")