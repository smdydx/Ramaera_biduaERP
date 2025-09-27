
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_employees():
    return {"message": "Employees endpoint - coming soon"}

@router.get("/{employee_id}")
async def get_employee(employee_id: str):
    return {"message": f"Employee {employee_id} details - coming soon"}
