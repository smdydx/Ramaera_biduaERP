
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_departments():
    return {"message": "Departments endpoint - coming soon"}

@router.get("/{department_id}")
async def get_department(department_id: str):
    return {"message": f"Department {department_id} details - coming soon"}
