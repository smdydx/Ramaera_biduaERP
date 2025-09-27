
from fastapi import APIRouter
from .endpoints import auth, users, customers, leads, employees, departments, leave_requests, attendance

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(customers.router, prefix="/customers", tags=["CRM - Customers"])
api_router.include_router(leads.router, prefix="/leads", tags=["CRM - Leads"])
api_router.include_router(employees.router, prefix="/employees", tags=["HRMS - Employees"])
api_router.include_router(departments.router, prefix="/departments", tags=["HRMS - Departments"])
api_router.include_router(leave_requests.router, prefix="/leave-requests", tags=["HRMS - Leave Requests"])
api_router.include_router(attendance.router, prefix="/attendance", tags=["HRMS - Attendance"])
