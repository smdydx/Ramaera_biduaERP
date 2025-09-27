from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection, get_database

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        await connect_to_mongo()
    except Exception as e:
        logger.error(f"Database connection failed during startup: {e}")
        # Continue without database for development
    yield
    # Shutdown
    await close_mongo_connection()

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
async def health_check(db = Depends(get_database)):
    try:
        # Test database connection
        if db is not None:
            await db.command('ping')
            db_status = "connected"
        else:
            db_status = "disconnected"
    except Exception:
        db_status = "error"
    
    return {
        "status": "healthy",
        "database": db_status,
        "database_name": settings.database_name,
        "environment": "development"
    }

# Include API routes
from app.api.v1.api import api_router
app.include_router(api_router, prefix="/api/v1")

@app.get("/api/v1/status")
async def api_status():
    return {
        "api_version": "v1",
        "modules": {
            "crm": "initialized",
            "hrms": "initialized", 
            "auth": "initialized"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)