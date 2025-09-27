from fastapi import APIRouter
from .endpoints import auth, crm, hrms, dashboard

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(crm.router, prefix="/crm", tags=["crm"])
api_router.include_router(hrms.router, prefix="/hrms", tags=["hrms"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])