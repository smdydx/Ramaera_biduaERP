from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from app.core.config import settings
from app.core.database import create_tables, test_connection, get_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        # Test database connection
        if test_connection():
            logger.info("Database connection successful")
            # Create all tables
            create_tables()
            logger.info("Database tables created successfully")
        else:
            logger.error("Database connection failed")
    except Exception as e:
        logger.error(f"Database startup failed: {e}")
    yield
    # Shutdown
    logger.info("Application shutdown")

app = FastAPI(
    title=settings.app_name,
    description="Professional MNC-style CRM and HRMS system",
    version=settings.version,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for Replit environment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "CRM + HRMS API is running",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check(db = Depends(get_db)):
    try:
        # Test database connection
        from sqlalchemy import text
        result = db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "error"

    return {
        "status": "healthy",
        "database": db_status,
        "database_name": settings.database_name,
        "environment": "development",
        "database_url_set": bool(settings.database_url)
    }

# Include API routes (temporarily commented for initial setup)
# from app.api.v1.api import api_router
# app.include_router(api_router, prefix="/api/v1")

@app.get("/api/v1/status")
async def api_status():
    return {
        "api_version": "v1",
        "database_connected": test_connection(),
        "modules": {
            "database": "connected" if test_connection() else "disconnected",
            "crm": "ready for implementation",
            "hrms": "ready for implementation",
            "auth": "ready for implementation"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000,
        reload=True,
        access_log=True
    )